"""
This module will display the highest & lowest temperatures and max humidity of a
given year along with respective dates
"""
from modules.data_models import YearData
from modules.utils import get_month_name


def generate_extremes_report(maximums):
    """
    This function prints/generates a report on the console based on the maximums list
    the report displays the following
    1. max_highest_temperature with date
    2. max_lowest_temperature with date
    3. max_humidity with date
    Args:
        maximums(list):     a 3x2 list every row contains a list like
                            [value, date] value(int)  date(str) is like '2006-3-1'
                            0 index contains [highest_temperature, date]
                            1 index contains [lowest_temperature, date]
                            2 index contains [max_humidity, date]
    Returns:
        None
    """

    starting_message = ["Highest", "Lowest", "Humidity"]
    for index, dictionary in enumerate(maximums):
        month, day = dictionary["date"].split("-")[1:]
        print(
            f"{starting_message[index]}: {dictionary['value']} on "
            f"{get_month_name(int(month))}, {day}"
        )


def extreme_temperatures_year(year, path):
    """
    Calculates Highest & Lowest temperatures and max humidity for a given year
    Args:
        year(str): a value containing 4 digit year like: '2002', '2003'.
        path(str): a value containing path to weather files e.g: 'weatherfiles/'
    Returns:
        (int or None):  0 for success
                        Or
                        None for error
    """
    maximums = YearData(year, path).get_max_extremes_with_date()
    if maximums is None:
        return None
    generate_extremes_report(maximums)
    return 0
