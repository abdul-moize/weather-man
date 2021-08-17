"""
This file contains methods that will provide ease to programmers
"""
import glob

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


def get_date(line):
    """
    Returns the 0th index of passed line
    Args:
        line(list): list which contains all fields of a weatherfile
    Returns:
        string: string contains date like '2002-3-1' year-month-day
    """
    return line[0]


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
