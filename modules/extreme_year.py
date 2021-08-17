"""
this module will return the highest and lowest temperatures of a
given year along with the most humid day.
"""
import glob


def read_year_data(year, path):
    """
    this function reads data from the files of a particular year
    :param year:
    :param path:
    :returns: generator object containing row of a file
    """
    files = glob.glob(path + f"*{year}*")
    if not files:
        print(
            f"We don't have information regarding the "
            f"year {year} in the given path"
        )
        return -1
    for i in files:
        with open(i, "r") as file:
            # skip first line as it contains field names
            file.readline()
            for j in file:
                yield j


def calculate_extremes(year, path):
    """
    this function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. max highest temperature
    2. max lowest temperature
    3. max humidity
    :param year: a string which contains a year e.g '2006', '2007'
    :param path: a string which contains path to a directory containing weather files
    :returns: a 3x2 list maximums where
    maximums[0] = [max_highest_temperature, date]
    maximums[1] = [max_lowest_temperature, date]
    maximums[2] = [max_humidity, date]
    date here is a string like: '2002-4-1', '2004-3-14'
    """
    # max_temperature contains highest temperature and
    # date on which the temperature was highest
    # min_temperature contains lowest temperature and date
    # max_humidity contains most humidity and date
    max_temperature = [0, ""]
    min_temperature = [0, ""]
    max_humidity = [0, ""]
    initialized = False
    # indexes to compare values with.
    # highest temperature is stored at index 1 of weather reading
    # lowest temperature is stored at index 3 of weather reading
    # max humidity is stored at index 7 of weather reading
    # see the weather files for further explanation
    indexes = [1, 3, 7]
    for line in read_year_data(year, path):
        # since readline() returns 'linedata\n' with split by '\n' to get ['linedata','\n]
        # then we get 'linedata' by grabbing the [0]
        # lastly,  we split by ',' to get the entries parsed
        parsed_line = line.split("\n")[0].split(",")
        date = parsed_line[0]
        if not initialized:
            max_temperature = [int(parsed_line[indexes[0]]), date]
            min_temperature = [int(parsed_line[indexes[1]]), date]
            max_humidity = [int(parsed_line[indexes[2]]), date]
            initialized = True
            continue

        if parsed_line[indexes[0]] != '':
            max_temperature_line = int(parsed_line[indexes[0]])
            if max_temperature_line >= max_temperature[0]:
                max_temperature = [max_temperature_line, date]

        if parsed_line[indexes[1]] != '':
            min_temperature_line = int(parsed_line[indexes[1]])
            if min_temperature_line <= min_temperature[0]:
                min_temperature = [min_temperature_line, date]

        if parsed_line[indexes[2]] != '':
            max_humidity_line = int(parsed_line[indexes[2]])
            if max_humidity_line >= max_humidity[0]:
                max_temperature = [max_humidity_line, date]

    return [max_temperature, min_temperature, max_humidity] if initialized else -1


def generate_extremes_report(maximums):
    """
    this functions prints/generates a report on the console based on the maximums array
    the reports displays the following
    1. max_highest_temperature with day
    2. max_lowest_temperature with day
    3. max_humidity with day
    :param maximums:
    :returns: None
    """
    number_to_month = [
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
    message_unit = [("Highest", "C"), ("Lowest", "C"), ("Humidity", "%")]
    for i, val in enumerate(maximums):
        month, day = maximums[i][1].split("-")[1:]
        print(
            f"{message_unit[i][0]}: {str(val[0])}{message_unit[i][1]} "
            f"on {number_to_month[int(month) - 1]} {day}"
        )


def extreme_temperatures_year(year, path):
    """
    this method uses two other methods to calculate max extreme temperatures and max humidity
    for a given year
    :param year: a string like: '2002', '2004', etc
    :param path: a string like: 'weatherfiles/'
    :returns: int 0 for success -1 for error
    """
    maximums = calculate_extremes(year, path)
    if maximums == -1:
        return -1
    generate_extremes_report(maximums)
    return 0
