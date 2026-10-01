import re
from bs4 import BeautifulSoup
from base_platform import Platform

class Amazon(Platform):
    def __init__(self):
        super().__init__("Amazon")
    
    def get_query(self,prompt):
        prompt = prompt.replace(" ", "+")
        self.query = f"https://www.amazon.in/s?k={prompt}"
        return self.query

    def make_list_cards(self) -> list:
        soup = BeautifulSoup(self.html, 'html.parser')
        valid_cards = []
        for card in soup.find_all("div", attrs={"data-asin": True}):
            asin = card.get("data-asin", "").strip()
            if asin and card.find("h2"):
                valid_cards.append(card)
        return valid_cards

    def get_info_card(self, card):
        try:
            h2_tags = card.find_all("h2")
            if h2_tags:
                title = h2_tags[-1].text.strip()
                k =title.split('|')
                title = k[0]
            else:
                title = "N/A"

            link = card.find("a", class_="a-link-normal", href=True)
            if link and link["href"]:
                href = link["href"]
                url = href if href.startswith("http") else f"https://www.amazon.in{href}"
            else:
                url = "N/A"

            whole = card.find("span", class_="a-price-whole")
            if whole:
                clean_digits = re.sub(r"[^\d]", "", whole.text)
                selling_price = int(clean_digits) if clean_digits else 0
            else:
                selling_price = 0

            specs = k[1:]

            image = card.find("img")["src"] 
            return {
                'platform':'Amazon',
                'title': title,
                "brand": title.split(' ')[0],
                'price': selling_price,
                'url': url,
                'image': image
            }
        except:
            return None