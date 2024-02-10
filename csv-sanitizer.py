# Import the required modules
import os
import re
import pandas as pd

# Define the sensitive values for XXX, TLD, and YY
XXX = "abc"
TLD = "com"
YY = "sg"

# Define the global variable for the hostname regex pattern
HOSTNAME_PATTERN = r"(?P<environment>[p|t|q])-(?P<location>[2|3])-(?P<segment>[e|a])-(?P<tier>[a|d|g|i|m|w])-(?P<virtualization>[v|p])-(?P<operating_system>[w|x|r|s|k])-(?P<application>[a-z0-9]{3,4})-(?P<server>[0-9]{2})(?:\.(?P<intra_inter>(intra|inter))(?P<suffix_env>(PRD|QAT))\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+)?\b"

# Define a function to validate the hostname format
def validate_hostname(hostname):
    # Check if the input is a string
    if not isinstance(hostname, str):
        raise TypeError("Hostname must be a string")
    # Match the input with the pattern, ignoring the case
    match = re.match(HOSTNAME_PATTERN, hostname, re.IGNORECASE)
    # Check if there is a match
    if match:
        # Get the environment, segment, intra_inter, and suffix_env groups from the match object
        environment = match.group("environment").lower()
        segment = match.group("segment").lower()
        intra_inter = match.group("intra_inter")
        suffix_env = match.group("suffix_env")
        # Check if the environment, segment, intra_inter, and suffix_env are consistent
        if environment == "p" and suffix_env and suffix_env.lower() != "prd":
            # Return False if the environment is production but the suffix environment is not PRD
            return False
        if environment in ["t", "q"] and suffix_env and suffix_env.lower() != "qat":
            # Return False if the environment is training or quality but the suffix environment is not QAT
            return False
        if segment == "a" and intra_inter and intra_inter.lower() != "intra":
            # Return False if the segment is intranet but the intra_inter is not intra
            return False
        if segment == "e" and intra_inter and intra_inter.lower() != "inter":
            # Return False if the segment is internet but the intra_inter is not inter
            return False
        # Check if the suffix is present
        if intra_inter and suffix_env:
            # Split the suffix by dots and get the XXX, TLD, and YY components
            suffix_parts = hostname.split(".")
            suffix_xxx = suffix_parts[2].lower()
            suffix_tld = suffix_parts[3].lower()
            suffix_yy = suffix_parts[4].lower()
            # Check if the suffix components match the sensitive values
            if suffix_xxx == XXX.lower() and suffix_tld == TLD.lower() and suffix_yy == YY.lower():
                # Return True if they match
                return True
            else:
                # Return False if they do not match
                return False
        else:
            # Return True if the suffix is not present and the other components are valid
            return True
    else:
        # Return False if there is no match
        return False

# Define a function to replace the command strings with sanitized strings and references
def regex_replace(command):
    # Define the regex patterns and replacement strings
    patterns = [r"'[A-Za-z0-9_-]{8}'", r"(/[^/\s]+)+|('[^']+')|(\"[^\"]+\")", r"(?<=echo )\d{5,12}", HOSTNAME_PATTERN]
    replacements = ["ALPHANUM8", "PATH", "NUMERIC", "HOSTNAME"]
    # Initialize an empty list to store the references
    references = []
    # Loop through the patterns and replacements
    for pattern, replacement in zip(patterns, replacements):
        # Find all the matches in the command string
        matches = re.findall(pattern, command)
        # Loop through the matches
        for match in matches:
            # Check if the match is a valid hostname
            if replacement == "HOSTNAME" and not validate_hostname("".join(match)):
                # Skip the match if it is not a valid hostname
                continue
            # Check if the match already exists in the references list
            if match not in references:
                # Append the match to the references list
                references.append(match)
            # Get the index of the match in the references list
            index = references.index(match)
            # Replace the match with the replacement string and the index as the suffix
            command = command.replace("".join(match), replacement + "_" + str(index))
    # Return the sanitized command string and the references list as a tuple
    return (command, references)

# Get the current working directory
cwd = os.getcwd()
# Get the list of files in the directory
files = os.listdir(cwd)
# Loop through the files
for file in files:
    # Check if the file is a CSV file and does not have a corresponding output file
    if file.endswith(".csv") and not os.path.exists(file[:-4] + "_sanitised.xlsx"):
        # Print a message indicating the file is being processed
        print(f"Processing {file}...")
        # Read the CSV file as a pandas dataframe
        df = pd.read_csv(file)
        # Check if the dataframe has the "Command/Events" column
        if "Command/Events" in df.columns:
            # Create a file specific dataframe to store the original strings and their counts
            original_df = pd.DataFrame(columns=["original", "count"])
            # Create a new column in the input dataframe to store the references
            df["References"] = ""
            # Loop through the rows of the input dataframe
            for i, row in df.iterrows():
                # Get the command string from the row
                command = row["Command/Events"]
                # Replace the command string with the sanitized string and the references
                sanitized, references = regex_replace(command)
                # Update the row with the sanitized string and the references
                df.loc[i, "Command/Events"] = sanitized
                df.loc[i, "References"] = references
                # Loop through the references
                for reference in references:
                    # Check if the reference already exists in the original dataframe
                    if reference in original_df["original"].tolist():
                        # Increment the count of the reference by one
                        original_df.loc[original_df["original"] == reference, "count"] += 1
                    else:
                        # Add the reference and its count to the original dataframe
                        original_df = pd.concat([original_df, pd.DataFrame({"original": [reference], "count": [1]})], ignore_index=True)
            # Create a dataframe to store the pattern counts
            pattern_df = pd.DataFrame(columns=["pattern", "count"])
            # Loop through the unique values in the original dataframe
            for value in original_df["original"].unique():
                # Get the pattern of the value by removing the suffix
                pattern = value.split("_")[0]
                # Check if the pattern already exists in the pattern dataframe
                if pattern in pattern_df["pattern"].values:
                    # Increment the count of the pattern by the count of the value
                    pattern_df.loc[pattern_df["pattern"] == pattern, "count"] += original_df.loc[original_df["original"] == value, "count"].values[0]
                else:
                    # Add the pattern and its count to the pattern dataframe
                    pattern_df = pattern_df.append({"pattern": pattern, "count": original_df.loc[original_df["original"] == value, "count"].values[0]}, ignore_index=True)
            # Create a pivot table of the sanitized values and their counts
            pivot_df = df.pivot_table(index="Command/Events", values="References", aggfunc="count")
            # Rename the pivot table column
            pivot_df.rename(columns={"References": "count"}, inplace=True)
            # Write the input dataframe to the first tab of an Excel file
            writer = pd.ExcelWriter(file[:-4] + "_sanitised.xlsx", engine="xlsxwriter")
            df.to_excel(writer, sheet_name="Sanitized", index=False)
            # Write the original dataframe to the second tab of the same Excel file
            original_df.to_excel(writer, sheet_name="Original", index=False)
            # Write the pattern dataframe to the third tab of the same Excel file
            pattern_df.to_excel(writer, sheet_name="Pattern Counts", index=False)
            # Write the pivot table to the fourth tab of the same Excel file
            pivot_df.to_excel(writer, sheet_name="Command Patterns", index=True)
            # Save and close the Excel file
            writer.save()
            writer.close()
            # Print a message indicating the file is processed
            print(f"Processed {file} and saved as {file[:-4] + '_sanitised.xlsx'}")
