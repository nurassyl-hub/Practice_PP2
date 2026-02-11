class Bird:
    def fly(self): print("Flying")
class Penguin(Bird):
    def fly(self): print("Swimming instead")
p = Penguin()
p.fly()