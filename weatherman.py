"""
weatherman is a software that generates reports about the past weather of murree
"""
import getopt
import re
import sys

import constants
from modules.average_month import get_averages_month
from modules.charts_month import charts_month
from modules.extreme_year import extreme_temperatures_year


def main():
    """
    The driver function for weatherman.
    Returns:
        None
    """
    allowed_parameters = ":e:a:c:"
    parameters, args = getopt.getopt(sys.argv[1:], allowed_parameters)
    if args:
        path, parameters = args[0], getopt.getopt(args[1:], allowed_parameters)[0]
    iteration = 0
    accepted_flags = ["-e", "-a", "-c"]
    accepted_regex = [r"\d{4}", r"\d{4}/\d{1,2}", r"\d{4}/\d{1,2}"]
    flag_handler = [extreme_temperatures_year, get_averages_month, charts_month]
    path = constants.WEATHER_FILES_DIR
    while iteration < len(parameters):
        if len(parameters) < 1:
            parameters = input(
                "Invalid command. "
                "The correct command format is: 'weatherman.py path flag date' "
                "path is optional"
            )
            iteration = 0
            path = constants.WEATHER_FILES_DIR
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            if args:
                path, parameters = (
                    args[0],
                    getopt.getopt(args[1:], allowed_parameters)[0],
                )
            continue
        valid_flag = False
        handler = flag_handler[0]
        j = 0
        if accepted_flags.__contains__(parameters[iteration][0]):
            handler = flag_handler[accepted_flags.index(parameters[iteration][0])]
            valid_flag = True
        if not valid_flag:
            parameters = input(
                f"Invalid Flag '{parameters[iteration][0]}'. "
                f"Please enter a valid command: "
            ).split(" ")
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            path = constants.WEATHER_FILES_DIR
            if args:
                path, parameters = (
                    args[0],
                    getopt.getopt(args[1:], allowed_parameters)[0],
                )
            iteration = 0
            continue
        if re.match(accepted_regex[j], parameters[iteration][1]):
            handler(parameters[iteration][1], path)
        else:
            parameters = input(
                f"Invalid date '{parameters[iteration][1]}'. "
                f"Please enter a valid command: "
            ).split(" ")
            parameters, args = getopt.getopt(parameters, allowed_parameters)
            path = constants.WEATHER_FILES_DIR
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
