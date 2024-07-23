import pandas as pd

# Function to find the header row dynamically and return the header and data
def extract_header_and_data(file_path, delimiter):
    header = None
    data_lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if "Deal Id" in line:
                header = [col.strip('"') for col in line.strip().split(delimiter)]
                print(f"Found header at line {i} in {file_path}")
            elif header:
                data_lines.append([col.strip('"') for col in line.strip().split(delimiter)])
    return header, data_lines

# Function to create a DataFrame from header and data
def create_dataframe(header, data):
    df = pd.DataFrame(data, columns=header)
    df.columns = df.columns.str.strip()  # Strip leading/trailing whitespace from column names
    return df

# Function to clean the DataFrame
def clean_dataframe(df):
    print("Columns in DataFrame after stripping whitespace:", df.columns.tolist())
    deal_id_col = [col for col in df.columns if 'deal id' in col.lower()]
    df_clean = df.dropna(subset=['Deal Id'])

    return df_clean, deal_id_col

# Load the data from the text files
file1 = 'fin-rep-vs-RTK/SpPos_et_FinRepPV1.txt'
file2 = 'fin-rep-vs-RTK/SpPos_et_RTK.txt'
delimiter = ';'

# Extract header and data for each file
header1, data1 = extract_header_and_data(file1, delimiter)
header2, data2 = extract_header_and_data(file2, delimiter)

# Check if headers are found
if not header1 or not header2:
    raise ValueError("Could not find the header row in one or both files.")

# Create DataFrames using the extracted header and data
df1 = create_dataframe(header1, data1)
df2 = create_dataframe(header2, data2)

# Find common columns to compare
common_columns = df1.columns.intersection(df2.columns)
print("Common columns:", common_columns.tolist())

# Filter both DataFrames to only include common columns
df1_filtered = df1[common_columns]
df2_filtered = df2[common_columns]

# Clean the DataFrames
df1_clean, deal_id_col1 = clean_dataframe(df1_filtered)
df2_clean, deal_id_col2 = clean_dataframe(df2_filtered)

# Sort DataFrames by 'Deal Id' or equivalent column to align rows for comparison
df1_sorted = df1_clean.sort_values(by=deal_id_col1).reset_index(drop=True)
df2_sorted = df2_clean.sort_values(by=deal_id_col2).reset_index(drop=True)

# Compare the values of the different rows
comparison = df1_sorted.compare(df2_sorted)

# Save the comparison result to a CSV file without excessive quotes
comparison_file = 'fin-rep-vs-RTK/comparison_result.csv'
comparison.to_csv(comparison_file, index=False, quoting=pd.io.common.csv.QUOTE_MINIMAL)

print(f"Comparison completed. Results saved to {comparison_file}.")
