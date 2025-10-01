from ..LLMEnums import LLMEnums
from .CohereProvider import CohereProvider
from .OpenAIProvider import OpenAIProvider


class LLMProviderFactory():
    def __init__(self,config) -> None:
        self.config = config

    def create_provider(self,provider_type:str) -> CohereProvider | OpenAIProvider | None:
        if provider_type == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_char=self.config.DEFAULT_INPUT_MAX_TOKENS,
                default_generation_max_out_tokens=self.config.DEFAULT_OUTPUT_MAX_TOKENS,
                default_generation_temperature=self.config.OPENAI_TEMPERATURE
            )
        elif provider_type == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_BASE_URL,
                default_input_max_char=self.config.DEFAULT_INPUT_MAX_TOKENS,
                default_generation_max_out_tokens=self.config.DEFAULT_OUTPUT_MAX_TOKENS,
                default_generation_temperature=self.config.OPENAI_TEMPERATURE
            )
        else:
            return None
