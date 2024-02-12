# Functional Specification

## Overview

This program is designed to simplify and analyze the command strings in a CSV file. It generates a pivot table of the simplified commands and their counts. It writes the output to an Excel file with three tabs: Simplified, References to Originals, and Pattern Counts.

## Input and Output

The input is a CSV file that contains the command strings in a column named "Command/Events". The output is an Excel file that contains the input dataframe with the simplified values, the references to the original values, and the pivot table of the simplified commands and their counts in separate tabs. The Simplified tab contains the input dataframe with the simplified values. The References to Originals tab contains the original values and their counts. The Pattern Counts tab contains the pivot table of the simplified commands and their counts.

## Simplification and Replacement Rules

- The program uses a function called `simplify_and_replace` to replace command strings with simplified strings and references according to specific rules, storing the original values and their counts in a separate dataframe `OriginalReferencesDataframe`. The simplified string is the command string with the original strings replaced by the replacement strings, and both the original and replacement strings are returned in the same order as they appear in the command string. For example, if the original value is `"aBcD_1-2"` and its index in `OriginalReferencesDataframe` is 2, the reference value will be `2`. For example, if the reference value is `1`, the Index column will have the value 1. This way, the references can be easily correlated with the original values and their counts.
- Replace a double quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8". For example, `"aBcD_1-2"` is replaced with `ALPHANUM8`.
- Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH". For example, `'/usr/bin/python'` and `"/home/user/file.txt"` are replaced with `PATH` and `PATH`, respectively. However, if a PATH is at the start of the command string, it should not be replaced or referenced. For example, `/usr/bin/python /home/user/file.txt` is not replaced or referenced, but `/usr/bin/python /home/user/file.txt` is replaced with `/usr/bin/python PATH` and referenced as `5`.
- Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC". For example, `echo 123456789` is replaced with `echo NUMERIC`.
- Replace valid hostnames with the string "HOSTNAME". A valid hostname follows the regex pattern defined in the global variable `hostname_pattern`. For example, `p2eavwaabc01.intraPRD.abc.com.sg` is replaced with `HOSTNAME_5`.

### How the References are Generated
Reference values are generated using the index number of the original value in `OriginalReferencesDataframe`, and are stored as a comma-separated list in a new Reference column of the input dataframe. The `OriginalReferencesDataframe` dataframe has an Index column that corresponds to the reference suffixes.

### Example Scenarios for PATH

The following are some examples of test cases and scenarios that demonstrate how the program should simplify and replace the command strings in the input CSV file.

#### Test case 1

The input CSV file contains a command string that starts with a path and has another path in the middle. The program should not replace or reference the first path, but should replace and reference the second path. For example, the input dataframe before processing:

| Command/Events | Reference |
| -------------- | --------- |
| /usr/bin/python /home/user/file.txt |  |

The input dataframe after processing:

| Command/Events | Reference |
| -------------- | --------- |
| /usr/bin/python PATH | [1] |

The `OriginalReferencesDataframe` dataframe should contain:

| Index | Value | Count |
| ----- | ----- | ----- |
| 1 | /home/user/file.txt | 1 |

The pivot table should contain:

| Command/Events | Reference |
| -------------- | --------- |
| /usr/bin/python PATH | 1 |

## Simplify and Replace Function

The `simplify_and_replace` function processes a command string as an argument. It returns a simplified string and a list of original strings that were replaced. The simplified string is derived from the command string by replacing the original strings with the replacement strings. Both the original and replacement strings are returned in the same order as they appear in the command string.

## Generate References Function

The program defines a function `generate_references` that takes a list of original strings and the `OriginalReferencesDataframe` dataframe as arguments and returns a reference value using the reference generation rules.

- The reference value is a list of integers of the reference values that correspond to the index of the original strings in the `OriginalReferencesDataframe` dataframe in the same order as they appear in the command string.
- The function modifies the `OriginalReferencesDataframe` dataframe in place according to the reference generation rules. The `OriginalReferencesDataframe` dataframe contains the original values and their counts in two columns: "Value" and "Count".

The function uses the following logic and algorithm to perform the reference generation:

- Initialize the reference value as an empty list
- For each original string, do the following:
  - Check if the original string is already in the `OriginalReferencesDataframe` dataframe
  - If yes, get the index of the original string in the `OriginalReferencesDataframe` dataframe
  - Increment the count of the original string in the `OriginalReferencesDataframe` dataframe by one
  - If no, get the index of the original string as the length of the `OriginalReferencesDataframe` dataframe
  - Append the original string and its count to the `OriginalReferencesDataframe` dataframe
  - Generate the reference value by appending the index number to the list
- Return the reference value


For example, if the command string is:

```python
/usr/bin/python /home/user/file.txt
```

The simplified string will be:

```python
/usr/bin/python PATH
```

The original list will be:

```python
["/home/user/file.txt"]
```

The replacement list will be:

```python
["PATH"]
```

The function uses the following logic and algorithm to perform the simplification and replacement:

The program simplifies and replaces the command strings with simplified strings and references using the following steps:

- Define the arrays of regex strings for the match patterns and replacement strings
- For each command string, do the following:
  - Initialize the simplified string and the lists of original and replacement strings
  - For each pattern, do the following:
    - Find the part of the command string that matches the pattern using `re.match` and `group(0)`
    - If the part is a path and it is at the start of the command string, do not replace or reference it
    - Otherwise, replace the part with the corresponding replacement string and add it to the lists of original and replacement strings
- Replace the match with the replacement string
- Append the match to the list of original strings
- Append the replacement string to the list of replacement strings
- Return the simplified string, the list of original strings, and the list of replacement strings

## Program State

The program maintains a state, saved to a 'program_state.pkl' file, which includes the file name, input dataframe, `OriginalReferencesDataframe` dataframe, and a counter variable; this state is loaded if it exists and matches the current file, and is deleted after the output file is saved. The program saves the state every time it processes 0.5% of the total lines and resumes from the previous state at the line indicated by the counter value.

## Logic and Algorithm

The program uses the following logic and algorithm to simplify and analyze the command strings in the CSV files:

- Import the modules os, sys, glob, pandas, numpy, re, time and pickle.
- Define a global variable `hostname_pattern` that contains the regex pattern for valid hostnames.
- Define a function `simplify_and_replace` that takes a command string as an argument and returns a simplified string and a list of original strings that were replaced using the simplification and replacement rules. 
- In simplify_and_replace, the regex strings and replacement strings should be in arrays to help reduce repetition in the code.
- Define a function `generate_references` that takes a list of original strings and the `OriginalReferencesDataframe` dataframe as arguments and returns a reference value and an updated `OriginalReferencesDataframe` dataframe using the reference generation rules.
- Define a function `save_state` that takes the file name, the input dataframe, the `OriginalReferencesDataframe` dataframe, and the counter as arguments and saves them to the state file using the pickle module.
- Define a function `load_state` that takes the file name as an argument and loads the program state from the state file if it exists and the file name matches the current file. It returns the input dataframe, the `OriginalReferencesDataframe` dataframe, and the counter. If the state file does not exist or the file name does not match, it returns None, None, and 0.
- Define a function `delete_state` that deletes the state file if it exists.
- Define a function `write_output` that takes the file name, the input dataframe, the `OriginalReferencesDataframe` dataframe, and the pivot table as arguments and writes them to the output Excel file in separate tabs using the `to_excel` method of pandas with the `index=True` argument to preserve the index of the dataframes.
- The program will also check if the input dataframe exceeds the maximum number of rows per sheet allowed by Excel, which is 1048576. If the input dataframe is too large, the program will split it into smaller chunks and write them to different sheets in the output Excel file. The sheet names will be based on the original sheet name, with a suffix consisting of an underscore, and then the record number of the next record. For example, if the input dataframe has 2000000 rows, the program will write the first 1048575 rows to a sheet named “Simplified”, and the remaining 951425 rows to a sheet named “Simplified_1048576”. This needs to take into account the row taken up by the header row at the top of each sheet.
- Define a function `process_file` that takes the file name as an argument and performs the following steps:
  - Load the program state from the state file using the `load_state` function and assign the returned values to `input_df`, `original`, and `counter`.
  - If `input_df` and `original` are None, create an empty dataframe named `original` with two columns: "Value" and "Count", then read in the CSV file and store it in a pandas dataframe named `input_df`.
  - Get the total number of rows in the `input_df` dataframe and assign it to a variable named `total`.
  - Assign the current time to a variable named `start_time`.
  - Loop through the rows of the `input_df` dataframe starting from the `counter` value and get the command string from the "Command/Events" column.
  - Simplify and replace the command string with the simplified string and the list of original strings using the `simplify_and_replace` function.
  - Every time the counter is a multiple of 0.5% of the total number of lines, do the following:
    - Call the save_state function with the file name, the input dataframe, the `OriginalReferencesDataframe` dataframe, and the counter as arguments. This will save the current progress of the program to a state file.
    - Print a message to the standard output that shows how many lines have been processed and what percentage of the total that is.
    - Calculate the average time per line and the remaining time based on the current time and the start time. Print a message to the standard output that shows the estimated time to finish the program.
  - Generate the reference value using the `generate_references` function with the list of original strings and the `OriginalReferencesDataframe` dataframe as arguments.
    - Update the `input_df` dataframe with the simplified string and the reference value in a new column named "Reference".
    - Increment the `counter` by one.
  - After the loop is finished, create a pivot table of the simplified commands and their counts using the `pivot_table` function of pandas. The pivot table has the simplified command strings as the index and the counts as the values.
  - Write the `input_df`, the `original` dataframe and the pivot table to the output Excel file using the `write_output` function.
  - Delete the state file using the `delete_state` function.
- Loop through all the CSV files in the current directory using the glob module and the pattern "*.csv".
- For each CSV file, call the `process_file` function with the file name as an argument.

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
r"(?P<environment>[p|t|q])(?P<location>[2|3])(?P<segment>[e|a])(?P<tier>[a|d|g|i|m|w])(?P<virtualization>[v|p])(?P<operating_system>[w|x|r|s|k])(?P<application>[a-z0-9]{3,4})(?P<server>[0-9]{2})(?:\.(?P<intra_inter>(intra|inter))(?P<suffix_env>(PRD|QAT))\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+)?\b"
```

This regex matches any string that follows the hostname format of:

[environment][location][segment][tier][virtualization][operating_system][application][server].suffix

- Each component has a specific meaning and a set of valid characters, as described below:

    - Environment: This component indicates the environment type of the server. It can be one of the following values:
        - Production (p): This indicates that the server is used for production purposes, such as hosting live applications or services.
        - Training (t): This indicates that the server is used for training purposes, such as providing a sandbox environment for learning or testing.
        - Quality (q): This indicates that the server is used for quality assurance purposes, such as performing verification or validation tests on applications or services.
    - Location: This component indicates the location code of the server. It can be either 2 or 3, depending on the region where the server is located. For example, 2 for Singapore, 3 for Tokyo, etc.
    - Segment: This component indicates the business segment of the server. It can be one of the following values:
        - Internet (e): This indicates that the server is used for internet-facing applications or services, such as web portals or APIs.
        - Intranet (a): This indicates that the server is used for internal applications or services, such as intranet sites or databases.
    - Tier: This component indicates the server tier of the server. It can be one of the following values:
        - App server (a): This indicates that the server is used for application logic or processing, such as running scripts or programs.
        - Database server (d): This indicates that the server is used for data storage or retrieval, such as hosting databases or files.
        - Gateway server (g): This indicates that the server is used for network communication or routing, such as providing access to other servers or networks.
        - Integration server (i): This indicates that the server is used for data integration or transformation, such as performing ETL (Extract, Transform, Load) operations or data cleansing.
        - Management server (m): This indicates that the server is used for management or administration, such as providing monitoring or security functions.
        - Web server (w): This indicates that the server is used for web presentation or delivery, such as hosting web pages or static content.
    - Virtualization: This component indicates the server type of the server. It can be one of the following values:
        - Virtual server (v): This indicates that the server is a virtual machine or a container, running on a physical host or a cloud platform.
        - Physical server (p): This indicates that the server is a physical machine or a bare metal server, running on dedicated hardware or a data center.
    - Operating System: This component indicates the operating system of the server. It can be one of the following values:
        - Windows (w): This indicates that the server is running on a Windows operating system, such as Windows Server or Windows 10.
        - Appliance with proprietary OS (x): This indicates that the server is running on a proprietary operating system, such as a network appliance or a security device.
        - Redhat (r): This indicates that the server is running on a Redhat operating system, such as Redhat Enterprise Linux or Redhat OpenShift.
        - SuSE (s): This indicates that the server is running on a SuSE operating system, such as SuSE Linux Enterprise or SuSE Cloud.
        - KMS appliance with proprietary OS (k): This indicates that the server is running on a proprietary operating system, specifically for a Key Management System (KMS) appliance.
    - Application: This component indicates the application identifier of the server. It can be a unique 3 or 4 character identifier for the application type, such as tns for Tenable, kms for Key Management System, etc.
    - Server: This component indicates the server identifier of the server. It can be a two-digit number indicating the server identifier within its specific application or type, such as 01, 02, 03, etc.
    - Suffix: This component is optional and indicates the intra/inter network, the suffix environment, and the sensitive values XXX, TLD, and YY of the server. It can be one of the following formats:
        - intraprd.XXX.TLD.YY: This indicates that the server is in the intranet network, the suffix environment is production, and the sensitive values are XXX, TLD, and YY. For example, intraprd.abc.com.sg.
        - interqat.XXX.TLD.YY: This indicates that the server is in the internet network, the suffix environment is quality or training, and the sensitive values are XXX, TLD, and YY. For example, interqat.abc.com.sg.

The environment, segment, intra_inter, and suffix_env must be consistent. For example, if the environment is production, the suffix_env must be prd. If the segment is intranet, the intra_inter must be intra. The suffix components must match the sensitive values for XXX, TLD, and YY. For example, if XXX is abc, TLD is com, and YY is sg, the suffix must be intraprd.abc.com.sg or interprd.abc.com.sg. The hostname must be converted to lowercase using casefold() before matching the regex and the specifications. This is to avoid case sensitive issues. For example, P2EAVWAABC01.INTRAPRD.ABC.COM.SG and p2eavwaabc01.intraprd.abc.com.sg are considered the same hostname.

## Input and Output
The program processes a CSV file, which must have a column named 'Command/Events', as input and generates an Excel file as output. The output file includes four tabs: 'Simplified' (input dataframe with simplified strings and references), 'Original' (original values and counts), 'Pattern Counts' (counts of simplified values), and 'Command Patterns' (pivot table of simplified values and counts); the output file name is derived from the source file name by appending a '_simplified' suffix."
