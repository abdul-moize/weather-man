"""
This module will return the highest and lowest temperatures of a
given year along with the most humid day.
"""

from modules.utils import (get_highest_temperature, get_lowest_temperature,
                           get_max_humidity, read_data)


def calculate_extremes(year, path):
    """
    This function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. max highest temperature
    2. max lowest temperature
    3. max humidity
    Args:
        year: a string which contains a year e.g '2006', '2007'
        path: a string which contains path to a directory containing weather files
    Returns:
           a 2d list or int: a 3x2 list maximums where
                            maximums[0] = [max_highest_temperature, date]
                            maximums[1] = [max_lowest_temperature, date]
                            maximums[2] = [max_humidity, date]
                            date here is a string like: '2002-4-1', '2004-3-14'
                            or an int if there is an error or failure
    """
    # max_temperature contains highest temperature and
    # date on which the temperature was highest
    # min_temperature contains lowest temperature and date
    # max_humidity contains most humidity and date
    max_temperature = [0, ""]
    min_temperature = [0, ""]
    max_humidity = [0, ""]
    initialized = False
    # indexes to compare values with.
    # highest temperature is stored at index 1 of weather reading
    # lowest temperature is stored at index 3 of weather reading
    # max humidity is stored at index 7 of weather reading
    # see the weather files for further explanation
    indexes = [1, 3, 7]
    for lines in read_data(year, path):
        for line in lines:
            # since readlines() returns ['linedata1\n','linedata2\n',...]
            # line contains ['linedata\n'] with split by '\n' to get ['linedata','\n]
            # then we get 'linedata' by grabbing the [0]
            # lastly,  we split by ',' to get the entries parsed
            parsed_line = line.split("\n")[0].split(",")
            date = parsed_line[0]
            if not initialized:
                max_temperature = [int(parsed_line[indexes[0]]), date]
                min_temperature = [int(parsed_line[indexes[1]]), date]
                max_humidity = [int(parsed_line[indexes[2]]), date]
                initialized = True
                continue

            max_temperature_line = get_highest_temperature(parsed_line)
            if max_temperature_line != -1000:
                if max_temperature_line >= max_temperature[0]:
                    max_temperature = [max_temperature_line, date]

            min_temperature_line = get_lowest_temperature(parsed_line)
            if min_temperature_line != -1000:
                if min_temperature_line <= min_temperature[0]:
                    min_temperature = [min_temperature_line, date]

            max_humidity_line = get_max_humidity(parsed_line)
            if max_humidity_line != -1000:
                if max_humidity_line >= max_humidity[0]:
                    max_temperature = [max_humidity_line, date]

    return [max_temperature, min_temperature, max_humidity] if initialized else -1


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
