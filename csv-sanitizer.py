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
              # Update the row with the sanitized str
