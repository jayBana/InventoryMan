__author__ = 'janosbana'

'''
this script makes an api call to ml studio web service we created and returns the predicted values
for each order item for the next seven days

Note: the code was taken from Azure's ML Studio web service information page and modified to fit our needs
'''

import json
import requests
from datetime import date, timedelta
from operator import itemgetter
from server.ml_helpers.collect_features import main as collect_features

def main():
    # get the features for 14 days from tomorrow
    start_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    days = 14
    # get the features to be passed in with api call
    values, event_info, weather_info = collect_features(start_date, days)

    # prepare API call body
    data = {

        "Inputs": {

            "input1":
                {
                    "ColumnNames": ["Date", "Daily Sales", "Day", "Week Number", "Year Day", "Weekend", "Bank Holiday",
                                    "City School Holidays", "County School Holidays", "UoN Welcome Week", "UoN Term",
                                    "UoN Graduation", "UoN Exam", "Trent Welcome Week", "Trent Term",
                                    "Trent Graduation", "Trent Exam", "Cloud Cover (%)", "Temp (celsius)",
                                    "Precip (mm)", "Wind speed (kmh)", "Capital Fm Arena", "National Ice Centre",
                                    "Playhouse", "Rock City", "Theatre Royal Concert Hall", "Target"],
                    "Values": values,
                }
        },
        "GlobalParameters": {}
    }

    # prepare parameters for API call
    body = str.encode(json.dumps(data))
    url = 'https://ussouthcentral.services.azureml.net/workspaces/2cef58aae0904039bd3bc470718fb9d9/services/98d96dd51860427ebec407b6871ec3c5/execute?api-version=2.0&details=true'
    api_key = 'IOgTLGR96fE2bHHw9+k7M6iRpsJTwROAFVTdrEEIHOZjAiLmCGZgoh073Z7ly9w5F7lnitFke++gJL8PbZzt9Q=='
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    # make the call
    try:
        response = requests.request('POST', url, data=body, headers=headers).json()

        # process the response
        results = []
        for item in response['Results']['output1']['value']['Values']:
            # create a list of tuples (date, item_name, predicted_quantity)
            entry = {'date': item[1], 'name': item[0], 'quantity': round(float(item[2]), 2)}
            results.append(entry)
        # sort list of dict
        results = sorted(results, key=itemgetter('date'))
        event_info = sorted(event_info, key=itemgetter('start'))
        weather_info = sorted(weather_info, key=itemgetter('date'))
        return results, event_info, weather_info

    # handle errors
    except requests.HTTPError as error:
        print(("The request failed with status code: " + str(error.code)))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure

if __name__ == '__main__':
    main()
