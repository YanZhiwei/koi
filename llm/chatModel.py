import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI


class ChatModel(object):
    def __init__(self, verbose: bool = False):
        load_dotenv()
        self.model_name = os.getenv("LLM_MODEL_NAME")
        self.model_key = os.getenv("LLM_MODEL_KEY")
        self.model_url = os.getenv("LLM_MODEL_URL")
        self.verbose = verbose

    def get(self) -> BaseChatModel:
        if self.model_name == "gemini-1.5-flash" or self.model_name == "gemini-1.5-pro":
            model = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.model_key,
                verbose=self.verbose,
            )
            return model
        elif self.model_name == "gpt-4o":
            model = OpenAI(
                model=self.model_name,
                base_url=self.model_url,
                api_key=self.model_key,
            )
            return model
        return None
