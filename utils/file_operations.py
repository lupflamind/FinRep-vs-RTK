import csv

def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = list(reader)
    return rows

def write_csv(file_path, title_row, data):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(title_row)
        writer.writerows(data)

def map_columns(headers, mapping):
    """
    Map columns from headers to the desired names based on a mapping dictionary.
    """
    mapped_headers = {mapping.get(header, header): idx for idx, header in enumerate(headers)}
    return mapped_headers