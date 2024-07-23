import json
import os
from utils.data_processing import find_title_row, clean_rows, remove_totals, load_file, create_combined_id
from utils.excel_writer import write_to_excel
from comparison import compare_files

# Load configuration
with open('fin-rep-vs-RTK/config.json', 'r') as config_file:
    config = json.load(config_file)

# Define file paths
file1_path = os.path.join(config['repository'], 'input_files', f"{config['prefix']}_RTK.txt")
file2_path = os.path.join(config['repository'], 'input_files', f"{config['prefix']}_FinRep.txt")

# Load and process files
file1 = load_file(file1_path)
file2 = load_file(file2_path)

# Find and extract title rows
title_row_index1, title_row1 = find_title_row(file1)
title_row_index2, title_row2 = find_title_row(file2)

if title_row1 is None or title_row2 is None:
    raise ValueError("Title row with 'Deal Id' not found in one or both files.")

# Check that key columns are present in title rows
missing_keys_file1 = [col for col in config['key_columns'] if col not in title_row1]
missing_keys_file2 = [col for col in config['key_columns'] if col not in title_row2]

if missing_keys_file1 or missing_keys_file2:
    raise KeyError(f"Missing key columns in title rows. In file 1: {missing_keys_file1}. In file 2: {missing_keys_file2}")

# Clean the rows based on header and remove totals
file1_filtered = clean_rows(file1[title_row_index1 + 1:], title_row1)
file1_filtered = remove_totals(file1_filtered, title_row1)
file2_filtered = clean_rows(file2[title_row_index2 + 1:], title_row2)
file2_filtered = remove_totals(file2_filtered, title_row2)

# Create column mappings
file1_column_mapping = {col.strip(): index for index, col in enumerate(title_row1)}
file2_column_mapping = {col.strip(): index for index, col in enumerate(title_row2)}

print(f"File 1 column mapping: {file1_column_mapping}")
print(f"File 2 column mapping: {file2_column_mapping}")

# Key columns for comparison
key_columns = config['key_columns']

# Compare files
differences = compare_files(file1_filtered, file2_filtered, title_row1, title_row2, file1_column_mapping, file2_column_mapping, key_columns)

# Write to Excel
output_file_path = os.path.join(config['repository'], 'output_files', f"{config['prefix']}.xlsx")
write_to_excel(file1_filtered, file2_filtered, title_row1, title_row2, differences, output_file_path, config['suffix1'], config['suffix2'], key_columns, file1_column_mapping, file2_column_mapping,)
