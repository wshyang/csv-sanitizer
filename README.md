# Functional Specifications

## Overview

The program is designed to perform the following tasks:

- Read a CSV file that contains a column named "Command/Events" with command strings
- Replace the command strings with sanitized strings that mask the sensitive values such as paths, numbers, hostnames, etc. with generic strings and references
- Store the original values and their counts in a separate dataframe
- Store the pattern counts of the sanitized values in another dataframe
- Create a pivot table of the sanitized values and their counts
- Write the input dataframe, the original dataframe, the pattern dataframe, and the pivot table to an Excel file with four tabs
- Print a status update and an estimated time of completion when every 0.5% of the lines are processed
- Save the program state to a file so that it can be resumed later if interrupted

## Input and Output

The program takes a CSV file as the input, and writes an Excel file as the output. The input CSV file must have a column named "Command/Events" that contains the command strings to be sanitized. The output Excel file will have four tabs: "Sanitized", "Original", "Pattern Counts", and "Command Patterns". The "Sanitized" tab will contain the input dataframe with the sanitized strings and the references. The "Original" tab will contain the original values and their counts. The "Pattern Counts" tab will contain the pattern counts of the sanitized values. The "Command Patterns" tab will contain the pivot table of the sanitized values and their counts.

## Logic and Algorithm

The program uses the following logic and algorithm to perform the tasks:

- Import the required modules: os, re, time, pickle, and pandas
- Define the sensitive values for XXX, TLD, and YY
- Define the global variable for the hostname regex pattern
- Define a function to validate the hostname format
- Define a function to replace the command strings with sanitized strings and references
- Get the current working directory
- Get the list of files in the directory
- Loop through the files
    - Check if the file is a CSV file and does not have a corresponding output file
        - Print a message indicating the file is being processed
        - Check if the program state file exists
            - If it exists, load the program state from the file and get the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable from the state
                - Check if the file name matches the current file
                    - If it matches, print a message indicating the program is resuming from the previous state
                    - If it does not match, print a message indicating the program is starting from the beginning and read the CSV file as a pandas dataframe, create a file specific dataframe to store the original strings and their counts, create a new column in the input dataframe to store the references, create a dataframe to store the pattern counts, create a pivot table of the sanitized values and their counts, and initialize the counter variable to zero
            - If it does not exist, read the CSV file as a pandas dataframe, create a file specific dataframe to store the original strings and their counts, create a new column in the input dataframe to store the references, create a dataframe to store the pattern counts, create a pivot table of the sanitized values and their counts, and initialize the counter variable to zero
        - Get the number of lines to be processed from the input dataframe
        - Calculate the threshold for printing the status update as 0.5% of the total lines
        - Get the current time as the start time
        - Loop through the rows of the input dataframe from the counter value
            - Get the command string from the row
            - Replace the command string with the sanitized string and the references
            - Update the row with the sanitized string and the references
            - Increment the counter by one
            - Check if the counter reaches the threshold
                - If it does, calculate the percentage of completion, the elapsed time, and the remaining time
                - Print the status update with the percentage, the elapsed time, and the estimated time of completion
                - Create a program state with the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable
                - Save the program state to the state file
            - Search through the references
                - Check if the reference already exists in the original dataframe
                    - If it does, increment the count of the reference by one
                    - If it does not, add the reference and its count to the original dataframe
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
The environment, segment, intra_inter, and suffix_env must be consistent. For example, if the environment is production, the suffix_env must be PRD. If the segment is intranet, the intra_inter must be intra. The suffix components must match the sensitive values for XXX, TLD, and YY. For example, if XXX is abc, TLD is com, and YY is sg, the suffix must be intraPRD.abc.com.sg or interPRD.abc.com.sg. The hostname must be converted to lowercase using casefold() before matching the regex and the specifications. This is to avoid case sensitive issues. For example, P-2-E-A-V-W-A-ABC-01.intraPRD.ABC.COM.SG and p-2-e-a-v-w-a-abc-01.intraprd.abc.com.sg are considered the same hostname.
