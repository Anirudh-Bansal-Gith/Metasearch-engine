import asyncio
from playwright.async_api import async_playwright 
import re
from bs4 import BeautifulSoup

async def get_html(prompt: str, platforms: list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        for platform in platforms:
            page = await context.new_page()
            try:
                for page_number in range(1, 4):
                    query = platform.get_query(prompt) + f"&page={page_number}"
                    await page.goto(query, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(2500)
                    platform.html += await page.content()
            finally:
                await page.close()

        await browser.close()