from datetime import datetime, date
from statistics import median
import pymysql

months31 = (1, 3, 5, 7, 8, 10, 12)
months30 = (4, 6, 9, 11)


def next_day(my_date):
    my_year = my_date.year
    my_month = my_date.month
    my_day = my_date.day
    # Define how many days in the month
    nb_days = 0
    if my_month == 2:
        bsx_modulo = my_year % 4
        nb_days = 29 if bsx_modulo == 0 else 28
    else:
        for month in months30:
            if month == my_month:
                nb_days = 30
                break
        if nb_days == 0:
            nb_days = 31
    # Increase date by 1
    if my_day < nb_days:
        my_day += 1
    else:
        if my_month == 12:
            my_year += 1
            my_month = 1
            my_day = 1
        else:
            my_month += 1
            my_day = 1
    # Return our new date
    new_date = date(my_year, my_month, my_day)
    return new_date


def count_day_rows(my_date):
    # Open database connection
    db = pymysql.connect("localhost", "admin", "admin", "smartwifi")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM csv_data WHERE time REGEXP \'" + str(my_date) + " *\'")
    rows = [my_date, cursor.fetchone()[0]]
    db.close()
    return rows


def count_days_rows(date_min, date_max):
    days_rows = []
    date_max = next_day(date_max)
    while date_min < date_max:
        days_rows.append(count_day_rows(date_min))
        date_min = next_day(date_min)
    return days_rows


def average_log_rows(days_rows):
    all_rows = 0
    for day_rows in days_rows:
        all_rows += day_rows[1]
    # Averaging
    rows_average = all_rows / len(days_rows)
    return int(rows_average)


def median_log_rows(days_rows):
    rows_array = []
    for day_rows in days_rows:
        rows_array.append(day_rows[1])
    # Median calculation
    rows_median = median(rows_array)
    return rows_median


#print(count_day_rows(date(2018, 3, 7)))
#print(date(2018, 3, 7))
#print(next_day(date(2021, 2, 28)))

test_days_rows = count_days_rows(date(2018, 3, 7), date(2018, 3, 15))
print(test_days_rows)
average = average_log_rows(test_days_rows)
print("Moyenne : " + str(average))
median = median_log_rows(test_days_rows)
print("Médiane : " + str(median))
