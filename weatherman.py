"""
weatherman is a software that generates reports about the past weather of murree
"""
import re
import sys

from modules.average_month import get_averages_month
from modules.extreme_year import extreme_temperatures_year


def main():
    """
    this is a driver function for weatherman.
    :return: nothing
    """
    parameters = sys.argv[1:]
    accepted_flags = ["-e", "-a"]
    accepted_regex = [r"\d{4}", r"\d{4}/(0[1-9]|1[012]|[1-9])"]
    flag_handler = [extreme_temperatures_year, get_averages_month]
    i = 0
    path = ""
    while i < len(parameters):
        if path == "":
            path = "weatherfiles/"
            if len(parameters) < 2:
                parameters = input(
                    "Too less options."
                    ' make sure command is like: "path flag date" path is optional'
                )
                i = 0
                continue
            if parameters[0][0] != "-" and len(parameters) >= 3:
                path, parameters = parameters[0], parameters[1:]
        valid_flag = False
        handler = flag_handler[0]
        j = 0
        for j, val in enumerate(accepted_flags):
            if parameters[i] == val:
                handler = flag_handler[j]
                valid_flag = True
                break
        if not valid_flag:
            parameters = input(
                f"Invalid Flag '{parameters[i]}'. " f"Please enter a valid command: "
            ).split(" ")
            i = 0
            path = ""
            continue
        if re.match(accepted_regex[j], parameters[i + 1]):
            handler(parameters[i + 1], path)
        else:
            parameters = input(
                f"Invalid date '{parameters[i+1]}'. " f"Please enter a valid command: "
            ).split(" ")
            i = 0
            path = ""
            continue
        i += 2
        print()


if __name__ == "__main__":
    main()
