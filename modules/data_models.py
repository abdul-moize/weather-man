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
            line(str): string containing raw line read of weather file
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
        parsed_line = parse_line(self.line)
        self.max_temperature = get_highest_temperature(parsed_line)
        self.min_temperature = get_lowest_temperature(parsed_line)
        self.max_humidity = get_max_humidity(parsed_line)
        self.mean_humidity = get_mean_humidity(parsed_line)
        self.date = get_date(parsed_line)


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
            month(int): Number containing value in range 1-12
            path(str):  Value containing path to weather files e.g 'weatherfiles/'
        """
        self.days_data = []
        self.month = month
        self.year = year
        self.path = path
        self.populate()

    def populate(self):
        """
        Initializes the days_data list with DayData objects for each day of the month
        Returns:
            None
        """
        pattern = f"{self.year}_{self.get_name('%b')}"
        month_data = next(read_data(pattern, self.path))
        for line in month_data:
            day_data = DayData(line)
            self.days_data.append(day_data)

    def get_name(self, flag="%B"):
        """
        Returns month name
        Args:
            flag(str):  '%B' for full name
                        '%b' for 3 letter name
        Returns:
            None
        """
        return get_month_name(self.month, flag)

    def get_max_month_humidity(self):
        """
        Returns the max humidity for the whole month with respective date
        Returns:
            (int or None):  max humidity of the month
                            Or
                            None if no data exists for the month
        """
        if len(self.days_data) == 0:
            return {"value": None}
        max_humidity = {"value": -1000, "date": ""}
        for day_data in self.days_data:
            max_arg2 = {"value": day_data.max_humidity, "date": day_data.date}
            max_humidity = max(
                max_humidity, max_arg2, key=lambda x: x["value"] or -1000
            )

        return max_humidity

    def get_max_month_temperature(self):
        """
        Returns the max highest temperature for the whole month with respective date
        Returns:
            (int or None):  max highest_temperature of the month
                            Or
                            None if no data exists for the month
        """
        if len(self.days_data) == 0:
            return {"value": None}
        max_temperature = {"value": -1000, "date": ""}
        for day_data in self.days_data:
            max_arg2 = {"value": day_data.max_temperature, "date": day_data.date}
            max_temperature = max(
                max_temperature, max_arg2, key=lambda x: x["value"] or -1000
            )

        return max_temperature

    def get_min_month_temperature(self):
        """
        Returns the min highest temperature for the whole month with respective date
        Returns:
            (int or None):  min highest_temperature of the month
                            Or
                            None if no data exists for the month
        """
        if len(self.days_data) == 0:
            return {"value": None}
        min_temperature = {"value": 1000, "date": ""}
        for day_data in self.days_data:
            min_arg2 = {"value": day_data.min_temperature, "date": day_data.date}
            min_temperature = min(
                min_temperature, min_arg2, key=lambda x: x["value"] or 1000
            )

        return min_temperature

    def get_max_month_temperature_avg(self):
        """
        Returns the average highest_temperature
        Returns:
            (list or None): avg_highest_temperature(str),
                            Or
                            None if no data exists for the month
        """
        if not self.days_data:
            return {"value": None}
        sum_highest_temperature = 0
        for day_data in self.days_data:
            sum_highest_temperature += day_data.max_temperature or 0
        return (
            f"{round(sum_highest_temperature / len(self.days_data))}"
            f"{TEMPERATURE_UNIT}"
        )

    def get_min_month_temperature_avg(self):
        """
        Returns the average lowest_temperature
        Returns:
            (str or None):  avg_lowest_temperature
                            Or
                            None if no data exists for the month
        """
        if not self.days_data:
            return None
        sum_lowest_temperature = 0
        for day_data in self.days_data:
            sum_lowest_temperature += day_data.min_temperature or 0
        return (
            f"{round(sum_lowest_temperature / len(self.days_data))}"
            f"{TEMPERATURE_UNIT}"
        )

    def get_max_month_humidity_avg(self):
        """
        Returns the average max humidity
        Returns:
            (str or None):  avg_max_humidity,
                            Or
                            None if no data exists for the month
        """
        if not self.days_data:
            return None
        sum_max_humidity = 0
        for day_data in self.days_data:
            sum_max_humidity += day_data.max_humidity or 0
        return f"{round(sum_max_humidity / len(self.days_data))}{TEMPERATURE_UNIT}"

    def get_month_max_temperatures(self):
        """
        Returns highest temperature of each day
        Returns:
            (list or None): list containing max_temperature
                            for each day of the month
                            month_data[i] = max_temperature_with_unit(str)
                            Or
                            None
        """

        if not self.days_data:
            return None
        month_data = []
        for day_data in self.days_data:
            month_data.append(day_data.max_temperature)

        return month_data

    def get_month_min_temperatures(self):
        """
        Returns lowest temperature of each day
        Returns:
            (list or None): list containing min_temperature for each day of the month with units
                            month_data[i] = min_temperature_with_units(str)
                            Or
                            None
        """

        if not self.days_data:
            return None
        month_data = []
        for day_data in self.days_data:
            month_data.append(day_data.min_temperature)

        return month_data

    def get_month_dates(self):
        """
        Returns date of each day
        Returns:
            (list or None): list containing date each day of the month
                            month_data[i] = date(date)
                            Or
                            None
        """

        if not self.days_data:
            return None
        month_data = []
        for day_data in self.days_data:
            month_data.append(day_data.date)

        return month_data


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
            month_data = MonthData(self.year, month, self.path)
            self.months_data.append(month_data)

    def get_max_year_temperature(self):
        """
        Returns maximum Highest temperature, for the whole year with relevant date
        Args:
        Returns:
            (dict or None): dictionary containing max temperature and date
                            max_humidity = {
                                        "value" = max_temperature_with_unit(str),
                                        "date" = date(date)
                                    }
                            Or
                            None if there is no data for the year
        """

        if not self.months_data:
            return None
        max_temperature = {"value": -1000, "date": ""}
        for month_data in self.months_data:
            month_max_temperature = month_data.get_max_month_temperature()

            max_temperature = max(
                max_temperature,
                month_max_temperature,
                key=lambda x: x["value"] or -1000,
            )

        max_temperature["value"] = f"{max_temperature['value']}{TEMPERATURE_UNIT}"
        return max_temperature

    def get_min_year_temperature(self):
        """
        Returns minimum lowest temperature for the whole year with relevant date
        Args:
        Returns:
            (dict or None): dictionary containing min temperature and date
                            max_humidity = {
                                        "value" = min_temperature_with_unit(str),
                                        "date" = date(date)
                                    }
                            Or
                            None if there is no data for the year
        """

        if not self.months_data:
            return None
        min_temperature = {"value": 1000, "date": ""}
        for month_data in self.months_data:
            month_min_temperature = month_data.get_min_month_temperature()
            min_temperature = min(
                min_temperature, month_min_temperature, key=lambda x: x["value"] or 1000
            )

        min_temperature["value"] = f"{min_temperature['value']}{TEMPERATURE_UNIT}"
        return min_temperature

    def get_max_year_humidity(self):
        """
        Returns maximum max humidity for the whole year with relevant date
        Args:
        Returns:
            (dict or None): dictionary containing max humidity and date
                            max_humidity = {
                                        "value" = max_humidity_with_unit(str),
                                        "date" = date(date)
                                    }
                            Or
                            None if there is no data for the year
        """

        if not self.months_data:
            return None
        max_humidity = {"value": -1000, "date": ""}
        for month_data in self.months_data:
            max_month_humidity = month_data.get_max_month_humidity()
            max_humidity = max(
                max_humidity, max_month_humidity, key=lambda x: x["value"] or -1000
            )
        max_humidity["value"] = f"{max_humidity['value']}{HUMIDITY_UNIT}"
        return max_humidity


class ReportGenerator:
    """
    Contains static functions which generate reports
    """

    def __init__(self, month_data=None, year_data=None):
        self.month_object = month_data
        self.year_object = year_data

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
        avg_max_temperature = self.month_object.get_max_month_temperature_avg()
        avg_min_temperature = self.month_object.get_min_month_temperature_avg()
        avg_max_humidity = self.month_object.get_max_month_humidity_avg()
        averages = [avg_max_temperature, avg_min_temperature, avg_max_humidity]
        starting_message = ["Highest", "Lowest", "Mean Humidity"]
        for index, val in enumerate(starting_message):
            print(f"Average {val}: {averages[index]}")

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
        max_temperature = self.year_object.get_max_year_temperature()
        min_temperature = self.year_object.get_min_year_temperature()
        max_humidity = self.year_object.get_max_year_humidity()
        maximums = [max_temperature, min_temperature, max_humidity]
        starting_message = ["Highest", "Lowest", "Humidity"]
        for index, dictionary in enumerate(maximums):
            print(
                f"{starting_message[index]}: {dictionary['value']} on "
                f"{dictionary['date'].strftime('%B')}, {dictionary['date'].day}"
            )

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
        max_temperatures = self.month_object.get_month_max_temperatures()
        min_temperatures = self.month_object.get_month_min_temperatures()
        dates = self.month_object.get_month_dates()
        extremes = [
            [i, j, k] for i, j, k in zip(dates, max_temperatures, min_temperatures)
        ]
        year, month = dates[0].year, self.month_object.get_name()
        print(f"{month} {year}")
        for entry in extremes:
            day = f"\33[0m{entry[0].day}"
            if entry[2] is None or entry[1] is None:
                continue
            red_plus = f"\33[91m{'+' * entry[1]}"
            blue_plus = f"\33[94m{'+' * entry[2]}"
            report_line = (
                f"{day} {blue_plus}{red_plus} "
                f"\33[0m{entry[2]}{TEMPERATURE_UNIT}-{entry[1]}{TEMPERATURE_UNIT}"
            )
            print(report_line)
