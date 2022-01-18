import pytest
from WHO_GHO_API_client.WHO_GHO_API_client import query_parser

def test_query_parser():
    actual = query_parser(IndicatorCode = 'WHOSIS_000001', SpatialDimType = 'Region', TimeDimType = 'year', Dim1 = 'WQ1')
    expected = "https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDimType eq 'Region' and TimeDimType eq 'year' and Dim1 eq 'WQ1'"
    assert actual == expected, "query_parser has not parsed the request url correctly."