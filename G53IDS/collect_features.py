__author__ = 'janosbana'

import json
import os

'''
load bank holiday dates, which is a day-off into a set
'''
def load_bank_holidays(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        b_holidays = json.load(data_file)

    bank_holidays = set()
    for entry in b_holidays:
        if entry['bunting']:
            bank_holidays.add(entry['date'])

    return bank_holidays

def main():
    # paths for resources
    data_dir_path = 'data' + os.sep
    daily_sales_path = data_dir_path + 'daily_sale_figures.json'
    bank_holiday_path = data_dir_path + 'england_bankHolidays.json'

    # load daily sales json
    with open(daily_sales_path, encoding='utf-8') as data_file:
        daily_sales = json.load(data_file)

    # load important dates into sets
    bank_holidays = load_bank_holidays(bank_holiday_path)


if __name__ == '__main__':
    main()