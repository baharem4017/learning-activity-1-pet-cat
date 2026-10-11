# Learning Activity 1: Pet and Cat

**Author:** Bahareh Mohamadtaheri  
**Course:** CS/DATA 5010, Bowling Green State University

## Objective and scope

Demonstrate Python inheritance with a `Pet` base class and a `Cat` subclass. Each object has its own name and age. `Cat` adds a breed and inherits `Pet.print_info()` without overriding it. The program prints the cat's breed separately.

The original Q1 uses five input lines and a specified output format. This version is an **interactive extension**, with a menu, years and additional months, input correction, a local supported-breed list, and controlled breed access through a getter and setter. These extensions are not presented as instructor requirements.

**This `main.py` does not implement the original prompt-free, five-line interface.** Original assignment sample files, if retained, are historical materials and cannot be used unchanged as input to this version. Its age descriptions also differ from the original numeric output.

## Requirements and environment setup

- An installed Python 3 interpreter supporting f-strings (Python 3.6 or later).
- A terminal or PyCharm with that Python interpreter selected.
- No third-party packages, API keys, or internet connection are needed to run the program.

Keep these four files together in one folder:

| File | Responsibility |
| --- | --- |
| `main.py` | Pet/Cat classes, menu, prompts, recovery, and output |
| `validation.py` | Text and nonnegative integer validation using explicit loops |
| `age_utils.py` | Readable age descriptions using a list, `append()`, and `join()` |
| `breed_service.py` | A fixed list of 106 supported names and breed validation |

Download and extract the project if necessary. Use the exact filenames above, without download suffixes such as `(1)`. No package installation or environment variables are required. An existing `CAT_API_KEY` setting has no effect on this version.

In PyCharm, open the project folder, select an installed Python 3 interpreter for the project, and run `main.py`. Alternatively, open a terminal in the folder containing the four files and run:

```bash
python main.py
```

If your Python command is named `python3`, use:

```bash
python3 main.py
```

You can check the selected command with `python --version` or `python3 --version`.

## Data and reference source

The program accepts Pet and Cat information from the user. This input is separate from the local breed reference; neither is a machine-learning training dataset.

`CAT_BREEDS` in `breed_service.py` contains all 106 names copied from the supplied `cat_breeds_reference(10).json`. The supplied file identifies its source as The Cat API and records a download timestamp of `2026-10-06T20:49:18.715858+00:00`. These are the file's recorded metadata, not a new verification of the live service.

The JSON may be retained as `data/cat_breeds_reference.json` for provenance, but **the program does not read it at runtime**. Editing that JSON will not update the Python list. To change supported names, edit `CAT_BREEDS`, keeping the comparison names lowercase and words separated by single spaces.

The list defines names supported by this project; it is not a claim to cover every recognized cat breed. The program has no online verification, reference-download step, or service-recovery menu.

## Menu and input order

The menu offers:

```text
Pet and Cat Information

1. Enter pet and cat information
2. Exit
```

Choose `1`, then answer these seven prompts in order:

1. Pet name.
2. Pet completed years.
3. Pet additional months.
4. Cat name.
5. Cat completed years.
6. Cat additional months.
7. Cat breed.

After a completed entry, the menu appears again. Choose `2` to exit. Menu choices must be exactly `1` or `2`; spaces around a menu choice are not removed.

## Reproduce a successful result

Run `main.py` and enter the following answers, one per prompt. The initial `1` selects entry and the final `2` exits after the result:

```text
1
Dobby
2
0
Luna
0
7
Persian
2
```

The result section should be:

```text
Pet Information:
   Name: Dobby
   Age: 2 years
Pet Information:
   Name: Luna
   Age: 7 months
   Breed: Persian
```

Menu text and input prompts also appear during the run. There is no saved-reference or online-service notice. Attribute lines begin with three spaces. PyCharm's process-completion message is not part of the program's output.

The first block describes the generic Pet; the second describes the Cat. Separate instances retain their own values. `print_result()` calls the inherited printing method and then reads the cat's breed through `get_breed()`.

## Parameters and validation rules

There are no command-line flags or runtime configuration files. The following settings and policies are defined in source code:

| Setting or rule | Location | Current value or behavior |
| --- | --- | --- |
| `MAX_TEXT_LENGTH` | `validation.py` | 30 characters after removing ordinary edge spaces |
| `MAX_NUMBER_DIGITS` | `validation.py` | 32 digits, excluding an optional sign |
| `CAT_BREEDS` | `breed_service.py` | 106 supported names |
| Additional months | `main.py`, `read_interactive_age()` | 0 through 11 |

If changing numeric limits, also update error messages that mention their values. These limits are project choices, not general standards for names or ages.

### Text

Names and breed text must be nonempty and contain at least one English letter. Only English letters, ordinary spaces, hyphens, and apostrophes are accepted. Digits, control characters, and other symbols are rejected.

`remove_edge_spaces()` removes ordinary spaces at either end using loops, without `strip()`. Capitalization and internal spaces are preserved. Validation uses explicit `for` loops instead of `any()`.

Breed text must additionally match `CAT_BREEDS`. Matching uses a lowercase copy with repeated spaces reduced for comparison only. Thus `Persian` and `PERSIAN` both match, and `Scottish  Fold` matches `scottish fold`. Output preserves the accepted text's capitalization and internal spacing.

### Years and months

Both are required nonnegative integers. Enter an explicit `0` when a part is zero. Decimals, words, and numeric separators are rejected. Optional signs and leading zeros are accepted when the resulting value is nonnegative: `+3`, `003`, and `-0` become `3`, `3`, and `0`.

Malformed or negative input retries the affected field. Months above 11 cause **both years and months for that animal** to be entered again. Other accepted input remains available during that correction.

For a total age of 15 months, enter `1` year and `3` additional months. The formatter does not convert excess months automatically.

| Years | Months | Display |
| --- | --- | --- |
| 0 | 7 | `7 months` |
| 2 | 0 | `2 years` |
| 2 | 3 | `2 years and 3 months` |
| 1 | 1 | `1 year and 1 month` |
| 0 | 0 | `0 months` |

## Breed encapsulation and program flow

`Cat.__init__()` calls `Pet.__init__()` for the shared attributes, then calls `set_breed()`.

- `set_breed()` calls `validate_breed()` and stores the accepted value in `__breed`.
- If validation fails, it raises `ValueError` before replacing the stored breed.
- `get_breed()` returns the stored value without validating again.
- Double underscores use Python name mangling to discourage accidental access; they are not a security boundary.

Name and age attributes remain public. This extension controls breed assignment through the documented getter/setter interface; it does not make every attribute private.

`read_cat_breed(name, age, age_months)` attempts Cat construction inside its correction loop and returns the accepted **Cat object**, not a string. Failed attempts do not return a completed Cat to the caller. Once Cat construction succeeds, the separate Pet is created and both are printed. No completed information blocks appear before all entry fields are accepted.

This program does not override `Cat.print_info()` or implement the previously discussed optional polymorphism demonstration.

## Reproduce corrections and interruptions

Start a new run or choose `1` for each entry scenario.

| Scenario | What to enter | Expected behavior |
| --- | --- | --- |
| Blank name | Press Enter at a name prompt | Error and repeat of that field |
| Invalid year | Enter `abc`, then `2` | Error followed by acceptance of `2` |
| Negative year | Enter `-1`, then `1` | Negative value rejected |
| Excess months | Enter years `1`, months `12`, then years `1`, months `3` | Both age fields repeat; display becomes `1 year and 3 months` |
| Unsupported breed | Enter `Banana`, then `Persian` | Only the breed is requested again |
| Invalid menu choice | Enter `3`, then `2` | Menu error, followed by exit |
| Cancellation | Press Ctrl+C while waiting for input | Cancellation message and program termination |
| End of input | Supply an incomplete redirected input file | Missing-field message and exit status 1 |

The breed correction message is:

```text
Error: Cat breed was not found in the supported breed list.
Help: Check the spelling and enter a supported breed name, such as Persian or Scottish Fold.
```

To reproduce EOF independently of terminal keyboard shortcuts, create `incomplete_input.txt` containing only `1` and a newline. Run this in Windows Command Prompt or a macOS/Linux shell:

```bash
python main.py < incomplete_input.txt
```

Use `python3` instead if appropriate. The `<` syntax shown is not a PowerShell input-redirection command. Expected error output:

```text
Error: The input ended before Pet name was provided.
Help: Run the program again and complete the entry.
```

A blank answer is different from EOF: a blank answer can be corrected, while EOF means no more input is available. EOF returns status 1. Normal exit and the handled Ctrl+C cancellation return status 0. Interruption messages are written to standard error.

## Verification of this revision

The four current modules were run together in the preparation environment on October 11, 2026. These scenarios passed: successful entry and exit, unsupported-breed correction, correction of an age pair with excess months, EOF at Pet name, and immediate menu exit.

Earlier focused checks in this revision process also confirmed all 106 reference names were copied and accepted, rejected setter updates retained the previous breed, simplified validation matched the previous implementation in 1,116 comparisons, and age formatting matched in 60 valid year/month combinations. The final age formatter was then restored to the original implementation with only docstrings/comments added; that implementation equivalence was checked.

These checks do not establish exhaustive correctness, a fresh installation on another computer, or performance benchmarks. Previous online/saved-reference transcripts describe the retired implementation and are not evidence of this version's runtime behavior. No exact local PyCharm interpreter version is claimed here.

## Limitations and possible improvements

- This is an interactive extension, not the original five-line automated-grading interface.
- Breed acceptance depends on the fixed supported-name list; aliases and unlisted names may be rejected.
- The list does not refresh automatically.
- Validation rules are deliberately limited to English letters and selected punctuation.
- Names and ages can still be changed directly through public attributes.
- The menu creates and displays entries; it does not save records, export files, or offer editing of previous entries.
- No execution-time or memory benchmark is included.

Possible future work includes a separate original-Q1 mode, additional reference aliases, and controlled age updates. These are optional improvements, not implemented features.

## Sources and retained materials

- Q1 Pet Information: instructor-supplied learning activity.
- Supplied breed-reference JSON: metadata identifies The Cat API and its recorded download date.

Original five-line samples and older online/offline transcripts, if kept in the repository, should be labeled historical. Use the input sequence and expected result in this README to reproduce the current interactive version.
