"""
This module contains functions that are used frequently
at multiple places in the application
"""
# pylint:disable= global-statement
import glob
from datetime import date

from constants import FULL_MONTH_NAME, validators
from modules.validators import is_month, is_year, is_year_month

DATE_INDEX = None
MAX_TEMPERATURE_INDEX = None
MIN_TEMPERATURE_INDEX = None
MAX_HUMIDITY_INDEX = None
MEAN_HUMIDITY_INDEX = None


def initialize_indexes(path):
    """
    Initializes the indexes from a file in the path
    Args:
        path(str): Value containing path to weather files like 'weatherfiles/'
    Returns:
        (int or None):  0 if indexes are initialized
                        Or
                        None if no files exist in the path
    """
    files = glob.glob(f"{path}*")
    if not files:
        return None
    with open(files[0], "r") as file:
        first_line = file.readline()
    fields = first_line.split("\n")[0].split(",")
    global DATE_INDEX, MIN_TEMPERATURE_INDEX, MAX_TEMPERATURE_INDEX
    global MAX_HUMIDITY_INDEX, MEAN_HUMIDITY_INDEX
    for index, field in enumerate(fields):
        if field == "PKT":
            DATE_INDEX = index
        elif field == "Max TemperatureC":
            MAX_TEMPERATURE_INDEX = index
        elif field == "Min TemperatureC":
            MIN_TEMPERATURE_INDEX = index
        elif field == "Max Humidity":
            MAX_HUMIDITY_INDEX = index
        elif field == " Mean Humidity":
            MEAN_HUMIDITY_INDEX = index
    return 0


def validate_command(flag, flag_input):
    """
    Validates the flag and the flag arguments by using the
    dictionary validators in constants.py
    Args:
        flag(str): Value containing flag e.g '-e', '-a', '-c'
        flag_input(str): Value containing the year or year_month e.g '2006', '2006/6'
    Returns:
        None
    """
    is_valid = False
    if flag in validators:
        if validators[flag](flag_input):
            is_valid = True
        else:
            print(f"Invalid flag argument '{flag_input}' for flag '{flag}'")
    else:
        print(f"Invalid flag '{flag}'")
    return is_valid


def parse_line(line):
    """
    Parses a raw line read from weather file to a list of strings
    Args:
        line(str):   raw line read from weather file
    Returns:
        (list): list of strings containing different fields
    """
    return line.split("\n")[0].split(",")


def pattern_search(pattern, path):
    """
    This function returns all the files in the given path that match the pattern given
    Args:
        pattern(str): a string which contains any pattern e.g '2006', '2007', '2005/6', etc
        path(str): a value containing path like: 'weatherfiles/'
    Returns:
        (list or None): path to all the files matching the pattern
                        Or
                        None if no files found
    """
    return glob.glob(path + f"*{pattern}*")


def read_data(pattern, path):
    """
    This function reads data from the files in the given path that match the pattern
    Args:
        pattern(str): value containing 4 digit year like '2002', '2003', '2004', etc
        path(str): value containing path like: 'weatherfiles/'
    Returns:
        (Generator or list):
            Generator object containing all lines of a file
            Or
            empty list if no file exists for a given year
    """
    files = pattern_search(pattern, path)
    if not files:
        yield []
    for i in files:
        with open(i, "r") as file:
            # skip first line as it contains field names
            yield file.readlines()[1:]


def get_date(line):
    """
    Returns the date from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
         (date or None):    date object
                            OR
                            None if there is no entry
    """
    try:
        # split into [yyyy, mm, dd] then convert to int and return date object
        return date(*[int(i) for i in line[DATE_INDEX].split("-")])
    except IndexError:
        return None


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
        highest_temperature = int(line[MAX_TEMPERATURE_INDEX])
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
        return int(line[MIN_TEMPERATURE_INDEX])
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
        return int(line[MAX_HUMIDITY_INDEX])
    except ValueError:
        return None


def get_mean_humidity(line):
    """
    Returns the mean humidity from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          (int or None):    mean humidity
                            Or
                            None if there is no entry or wrong entry
    """
    try:
        return int(line[MEAN_HUMIDITY_INDEX])
    except ValueError:
        return None


def get_month_name(number, flag=FULL_MONTH_NAME):
    """
    Return the name of the month depending on the number
    Args:
        number(int):    integer in range 1-12
        flag(str):  '%B' for full month name like 'January, February'
                    '%b' for 3 characters like 'Jan', 'Feb'
    Returns:
        (str or None):  str containing month name
                        Or
                        None if number is not in the range 1-12
    """
    if isinstance(number, int) and 0 < number < 13:
        return date(1, number, 1).strftime(flag)
    return None


def get_month(month):
    """
    Checks if the value in year contains a 4 digit year and returns
    the int value
    Args:
        month(str):  Value containing digits(01-12 or 1-9)
    Returns:
        (int or None):  integer value containing a number(1-12)
                        Or
                        None if month does not contain digits(1-9 or 01-12)
    """

    if is_month(month):
        return int(month)
    return None


def get_year(year):
    """
    Returns integer containing 4 digit year
    Args:
        year(str):  Value containing 4 digit year e.g '2004', '2005', etc
    Returns:
        (int or None):  Integer containing 4 digit year
                        Or
                        None if year is not in valid format
    """
    if is_year(year):
        return int(year)
    return None


def get_year_month(year_month):
    """
    Returns a tuple containing  two integers year and month
    Args:
        year_month(str):    Value containing 4 digit year and 2 digit month
                            like '2004/01', '2004/1', etc
    Returns:
        (tuple or None):    A tuple containing year and month
                            (year(int), month(int))
                            Or
                            None if year_month is not in right format
    """
    if is_year_month(year_month):
        year, month = year_month.split("/")
        return get_year(year), get_month(month)
    return None
