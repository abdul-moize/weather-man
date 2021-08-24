"""
This module generates charts on console
"""

from modules.utils import (
    get_date,
    get_highest_temperature,
    get_lowest_temperature,
    number_to_month,
    read_data,
)


def get_all_extremes(year_month, path):
    """
    Appends all extreme temperatures in a file to the list extremes
    Args:
        year_month(str):    Value containing 4 digit year and 2 digit month
                            e.g '2002/5', '2005/6', etc
        path(str):  Value containing path to weather files
                    e.g 'weatherfiles/', 'path/to/files/'
    Returns:
        (list or None): Contains all the extremes of one month
                        an element looks  like: [date(str), max_temp(int), min_temp(int)]
                        Or
                        None for failure
    """
    extremes = []
    for lines in read_data(year_month, path):
        if lines:
            for line in lines:
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
    print(number_to_month[month - 1] + " " + year)
    for entry in extremes:
        day = f"\33[0m{entry[0].split('-')[2]}"
        red_plus = f"\33[91m{'+'*entry[1]}"
        blue_plus = f"\33[94m{'+'*entry[2]}"
        if entry[1] is None:
            entry[1] = "No Entry"
        if entry[2] is None:
            entry[2] = "No Entry"
        entry[1] = f"\33[91m{entry[1]}C"
        entry[2] = f"\33[94m{entry[2]}C"
        report_line = f"{day} {entry[2]} {blue_plus}{red_plus} {entry[1]}"
        print(report_line)


def charts_month(year_month, path):
    """
    Displays chart on screen
    Args:
        year_month(str): Value containing 4 digit year like, '2004/5', '2006/7', etc
        path(str):  Value containing path to weather files
                    e.g 'weatherfiles/', 'path/to/files/'
    Returns:
        (int or None):  0 for success
                        Or
                        None for error
    """
    # split contains [year, month]
    split = year_month.split("/")
    year_month = split[0] + "_" + number_to_month[int(split[1]) - 1]
    extremes = get_all_extremes(year_month, path)
    if extremes is None:
        return None
    generate_report_charts(extremes)
    return 0
