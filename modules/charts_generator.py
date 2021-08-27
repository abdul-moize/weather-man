"""
This module displays in colored format Highest & Lowest Temperatures
of each day of a given month
"""

from constants import TEMPERATURE_UNIT
from modules.data_models import MonthData
from modules.utils import get_month_name, get_year_month


def generate_report_charts(extremes):
    """
    This function displays month's report on console
    A report looks like
    "Month Year"
    "day1 lowest_temp ++++++++++++++ highest_temp"
    "day2 lowest_temp ++++++++++++++ highest_temp"
    .
    .
    .
    "day30 lowest_temp ++++++++++++++ highest_temp"
    Args:
        extremes(list): contains all the entries of one month
                        entry = [highest_temp, lowest_temp, mean_humidity]
    Returns:
        None
    """
    year, month = extremes[0][0:2]
    print(f"{month} {year}")
    for entry in extremes:
        day = f"\33[0m{entry[2]}"
        if entry[3] is None or entry[4] is None:
            continue
        red_plus = f"\33[91m{'+' * entry[3]}"
        blue_plus = f"\33[94m{'+' * entry[4]}"
        report_line = (
            f"{day} {blue_plus}{red_plus} "
            f"\33[0m{entry[4]}{TEMPERATURE_UNIT}-{entry[3]}{TEMPERATURE_UNIT}"
        )
        print(report_line)


def charts_month(year_month, path):
    """
    Displays Highest & Lowest temperatures of each day of month on screen
    Args:
        year_month(str): Value containing 4 digit year like, '2004/5', '2006/7', etc
        path(str):  Value containing path to weather files
                    e.g 'weatherfiles/', 'path/to/files/'
    Returns:
        (int or None):  0 for success
                        Or
                        None for error
    """
    year, month = get_year_month(year_month)
    # convert from number to month name
    month = get_month_name(month)
    month_extremes = MonthData(year, month, path).get_month_values()
    if month_extremes is None:
        return None
    generate_report_charts(month_extremes)
    return 0
