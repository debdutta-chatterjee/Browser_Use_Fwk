import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self,api_key):
        self.api_key=api_key

    def get_llm_model(self):
        try:            
            if not self.api_key:
                load_dotenv()
                self.api_key= os.environ["GROQ_API_KEY"]

            llm = ChatGroq(
                api_key =self.api_key, 
                model="qwen-2.5-32b",
                streaming=True,
                temperature=0
                )
        except Exception as e:
            raise ValueError(f"Error Occurred with Exception : {e}")
        return llm