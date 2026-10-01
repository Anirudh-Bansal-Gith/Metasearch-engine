# Multi-Platform Product Search Engine

A full-stack product aggregation engine built with FastAPI and vanilla JavaScript. The application simultaneously queries multiple e-commerce platforms (Amazon, Flipkart, and Croma), standardizes heterogeneous search data into a uniform schema, and serves real-time pricing and product comparisons.

---

## Architecture Overview

E-commerce platforms employ vastly different anti-bot measures, network topologies, and rendering pipelines. To maximize throughput and reliability, the backend uses a hybrid data extraction architecture:

* **Direct API Ingestion (Croma):** Directly queries internal JSON search endpoints via standard HTTP requests, bypassing heavy frontend browser automation entirely.
* **Headless Browser Automation (Amazon & Flipkart):** Uses Playwright to render JavaScript-heavy frontend layouts and bypass strict client-side verification barriers.
* **Unified OOP Schema:** Regardless of whether the raw payload is rendered HTML or a JSON string, all platform scrapers inherit from an abstract `Platform` base class to enforce a consistent product representation across the entire pipeline.

---

## Directory Structure

```text
├── index.html         # Frontend interface
├── style.css          # UI styles & product card layout
├── script.js          # Client-side filtering, sorting, and API bindings
├── main.py            # FastAPI server and routing entry point
├── manager.py         # Headless browser (Playwright) lifecycle management
├── base_platform.py   # Abstract base class for platform scrapers
└── platforms/
    ├── amazon.py      # Amazon extraction logic
    ├── flipkart.py    # Flipkart extraction logic
    └── croma.py       # Croma API integration and adapter logic
```

---

## Tech Stack

* **Backend:** Python 3.12+, FastAPI, Uvicorn
* **Scraping & Automation:** Playwright, BeautifulSoup4, Requests
* **Frontend:** Vanilla JavaScript (ES6+), HTML5, CSS3

---

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.12+ installed. Set up and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install fastapi uvicorn requests beautifulsoup4 playwright
playwright install chromium
```

### 3. Start the Backend Server

Launch the FastAPI application on port `8000`:

```bash
uvicorn main:app --reload --port 8000
```

The API endpoints will be accessible at `[http://127.0.0.1:8000](http://127.0.0.1:8000)`.

### 4. Serve the Frontend

Modern web browsers block cross-origin requests from raw `file:///` URLs. Serve the frontend directory using Python's built-in HTTP server on a separate port:

```bash
# In the directory containing index.html, style.css, and script.js
python3 -m http.server 5500
```

Navigate to `http://localhost:5500` in your browser.

---

## API Reference

### Search Products

Retrieves matching products across selected platforms.

* **Endpoint:** `GET /search`
* **Query Parameters:**
  * `query` (string, required): Product search terms (e.g., `samsung galaxy`, `laptop`).
  * `platforms` (list of strings, optional): Targets specific platforms. Supported options: `all`, `croma`, `amazon`, `flipkart`. Default: `["all"]`.

#### Example Request
```http
GET /search?query=samsung&platforms=croma&platforms=amazon HTTP/1.1
Host: 127.0.0.1:8000
```

#### Example Response
```json
[
  {
    "platform": "Croma",
    "title": "Samsung Galaxy S23 5G (128GB, Phantom Black)",
    "brand": "Samsung",
    "price": 54999,
    "url": "https://www.croma.com/samsung-galaxy-s23-5g...",
    "image": "https://media-ik.croma.com/prod/https://media.croma.com/..."
  },
  {
    "platform": "Amazon",
    "title": "Samsung Galaxy S23 5G (Phantom Black, 8GB, 128GB Storage)",
    "brand": "Samsung",
    "price": 52999,
    "url": "https://www.amazon.in/dp/...",
    "image": "https://m.media-amazon.com/images/I/..."
  }
]
```

---

## Extending Platforms

To add a new e-commerce provider, inherit from `Platform` in `base_platform.py` and implement the extraction methods:

```python
from base_platform import Platform

class NewStore(Platform):
    def __init__(self):
        super().__init__("NewStore")

    def get_query(self, prompt: str):
        # Build search URL and fetch raw payload
        ...

    def make_list_cards(self):
        # Extract product elements or JSON nodes
        ...

    def get_info_card(self, card):
        # Return standardized dictionary: title, brand, price, url, image
        ...
```

Register your new platform class inside `PLATFORM_MAP` in `main.py`.
