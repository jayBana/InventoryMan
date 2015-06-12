#!/usr/bin/python3

'''
script that scrapes event date for Capital FM Arena, National Ice Centre,
Playhouse and Royal Concert Hall in Nottingham from UKTDB's website
'''

import os.path
import requests
from openpyxl import Workbook
from time import strptime, strftime, mktime
from datetime import timedelta, datetime
from bs4 import BeautifulSoup

def main():
    # path for files to be saved
    dir_path = '..' + os.sep + '..' + os.sep + 'data' + os.sep + 'events' + os.sep

    # UKTDB link for specific venue
    links = ['http://www.uktw.co.uk/archive/nottinghamshire/nottingham/capital-fm-arena-nottingham/V0543542209/',
             'http://www.uktw.co.uk/archive/nottinghamshire/nottingham/national-ice-centre/V0843992113/',
             'http://www.uktw.co.uk/archive/nottinghamshire/nottingham/playhouse/V457/',
             'http://www.uktw.co.uk/archive/nottinghamshire/nottingham/theatre-royal-concert-hall/V462/'
             ]

    # process each url
    for url in links:
        # get content of html
        r = requests.get(url)
        soup = BeautifulSoup(r.text)

        # create a new workbook and sheet
        wb = Workbook()
        ws = wb.get_active_sheet()

        # create headers
        header = ('Date', 'Name', 'Event Type', 'Link')
        ws.append(header)

        # get the name of the venue and set output filename
        title = soup.find('h1').string
        output_file_name = title.strip().replace('archive listings', '')
        if 'Nottingham' in output_file_name: output_file_name = title.replace('Nottingham', '')
        output_file_name = 'events_' + output_file_name.split(' (')[0].strip().lower().replace(' ', '-') + '.xlsx'

        # get table element of html
        table = soup.find('table')

        # for each row in table
        for tr in table:

            # row contains only a cell string, but not the year
            if len(tr.contents) == 1 and not tr.contents[0].b.string[-4:].isdigit():
                break
            # row is en event entry
            elif len(tr.contents) == 2:

                # date is in first cell
                event_date = tr.contents[0].text
                # event name is in the second cell
                name = tr.contents[1].b.text
                # get event type from string
                event_type = tr.contents[1].i.contents[0].split('::')[0].strip()
                # get link for event info
                link = tr.contents[1].a.get('href')

                # event is on multiple days
                if 'to' in event_date:
                    # break down string
                    days = event_date.split('to')
                    start_date = datetime.fromtimestamp(mktime(strptime(days[0].strip(), '%d %b %y')))
                    end_date = datetime.fromtimestamp(mktime(strptime(days[1].strip(), '%d %b %y')))

                    # create a new entry in excel sheet for each day with the same event info
                    delta = end_date - start_date
                    for d in range(delta.days + 1):
                        new_date = end_date - timedelta(days=d)
                        event_date = new_date.strftime("%Y-%m-%d")
                        new_row = (event_date, name, event_type, link)
                        ws.append(new_row)
                # event is only on a single day
                else:
                    d = strptime(event_date, '%d %b %y')
                    event_date = strftime('%Y-%m-%d', d)
                    new_row = (event_date, name, event_type, link)
                    ws.append(new_row)

        # save workbook
        wb.save(dir_path + output_file_name)


if __name__ == '__main__':
    main()
