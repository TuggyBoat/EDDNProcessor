import csv
from os.path import exists
import pandas as pd


def csv_exist_check():
    file_exists = exists('commodity.csv')

    if file_exists:
        return True

    else:
        open('commodity.csv', 'x')
        return True


# Check if value is in CSV
def csv_value_check(value, column):
    df = pd.read_csv('commodity.csv', sep=',', header=None)
    check = df[df[column] == value]
    check = str(check).split(' ')[0]

    if check == 'Empty':
        return False

    else:
        return True


# Write a list to row
def csv_write_commodity(_list: list):
    csv_exist_check()
    csv_file = open('commodity.csv', 'r+', newline='')
    writer = csv.writer(csv_file)
    reader = csv.reader(csv_file)
    try:
        # Get last row
        row_count = sum(1 for row in reader)
        _list[0] = row_count + 1

        # Write to csv
        writer.writerow(_list)
        csv_file.close()
        return row_count + 1

    except:
        csv_file.close()
        return False
