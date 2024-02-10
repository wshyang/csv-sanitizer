# Functional Specification

## Overview

This program is designed to simplify and analyze the command strings in a CSV file. It replaces the command strings with simplified strings and references, and stores the original values and their counts in a separate dataframe. It also generates a pivot table of the simplified commands and their counts. It writes the output to an Excel file with three tabs: Simplified, References to Originals, and Pattern Counts.

## Input and Output

The input is a CSV file that contains the command strings in a column named "Command/Events". The output is an Excel file that contains the input dataframe with the simplified values, the references to the original values, and the pivot table of the simplified commands and their counts in separate tabs. The Simplified tab contains the input dataframe with the simplified values. The References to Originals tab contains the original values and their counts. The Pattern Counts tab contains the pivot table of the simplified commands and their counts.

## Simplification and Replacement Rules

The program simplifies and replaces the command strings with simplified strings and references using the following rules:

- The reference values are generated by appending a suffix of the index number to the simplified value. The index number is the same as the index of the original value in the references dataframe. For example, if the original value is `'aBcD_1-2'` and its index in the references dataframe is 2, the reference value will be `ALPHANUM8_2`. The reference values are stored as a comma separated list in the new Reference column of the input dataframe. The references dataframe has an Index column that corresponds to the reference suffixes. For example, if the reference value is `PATH_1`, the Index column will have the value 1. This way, the references can be easily correlated with the original values and their counts.
- Replace a single quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8". For example, `'aBcD_1-2'` is replaced with `ALPHANUM8`.
- Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH". For example, `'/usr/bin/python'` and `"/home/user/file.txt"` are replaced with `PATH` and `PATH`, respectively. However, if a PATH is at the start of the command string, it should not be replaced or referenced. For example, `/usr/bin/python /home/user/file.txt` is not replaced or referenced, but `/usr/bin/python /home/user/file.txt` is replaced with `/usr/bin/python PATH` and referenced as `PATH_5`.
- Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC". For example, `echo 123456789` is replaced with `NUMERIC_0`.
- Replace valid hostnames with the string "HOSTNAME". A valid hostname follows the regex pattern defined in the global variable `hostname_pattern`. For example, `p2eavwaabc01.intraPRD.abc.com.sg` is replaced with `HOSTNAME_5`.

### How the References are Generated
The references are generated by appending a suffix consisting of an underscore, followed by the index number to the simplified value. For example, if the simplified value is PATH, the reference value will be PATH_1, PATH_2, etc. depending on how many times the path value has been encountered and replaced in the input dataframe. The reference values are stored as a comma separated list in the new Reference column of the input dataframe. The references dataframe has an Index column that corresponds to the reference suffixes. For example, if the reference value is PATH_1, the Index column will have the value 1. This way, the references can be easily correlated with the original values and their counts.

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
| /usr/bin/python PATH | PATH_1 |

The references dataframe should contain:

| Index | Value | Count |
| ----- | ----- | ----- |
| 1 | /home/user/file.txt | 1 |

The pivot table should contain:

| Command/Events | Reference |
| -------------- | --------- |
| /usr/bin/python PATH | 1 |


## Program State

The program saves and loads the program state to and from a state file named "program_state.pkl". The program state is a dictionary that contains the following keys and values:

- "file_name": the name of the input CSV file
- "input_df": the input dataframe
- "original": the references dataframe
- "counter": the counter variable that tracks the progress of the program

The program saves the program state to the state file every time it reaches a threshold of 0.5% of the total lines to be processed. The program loads the program state from the state file if it exists and the file name matches the current file. The program resumes from the previous state at the line indicated by the counter value. The program deletes the state file after the output file is written and saved.

## Logic and Algorithm

The program uses the following logic and algorithm to simplify and analyze the command strings in the CSV files:

- Import the modules os, sys, glob, pandas, and re.
- Define a global variable `hostname_pattern` that contains the regex pattern for valid hostnames.
- Define a function `simplify_and_replace` that takes a command string as an argument and returns a simplified string and a list of original strings that were replaced using the simplification and replacement rules. 
- In simplify_and_replace, the regex strings and replacement strings should be in arrays to help reduce repetition in the code.
- Define a function `generate_references` that takes a list of original strings and the original dataframe as arguments and returns a reference value and an updated original dataframe using the reference generation rules.
- Define a function `save_state` that takes the file name, the input dataframe, the original dataframe, and the counter as arguments and saves them to the state file using the pickle module.
- Define a function `load_state` that takes the file name as an argument and loads the program state from the state file if it exists and the file name matches the current file. It returns the input dataframe, the original dataframe, and the counter. If the state file does not exist or the file name does not match, it returns None, None, and 0.
- Define a function `delete_state` that deletes the state file if it exists.
- Define a function `write_output` that takes the file name, the input dataframe, the original dataframe, and the pivot table as arguments and writes them to the output Excel file in separate tabs using the `to_excel` method of pandas with the `index=True` argument to preserve the index of the dataframes.
- Define a function `process_file` that takes the file name as an argument and performs the following steps:
  - Load the program state from the state file using the `load_state` function and assign the returned values to `input_df`, `original`, and `counter`.
  - If `input_df` and `original` are None, create an empty dataframe named `original` with two columns: "Value" and "Count", then read in the CSV file and store it in a pandas dataframe named `input_df`.
  - Get the total number of rows in the `input_df` dataframe and assign it to a variable named `total`.
  - Loop through the rows of the `input_df` dataframe starting from the `counter` value and get the command string from the "Command/Events" column.
  - Simplify and replace the command string with the simplified string and the list of original strings using the `simplify_and_replace` function.
- Generate the reference value and the updated original dataframe using the `generate_references` function with the list of original strings and the original dataframe as arguments.
  - Update the `input_df` dataframe with the simplified string and the reference value in a new column named "Reference".
  - Increment the `counter` by one.
  - Print a status message to the standard output showing the percentage of completion.
  - Save the current program state to the state file using the `save_state` function every time the `counter` reaches a multiple of 0.05% of the `total`.
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
The program takes a CSV file as the input, and writes an Excel file as the output. The input CSV file must have a column named “Command/Events” that contains the command strings to be simplified. The output Excel file will have four tabs: “Simplified”, “Original”, “Pattern Counts”, and “Command Patterns”. The “Simplified” tab will contain the input dataframe with the simplified strings and the references. The “Original” tab will contain the original values and their counts. The “Pattern Counts” tab will contain the pattern counts of the simplified values. The “Command Patterns” tab will contain the pivot table of the simplified values and their counts. The output file name will be derived from the source file name by appending a suffix of “_simplified”. For example, if the input file name is “commands.csv”, the output file name will be “commands_simplified.xlsx”.
