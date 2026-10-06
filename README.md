# Learning Activity 1: Pet and Cat

Author: Bahareh Mohamadtaheri  
Course: CS/DATA 5010, Bowling Green State University

## Objective

Demonstrate inheritance in Python through a Pet base class
and a Cat derived class.

Pet stores name, age, and additional months.
Cat inherits from Pet and adds breed.

Both objects use Pet.print_info().
Cat does not override this method.
The Cat breed is printed separately after cat.print_info().

## Assignment and Extension

The original Q1 requires five input lines and numeric age output.

The current program extends Q1 with:
- An interactive menu.
- Age entry using completed years and additional months.
- Input validation and correction.
- Cat breed verification against a reference.
- Graceful cancellation and end-of-input handling.

The current main.py starts with the interactive menu.
It does not provide the original prompt-free assignment mode.

The original instructor sample files are retained as materials
from the earlier basic implementation.

## Requirements

- Python 3.
- The program has been run using Python 3.14.7 on macOS.
- The application uses the Python standard library only.
- No API key or internet connection is required when the saved
  breed reference is available.

Online verification is optional and requires internet access
and a CAT_API_KEY environment variable.

## Files

- main.py: Classes, menu, input handling, and result printing.
- validation.py: Text and integer validation.
- age_utils.py: Age formatting.
- breed_service.py: Online and saved-reference breed verification.
- data/cat_breeds_reference.json: Saved breed reference.
- data/offline_breed_validation_actual.txt:
  Recorded verification without an API key.
- data/breed_validation_actual.txt:
  Earlier recorded online breed verification.
- data/month_range_actual.txt:
  Recorded month-range error and correction.
- data/sample_input.txt: Original five-line instructor input.
- data/sample_expected.txt: Original required output.
- data/sample_actual.txt: Output from the earlier basic program.

## Run Without an API Key

1. Download and extract the repository.
2. Keep the files in their existing folders.
3. Confirm that data/cat_breeds_reference.json is present.
4. Open a terminal in the folder containing main.py.
5. Run:

```bash
python3 main.py
```

If your Python executable is named python, use:

```bash
python main.py
```

Alternatively, open the extracted project in PyCharm,
select an installed Python 3 interpreter, and run main.py.

Do not configure CAT_API_KEY when testing the saved-reference
behavior.

## Menu

```text
Pet and Cat Information

1. Enter pet and cat information
2. Exit

Choose an option (1-2):
```

Choose 1 to enter a record.
Choose 2 to exit.

After a completed record, the program returns to the menu.

## Input Order

After choosing 1, enter:

1. Pet name.
2. Pet age in completed years.
3. Pet additional months.
4. Cat name.
5. Cat age in completed years.
6. Cat additional months.
7. Cat breed.

Enter each answer when its corresponding prompt appears.

## Example Run Without an API Key

```text
Pet name: Dobby
Pet age in years: 2
Pet additional months: 0
Cat name: Luna
Cat age in years: 0
Cat additional months: 7
Cat breed: persian
Notice: Using the saved breed reference without an API key.

Pet Information:
   Name: Dobby
   Age: 2 years
Pet Information:
   Name: Luna
   Age: 7 months
   Breed: persian
```

The saved-reference notice appears when the reference is first
loaded successfully during a program session.

## Understanding the Output

The first block describes the generic Pet.
The second block describes the Cat.

The objects have separate attributes.
Cat inherits print_info() from Pet.
A separate statement prints the Cat breed.

Age formatting uses only the relevant units:
- 0 years and 7 months: 7 months.
- 2 years and 0 months: 2 years.
- 2 years and 3 months: 2 years and 3 months.
- 1 year and 1 month: 1 year and 1 month.
- 0 years and 0 months: 0 months.

## Validation Rules

### Names and Breed Text

- Required and nonempty.
- Maximum 30 characters after trimming outer spaces.
- English letters, spaces, hyphens, and apostrophes are allowed.
- At least one English letter is required.
- Digits, unsupported characters, and control characters
  are rejected.
- Capitalization and internal spaces are preserved.

The 30-character limit is a project choice, not a universal
standard.

Breed text must also match a name in the selected reference.
Matching ignores capitalization and repeated spaces.
The displayed text preserves the user's accepted entry.

### Years and Months

- Years must be a whole number of 0 or more.
- Additional months must be a whole number from 0 to 11.
- Both parts are required, including an explicit 0.
- Decimal values, words, and separators are rejected.
- Signed values such as +3 and leading zeros such as 003
  are accepted and converted to integers.
- -0 is accepted as 0.
- A numeric part may contain no more than 32 digits,
  excluding its optional sign.

For 15 months, enter 1 completed year and 3 additional months.

Malformed or negative input retries the affected field.
A month value of 12 or more restarts that pet's years-and-months
entry while retaining its name and the other accepted data.

## Breed Reference Behavior

The reference originates from The Cat API:

https://api.thecatapi.com/v1/breeds?lang=en

The saved file records:
- Source name.
- Source URL.
- Download timestamp.
- Breed names normalized for matching.

When CAT_API_KEY is configured, the program first attempts
online verification.

If the online reference is unavailable, it attempts to use
the saved file.

Without CAT_API_KEY, it uses the saved file directly.

A successfully loaded breed list is reused for the remainder
of the program session.

The program does not automatically refresh the saved file.

If neither reference can be loaded, the program offers:
1. Retry breed verification.
2. Return to the main menu.

It does not print a completed record when breed verification
remains unresolved.

## Example Breed Correction

```text
Cat breed: jhgfuf
Error: Cat breed was not found in the breed reference.
Help: Check the spelling and enter the full breed name, such as Persian or Scottish Fold.
Cat breed: Persian
```

A missing match means the entry was not found in the reference.
It does not prove that a breed does not exist.

## Optional Online Verification

To enable online verification in PyCharm:

1. Open the run configuration for main.py.
2. Open Environment variables.
3. Add CAT_API_KEY as the variable name.
4. Paste your own API key as its value.
5. Save the configuration and run main.py.

Keep the key out of source files, screenshots, and GitHub.

If a python.org installation on macOS reports
CERTIFICATE_VERIFY_FAILED, run its supplied
Install Certificates.command and restart the program.

## Cancellation and End of Input

Control+C cancels the program:

```text
Entry cancelled.
You can run the program again when you are ready.
```

The current cancellation handler returns normally.
The observed terminal exit status was 0.

End of input stops the program and identifies the missing field.
For example:

```text
Error: The input ended before Pet name was provided.
Help: Run the program again and complete the entry.
```

The end-of-input handler returns exit status 1.

A blank line is an empty answer and can be corrected.
End of input means no further answer is available.

No completed information blocks are printed until all fields
in the current record have been accepted.

## Verification

The following behaviors were observed in local runs:

- Earlier basic Q1 sample completed with exit code 0.
- Earlier sample_actual.txt and sample_expected.txt were
  compared in PyCharm; Contents are identical was reported.
- Invalid year text was rejected and corrected.
- Blank names were rejected and corrected.
- Negative and decimal years were rejected.
- Digits in names were rejected.
- A 30-character Pet name was accepted.
- 31-character Pet names, Cat names, and breeds were rejected.
- Invalid menu choices were rejected.
- Months outside 0–11 were rejected.
- A month value of 12 restarted the affected age pair.
- An unknown breed was rejected and corrected to Persian.
- The saved reference accepted a known breed without an API key.
- The saved reference rejected jhgfuf and accepted its
  correction to Persian.
- Control+C displayed the cancellation notice.
- After the cancellation change, terminal exit status 0
  was observed.
- End of input at Pet name displayed the missing-field message.
- Menu option 2 displayed Goodbye and exited successfully.

These observations cover the demonstrated cases.
They do not establish that every possible case has been tested.

A fresh download of the latest repository still needs to be
run without an API key to confirm that all required files
are included.

## Limitations

- The original question does not specify an age unit;
  years and months are an extension.
- The current main.py uses interactive prompts and a menu,
  rather than the original five-line assignment interface.
- Breed verification depends on the names in the reference.
- The saved reference reflects its recorded download time.
- Alternative spellings, aliases, or unlisted breeds
  may be rejected.
- Text rules and length limits are chosen project policies.
- Not every error condition or interruption point has
  been tested.
- Operating-system failures and unexpected programming
  defects are outside the handled input-error cases.

## Sources

- Q1 Pet information: Assignment supplied by the instructor.
- The Cat API: https://thecatapi.com/
- Python documentation: https://docs.python.org/3/