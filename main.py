import asyncio

from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from dotenv import load_dotenv

load_dotenv()
from browser_use import Agent
from langchain_openai import AzureChatOpenAI

task = """
   ### Prompt for Read Assignment Confirmations
   
**Objective:**
Visit [Read Assignments](https://zdi-wiki.zeiss.com/users/readack/view.action), identify all pending read assignments. 
Go to each of them by visiting the linked page and confirm that the page has been read by clicking the confirm button 
on the bottom.
Sign in before if necessary.
---

### Step 1: Navigate to the website
- [Read Assignments](https://zdi-wiki.zeiss.com/users/readack/view.action).
- If not logged in already, sign in as x_username.
---

### Step 2: Confirm pending read assignments
For each item in the table of pending read assignments
  - Open the page
  - Scroll down to the "Confirm" link at the bottom of the page
  - Click on the "Confirm" link and the OK button that pops up
If there aren't any items, proceed to step 3.
---

### Step 3: Output Summary
- Once all pending read assignments have been confirmed, output a summary including:
  - **List of pending read assignments** (if any).
  - **Info text if there weren't any pending read assignments**.
"""
model = AzureChatOpenAI(azure_deployment="gpt-4o-2024-08-06",
                        api_version="2024-09-01-preview",
                        model="gpt-4o-2024-08-06")

browser=Browser()

async def main():
    agent = Agent(
        task=task,
        llm=model,
        sensitive_data={"x_username": "stefan.bley@zeiss.com"},
        browser_context=BrowserContext(browser=browser, config=BrowserContextConfig(
            allowed_domains=['microsoftonline.com', 'zeiss.com'])),
        # Workaround for https://github.com/browser-use/browser-use/issues/1578
        tool_calling_method="function_calling"
    )
    await agent.run()
    input('Press Enter to close the browser...')
    await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
