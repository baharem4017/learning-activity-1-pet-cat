"""Reproduce the Pet/Cat presentation's local performance microbenchmark.

Run from the project folder with: python Benchmark.py
Place this file beside main.py, validation.py, age_utils.py and breed_service.py.

This measures input validation and construction of one Pet/Cat pair.
It does not measure typing, menu interaction, printing, or application startup.
"""

import statistics
import timeit

from main import Cat, Pet
from validation import validate_integer, validate_text


def benchmark_operation():
    """Validate two names and four age values, then construct two objects.

    Constructing Cat also validates the breed against the local reference list.
    """
    pet_name = validate_text("Dobby", "Pet name")
    cat_name = validate_text("Luna", "Cat name")

    pet_years = validate_integer("2", "Pet age in years")
    pet_months = validate_integer("3", "Pet additional months")
    cat_years = validate_integer("1", "Cat age in years")
    cat_months = validate_integer("6", "Cat additional months")

    cat = Cat(cat_name, cat_years, "Persian", cat_months)
    pet = Pet(pet_name, pet_years, pet_months)
    return pet, cat


def main():
    operations_per_repeat = 10_000
    repeats = 7

    elapsed_seconds = timeit.repeat(
        benchmark_operation,
        number=operations_per_repeat,
        repeat=repeats,
    )
    microseconds_per_operation = [
        elapsed / operations_per_repeat * 1_000_000
        for elapsed in elapsed_seconds
    ]
    median_us = statistics.median(microseconds_per_operation)
    print(f"Median execution time: {median_us:.2f} μs")


if __name__ == "__main__":
    main()
