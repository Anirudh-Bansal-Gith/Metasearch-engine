import asyncio
from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from amazon import Amazon
from base_platform import Platform
from flipkart import Flipkart
from croma import Croma
from manager import get_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PLATFORM_MAP = {"amazon": Amazon, "flipkart": Flipkart}

@app.get("/search")
async def search(query: str, platforms: Optional[List[str]] = Query(default=["all"])) :
    selected = [p.lower() for p in platforms]

    results = []
    if "all" in selected or "croma" in selected:
        croma = Croma()
        croma.get_query(query)
        results.extend(croma.get_results())
        
    if not selected or "all" in selected:
        playwright_platforms = [class_obj() for class_obj in PLATFORM_MAP.values()]
    else:
        playwright_platforms = [PLATFORM_MAP[value]() for value in selected if value in PLATFORM_MAP]

    if playwright_platforms:
        await get_html(query, playwright_platforms)
        
        for platform in playwright_platforms:
            results.extend(platform.get_results())

    return results

    


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)