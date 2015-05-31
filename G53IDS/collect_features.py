__author__ = 'janosbana'

import json
import os
import requests
from datetime import datetime, timedelta, date
from xml.etree import ElementTree as ET

# get events data for next 7 days from eventful api
def get_eventful_data(venue_names_path, today):

    # save our api key
    app_key = '2J7PsVHMXzdwZHfZ'

    # format dates to required scheme for api call
    from_date = today.strftime("%Y%m%d") + "00"
    to_date = (today + timedelta(days=7)).strftime("%Y%m%d") + "00"

    # open file that contains venue ids
    with open(venue_names_path, encoding='utf-8') as data_file:
        venues = json.load(data_file)['venues']

    # create empty list for dates
    event_dates = []

    # for each venue in our list
    for venue in venues:
        # get name and location id
        venue_name, location = venue.split(':')

        # prepare url and make api call
        url = 'http://api.eventful.com/rest/events/search?app_key=' + app_key + '&date=' + from_date + '-' + to_date + '&location=' + location
        response = requests.request('GET', url)

        # parse XML response
        root = ET.fromstring(response.content)
        events = root.find('events')

        # set of dates for this venue
        dates = set()

        # if there are no events for this venue, then just add a None object to out list and continue to next iteration
        if not events:
            event_dates.append((venue_name, None))
            continue

        # for each event
        for event in events:
            # get start end end dates
            start_date = event.find("start_time").text
            end_date = event.find("stop_time").text

            # if there is no end date then we know that this event is on one day only
            if end_date is None:
                dates.add(start_date.split(" ")[0])
                continue

            # create date objects
            s_date = datetime.strptime(start_date.split(" ")[0], "%Y-%m-%d").date()
            e_date = datetime.strptime(end_date.split(" ")[0], "%Y-%m-%d").date()

            # get number of days between two dates
            delta = e_date - s_date

            # for each day from start to end date
            for d in range(delta.days + 1):
                # convert date to ISO 8601 format
                add_date = (s_date + timedelta(days=d)).strftime("%Y-%m-%d")

                # add date to set if not already in set
                if add_date not in dates:
                    dates.add(add_date)

        # append set to list of dates with the venue's name
        event_dates.append((venue_name, dates))

    return event_dates

# get weather data for the next 7 days from worldweatheronline.com api
def get_weather_data():
    # define parameters for api call
    location = 'NG1'
    date = 'today'
    days = '7'
    time_interval = '24'
    format = 'json'
    api_key = 'ec3b4eb6ae0fd0c07912a156c046d'
    url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx?' + 'q=' + location + '&date=' + date + \
          '&num_of_days=' + days + '&tp=' + time_interval + '&format=' + format + '&key=' + api_key

    # make the call and format as json
    response = requests.request('GET', url).json()

    # create dictionary for extracting only info that we need
    weather_data = {}

    # each day in response
    for entry in response['data']['weather']:
        # get the information that we are interested at
        date_string = entry['date']
        cloud_cover = entry['hourly'][0]['cloudcover']
        temp = entry['hourly'][0]['FeelsLikeC']
        precip = entry['hourly'][0]['precipMM']
        wind_speed = entry['hourly'][0]['windspeedKmph']

        # add the info as a list to dict with key of the day's date
        weather_data[date_string] = [float(cloud_cover), float(temp), float(precip), float(wind_speed)]

    return weather_data


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
    venue_names_path = data_dir_path + 'eventful_venues.json'
    events_data = get_eventful_data(venue_names_path, today)

    # load daily sales json
    with open(daily_sales_path, encoding='utf-8') as data_file:
        daily_sales = json.load(data_file)

    # load important dates into sets
    bank_holidays = load_bank_holidays(bank_holiday_path)
    city_school_days = load_school_days(city_days_path)
    county_school_days = load_school_days(county_days_path)
    uni_key_dates = load_uni_key_dates(uni_key_dates_path)

    today = date.today()

    # get data from apis
    weather_data = get_weather_data()
    events_data = get_eventful_data(venue_names_path, today)


if __name__ == '__main__':
    main()
