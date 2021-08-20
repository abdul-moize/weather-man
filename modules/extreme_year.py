"""
This module will return the highest and lowest temperatures of a
given year along with the most humid day.
"""
import constants
from modules.utils import read_data


def get_highest_temperature(line):
    """
    Returns the highest temperature from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
         (int or None): highest temperature
                        OR
                        None if there is no entry
    """
    try:
        highest_temperature = int(line[1])
        return highest_temperature
    except ValueError:
        return None


def get_lowest_temperature(line):
    """
    Returns the lowest temperature from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          (int or None):    lowest temperature
                            OR
                            None if there is no entry
    """
    try:
        return int(line[3])
    except ValueError:
        return None


def get_max_humidity(line):
    """
    Returns the maximum humidity from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          (int or None):    max humidity
                            Or
                            None if there is no entry or wrong entry
    """
    try:
        return int(line[7])
    except ValueError:
        return None


def calculate_extremes(year, path):
    """
    This function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. max highest temperature
    2. max lowest temperature
    3. max humidity
    Args:
        year(str): a value containing 4 digit year like: '2002', '2003'.
        path(str): a value containing path like: 'weatherfiles/'
    Returns:
           (list or None):  a 3x2 list maximums where
                            maximums[0] = [max_highest_temperature, date]
                            maximums[1] = [max_lowest_temperature, date]
                            maximums[2] = [max_humidity, date]
                            date here is a string like: '2002-4-1', '2004-3-14'
                            or None if there is an error or failure
    """
    # max_temperature contains highest temperature and
    # date on which the temperature was highest
    # min_temperature contains lowest temperature and date
    # max_humidity contains most humidity and date
    max_temperature = [0, ""]
    min_temperature = [0, ""]
    max_humidity = [0, ""]
    initialized = False
    for lines in read_data(year, path):
        for line in lines:
            # since readlines() returns ['linedata1\n','linedata2\n',...]
            # line contains ['linedata\n'] with split by '\n' to get ['linedata','\n]
            # then we get 'linedata' by grabbing the [0]
            # lastly,  we split by ',' to get the entries parsed
            parsed_line = line.split("\n")[0].split(",")
            date = parsed_line[0]
            if not initialized:
                max_temperature = [get_highest_temperature(parsed_line), date]
                min_temperature = [get_lowest_temperature(parsed_line), date]
                max_humidity = [get_max_humidity(parsed_line), date]
                initialized = True
            else:
                if max_temperature[0] is None:
                    max_temperature = [get_highest_temperature(parsed_line), date]

                if min_temperature[0] is None:
                    min_temperature = [get_lowest_temperature(parsed_line), date]

                if max_humidity[0] is None:
                    max_humidity = [get_max_humidity(parsed_line), date]

            max_temperature_line = get_highest_temperature(parsed_line)
            if max_temperature_line is not None:
                # get max by index 0 which is temperature
                max_temperature = max(
                    max_temperature, [max_temperature_line, date], key=lambda x: x[0]
                )

            min_temperature_line = get_lowest_temperature(parsed_line)
            if min_temperature_line is not None:
                # get min by comparing index 0 elements only
                min_temperature = min(
                    [min_temperature_line, date], min_temperature, key=lambda x: x[0]
                )

            max_humidity_line = get_max_humidity(parsed_line)
            if max_humidity_line is not None:
                max_humidity = max(
                    [max_humidity_line, date], max_humidity, key=lambda x: x[0]
                )

    return [max_temperature, min_temperature, max_humidity] if initialized else None


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
    months_list = [
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
            f"on {months_list[int(month) - 1]} {day}"
        )


def extreme_temperatures_year(year, path=constants.WEATHER_FILES_DIR):
    """
    Calculates extreme temperatures and max humidity for a given year
    Args:
        year(str): a value containing 4 digit year like: '2002', '2003'.
        path(str): a value containing path like: 'weatherfiles/'
    Returns:
        (int or None):  0 for success
                        Or
                        None for error
    """
    maximums = calculate_extremes(year, path)
    if maximums is None:
        return None
    generate_extremes_report(maximums)
    return 0
