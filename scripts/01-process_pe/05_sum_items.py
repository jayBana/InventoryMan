#!/usr/bin/python3

'''
script that sums the daily product usage for items from a list
'''

import os
import os.path
import csv
import json
import pandas as pd
from pandas import ExcelWriter, merge


def main():
    # first argument the path for file to be processed
    dir_path = '..' + os.sep + '..' + os.sep + 'data' + os.sep + 'peData' + os.sep
    file_path = dir_path + 'daily_ingredient_usage.xlsx'

    # read sheet
    table = pd.read_excel(file_path, 'Sheet', index_col=None, na_values=['NA'])

    # read the product list for items that we are interested in
    list_to_sum = csv.reader(open(dir_path + 'list_sum_up.csv', 'rU'))

    # read the list of all products
    with open(dir_path + 'list_products.json', encoding='utf-8') as data_file:
        products = json.load(data_file)

    # create dictionary where we save the product codes for each product
    # some products maybe part of a set menu
    dict_to_sum = {}

    # each line in csv reader object
    for line in list_to_sum:
        # create empty set
        ids = set()
        # check against each name variation
        for l in line:
            # find the product keys for names
            for k in products.keys():
                if l.strip() in products[k]['Description']:
                    ids.add(int(k))

        # save set of product keys for each item
        dict_to_sum[line[0]] = ids

    # create a final table
    final_table = pd.DataFrame(table['Date']).groupby(['Date'], as_index=False).sum()

    # sum up products for each day
    for k, v in dict_to_sum.items():
        # sum up product if in set of product keys per item
        result = table.loc[table['Stock Code'].isin(v)].groupby(['Date'], as_index=False).sum()[['Date', 'Unit Sales']]
        # create the name for saving the file
        prod_name = 'prod_' + k.lower().replace(' ', '_')
        # rename the summed column
        result.rename(columns={result.columns[1]: prod_name}, inplace=True)
        # merge results together
        final_table = merge(final_table, result, how='outer', on='Date')

    # get the list of ingredients
    ingredients = []
    for l in list(table.columns.values):
        if 'ing_' in l:
            ingredients.append(l)

    # for each ingredient
    for i in ingredients:
        # sum daily ingredient usage
        result = table[['Date', i]].groupby(['Date'], as_index=False).sum()
        # merge results together
        final_table = merge(final_table, result, how='outer', on='Date')

    # fill NaN values
    final_table = final_table.fillna(0)

    # define where to save the file
    file_path = dir_path + 'daily_summed_usage' + os.sep + 'merged_table.csv'
    # save it as a csv file
    with open(file_path, mode='w') as fp:
        final_table.to_csv(fp, index=False)


if __name__ == '__main__':
    main()
