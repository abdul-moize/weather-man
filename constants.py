"""
This file contains constant values that are not expected to change throughout
the run of a program
"""
from modules.validators import is_year, is_year_month

ALLOWED_PARAMETERS = ":e:a:c:"
WEATHER_FILES_DIR = "weatherfiles/"
FULL_MONTH_NAME = "%B"
SHORT_MONTH_NAME = "%b"
validators = {"-e": is_year, "-a": is_year_month, "-c": is_year_month}
TEMPERATURE_UNIT = "C"
HUMIDITY_UNIT = "%"
months_list = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
