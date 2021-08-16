"""
this module generates a report which displays average highest and lowest temperature
as well as average max humidity for a given month
"""
import glob


def read_and_calculate_averages(pattern, path):
    """
    this function reads all the files at the given path which contain the given pattern
    from each file that matches the pattern finds the following:
    1. avg highest temperature
    2. avg lowest temperature
    3. avg mean humidity
    :param pattern: a string which contains a year/month e.g '2006/5', '2007/3'
    :param path: a string which contains path to a directory containing weather files
    :return: a list of length 3, averages where
    averages[0] = avg_highest_temperature
    averages[1] = avg_lowest_temperature
    averages[2] = avg_mean_humidity
    """
    files = glob.glob(path + f"*{pattern}*.txt")
    if not files:
        print(f"We don't have information" f" regarding {pattern}")
        return -1
    # entries of the month
    entries = 0
    # contains the sum of all entries or highest, lowest temperature and  mean humidity
    # sums[0] = sum of highest temperatures
    # sums[1] = sum of lowest temperatures
    # sums[2] = sum of mean humidity
    sums = [0, 0, 0]
    # indexes to sum values with.
    # highest temperature is stored at index 1 of weather reading
    # lowest temperature is stored at index 3 of weather reading
    # max humidity is stored at index 7 of weather reading
    # see the weather files for further explanation
    indexes = [1, 3, 8]
    for i in files:
        with open(i, "r") as file:
            # ignore first line
            file.readline()
            for j in file:
                parsed_line = j.split("\n")[0].split(",")
                entries += 1
                for k, val in enumerate(indexes):
                    if parsed_line[val] == "":
                        continue
                    sums[k] += int(parsed_line[val])

    return [i / entries for i in sums]


def generate_averages_report_month(averages):
    """
    generates report using the averages list and displays
    1. average highest temperature
    2. average lowest temperature
    3. average mean humidity
    :param averages: a list of length 3, averages where
        averages[0] = avg_highest_temperature
        averages[1] = avg_lowest_temperature
        averages[2] = avg_mean_humidity
    :return: nothing
    """
    value = ["Highest", "Lowest", "Mean Humidity"]
    units = ["C", "C", "%"]
    for i, val in enumerate(value):
        print(f"Average {val}: {averages[i]}{units[i]}")


def get_averages_month(month, path):
    """
    this function uses 2 methods to calculate and display on console
    the average highest and lowest temperatures and average mean humidity
    for a given month in given path
    :param month: a string which contains year/month like: '2006/6', '2007/3' , etc
    :param path: a string which contains path to weather files like: 'path/'
    :return: nothing
    """
    number_to_month = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    month = number_to_month[int(month.split("/")[1]) - 1]
    averages = read_and_calculate_averages(month, path)
    if averages == -1:
        return -1
    generate_averages_report_month(averages)
    return 0
