import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize': (8, 5), 'figure.dpi': 120})
plt.style.use('seaborn')

class PageHinkleyTest:
    def __init__(self, admissibleChange, threshold):
        """Summary or Description of the Function
    
        Parameters:
        argument1 (int): Description of arg1
    
        Returns:
        int:Returning value
    
        """
        self.admissibleChange = admissibleChange
        self.threshold = threshold
        self.n = 0
        self.mT = 0
        self.MT = 1
        self.sumError = 0
        self.residuals = []
        self.acumError = []
        self.meanError = 0

    def runTest(self, x):
        """Summary or Description of the Function

        Parameters:
        argument1 (int): Description of arg1
    
        Returns:
        int:Returning value

        """
        self.n += 1
        self.sumError += x
        self.meanError = (x + self.meanError * (self.n - 1)) / self.n
        self.mT = max(0, 0.94 * self.mT +
                      (x - self.meanError - self.admissibleChange))
        self.MT = min(self.MT, self.mT)
        pH = self.mT - self.MT
        self.residuals.append(x)
        self.acumError.append(self.sumError)
        return pH >= self.threshold
    
    def plotResiduals(self):
        plt.scatter(list(range(len(self.residuals))), self.residuals, color='y',label = 'AcumError')
        plt.title("Residuals")
        plt.show()
 
        
    def plotErrorAcum(self):
        plt.plot(self.acumError,color='orange')
        plt.title("Acumulated Error")
        
    def getSumError(self):
        return self.sumError