import csv
from tkinter.filedialog import askopenfilename, Tk

import pymysql


class Style:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def convertToSQL(str, csv_file, tableName):
    # Open database connection
    db = pymysql.connect("localhost", "l1k1", "raccoon", "projetM1")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute("LOAD DATA LOCAL INFILE '" + csv_file + "' INTO TABLE " + tableName + " " +
                   "FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\\n'" +
                   "(total_rev,monthly_rev,day_rev)")
    db.close()


def createTable(list, tableName):
    # Open database connection
    db = pymysql.connect("localhost", "l1k1", "raccoon", "projetM1")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('CREATE TABLE csv_data (' +
                   'time DATETIME,' +
                   'mac_address VARCHAR(100)' +
                   'vendor VARCHAR(100)' +
                   'ssid VARCHAR(100)')
    # Fetch a single row using fetchone() method.
    # data = cursor.fetchone()
    # print("Database version : %s " % data)
    db.close()


def isColumnsFromCSV(CSVfile, columns):
    print(columns)
    errorIndex = 0
    csv_columns = []
    with open('../data/wifi_data.csv', newline='') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            csv_columns.append(row)
            break
    for col in columns:
        print(any(ele in csv_columns[0] for ele in col))


test_string = "There are 2 apples for 4 persons"

# initializing test list
test_list = ['apples', 'oranges']

# printing original string
print("The original string : " + test_string)

# printing original list
print("The original list : " + str(test_list))

# using list comprehension
# checking if string contains list element
res = any(ele in test_string for ele in test_list)

Tk().withdraw()
filename = askopenfilename()
columns = []
print(filename)
print("Write the column name corresponding to the" + Style.BOLD + "datetime : " + Style.ENDC)
columns.append(input())
print("Write the column name corresponding to the" + Style.BOLD + "MAC address : " + Style.ENDC)
columns.append(input())
print("Write the column name corresponding to the" + Style.BOLD + "SSID : " + Style.ENDC)
columns.append(input())
isColumnsFromCSV('test', columns)
