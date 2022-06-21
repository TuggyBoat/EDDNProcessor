import csv
from os.path import exists
import pandas as pd


def csv_exist_check(file_name: str):
    file_exists = exists(file_name)

    if file_exists:
        return True

    else:
        open(file_name, 'x')
        return True


# Check if value is in CSV
def csv_value_check(file_name, value, column):
    csv_exist_check(file_name)
    try:
        df = pd.read_csv(file_name, sep=',', header=None)
        check = df[df[column] == value]
        check = str(check).split(' ')[0]
    except:
        return False

    if check == 'Empty':
        return False
    else:
        return True


# Write a list to row
def csv_write_line(_list: list, file_name: str):
    csv_exist_check(file_name)
    csv_file = open(file_name, 'r+', newline='')
    writer = csv.writer(csv_file)
    reader = csv.reader(csv_file)
    try:
        # Get last row
        row_count = sum(1 for row in reader)
        _list.insert(0, row_count + 1)

        # Write to csv
        writer.writerow(_list)
        csv_file.close()
        return row_count + 1

    except:
        csv_file.close()
        return False


def update_timestamp(file_name: str, search_criteria, timestamp, search_column: int, timestamp_column: int):
    csv_exist_check(file_name)
    csv_file = open(file_name, 'r+', newline='')
    df = pd.read_csv(file_name, sep=',', header=None)

    # Search for value in column
    try:
        search = df.loc[df[search_column] == search_criteria].index[0]
        df.at[search, timestamp_column] = timestamp
    except:
        print('Failed to update timestamp.')
        return False

    return True

