from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import RANSACRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import numpy as np
from numpy import newaxis



class Regression(object):

    def fnLinearRegression1(self, year, avgTemp):        
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(feature_train[:, newaxis], target_train)
        return (feature_train, target_train, feature_test, target_test, feature_train, reg.predict(feature_train[:, newaxis]), reg.coef_, reg.intercept_)

    def fnLinearRegression(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        reg = linear_model.LinearRegression()
        reg.fit(feature_train[:, newaxis], target_train)    
        return (reg.score(feature_test[:, newaxis], target_test), reg.predict(predictYear))

    def fnIsotonicRegression(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        isoReg = IsotonicRegression()
        isoReg.fit(feature_train, target_train)
        return (isoReg.score(feature_test, target_test), isoReg.predict(predictYear))

    def fnBayesianRidge(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        br = BayesianRidge(compute_score=True)
        br.fit(feature_train[:, np.newaxis], target_train)
        return (br.score(feature_test[:, np.newaxis], target_test), br.predict(predictYear))

    def fnRANSACRegressor(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        rr = RANSACRegressor()
        rr.fit(feature_train[:, np.newaxis], target_train)
        return (rr.score(feature_test[:, np.newaxis], target_test), rr.predict(predictYear))

    def fnGaussianProcessRegressor(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        gp = GaussianProcessRegressor(kernel = 1.0 * RBF([1.0]))
        gp.fit(feature_train[:, np.newaxis], target_train)
        return (gp.score(feature_test[:, np.newaxis], target_test), gp.predict(predictYear))

    def fnSVR(self, year, avgTemp, predictYear):
        feature_train, feature_test, target_train, target_test = train_test_split(year, avgTemp, test_size=0.1, random_state=42)
        sv = SVR(kernel='rbf',C=10000,gamma=.001)
        sv.fit(feature_train[:, np.newaxis], target_train)
        return (sv.score(feature_test[:, np.newaxis], target_test), sv.predict(predictYear))