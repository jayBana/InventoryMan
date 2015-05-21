#!/usr/bin/python3

'''
script that collects weather data from
'''

import urllib.request
import sys
import os
import time
from datetime import date, timedelta, datetime
from calendar import monthrange


def main():
    # path for files to be saved
    dir_path = '..' + os.sep + '..' + os.sep + 'data' + os.sep + 'weather' + os.sep
    # command line arguments for specifying start and end data ISO 8601 date format
    start = sys.argv[1].split('-')
    end = sys.argv[2].split('-')

    # create date objects
    start_date = date(int(start[0]), int(start[1]), int(start[2]))
    end_date = date(int(end[0]), int(end[1]), int(end[2]))

    # get today's date and create date object
    today = datetime.now().date()
    full_month = True

    # get weather data for each month between the two dates
    while start_date != end_date:
        # get the number of days for current month
        month_days_no = monthrange(start_date.year, start_date.month)[1]
        # set the end date for current iteration
        month_end = start_date + timedelta(days=month_days_no - 1)

        # case when last month is not a full month
        if month_end > today:
            month_end = today
            full_month = False

        # specify url for worldweatheronline.com API call
        url_data = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?q=NG1&format=json&date=' + str(
            start_date) + '&enddate=' + str(month_end) + '&tp=24&key=ec3b4eb6ae0fd0c07912a156c046d'

        # api call
        web_url = urllib.request.urlopen(url_data)

        # handle result
        response = web_url.read()
        data = response.decode('utf-8')

        # save the result as a json file
        file_name = dir_path + str(start_date.year) + "-" + str(start_date.month).zfill(2) + ".json"
        with open(file_name, 'w') as outfile:
            outfile.write(data)

        # change the start date
        start_date = month_end + timedelta(days=1)

        # break if last month is not full month
        if not full_month:
            break

        time.sleep(10)


if __name__ == '__main__':
    main()
