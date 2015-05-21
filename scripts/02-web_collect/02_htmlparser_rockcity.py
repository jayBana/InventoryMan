#!/usr/bin/python3

'''
script that scrapes event info for Rock City Nottingham from its website
'''

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from openpyxl import Workbook
import sys
import os.path


def process(year, ws):
    # set up url and pull content of website
    url = 'http://www.rock-city.co.uk'
    archive_url = url + '/gig-guide/archive/' + str(year)
    r = requests.get(archive_url)

    # create handle object for html
    soup = BeautifulSoup(r.text)

    # set tag that we want to work with
    tag = soup.find('div', 'gig_archive')

    # process each month in current year
    for child in tag:
        # get month name
        if type(child) is Tag and child.name == 'div' and 'class' in child.attrs and 'month' in child['class']:
            month = child.h2.contents[0].strip()

            # for each element in list
            for li in child.ul:
                if type(li) is Tag:
                    # get date
                    day = li.contents[0].strip().split(' ')[1][:-2] + ' ' + month
                    # create ISO 8601 date string
                    d = time.strptime(day, '%d %B %Y')
                    date = time.strftime('%Y-%m-%d', d)

                    # get link for event
                    anchor_tag = li.ul.li.a

                    # create row and add it to sheet
                    new_row = (date, anchor_tag.contents[0].strip(), 'Concert', url + anchor_tag.get('href'))
                    ws.append(new_row)


def main():
    # path for files to be saved
    dir_path = '..' + os.sep + '..' + os.sep + 'data' + os.sep + 'events' + os.sep

    # command line arguments: start year
    start = int(sys.argv[1])
    # command line arguments: end year
    end = int(sys.argv[2])

    # create a new workbook and sheet
    wb = Workbook()
    ws = wb.get_active_sheet()

    # create headers
    header = ('Date', 'Name', 'Event Type', 'Link')
    ws.append(header)

    # process for each year
    for year in range(start, end + 1):
        process(year, ws)

    # save workbook
    wb.save(dir_path + 'events_rock-city.xlsx')


if __name__ == '__main__':
    main()
