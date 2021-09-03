"""
Weatherman is a software that generates reports about the past weather of murree
"""
import sys
from getopt import GetoptError, getopt

from constants import ALLOWED_PARAMETERS, WEATHER_FILES_DIR
from modules.data_models import MonthData, ReportGenerator, YearData
from modules.utils import get_year_month, initialize_indexes, validate_command


def re_take_input():
    """
    Takes input from user and returns parameters and path
    Returns:
        (tuple):    tuple containing path(str) and parameters(list) returned by getopt
                    path contains path to weather files like 'weatherfiles/'
                    parameters contains [[flag(str), argument(str)],...]
    """
    parameters = input(
        "The correct command format is: 'weatherman.py path flag date' "
        "path is optional: "
    ).split(" ")
    if len(parameters) <= 1:
        print("Too few options")
        return re_take_input()
    try:
        path = WEATHER_FILES_DIR
        parameters, args = getopt(parameters, ALLOWED_PARAMETERS)
        if args:
            path = args[0]

        if not path.endswith("/"):
            path += "/"
        if not parameters:
            parameters = getopt(args[1:], ALLOWED_PARAMETERS)[0]

        return path, parameters
    except GetoptError:
        print("Invalid flag or no flag argument")
        return re_take_input()


def main():
    """
    The driver function for weatherman.
    Returns:
        None
    """
    try:
        path = WEATHER_FILES_DIR
        parameters, args = getopt(sys.argv[1:], ALLOWED_PARAMETERS)
        if args:
            path, parameters = args[0], getopt(args[1:], ALLOWED_PARAMETERS)[0]
    except GetoptError:
        print("Invalid flag or no flag argument")
        path, parameters = re_take_input()
    iteration = 0
    valid_input = True
    while iteration < len(parameters):
        flag, flag_argument = parameters[iteration]
        if initialize_indexes(path) is None:
            print(
                f"There are no weather files in {path}. " f"Please give a correct path"
            )
            valid_input = False

        if not validate_command(flag, flag_argument):
            valid_input = False

        if not valid_input:
            iteration = 0
            valid_input = True
            path, parameters = re_take_input()
            continue
        iteration += 1

    for parameter in parameters:
        flag, flag_argument = parameter
        if flag == "-e":
            year_data = YearData(flag_argument, path)
            ReportGenerator(year_data=year_data).generate_extremes_report()
        else:
            year, month = get_year_month(flag_argument)
            month_data = MonthData(year, month, path)
            if flag == "-a":
                ReportGenerator(month_data).generate_averages_report_month()
            elif flag == "-c":
                ReportGenerator(month_data).generate_report_charts()
        print()


if __name__ == "__main__":
    main()
