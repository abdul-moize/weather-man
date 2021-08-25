"""
Weatherman is a software that generates reports about the past weather of murree
"""
import getopt
import sys

from constants import WEATHER_FILES_DIR
from modules.average_month import averages_month
from modules.charts_month import charts_month
from modules.extreme_year import extreme_temperatures_year
from modules.validators import is_year, is_year_month


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
    flag_handler = [extreme_temperatures_year, averages_month, charts_month]
    while iteration < len(parameters):
        if len(parameters) < 1:
            parameters = input(
                "Invalid command. "
                "The correct command format is: 'weatherman.py path flag date' "
                "path is optional"
            )
            iteration = 0
            path = WEATHER_FILES_DIR
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            if args:
                path, parameters = (
                    args[0],
                    getopt.getopt(args[1:], allowed_parameters)[0],
                )
            continue
        valid_flag = False
        handler = flag_handler[0]
        validator = validators[0]
        if accepted_flags.__contains__(parameters[iteration][0]):
            index = accepted_flags.index(parameters[iteration][0])
            handler = flag_handler[index]
            validator = validators[index]
            valid_flag = True
        if not valid_flag:
            parameters = input(
                f"Invalid Flag '{parameters[iteration][0]}'. "
                f"Please enter a valid command: "
            ).split(" ")
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            path = WEATHER_FILES_DIR
            if args:
                path, parameters = (
                    args[0],
                    getopt.getopt(args[1:], allowed_parameters)[0],
                )
            iteration = 0
            continue
        if validator(parameters[iteration][1]):
            handler(parameters[iteration][1], path)
        else:
            parameters = input(
                f"Invalid date '{parameters[iteration][1]}'. "
                f"Please enter a valid command: "
            ).split(" ")
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            path = WEATHER_FILES_DIR
            if args:
                path, parameters = (
                    args[0],
                    getopt.getopt(args[1:], allowed_parameters)[0],
                )
            iteration = 0
            continue
        iteration += 1
        print()


if __name__ == "__main__":
    main()
