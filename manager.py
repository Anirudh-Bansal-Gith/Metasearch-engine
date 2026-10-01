import asyncio
from playwright.async_api import async_playwright 
import re
from bs4 import BeautifulSoup





async def get_html(prompt:str,platforms:list):

    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        
        for platform in platforms:
            query = platform.get_query(prompt)
            page = await context.new_page()
            for page_number in range(1, 4):  # Fetches pages 1, 2, and 3
                query = platform.get_query(prompt) + f"&page={page_number}"
                await page.goto(query, wait_until="domcontentloaded")
                await page.wait_for_timeout(2500)

                platform.html += await page.content()
        await page.close()