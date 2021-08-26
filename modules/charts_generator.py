"""
This module displays in colored format Highest & Lowest Temperatures
of each day of a given month
"""

from constants import WEATHER_FILES_DIR
from modules.utils import (
    get_date,
    get_highest_temperature,
    get_lowest_temperature,
    get_month_name,
    get_year_month,
    read_data,
)


def get_all_extremes(year, month, path):
    """
    Appends Highest & Lowest temperatures of each day in the file which matches the year and month
    to the list extremes and returns it
    Args:
        year(str or int):  Value containing 4 digit year e.g: '2004', '2005'
        month(str): Value containing 3 character month name e.g: 'Feb', 'Aug'.
        path(str):  Value containing path to weather files
                    e.g 'weatherfiles/', 'path/to/files/'
    Returns:
        (list or None): Contains all the extremes of one month
                        an element looks  like: [date(str), max_temp(int), min_temp(int)]
                        Or
                        None for failure
    """
    extremes = []
    for month_data in read_data(f"{year}_{month}", path):
        for line in month_data:
            parsed_line = line.split("\n")[0].split(",")
            date = get_date(parsed_line)
            max_temp = get_highest_temperature(parsed_line)
            min_temp = get_lowest_temperature(parsed_line)
            extremes.append([date, max_temp, min_temp])
    return extremes if len(extremes) > 0 else None


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


def charts_month(year_month, path=WEATHER_FILES_DIR):
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
    extremes = get_all_extremes(year, month, path)
    if extremes is None:
        return None
    generate_report_charts(extremes)
    return 0
