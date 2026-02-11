class Animal:
    def speak(self): print("Sound")
class Dog(Animal):
    def bark(self): print("Woof")
d = Dog()
d.speak()