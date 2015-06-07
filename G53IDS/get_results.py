'''
responsible for making calling the ml_studio_request script and process the results
'''
from datetime import datetime, timedelta
from math import ceil
from ml_studio_request import main as mls_request

# data to be stored
global predictions
global today

# call ml_studio_request
def get_predictions_all():
    global predictions
    global today
    predictions, today = mls_request()

# process the results and
def get_predictions_subset(start_date=None, end_date=None):

    # set flag for default or specific range return
    is_login = True if start_date is None and end_date is None else False

    # upon login get it only for seven days
    if is_login:
        start_date = today
        end_date = (datetime.strptime(start_date, "%Y-%m-%d").date() + timedelta(days=6)).strftime("%Y-%m-%d")

    # cut off date for period (first instance of the day after of the actual end date)
    cut_off_date = (datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(days=1)).strftime("%Y-%m-%d")

    # get the index of the first day to predict from in the list of tuples
    start_index = 0 if end_date is None else predictions.index(next(x for x in predictions if x[0] == start_date))

    # extract and store predictions for a specific date
    results_list = []
    summed = {}
    # from beginning to the end of the list
    for i in range(start_index, len(predictions)):
        # stop if we reached the cut_off_date (first instance of day after end date)
        if predictions[i][0] == cut_off_date:
            break
        # add to  list
        results_list.append(predictions[i])
        # sum the item quantities
        if predictions[i][1] not in summed:
            summed[predictions[i][1]] = 0
        summed[predictions[i][1]] = int(ceil(float(predictions[i][2])))

    # return values accordingly
    if is_login:
        return results_list, summed, start_date, end_date
    else:
        return results_list, summed