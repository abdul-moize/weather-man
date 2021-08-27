"""
This module contains classes for easy data management
"""
from constants import HUMIDITY_UNIT, TEMPERATURE_UNIT, WEATHER_FILES_DIR
from modules.utils import (
    get_date,
    get_highest_temperature,
    get_lowest_temperature,
    get_max_humidity,
    get_mean_humidity,
    get_month_name,
    parse_line,
    read_data,
)


class DayData:
    """
    This class holds data of a particular day
    """

    def __init__(self, line):
        """
        Initializes the line member and calls populate to initialize other members
        Args:
            line(list): list of strings containing all data from line read of weather file
        """
        self.line = line
        self.populate()

    def populate(self):
        """
        Sets the values of highest_temperature, lowest_temperature, max_humidity,
        mean_humidity and date by using the parsed_line
        Returns:
            None
        """
        self.highest_temperature = get_highest_temperature(self.line)
        self.lowest_temperature = get_lowest_temperature(self.line)
        self.max_humidity = get_max_humidity(self.line)
        self.mean_humidity = get_mean_humidity(self.line)
        self.date = get_date(self.line)

    def get_max_temperature(self):
        """
        Returns the highest_temperature, can be None
        Returns:
            (int or None):  highest_temperature in degree celsius
                            Or
                            None
        """

        return self.highest_temperature

    def get_min_temperature(self):
        """
        Returns the lowest_temperature, can be None
        Returns:
            (int or None):  lowest_temperature in degree celsius
                            Or
                            None
        """

        return self.lowest_temperature

    def get_max_humidity(self):
        """
        Returns the max_humidity, can be None
        Returns:
            (int or None):  max_humidity in percentage
                            Or
                            None
        """

        return self.max_humidity

    def get_mean_humidity(self):
        """
        Returns the mean_humidity, can be None
        Returns:
            (int or None):  mean_humidity in percentage
                            Or
                            None
        """

        return self.mean_humidity

    def get_date(self):
        """
        Returns the date
        Returns:
            (str): Value containing date in yyyy-mm-dd format e.g '2005-6-2'
        """

        return self.date


class MonthData:
    """
    This class holds the data of an entire month
    """

    def __init__(self, year, month, path=WEATHER_FILES_DIR):
        """
        Initializes the members name, year and path and
        calls populate to fill days_data list
        Args:
            year(str or int):   Value containing 4 digit year e.g '2004'
            month(str): Value containing 3 character month name e.g 'Feb', 'Mar'
            path(str):  Value containing path to weather files e.g 'weatherfiles/'
        """
        self.days_data = []
        self.name = month
        self.year = year
        self.path = path
        self.populate()

    def populate(self):
        """
        Initializes the days_data list with DayData objects for each day of the month
        Returns:
            None
        """

        month_data = next(read_data(f"{self.year}_{self.name[0:3]}", self.path))
        for line in month_data:
            day_data = DayData(parse_line(line))
            self.days_data.append(day_data)

    def get_max_extremes_with_date(self):
        """
        Returns the max highest temperature, min lowest temperature and max humidity
        for the whole month with respective dates
        Returns:
            (list or None): list containing 3 elements
                            [
                                [max_temperature(int), date(str)],
                                [min_temperature(int), date(str)],
                                [max_humidity(int), date(str)],
                            ]
                            Or
                            None if no data exists for the month
        """
        max_temperature = {"value": -1000, "date": ""}
        min_temperature = {"value": 1000, "date": ""}
        max_humidity = {"value": -1000, "date": ""}
        for day_data in self.days_data:
            date = day_data.get_date()

            max_arg2 = {"value": day_data.get_max_temperature(), "date": date}
            max_temperature = max(
                max_temperature, max_arg2, key=lambda x: x["value"] or -1000
            )

            min_arg2 = {"value": day_data.get_min_temperature(), "date": date}
            min_temperature = min(
                min_temperature, min_arg2, key=lambda x: x["value"] or 1000
            )

            max_arg2 = {"value": day_data.get_max_humidity(), "date": date}
            max_humidity = max(
                max_humidity, max_arg2, key=lambda x: x["value"] or -1000
            )
        return [
            max_temperature,
            min_temperature,
            max_humidity,
        ]

    def get_averages(self):
        """
        Returns the averages highest_temperature, lowest_temperature and mean_humidity
        Returns:
            (list or None): list containing rounded averages
                            [
                                avg_highest_temperature(str),
                                avg_lowest_temperature(str),
                                avg_mean_humidity(str)
                            ]
                            Or
                            None if no data exists for the month
        """
        if not self.days_data:
            return None
        sum_highest_temperature = 0
        sum_lowest_temperature = 0
        sum_mean_humidity = 0
        for day_data in self.days_data:
            sum_highest_temperature += day_data.get_max_temperature() or 0

            sum_lowest_temperature += day_data.get_min_temperature() or 0

            sum_mean_humidity += day_data.get_mean_humidity() or 0

        return [
            f"{round(sum_highest_temperature / len(self.days_data))}{TEMPERATURE_UNIT}",
            f"{round(sum_lowest_temperature / len(self.days_data))}{TEMPERATURE_UNIT}",
            f"{round(sum_mean_humidity / len(self.days_data))}{HUMIDITY_UNIT}",
        ]

    def get_month_values(self):
        """
        Returns date, highest temperature, lowest temperature and max humidity for each day
        Returns:
            (list or None): list containing year, month, day, max_temperature and min_temperature
                            for each day of the month
                            month_data[i] = [
                                year(str),
                                name(str),
                                day(str),
                                max_temperature_with_unit(str),
                                min_temperature_with_unit(str)
                            ]
        """

        if not self.days_data:
            return None
        month_data = []
        for day_data in self.days_data:
            month_data.append(
                [
                    self.year,
                    self.name,
                    day_data.get_date().split("-")[2],
                    day_data.get_max_temperature(),
                    day_data.get_min_temperature(),
                ]
            )

        return month_data

    def generate_averages_report_month(self):
        """
        Generates report using the averages list and displays
        1. average highest temperature
        2. average lowest temperature
        3. average mean humidity
        for a month
        Returns:
            None
        """
        averages = self.get_averages()
        starting_message = ["Highest", "Lowest", "Mean Humidity"]
        for index, val in enumerate(starting_message):
            print(f"Average {val}: {averages[index]}")

    def generate_report_charts(self):
        """
        This function displays month's report on console
        A report looks like
        "Month Year"
        "day1 lowest_temp ++++++++++++++ highest_temp"
        "day2 lowest_temp ++++++++++++++ highest_temp"
        .
        .
        .
        "day30 lowest_temp ++++++++++++++ highest_temp"
        Returns:
            None
        """
        extremes = self.get_month_values()
        year, month = extremes[0][0:2]
        print(f"{month} {year}")
        for entry in extremes:
            day = f"\33[0m{entry[2]}"
            if entry[3] is None or entry[4] is None:
                continue
            red_plus = f"\33[91m{'+' * entry[3]}"
            blue_plus = f"\33[94m{'+' * entry[4]}"
            report_line = (
                f"{day} {blue_plus}{red_plus} "
                f"\33[0m{entry[4]}{TEMPERATURE_UNIT}-{entry[3]}{TEMPERATURE_UNIT}"
            )
            print(report_line)


class YearData:
    """
    This class holds data of an entire year
    """

    def __init__(self, year, path=WEATHER_FILES_DIR):
        """
        Initializes the members year, path and calls populate to fill months_data list
        Args:
            year(str or int):   Value containing 4 digit year e.g '2004'
            path(str):  Value containing path to weather files e.g 'weatherfiles/'
        """
        self.months_data = []
        self.year = year
        self.path = path
        self.populate()

    def populate(self):
        """
        Initializes the months_data member with MonthData objects
        Returns:
            None
        """
        for month in range(1, 13):
            month_data = MonthData(self.year, get_month_name(month)[0:3], self.path)
            self.months_data.append(month_data)

    def get_max_extremes_with_date(self):
        """
        Returns maximum Highest temperature, minimum lowest temperature and
        maximum max humidity for the whole year with relevant dates
        Args:
        Returns:
            (list or None): list containing max extremes with dates
                            [
                                [max_temperature(int), date(str)],
                                [min_temperature(int), date(str)],
                                [max_humidity(int), date(str)]
                            ]
                            Or
                            None if there is no data for the year
        """

        if not self.months_data:
            return None
        max_temperature = {"value": -1000, "date": ""}
        min_temperature = {"value": 1000, "date": ""}
        max_humidity = {"value": -1000, "date": ""}
        for month_data in self.months_data:
            month_max_extremes = month_data.get_max_extremes_with_date()

            max_temperature = max(
                max_temperature,
                month_max_extremes[0],
                key=lambda x: x["value"] or -1000,
            )

            min_temperature = min(
                min_temperature, month_max_extremes[1], key=lambda x: x["value"] or 1000
            )

            max_humidity = max(
                max_humidity, month_max_extremes[2], key=lambda x: x["value"] or -1000
            )
        max_temperature["value"] = f"{max_temperature['value']}{TEMPERATURE_UNIT}"
        min_temperature["value"] = f"{min_temperature['value']}{TEMPERATURE_UNIT}"
        max_humidity["value"] = f"{max_humidity['value']}{HUMIDITY_UNIT}"
        return [max_temperature, min_temperature, max_humidity]

    def generate_extremes_report(self):
        """
        This function prints/generates a report on the console based on the maximums list
        the report displays the following
        1. max_highest_temperature with date
        2. max_lowest_temperature with date
        3. max_humidity with date
        Returns:
            None
        """
        maximums = self.get_max_extremes_with_date()
        starting_message = ["Highest", "Lowest", "Humidity"]
        for index, dictionary in enumerate(maximums):
            month, day = dictionary["date"].split("-")[1:]
            print(
                f"{starting_message[index]}: {dictionary['value']} on "
                f"{get_month_name(int(month))}, {day}"
            )
