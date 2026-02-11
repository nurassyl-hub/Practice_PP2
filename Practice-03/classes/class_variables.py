class Dog:
    species = "Canine"
    def __init__(self, name):
        self.name = name
d = Dog("Rex")
print(d.species)