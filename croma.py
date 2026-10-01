import json
import requests
from base_platform import Platform

class Croma(Platform):
    def __init__(self):
        super().__init__("Croma")
    
    def get_query(self, prompt):
        clean_prompt = prompt.replace(" ", "%20")
        self.query = f"https://api.croma.com/searchservices/v1/search?currentPage=0&query={clean_prompt}%3Arelevance&fields=FULL&channel=WEB&channelCode=400049&spellOpt=DEFAULT"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
        }
        
        response = requests.get(self.query, headers=headers)
        self.html = response.text

    def make_list_cards(self):
        try:
            data = json.loads(self.html)
            return data.get("products", [])
        except Exception:
            return []

    def get_info_card(self, card):
        try:
            title = card.get("name", "N/A")
            brand = card.get("manufacturer", title.split(" ")[0] if title != "N/A" else "N/A")
            
            price_obj = card.get("price") or card.get("pincodePrice") or {}
            selling_price = int(price_obj.get("value", 0))

            url_path = card.get("url", "")
            url = url_path if url_path.startswith("http") else f"https://www.croma.com{url_path}" if url_path else "N/A"

            image = card.get("plpImage", "N/A")

            return {
                "platform": "Croma",
                "title": title,
                "brand": brand,
                "price": selling_price,
                "url": url,
                "image": image,
            }
        except Exception:
            return None