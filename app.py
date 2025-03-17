from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from pydantic import BaseModel
from browser_use import Controller,ActionResult
from playwright.async_api import BrowserContext

load_dotenv()
gemini_api_key = os.environ["GEMINI_API_KEY"]

task =(
    'I am UI automation tester validating the tasks'
    'open the website url "https://rahulshettyacademy.com/loginpagePractise/"'
    'Login with username and password, Login details available in the same page'
    'Get attribute and url of the page'
    'After login, select first 2 products and them to cart'
    'Then checkout and store the total value you see on the screen'
    'Increase the quantity of any product and check if total value is updated accordingly'
    'checkout and select country, agree terms and purchase'
    'verify thank you message is displayed'
)


class CheckoutResult(BaseModel):
    login_status:str
    cart_status: str
    checkout_status:str
    total_update_status:str
    delivery_location_status:str
    confirmation_message:str
    url: str

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



llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key =gemini_api_key)
#task="Compare the price of gpt-4o and DeepSeek-V3"
async def main():
    agent = Agent(
        task= task,
        llm=llm,
        controller=controller
        #,use_vision = true
    )
    history = await agent.run()
    history.save_to_file('result.json')
    test_result = history.final_result()
    result = CheckoutResult.model_validate_json(test_result)
    print(test_result)
    assert result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-)."
asyncio.run(main())

import json
from fpdf import FPDF

# Load JSON data
with open('result.json', 'r') as json_file:
    data = json.load(json_file)

# Initialize PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Write JSON data to PDF
for key, value in data.items():
    pdf.cell(0, 10, f"{key}: {value}", ln=True)

# Save the PDF
pdf.output("output.pdf")

print("PDF has been created successfully!")
