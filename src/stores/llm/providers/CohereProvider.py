import logging

import cohere

from ..LLMEnums import CohereEnums, DocumentType
from ..LLMInterface import LLMInterface


class CohereProvider(LLMInterface):

    def __init__(self,
                api_key:str,
                default_input_max_char:int=1000,
                default_generation_max_out_tokens:int= 1000,
                default_generation_temperature:float= 0.1 ):

        self.api_key=api_key
        self.default_input_max_char=default_input_max_char
        self.default_generation_max_out_tokens=default_generation_max_out_tokens
        self.default_generation_temperature=default_generation_temperature
        self.generation_model_id= None
        self.embedding_model_id = None
        self.embedding_model_size= None

        self.client = cohere.ClientV2(api_key = self.api_key)
        self.logger = logging.getLogger(__name__)

    def set_generatoin_model(self, model_id:str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id:str, embedding_size:int):
        self.embedding_model_id= model_id
        self.embedding_model_size = embedding_size

    def generate_text(self, prompt:str,chat_history: list=[], max_output_tokens:int=None, temperature:float= None):
        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None

        if not self.generation_model_id:
            self.logger.error("No generation model id is set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_out_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=CohereEnums.USER.value)
        )

        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            temperature=temperature,
            max_tokens=self.default_generation_max_out_tokens
        )

        if not response or not getattr(response, "message", None):
            self.logger.error("No response or missing message object")
            return None

        content_blocks = getattr(response.message, "content", [])
        if not content_blocks or not hasattr(content_blocks[0], "text"):
            self.logger.error("No text content in response")
            return None

        return content_blocks[0].text

    def process_text(self, text:str):
        return text[:self.default_input_max_char].strip()


    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Cohere client is not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("No embedding model id is set")
            return None

        try:
            if document_type == DocumentType.DOCUMENT.value:
                input_type = CohereEnums.DOCUMENT.value
            elif document_type == DocumentType.QUERY.value:
                input_type = CohereEnums.QUERY.value
            else:
                input_type = None

            response: cohere.EmbedByTypeResponse = self.client.embed(
                model=self.embedding_model_id,
                texts=[self.process_text(text)],   # Cohere expects list[str]
                input_type=input_type,
                embedding_types=["float"]          # must be a list of strings, not Python types
            )
        except Exception as e:
            self.logger.error(f"Error during embedding: {e}")
            return None

        if not response or not response.embeddings:
            self.logger.error("No embeddings returned")
            return None

        return response.embeddings["float"] # type: ignore

    def construct_prompt(self, prompt:str, role:str):
        return({
            "role":role,
            "content":self.process_text(prompt)
        })

