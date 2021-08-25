"""
This file contains methods that will provide ease to programmers
"""
import glob

from constants import (
    DATE_INDEX,
    MAX_HUMIDITY_INDEX,
    MAX_TEMPERATURE_INDEX,
    MEAN_HUMIDITY_INDEX,
    MIN_TEMPERATURE_INDEX,
)
from modules.validators import is_month, is_year, is_year_month


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


def read_data(year, path):
    """
    This function reads data from the files of a particular year
    Args:
        year(str): value containing 4 digit year like '2002', '2003', '2004', etc
        path(str): value containing path like: 'weatherfiles/'
    Returns:
        (Generator or list):
            Generator object containing all lines of a file
            Or
            empty list if no file exists for a given year
    """
    files = pattern_search(year, path)
    if not files:
        print(f"We don't have information regarding the year {year} in the given path")
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
         (str or None): date in format yyyy-mm-dd e.g '2004-3-3'
                        OR
                        None if there is no entry
    """
    try:
        return line[DATE_INDEX]
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
