# Learning Activity 1: Pet and Cat

Author: Bahareh Mohamadtaheri  
Course: CS/DATA 5010, Bowling Green State University

## Objective

Demonstrate Python inheritance through a Pet base class and a Cat
derived class.

Pet stores name and age. Cat inherits from Pet and adds breed.
Both objects use Pet.print_info() without a Cat override.
The Cat breed is printed separately.

The current program extends Q1 with an interactive menu,
input validation, age entry in years and months, and online
breed verification. These features are project extensions.

## Requirements

- Python 3.
- Development environment: Python 3.14.7, PyCharm, macOS.
- Internet access for the first successful breed lookup in each run.
- A personal The Cat API key.
- The application uses Python's standard library.
- No additional application packages are required.

Get an API key:
https://www.thecatapi.com/signup

## Files

| File | Purpose |
|---|---|
| main.py | Pet and Cat classes, menu, input recovery, and output |
| validation.py | Text and integer validation |
| age_utils.py | Age formatting with year/month units |
| breed_service.py | Online breed lookup and connection handling |
| data/breed_validation_actual.txt | Recorded breed rejection and correction |
| data/sample_input.txt | Original five-line instructor sample |
| data/sample_expected.txt | Original required sample output |
| data/sample_actual.txt | Output recorded from the earlier basic solution |

The original sample files document the earlier basic solution.
The current program uses a menu and seven data fields.
Do not use the original five-line input file as its input sequence.

## Set Up in PyCharm

1. Download and extract the repository.
2. Open the extracted project folder in PyCharm.
3. Select a Python 3 interpreter.
4. Keep all four Python files together in the project root.
5. Open Run > Edit Configurations and select the main configuration.
6. In Environment variables, add:
   - Name: CAT_API_KEY
   - Value: your personal API key
7. Apply the changes and run main.py.

Keep the API key out of source files, screenshots, and GitHub.
Each user should configure their own key.

### macOS Certificate Setup

For Python installed from python.org, if a request fails with
CERTIFICATE_VERIFY_FAILED, run Install Certificates.command
from the Applications folder for the installed Python version.

For the development installation, the location was:

```text
/Applications/Python 3.14/Install Certificates.command
```

Restart the program after installation.
Do not disable HTTPS certificate verification.

## Run

Run main.py in PyCharm using the configured main run configuration.

The program displays:

```text
Pet and Cat Information

1. Enter pet and cat information
2. Exit

Choose an option (1-2):
```

Choose 1 to enter a record, or 2 to exit.

The seven data fields are:

1. Pet name
2. Pet completed years
3. Pet additional months
4. Cat name
5. Cat completed years
6. Cat additional months
7. Cat breed

After a completed record, the main menu appears again.

### Terminal Alternative

From the project root on macOS:

```bash
export CAT_API_KEY='YOUR_API_KEY'
python3 main.py
```

Replace YOUR_API_KEY locally with your own key.
The setting applies to that terminal session and is separate
from PyCharm's run configuration.

If using the project's existing virtual environment:

```bash
.venv/bin/python main.py
```

## Example Run

Select menu option 1, then enter:

```text
Dobby
2
0
Kreacher
0
7
Persian
```

After successful breed verification, the information blocks are:

```text
Pet Information:
   Name: Dobby
   Age: 2 years
Pet Information:
   Name: Kreacher
   Age: 7 months
   Breed: Persian
```

Each attribute line begins with three spaces.

## Understanding the Output

The first information block describes the generic Pet.
The second information block describes the Cat.

Pet and Cat are separate objects with separate state.
Cat inherits print_info() from Pet without overriding it.
A separate statement prints breed after cat.print_info().

Age displays only the relevant units:

| Completed years | Additional months | Display |
|---|---|---|
| 0 | 7 | 7 months |
| 2 | 0 | 2 years |
| 1 | 1 | 1 year and 1 month |
| 2 | 3 | 2 years and 3 months |
| 0 | 0 | 0 months |

## Validation Rules

### Names and Breed Text

- Required and no longer than 30 characters after trimming.
- English letters, ordinary spaces, hyphens, and apostrophes only.
- Must contain at least one letter.
- Digits and control characters are rejected.
- Outer spaces are removed.
- Internal spaces and capitalization are preserved.

These are chosen project rules, not universal naming standards.

### Age

- Years must be a nonnegative whole number.
- Additional months must be a whole number from 0 to 11.
- Both fields are required.
- Blank values are not replaced with zero.
- Decimals, words, scientific notation, and separators are rejected.
- A leading sign and leading zeros are accepted when the resulting
  value is nonnegative.
- Numeric input is limited to 32 digits excluding the sign.
- No biological maximum age is imposed.

For 15 months, enter 1 completed year and 3 additional months.

### Breed Verification

The program retrieves breed names from The Cat API:

https://api.thecatapi.com/v1/breeds?lang=en

Matching ignores capitalization and repeated spaces.
The displayed breed retains the user's accepted text.

A name absent from this reference is reported as not found.
This does not prove that the breed does not exist elsewhere.

Successful reference data is reused in memory during the same run.
It is not saved for use after restarting the program.

## Error Messages and Recovery

Each rejected input produces an error message and short guidance.

- Invalid text, integer formats, and negative values retry only
  the affected field.
- Additional months above 11 restart that pet's year/month pair.
- A breed not found in the reference retries only the breed.
- Connection or service failures allow retrying the same breed
  or returning to the main menu.
- Returning to the main menu discards the unfinished record.
- No completed information blocks are printed until all fields,
  including breed verification, are accepted.
- An invalid menu choice displays guidance and asks again.

### Cancellation with Ctrl+C

The program displays:

```text
Entry cancelled.
You can run the program again when you are ready.
```

It then stops without printing an unfinished record.
The cancellation handler uses return without a numeric value;
the current program therefore exits with status 0 after cancellation.

### End-of-File

EOF means that no further input is available.
It is different from pressing Enter to submit a blank field.

For example, EOF while waiting for Pet name produces:

```text
Error: The input ended before Pet name was provided.
Help: Run the program again and complete the entry.
```

The program stops with exit status 1.

In a macOS terminal, Ctrl+D on an empty input line can signal EOF.

### Normal Exit

Menu option 2 prints:

```text
Goodbye.
```

The program exits with status 0.

## Verification

Manual testing was performed on October 6, 2026,
using Python 3.14.7 on macOS.

Observed during development:

- Invalid year text such as two was rejected and corrected.
- Blank Pet names were rejected and corrected.
- Negative years and decimal ages were rejected and corrected.
- Names containing digits were rejected.
- Pet and Cat names longer than 30 characters were rejected.
- Breed text longer than 30 characters was rejected.
- Negative months displayed guidance specifying 0 to 11.
- An invalid main-menu choice was rejected.
- After resolving a local certificate issue, an unrecognized breed
  was rejected using the online reference.
- Correcting the breed to Persian produced the complete result
  while preserving accepted names and ages.
- Menu option 2 printed Goodbye. and finished with exit code 0.
- Ctrl+C at Pet name displayed the cancellation notice
  and stopped without printing a completed result.
- EOF at Pet name identified the missing field
  and stopped without printing a completed result.

The breed transcript is saved in:

```text
data/breed_validation_actual.txt
```

The Ctrl+C and EOF observations were made before changing
the cancellation handler from return 130 to return.
The revised cancellation exit status has not yet been verified.

### Earlier Basic-Solution Verification

The original instructor sample matched its expected output
in PyCharm Compare Files, which reported:

```text
Contents are identical
```

That result applies to the earlier five-input version,
not the current interactive interface.

### Remaining Verification

Not every test was repeated after every code revision.

Remaining checks include:

- Retesting cancellation after the handler change.
- Testing EOF and Ctrl+C at other input fields.
- Testing acceptance at the exact 30-character boundary.
- Testing all service failure and recovery cases.
- Running the documented setup from a fresh repository download.

These checks are not marked Passed.

## Limitations

- The current program is interactive; it does not reproduce the
  original five-input, prompt-free assignment interface.
- Breed acceptance depends on the reference's coverage and
  exact normalized names.
- Aliases and mixed breeds may not match the reference.
- The first breed lookup requires internet access and a working key.
- Age uses whole years and months; days are not represented.
- Input limits do not guarantee handling of every possible failure.
- Unexpected programming defects require debugging.
- Runtime and memory usage have not been benchmarked.

## Potential Improvements

- Documented breed aliases.
- A dated offline reference cache.
- Automated regression tests.
- A separate original-assignment entry point.
- Measured runtime and memory results.

## References

- Q1 Pet information: assignment supplied by the instructor.
- The Cat API:
  https://docs.thecatapi.com/docs/examples/breeds
- Python on macOS:
  https://docs.python.org/3.14/using/mac.html