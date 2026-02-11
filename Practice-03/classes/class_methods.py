class Car:
    def __init__(self, b, m):
        self.brand = b
        self.model = m
    def display(self):
        print(f"{self.brand} {self.model}")
c = Car("Tesla", "S")
c.display()