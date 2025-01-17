class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        print(f"Hello, my name is {self.name} and im {self.age} years old")

person1 = Person("Asael", 26)

print(person1.age)
print(person1.name)
person1.greet()