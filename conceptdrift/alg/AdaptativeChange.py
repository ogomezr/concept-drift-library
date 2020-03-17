import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from abc import ABC,abstractclassmethod
import matplotlib.pyplot as plt
import conceptdrift.alg.components.ChooseModel as cm
import conceptdrift.alg.components.PageHinkleyTest as ph
##import seaborn as sns
plt.rcParams.update({'figure.figsize': (8, 5), 'figure.dpi': 120})
plt.style.use('seaborn')
##sns.set_style("dark")
##sns.set(color_codes=True)

class AdaptativeChange(ABC):
    @abstractclassmethod
    def __init__(self, sizeBig, sizeSmall, x, y, phAdmissibleChange,
             phThreshold, mode=['lin', 'pol', 'tree']):
        if len(x)>sizeBig:
            x = x[len(x)-sizeBig:len(x)]
            y = y[len(y)-sizeBig:len(y)]
            self.lenData = sizeBig
        else:
            self.lenData = len(x)
        self.xData = x
        self.yData = y
        self.sizeBig = sizeBig
        self.sizeSmall = sizeSmall
        self.chooseModel = cm.ChooseModel()
        self.model = self.chooseModel.chooseBest(x, y, mode)
        self.error = []
        self.ph = ph.PageHinkleyTest(phAdmissibleChange, phThreshold)
        self.changeTime = False
        self.mode = mode
        self.changePoints = []
        self.recoverPoints = []
        self.n = 0
        
    def changeModel(self):
        self.xData = self.xData[-self.sizeSmall:]
        self.yData = self.yData[-self.sizeSmall:]
        self.model = self.chooseModel.chooseBest(
            self.xData, self.yData, self.mode)
        self.lenData = self.sizeSmall
        self.changePoints.append(self.n)
        self.changeTime = True

    def getModel(self):
        return self.chooseModel

    def returnModel(self, model):
        r = np.arange(0, 10, 0.1)
        xData = sm.add_constant(r)
        tittle = self.chooseModel.bestModel[1]
        if tittle == "PolynomialRegression":
            polynomial_features = PolynomialFeatures(degree=3)
            xData = polynomial_features.fit_transform(xData)
        yData = model.predict(xData)
        return yData

    def predict(self, x, y):
        yData = y
        xData = [[1., x]]
        tittle = self.chooseModel.bestModel[1]
        if tittle == "PolynomialRegression":
            polynomial_features = PolynomialFeatures(degree=3)
            xData = polynomial_features.fit_transform(xData)
        yPred = self.model.predict(xData)
        error = abs(yData - yPred[0])
        self.error.append(error)
        return error
    
    def plotResiduals(self):
        self.ph.plotResiduals()

    
    def plotErrorAcum(self):
        self.ph.plotErrorAcum()   
        ymax=self.ph.getSumError()
        plt.vlines(self.changePoints,0,ymax,linewidth=1,ls='--',color='r',label='Change')
        plt.vlines(self.recoverPoints,0,ymax,linewidth=1,ls='-.',color='b',label='Recovery')
        plt.legend(['AcumError','Change','Recovery'],loc = 4)
        plt.show()
        
    def printModel(self):          
        r =np.arange(0,10,0.05)
        xData = sm.add_constant(r)
        tittle = self.chooseModel.bestModel[1]
        if tittle == "PolynomialRegression":
            polynomial_features= PolynomialFeatures(degree=3)
            xData = polynomial_features.fit_transform(xData)  
        tittle+=' || Window Big: ' + str(self.sizeBig) + ' Small: '+str(self.sizeSmall) + ' || PH - \u03C3: ' + str(
            self.ph.admissibleChange) + ' \u03BB: ' + str(self.ph.threshold)
        yData = self.model.predict(xData)   
        plt.scatter(self.xData,self.yData)
        plt.plot(r, yData, color='red', linewidth=2)
        plt.title(tittle)
        plt.show()
        
    def mae(self):
        sum = 0
        for error in self.error:
            sum+=error
        mse = sum/self.n
        print('MAE: ' + str("%.2f" % mse))
        
        
        
class DetectChangeAlg(AdaptativeChange):
    def __init__(self, sizeBig, sizeSmall, x, y, phAdmissibleChange,
                 phThreshold, mode=['lin', 'knn', 'pol', 'tree'], minCont=25):
        super().__init__(sizeBig, sizeSmall, x, y, phAdmissibleChange,
                 phThreshold, mode)
        self.debt = False
        self.minCont = minCont
        self.cont = 0

    def addData(self, x, y):
        xData = x.copy()
        yData = y.copy()
        while xData:
            nextX = xData.pop(0)
            nextY = yData.pop(0)
            self.xData.append(nextX)
            self.yData.append(nextY)
            self.lenData += 1
            self.n+=1
            if self.lenData > self.sizeBig:
                self.xData.pop(0)
                self.yData.pop(0)
                self.lenData -= 1
            error = self.predict(nextX, nextY)
            self.cont+=1
            if self.ph.runTest(error):
                if self.cont >= self.minCont:
                    self.changeModel()
                    self.cont = 0
                    self.debt = True
            elif self.cont > 0 and self.debt:
                self.changeModel()
                self.cont = 0
                self.debt = False
            if self.changeTime and self.lenData == self.sizeBig:
                self.model = self.chooseModel.chooseBest(
                    self.xData, self.yData, self.mode)
                self.recoverPoints.append(self.n)
                self.changeTime = False
            


    

class DetectChangeAlgOnline(AdaptativeChange):
    def __init__(self, sizeBig, sizeSmall, x, y, phAdmissibleChange,
                 phThreshold, mode=['lin', 'knn', 'pol', 'tree']):
        super().__init__(sizeBig, sizeSmall, x, y, phAdmissibleChange,
                 phThreshold, mode)

    def addData(self, x, y):
        xData = x.copy()
        yData = y.copy()
        while xData:
            nextX = xData.pop(0)
            nextY = yData.pop(0)
            self.xData.append(nextX)
            self.yData.append(nextY)
            self.lenData += 1
            self.n+=1
            if self.lenData > self.sizeBig:
                self.xData.pop(0)
                self.yData.pop(0)
                self.lenData -= 1
            error = self.predict(nextX, nextY)
            if self.ph.runTest(error):
                self.changeModel()
                self.changeTime = True
            else:
                self.model = self.chooseModel.chooseBest(
                    self.xData, self.yData, self.mode)       
            if self.changeTime and self.lenData == self.sizeBig:       
                self.recoverPoints.append(self.n)
                self.changeTime = False
            

    
    def plotErrorAcum(self):
        self.ph.plotErrorAcum()   
        ymax=self.ph.getSumError()
        plt.vlines(self.changePoints,0,ymax,linewidth=1,ls='--',color='lightpink',label='Change')
        plt.vlines(self.recoverPoints,0,ymax,linewidth=1,ls='-.',color='b',label='Recovery')
        plt.legend(['AcumError','Change','Recovery'],loc = 4)
        plt.show()
        
