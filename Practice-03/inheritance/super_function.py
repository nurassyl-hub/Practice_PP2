class Parent:
    def __init__(self, n): self.name = n
class Child(Parent):
    def __init__(self, n, g):
        super().__init__(n)
        self.grade = g
s = Child("Leo", "A")
print(s.name)