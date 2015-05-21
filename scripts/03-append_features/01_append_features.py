#!/usr/bin/python3

'''
script that appends features to each ingredient and product file
'''

import os.path
import json
from os.path import isfile, join
from posix import listdir
from datetime import datetime
from openpyxl import load_workbook

'''
function that adds sales data to sheet as well as date related information
'''


def append_sales():
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

    # do this for each row in column
    for r in range(2, highest_row + 1):
        # get date for row
        date = ws.cell(row=r, column=1).value
        # create date object from string
        d_date = datetime.strptime(date, "%Y-%m-%d").date()
        # create key from date object (YYYY-MM format)
        week_sales_key = str(d_date.isocalendar()[0]) + '-' + str(d_date.isocalendar()[1])
        week_no = d_date.isocalendar()[1]
        day_no = d_date.isoweekday()
        d_sales = daily_sales[date]
        w_sales = weekly_sales[week_sales_key]
        y_day = d_date.timetuple().tm_yday
        weekend = 1 if (day_no == 6 or day_no == 7) else 0

        ws.cell(row=r, column=highest_col + 1).value = d_sales
        ws.cell(row=r, column=highest_col + 2).value = w_sales
        ws.cell(row=r, column=highest_col + 3).value = day_no
        ws.cell(row=r, column=highest_col + 4).value = week_no
        ws.cell(row=r, column=highest_col + 5).value = y_day
        ws.cell(row=r, column=highest_col + 6).value = weekend


def main():
    # path for data files
    global data_dir_path
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

        # append data
        append_sales()

        # save workbook
        wb.save(input_file_name)


if __name__ == "__main__":
    main()
