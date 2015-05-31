__author__ = 'janosbana'

'''
this script makes an api call to ml studio web service we created and returns the predicted values
for each order item for the next seven days

Note: the code was taken from Azure's ML Studio web service information page and modified to fit our needs
'''

import json
import requests
from collect_features import main as collect_features


def main():
    # get the features to be passed in with api call
    values = collect_features()

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
    url = 'https://ussouthcentral.services.azureml.net/workspaces/2cef58aae0904039bd3bc470718fb9d9/services/7a76e2bb985a4d5ba3eadee43c76b8eb/execute?api-version=2.0&details=true'
    api_key = 'UGlKgykV4BSYFf3YH1+WK0W4Jtj2iZQWTWf2x2mAmJsZWwjSsOKn8vOG+rVGrTEojhD0PH5f2MXiL+6duRSMuw=='
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    # make the call
    try:
        response = requests.request('POST', url, data=body, headers=headers).json()

        # process the response
        results = {}
        for item in response['Results']['output1']['value']['Values']:
            if item[1] not in results:
                results[item[1]] = {}

            # save each item in dictionary with date as key, each value is product/ingredient key: consumption value
            results[item[1]][item[0]] = item[2]

        return results

    # handle errors
    except requests.HTTPError as error:
        print(("The request failed with status code: " + str(error.code)))
        # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
        print((error.info()))

if __name__ == '__main__':
    main()
