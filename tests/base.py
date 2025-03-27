import pytest
from src.util.file_util import FileUtil
from src.llm.gemini_llm import GeminiLLM
from src.llm.groq_llm import GroqLLM
from src.agent.browser_use_agent import BrowserAgent
from browser_use import Controller
from playwright.async_api import BrowserContext
from src.util.result_handler import ResultHandler
from src.util.report_util import ReportUtil
from pydantic import BaseModel
from typing import Type

class BasePytestBrowserTest:
   
    async def run_flow(
            self,
            controller,
            test_case_file            
            ):
        
        file_content = FileUtil.read_file_to_string(test_case_file)
        task = FileUtil.extract_steps(file_content)
        llm = GeminiLLM("").get_llm_model()
        #llm = GroqLLM("").get_llm_model()
        
        agent = BrowserAgent(task, controller, llm).get_agent()
        history = await agent.run()
        return history

    def setup_controller(self, class_model):
        """Override this method in subclasses to add custom controller actions."""
        return Controller(output_model=class_model)
    
    def save_report(self, history, output_path, output_model,report_name):
        result = ResultHandler.save_result(history, output_path, output_model)
        ReportUtil.generate_pdf_from_json_file(output_path, report_name)
        return result