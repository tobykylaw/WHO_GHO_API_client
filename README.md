# WHO_GHO_API_client

A hassle-free way to access the WHO Global Health Observatory database!

## Introduction
The World Health Organization Global Health Observatory hosts a database containing global health indicator measurements and statistics content, and the GHO OData API provides a query interface.

API documentation: [https://www.who.int/data/gho/info/gho-odata-api](https://www.who.int/data/gho/info/gho-odata-api)

Base URL: [https://ghoapi.azureedge.net/api/](https://ghoapi.azureedge.net/api/)

## Overview of WHO_GHO_API_client package functions:
The database contains measurement for indicators of health (eg. immunization coverage, air pollution attributable deaths), as well as a plethora of dimensions in which these indicators are measured (eg. age, sex, country/region, income). 
To make it easier to obtain data without directly interacting with the API, this package aims to provide a API wrapper/client that allows the user to view and search indicators and dimensions available in the database, select the dimensions and indicators they are interested in, and easily download the data they need in form of a filtered pandas dataframe, which can be exported as csv files if needed.

The package will be broken down into the following 5 main and accessory functions, and executed accordingly:

* `get_indicators()`: returns all possible indicators of global health in the database, with the option of implementing a filtered search on the indicators names retrieved.

* `get_records()`: retrieves indicator records based on selected dimension filters, which depends on
     - `query_parser()`: Allows user to specify dimensions and indicators they would like to retrieve from the database in the arguments, and parse them into the format that could be submitted via a get request.

* `get_dimensions()`: returns all possible dimensions of measurement in the database, with the option of implementing a regex search on the dimensions retrieved by Function 3. 

* `get_dimension_values()`: implement a regex search on the values of a specific dimension.

## Resource Guides and Documentation
[See vignette here](../Vignette_WHO_GHO_API_client.ipynb)

[See documentation here](./docs/_build/html/modules.html)

[Github repository](https://github.com/tobykylaw/WHO_GHO_API_client) 

[TestPyPI page](https://test.pypi.org/project/who-gho-api-client/)

## Installation

Installation will only be successful when all dependencies are pre-installed. Please follow the prompts.
```bash
$ pip install -i https://test.pypi.org/simple/ who-gho-api-client
```

## Example usage in Python Console

```
# Importing package functions
>>> from WHO_GHO_API_client import WHO_GHO_API_client as GHO

# Example function calls
>>> GHO.get_indicators()
>>> GHO.search_dimensions()
>>> GHO.get_records()

# Docstrings for package functions
>>> help(GHO.query_parser)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`WHO_GHO_API_client` was created by Toby Law. It is licensed under the terms of the MIT license.

## Credits

`WHO_GHO_API_client` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
