import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI


class ChatModel(object):
    def __init__(self, verbose: bool = False):
        load_dotenv()
        self.model_name = os.getenv("LLM_MODEL_NAME")
        self.model_key = os.getenv("LLM_MODEL_KEY")
        self.verbose = verbose

    def get(self) -> BaseChatModel:
        if self.model_name == "gemini-1.5-flash":
            model = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.model_key,
                verbose=self.verbose,
            )
            return model
        return None
