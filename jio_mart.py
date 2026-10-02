import json
import requests
from base_platform import Platform

class JioMart(Platform):
    def __init__(self):
        super().__init__("JioMart")

    def get_query(self, prompt):
        clean_prompt = prompt.replace(" ", "%20")
        
        pincode = "160047"  
        self.query = f"https://www.jiomart.com/ext/vertex/application/api/v1.0/products?f=journey%3Astandard&page_id=%2A&page_size=50&q={clean_prompt}&pincode={pincode}"
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'x-currency-code': 'INR',
            'x-location-detail': f'{{"pincode":"{pincode}"}}'
        }
        
        response = requests.get(self.query, headers=headers)
        self.html = response.text
        
    def make_list_cards(self):
        try:
            data = json.loads(self.html)
            return data.get("data", []) or data.get("items", []) or data.get("products", [])
        except Exception:
            return []

    def get_info_card(self, card):
        try:
            title = card.get("name") or card.get("display_name") or "N/A"
            brand = card.get("brand") or (title.split(" ")[0] if title != "N/A" else "N/A")
            
            price_info = card.get("price", {})
            price = int(price_info.get("selling_price") or price_info.get("mrp") or 0)
            
            slug = card.get("url_path") or card.get("slug") or ""
            url = f"https://www.jiomart.com/{slug.lstrip('/')}" if slug else "N/A"
            
            images = card.get("images", [])
            image = images[0].get("url") if images and isinstance(images[0], dict) else card.get("image_url", "N/A")

            return {
                "platform": "JioMart",
                "title": title,
                "brand": brand,
                "price": price,
                "url": url,
                "image": image,
            }
        except Exception:
            return None