from pyspark import SparkContext
from pyspark.sql import SQLContext
import numpy as np


class ListAttribute:
        """
        These are the column number of data found in file.
        """ 
        dt = 0
        AverageTemperature = 1
        AverageTemperatureUncertainty = 2
        City = 3
        Country = 4
        Latitude = 5
        Longitude = 6

class DataParser(object):   
    
    
    def __init__(self):
        """
        Initialize the spark and sql context.
        Read the .csv file in dataframe format.
        """
        sc = SparkContext()
        sqlContext = SQLContext(sc)
        
        global df
        df = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").load("Data/GlobalLandTemperaturesByCity.csv")

        #Remove the data for which there is no Average temperature
        df = df.filter(df['AverageTemperature'].rlike("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"))
        self.city = df.rdd.map(lambda x: x[3]).collect()
        self.country = df.rdd.map(lambda x: x[4]).collect()
        self.year = df.rdd.map(lambda x: int(x[0][:4])).collect()

        

    def getListOfCountryCity(self):
        return (list(set(self.country)), list(set(self.city)), list(set(self.year)))
    
    def getAvgTempForMonthYear(self, Month, Year):
        """
        return list of coordinates and list of avg temperature
        """
        p = df.filter(df['dt'].rlike(str(Year).zfill(4)+"-"+str(Month).zfill(2)+"-"+"[.digit.]*"))
        pCoordinate = p.rdd.map(lambda x: [float(x[5][:-1])*-1 if x[5][-1] == 'S' else float(x[5][:-1]), float(x[6][:-1])*-1 if x[6][-1] == 'W' else float(x[6][:-1])]).collect()
        pAvgTemp = p.rdd.map(lambda x: float(x[1])).collect()
        return (pCoordinate, pAvgTemp)
    

    def getPerMonthAvgTempData(self, City, Country, Month, numberOfItems):
        """
        get the list of data for specific city, country and Month
        Data is returned as a list of list
        Returned list contains data in this format: [ [year, angTemp], [year, avgTemp]]
        """

        #get a list of list for data for specific country. [:4] is used to extract year.
        p = df.filter(df['Country'] == Country).filter(df['City'] == City).filter(df['dt'].rlike("[.digit.]*"+"-"+str(Month).zfill(2)+"-"+"[.digit.]*")).limit(int(numberOfItems))
        pList = p.rdd.map(lambda x: [float(x[0][:4]), float(x[1])]).collect()
        return pList

    def getDataForCityCountryMonth(self, City, Country, Month):
        """
        get the list of data for specific city, country and Month
        Data is returned as a list of list
        Returned list contains data in this format: [ [year...], [avgTemp...], [avgTempUncertainity...], [latitude...], [longitude...]]
        """

        #get a list of list for data for specific country. [:4] is used to extract year.
        p = df.filter(df['Country'] == Country).filter(df['City'] == City).filter(df['dt'].rlike("[.digit.]*"+"-"+str(Month).zfill(2)+"-"+"[.digit.]*"))
        pList = p.rdd.map(lambda x: [float(x[0][:4]), float(x[1]), float(x[2]), x[5], x[6]]).collect()
        
        l = []
        pList = np.array(pList)
        for attr in [0,1,2,3,4]:
            p = pList[ : ,attr]            
            l.append(p)
        return l

    def getTemperature(self, City, Country, Month, Year):
        """
        get the list of data for specific city, country and Month
        Data is returned as a list of list
        Returned list contains data in this format: [ [year...], [avgTemp...], [avgTempUncertainity...], [latitude...], [longitude...]]
        temp is the avgTemp for specified year. If there is no data for speciified year, -9999 is returned.
        """

        p = df.filter(df['Country'] == Country).filter(df['City'] == City).filter(df['dt'].rlike("[.digit.]*"+"-"+str(Month).zfill(2)+"-"+"[.digit.]*"))
        pList = p.rdd.map(lambda x: [float(x[0][:4]), float(x[1]), float(x[2]), x[5], x[6]]).collect()
        
        temp = -9999
        for row in pList:
            if row[0] == float(Year):
                temp = row[1]
                break

        l = []
        pList = np.array(pList)
        for attr in [0,1,2,3,4]:
            p = pList[ : ,attr]            
            l.append(p)
        return (temp, l)
        

    def SplitYearAvgTemp(self, pList):
        return pList[ListAttribute.dt], pList[ListAttribute.AverageTemperature]
