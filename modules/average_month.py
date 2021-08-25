"""
This module generates a report which displays average highest and lowest temperature
as well as average mean humidity for a given month
"""
from constants import WEATHER_FILES_DIR, months_list
from modules.utils import (
    get_highest_temperature,
    get_lowest_temperature,
    get_mean_humidity,
    get_year_month,
    read_data,
)


def calculate_averages(year, month, path):
    """
    Calculates average of highest_temperature, lowest_temperature and mean_humidity
    from file with names that match the year and month in given path
    1. avg highest temperature
    2. avg lowest temperature
    3. avg mean humidity
    Args:
        year(str or int):  Value containing 4 digit year e.g: '2004', '2005'
        month(str): Value containing 3 character month name e.g: 'Feb', 'Aug'.
        path(str): a value containing path to weather files e.g: 'weatherfiles/'
    Returns:
        (list or None): list of length 3, averages where
                        averages[0](float) = avg_highest_temperature
                        averages[1](float) = avg_lowest_temperature
                        averages[2](float) = avg_mean_humidity
                        Or
                        None for failure
    """

    sum_highest_temperature = 0
    sum_lowest_temperature = 0
    sum_mean_humidity = 0
    lines = []
    for lines in read_data(f"{year}_{month}", path):
        for line in lines:
            parsed_line = line.split("\n")[0].split(",")

            sum_highest_temperature += get_highest_temperature(parsed_line) or 0
            sum_lowest_temperature += get_lowest_temperature(parsed_line) or 0
            sum_mean_humidity += get_mean_humidity(parsed_line) or 0

    if lines:
        avg_highest_temperature = sum_highest_temperature / len(lines)
        avg_lowest_temperature = sum_lowest_temperature / len(lines)
        avg_mean_humidity = sum_mean_humidity / len(lines)
        averages = [
            avg_highest_temperature,
            avg_lowest_temperature,
            avg_mean_humidity,
        ]
        return averages
    return None


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

    if not isinstance(year_month, str):
        return None
    year, month = get_year_month(year_month)
    # convert from number to month name
    month = months_list[month - 1][0:3]
    averages = calculate_averages(year, month, path)
    if averages is None:
        return None
    generate_averages_report_month(averages)
    return 0
