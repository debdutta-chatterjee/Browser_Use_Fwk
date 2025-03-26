import os
import sys
from pathlib import Path
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

import pyperclip
from langchain_openai import ChatOpenAI

from browser_use import Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		headless=False,
	)
)
controller = Controller()


@controller.registry.action('Copy text to clipboard')
def copy_to_clipboard(text: str):
	pyperclip.copy(text)
	print("copy_to_clipboard*****************************")
	return ActionResult(extracted_content=text)


@controller.registry.action('Paste text from clipboard')
async def paste_from_clipboard(browser: BrowserContext):
	print("paste_from_clipboard*****************************")
	text = pyperclip.paste()
	# send text to browser
	page = await browser.get_current_page()
	await page.keyboard.type(text)

	return ActionResult(extracted_content=text)


async def main():
	gemini_api_key="AIzaSyCtTc-rIeCTfJsfIMHFqnSIjhPbSJpy5Yc"
	task = f'Copy the text "Hello, world!" to the clipboard, then go to google.com and paste the text'
	model = llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key =gemini_api_key)

	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())