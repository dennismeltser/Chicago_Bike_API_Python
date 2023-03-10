#Name: Dennis Meltser
#Class: ISMG 6020-E02
#Date:9/20/2021

#opening the file and reading the lines
fname = input('Enter the file name: ')
try:
    fhand = open("bdata.txt")
except:
    print('Error: ',fname, 'cannot be opened.')
    quit()

fileText = fhand.readlines()

#This was a sanity check print(type(fileText[0]))

#a list of the id stations **Extra**
idStrings = ['"id": "27"','"id": "28"','"id": "60"','"id": "224"','"id": "331"']

#each data variable as a list to be appended to
stationNames = []
bikesAvailable = []
timeStamps = []
availableDocks = []
statNums = []
totalDocks = []

#the for loops that iterate through the id stations and the file provided
for line in fileText:
    for idString in idStrings: 
        if idString in line:
            data = line.split(",")
            statName = data[2].split(":")
            stationNames.append(statName[1].strip('" "'))
            bikes = data[6].split(":")
            bikesAvailable.append(bikes[1].strip('" "'))
            time = line.split()
            timeStamps.append(time[3].strip('"",'))
            available = data[5].split(":")
            availableDocks.append(available[1].strip('" "'))
            num = data[0].split(":")
            statNums.append(num[1].strip('" "'))
            total = data[3].split(":")
            totalDocks.append(total[1].strip('" "'))
  
fhand.close()

#the bikestation object that prints out the lines
class bikeStation:
    def __init__(self, statNum, timestamp, stationName, totalDocks, availableDocks, bikesAvailable):
        self.ID=statNum
        self.timestamp=timestamp
        self.StationName=stationName
        self.TotalDocks=totalDocks
        self.availableDocks=availableDocks
        self.availableBikes=bikesAvailable
        print(stationName, " had", bikesAvailable, " bikes available on", timestamp.replace("T", " ").replace(".000", ""))
    
    #the position class for latitude and longitude (for future use)
    class position:
        def __init__(self,longitude,latitude):
            self.longitute = longitude
            self.latitude = latitude

    #property for the stationname variable
    @property
    def StationName(self):
        return self.__StationName
    @StationName.setter
    def StationName(self, x):
        x = str(x)
        self.__StationName = x[0:20]

#creates an object for each iteration of the id stations list and has it printed **Extra**
for i in range (len(idStrings)):
    bs1 = bikeStation(statNums[i], timeStamps[i], stationNames[i], totalDocks[i], availableDocks[i], bikesAvailable[i])

#a variable for the stations id numbers in order
stations = (statNums[1], statNums[2], statNums[4], statNums[0], statNums[3])

#variables for summing the total number of available docks and total number of available bikes
totalAvailableDocks = sum([int(item) for item in availableDocks])
totalAvailableBikes = sum([int(item) for item in bikesAvailable])

#prints the station ids with the available docks and bikes
print("Stations:", stations, "Bikes Available", totalAvailableBikes, "Docks Available", totalAvailableDocks)