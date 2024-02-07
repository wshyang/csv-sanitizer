# CSV Sanitizer

This is a Python script that reads a CSV file that contains a column of command strings that need to be sanitized, and writes an Excel file with four tabs: one with the sanitized version of the original CSV table, one with a dataframe of the original values and their counts, one with a dataframe of the pattern counts, and one with a pivot table of the sanitized values and their counts.

## Requirements

- Python 3
- pandas

## Usage

- Place the CSV files that need to be sanitized in the same directory as the script.
- Run the script with `python csv_sanitizer.py`.
- The script will scan the directory for all CSV files that don't have a corresponding output file with the same name and "_sanitised" added, and process them one by one.
- The output files will be named as the input files with "_sanitised.xlsx" added, and will have four tabs: "Sanitized", "Original", "Pattern Counts", and "Command Patterns".

## Functionality

The script performs the following tasks:

- It defines a file specific dataframe to store the original strings and their counts, with the columns "original" and "count".
- It defines a function `regex_replace` that takes a string as an input and returns a tuple of two elements: the sanitized string and the references list. The function applies a series of regex replacements on each command string to sanitize them. The regex replacements are as follows:
    - Replace a single quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8".
    - Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH".
    - Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC".
    - Replace valid hostnames with the string "HOSTNAME".
- It stores the original values and their counts in a dataframe specific for each file, and checks if the value already exists before adding it to the dataframe. The index of the original value in the dataframe is used as the suffix for the replacement string, preceded by an underscore.
- It adds a new column to the input dataframe to store the references, which are the replacement strings with the suffixes. The command strings in the input dataframe are updated with the sanitized command strings, which are the replacement strings without the suffixes.
- It writes the input dataframe to the first tab of an Excel file, with the sheet name "Sanitized".
- It writes the file specific dataframe with the original values and their counts to the second tab of the same Excel file, with the sheet name "Original".
- It creates a dataframe to store the pattern counts, which are the replacement strings and their counts in the file specific dataframe. It writes the pattern dataframe to the third tab of the same Excel file, with the sheet name "Pattern Counts".
- It creates a pivot table of the sanitized values and their counts in the input dataframe. It writes the pivot table to the fourth tab of the same Excel file, with the sheet name "Command Patterns".

## Error Handling

The script handles any errors or exceptions gracefully, and provides informative messages to the user. Some possible errors or exceptions are:

- The input hostname is not a string.
- The input hostname does not match the specified pattern.
- The input file is not a CSV file or does not have the "Command / Event" column.
- The output file already exists or cannot be written.

## Assumptions

The script makes the following assumptions:

- The provided hostname string contains alphanumeric characters only.
- The script does not perform DNS resolution or check network connectivity.
- The script does not validate the existence of the server or its configuration; it only validates the format of the hostname string.
- The CSV files that need to be sanitized are placed in the same directory as the script.
- The CSV files have a column named "Command / Event" that contains the command strings that need to be sanitized.
- The command strings do not contain any other special characters or symbols that need to be sanitized.

## Constraints

The script has the following constraints:

- The script is designed to work with hostnames that adhere to the specified pattern. Hostnames deviating from this pattern may not be accurately validated.
- The script is designed to work with command strings that match the specified regex expressions. Command strings deviating from these expressions may not be accurately sanitized.

## Dependencies

The script depends on the following modules:

- os
- re
- pandas

## Version History

- v1.0: Initial release.
