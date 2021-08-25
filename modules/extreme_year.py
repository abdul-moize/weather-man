"""
This module will display the highest & lowest temperatures and max humidity of a
given year along with respective dates
"""
from constants import WEATHER_FILES_DIR, months_list
from modules.utils import (
    get_date,
    get_highest_temperature,
    get_lowest_temperature,
    get_max_humidity,
    read_data,
)
from modules.validators import is_year


def calculate_extremes(year, path):
    """
    This function filters and returns the highest, lowest temperatures and max humidity
    from weather files of a given year in path
    1. max highest temperature
    2. max lowest temperature
    3. max humidity
    Args:
        year(str or int): Value containing 4 digit year like: '2002', '2003'.
        path(str): Value containing path to weather files e.g: 'weatherfiles/'
    Returns:
           (list or None):  a 3x2 list maximums where
                            maximums[0] = [max_highest_temperature(int), date(str)]
                            maximums[1] = [max_lowest_temperature(int), date(str)]
                            maximums[2] = [max_humidity(int), date(str)]
                            or None if there are no files for the given year
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
            date = get_date(parsed_line)
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
        maximums(list):     a 3x2 list every row contains a list like
                            [value, date] value(int)  date(str) is like '2006-3-1'
                            0 index contains [highest_temperature, date]
                            1 index contains [lowest_temperature, date]
                            2 index contains [max_humidity, date]
    Returns:
        None
    """

    message_unit = [("Highest", "C"), ("Lowest", "C"), ("Humidity", "%")]
    for i, val in enumerate(maximums):
        month, day = maximums[i][1].split("-")[1:]
        print(
            f"{message_unit[i][0]}: {str(val[0])}{message_unit[i][1]} "
            f"on {months_list[int(month) - 1]} {day}"
        )


def extreme_temperatures_year(year, path=WEATHER_FILES_DIR):
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
    if is_year(year):
        maximums = calculate_extremes(year, path)
        if maximums is None:
            return None
        generate_extremes_report(maximums)
        return 0
    return None
