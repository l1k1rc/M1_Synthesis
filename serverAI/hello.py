import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)

mydb = mysql.connector.connect(
    host="localhost",
    user="l1k1",
    passwd="raccoon",
    database="projetM1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT time, count(*) as NUM FROM csv_data GROUP BY time LIMIT 100")
result_set = mycursor.fetchall()
time = []
user = []
dt = []
for row in result_set:
    dt.append(row)
    # print("%s, %s" % (row[0], row[1]))
    # user.append(row[1])
    # time.append(row[0])




# register_matplotlib_converters()


def getData(filename):
    list_daf = []
    daf = pd.read_csv(filename, parse_dates=['0'], index_col=['0'])
    for val in daf['1']:
        list_daf.append(val)

    ts = list_daf

    print(ts)
    return ts


y = pd.DataFrame(getData("../data/log_lundi.csv"))
y2 = pd.DataFrame(getData("../data/log_lundi_bw.csv"))