
from flask import Flask, render_template, request
from bson.json_util import dumps
from Data_parser import DataParser, ListAttribute
from regression import Regression
from classification import Classification
import numpy as np
from numpy import newaxis
import visualizations


app = Flask(__name__)


@app.route("/")
def index():
   return render_template("index.html")

@app.route('/ListofCountryCity', methods=['POST','GET'])
def ListofCountryCity():
    try:
        country, city, year  = dataFrame.getListOfCountryCity();
        return dumps({"country":country, "city":city, "year":year})
    except:
        return "error"


@app.route('/AvgMonthTemp', methods=['POST','GET'])
def AvgMonthTemp():           
    """
    get the list of data for specific city, country and Month
    Data is returned as a list of list
    Returned list contains data in this format: [ ['Year','Avg Temperature'] [year, avgTemp].......]
    """
    try:
        print "City"+request.form['City']
        p = dataFrame.getPerMonthAvgTempData(City=request.form['City'], Country=request.form['Country'], Month=request.form['Month'], numberOfItems=request.form["NumberOfYears"])

        l = []
        pList = np.array(p)
        for attr in [0,1]:
            pp = pList[ : ,attr]            
            l.append(pp)

        yearList, avgTempList = dataFrame.SplitYearAvgTemp( l )
        avgTempList = np.array(avgTempList).astype(np.float)
        yearList = np.array(yearList).astype(np.float)
        training_x, training_y, test_x, test_y, predictLine_x, predictLine_y, cofficient, intercept = regression.fnLinearRegression1(yearList, avgTempList)
        return dumps({"data":p, "cofficient":cofficient, "intercept":intercept})
    except:
        return "error"


@app.route('/TemperaturePredictionForCoordinates', methods=['POST','GET'])
def TemperaturePredictionForCoordinates():           
    """
    For any longitude, Latitude, it predicts wheather temperature is hot, medium or cold.
    Returned list contains data in this format: [[list of coordinates][list of temperature class][predicted class][score in percentage]]
    """
    try:
        pCoordinate, pAvgTemp = dataFrame.getAvgTempForMonthYear(Month=request.form['Month'], Year=request.form['Year'])
        pred, score = classification.avgTempPredectionBasedOnCoordinates(pAvgTemp, pCoordinate, request.form['Latitude'],request.form['Longitude'])
        return dumps({"pred":pred, "score":score})
    except:
        return "error"

@app.route('/TemperatureClassificationForCoordinates', methods=['POST','GET'])
def TemperatureClassificationForCoordinates():           
    """
    For any longitude, Latitude, it predicts wheather temperature is hot, medium or cold.
    Returned list contains data in this format: [[list of coordinates][list of temperature class]]
    """
    try:
        pCoordinate, pAvgTemp = dataFrame.getAvgTempForMonthYear(Month=request.form['Month'], Year=request.form['Year'])        
        pCoordinate, TempClassification = classification.avgTempClassificationOnCoordinates(pAvgTemp, pCoordinate)
        return dumps({"coordinates":pCoordinate, "Temp_Class":TempClassification})
    except:
        return "error"


@app.route('/AvgTempForSpecifiedMonthWithRegression', methods=['POST','GET'])
def AvgTempForSpecifiedMonthWithRegression():          
    """
    return avg temperature for specified month/year/country/city.
    returned data is in float.
    """ 
    try:
        print request.form['City']
        temp, pList = dataFrame.getTemperature(City=request.form['City'], Country=request.form['Country'], Month=request.form['Month'], Year=request.form['Year'])      

        #if temp is found in database, return the temperature
        if temp > -9999:
            print "actual"
            return dumps(temp)
        #if temp is not found in database, predict it using regression
        else:
            yearList, avgTempList = dataFrame.SplitYearAvgTemp( pList )
            avgTempList = np.array(avgTempList).astype(np.float)
            yearList = np.array(yearList).astype(np.float)
            pYear = float(request.form['Year'])
            predictYear = []
            predictYear.append(pYear)

            scoreReg, PvalueReg = regression.fnLinearRegression(yearList, avgTempList, predictYear)
            print "Linear Regression. Score = " + str(scoreReg) + " ,Predicted Temperature: " + str(PvalueReg)
            scoreIso, PvalueIso = regression.fnIsotonicRegression(yearList, avgTempList, predictYear)
            print "Isotonic Regression. Score = " + str(scoreIso) + " ,Predicted Temperature: " + str(PvalueIso)
            scoreBR, PvalueBR =  regression.fnBayesianRidge(yearList, avgTempList, predictYear)
            print "Bayesian Ridge Regression. Score = " + str(scoreBR) + " ,Predicted Temperature: " + str(PvalueBR)
            scoreRR, PvalueRR = regression.fnRANSACRegressor(yearList, avgTempList, predictYear)
            print "RANSAC Regression. Score = " + str(scoreRR) + " ,Predicted Temperature: " + str(PvalueRR)
            scoreGP, PvalueGP = regression.fnGaussianProcessRegressor(yearList, avgTempList, predictYear)
            print "GaussianProcess Regression. Score = " + str(scoreGP) + " ,Predicted Temperature: " + str(PvalueGP)
            scoreSV, PvalueSV = regression.fnSVR(yearList, avgTempList, predictYear)
            print "SVR Regression. Score = " + str(scoreSV) + " ,Predicted Temperature: " + str(PvalueSV)

            score = np.array([scoreReg, scoreIso, scoreBR, scoreRR, scoreGP, scoreSV])
            pValue = np.array([PvalueReg, PvalueIso, PvalueBR, PvalueRR, PvalueGP, PvalueSV])

            pValue = pValue[np.logical_not(np.isnan(pValue))]
            score = score[np.logical_not(np.isnan(pValue))]           

            minScoreIndex = np.argmin(score)

            

        return dumps({"avgTemp" : pValue[minScoreIndex]})
    except:
        return "error"


@app.route('/AvgMonthTempWithRegression', methods=['POST','GET'])
def AvgMonthTempWithRegression():           
    """
    get the list of data for specific city, country and Month
    Data is returned as a list of list
    Returned list contains data in this format: [ [training_x], [training_y], [test_x], [test_y], [predictLine_x], [predictLine_y]]
    """
    try:
        p = dataFrame.getDataForCityCountryMonth(City=request.form['City'], Country=request.form['Country'], Month=request.form['Month'])
        yearList, avgTempList = dataFrame.SplitYearAvgTemp( p )
        avgTempList = np.array(avgTempList).astype(np.float)
        yearList = np.array(yearList).astype(np.float)
        training_x, training_y, test_x, test_y, predictLine_x, predictLine_y, cofficient, intercept = regression.fnLinearRegression1(yearList, avgTempList)
        return dumps({"training_x":training_x, "training_y":training_y, "test_x":test_x, "test_y":test_y, "predictLine_x":predictLine_x, "predictLine_y":predictLine_y, "cofficient":cofficient, "intercept":intercept})
    except:
        return "error"



if __name__ == '__main__':    
    global dataFrame
    global regression
    global classification    
    dataFrame = DataParser()
    regression = Regression()
    classification = Classification()
    visualization = visualizations.Visualization()
    
    app.run()
