# Import the required modules
import os
import re
import time
import pickle
import pandas as pd
from itertools import islice

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
    patterns = [r"'[A-Za-z0-9_-]{8}'", r"(/(bin|boot|dev|etc|home|lib|lib64|media|mnt|opt|proc|root|run|sbin|srv|sys|tmp|usr|var)(/[^/\s]+)*)|('[^']+')|(\"[^\"]+\")", r"(?<=echo )\d{5,12}", HOSTNAME_PATTERN]
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
        # Check if the program state file exists
        if os.path.exists("state.pkl"):
            # Load the program state from the file
            with open("state.pkl", "rb") as f:
                state = pickle.load(f)
            # Get the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable from the state
            file_name = state["file_name"]
            df = state["df"]
            original_df = state["original_df"]
            pattern_df = state["pattern_df"]
            pivot_df = state["pivot_df"]
            counter = state["counter"]
            # Check if the file name matches the current file
            if file_name == file:
                # Print a message indicating the program is resuming from the previous state
                print(f"Resuming from the previous state at line {counter + 1}...")
            else:
                # Print a message indicating the program is starting from the beginning
                print(f"Starting from the beginning...")
                # Read the CSV file as a pandas dataframe
                df = pd.read_csv(file)
                # Create a file specific dataframe to store the original strings and their counts
                original_df = pd.DataFrame(columns=["original", "count"])
                # Create a new column in the input dataframe to store the references
                df["References"] = ""
                # Create a dataframe to store the pattern counts
                pattern_df = pd.DataFrame(columns=["pattern", "count"])
                # Create a pivot table of the sanitized values and their counts
                pivot_df = df.pivot_table(index="Command/Events", values="References", aggfunc="count")
                # Rename the pivot table column
                pivot_df.rename(columns={"References": "count"}, inplace=True)
                # Initialize the counter variable to zero
                counter = 0
        else:
            # Read the CSV file as a pandas dataframe
            df = pd.read_csv(file)
            # Create a file specific dataframe to store the original strings and their counts
            original_df = pd.DataFrame(columns=["original", "count"])
            # Create a new column in the input dataframe to store the references
            df["References"] = ""
            # Create a dataframe to store the pattern counts
            pattern_df = pd.DataFrame(columns=["pattern", "count"])
            # Create a pivot table of the sanitized values and their counts
            pivot_df = df.pivot_table(index="Command/Events", values="References", aggfunc="count")
            # Rename the pivot table column
            pivot_df.rename(columns={"References": "count"}, inplace=True)
            # Initialize the counter variable to zero
            counter = 0
        # Get the number of lines to be processed from the input dataframe
        total_lines = len(df)
        # Calculate the threshold for printing the status update as 0.5% of the total lines
        threshold = int(total_lines * 0.005)
        # Get the current time as the start time
        start_time = time.time()
        # Loop through the rows of the input dataframe from the counter value
        for i, row in islice(df.iterrows(), counter, None):
            # Get the command string from the row
            command = row["Command/Events"]
            # Replace the command string with the sanitized string and the references
            sanitized, references = regex_replace(command)
      # Increment the counter by one
        counter += 1
        # Check if the counter reaches the threshold
        if counter % threshold == 0:
            # Calculate the percentage of completion
            percentage = round(counter / total_lines * 100, 2)
            # Get the current time as the end time
            end_time = time.time()
            # Calculate the elapsed time
            elapsed_time = end_time - start_time
            # Calculate the remaining time
            remaining_time = elapsed_time / percentage * (100 - percentage)
            # Format the elapsed time and the remaining time as hh:mm:ss
            elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            remaining_time_str = time.strftime("%H:%M:%S", time.gmtime(remaining_time))
            # Print the status update with the percentage, the elapsed time, and the estimated time of completion
            print(f"{percentage}% completed in {elapsed_time_str}. Estimated time of completion: {remaining_time_str}.")
            # Create a program state with the file name, the input dataframe, the original dataframe, the pattern dataframe, the pivot table, and the counter variable
            state = {"file_name": file, "df": df, "original_df": original_df, "pattern_df": pattern_df, "pivot_df": pivot_df, "counter": counter}
            # Save the program state to the state file
            with open("state.pkl", "wb") as f:
                pickle.dump(state, f)
              # Update the row with the sanitized string and the references
            df.loc[i, "Command/Events"] = sanitized
