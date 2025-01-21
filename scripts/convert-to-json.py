#!/usr/bin/env python3

import os
import csv
import json
import argparse

def convert_csv_to_json(input_csv_path, output_json_path):
    """
    Read the CSV file content and write it to a JSON file.
    By default, each row is stored as a dictionary based on the CSV header.
    For example, if CSV columns are (Name, Age), rows become:
      [
        {"Name": "Alice", "Age": "30"},
        {"Name": "Bob",   "Age": "25"}
      ]
    """
    with open(input_csv_path, 'r', encoding='utf-8') as f:
        # Use DictReader to automatically parse the first row as field names
        csv_reader = csv.DictReader(f)
        rows = list(csv_reader)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Write rows to JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def process_directory(input_dir, output_dir=None):
    """
    Recursively walk through the input_dir.
    For every .csv file found, create a corresponding .json file.

    If output_dir is specified, the JSON files will be created under that directory
    with the same relative structure as input_dir.
    If output_dir is None, the JSON files will be created next to each .csv file.
    """
    if not output_dir:
        # If output_dir is not specified, write .json next to each .csv file
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if filename.lower().endswith('.csv'):
                    csv_path = os.path.join(root, filename)
                    json_path = os.path.splitext(csv_path)[0] + '.json'
                    convert_csv_to_json(csv_path, json_path)
        return

    # If output_dir is specified, mirror the structure under output_dir
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith('.csv'):
                csv_path = os.path.join(root, filename)
                # Calculate the relative path of the current file to input_dir
                rel_path = os.path.relpath(csv_path, start=input_dir)
                # Replace the .csv extension with .json
                rel_json_path = os.path.splitext(rel_path)[0] + '.json'
                # Build the final output path under output_dir
                output_json_path = os.path.join(output_dir, rel_json_path)
                convert_csv_to_json(csv_path, output_json_path)


def main():
    parser = argparse.ArgumentParser(
        description="Recursively find and convert .csv files into corresponding .json files."
    )
    parser.add_argument("input_dir", help="Path to the directory to search for .csv files.")
    parser.add_argument(
        "--output_dir",
        help="Path to the directory where .json files will be placed. "
             "If not provided, .json files will be created next to each .csv file.",
        default=None
    )

    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()