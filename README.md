# Learning Activity 1: Pet and Cat

**Author:** Bahareh Mohamadtaheri  
**Course:** CS/DATA 5010, Bowling Green State University

## Objective and scope

Demonstrate Python inheritance with a `Pet` base class and a `Cat` subclass. Each object has its own name and age. `Cat` adds a breed and inherits `Pet.print_info()` without overriding it. The program prints the cat's breed separately.

The original Q1 uses five input lines and a specified output format. This version is an **interactive extension**, with a menu, years and additional months, input correction, a local supported-breed list, and breed validation during Cat construction. These extensions are not presented as instructor requirements.


## Requirements and environment setup

- An installed Python 3 interpreter supporting f-strings. Use the Python 3 interpreter selected for this project in PyCharm.
- A terminal or PyCharm with that Python interpreter selected.
- No third-party packages, API keys, or internet connection are needed to run the program.

Keep these four required application files together in one folder. To reproduce the measured efficiency result, also include the separate `Benchmark.py` script in that folder:

| File | Responsibility |
| --- | --- |
| `main.py` | Pet/Cat classes, menu, prompts, recovery, and output |
| `validation.py` | Text and nonnegative integer validation |
| `age_utils.py` | Readable age descriptions using a list, `append()`, and `join()` |
| `breed_service.py` | A fixed list of 106 supported names and breed validation |
| `Benchmark.py` | Optional performance-measurement script used for the reported efficiency result; not needed to run `main.py` |


In PyCharm, open the project folder, select an installed Python 3 interpreter for the project, and run `main.py`. Alternatively, open a terminal in the folder containing the four required application files and run:

```bash
python main.py
```

If your Python command is named `python3`, use:

```bash
python3 main.py
```

You can check the selected command with `python --version` or `python3 --version`.

## Data and reference source

The program accepts Pet and Cat information from the user. This input is separate from the local breed reference.

`CAT_BREEDS` in `breed_service.py` contains 106 supported names. Source metadata for the reference list identifies The Cat API and a download date of October 6, 2026.

The reference names are stored directly in the Python list. To change supported names, edit `CAT_BREEDS`, using lowercase names with single spaces between words, then restart the program.

The list defines the names supported by this project, not every recognized cat breed. User entries are checked against this list locally.

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
Max
0
6
Mimi
2
1
PERSIAN
2
```

The result section should be:

```text
Pet Information:
   Name: Max
   Age: 6 months
Pet Information:
   Name: Mimi
   Age: 2 years and 1 month
   Breed: PERSIAN
```

Menu text and input prompts also appear during the run. Attribute lines begin with three spaces. 

The first block describes the generic Pet; the second describes the Cat. Separate instances retain their own values. `print_result()` calls the inherited printing method and then prints the cat's public `breed` attribute separately.

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

Names and breed text must be nonempty and contain at least one  letter. Only English letters, ordinary spaces, hyphens, and apostrophes are accepted. Digits, control characters, and other symbols are rejected.

Ordinary spaces at either end of a name or breed are ignored. Capitalization and internal spaces are preserved.

Breed text must additionally match `CAT_BREEDS`. Matching uses a lowercase copy with repeated spaces reduced for comparison only. Thus `Persian` and `PERSIAN` both match, and `Scottish  Fold` matches `scottish fold`. Output preserves the accepted text's capitalization and internal spacing.

Blank inputs do not select defaults. There is no fixed retry limit: the program continues asking until input is valid or the user ends/cancels the program.

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

## Breed validation and program flow

`Cat.__init__()` calls `Pet.__init__()` for the shared attributes, then validates and stores the public breed:

```python
self.breed = validate_breed(breed, "Cat breed")
```

`validate_breed()` checks the text and supported-breed list. Invalid input raises `ValueError`; only accepted text is stored. There are no breed getter or setter methods. The output function reads `cat.breed` directly.

Name, age, and breed attributes are public. Breed validation runs during construction; later direct assignments do not automatically run validation. The interactive menu does not offer updates to existing objects.

`read_cat_breed(name, age, age_months)` attempts Cat construction inside its correction loop and returns the accepted **Cat object**, not a string. Failed attempts do not return a completed Cat to the caller. Once Cat construction succeeds, the separate Pet is created and both are printed. No completed information blocks appear before all entry fields are accepted.

The current Cat inherits `print_info()` without overriding it. An optional polymorphism extension could give Cat its own printing method and use a shared loop, but that alternative is not implemented here.

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

## Recorded run: input correction in PyCharm


This example shows correction of a nonnumeric age and an unsupported breed, acceptance of uppercase breed text, age formatting, return to the menu, and exit. It does not test the upper month boundary.

```text
Pet and Cat Information

1. Enter pet and cat information
2. Exit

Choose an option (1-2): 1

Pet name: Max
Pet age in years: E
Error: Pet age in years must be a whole number.
Help: Enter 0 or a positive integer. Do not enter decimals or words.
Pet age in years: 0
Pet additional months: 6
Cat name: Mimi
Cat age in years: 2
Cat additional months: 1
Cat breed: HGF
Error: Cat breed was not found in the supported breed list.
Help: Check the spelling and enter a supported breed name, such as Persian or Scottish Fold.
Cat breed: PERSIAN

Pet Information:
   Name: Max
   Age: 6 months
Pet Information:
   Name: Mimi
   Age: 2 years and 1 month
   Breed: PERSIAN

Pet and Cat Information

1. Enter pet and cat information
2. Exit

Choose an option (1-2): 2
Goodbye.
```

To repeat this test, enter the answers shown after each prompt, including `E` and `HGF`. The program retries the affected field rather than replacing it with a default. `PERSIAN` remains uppercase in the displayed result because normalization is used only for comparison.

## Example: correcting additional months

Use the following sequence for a separate test. This is a reproduction recipe with expected output, not a claim that this exact Max/Mimi sequence was run locally.

| Prompt | Answer |
| --- | --- |
| Menu | `1` |
| Pet name | `Max` |
| Pet years | `1` |
| Pet months | `12` |
| Pet years again | `1` |
| Pet months again | `3` |
| Cat name | `Mimi` |
| Cat years | `2` |
| Cat months | `1` |
| Cat breed | `Persian` |
| Menu after the result | `2` |

After entering `12`, expect:

```text
Error: Pet additional months must be between 0 and 11.
Help: Enter completed years and remaining months; for 15 months, use 1 year and 3 months.
```

The program asks for Pet years and months again. After correction and completion, expect this result section:

```text
Pet Information:
   Name: Max
   Age: 1 year and 3 months
Pet Information:
   Name: Mimi
   Age: 2 years and 1 month
   Breed: Persian
```

## Performance benchmark

The presentation reports a **median local execution time of 2.15 microseconds (µs) per operation** .


From the project directory, with the same Python environment as the application, run:

```bash
python Benchmark.py
```

If your system uses `python3` as the command, run:

```bash
python3 Benchmark.py
```

In PyCharm, you can instead right-click `Benchmark.py` and select **Run 'Benchmark'**. The result appears in the **Run** tool window. The author's recorded result was:

```text
Median execution time: 2.14 μs

Process finished with exit code 0
```

### What the benchmark measures

The benchmark function from the presentation:

1. Validates **two names** with `validate_text()`.
2. Validates **four age values** (years and additional months for Pet and Cat) with `validate_integer()`.
3. Validates the Cat breed using the program's **local breed list** as part of creating the Cat object.
4. Creates one **Pet** and one **Cat** object.

It uses Python's built-in `timeit.repeat()` with **7 repeats of 10,000 executions each**. For each repeat, elapsed time is divided by 10,000 to calculate time per operation, converted to microseconds, and the **median of the seven per-operation measurements** is reported. 

**Scope:** This microbenchmark does **not** measure the full interactive session. It excludes user typing, menu interaction, printing the results, and file/network activity. Results will vary with Python version, CPU, system load, and environment. To compare results fairly, keep the benchmark code and measurement procedure unchanged and record the interpreter/version used. The fixed-size core operation can be described as **O(1)** under fixed input-size bounds and a fixed breed list.

## Verification

A targeted check of the current public-breed implementation was run on October 12, 2026 in a separate execution environment. It confirmed accepted `PERSIAN`, rejected `HGF`, and replayed the Max/Mimi interaction with invalid year and breed corrections. Standard output, standard error, and exit status matched the earlier implementation exactly for that sequence; exit status was 0. This check was not a new benchmark or a complete test of every scenario below.


The recorded Max/Mimi run above was completed in PyCharm on macOS on October 11, 2026. It demonstrates:

- Rejection and correction of a nonnumeric year entry.
- Rejection and correction of an unsupported breed.
- Acceptance of uppercase breed text.
- Correct display of months alone and combined years/months.
- Return to the main menu after the result.
- The `Goodbye.` message after choosing option 2.


`data/breed_validation_actual.txt` can hold the recorded transcript, and `data/verification_notes.txt` can summarize completed checks. These documentation files are not read by the program.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError` for a project module | Keep all four Python files together with the exact filenames shown above. |
| `IndentationError` after copying code | Replace the complete affected file with the intended version; check indentation and list brackets rather than appending new code below old code. |
| Valid-looking breed is rejected | Check spelling against `CAT_BREEDS`; a missing name is unsupported, not proof that the breed does not exist. |
| Program asks for years again | A month value above 11 restarts that animal's age pair. |
| Menu choice is rejected | Enter exactly `1` or `2`, without surrounding spaces. |

## Limitations and possible improvements

- This is an interactive extension, not the original five-line automated-grading interface.
- Breed acceptance depends on the fixed supported-name list; aliases and unlisted names may be rejected.
- The list does not refresh automatically.
- Validation rules are deliberately limited to English letters and selected punctuation.
- Names, ages, and breed can be changed directly through public attributes; direct assignments do not automatically validate the new values.
- The menu creates and displays entries; it does not save records, export files, or offer editing of previous entries.
- The included local `Benchmark.py` script measures only selected validation and object-creation operations; it does not benchmark full interactive runtime or memory usage.

Possible future work includes a separate original-Q1 mode, additional reference aliases, and controlled age updates. These are optional improvements, not implemented features.

## Sources

- Q1 Pet Information: instructor-supplied learning activity.
- Breed-list source: The Cat API, as identified in reference metadata dated October 6, 2026. Supported names are stored in `breed_service.py`.

Use the input sequences and expected results in this README to reproduce the current interactive version. Retained original five-line samples describe the basic assignment interface.
