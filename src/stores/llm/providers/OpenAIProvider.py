import logging
from typing import List

from openai import OpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse

from ..LLMEnums import OpenAIEnums
from ..LLMInterface import LLMInterface


class OpenAIProvider(LLMInterface):

    def __init__(self,
                api_key:str,
                api_url:str=None,
                default_input_max_char:int=1000,
                default_generation_max_out_tokens:int= 1000,
                default_generation_temperature:float= 0.1 ):

        self.api_key=api_key
        self.api_url=api_url
        self.default_input_max_char=default_input_max_char
        self.default_generation_max_out_tokens=default_generation_max_out_tokens
        self.default_generation_temperature=default_generation_temperature
        self.generation_model_id= None
        self.embedding_model_id = None
        self.embedding_model_size= None

        self.client = OpenAI(api_key = self.api_key, base_url = self.api_url)
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
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        response = self.client.chat.completions.create(model=self.generation_model_id,
                                                  messages=chat_history,
                                                  temperature=temperature,
                                                  max_completion_tokens=self.default_generation_max_out_tokens)
        if not response or response.choices or len(response.choices)==0 or not response.choices[0].message:
            self.logger.error("there was an error in the generation")
            return None
        return response.choices[0].message.content

    def process_text(self, text:str):
        return text[:self.default_input_max_char].strip()


    def embed_text(self, text: str, document_type: str=None) -> List[float] | None:
        if not self.client:
            self.logger.error("OpenAI client is not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("No embedding model id is set")
            return None

        response: CreateEmbeddingResponse = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("There was an error while embedding the data")
            return None

        return response.data[0].embedding


    def construct_prompt(self, prompt:str, role:str):
        return({
            "role":role,
            "content":self.process_text(prompt)
        })

