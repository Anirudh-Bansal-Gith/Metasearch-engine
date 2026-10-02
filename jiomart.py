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
            # 1. Title
            title = card.get("name") or "N/A"

            # 2. Brand
            brand_data = card.get("brand")
            if isinstance(brand_data, dict):
                brand = brand_data.get("name", "Generic")
            elif isinstance(brand_data, str):
                brand = brand_data
            else:
                brand = title.split()[0] if title != "N/A" else "Generic"

            # 3. Price
            price_info = card.get("price") or {}
            effective_price = price_info.get("effective", {})
            marked_price = price_info.get("marked", {})
            
            price_val = effective_price.get("min") or marked_price.get("min") or 0
            price = int(price_val)

            # 4. URL
            slug = card.get("slug", "")
            url = f"https://www.jiomart.com/{slug.lstrip('/')}" if slug else "N/A"

            # 5. Image
            medias = card.get("medias") or []
            image = "N/A"
            if isinstance(medias, list) and len(medias) > 0:
                first_media = medias[0]
                if isinstance(first_media, dict):
                    image = first_media.get("url", "N/A")

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