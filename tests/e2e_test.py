from tests.base import BasePytestBrowserTest
from src.models.checkout_results import CheckoutResult
from src.models.wkipedia_results import WikipediaResult
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext

import pytest
class Test(BasePytestBrowserTest):
        
    @pytest.mark.asyncio
    async def test_wikipedia_flow(self, sample_fixture):
        output_path = './output/TC_02_test_result.json'
        report_name = "./output/TC_02.pdf"
        test_case_file = './test_cases/tc_02_wikipedia_validation.feature'        
        controller = Controller(output_model=WikipediaResult)
        history = await self.run_flow(controller,test_case_file)
        test_result = history.final_result()
        result = WikipediaResult.model_validate_json(test_result)
        assert result.page_header in "Artificial intelligence"
        self.save_report(history,output_path,WikipediaResult,report_name)

    @pytest.mark.asyncio
    async def test_shopping_cart_flow(self, sample_fixture):
        output_path = './output/TC_01_test_result.json'
        report_name = "./output/TC_01.pdf"
        test_case_file = "./test_cases/tc_0001_ui_flow.feature"

        controller = Controller(output_model=CheckoutResult)
        @controller.action(description='Get attribute and url of the page')
        async def get_attr_url(browser: BrowserContext):
            page = await browser.get_current_page()
            url = page.url
            attr = await page.get_by_text('Shop Name').get_attribute('class')
            print("Controller action called")
            print(url)
            return ActionResult(extracted_content=f"url is {url} and attribute is {attr}")


        controller = Controller(output_model=CheckoutResult)
        history = await self.run_flow(controller,test_case_file)
        test_result = history.final_result()
        result = CheckoutResult.model_validate_json(test_result)

        assert result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-)."
        self.save_report(history,output_path,CheckoutResult,report_name)