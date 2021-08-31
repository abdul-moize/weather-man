"""
This module provides validators that verify the values of variables
"""
import re


def is_year(year):
    """
    This function verifies if that the value of year
    is a 4 digit year or not
    Args:
        year(str): Value containing 4 digit year e.g '2004', '2005', etc
    Returns:
        (boolean):  True if year contains 4 digit year
                    False if year does not contain 4 digit year
    """
    if isinstance(year, str):
        regex = """
        [1-9]       # starting character must be in range 1-9
        \\d{3}\\b   # must end with 3 digits(0-9)
        """
        if re.match(regex, year, re.VERBOSE):
            return True
    return False


def is_month(month):
    """
    This function verifies that the value of argument month is a
    2 digit month
    Args:
        month(str): Value containing digits(1-9 or 01-12)
    Returns:
        (boolean):  True if month contains digits(1-9 or 01-12)
                    False if it does not contain digits(01-12 or 1-9)
    """
    if isinstance(month, str):
        regex = """
        0?[1-9]\\b  # 0 is optional but must end with a digit(1-9)
        |           # or
        1[0-2]\\b   # start with 1 and end with digit(0-2)
        """
        if re.match(regex, month, re.VERBOSE):
            return True
    return None


def is_year_month(year_month):
    """
    Checks if year_month contains 4 digit year and 2 digit month or not
    e.g '2005/6', '2006/05'
    Args:
        year_month(str):
    Returns:
        (boolean):  True if year_month contains year and month
                    False if year_month is not in correct format
    """

    if isinstance(year_month, str):
        regex = '''
        [1-9]       # starting character must be in range 1-9
        \\d{3}\\b   # must end with 3 digits(0-9)
        /           # followed by a slash
        0?[1-9]\\b  # 0 is optional but must end with a digit(1-9)
        |           # or
        1[0-2]\\b   # start with 1 and end with digit(0-2)
        '''
        if re.match(regex, year_month, re.VERBOSE):
            return True
    return False
