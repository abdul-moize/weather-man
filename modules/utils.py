"""
This file contains methods that will provide ease to programmers
"""
import glob


def pattern_search(pattern, path):
    """
    This function returns all the files in the given path that match the pattern given
     Args:
        pattern(str): a string which contains any pattern e.g '2006', '2007', '2005/6', etc
        path(str): a string which contains path to a directory containing weather files
    Returns:
        a list: path to all the files matching the pattern
    """
    return glob.glob(path + f"*{pattern}*")


def read_data(year, path):
    """
    This function reads data from the files of a particular year
    Args:
        year(str): 4digit string like '2002', '2003', '2004', etc
        path(str): like any path string 'weatherfile/', 'path/to/files', etc
    Returns:
        generator object containing row of a file or -1 if no file exists for a given year
    """
    files = pattern_search(year, path)
    if not files:
        print(
            f"We don't have information regarding the " f"year {year} in the given path"
        )
        yield -1
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
         highest_temperature(int): Value stored at index 1 of line is highest temperature
    """
    highest_temperature = int(line[1]) if line[1] != "" else -1000
    return highest_temperature


def get_lowest_temperature(line):
    """
    Returns the lowest temperature from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          an int: either the lowest temperature or -1000 if there is no entry
    """
    return int(line[3]) if line[3] != "" else -1000


def get_max_humidity(line):
    """
    Returns the maximum humidity from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          an int: either the max humidity or -1000 if there is no entry
    """
    return int(line[7]) if line[7] != "" else -1000


def get_mean_humidity(line):
    """
    Returns the mean humidity from the line read of a weather file
    Args:
        line(list): a list of strings containing different fields at different index
                    please have a look at any weatherfile for more clarity
    Returns:
          an int: either the mean humidity or -1000 if there is no entry
    """
    return int(line[8]) if line[8] != "" else -1000
