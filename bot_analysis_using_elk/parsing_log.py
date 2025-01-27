import os
import re
import json
from user_agents import parse

# Parse a single log entry into a dictionary
def parse_log_entry(log_data):
    fields = {}
    pattern = r"^\s*(.+?):\s*(.*?)\s*$"  # Key-value pair extraction
    
    for line in log_data.strip().split("\n"):
        match = re.match(pattern, line)
        if match:
            key, value = match.groups()
            fields[key.strip()] = value.strip()

    # No need for browser field
    return fields if fields else None

# Read and parse a file
def parse_log_file(file_path):
    parsed_logs = []
    with open(file_path, "r") as file:
        data = file.read()
        entries = data.split("***************************")
        for entry in entries:
            if entry.strip():
                parsed_entry = parse_log_entry(entry)
                if parsed_entry:  # Exclude empty objects
                    parsed_logs.append(parsed_entry)
    return parsed_logs

# Parse all files in a directory
def parse_logs_from_directory(directory):
    all_logs = []
    for file_name in os.listdir(directory):
        if file_name.endswith(".txt"):  # Process only .log files
            file_path = os.path.join(directory, file_name)
            print(f"Parsing file: {file_path}")
            file_logs = parse_log_file(file_path)
            if file_logs:  # Exclude empty lists
                all_logs.extend(file_logs)
    return all_logs

# Save parsed logs to a custom format
def save_parsed_logs_to_file(parsed_logs, output_file):
    if parsed_logs:  # Ensure no empty list is saved
        with open(output_file, "w") as file:
            for log in parsed_logs:
                file.write(json.dumps(log) + "\n")  # Write each object on a new line
        print(f"Parsed logs saved to: {output_file}")
    else:
        print("No valid logs to save.")

# Main script execution
if __name__ == "__main__":
    # Directory containing your log files
    log_directory = "/home/ubuntu/bot_analysis"
    
    # Parse all logs from all files
    all_parsed_logs = parse_logs_from_directory(log_directory)
    
    # Save the parsed logs to a JSON file
    output_file = "/home/ubuntu/bot_analysis/parsed_logs.ndjson"  # Use .ndjson for newline-delimited JSON
    save_parsed_logs_to_file(all_parsed_logs, output_file)
    
    # Print summary
    print(f"Total logs parsed: {len(all_parsed_logs)}")
