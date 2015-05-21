#!/usr/bin/python3

'''
script that appends features to each ingredient and product file
'''

import os.path
import json
from os.path import isfile, join
from posix import listdir
from datetime import datetime, timedelta, date
from openpyxl import load_workbook

# loads all school holiday related info from json to a set
def load_schooldays(file_path):
    with open(file_path, encoding='utf-8') as data_file:
        data = json.load(data_file)

    school_days = set()

    for entry in data:
        start = entry['start'].split('-')
        end = entry['end'].split('-')

        start_date = date(int(start[0]), int(start[1]), int(start[2]))
        end_date = date(int(end[0]), int(end[1]), int(end[2]))

        delta = end_date - start_date

        for d in range(delta.days + 1):
            new_date = start_date + timedelta(days=d)
            school_days.add(new_date.strftime("%Y-%m-%d"))

    return school_days


# load all data into global sets just once
def load_all_data(data_dir_path):
    ### DAILY SALES ###
    global weekly_sales
    global daily_sales

    # daily sales json path
    daily_sales_path = data_dir_path + 'peData' + os.sep + 'daily_sale_figures.json'

    # load json as dictionary
    with open(daily_sales_path, encoding='utf-8') as data_file:
        daily_sales = json.load(data_file)

    # calculate weekly total sales
    weekly_sales = {}
    for k, v in daily_sales.items():
        # create date object from key string
        day_date = datetime.strptime(k, "%Y-%m-%d").date()
        # create key from date object (YYYY-MM format)
        week_no = str(day_date.isocalendar()[0]) + '-' + str(day_date.isocalendar()[1])
        # sum up daily sales for each week
        weekly_sales[week_no] = weekly_sales[week_no] + v if week_no in weekly_sales else v

    # save weekly sales as json to the same place as daily sales
    fp = data_dir_path + 'weekly_sales.json'
    with open(fp, 'w', encoding='utf-8') as out_file:
        json.dump(weekly_sales, out_file)

    ### BANK HOLIDAYS ###
    global bank_holidays

    # bank holidays json path
    bank_holidays_path = data_dir_path + 'holidays' + os.sep + 'england_bankHolidays.json'

    # load bank holidays into a set
    with open(bank_holidays_path, encoding='utf-8') as data_file:
        data = json.load(data_file)
    bank_holidays = set()
    for entry in data:
        # only the ones that are actual days offs
        if entry['bunting']:
            bank_holidays.add(entry['date'])

    ### SCHOOL HOLIDAYS ###
    global city_days
    global county_days

    # school holidays json path
    city_days_path = data_dir_path + 'holidays' + os.sep + 'nottcity_SchoolHolidays.json'
    county_days_path = data_dir_path + 'holidays' + os.sep + 'nottshire_SchoolHolidays.json'

    # load school dates into sets
    city_days = load_schooldays(city_days_path)
    county_days = load_schooldays(county_days_path)

    ### UNI KEY DATES ###
    global uon_sets
    global trent_sets
    # uni key dates json path
    uni_key_dates_path = data_dir_path + 'holidays' + os.sep + 'uni_key-dates.json'

    # open json and load info into sets
    with open(uni_key_dates_path, encoding='utf-8') as data_file:
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
        start = entry['start'].split('-')
        end = entry['end'].split('-')

        start_date = date(int(start[0]), int(start[1]), int(start[2]))
        end_date = date(int(end[0]), int(end[1]), int(end[2]))
        delta = end_date - start_date

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


# appends all data to each row in each file
def append_all_data():
    # get sheet info
    highest_col = ws.get_highest_column()
    highest_row = ws.get_highest_row()

    # create headers
    ws.cell(row=1, column=highest_col + 1).value = 'Daily Sales'
    ws.cell(row=1, column=highest_col + 2).value = 'Weekly Sales'
    ws.cell(row=1, column=highest_col + 3).value = 'Day'
    ws.cell(row=1, column=highest_col + 4).value = 'Week Number'
    ws.cell(row=1, column=highest_col + 5).value = 'Year Day'
    ws.cell(row=1, column=highest_col + 6).value = 'Weekend'
    ws.cell(row=1, column=highest_col + 7).value = 'Bank Holiday'
    ws.cell(row=1, column=highest_col + 8).value = 'City School Holidays'
    ws.cell(row=1, column=highest_col + 9).value = 'County School Holidays'
    ws.cell(row=1, column=highest_col + 10).value = 'UoN Welcome Week'
    ws.cell(row=1, column=highest_col + 11).value = 'UoN Term'
    ws.cell(row=1, column=highest_col + 12).value = 'UoN Graduation'
    ws.cell(row=1, column=highest_col + 13).value = 'UoN Exam'
    ws.cell(row=1, column=highest_col + 14).value = 'Trent Welcome Week'
    ws.cell(row=1, column=highest_col + 15).value = 'Trent Term'
    ws.cell(row=1, column=highest_col + 16).value = 'Trent Graduation'
    ws.cell(row=1, column=highest_col + 17).value = 'Trent Exam'

    # do this for each row in column
    for r in range(2, highest_row + 1):
        # get date for row
        date_string = ws.cell(row=r, column=1).value
        # create date object from string
        d_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        # create key from date object (YYYY-MM format)
        week_sales_key = str(d_date.isocalendar()[0]) + '-' + str(d_date.isocalendar()[1])
        week_no = d_date.isocalendar()[1]
        day_no = d_date.isoweekday()
        d_sales = daily_sales[date_string]
        w_sales = weekly_sales[week_sales_key]
        y_day = d_date.timetuple().tm_yday
        weekend = 1 if (day_no == 6 or day_no == 7) else 0

        # sales
        ws.cell(row=r, column=highest_col + 1).value = d_sales
        ws.cell(row=r, column=highest_col + 2).value = w_sales
        # date info
        ws.cell(row=r, column=highest_col + 3).value = day_no
        ws.cell(row=r, column=highest_col + 4).value = week_no
        ws.cell(row=r, column=highest_col + 5).value = y_day
        ws.cell(row=r, column=highest_col + 6).value = weekend
        # holidays
        ws.cell(row=r, column=highest_col + 7).value = 1 if date_string in bank_holidays else 0
        ws.cell(row=r, column=highest_col + 8).value = 0 if date_string in city_days else 1
        ws.cell(row=r, column=highest_col + 9).value = 0 if date_string in county_days else 1
        # Uni of Nott key dates
        ws.cell(row=r, column=highest_col + 10).value = 1 if date_string in uon_sets[0] else 0
        ws.cell(row=r, column=highest_col + 11).value = 1 if date_string in uon_sets[1] else 0
        ws.cell(row=r, column=highest_col + 12).value = 1 if date_string in uon_sets[2] else 0
        ws.cell(row=r, column=highest_col + 13).value = 1 if date_string in uon_sets[3] else 0
        # Trent uni key dates
        ws.cell(row=r, column=highest_col + 14).value = 1 if date_string in trent_sets[0] else 0
        ws.cell(row=r, column=highest_col + 15).value = 1 if date_string in trent_sets[1] else 0
        ws.cell(row=r, column=highest_col + 16).value = 1 if date_string in trent_sets[2] else 0
        ws.cell(row=r, column=highest_col + 17).value = 1 if date_string in trent_sets[3] else 0


def main():
    # path for data files
    data_dir_path = '..' + os.sep + '..' + os.sep + 'data' + os.sep

    # path for file to be processed
    summed_dir_path = data_dir_path + 'peData' + os.sep + 'daily_summed_usage' + os.sep

    # get the list of files in the directory
    only_files = [f for f in listdir(summed_dir_path) if isfile(join(summed_dir_path, f))]

    for f in only_files:
        input_file_name = summed_dir_path + f
        # open workbook and worksheet
        wb = load_workbook(input_file_name)
        global ws
        ws = wb.get_active_sheet()

        # load data
        load_all_data(data_dir_path)

        # append data
        append_all_data()

        # save workbook
        wb.save(input_file_name)


if __name__ == "__main__":
    main()
