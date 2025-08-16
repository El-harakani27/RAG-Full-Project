from .LLMEnum import LLMEnum
from .providers.CohereProvider import CoHereProvider
from .providers.OpenAIProvider import OpenAIProvider
class LLMProviderFactory:
    def __init__(self,config:dict):
        self.config = config
    def create(self,provider:str):
        if provider == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key= self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                defaut_generation_max_output_tokens=self.config.DEFAULT_GENERATATION_OUTPUT_TOKENS,
                default_temprature=self.config.DEFAULT_TEMPRATURE,
            )
        if provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key= self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                defaut_generation_max_output_tokens=self.config.DEFAULT_GENERATATION_OUTPUT_TOKENS,
                default_temprature=self.config.DEFAULT_TEMPRATURE,
            )            
        return None