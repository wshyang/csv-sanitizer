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
- It defines a global variable for the hostname regex pattern, which is used to validate and replace the hostnames in the command strings.
- It defines a function `regex_replace` that takes a string as an input and returns a tuple of two elements: the sanitized string and the references list. The function applies a series of regex replacements on each command string to sanitize them. The regex replacements are as follows:
    - Replace a single quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8".
    - Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH".
    - Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC".
    - Replace valid hostnames with the string "HOSTNAME".
- It stores the original values and their counts in a dataframe specific for each file, and checks if the value already exists in the dataframe before adding it to the dataframe. The index of the original value in the dataframe is used as the suffix for the replacement string, preceded by an underscore.
- It adds a new column to the input dataframe to store the references, which are the replacement strings with the suffixes. The command strings in the input dataframe are updated with the sanitized command strings, which are the replacement strings without the suffixes.
- It writes the input dataframe to the first tab of an Excel file, with the sheet name "Sanitized".
- It writes the file specific dataframe with the original values and their counts to the second tab of the same Excel file, with the sheet name "Original".
- It creates a dataframe to store the pattern counts, which are the replacement strings and their counts in the file specific dataframe. It writes the pattern dataframe to the third tab of the same Excel file, with the sheet name "Pattern Counts".
- It creates a pivot table of the sanitized values and their counts in the input dataframe. It writes the pivot table to the fourth tab of the same Excel file, with the sheet name "Command Patterns".

## Hostname Format and Validation

- A hostname is a string that uniquely identifies a server in a network.
- A hostname consists of seven components, separated by hyphens, that indicate various attributes such as environment, location, segment, tier, virtualization, operating system, and application.
- A hostname may also have an optional suffix, preceded by a dot, that indicates the intra/inter network, the suffix environment, and the sensitive values XXX, TLD, and YY.
- The format of a hostname is as follows:

`environment-location-segment-tier-virtualization-operating_system-application-server.suffix`

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
        - intraPRD.XXX.TLD.YY: This indicates that the server is in the intranet network, the suffix environment is production, and the sensitive values are XXX, TLD, and YY. For example, intraPRD.abc.com.sg.
        - interQAT.XXX.TLD.YY: This indicates that the server is in the internet network, the suffix environment is quality or training, and the sensitive values are XXX, TLD, and YY. For example, interQAT.abc.com.sg.

- To validate a given hostname string, a function can be defined that uses the global hostname regex pattern to match each component of the hostname according to the specified requirements. The function returns True if the hostname matches the pattern and is consistent with the environment, segment, and suffix, and False otherwise. The function also raises a TypeError if the input hostname is not a string.

## Error Handling

The script handles any errors or exceptions gracefully, and provides informative messages to the user. Some possible errors or exceptions are:

- The input hostname is not a string.
- The input hostname does not match the specified pattern.
- The input file is not a CSV file or does not have the "Command/Events" column.
- The output file already exists or cannot be written.

## Assumptions

The script makes the following assumptions:

- The provided hostname string contains alphanumeric characters only.
- The script does not perform DNS resolution or check network connectivity.
- The script does not validate the existence of the server or its configuration; it only validates the format of the hostname string.
- The CSV files that need to be sanitized are placed in the same directory as the script.
- The CSV files have a column named "Command/Events" that contains the command strings that need to be sanitized.
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
