class Item:
    def __init__(self, picture_url: str, name: str, price: float, url: str):
        self.picture_url = picture_url
        self.name = name
        self.price = price
        self.url = url
    
    def __repr__(self):
        return f"Item(picture_url={self.picture_url}, name={self.name}, price={self.price}, url={self.url})"