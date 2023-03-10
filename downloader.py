#Name: Dennis Meltser
#Class: ISMG 6020-E02
#Date:10/1/2021

import json
import urllib.request, urllib.parse, urllib.error
import datetime
import pymongo
import pprint
import certifi

#Connection to the MongoDB server
mc = pymongo.MongoClient('mongodb+srv://m001-student:m001-mongodb-basics@sandbox.ji1pp.mongodb.net/bikedata?retryWrites=true&w=majority',tlsCAFile=certifi.where())
bikesDB = mc['bikedata']
collection = bikesDB['bikestations']

#Check for the connection
print("Connected to MongoDB")

#list of the station ID's
BIKE_ID = ['27','28','60','224','331']

# Initial settings that control the data download
paramD = dict()                          

#loops through the list and replaces the ID section of the URL with each station ID
for i in range(len(BIKE_ID)):
     bikeURL = 'https://data.cityofchicago.org/resource/eq45-8inv.json?id={}&%24order=timeStamp+DESC&%24limit=5000'.format(BIKE_ID[i])

# create a URL based on base URL
     print("\n",bikeURL)

     # open the URL using the urllib library
     document = urllib.request.urlopen(bikeURL)
     # get all of the text from the document
     text = document.read().decode()
          
     if document.getcode() != 200 :
          print("Error code=",document.getcode(), bikeURL)
          text = "{}"

     # Load the JSON text from the URL into a dictionary using the json library
     js = json.loads(text)

     #Inserts many to the MongoDB bikestations collection
     result = collection.insert_many(js)
     #Creates the time to print
     ts = datetime.datetime.now()
     # Outputs that the station is done downloading
     print("Bikestation ID: ", BIKE_ID[i], "is done downloading")
     #prints that the database was updated with bikestation data with a current timestamp
     print("Database updated with", len(js), "stations on", ts)

#Verifies the total number of documents in the collection
print("\nTotal number of documents downloaded: ",collection.count_documents({}))

#**EXTRA** Line 55 was used from code review which prints an example of an object in the collection
print("\nExample object in collection: ")
pprint.pprint(js[0])