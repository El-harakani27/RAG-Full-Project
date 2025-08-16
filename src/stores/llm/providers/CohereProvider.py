from ..LLMinterface import LLMinterface
from ..LLMEnum import CoHereEnums, DocumentTypeEnum
import logging 
import cohere
class CoHereProvider(LLMinterface):
    def __init__(self,api_key:str,default_input_max_characters:int=1000,default_generation_max_output_tokens:int = 1000,default_temprature:float=0.1):
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_temprature = default_temprature

        self.generate_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(
            api_key=self.api_key
        )    
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generate_model_id = model_id
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
    
    def process_text(self,text:str):
        return text[:self.default_input_max_characters]
    def generate_text(self, prompt: str, chat_history: list =[], max_output_tokens: int = None, temprature: float = None):
        
        if not self.client:
            self.logger.error("Error with creating CoHere client")
            return None
        if not self.generate_model_id:
            self.logger.error("Error no Model id inserted")
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temprature = temprature if temprature else self.default_temprature
        response = self.client.chat(
            model = self.generate_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            max_tokens= max_output_tokens,
            temperature = temprature 
        )
        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None

        return response.text

    def embed_text(self, text: str, document_type: str = None):
        if not self.client:
            self.logger.error("Error with creating CoHere client")
            return None
        if not self.embedding_model_id:
            self.logger.error("Error no Embedding id inserted")
        
        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnums.QUERY.value
        response = self.client.embed(
            input_type= input_type,
            model= self.embedding_model_id,
            texts = [self.process_text(text)],
            embedding_types=['float']  
        )
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error While embedding text with cohere")
            return None
        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        return {'role':role,'content':prompt}