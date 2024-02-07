# Import the required modules
import os
import re
import pandas as pd

# Define the sensitive values for XXX, TLD, and YY
XXX = "abc"
TLD = "com"
YY = "sg"

# Define a function to validate the hostname format
def validate_hostname(hostname):
    # Check if the input is a string
    if not isinstance(hostname, str):
        raise TypeError("Hostname must be a string")
    # Define the regex pattern for the hostname components
    pattern = r"(?P<environment>[p|t|q])-(?P<location>[2|3])-(?P<segment>[e|a])-(?P<tier>[a|d|g|i|m|w])-(?P<virtualization>[v|p])-(?P<operating_system>[w|x|/r|~s|k])-(?P<application>[a-z0-9]{3,4})-(?P<server>[0-9]{2})(?:\.(?P<suffix>(intra|inter)\.(PRD|QAT|TRG)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+))?\b"
    # Match the input with the pattern
    match = re.match(pattern, hostname, re.IGNORECASE)
    # Check if there is a match
    if match:
        # Get the suffix group from the match object
        suffix = match.group("suffix")
        # Check if the suffix is present
        if suffix:
            # Split the suffix by dots and get the XXX, TLD, and YY components
            suffix_parts = suffix.split(".")
            suffix_xxx = suffix_parts[2]
            suffix_tld = suffix_parts[3]
            suffix_yy = suffix_parts[4]
            # Check if the suffix components match the sensitive values
            if suffix_xxx == XXX and suffix_tld == TLD and suffix_yy == YY:
                # Return True if they match
                return True
            else:
                # Return False if they do not match
                return False
        else:
            # Return True if the suffix is not present
            return True
    else:
        # Return False if there is no match
        return False

# Define a function to sanitize the command strings
def regex_replace(command):
    # Define a list of tuples with regex and replacement string
    regex_list = [
        # Replace a single quote enclosed block of 8 characters consisting of both upper and lowercase alphanumeric characters, underscore and dash, with the string "ALPHANUM8"
        (r"'[a-zA-Z0-9_-]{8}'", "ALPHANUM8"),
        # Replace strings that resemble UNIX paths under the default directories, either not enclosed in quotes, or enclosed in matching single or double quotes, with the string "PATH"
        (r"(['\"]?/((bin|boot|dev|etc|home|lib|lib64|media|mnt|opt|proc|root|run|sbin|srv|sys|tmp|usr|var)/?)+[^'\"]*['\"]?)", "PATH"),
        # Replace numbers between 5 and 12 digits long that follow the word "echo" with the string "NUMERIC"
        (r"(echo\s+)([0-9]{5,12})", r"\1NUMERIC"),
        # Replace valid hostnames with the string "HOSTNAME"
        (r"\b([p|t|q][2|3][e|a][a|d|g|i|m|w][v|p][w|x|/r|~s|k][a-z0-9]{3,4}[0-9]{2})(?:\.(intra|inter)\.(PRD|QAT|TRG)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+))?\b", "HOSTNAME")
    ]
    # Initialize an empty list to store the replaced values with suffixes
    replaced_values = []
    # Loop through the regex list and apply each expression on the command string
    for regex, replacement in regex_list:
        # Find all the matches of the regex in the command string
        matches = re.findall(regex, command, re.IGNORECASE)
        # Initialize an empty list to store the suffixes
        suffixes = []
        # Loop through the matches and generate the suffixes
        for match in matches:
            # Check if the match is a tuple (due to capturing groups)
            if isinstance(match, tuple):
                # Get the first element of the tuple as the original value
                original = match[0]
            else:
                # Get the match as the original value
                original = match
            # Check if the original value already exists in the file specific dataframe
            if original in df_file.index:
                # Increment its count by one
                df_file.loc[original, "count"] += 1
                # Get the index of the original value as the suffix
                suffix = df_file.index.get_loc(original)
            else:
                # Add the original value to the file specific dataframe and initialize its count to one
                df_file.loc[original, "count"] = 1
                # Get the index of the original value as the suffix
                suffix = df_file.index.get_loc(original)
            # Append the suffix to the suffixes list
            suffixes.append(suffix)
            # Append the replacement string and the suffix to the replaced values list
            replaced_values.append(replacement + "_" + str(suffix))
        # Replace the matches with only the replacement string in the command string
        command = re.sub(regex, replacement, command, flags=re.IGNORECASE)
    # Return the sanitized command and the replaced values list as a tuple
    return (command, replaced_values)

# Scan the working directory for all CSV files that don't have a corresponding output file
files = [file for file in os.listdir() if file.endswith(".csv") and not os.path.exists(file.replace(".csv", "_sanitised.xlsx"))]

# Loop through the CSV files and process them one by one
for file in files:
    # Read the CSV file with the "Command / Event" column
    df_input = pd.read_csv(file, usecols=["Command / Event"])
    # Define a file specific dataframe to store the original strings and their counts
    df_file = pd.DataFrame(columns=["original", "count"])
    df_file.set_index("original", inplace=True)
    # Add a new column to the input dataframe to store the references
    df_input["References"] = None
    # Loop through the rows of the input dataframe
    for index, row in df_input.iterrows():
        # Get the command string from the "Command / Event" column
        command = row["Command / Event"]
        # Call the regex_replace function with the command string
        sanitized_command, references = regex_replace(command)
        # Update the command string with the sanitized command in the input dataframe
        df_input.loc[index, "Command / Event"] = sanitized_command
        # Update the references with the references list in the input dataframe
        df_input.loc[index, "References"] = references
    # Write the input dataframe to the first tab of an Excel file, with the sheet name "Sanitized"
    df_input.to_excel(file.replace(".csv", "_sanitised.xlsx"), sheet_name="Sanitized", index=False)
    # Write the file specific dataframe with the original values and their counts to the second tab of the same Excel file, with the sheet name "Original"
    df_file.to_excel(file.replace(".csv", "_sanitised.xlsx"), sheet_name="Original", startrow=2)
    # Create a dataframe to store the pattern counts
    df_pattern = pd.DataFrame(columns=["Pattern", "Count"])
    # Loop through the regex list and get the replacement string and the count
    for regex, replacement in regex_list:
        # Get the count of the replacement string in the file specific dataframe
        count = df_file[df_file.index.str.contains(replacement, case=False)]["count"].sum()
        # Append the replacement string and the count to the pattern dataframe
        df_pattern.loc[len(df_pattern)] = [replacement, count]
    # Write the pattern dataframe to the third tab of the same Excel file, with the sheet name "Pattern Counts"
    df_pattern.to_excel(file.replace(".csv", "_sanitised.xlsx"), sheet_name="Pattern Counts", startrow=2, index=False)
    # Create a pivot table of the sanitized values and their counts in the input dataframe
    df_pivot = df_input["Command / Event"].value_counts().reset_index()
    # Rename the columns of the pivot table to "Sanitized Value" and "Count"
    df_pivot.columns = ["Sanitized Value", "Count"]
    # Write the pivot table to the fourth tab of the same Excel file, with the sheet name "Command Patterns"
    df_pivot.to_excel(file.replace(".csv", "_sanitised.xlsx"), sheet_name="Command Patterns", startrow=2, index=False)
    # Derive the output file name from the input file name
    output_file = file.replace(".csv", "_sanitised.xlsx")
    # Print a message to indicate the completion of the processing
    print(f"Processed {file} and wrote the output to {output_file}")
