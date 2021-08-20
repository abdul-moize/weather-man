"""
This module generates a report which displays average highest and lowest temperature
as well as average max humidity for a given month
"""
from modules.utils import (
    get_highest_temperature,
    get_lowest_temperature,
    get_mean_humidity,
    read_data,
)


def calculate_averages(pattern, path):
    """
    This function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. avg highest temperature
    2. avg lowest temperature
    3. avg mean humidity
    Args:
        pattern: a string which contains a year/month e.g '2006/5', '2007/3'
        path: a string which contains path to a directory containing weather files
    Returns:
        (list or None): list of length 3, averages where
                        averages[0] = avg_highest_temperature
                        averages[1] = avg_lowest_temperature
                        averages[2] = avg_mean_humidity
                        Or
                        None for failure
    """
    sum_highest_temperature = 0
    sum_lowest_temperature = 0
    sum_mean_humidity = 0
    lines = []
    for lines in read_data(pattern, path):
        if lines is None:
            return None
        for line in lines:
            parsed_line = line.split("\n")[0].split(",")
            max_temperature = get_highest_temperature(parsed_line)
            if max_temperature is not None:
                sum_highest_temperature += max_temperature
            min_temperature = get_lowest_temperature(parsed_line)
            if min_temperature is not None:
                sum_lowest_temperature += min_temperature
            mean_humidity = get_mean_humidity(parsed_line)
            if mean_humidity is not None:
                sum_mean_humidity += mean_humidity

    avg_highest_temperature = sum_highest_temperature / len(lines)
    avg_lowest_temperature = sum_lowest_temperature / len(lines)
    avg_mean_humidity = sum_mean_humidity / len(lines)
    averages = [avg_highest_temperature, avg_lowest_temperature, avg_mean_humidity]
    return averages


def generate_averages_report_month(averages):
    """
    Generates report using the averages list and displays
    1. average highest temperature
    2. average lowest temperature
    3. average mean humidity
    Args:
        averages: a list of length 3, averages where
            averages[0] = avg_highest_temperature
            averages[1] = avg_lowest_temperature
            averages[2] = avg_mean_humidity
    Returns:
        None
    """
    value_units = [("Highest", "C"), ("Lowest", "C"), ("Mean Humidity", "%")]
    for i, val in enumerate(value_units):
        print(f"Average {val[0]}: {averages[i]}{val[1]}")


def get_averages_month(month, path):
    """
    Calculates and displays the average highest, lowest temperatures
    and average mean humidity for a given month in given path
    Args:
        month(str): a value containing 4 digit year and 2 digit month like: '2002/02', '2003/04'.
        path(str): a value containing path like: 'weatherfiles/'
    Returns:
        None
    """
    months_list = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    month_split = month.split("/")
    month = month_split[0] + "_" + months_list[int(month_split[1]) - 1]
    averages = calculate_averages(month, path)
    if averages is None:
        return None
    generate_averages_report_month(averages)
    return 0
