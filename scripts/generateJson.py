#!/usr/bin/env python3

import pandas as pd
from typing import List
import os
import argparse
import re
import json
import warnings


def get_all_files(base_dir: str, pattern: str) -> dict:
    """

    Args:
        base_dir ():
        pattern ():

    Returns:

    """
    files_dict = {}
    reg_compile = re.compile(pattern)
    for dir_path, dir_names, filenames in os.walk(base_dir):
        for filename in sorted(filenames):
            res = reg_compile.match(filename)
            if res:
                files_dict[res.group(1)] = os.path.join(dir_path, filename)

    return files_dict


def get_all_cases(base_dir: str) -> dict:
    """
    Get the list of all case files 'casesYYYYMMDD.cvs'
    Args:
        base_dir (str): the folder where to look for the files.

    Returns:
        A dictionary where the key is the date in YYYYMMDD format and the value the filename
    """
    return get_all_files(base_dir, r"cases(\d{8}).csv")


def get_all_hospitals(base_dir: str) -> dict:
    """
    Get the list of all hospital files 'hospitalsYYYYMMDD.cvs'
    Args:
        base_dir (str): the folder where to look for the files.

    Returns:
        A dictionary where the key is the date in YYYYMMDD format and the value the filename
    """
    return get_all_files(base_dir, r"hospitals(\d{8}).csv")


def read_all_cases(files_dict: dict) -> dict:
    """
    Given the list of case files, read all the file and populate a dictionary with the relevant data
    Args:
        files_dict (dict): the key is the data, the value the filename (see :py:func: `get_all_cases()`)

    Returns:
        A dictionary containing all the data.
        Each key is a city (str)
        The value of each key is a dictionary containing 2 keys, 'totale_positivi' and 'isolamento'
        For each of these 2 keys, the value is a dictionary with date as a key and the relevant number as value.
    """
    cases_dict = {}
    for date, filename in files_dict.items():
        print(date)
        # load csv
        df = pd.read_csv(filename)
        df.fillna(value=0, inplace=True)
        # for each row
        for index, row in df.iterrows():
            # the residence is the key
            city = row['residenza']
            if not isinstance(city, str):
                raise TypeError('city must be a string in ' + filename)
            # at the beginning Lombardia was counted then i guess it was merged in a more general category
            if city == 'Lombardia':
                city = 'Domicilio fuori Veneto'
            # I'm assuming that Padova always was without the Vo' cluster
            if city == "Padova (escluso domiciliati Vo')":
                city = 'Padova'
            # initialize
            if city not in cases_dict:
                cases_dict[city] = {'totale positivi': {}, 'isolamento': {}}
            cases_dict[city]['totale positivi'][date] = row['totale positivi']
            # isolamento was not given from the beginning
            if 'isolamento' in df.columns:
                cases_dict[city]['isolamento'][date] = int(row['isolamento'])

    return cases_dict


def read_all_hospitals(files_dict: dict) -> dict:
    hospital_dict = {}
    for date, filename in files_dict.items():
        print(date)
        # load csv
        df = pd.read_csv(filename)
        df.fillna(value=0, inplace=True)
        # for each row
        for index, row in df.iterrows():
            if not isinstance(row['struttura'], str):
                raise TypeError('city must be a string in ' + filename)

            # some of the entries have a \n
            hospital = row['struttura'].replace('\n', ' ')
            # some fixes because some entries have footnote symbols, remove them
            hospital = hospital.replace(' °', '')
            hospital = hospital.replace('^', '')
            hospital = hospital.replace('  ', ' ')
            # Uniform the data with "Ospedale <city>" instead of "Ospedale di <city>"
            hospital = hospital.replace('Ospedale di ', 'Ospedale ')
            # some specific inconsistencies
            if hospital == 'Ospedale Sacro Cuore Don Calabria':
                hospital = 'Ospedale Sacro Cuore Don Calabria-Negrar'
            if hospital == 'Ospedale Villa Salus':
                hospital = 'Ospedale Villa Salus-Mestre'
            if hospital == 'ULSS 6- Osedale Camposampiero':
                hospital = 'ULSS 6 - Ospedale Camposampiero'

            # initialize
            if hospital not in hospital_dict:
                hospital_dict[hospital] = {'non critici': {}, 'terapia intensiva': {}, 'dimessi': {}, 'decessi': {}}
            hospital_dict[hospital]['non critici'][date] = int(row['non critici'])
            hospital_dict[hospital]['terapia intensiva'][date] = int(row['terapia intensiva'])
            hospital_dict[hospital]['dimessi'][date] = int(row['dimessi'])
            hospital_dict[hospital]['decessi'][date] = int(row['decessi'])

    return hospital_dict


def generate_summary(cases_dict: dict) -> dict:
    """
    Given a dictionary containing the case data it returns a dictionary with the overall summary for each category
    Args:
        cases_dict (dict): the data

    Returns:
        A dictionary that contains the same categories as keys as the input and as values a dictionary date-value with
        the overall sum of all the input values
    """
    summary = {}

    for city, categories in cases_dict.items():
        for category, data in categories.items():
            for date, value in data.items():
                # initialize the first one
                if category not in summary:
                    summary[category] = {}
                summary[category][date] = value + summary[category].get(date, 0)

    return summary


def save_category_to_csv(case_dict: dict, category: str, dates: List[str], filename: str):

    d = {'date': dates}
    for city, categories in case_dict.items():
        # this is to assure that there is a number for each date, if it is not provided it is assumed 0
        d[city] = []
        for day in dates:
            d[city].append(case_dict[city][category].get(day, 0))

    pd.DataFrame(d).to_csv(filename.replace(' ', '_'), index=False)


def save_to_json(case_dict: dict, filename: str):

    with open(filename, 'w') as fp:
        json.dump(case_dict, fp, sort_keys=True, indent=4)


def cases_sanity_check(case_dict: dict):
    # check we have all the cities
    assert len(case_dict.keys()) == 11

    num_elem = -1

    # check consistency
    for city, data in case_dict.items():
        # number of element for total positives must be the same (i.e. same number of days)
        if num_elem == -1:
            num_elem = len(data['totale positivi'].keys())
        else:
            assert len(data['totale positivi'].keys()) == num_elem

        # totale positivi, is it a cumulative data?
        days = list(data['totale positivi'].keys())
        positive = data['totale positivi']
        for idx, day in enumerate(days):
            if idx > 0:
                if positive[days[idx]] < positive[days[idx - 1]]:
                    warnings.warn('decreasing in total positives for ' + city + ' on ' + days[idx] + ' (' + str(
                        positive[days[idx]]) + ') and ' + days[idx - 1] + ' (' + str(positive[days[idx - 1]]) + ')',
                                  Warning)


def hospitals_sanity_check(case_dict: dict):
    # check we have all the hospitals
    assert len(case_dict.keys()) == 44


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate json database file from raw data')
    # general parameters
    parser.add_argument('--baseDir', required=True, help='the folder containing the csv')
    parser.add_argument('--jsonDir', required=True, help='the output folder where to save the json files')
    parser.add_argument('--csvDir', required=True, help='the output folder where to save the csv files')

    args = parser.parse_args()

    # get all the files
    files_cases = get_all_cases(args.baseDir)
    # read and generate dict database
    cases = read_all_cases(files_cases)
    # add veneto summary
    veneto = generate_summary(cases)
    cases['Veneto'] = veneto

    # print(cases.keys())
    cases_sanity_check(cases)
    # print(cases)

    # save the csv files
    for city_name, category_names in cases.items():
        for category_name in list(category_names.keys()):
            save_category_to_csv(cases, dates=list(files_cases.keys()), category=category_name, filename=os.path.join(args.csvDir, 'cases_' + category_name + '.csv'))

    # save json file
    save_to_json({'places': cases, 'dates': list(files_cases.keys())}, filename=os.path.join(args.jsonDir, 'cases.json'))

    # Hospitals
    files_hospitals = get_all_hospitals(args.baseDir)

    hospitals = read_all_hospitals(files_hospitals)
    # add veneto summary
    veneto = generate_summary(hospitals)
    hospitals['Veneto'] = veneto

    print('\n'.join('{}'.format(l) for l in sorted(list(hospitals.keys()))))
    print(len(list(hospitals.keys())))
    print(hospitals)

    hospitals_sanity_check(hospitals)

    # save json file
    save_to_json({'hospitals': hospitals, 'dates': list(files_hospitals.keys())}, filename=os.path.join(args.jsonDir, 'hospitals.json'))

    # save the csv files
    for hospital_name, category_names in hospitals.items():
        for category_name in list(category_names.keys()):
            save_category_to_csv(hospitals, dates=list(files_hospitals.keys()), category=category_name, filename=os.path.join(args.csvDir, 'hospitals_' + category_name + '.csv'))


