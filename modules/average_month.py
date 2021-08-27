"""
This module calculates and displays average highest, lowest temperatures
and average mean humidity for a given month
"""
from constants import WEATHER_FILES_DIR, months_list
from modules.data_models import MonthData
from modules.utils import get_year_month


def generate_averages_report_month(averages):
    """
    Generates report using the averages list and displays
    1. average highest temperature
    2. average lowest temperature
    3. average mean humidity
    for a month
    Args:
        averages: a list of length 3, averages where
            averages[0](int) = avg_highest_temperature
            averages[1](int) = avg_lowest_temperature
            averages[2](int) = avg_mean_humidity
    Returns:
        None
    """

    value_units = [("Highest", "C"), ("Lowest", "C"), ("Mean Humidity", "%")]
    for i, val in enumerate(value_units):
        print(f"Average {val[0]}: {averages[i]}{val[1]}")


def averages_month(year_month, path=WEATHER_FILES_DIR):
    """
    Calculates and displays the average highest, lowest temperatures
    and average mean humidity for a given month
    Args:
        year_month(str): value containing 4 digit year and 2 digit month
                        e.g: '2002/02', '2003/04'.
        path(str): a value containing path to weather files e.g: 'weatherfiles/'
    Returns:
        (int or None):  0 for success
                        Or
                        None for failure
    """

    year, month = get_year_month(year_month)
    # convert from number to month name
    month = months_list[month - 1][0:3]
    averages = MonthData(year, month, path).get_averages()
    if averages is None:
        return None
    generate_averages_report_month(averages)
    return 0
