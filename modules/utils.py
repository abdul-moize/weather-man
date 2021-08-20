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
