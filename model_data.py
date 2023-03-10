import pymongo
import certifi
import sqlite3
import datetime
import os

#Connection to the MongoDB server
mc = pymongo.MongoClient('mongodb+srv://m001-student:m001-mongodb-basics@sandbox.ji1pp.mongodb.net/bikedata?retryWrites=true&w=majority',tlsCAFile=certifi.where())
bikesDB = mc['bikedata']
collection = bikesDB['bikestations']

#Check for the connection
print("Connected to MongoDB")

#EXTRA!!
#Lines 17-18 was adapted from code I reviewed
if 'index.sqlite' in os.listdir('.'):
    os.remove('index.sqlite')

#Connection to the sqlite database
dbconn = sqlite3.connect('index.sqlite')
cur = dbconn.cursor()

#Check for connection to SQLite database
print("Connected to SQLite")

#Drops the table every run
cur.executescript('DROP TABLE IF EXISTS BikeStations')

#Creates the BikeStations table with the correct data
cur.execute('''CREATE TABLE BikeStations (id INTEGER, 
                                          biketime TEXT, 
                                          station_name TEXT, 
                                          total_docks INTEGER, 
                                          docks_in_service INTEGER, 
                                          available_docks INTEGER, 
                                          available_bikes INTEGER,
                                          percent_full INTEGER,
                                          status TEXT,
                                          latitude REAL,
                                          longitude REAL)''')

#Grabs all the documents without the json created '_id'
stations = collection.find({},{'_id':0})

#A counter for committing 100 documents at a time
count = 0

#Loops through the documents pulling each object
for objects in stations:
    #Grabs the timestamp from the object and converts from iso format
    isodate = objects['timestamp']
    dt = datetime.datetime.fromisoformat(isodate)

    #Creates the data for the sql insert statement
    stationName = objects['station_name']
    statuses = objects['status']
    latitude = objects['latitude']
    longitude = objects['longitude']
    #Checks to make sure the data pulled is of int value and will print an error if not
    try:
        ids = int(objects['id'])
        totalDocks = int(objects['total_docks'])
        docksInService = int(objects['docks_in_service'])
        availableDocks = int(objects['available_docks'])
        availableBikes = int(objects['available_bikes'])
        percentFull = int(objects['percent_full'])
    except ValueError:
        print("\nError! Input should be an integer ")

    #Inserts the bikestation documents into their respective rows and columns
    cur.execute('''INSERT INTO BikeStations(id, 
                                            biketime, 
                                            station_name, 
                                            total_docks, 
                                            docks_in_service, 
                                            available_docks, 
                                            available_bikes, 
                                            percent_full, 
                                            status, 
                                            latitude, 
                                            longitude) 
                                            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (ids, dt, stationName, totalDocks, docksInService, availableDocks, availableBikes, percentFull, statuses, latitude, longitude)) 
    
    #Increments the count for every document
    count = count + 1

    #Only commits the documents when there is 100 at a time
    if count%100==0:
        print("100 records committed")
        dbconn.commit()

#Confirms the total bikestations processed while saving and closing the process
print(count,"Bikestations processed")
dbconn.commit()
dbconn.close()