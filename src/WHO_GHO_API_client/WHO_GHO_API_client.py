import os
import requests
import json
import pandas as pd
import re
import numpy as np


def get_indicators(IndicatorName='all'):
    """
    Retrieves by default a dataframe of indicators codes and description available on the GHO database,
    and provides a simple functionality to filter for indicator names of interest.
    The search function is case-insensitive.
    Returns a dash symbol when no records are found.

    Parameters
    ----------
    IndicatorName : str
        A search word which we want to retrieve relevant indicators for.

    Returns
    -------
    pandas.core.frame.DataFrame
        A dataframe containing the requested indicators recorded in the GHO database.
        Consists of indicator codes and descriptions.

    Examples
    --------
    >>> get_indicators(IndicatorName = 'female')
    returns a dataframe of all indicators containing "female" in the description.
    """
    if IndicatorName == 'all':
        url = "https://ghoapi.azureedge.net/api/Indicator"
    elif IndicatorName != 'all':
        url = "https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName," + "'{}'".format(
            IndicatorName) + ")"
    r = requests.get(url)
    indicators = r.json()
    return pd.DataFrame(indicators['value'])


def query_parser(IndicatorCode='WHOSIS_000001',
                 SpatialDimType='', SpatialDim='',
                 TimeDimType='', TimeDim='',
                 Dim1Type='', Dim1='',
                 Dim2Type='', Dim2='',
                 Dim3Type='', Dim3=''):
    """
    Accessory function of get_records().
    With user-defined geographical, temporal and demographical filters, a request query is parsed for the desired indicator.
    All arguments are taken from those submitted to get_records().

    Parameters
    ----------
    IndicatorCode : str
        The GHO database unique identifier for which we want to query.

    SpatialDimType : str
        If the chosen indicator has records for more than one type of spatial dimension (eg. records for a single
        country and continent), this argument can be used to filter records for the desired one.

    SpatialDim : str
        If the chosen spatial dimension has more than one unique values,
        this argument can be used to filter records for the desired one.

    TimeDimType : str
        If the chosen indicator has records for more than one type of temporal dimension (eg. month of the year vs.
        entire year), this argument can be used to filter records for the desired one.

    TimeDim : str
        If the chosen temporal dimension has more than one unique values,
        this argument can be used to filter records for the desired one.

    Dim1/Dim2/Dim3Type : str
        Additional demographical dimensions to filter indicator records by. Refer to full indicator dataframe or summary for
        filtering options.

    Dim1/Dim2/Dim3 : str
        Dimension values to filter indicator records by. Refer to full indicator dataframe or summary for
        filtering options.

    Returns
    -------
    str
        A parsed url used to query the database and obtain the data entries of interest from the GHO database.

    Examples
    --------
    >>> query_parser(IndicatorCode = 'WHOSIS_000001', SpatialDimType = 'Region', TimeDimType = 'year', Dim1 = 'WQ1')
        "https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDimType eq 'Region' and TimeDimType eq 'year' and Dim1 eq 'WQ1'"
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
                csv_name="output.csv"):
    """
    Returns a dataframe of records for an indicator of choice, optionally with geographical, temporal and demographical
    filters implemented.
    Allows for the option to generate a summary of recorded dimensions for the indicator.
    The pulled dataframe can also be saved to csv.

    Parameters
    ----------
    indicator_code : str
        The GHO database unique identifier of the indicator we want to obtain records for.
        Run get_indicators() function and refer to the IndicatorCode column.

    spatial_dimension : str
        (Optional) If the chosen indicator has records for more than one type of spatial dimension (eg. records for a single
        country and continent), this argument can be used to filter records for the desired one.

    country : str
        (Optional) If the chosen indicators has records on a country level, this argument can be used to filter records for a country
        of interest.

    temporal_dimension : str
        (Optional) If the chosen indicator has records for more than one type of temporal dimension (eg. month of the year vs.
        entire year), this argument can be used to filter records for the desired one.

    year : str
        (Optional) If the chosen indicators has records on a yearly basis, this argument can be used to filter for a year
        of interest.

    filter_1/filter_2/filter_3 : str
        (Optional) Additional demographical dimensions to filter indicator records by.
        Refer to full indicator dataframe or summary for filtering options.

    filter_1/filter_2/filter_3 value : str
        (Optional) Dimension values to filter indicator records by.
        Refer to full indicator dataframe or summary for filtering options.

    summary : bool
        If true, generates summary dictionary of the recorded dimensions for the indicator of choice.

    to_csv : bool
        If true, saves the resultant indicator entries dataframe to a local csv file.

    csv_name : str
        Name for output csv file.

    Returns
    -------
    pandas.core.frame.DataFrame
        Containing the requested indicator entries.

    dict
        Summarizing the values in each column of the output dataframe.
        Provides a overview of what dimensions are measured for a certain indicator, to use as guidance for further filtering.

    csv
        Output dataframe saved locally.

    Examples
    --------
    >>> get_records(indicator_code = 'AIR_11', to_csv = True,
                    csv_name = 'Household air pollution attributable deaths.csv', country = "USA")
            Returns a dataframe and csv file with entries for the AIR_11 indicator, filtered for records about the USA only.
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
        desired_columns = ['IndicatorCode', 'SpatialDimType', 'SpatialDim', 'TimeDimType',
                           'TimeDim', 'Dim1Type', 'Dim1', 'Dim2Type', 'Dim2', 'Dim3Type', 'Dim3']
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
    A local, case-insensitive keyword search can be optionally implemented, to locate dimensions of interest.

    Parameters
    ----------
    search_for : str
        A searchword specifying dimensions of interest. Used to filter for dimension codes containing the searchword.

    Returns
    -------
    pandas.core.frame.DataFrame
        Containing all dimension codes and descriptions recorded in the database, or alternatively fitting the search criteria.

    Examples
    --------
    >>> search_dimensions()
        Retrives all dimensions recorded in the database.

    >>> search_dimensions(search_for = "type")
        Retrives dimensions in the database that contains the word "type" in its code.
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
    Allows user to inspect, and run a case-insensitive search through the values of a specific dimension.

    Parameters
    ----------

    dimension_code : str
        The GHO database unique identifier for each dimension.

    search_for : str
        A searchword specifying dimension values of interest.
        This search applies to all elements in the dimension values dataframe.

    Returns
    -------
    pandas.core.frame.DataFrame
        Containing all exisiting values and descriptions for a particular dimension,
        or alternatively values that fit the search criteria.

    Examples
    --------
    >>> get_dimension_values(dimension_code = "country")
        Retrives all countries with records in the GHO database.

    >>> get_dimension_values(dimension_code = "country", search_for = "africa")
        Retrives all African countries with records in the GHO database.

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