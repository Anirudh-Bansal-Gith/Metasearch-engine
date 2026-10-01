from base_platform import Platform
import re
from bs4 import BeautifulSoup

class Flipkart(Platform):
    def __init__(self):
        super().__init__("Flipkart")

    def get_query(self,prompt):
        prompt = prompt.replace(" ", "+")
        self.query = f"https://www.flipkart.com/search?q= {prompt}"
        return self.query

    def make_list_cards(self) -> list:
        soup = BeautifulSoup(self.html, 'html.parser')
        cards = soup.find_all("div", attrs={"data-id": True})
        return cards
    
    def get_info_card(self, card):
        try:

            img = card.find("img")
            title = ""
            image = ""
            if img:
                title = img.get("alt") or img.get("title") or ""
                image = img.get("src") or img.get("data-src") or ""


            if not title:
                title_elem = card.find("div", class_=re.compile(r"wjcEIp|KzDlHZ|col"))
                title = title_elem.text.strip() if title_elem else "Product"

            anchor = card if card.name == "a" else card.find("a")
            href = anchor.get("href", "") if anchor else ""
            url = ("https://www.flipkart.com" + href) if href else ""


            selling_price = None
            price_element = card.find(lambda tag: tag.name == "div" and "₹" in tag.text)
            if price_element:
                prices = re.findall(r"₹[\d,]+", price_element.text.strip())
                if prices:
                    selling_price = int(
                        prices[0].replace("₹", "").replace(",", "")
                    )

            specs = [item.text.strip() for item in card.find_all("li")]


            return {
                "platform": "Flipkart",
                "title": title,
                "brand": title.split(' ')[0] if title else "Unknown" ,
                "specs": specs,
                "price": selling_price,
                "url": url,
                "image": image,
            }

        except Exception as e:
            print(f"Error parsing Flipkart card: {e}")
            return None