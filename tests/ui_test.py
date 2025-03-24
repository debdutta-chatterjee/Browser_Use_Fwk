import pytest
from src.util.file_util import FileUtil
from src.llm.gemini_llm import GeminiLLM
from src.agent.browser_use_agent import BrowserAgent
from dotenv import load_dotenv
import os 
from browser_use import Controller,ActionResult
from pydantic import BaseModel
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import BaseModel
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext

class CheckoutResult(BaseModel):
    login_status:str
    cart_status: str
    checkout_status:str
    total_update_status:str
    delivery_location_status:str
    confirmation_message:str
    url: str


def test_ui_flow(sample_fixture):
    
    file_content = FileUtil.read_file_to_string("./test_cases/tc_0001_ui_flow.feature")
    print(file_content)

    steps = FileUtil.extract_steps(file_content)
    print(steps)

    load_dotenv()
    gemini_api_key = os.environ["GEMINI_API_KEY"]
    gemini =GeminiLLM(gemini_api_key)
    llm = gemini.get_llm_model

    
    controller = Controller(output_model=CheckoutResult)
    
    @controller.action(description='open the website url')
    async def open_website(browser: BrowserContext):
        page = await browser.get_current_page()
        await page.goto("https://rahulshettyacademy.com/loginpagePractise/")
        return ActionResult(extracted_content="Navigated to url")

    @controller.action(description='Get attribute and url of the page')
    async def get_attr_url(browser: BrowserContext):
        page = await browser.get_current_page()
        url = page.url
        attr = await page.get_by_text('Shop Name').get_attribute('class')
        print(url)
        return ActionResult(extracted_content="url is {url} and attribute is {attr}")
    
    browser_use = BrowserAgent(steps,controller,llm)
    agent = browser_use.get_agent()

    print("\nExecuting test case")
    assert 2 + 2 == 4  # Example assertion