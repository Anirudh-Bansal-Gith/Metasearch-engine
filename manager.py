import asyncio
from playwright.async_api import async_playwright

async def scrape_single_platform(context, platform, prompt: str):
    page = await context.new_page()
    try:
        # Fetch page 1 (or expand range(1, 2) to range(1, 3) if more results are needed)
        for page_number in range(1, 2):
            query = platform.get_query(prompt) + f"&page={page_number}"
            await page.goto(query, wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_timeout(1000)
            platform.html += await page.content()
    finally:
        await page.close()

async def get_html(prompt: str, platforms: list):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        # Block server-side asset downloads to save CPU and bandwidth
        await context.route(
            "**/*",
            lambda route: (
                route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"]
                else route.continue_()
            )
        )

        # Run scraping concurrently across all requested platforms
        tasks = [scrape_single_platform(context, platform, prompt) for platform in platforms]
        await asyncio.gather(*tasks)

        await browser.close()