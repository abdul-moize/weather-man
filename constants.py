"""
This file contains constant values that are not expected to change throughout
the run of a program
"""
import glob

from modules.validators import is_year, is_year_month

ALLOWED_PARAMETERS = ":e:a:c:"
WEATHER_FILES_DIR = "weatherfiles/"
FULL_MONTH_NAME = "%B"
SHORT_MONTH_NAME = "%b"
validators = {"-e": is_year, "-a": is_year_month, "-c": is_year_month}
TEMPERATURE_UNIT = "C"
HUMIDITY_UNIT = "%"
with open(glob.glob(f"{WEATHER_FILES_DIR}*")[0], "r") as f:
    first_line = f.readline()
fields = first_line.split("\n")[0].split(",")
for index, field in enumerate(fields):
    if field == "PKT":
        DATE_INDEX = index
    elif field == "Max TemperatureC":
        MAX_TEMPERATURE_INDEX = index
    elif field == "Min TemperatureC":
        MIN_TEMPERATURE_INDEX = index
    elif field == "Max Humidity":
        MAX_HUMIDITY_INDEX = index
    elif field == " Mean Humidity":
        MEAN_HUMIDITY_INDEX = index
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
