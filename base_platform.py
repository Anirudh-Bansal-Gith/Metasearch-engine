class Platform:
    def __init__(self,name):
        self.name = name
        self.html = ''
        self.query = ""

    def take_format(self, query_format):
        self.query_format = query_format

    def get_query_structure(self):
        return self.query_format
    
    def get_query(self,prompt):
        raise NotImplementedError

    def make_list_cards(self) -> list:
        raise NotImplementedError

    def get_info_card(self, card):
        raise NotImplementedError

    def get_results(self):
        cards = self.make_list_cards()
        results = []
        for card in cards:
            results.append(self.get_info_card(card))
        return results

