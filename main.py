class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_info(self):
        print("Pet Information:")
        print(f"   Name: {self.name}")
        print(f"   Age: {self.age}")


class Cat(Pet):
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed


pet_name = input()
pet_age = int(input())
cat_name = input()
cat_age = int(input())
cat_breed = input()

pet = Pet(pet_name, pet_age)
cat = Cat(cat_name, cat_age, cat_breed)

pet.print_info()
cat.print_info()
print(f"   Breed: {cat.breed}")
