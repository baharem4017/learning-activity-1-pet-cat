import sys

from validation import validate_text, validate_integer
from age_utils import format_age
from breed_service import validate_breed, BreedServiceError


class Pet:
    def __init__(self, name, age, age_months=0):
        self.name = name
        self.age = age
        self.age_months = age_months

    def print_info(self):
        print("Pet Information:")
        print(f"   Name: {self.name}")
        print(f"   Age: {format_age(self.age, self.age_months)}")


class Cat(Pet):
    def __init__(self, name, age, breed, age_months=0):
        self.name = name
        self.age = age
        self.age_months = age_months
        self.breed = breed


class IncompleteInputError(Exception):
    pass


class ReturnToMenu(Exception):
    pass


def read_line(field):
    try:
        return input(f"{field}: ")
    except EOFError:
        raise IncompleteInputError(field) from None


def read_interactive_field(field, validator):
    while True:
        raw = read_line(field)

        try:
            return validator(raw, field)
        except ValueError as error:
            print(error)


def read_interactive_age(pet_label):
    while True:
        years = read_interactive_field(
            f"{pet_label} age in years",
            validate_integer
        )

        months = read_interactive_field(
            f"{pet_label} additional months",
            validate_integer
        )

        if months <= 11:
            return years, months

        print(
            f"Error: {pet_label} additional months "
            "must be between 0 and 11."
        )
        print(
            "Help: Enter completed years and remaining months; "
            "for 15 months, use 1 year and 3 months."
        )


def choose_service_recovery():
    while True:
        print()
        print("1. Retry online verification")
        print("2. Return to the main menu")

        choice = read_line("Choose an option (1-2)").strip()

        if choice in ("1", "2"):
            return choice

        print("Error: Menu choice must be 1 or 2.")
        print(
            "Help: Enter 1 to retry "
            "or 2 to return to the main menu."
        )


def read_cat_breed():
    while True:
        raw = read_line("Cat breed")

        while True:
            try:
                return validate_breed(raw, "Cat breed")

            except ValueError as error:
                print(error)
                break

            except BreedServiceError as error:
                print(error)

                choice = choose_service_recovery()

                if choice == "2":
                    raise ReturnToMenu()


def print_result(pet, cat):
    pet.print_info()
    cat.print_info()
    print(f"   Breed: {cat.breed}")


def run_interactive():
    pet_name = read_interactive_field(
        "Pet name",
        validate_text
    )

    pet_years, pet_months = read_interactive_age("Pet")

    cat_name = read_interactive_field(
        "Cat name",
        validate_text
    )

    cat_years, cat_months = read_interactive_age("Cat")

    cat_breed = read_cat_breed()

    pet = Pet(
        name=pet_name,
        age=pet_years,
        age_months=pet_months
    )

    cat = Cat(
        name=cat_name,
        age=cat_years,
        breed=cat_breed,
        age_months=cat_months
    )

    print()
    print_result(pet, cat)


def main():
    try:
        while True:
            print()
            print("Pet and Cat Information")
            print()
            print("1. Enter pet and cat information")
            print("2. Exit")
            print()

            choice = read_line("Choose an option (1-2)").strip()

            if choice == "1":
                print()

                try:
                    run_interactive()
                except ReturnToMenu:
                    print(
                        "Entry stopped. "
                        "No completed result was printed."
                    )

            elif choice == "2":
                print("Goodbye.")
                return 0

            else:
                print("Error: Menu choice must be 1 or 2.")
                print(
                    "Help: Enter 1 to enter information "
                    "or 2 to exit."
                )

    except IncompleteInputError as error:
        print(
            f"\nError: The input ended before {error} was provided.\n"
            "Help: Run the program again and complete the entry.",
            file=sys.stderr
        )
        return 1

    except KeyboardInterrupt:
        print(
            "\nEntry cancelled.\n"
            "You can run the program again when you are ready.",
            file=sys.stderr
        )
        return


if __name__ == "__main__":
    sys.exit(main())