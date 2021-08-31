"""
This file contains constant values that are not expected to change throughout
the run of a program
"""
WEATHER_FILES_DIR = "weatherfiles/"
TEMPERATURE_UNIT = "C"
HUMIDITY_UNIT = "%"
first_line = open(f"{WEATHER_FILES_DIR}Murree_weather_2004_Aug.txt", "r").readline()
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
