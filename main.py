"""Run the interactive Pet/Cat activity with breed validation at construction.

Keep validation.py, age_utils.py, breed_service.py beside this file. Cat inherits Pet.print_info(); breed is printed separately.
Docstrings explain each component; comments explain statements and decisions.
"""

import sys  # Provide stderr and the program's exit status.

from validation import validate_text, validate_integer  # Check names and numbers.
from age_utils import format_age  # Convert years/months into readable text.
from breed_service import validate_breed  # Check the local supported breed list.


class Pet:
    """Group a pet's name and age with the method that displays them."""

    def __init__(self, name, age, age_months=0):
        """Store the supplied name, completed years, and additional months.

        The interactive workflow validates these values before construction.
        These three attributes are public.
        """
        self.name = name  # Store this object's name.
        self.age = age  # Store completed years.
        self.age_months = age_months  # Store remaining months; default is zero.

    def print_info(self):
        """Print the shared information; Cat inherits this method unchanged."""
        print("Pet Information:")  # Print the required heading.
        print(f"   Name: {self.name}")  # Indent the name by three spaces.
        print(f"   Age: {format_age(self.age, self.age_months)}")  # Format the age.


class Cat(Pet):
    """Extend Pet with a public breed validated when the object is created."""

    def __init__(self, name, age, breed, age_months=0):
        """Initialize the shared attributes and store a supported breed.

        validate_breed checks the text and local breed list. Invalid input
        raises ValueError, so construction does not return a Cat to the caller.
        Later direct assignments to breed do not automatically validate it.
        """
        Pet.__init__(self, name, age, age_months)  # Initialize this Cat's Pet data.
        self.breed = validate_breed(breed, "Cat breed")  # Check before storing.


class IncompleteInputError(Exception):
    """Identify the field that could not be read because input ended."""
    pass  # Inherit Exception's behavior; no additional implementation is needed.


def read_line(field):
    """Prompt for one line and translate EOF into a field-specific exception."""
    try:  # Input may end before the user supplies the requested field.
        return input(f"{field}: ")  # Return entered text without calling strip().
    except EOFError:
        raise IncompleteInputError(field) from None  # Hide the original chain.


def read_interactive_field(field, validator):
    """Retry this field after invalid input; return the validator's result."""
    while True:  # Continue until a valid value is returned.
        raw = read_line(field)  # Read a fresh entry for this field.
        try:
            return validator(raw, field)  # Validate, convert if needed, and return.
        except ValueError as error:
            print(error)  # Explain the mistake; the loop then asks again.


def read_interactive_age(pet_label):
    """Read nonnegative years/months, repeating both if months exceed eleven."""
    while True:  # Each iteration collects a complete age pair.
        years = read_interactive_field(
            f"{pet_label} age in years", validate_integer
        )  # The integer validator rejects negative and non-integer input.
        months = read_interactive_field(
            f"{pet_label} additional months", validate_integer
        )  # Additional months must also be nonnegative integers.
        if months <= 11:  # Check the upper bound specific to additional months.
            return years, months  # Return the accepted age pair.
        print(
            f"Error: {pet_label} additional months "
            "must be between 0 and 11."
        )  # Explain why the pair was rejected.
        print(
            "Help: Enter completed years and remaining months; "
            "for 15 months, use 1 year and 3 months."
        )  # Give an example before the loop asks for both fields again.


def read_cat_breed(name, age, age_months=0):
    """Read a breed and return a Cat after its constructor validates it.

    Retry only the breed after ValueError; previously entered names and ages
    remain available. Construction validates the breed once per attempt.
    No network recovery menu is needed because the reference is a Python list.
    """
    # Repeat this field until a supported breed is accepted.
    while True:
        # Read new breed text; EOF and Ctrl+C propagate to main().
        raw = read_line("Cat breed")
        try:
            # The constructor validates the breed before storing it.
            return Cat(name, age, raw, age_months)
        except ValueError as error:
            # Explain the problem, then repeat the breed prompt.
            print(error)


def print_result(pet, cat):
    """Print shared information for each object, then the public cat breed."""
    pet.print_info()  # Display the generic pet's name and formatted age.
    cat.print_info()  # Use the inherited method for the cat's name and age.
    print(f"   Breed: {cat.breed}")  # Display the validated breed stored in this Cat.


def run_interactive():
    """Collect one entry, finish both objects, then display the result.

    Input order stays Pet name, Pet age, Cat name, Cat age, Cat breed.
    Cat construction is attempted at the breed step; it completes only when
    the breed passes validation. Pet is then created and both are displayed.
    """
    pet_name = read_interactive_field("Pet name", validate_text)  # Validate name.
    pet_years, pet_months = read_interactive_age("Pet")  # Collect the first age.
    cat_name = read_interactive_field("Cat name", validate_text)  # Validate name.
    cat_years, cat_months = read_interactive_age("Cat")  # Collect the second age.
    cat = read_cat_breed(cat_name, cat_years, cat_months)  # Obtain a verified Cat.
    pet = Pet(
        name=pet_name, age=pet_years, age_months=pet_months
    )  # Create the separate generic Pet after the complete entry is accepted.
    print()  # Separate prompts from results.
    print_result(pet, cat)  # Return to main after displaying this entry.


def main():
    """Repeat the menu; handle EOF and keyboard cancellation.

    Return 1 for incomplete input. Normal exit and Ctrl+C return None, which
    sys.exit treats as a successful exit.
    """
    try:  # Handle interruptions anywhere in the menu or entry workflow.
        while True:  # Successful entries return here for another menu choice.
            print()  # Add spacing before the menu.
            print("Pet and Cat Information")  # Display the program heading.
            print()
            print("1. Enter pet and cat information")
            print("2. Exit")
            print()
            choice = read_line("Choose an option (1-2)")  # Read the menu choice.
            if choice == "1":
                print()  # Separate menu from entry prompts.
                run_interactive()  # Collect and print one complete entry.
            elif choice == "2":
                print("Goodbye.")  # Acknowledge the request to exit.
                return  # End the menu loop and main function.
            else:
                print("Error: Menu choice must be 1 or 2.")
                print("Help: Enter 1 to enter information or 2 to exit.")
                # The loop displays the menu again after an invalid choice.
    except IncompleteInputError as error:
        print(
            f"\nError: The input ended before {error} was provided.\n"
            "Help: Run the program again and complete the entry.",
            file=sys.stderr  # Send the incomplete-input message to the error stream.
        )
        return 1  # Report incomplete input to the operating system.
    except KeyboardInterrupt:
        print(
            "\nEntry cancelled.\n"
            "You can run the program again when you are ready.",
            file=sys.stderr  # Display a friendly cancellation message.
        )
        return  # End the program without showing a traceback.


if __name__ == "__main__":  # Run the menu only when this file is executed directly.
    sys.exit(main())  # Pass main's return value to the operating system.
