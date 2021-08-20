"""
This file contains methods that will provide ease to programmers
"""
import glob


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
        year(str): a value containing 4 digit year like '2002', '2003', '2004', etc
        path(str): a value containing path like: 'weatherfiles/'
    Returns:
        generator object containing row of a file or None if no file exists for a given year
    """
    files = pattern_search(year, path)
    if not files:
        print(f"We don't have information regarding the year {year} in the given path")
        yield None
    for i in files:
        with open(i, "r") as file:
            # skip first line as it contains field names
            yield file.readlines()[1:]


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
        return int(line[8])
    except ValueError:
        return None
