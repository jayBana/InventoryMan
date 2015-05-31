__author__ = 'janosbana'

import json
import os
from datetime import timedelta, date

# load uni key dates
def load_uni_key_dates(file_path):
    # open json and load info into sets
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)

    # create sets for Uni of Nottingham
    uon_welcome = set()
    uon_term = set()
    uon_graduation = set()
    uon_exam = set()
    uon_sets = [uon_welcome, uon_term, uon_graduation, uon_exam]

    # create sets for Trent Uni
    trent_welcome = set()
    trent_term = set()
    trent_graduation = set()
    trent_exam = set()
    trent_sets = [trent_welcome, trent_term, trent_graduation, trent_exam]

    # add dates from json to set
    for entry in data:
        # get start and end date and calculate the number of days between them
        start = entry['start'].split('-')
        end = entry['end'].split('-')
        start_date = date(int(start[0]), int(start[1]), int(start[2]))
        end_date = date(int(end[0]), int(end[1]), int(end[2]))
        delta = end_date - start_date

        # save dates into sets for each entry
        for d in range(delta.days + 1):
            new_date = start_date + timedelta(days=d)
            add_date = new_date.strftime(("%Y-%m-%d"))

            if entry['type'] == 'welcome':
                index = 0
            elif entry['type'] == 'term':
                index = 1
            elif entry['type'] == 'graduation':
                index = 2
            elif entry['type'] == 'exam':
                index = 3

            if entry['uni'] == 'uon':
                uon_sets[index].add(add_date)
            else:
                trent_sets[index].add(add_date)

    uni_key_dates = [uon_sets, trent_sets]
    return uni_key_dates


# load school days into sets
def load_school_days(file_path):
    # open json
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)

    # set to hold school days
    school_days = set()

    # save each date to appropriate set
    for entry in data:
        # get start and end date and calculate the number of days between them
        start = entry['start'].split('-')
        end = entry['end'].split('-')
        start_date = date(int(start[0]), int(start[1]), int(start[2]))
        end_date = date(int(end[0]), int(end[1]), int(end[2]))
        delta = end_date - start_date

        # create and add new date between start and end
        for d in range(delta.days + 1):
            new_date = start_date + timedelta(days=d)
            school_days.add(new_date.strftime("%Y-%m-%d"))

    return school_days


# load bank holiday dates, which is a day-off into a set
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
    city_days_path = data_dir_path + 'nottcity_SchoolHolidays.json'
    county_days_path = data_dir_path + 'nottshire_SchoolHolidays.json'
    uni_key_dates_path = data_dir_path + 'uni_key-dates.json'

    # load daily sales json
    with open(daily_sales_path, encoding='utf-8') as data_file:
        daily_sales = json.load(data_file)

    # load important dates into sets
    bank_holidays = load_bank_holidays(bank_holiday_path)
    city_school_days = load_school_days(city_days_path)
    county_school_days = load_school_days(county_days_path)
    uni_key_dates = load_uni_key_dates(uni_key_dates_path)


if __name__ == '__main__':
    main()
