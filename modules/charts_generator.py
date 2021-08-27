"""
This module displays in colored format Highest & Lowest Temperatures
of each day of a given month
"""

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
    split = extremes[0][0].split("-")
    month = int(split[1])
    year = split[0]
    print(get_month_name(month) + " " + year)
    for entry in extremes:
        day = f"\33[0m{entry[0].split('-')[2]}"
        if entry[1] is None or entry[2] is None:
            continue
        red_plus = f"\33[91m{'+' * entry[1]}"
        blue_plus = f"\33[94m{'+' * entry[2]}"
        report_line = f"{day} {blue_plus}{red_plus} \33[0m{entry[2]}C-{entry[1]}C"
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
    month = get_month_name(month)[0:3]
    month_extremes = MonthData(year, month, path).get_month_values()
    if month_extremes is None:
        return None
    generate_report_charts(month_extremes)
    return 0
