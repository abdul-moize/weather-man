"""
Weatherman is a software that generates reports about the past weather of murree
"""
import getopt
import sys

from constants import WEATHER_FILES_DIR
from modules.data_models import MonthData, YearData
from modules.utils import get_month_name, get_year_month
from modules.validators import is_year, is_year_month


def re_take_input(allowed_parameters):
    """
    Takes input from user and returns parameters and path
    Args:
        allowed_parameters(str): Value containing allowed flags like ':e:', ':e:a:'
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
    parameters, args = getopt.getopt(parameters, allowed_parameters)
    if args:
        path, parameters = (
            args[0],
            getopt.getopt(args[1:], allowed_parameters)[0],
        )
    return path, parameters


def main():
    """
    The driver function for weatherman.
    Returns:
        None
    """
    allowed_parameters = ":e:a:c:"
    path = WEATHER_FILES_DIR
    parameters, args = getopt.getopt(sys.argv[1:], allowed_parameters)
    if args:
        path, parameters = args[0], getopt.getopt(args[1:], allowed_parameters)[0]
    iteration = 0
    accepted_flags = ["-e", "-a", "-c"]
    validators = [is_year, is_year_month, is_year_month]
    while iteration < len(parameters):
        if len(parameters) < 1:
            iteration = 0
            path, parameters = re_take_input(allowed_parameters)
            continue
        valid_flag = False
        validator = validators[0]
        if accepted_flags.__contains__(parameters[iteration][0]):
            index = accepted_flags.index(parameters[iteration][0])
            validator = validators[index]
            valid_flag = True

        if not valid_flag:
            iteration = 0
            path, parameters = re_take_input(allowed_parameters)
            continue

        if validator(parameters[iteration][1]):
            if parameters[iteration][0] == "-e":
                YearData(parameters[iteration][1], path).generate_extremes_report()
            else:
                year, month = get_year_month(parameters[iteration][1])
                month_data = MonthData(year, get_month_name(month), path)
                if parameters[iteration][0] == "-a":
                    month_data.generate_averages_report_month()
                else:
                    month_data.generate_report_charts()
        else:
            iteration = 0
            path, parameters = re_take_input(allowed_parameters)
            continue

        iteration += 1
        print()


if __name__ == "__main__":
    main()
