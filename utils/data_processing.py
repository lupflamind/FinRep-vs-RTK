import csv

def find_title_row(rows):
    """
    Find the title row in the data. Assumes the title row contains 'Deal Id'.
    """
    for i, row in enumerate(rows):
        if "Deal Id" in row:
            return i, row
    return None, None

def clean_rows(rows, title_row):
    """
    Remove rows that do not match the title row length or are empty.
    """
    clean_data = []
    title_length = len(title_row)
    
    for row in rows:
        if len(row) == title_length and any(row):
            clean_data.append(row)
    return clean_data

def remove_totals(rows, title_row):
    """
    Remove rows where the 'Deal Id' column is empty or rows that are total summaries.
    """
    deal_id_index = title_row.index("Deal Id")
    filtered_data = [row for row in rows if row[deal_id_index].strip() and "Total" not in row]
    return filtered_data

def load_file(file_path):
    """
    Load a file and return its rows.
    """
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = list(reader)
    return rows

def create_combined_id(row, column_mapping, key_columns):
    """
    Create a unique ID for each row based on the specified key columns.
    """
    return tuple(row[column_mapping[col]] for col in key_columns)
