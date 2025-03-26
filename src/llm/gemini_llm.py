from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

class GeminiLLM:

    def __init__(self,api_key):
        self.api_key=api_key

    def get_llm_model(self):
        try:
            if not self.api_key:
                load_dotenv()
                self.api_key= os.environ["GEMINI_API_KEY"]

            llm = ChatGoogleGenerativeAI(
                api_key =self.api_key, 
                model="gemini-2.0-flash-exp",
                streaming=True,
                temperature=0
                )
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return llm