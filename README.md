# Functional Specification

## Overview

This program is designed to simplify and analyze the command strings in a CSV file. It replaces the command strings with simplified strings and references, and stores the original values and their counts in a separate dataframe. It also generates a pivot table of the simplified commands and their counts. It writes the output to an Excel file with two tabs.

## Input and Output

The input is a CSV file that contains the command strings in a column named "Command/Events". The output is an Excel file that contains two tabs: Original and Command Patterns. The Original tab contains the original values and their counts. The Command Patterns tab contains the pivot table of the simplified commands and their counts.

## Simplification and Replacement

The program simplifies and replaces the command strings with simplified strings and references using the following rules:

- Replace a single quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8". For example, `'aBcD_1-2'` is replaced with `ALPHANUM8_2`.
- Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH". For example, `'/usr/bin/python'` and `"/home/user/file.txt"` are replaced with `PATH_4` and `PATH_5`, respectively. However, if a PATH is at the start of the command string, it should not be replaced or referenced. For example, `/usr/bin/python /home/user/file.txt` is not replaced or referenced, but `/usr/bin/python /home/user/file.txt` is replaced with `/usr/bin/python PATH_5` and referenced as `PATH_5`.
- Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC". For example, `echo 123456789` is replaced with `NUMERIC_0`.
- Replace valid hostnames with the string "HOSTNAME". A valid hostname follows the regex pattern defined in the global variable `hostname_pattern`. For example, `p2eavwaabc-01.intraPRD.abc.com.sg` is replaced with `HOSTNAME_5`.

The program stores the original values and their counts in a file specific dataframe named `original`. It also generates the reference values for the original values by appending an underscore and the index of the original value in the `original` dataframe to the simplified strings. For example, the reference value for `123456789` is `NUMERIC_0`. The program updates the input dataframe with the simplified strings and the references in a new column named "Reference".

## Pivot Table

The program creates a pivot table of the simplified commands and their counts using the `pivot_table` function of pandas. The pivot table has the simplified command strings as the index and the counts as the values. The program writes the pivot table to the output Excel file in a separate tab.

## Program State

The program saves and loads the program state to and from a state file named "program_state.pkl". The program state is a dictionary that contains the following keys and values:

- "file_name": the name of the input CSV file
- "input_df": the input dataframe
- "original": the original dataframe
- "counter": the counter variable that tracks the progress of the program

The program saves the program state to the state file every time it reaches a threshold of 0.5% of the total lines to be processed. The program loads the program state from the state file if it exists and the file name matches the current file. The program resumes from the previous state at the line indicated by the counter value. The program deletes the state file after the output file is written and saved.

## Logic and Algorithm

The program uses the following logic and algorithm to perform the tasks:

- Import the required modules: os, re, time, pickle, and pandas
- Define the sensitive values for XXX, TLD, and YY
- Define the global variable for the hostname regex pattern
- Define a function to validate the hostname format
- Define a function to replace the command strings with simplified strings and references
- Get the current working directory
- Get the list of files in the directory
- Loop through the files
    - Check if the file is a CSV file and does not have a corresponding output file
        - Print a message indicating the file is being processed
        - Check if the program state file exists
            - If it exists, load the program state from the file and get the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable from the state
                - Check if the file name matches the current file
                    - If it matches, print a message indicating the program is resuming from the previous state
                    - If it does not match, print a message indicating the program is starting from the beginning and read the CSV file as a pandas dataframe, create a file specific dataframe to store the original values and their counts, create a new column in the input dataframe to store the references, create a dataframe to store the pattern counts, create a pivot table of the simplified values and their counts, and initialize the counter variable to zero
            - If it does not exist, read the CSV file as a pandas dataframe, create a file specific dataframe to store the original values and their counts, create a new column in the input dataframe to store the references, create a dataframe to store the pattern counts, create a pivot table of the simplified values and their counts, and initialize the counter variable to zero
        - Get the number of lines to be processed from the input dataframe
        - Calculate the threshold for printing the status update as 0.5% of the total lines
        - Get the current time as the start time
        - Loop through the rows of the input dataframe from the counter value
            - Get the command string from the row
            - Replace the command string with the simplified string and the references
            - Update the row with the simplified string and the references
            - Increment the counter by one
            - Check if the counter reaches the threshold
                - If it does, calculate the percentage of completion, the elapsed time, and the remaining time
                - Print the status update with the percentage, the elapsed time, and the estimated time of completion
                - Create a program state with the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable
                - Save the program state to the state file
            - Search through the references
                - For each reference, check if the value already exists in the original dataframe
                    - If it does, increment the count of the value by one
                    - If it does not, add the value and its count to the original dataframe
        - Search through the unique values in the original dataframe
            - Get the pattern of the value by removing the suffix
            - Check if the pattern already exists in the pattern dataframe
                - If it does, increment the count of the pattern by the count of the value
                - If it does not, add the pattern and its count to the pattern dataframe
        - Write the input dataframe, the original dataframe, the pattern dataframe, and the pivot table to an Excel file with four tabs
        - Delete the program state file
        - Print a message indicating the file is processed and saved

## Details of the Regexs and the Hostname Specifications

The program uses the following regexs and hostname specifications to perform the string replacements:

- The regex for matching paths is:

```python
r"(/(bin|boot|dev|etc|home|lib|lib64|media|mnt|opt|proc|root|run|sbin|srv|sys|tmp|usr|var)(/[^/\s]+)*)|('[^']+')|(\"[^\"]+\")"
```

This regex matches any string that starts with a slash and contains one of the default directories as the first component, followed by zero or more non-slash and non-whitespace characters, or any string that is enclosed in matching single or double quotes.

The regex for matching numbers is:

```python
r"(?<=echo )\d{5,12}"
```

This regex matches any string that consists of 5 to 12 digits and is preceded by the word “echo”.

The regex for matching hostnames is:

```python
r"(?P<environment>[p|t|q])-(?P<location>[2|3])-(?P<segment>[e|a])-(?P<tier>[a|d|g|i|m|w])-(?P<virtualization>[v|p])-(?P<operating_system>[w|x|r|s|k])-(?P<application>[a-z0-9]{3,4})-(?P<server>[0-9]{2})(?:\.(?P<intra_inter>(intra|inter))(?P<suffix_env>(PRD|QAT))\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+)?\b"
```

This regex matches any string that follows the hostname format of:

environment-location-segment-tier-virtualization-operating_system-application-server.suffix

where:

environment is one of p, t, or q
location is either 2 or 3
segment is either e or a
tier is one of a, d, g, i, m, or w
virtualization is either v or p
operating_system is one of w, x, r, s, or k
application is a 3 or 4 letter alphanumeric string
server is a 2 digit number
suffix is optional and consists of intra_inter and suffix_env (without any delimitor) and followed by XXX, TLD, and YY separated by dots
The regex also captures the named groups for each component of the hostname.

The hostname specifications are:
The environment, segment, intra_inter, and suffix_env must be consistent. For example, if the environment is production, the suffix_env must be prd. If the segment is intranet, the intra_inter must be intra. The suffix components must match the sensitive values for XXX, TLD, and YY. For example, if XXX is abc, TLD is com, and YY is sg, the suffix must be intraprd.abc.com.sg or interprd.abc.com.sg. The hostname must be converted to lowercase using casefold() before matching the regex and the specifications. This is to avoid case sensitive issues. For example, P2EAVWAABC01.INTRAPRD.ABC.COM.SG and p2eavwaabc01.intraprd.abc.com.sg are considered the same hostname.

## Input and Output
The program takes a CSV file as the input, and writes an Excel file as the output. The input CSV file must have a column named “Command/Events” that contains the command strings to be simplified. The output Excel file will have four tabs: “Simplified”, “Original”, “Pattern Counts”, and “Command Patterns”. The “Simplified” tab will contain the input dataframe with the simplified strings and the references. The “Original” tab will contain the original values and their counts. The “Pattern Counts” tab will contain the pattern counts of the simplified values. The “Command Patterns” tab will contain the pivot table of the simplified values and their counts. The output file name will be derived from the source file name by appending a suffix of “_simplified”. For example, if the input file name is “commands.csv”, the output file name will be “commands_simplified.xlsx”.

## How the References are Generated
The references are generated by appending a suffix of the index number to the simplified value. For example, if the simplified value is PATH, the reference value will be PATH_1, PATH_2, etc. depending on how many times the path value has been encountered and replaced in the input dataframe. The reference values are stored as a comma separated list in the new Reference column of the input dataframe. The Original dataframe has an Index column that corresponds to the reference suffixes. For example, if the reference value is PATH_1, the Index column will have the value 1. This way, the references can be easily correlated with the original values and their counts.
