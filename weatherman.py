"""
Weatherman is a software that generates reports about the past weather of murree
"""
import getopt
import sys

from constants import ALLOWED_PARAMETERS, WEATHER_FILES_DIR
from modules.data_models import MonthData, ReportGenerator, YearData
from modules.utils import get_year_month, validate_command


def re_take_input():
    """
    Takes input from user and returns parameters and path
    Returns:
        (tuple):    tuple containing path(str) and parameters(list) returned by getopt
                    path contains path to weather files like 'weatherfiles/'
                    parameters contains [[flag(str), argument(str)],...]
    """
    parameters = input(
        "Invalid command. "
        "The correct command format is: 'weatherman.py path flag date' "
        "path is optional"
    )
    path = WEATHER_FILES_DIR
    parameters, args = getopt.getopt(parameters, ALLOWED_PARAMETERS)
    if args:
        path, parameters = (
            args[0],
            getopt.getopt(args[1:], ALLOWED_PARAMETERS)[0],
        )
    return path, parameters


def main():
    """
    The driver function for weatherman.
    Returns:
        None
    """
    path = WEATHER_FILES_DIR
    parameters, args = getopt.getopt(sys.argv[1:], ALLOWED_PARAMETERS)
    if args:
        path, parameters = args[0], getopt.getopt(args[1:], ALLOWED_PARAMETERS)[0]
    iteration = 0
    while iteration < len(parameters):
        if len(parameters) < 1:
            iteration = 0
            path, parameters = re_take_input()
            continue
        flag, flag_argument = parameters[iteration]
        if validate_command(flag, flag_argument):
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
        else:
            iteration = 0
            path, parameters = re_take_input()
            continue

        iteration += 1
        print()


if __name__ == "__main__":
    main()
