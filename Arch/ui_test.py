import pytest
from src.util.file_util import FileUtil
from src.llm.gemini_llm import GeminiLLM
from src.agent.browser_use_agent import BrowserAgent
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext
from src.models.checkout_results import CheckoutResult
from src.models.wkipedia_results import WikipediaResult
from src.util.result_handler import ResultHandler
from src.util.report_util import ReportUtil
from pydantic import BaseModel

@pytest.mark.asyncio
async def test_002_wikipedia_flow(sample_fixture):
    
    file_content = FileUtil.read_file_to_string("./test_cases/tc_02_wikipedia_validation.feature")
    task = FileUtil.extract_steps(file_content)     
    llm = GeminiLLM("").get_llm_model()

    controller = Controller(output_model=WikipediaResult)

    agent = BrowserAgent(task,controller,llm).get_agent()
    history = await agent.run()
    result = ResultHandler.save_result(history, './output/TC_02_test_result.json', WikipediaResult)
    ReportUtil.generate_pdf_from_json_file('./output/TC_02_test_result.json',"TC_02.pdf")
    assert result.total_refences > 100

@pytest.mark.asyncio
async def test_001_shopping_cart_flow(sample_fixture):
    
    file_content = FileUtil.read_file_to_string("./test_cases/tc_0001_ui_flow.feature")
    task = FileUtil.extract_steps(file_content)     
    llm = GeminiLLM("").get_llm_model()

    controller = Controller(output_model=CheckoutResult)

    @controller.action(description='Get attribute and url of the page')
    async def get_attr_url(browser: BrowserContext):
        page = await browser.get_current_page()
        url = page.url
        attr = await page.get_by_text('Shop Name').get_attribute('class')
        print("Controller action called")
        print(url)
        return ActionResult(extracted_content="url is {url} and attribute is {attr}")
    
    agent = BrowserAgent(task,controller,llm).get_agent()
    history = await agent.run()
    result = ResultHandler.save_result(history, './output/TC_01_test_result.json', CheckoutResult)
    ReportUtil.generate_pdf_from_json_file('./output/TC_01_test_result.json',"TC_01.pdf")
    assert result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-)."
