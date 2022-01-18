import pytest
import pandas as pd
from WHO_GHO_API_client.WHO_GHO_API_client import get_records


correct_output = pd.read_csv("Household air pollution attributable deaths.csv",
                             dtype = {'Dim3Type': object, 'Dim3': object,'DataSourceDimType': object,
                                      'DataSourceDim': object, 'Comments': object, 'TimeDimensionValue': object},
                             index_col = 0)

test_cases = [
    ('AIR_11', True, 'Household air pollution attributable deaths.csv', '', 'USA', correct_output),
    ('AIR_11', True, 'Household air pollution attributable deaths.csv', 2013, '', correct_output),
    ('jibberish', True, 'Household air pollution attributable deaths.csv', 2013, 'CHL', correct_output)
]

@pytest.mark.parametrize('indicator_code, to_csv, csv_name, year, country, result', test_cases)
class TestGetRecords:
    def test_basic_function(self, indicator_code, to_csv, csv_name, year, country, result):
        """Testing if correct records are retrieved."""
        if indicator_code == "AIR_11" and country == 'USA':
            actual = get_records(indicator_code=indicator_code, to_csv=to_csv,
                                 csv_name=csv_name, year=year, country=country)
            expected = result
            assert actual[0].equals(expected), "get_records has failed to retrieve the correct dataframe."

    def test_no_matching_entries(self, indicator_code, to_csv, csv_name, year, country, result):
        """Testing if an exception is raised when making a query which does not return any records."""
        if indicator_code == "AIR_11" and year == 2013:
            with pytest.raises(Exception) as exception_info:
                get_records(indicator_code=indicator_code, to_csv=to_csv,
                            csv_name=csv_name, year=year, country=country)

    def test_invalid_argument(self, indicator_code, to_csv, csv_name, year, country, result):
        """Testing if invalid arguments to the function raises a ValueError."""
        if indicator_code == "jibberish":
            with pytest.raises(ValueError) as exception_info:
                get_records(indicator_code=indicator_code, to_csv=to_csv,
                            csv_name=csv_name, year=year, country=country)
