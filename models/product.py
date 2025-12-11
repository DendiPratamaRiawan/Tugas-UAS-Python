class Product:
    def __init__(self, id, name, category, price):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

    def display(self):
        print(f"[{self.id}] {self.name} - {self.category} - Rp{self.price}")
