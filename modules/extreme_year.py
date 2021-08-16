"""
this module will return the highest and lowest temperatures of a
given year along with the most humid day.
"""
import glob


def read_and_calculate_extremes(pattern, path):
    """
    this function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. max highest temperature
    2. max lowest temperature
    3. max humidity
    :param pattern: a string which contains a year e.g '2006', '2007'
    :param path: a string which contains path to a directory containing weather files
    :return: a 3x2 list maximums where
    maximums[0] = [max_highest_temperature, date]
    maximums[1] = [max_lowest_temperature, date]
    maximums[2] = [max_humidity, date]
    date here is a string like: '2002-4-1', '2004-3-14'
    """
    files = glob.glob(path + F'*{pattern}*')
    if not files:
        print(F"We don't have information regarding the "
              F"year {pattern} in the given path")
        return -1
    # maximums[0] contains highest temperature and day
    # maximums[1] contains lowest temperature and day
    # maximums[2] contains most humidity and day
    maximums = [[0, ''], [0, ''], [0, '']]
    initialized = False
    # indexes to compare values with.
    # highest temperature is stored at index 1 of weather reading
    # lowest temperature is stored at index 3 of weather reading
    # max humidity is stored at index 7 of weather reading
    # see the weather files for further explanation
    indexes = [1, 3, 7]
    for i in files:
        with open(i, 'r') as file:
            lines = file.readlines()
            # skip first line as it contains field names
            for line in lines[1:]:
                # since readline() returns 'linedata\n' with split by '\n' to get ['linedata','\n]
                # then we get 'linedata' by grabbing the [0]
                # lastly,  we split by ',' to get the entries parsed
                parsed_line = line.split('\n')[0].split(',')
                if not initialized:
                    for j, val in enumerate(indexes):
                        maximums[j] = [int(parsed_line[val]), parsed_line[0]]
                    initialized = True
                    continue
                for j, val in enumerate(indexes):
                    # index of weather record to compare value of current maximum with
                    index_to_compare = val
                    # value of temperatures or humidity or none
                    value = parsed_line[index_to_compare]
                    if value == '':
                        continue
                    value = int(value)
                    if j != 1 and value >= maximums[j][0]:
                        maximums[j] = [value, parsed_line[0]]
                    elif value <= maximums[j][0]:
                        maximums[j] = [value, parsed_line[0]]

    return maximums


def generate_extremes_report(maximums):
    """
    this functions prints/generates a report on the console based on the maximums array
    the reports displays the following
    1. max_highest_temperature with day
    2. max_lowest_temperature with day
    3. max_humidity with day
    :param maximums:
    :return: nothing
    """
    number_to_month = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]
    initial_message = ['Highest', 'Lowest', 'Humidity']
    unit = ['C', 'C', '%']
    for i, val in enumerate(maximums):
        month, day = maximums[i][1].split('-')[1:]
        print(f'{initial_message[i]}: {str(val[0])}{unit[i]} '
              f'on {number_to_month[int(month) - 1]} {day}')


def extreme_temperatures_year(year, path):
    """
    this method uses two other methods to calculate max extreme temperatures and max humidity
    for a given year
    :param year: a string like: '2002', '2004', etc
    :param path: a string like: 'weatherfiles/'
    :return: nothing
    """
    maximums = read_and_calculate_extremes(year, path)
    if maximums == -1:
        return -1
    generate_extremes_report(maximums)
    return 0
