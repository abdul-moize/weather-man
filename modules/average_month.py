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
        a list: length 3, averages where
    averages[0] = avg_highest_temperature
    averages[1] = avg_lowest_temperature
    averages[2] = avg_mean_humidity
    """
    # entries of the month
    entries = 0
    sum_highest_temperature = 0
    sum_lowest_temperature = 0
    sum_mean_humidity = 0
    # indexes to sum values with.
    # highest temperature is stored at index 1 of weather reading
    # lowest temperature is stored at index 3 of weather reading
    # max humidity is stored at index 7 of weather reading
    # see the weather files for further explanation
    for lines in read_data(pattern, path):
        entries = len(lines)
        for line in lines:
            parsed_line = line.split("\n")[0].split(",")
            sum_highest_temperature += get_highest_temperature(parsed_line)
            sum_lowest_temperature += get_lowest_temperature(parsed_line)
            sum_mean_humidity += get_mean_humidity(parsed_line)

    avg_highest_temperature = sum_highest_temperature / entries
    avg_lowest_temperature = sum_lowest_temperature / entries
    avg_mean_humidity = sum_mean_humidity / entries
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
    This function uses 2 methods to calculate and display on console
    the average highest and lowest temperatures and average mean humidity
    for a given month in given path
    Args:
        month: a string which contains year/month like: '2006/6', '2007/3' , etc
        path: a string which contains path to weather files like: 'path/'
    Returns:
        None
    """
    number_to_month = [
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
    month = number_to_month[int(month.split("/")[1]) - 1]
    averages = calculate_averages(month, path)
    if averages == -1:
        return -1
    generate_averages_report_month(averages)
    return 0
