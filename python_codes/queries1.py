import psycopg2
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import matplotlib
import csv
# from pandas import DataFrame


connection = psycopg2.connect(user="root",
                              password="sumpr0ject",
                              host="localhost",
                              port="35432",
                              database="skoda-postgres")

daysNumber = 20

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):


    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False, labelsize=5.5)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:d}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


"""How many records is in database"""


def countRecords():
    cursor = connection.cursor()
    query = "select count(*) from carsharing"
    cursor.execute(query)
    num = cursor.fetchone()
    print("There are " + str(num[0]) + " records in database")

    return num[0]


"""How many cars is in database"""


def countCars():
    cursor = connection.cursor()
    query = "select count(distinct name) from carsharing"
    cursor.execute(query)
    num = cursor.fetchone()
    print("There are " + str(num[0]) + " cars in database")
    return num[0]


"""How many users is in database"""


def countUsers():
    cursor = connection.cursor()
    query = "select count(distinct userid) from carsharing"
    cursor.execute(query)
    num = cursor.fetchone()
    print("There are " + str(num[0]) + " users in database")
    return num[0]


"""How many locations are in database"""


def countLocations():
    cursor = connection.cursor()
    query = "select count(distinct departureparking), count(distinct arrivalparking) from carsharing"
    cursor.execute(query)
    num = cursor.fetchone()
    print("There are " + str(num[0]) + " departure locations and " + str(num[1]) + " arrival locations in database")
    return num[0]


"""Median number of rides per user"""


def medianRides():
    cursor = connection.cursor()
    rides = "select userid, count(userid) as cnt from carsharing group by userid order by cnt desc"
    cursor.execute(rides)
    query = cursor.fetchall()
    arr = []
    for row in query:
        arr.append(row[1])
    med = float(st.median(arr))
    print("Median number of rides per user is " + str(med))
    return med


"""Average number of rides per user"""


def avgRides():
    cursor = connection.cursor()
    totalRides = "select count(*) from carsharing"
    distinctUsers = "select count(distinct userid) from carsharing"
    cursor.execute(distinctUsers)
    users = cursor.fetchone()
    cursor.execute(totalRides)
    rides = cursor.fetchone()
    print("Average number of rides per user is: " + str(rides[0] / users[0]))

    return rides[0] / users[0]


"""Returns table with number of rides of each individual user in descending order"""


def individualsRides():
    cursor = connection.cursor()
    rides = "select userid, count(userid) as cnt from carsharing group by userid order by cnt desc"
    cursor.execute(rides)
    query = cursor.fetchall()
    return query


"""Creates histogram from table with usage of service by each user"""


def individualsRidesHist(query):
    x = np.array((), dtype=np.int64)
    up = 0
    for row in query:
        x = np.append(x, row[1])
        if up < row[1]:
            up = row[1]
    print(np.average(x))
    plt.hist(x, bins=up, color='xkcd:lightish blue', range=(1, up))
    plt.axvline(np.average(x), linewidth=0.75, color="xkcd:peach", linestyle= 'dashdot')
    plt.legend(['Average = 4.27'],loc=1)
    plt.axhline(10, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(20, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(30, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(40, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(50, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(60, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(70, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(80, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.ylabel('No of users')
    plt.xlabel('No of rides per user')
    plt.title('Number of usages per user during May')
    # plt.xticks(range(1, up))
    plt.savefig('outputs/users_histogram.png', dpi = 300)
    plt.show()


"""Returns number of rides from each parking spot in descending order"""


def spotsUsageFrom():
    cursor = connection.cursor()
    rides = "select departureparking, count(departureparking) as cnt from carsharing group by departureparking order by cnt desc"
    cursor.execute(rides)
    query = cursor.fetchall()

    return query


"""Returns number of rides to each parking spot in descending order"""


def spotsUsageTo():
    cursor = connection.cursor()
    rides = "select arrivalparking, count(arrivalparking) as cnt from carsharing group by arrivalparking order by cnt desc"
    cursor.execute(rides)
    query = cursor.fetchall()

    return query





"""Return table with car name and cardinality of rides in descending order"""


def carsUsage():
    cursor = connection.cursor()
    rides = "select name, count(name) as cnt from carsharing group by name order by cnt desc"
    cursor.execute(rides)
    query = cursor.fetchall()

    return query











"""Balance of individual destinations in every day of month May"""


def dailyBalance():  # Create heatmap
    cursor = connection.cursor()
    sel = "select distinct departureparking from carsharing"
    cursor.execute(sel)
    query = cursor.fetchall()
    balance = {}
    arrivals = {}
    departures = {}
    zeros = np.zeros(31, dtype=np.int64)
    locationsLst = []
    for row in query:
        balance[row[0]] = zeros.copy()
        arrivals[row[0]] = zeros.copy()
        departures[row[0]] = zeros.copy()
        locationsLst.append(row[0])

    rides = "select departureparking, arrivalparking, dateto, datefrom from carsharing"
    cursor.execute(rides)
    query = cursor.fetchall()
    for row in query:
        balance[row[0]][row[2].day - 1] -= 1
        balance[row[1]][row[3].day - 1] += 1
        departures[row[0]][row[2].day - 1] += 1
        arrivals[row[1]][row[3].day - 1] += 1

    createCSVfromDailyBal(balance, departures, arrivals)
    return balance, departures, arrivals

def createCSVfromDailyBal(balance, departures, arrivals):
    export = None
    for key in balance.keys():
        if export is None:
            export = np.array([balance[key]])
        else:
            export = np.append(export, [balance[key]], axis=0)
    np.savetxt('outputs/balance.csv', export, delimiter=',', fmt='%d')

    export = None
    for key in departures.keys():
        if export is None:
            export = np.array([departures[key]])
        else:
            export = np.append(export, [departures[key]], axis=0)
    np.savetxt('outputs/departures.csv', export, delimiter=',', fmt='%d')

    export = None
    for key in arrivals.keys():
        if export is None:
            export = np.array([arrivals[key]])
        else:
            export = np.append(export, [arrivals[key]], axis=0)
    np.savetxt('outputs/arrivals.csv', export, delimiter=',', fmt='%d')

"""Query used just for debugging purposes"""


def testQuery():
    cursor = connection.cursor()
    rides = "SELECT userid, dateto, datefrom FROM carsharing"
    cursor.execute(rides)
    query = cursor.fetchall()
    sum = 0.0
    for row in query:
        if row[1].day != row[2].day:
            print("different days")

    return sum





"""Creates bar with number of cars being used on Y-axis and daytime on X-axis."""


def usageDuringDayBar(array):
    indices = np.arange(len(array))
    plt.bar(indices, array, color='xkcd:peach', width=0.25)
    plt.axhline(5, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(10, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(15, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(20, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.xticks(indices, rotation='horizontal')
    plt.ylabel('No of reservations')
    plt.xlabel('Daytime')
    plt.title('Usage of cars during average day in May')
    plt.savefig('outputs/usage_during_day.png', dpi = 300)
    plt.show()


"""Returns usage in each day of month"""


def usageDuringMonth():
    cursor = connection.cursor()
    rides = "SELECT datefrom FROM carsharing"
    cursor.execute(rides)
    query = cursor.fetchall()
    month = np.zeros(31, dtype=np.int64)
    notValid = notValidDaysDic()
    for row in query:
        if not row[0].day in notValid:
            dep = row[0].day
            month[dep - 1] += 1

    return month


""""""


def usageDuringMonthBar(array):
    indices = np.arange(1, len(array) + 1)
    plt.bar(indices, array, color='xkcd:peach', width=0.25)
    plt.xticks(indices, rotation='vertical')
    plt.axhline(20, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(40, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(60, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(80, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(100, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.ylabel('No of reservations')
    plt.xlabel('May [day]')
    plt.title('Usage of cars during May')

    plt.savefig('outputs/usage_during_month.png', dpi = 300)
    plt.show()


def totalTime(): #FIX ME!
    cursor = connection.cursor()
    rides = "SELECT userid, dateto, datefrom FROM carsharing"
    cursor.execute(rides)
    query = cursor.fetchall()
    sum = 0.0
    for row in query:
        t1 = row[1].hour + row[1].minute / 60
        t2 = row[2].hour + row[2].minute / 60
        sum += (t1 - t2)

    return sum


"""How much time did each user spend in carsharing"""


def totalTimeUser():
    cursor = connection.cursor()
    rides = "SELECT userid, (sum(DATE_PART('days', dateto::timestamp - datefrom::timestamp)*24 + DATE_PART('hours', dateto::timestamp - datefrom::timestamp) + DATE_PART('minutes', dateto::timestamp - datefrom::timestamp)/60)::float) as sm FROM carsharing group by userid order by sm desc"
    cursor.execute(rides)
    query = cursor.fetchall()
    sum = 0.0
    for row in query:
        sum += row[1]
    print("Overall time in hours: " + str(sum))
    return query





"""Creates histogram of arrivals during the day in May"""


def arrivalHoursHist(hours):
    plt.hist(hours, color='xkcd:lightish blue')
    plt.ylabel('Frequency')  # Something should be done with y-axis
    plt.xlabel('Time of the day')
    plt.title('Frequency of arrivals during the day')
    plt.savefig('outputs/arrivals_time_histogram.png', dpi = 300)
    plt.xticks(range(0, 24))
    plt.show()

"""Creates histogram of departures during the day in May"""


def departureHoursHist(hours):
    plt.hist(hours, color='xkcd:lightish blue')
    plt.ylabel('Frequency')  # Something should be done with y-axis
    plt.xlabel('Time of the day')
    plt.title('Frequency of departures during the day')
    plt.savefig('outputs/departures_time_histogram.png', dpi = 300)
    plt.xticks(range(0, 24))
    plt.show()

"""Creates bar with usage of each parking spot"""


def spotsUsageBar(queryFrom, queryTo):
    word1 = []
    word2 = []
    frequency1 = []
    frequency2 = []
    leg = ['Departures', 'Arrivals']

    for i in range(len(queryFrom)):
        word1.append(queryFrom[i][0])
        frequency1.append(queryFrom[i][1])

    for i in range(len(queryTo)):
        word2.append(queryTo[i][0])
        frequency2.append(queryTo[i][1])

    indices1 = np.arange(len(queryFrom))
    indices2 = np.arange(len(queryTo))

    plt.bar(indices1, frequency1, color='xkcd:peach', width=0.25)
    plt.bar(indices2 + 0.25, frequency2, color='xkcd:lightish blue', width=0.25)
    plt.legend(leg, loc=1)
    plt.axhline(50, linewidth=0.3, color='xkcd:black', linestyle = 'dashed')
    plt.axhline(100, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(150, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(200, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.xticks(indices1, word1, rotation='vertical')


    plt.ylabel('No of departures/arrivals')
    plt.xlabel('Parking')
    plt.title('Usage of parking spots during May')

    plt.savefig('outputs/spots_usage.png', dpi = 300)
    plt.show()





def usageDuringWeekBar(array):
    indices = ['PO','ÚT','ST','ČT','PÁ']
    plt.bar(indices, array[:5], color='xkcd:peach', width=0.25)
    plt.xticks(indices, rotation='horizontal')
    plt.axhline(4, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(8, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(12, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(16, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(2, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(6, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(10, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(14, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.ylabel('No of reservations')
    plt.xlabel('Days')
    plt.title('Usage of cars during average week in May')

    plt.savefig('outputs/usage_during_week.png', dpi = 300)
    plt.show()



def cartesianQuery():
    cursor = connection.cursor()
    select = "SELECT arrivalparking, departureparking, count(*) as cnt FROM carsharing group by (departureparking, arrivalparking) order by cnt desc"

    cursor.execute(select)
    query = cursor.fetchall()
    spots = getSpotsDic()
    matrix = np.zeros(((21,21)), dtype=np.int64)
    total = 0.0
    same = 0.0

    with open('od.txt', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(query)
    f.close()
    for row in query:
        matrix[spots[row[0]]][spots[row[1]]] = row[2]


    for row in query:
        if row[0] == row[1]:
            same += row[2]

        total += row[2]
    perc = float(same/total)



    return matrix

def getSpotsDic():
    cursor = connection.cursor()
    select = "SELECT arrivalparking, count(*) as cnt FROM carsharing group by arrivalparking order by cnt desc"
    cursor.execute(select)
    query = cursor.fetchall()
    spots = {}
    i = 0
    for row in query:
        spots[row[0]] = i
        i += 1

    return spots

def validDays():
    cursor = connection.cursor()
    select = "select datefrom from carsharing"

    cursor.execute(select)
    query = cursor.fetchall()
    valid = 0
    days = np.zeros((31,),dtype=np.int64)
    for row in query:
        days[row[0].day-1] += 1
    for day in days:
        if day > 5:
            valid +=1
    days[days <= 5] = 0
    idx = np.where(days > 0)[0]
    idx += 1
    return idx



def getSpotsList():
    cursor = connection.cursor()
    select = "SELECT arrivalparking, count(*) as cnt FROM carsharing group by arrivalparking order by cnt desc"
    cursor.execute(select)
    query = cursor.fetchall()
    spots = []
    for row in query:
        spots.append(row[0])

    return spots

def createHeatmapWithSame():
    fig, ax = plt.subplots()
    spots = getSpotsList()

    im, cbar = heatmap(cartesianQuery(), spots, spots, ax=ax,
                       cmap="magma_r", cbarlabel="No of rides")
    texts = annotate_heatmap(im, valfmt="{x:d}", size=5)

    fig.tight_layout()
    plt.title('Origin-destination heatmap with same start and finish')
    plt.ylabel('Starting position',fontsize=9)
    plt.xlabel('Destination position',fontsize=9)
    ax.xaxis.set_label_position('top')

    plt.savefig('outputs/heatmap_with.png', dpi=300, bbox_inches = 'tight')
    plt.show()

def cartesianQueryNotSame():
    cursor = connection.cursor()
    select = "SELECT arrivalparking, departureparking, count(*) as cnt FROM carsharing group by (departureparking, arrivalparking) order by cnt desc"

    cursor.execute(select)
    query = cursor.fetchall()
    spots = getSpotsDic()
    matrix = np.zeros(((21,21)), dtype=np.int64)
    total = 0.0
    same = 0.0
    for row in query:
        if row[0] != row[1]:
            matrix[spots[row[0]]][spots[row[1]]] = row[2]

    return matrix

def createHeatmapWithoutSame():
    fig, ax = plt.subplots()
    spots = getSpotsList()

    im, cbar = heatmap(cartesianQueryNotSame(), spots, spots, ax=ax,
                       cmap="magma_r", cbarlabel="No of rides")
    texts = annotate_heatmap(im, valfmt="{x:d}", size=5)

    fig.tight_layout()
    plt.title('Origin-destination heatmap without same start and finish')
    plt.ylabel('Starting position',fontsize=9)
    plt.xlabel('Destination position',fontsize=9)
    ax.xaxis.set_label_position('top')

    plt.savefig('outputs/heatmap_without.png', dpi=300, bbox_inches = 'tight')
    plt.show()

def usageWeek():
    month = usageDuringMonth()
    week = np.zeros((7,), dtype=np.int64)

    start = 2
    notValid = notValidDaysDic()
    for i in range(len(month)):
        if not ((month[i]+1) in notValid):
            week[start] += month[i]
            start = (start+1)%7
            print("Validay is " + str(i) + " with usage " + str(month[i]))
        else:
            start = (start + 1) % 7
            print("Invaliday is " + str(i))

    #print(week/31)
    return week / daysNumber


"""Returns average day usage in array"""


def usageDuringDay():
    cursor = connection.cursor()
    rides = "SELECT datefrom, dateto FROM carsharing"
    cursor.execute(rides)
    query = cursor.fetchall()
    day = np.zeros(24, dtype=np.float)
    notValid = notValidDaysDic()
    for row in query:
        if not (row[0].day in notValid) or not (row[1].day in notValid):
            dep = row[0].hour
            arr = row[1].hour
            if (row[1].minute == 0):
                arr -= 1
            day[dep] += 1
            for i in range(arr - dep):
                day[dep + i + 1] += 1
        #else:
            #print("Day1 " + str(row[0].day))
            #print("Day2 " + str(row[1].day))
    return day / daysNumber

def notValidDaysDic():
    cursor = connection.cursor()
    select = "select datefrom from carsharing"

    cursor.execute(select)
    query = cursor.fetchall()
    valid = 0
    days = np.zeros((31,), dtype=np.int64)
    notValid = []
    for row in query:
        days[row[0].day - 1] += 1
    for i in range(days.shape[0]):
        #print(days[i])
        if days[i] > 5:
            valid += 1
        else:
            notValid.append(i+1)
    return notValid


def arrDepBar(dep, arr):
    arrHours = np.zeros((24,), dtype=np.int64)
    depHours = np.zeros((24,), dtype=np.int64)
    leg = ['Departures', 'Arrivals']

    for i in range(len(dep)):
        depHours[dep[i]] += 1

    for i in range(len(arr)):
        arrHours[arr[i]] += 1

    depHours = np.divide(depHours, daysNumber)
    arrHours = np.divide(arrHours, daysNumber)
    indices1 = np.arange(len(depHours))
    indices2 = np.arange(len(arrHours))
    plt.bar(indices1, depHours, color='xkcd:peach', width=0.25)
    plt.bar(indices2 + 0.25, arrHours, color='xkcd:lightish blue', width=0.25)
    plt.xticks(indices1, indices1, rotation='vertical')
    plt.ylabel('No of departures/arrivals')
    plt.xlabel('Daytime')
    plt.title('Arrivals and departures during day')
    plt.legend(leg)
    plt.axhline(2, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(4, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(6, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(8, linewidth=0.3, color='xkcd:black', linestyle='dashed')

    plt.savefig('outputs/dep_arr_usage.png', dpi = 300)
    plt.show()


"""Create array of frequencies of departures during day"""


def departureHours():
    cursor = connection.cursor()
    time = "SELECT datefrom FROM carsharing"
    cursor.execute(time)
    query = cursor.fetchall()
    # hours = np.zeros(24, dtype=np.int64)
    valid = validDays()
    hours = np.array((), dtype=np.int64)
    for row in query:
        if row[0].day in valid:
            hours = np.append(hours, row[0].hour)
        # hours[tmp] += 1
    ret = query[0][0].hour

    return hours


"""Create array of frequencies of arrivals during day"""


def arrivalHours():
    cursor = connection.cursor()
    time = "SELECT dateto FROM carsharing"
    cursor.execute(time)
    query = cursor.fetchall()
    # hours = np.zeros(24, dtype=np.int64)
    valid = validDays()
    hours = np.array((), dtype=np.int64)
    for row in query:
        if row[0].day in valid:
            hours = np.append(hours, row[0].hour)
        # hours[tmp] += 1
    ret = query[0][0].hour

    return hours



"""Histogram of vehicle usage"""


def carUsageHist(query):  # Number of cars that are being used for some time (1, 2, 3, 4, ... hours) CHECK ME!
    x = np.array((), dtype=np.int64)
    up = 0
    for row in query:
        x = np.append(x, row[1])
        if up < row[1]:
            up = row[1]
    print(x)
    plt.hist(x, color='xkcd:lightish blue')
    plt.ylabel('No of cars')
    plt.xlabel('Time used [hours]')
    plt.title('Total duration of usages for each car during May')
    mean = np.mean(x)
    avg = np.average(x)
    median = np.median(x)
    std = np.sqrt(np.var(x))
    plt.axvline(mean, color='xkcd:orange', linestyle='--', linewidth=2, label="Mean")
    plt.axvline(avg, color='xkcd:lime', linestyle='dotted', linewidth=2, label="Average")
    plt.axvline(std, color='k', linestyle='dashdot', linewidth=2, label="Variance")
    plt.axvline(median, color='xkcd:purple', linestyle='dotted', linewidth=2, label="Median")
    plt.axvline(2 * mean - std, color='k', linestyle='dashdot', linewidth=2)
    plt.legend()
    plt.savefig('outputs/cars_histogram.png', dpi = 300)
    plt.show()

"""Bar of vehicle usage"""


def carUsageBar():  # Number of cars that are being used for some time (1, 2, 3, 4, ... hours) CHECK ME!
    query, names = totalTimeCar()
    x = np.array((), dtype=np.int64)
    up = 0
    for row in query:
        x = np.append(x, row[1])
        if up < row[1]:
            up = row[1]
    print(x)

    plt.ylabel('Time used [hours]')
    plt.xlabel('Cars [one bar = one car]')
    plt.title('Duration of usages for each car during May')

    tmp = np.arange(start=1, stop=len(x) + 1, step=1)
    print(tmp)
    print(len(tmp))
    print(len(x))
    avg = np.average(x)
    median = np.median(x)
    std = np.sqrt(np.var(x))
    mean = np.mean(x)
    plt.axhline(20, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(40, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(60, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(80, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(100, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(mean, color='xkcd:orange', linestyle='--', linewidth=2, label="Mean")
    plt.axhline(avg, color='xkcd:lime', linestyle='dotted', linewidth=2, label="Average")
    plt.axhline(std, color='k', linestyle='dashdot', linewidth=2, label="Variance")
    plt.axhline(median, color='xkcd:purple', linestyle='dotted', linewidth=2, label="Median")
    plt.axhline(2 * mean - std, color='k', linestyle='dashdot', linewidth=2)

    plt.bar(tmp, x, color='xkcd:lightish blue', width=0.75, )
    frame = plt.gca()

    frame.axes.get_xaxis().set_ticks([])
    plt.legend()
    #plt.xticks(np.arange(min(tmp), max(tmp), 1.0), rotation = 270)
    plt.tight_layout()


    plt.savefig('outputs/cars_bar.png', dpi = 300)
    plt.show()


def carUsageBarAvg():  # Number of cars that are being used for some time (1, 2, 3, 4, ... hours) CHECK ME!
    query, names = totalTimeCar()
    x = np.array((), dtype=np.int64)
    up = 0
    for row in query:
        x = np.append(x, row[1])
        if up < row[1]:
            up = row[1]
    print(x)
    x /= daysNumber
    plt.ylabel('Time used [hours]')
    plt.xlabel('Cars [one bar = one car]')
    plt.title('Duration of usage for each car during average day')

    tmp = np.arange(start=1, stop=len(x) + 1, step=1)
    print(tmp)
    print(len(tmp))
    print(len(x))
    avg = np.average(x)
    median = np.median(x)
    std = np.sqrt(np.var(x))
    mean = np.mean(x)

    plt.axhline(1, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(2, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(3, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(4, linewidth=0.3, color='xkcd:black', linestyle='dashed')
    plt.axhline(5, linewidth=0.3, color='xkcd:black', linestyle='dashed')

    plt.axhline(mean, color='xkcd:orange', linestyle='--', linewidth=2, label="Mean")
    plt.axhline(avg, color='xkcd:lime', linestyle='dotted', linewidth=2, label="Average")
    plt.axhline(std, color='k', linestyle='dashdot', linewidth=2, label="Variance")
    plt.axhline(median, color='xkcd:purple', linestyle='dotted', linewidth=2, label="Median")
    plt.axhline(2 * mean - std, color='k', linestyle='dashdot', linewidth=2)

    plt.bar(tmp, x, color='xkcd:lightish blue', width=0.75, )
    plt.legend()
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    #plt.xticks(np.arange(min(tmp), max(tmp), 1.0), rotation = 270)
    plt.tight_layout()


    plt.savefig('outputs/cars_bar_avg.png', dpi = 300)
    plt.show()


"""Sum of time for which each vehicle was used"""


def totalTimeCar():
    cursor = connection.cursor()
    rides = "SELECT name, (sum(DATE_PART('days', dateto::timestamp - datefrom::timestamp)*24 + DATE_PART('hours', dateto::timestamp - datefrom::timestamp) + DATE_PART('minutes', dateto::timestamp - datefrom::timestamp)/60)::float) as sm FROM carsharing group by name order by sm desc"

    cursor.execute(rides)
    query = cursor.fetchall()
    sum = 0
    names = []
    for row in query:
        sum += row[1]
        names.append(row[0])



    return query, names






"""Main function used for debugging purposes uncomment line to see how functions works"""
if __name__ == "__main__":

    #usageDuringMonthBar(usageDuringMonth())
    #cartesianQuery()
    #createHeatmapWithSame()
    #createHeatmapWithoutSame()
    #usageDuringDayBar(usageDuringDay())
    #usageDuringWeekBar(usageWeek())
    #notValidDaysDic()
    #validDays()
    #arrDepBar(departureHours(), arrivalHours())
    #totalTimeCar()
    carUsageBar()
    #usageDuringMonthBar(usageDuringMonth())

    #########DONE
    #carUsageHist(totalTimeCar()[0])
    #print(validDays())
    """
    spotsUsageBar(spotsUsageFrom(), spotsUsageTo())
    carUsageHist(totalTimeCar())
    
    
    usageDuringWeekBar(usageWeek())
    usageDuringDayBar(usageDuringDay())
    individualsRidesHist(individualsRides())
    
    
    cartesianQuery()

    print(totalTime())
    totalTimeUser()
    dailyBalance()
    usageDuringWeekBar(usageWeek())



    arrDepBar(departureHours(),arrivalHours())
    arrivalHoursHist(arrivalHours()) # spojit s dep
    departureHoursHist(departureHours())

    dailyBalance()
    
    #testQuery()
    usageDuringMonthBar(usageDuringMonth())
    usageDuringDayBar(usageDuringDay())
    countRecords()
    countCars()
    countUsers()
    avgRides()
    medianRides()
    
    countLocations()
    spotsUsageFrom()
    spotsUsageTo()
    carsUsage()

    print(medianRides())"""
