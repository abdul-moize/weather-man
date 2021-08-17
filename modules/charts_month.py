"""
This module generates charts on screen
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
        year_month(str): string like '2002/5', '2005/6', etc
        path(str): string like path, 'weatherfiles/', 'path/to/files/'
    Returns:
        extremes(list): contains all the extremes of one month
                        an element looks  like: [date(str), max_temp(int), min_temp(int)]
    """
    extremes = []
    for lines in read_data(year_month, path):
        for line in lines:
            parsed_line = line.split("\n")[0].split(",")
            date = get_date(parsed_line)
            max_temp = get_highest_temperature(parsed_line)
            min_temp = get_lowest_temperature(parsed_line)
            extremes.append([date, max_temp, min_temp])
    return extremes if len(extremes) != 0 else -1


def generate_report_charts(extremes):
    """
    This function displays a month report on console
    The report consists
    1. day(int)
    :param extremes:
    :return:
    """
    for i in extremes:
        date = i[0].split("-")[2]
        red_plus = f"\33[91m{'+'*i[1]}"
        blue_plus = f"\33[94m{'+'*i[2]}"
        if i[1] == -1000:
            i[1] = "No Entry"
        if i[2] == -1000:
            i[2] = "No Entry"

        print(f"\33[0m{date} \33[94m{i[2]}C {blue_plus}", end="")
        print(f"{red_plus} {i[1]}C")


def charts_month(year_month, path):
    """
    This function uses get_all_extremes() to get all readings of a month
    Then it uses generate_report_charts() to print report on console
    Args:
        year_month(str): string like, '2004/5', '2006/7', etc
        path(str):  path like, 'weatherfiles/', 'path/to/files/'
    Returns:
        an int: 0 for success -1 for error
    """
    # split contains [year, month]
    split = year_month.split("/")
    year_month = split[0] + "_" + number_to_month[int(split[1]) - 1]
    extremes = get_all_extremes(year_month, path)
    if extremes == -1:
        return -1
    generate_report_charts(extremes)
    return 0
