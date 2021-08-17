"""
This module will return the highest and lowest temperatures of a
given year along with the most humid day.
"""

from modules.utils import calculate_extremes


def generate_extremes_report(maximums):
    """
    This function prints/generates a report on the console based on the maximums list
    the report displays the following
    1. max_highest_temperature with date
    2. max_lowest_temperature with date
    3. max_humidity with date
    Args:
        maximums(2d list):  a 3x2 list every row contains a list like
                            [value, date] value(int)  date(str) is like '2006-3-1'
                            0 index contains [highest_temperature, date]
                            1 index contains [lowest_temperature, date]
                            2 index contains [max_humidity, date
    Returns:
        None
    """
    number_to_month = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    message_unit = [("Highest", "C"), ("Lowest", "C"), ("Humidity", "%")]
    for i, val in enumerate(maximums):
        month, day = maximums[i][1].split("-")[1:]
        print(
            f"{message_unit[i][0]}: {str(val[0])}{message_unit[i][1]} "
            f"on {number_to_month[int(month) - 1]} {day}"
        )


def extreme_temperatures_year(year, path):
    """
    This method uses two other methods to calculate max extreme temperatures and max humidity
    for a given year
    Args:
        year(str): a string like: '2002', '2004', etc
        path(str): a string like: 'weatherfiles/'
    Returns:
        an int: 0 for success -1 for error
    """
    maximums = calculate_extremes(year, path)
    if maximums == -1:
        return -1
    generate_extremes_report(maximums)
    return 0
