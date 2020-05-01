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


def convertToSQL(list, csv_file):
    # Open database connection
    db = pymysql.connect("localhost", "l1k1", "raccoon", "projetM1")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    print(("LOAD DATA LOCAL INFILE '" + str(csv_file) + "' INTO TABLE csv_data " +
                   "FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\n'" +
                   " ("+str(list[0])+","+str(list[1])+","+str(list[2])+")"))
    cursor.execute("LOAD DATA LOCAL INFILE '" + csv_file + "' INTO TABLE csv_data " +
                   "FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\n'" +
                   " ("+list[0]+","+list[1]+","+list[2]+")")
    db.close()

    LOAD DATA INFILE '/tmp/db.txt'
       INTO TABLE test FIELDS TERMINATED BY ','
       OPTIONALLY ENCLOSED BY '"'
       IGNORE 1 LINES (id, mycol1, mycol2);
def createTable():
    # Open database connection
    db = pymysql.connect("localhost", "l1k1", "raccoon", "projetM1")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('DROP TABLE csv_data;')
    cursor.execute('CREATE TABLE csv_data (time DATETIME, mac_address VARCHAR(100), ssid_data VARCHAR(100));')

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
        print(any(col in s for s in csv_columns[0]))


def display_columnsCSV(file):
    csv_columns = []
    with open(file, newline='') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            csv_columns.append(row)
            break
    print(Style.BOLD + Style.OKBLUE + str(csv_columns[0]) + Style.ENDC)


Tk().withdraw()
filename = askopenfilename(title="Select CSV logs file :",
                           filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
columns = []
print("File choosen :\n"+filename)
display_columnsCSV(filename)
# 1 = datetime, 2 = MAC Address, 3 = SSID
print("Write the column name corresponding to the" + Style.BOLD + Style.OKGREEN + " datetime : " + Style.ENDC)
columns.append(input())
print("Write the column name corresponding to the" + Style.BOLD + Style.OKGREEN + " MAC address : " + Style.ENDC)
columns.append(input())
print("Write the column name corresponding to the" + Style.BOLD + Style.OKGREEN + " SSID : " + Style.ENDC)
columns.append(input())
isColumnsFromCSV(filename, columns)
createTable()
convertToSQL(columns,filename)