#Name: Dennis Meltser
#Class: ISMG 6020-E02
#Date:10/15/2021

# Import statements for using SQLite, Numpy, Pandas, and Matplotlib
import sqlite3
import numpy as np
from numpy.lib.function_base import average
import pandas as pd
import matplotlib.pyplot as plt

#Create the connection to the database
conn = sqlite3.connect('index.sqlite')

#Extra: created the pandas dataframe with one read line
#Read the database query into a pandas dataframe
data = pd.read_sql_query("SELECT id, docks_in_service, available_bikes, percent_full, biketime FROM BikeStations", conn, index_col=['id'])

#Create filters for each bike station
idStation27 = data.filter(like='27', axis=0)
idStation28 = data.filter(like='28', axis=0)
idStation60 = data.filter(like='60', axis=0)
idStation224 = data.filter(like='224', axis=0)
idStation331 = data.filter(like='331', axis=0)

#create the necessary averages for each bikestation and their columns
avgBikes27 = idStation27['available_bikes'].mean()
avgDocks27 = idStation27['docks_in_service'].mean()
avgBikes28 = idStation28['available_bikes'].mean()
avgDocks28 = idStation28['docks_in_service'].mean()
avgBikes60 = idStation60['available_bikes'].mean()
avgDocks60 = idStation60['docks_in_service'].mean()
avgBikes224 = idStation224['available_bikes'].mean()
avgDocks224 = idStation224['docks_in_service'].mean()
avgBikes331 = idStation331['available_bikes'].mean()
avgDocks331 = idStation331['docks_in_service'].mean()

#prints out each average for each bike station
print("\nThe average docks in service for id station 27 is: ", avgDocks27)
print("The average bikes available for id station 27 is: ", avgBikes27)
print("\nThe average docks in service for id station 28 is: ", avgDocks28)
print("The average bikes available for id station 28 is: ", avgBikes28)
print("\nThe average docks in service for id station 60 is: ", avgDocks60)
print("The average bikes available for id station 60 is: ", avgBikes60)
print("\nThe average docks in service for id station 224 is: ", avgDocks224)
print("The average bikes available for id station 224 is: ", avgBikes224)
print("\nThe average docks in service for id station 331 is: ", avgDocks331)
print("The average bikes available for id station 331 is: ", avgBikes331,"\n")

#creates and prints out a pivot table with the ids and their averages for bikes and docks
table = data.pivot_table(data, index=['id'],aggfunc={'docks_in_service': np.mean, 'available_bikes': np.mean})
print(table)

#creates a bar chart showing the averages
table.plot(kind='bar')
plt.xlabel('Bike Station Id')
plt.ylabel('Number for Averages')
plt.title('Average of available bikes and docks in service for each station')
plt.savefig('baraverage.png')
plt.show()

#creates a line graph showing the averages
table.plot()
plt.xticks([27,28,60,224,331])
plt.xlabel('Bike Station Id')
plt.ylabel('Number for Averages')
plt.title('Average of available bikes and docks in service for each station')
plt.savefig('lineaverage.png')
plt.show()

#creates a chart for counting total bikes and docks for each day of the week
data['biketime'] = pd.to_datetime(data['biketime'])
data.groupby(data['biketime'].dt.weekday)['available_bikes','docks_in_service'].count().plot(kind='bar', rot=0)
positions = (0,1,2,3,4,5,6)
labels = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
plt.xticks(positions,labels)
plt.ylabel('Total Count')
plt.xlabel('Days of the week')
plt.title('Total count of bikes available and docks in service for each day')
plt.savefig('totalcount.png')
plt.show()

#creates a pie chart with the averages of percent_full for each station
id_labels = '27','28','60','224','331'
percents = [21.95,26.96,23.53,30.42,27.61]
explode = (0, 0, 0, 0, 0)
fig1, ax1 = plt.subplots()

#extra feature found online for showing actual value on the pie slices
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

ax1.pie(percents, explode=explode, labels=id_labels, autopct = make_autopct(percents),
        shadow=True, startangle=90)

ax1.axis('equal')
plt.title('Avertage Percent Full for Each Station')
plt.savefig('averagepercentfullpie.png')
plt.show()

conn.close()