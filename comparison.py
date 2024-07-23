import logging
from utils.data_processing import create_combined_id

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def compare_files(file1_filtered, file2_filtered, title_row1, title_row2, file1_column_mapping, file2_column_mapping, key_columns):
    """
    Compare two filtered files based on given column mappings and return a list of differences.
    """
    differences = []

    file1_combined_ids = [create_combined_id(row, file1_column_mapping, key_columns) for row in file1_filtered]
    file2_combined_ids = [create_combined_id(row, file2_column_mapping, key_columns) for row in file2_filtered]

    file1_dict = {id: row for id, row in zip(file1_combined_ids, file1_filtered)}
    file2_dict = {id: row for id, row in zip(file2_combined_ids, file2_filtered)}

    common_ids = set(file1_combined_ids).intersection(set(file2_combined_ids))

    for combined_id in common_ids:
        row1 = file1_dict[combined_id]
        row2 = file2_dict[combined_id]

        row1_dict = dict(zip(title_row1, row1))
        row2_dict = dict(zip(title_row2, row2))

        for column in title_row1:
            if column in title_row2 and row1_dict[column] != row2_dict[column]:
                differences.append((combined_id, column, row1_dict[column], row2_dict[column]))

    logging.debug(f"differences: {differences}")

    return differences
