import os
import requests
import json
import pandas as pd
import re
import numpy as np

def get_indicators(IndicatorName = 'all'):
    """
    Retrieves by default a dataframe of indicators codes and description available on the GHO database,
    and provides a simple functionality to filter for indicator names of interest.
    The search function is case-insensitive.
    Returns a dash symbol when no records are found.
    """
    if IndicatorName == 'all':
        url = "https://ghoapi.azureedge.net/api/Indicator"
    elif IndicatorName != 'all':
        url = "https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName," + "'{}'".format(IndicatorName) + ")"
    r = requests.get(url)
    indicators = r.json()
    return pd.DataFrame(indicators['value'])

def query_parser(IndicatorCode='WHOSIS_000001', SpatialDimType='', SpatialDim='', TimeDimType='', TimeDim='',
                 Dim1Type='', Dim1='', Dim2Type='', Dim2='', Dim3Type='', Dim3=''):
    """
    With user-defined geographical, temporal and demographical filters, a request query is parsed for the desired indicator.
    """
    d = locals()
    given_filters = {key: value for key, value in d.items() if value}
    if len(given_filters) >= 1:
        parsed_request_url = "https://ghoapi.azureedge.net/api/" + IndicatorCode
        if len(given_filters) > 1:
            del (given_filters["IndicatorCode"])
            filters = '?$filter='
            for key, value in given_filters.items():
                if key == "TimeDim":
                    filters += key + " eq " + str(value) + ' and '
                else:
                    filters += key + " eq " + "'{}'".format(value) + ' and '
            parsed_request_url += filters.rstrip(' and ')

    return parsed_request_url

def get_records(indicator_code="AIR_11", spatial_dimension='', country='', temporal_dimension='', year='',
                filter_1='', filter_1_value='',
                filter_2='', filter_2_value='',
                filter_3='', filter_3_value='',
                summary=True, to_csv=True,
                csv_name=""):
    """
    Return a dataframe of records for an indicator of choice, optionally with geographical, temporal and demographical
    filters implemented.
    Allows for the option to generate a summary of recorded dimensions for the indicator.
    The pulled dataframe can also be saved to csv.
    """
    # Calling the query_parser function to format a query url using submitted arguments
    try:
        url = query_parser(IndicatorCode=indicator_code, SpatialDimType=spatial_dimension, SpatialDim=country,
                           TimeDimType=temporal_dimension, TimeDim=year,
                           Dim1Type=filter_1, Dim1=filter_1_value,
                           Dim2Type=filter_2, Dim2=filter_2_value,
                           Dim3Type=filter_3, Dim3=filter_3_value)
        records = requests.get(url)
        r_df = pd.DataFrame(records.json()['value'])
    except ValueError:
        print("Invalid search criteria provided, please check arguments and try again.")
        return

    # generate a dictionary summarizing the recorded dimensions for this indicator for user consideration
    if summary == True and r_df.shape != (0, 0):
        desired_columns = ['IndicatorCode', 'SpatialDimType', 'SpatialDim', 'TimeDimType', 'TimeDim', 'Dim1Type',
                           'Dim1', 'Dim2Type', 'Dim2', 'Dim3Type', 'Dim3']
        objects = r_df[desired_columns]
        summary_dict = {}
        for (colname, data) in objects.iteritems():
            summary_dict[colname] = data.unique()
    elif summary == True and r_df.shape == (0, 0):
        summary_dict = {}
        raise Exception("0 entries matching search criteria, please adjust and try again.")
        return

    # generate output file
    if to_csv == True and r_df.shape != (0, 0):
        r_df.to_csv(csv_name)

    return r_df, summary_dict


def search_dimensions(search_for='all'):
    """
    Retrieves a dataframe of all dimensions recorded in the GHO database.
    A local keyword search can be optionally implemented, to locate dimensions of interest.
    """
    r = requests.get('https://ghoapi.azureedge.net/api/Dimension')
    dimensions = pd.DataFrame(r.json()['value'])

    if search_for == 'all':
        return dimensions
    elif search_for != 'all':
        dimensions = dimensions[dimensions.Code.str.contains(search_for.upper())]
        if dimensions.shape == (0, 2):
            raise Exception('No matching dimensions found, please adjust your search.')

    return dimensions


def get_dimension_values(dimension_code='YEAR', search_for=''):
    """
    Allows user to inspect, and run a case-insensitive search through values of a specific dimension.
    """
    url = "https://ghoapi.azureedge.net/api/DIMENSION/" + dimension_code.upper() + "/DimensionValues"
    dimension_values = requests.get(url)
    dimension_values_df = pd.DataFrame(dimension_values.json()['value'])

    if search_for == '':
        pass
    elif search_for != '':
        result = dimension_values_df.apply(
            lambda row: row.astype(str).str.contains(search_for, na=False, flags=re.IGNORECASE).any(), axis=1)
        dimension_values_df = dimension_values_df.loc[result]

    if dimension_values_df.shape == (0, 6):
        raise Exception('No matching dimension values found, please adjust your search.')

    return dimension_values_df
