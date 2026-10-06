# Learning Activity 1: Pet and Cat

Author: Bahareh Mohamadtaheri  
Course: CS/DATA 5010, BGSU

## Objective

Demonstrate inheritance in Python.

Pet stores name and age.
Cat inherits from Pet and adds breed.
Both objects use Pet.print_info().
The Cat breed is printed separately.

## Requirements

- Python 3.
- The instructor sample was run using Python 3.14.7
  in PyCharm on macOS.
- No additional packages are required.

## Files

- main.py: Python program.
- data/sample_input.txt: Instructor sample input.
- data/sample_expected.txt: Expected sample output.
- data/sample_actual.txt: Output recorded from the sample run.

## Run

1. Download and extract the repository.
2. Open the project folder in PyCharm.
3. Open main.py and select Run 'main'.
4. Enter the following five lines in the Run console,
   pressing Enter after each line:

```text
Dobby
2
Kreacher
3
Scottish Fold
```

The program does not display input prompts.
It waits for all five input lines before printing the result.

## Expected Output

```text
Pet Information:
   Name: Dobby
   Age: 2
Pet Information:
   Name: Kreacher
   Age: 3
   Breed: Scottish Fold
```

Each attribute line begins with three spaces.

## Understanding the Output

The first information block describes the generic Pet:
Dobby, age 2.

The second information block describes the Cat:
Kreacher, age 3, breed Scottish Fold.

Pet and Cat are two separate objects.
Cat inherits print_info() from Pet without overriding it.
A separate statement prints the Cat breed after cat.print_info().

## Verification

The instructor sample was executed in PyCharm on October 6, 2026.
The program finished with exit code 0.

The saved actual output was compared with the expected output
using PyCharm Compare Files.

PyCharm reported: Contents are identical.

This confirms the instructor sample.
Additional input-validation tests have not been executed.

## Current Limitations

- The program expects five input lines in the specified order.
- Ages must be entered as integers.
- Invalid age text, such as two, causes a conversion error.
- Helpful validation and input correction are not yet implemented.
- Years-and-months entry is not yet implemented.
- The original question does not specify an age unit.

## Planned Improvements

An optional interactive extension will provide:
- Age entry using completed years and additional months.
- Input validation with clear error messages and short guidance.
- Correction of invalid fields.
- Graceful handling of incomplete input and cancellation.

These features are planned extensions, not requirements of Q1.
