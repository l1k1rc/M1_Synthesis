from datetime import datetime, date
from statistics import median
import matplotlib.pyplot as plt
from minisom import MiniSom
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


def count_rows_between_hours(date_min, date_max):
    # Open database connection
    db = pymysql.connect("localhost", "admin", "admin", "smartwifi")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM csv_data WHERE time >= \'" + str(date_min) + "\' AND time <= \'" + str(date_max) + "\'")
    return cursor.fetchone()[0]

def list_clients_between_dates(date_min, date_max):
    clients = []
    # Open database connection
    db = pymysql.connect("localhost", "admin", "admin", "smartwifi")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT * FROM csv_data WHERE time >= \'" + str(date_min) + "\' AND time <= \'" + str(date_max) + "\'")
    return cursor.fetchall()


def sort_list(log_list, column):
    clients_array = [[]]
    current_date = log_list[0][0]
    clients_array_cursor = 0
    for client in log_list:
        if client[0] == current_date:
            clients_array[clients_array_cursor].append(client)
        else:
            current_date = client[0]
            clients_array_cursor += 1
            clients_array.append([client])

    return clients_array


def average_log_rows(days_rows):
    all_rows = 0
    for day_rows in days_rows:
        all_rows += day_rows[1]
    # Averaging
    rows_average = all_rows / len(days_rows)
    return int(rows_average)


def average_clients(client_list):
    all_clients = 0
    for clients in client_list:
        all_clients += len(clients)
    client_average = all_clients / len(client_list)
    return int(client_average)


def median_log_rows(days_rows):
    rows_array = []
    for day_rows in days_rows:
        rows_array.append(day_rows[1])
    # Median calculation
    rows_median = median(rows_array)
    return rows_median


def median_clients(client_list):
    all_clients = []
    for clients in client_list:
        all_clients.append(len(clients))
    client_median = median(all_clients)
    return int(client_median)


def plt_data(array_data, scale):
    time_array = []
    nbr_array = []
    for data in array_data:
        # TODO: dynamique
        time_array.append(data[0][0])
        #time_array.append(str(data[0][0]))
        nbr_array.append(len(data))
    plt.plot(time_array, nbr_array)
    plt.xlabel("Time")
    plt.ylabel("Clients")
    plt.title("Clients between " + str(array_data[0][0][0]) + " and " + str(array_data[len(array_data)-1][0][0]))
    plt.show()

#print(count_day_rows(date(2018, 3, 7)))
#print(date(2018, 3, 7))
#print(next_day(date(2021, 2, 28)))

#test_days_rows = count_days_rows(date(2018, 3, 7), date(2018, 3, 15))
#print(test_days_rows)
#average = average_log_rows(test_days_rows)
#print("Moyenne : " + str(average))
#median = median_log_rows(test_days_rows)
#print("Médiane : " + str(median))

#print(count_rows_between_hours(datetime(2018, 3, 7, 17), datetime(2018, 3, 7, 17, 9)))

#list_clients_between_dates(datetime(2018, 3, 7, 17), datetime(2018, 3, 7, 17, 8))

#test_array = sort_list(list_clients_between_dates(datetime(2018, 3, 7, 17), datetime(2018, 3, 7, 17, 10)), 0)
#print(len(test_array))
#print(test_array[0][0][0].minute)
#print(len(test_array[1]))
#print(len(test_array[2]))


#TESTS rapport
print("Analyse statistique :")
list = list_clients_between_dates(datetime(2018, 4, 4, 8), datetime(2018, 4, 4, 17))
sorted_list = sort_list(list, "minutes")
plt_data(sorted_list, "minutes")
print("Moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(average_clients(sorted_list)))
print("Médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(median_clients(sorted_list)))

list = list_clients_between_dates(datetime(2018, 4, 11, 8), datetime(2018, 4, 11, 17))
sorted_list = sort_list(list, "minutes")
plt_data(sorted_list, "minutes")
print("Moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(average_clients(sorted_list)))
print("Médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(median_clients(sorted_list)))

list = list_clients_between_dates(datetime(2018, 4, 18, 8), datetime(2018, 4, 18, 17))
sorted_list = sort_list(list, "minutes")
plt_data(sorted_list, "minutes")
print("Moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(average_clients(sorted_list)))
print("Médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(median_clients(sorted_list)))

list = list_clients_between_dates(datetime(2018, 4, 25, 8), datetime(2018, 4, 25, 17))
sorted_list = sort_list(list, "minutes")
plt_data(sorted_list, "minutes")
print("Moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(average_clients(sorted_list)))
print("Médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(median_clients(sorted_list)))

print("___________________________________________________________")
print("Estimation pout le 5ème jour :")
moy = (12 + 11 + 9 + 8)/4
med = median([14, 11, 9, 8])
list = list_clients_between_dates(datetime(2018, 5, 2, 8), datetime(2018, 5, 2, 17))
sorted_list = sort_list(list, "minutes")
plt_data(sorted_list, "minutes")
print("Estimation de moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(moy))
print("Estimation de médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(med))

print("___________________________________________________________")
print("Réalité :")
print("Moyenne des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(average_clients(sorted_list)))
print("Médiane des clients du " + str(sorted_list[0][0][0]) + " au " + str(sorted_list[len(sorted_list)-1][0][0]) + " : " + str(median_clients(sorted_list)))


