import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
##import seaborn as sns
plt.rcParams.update({'figure.figsize': (8, 5), 'figure.dpi': 120})
plt.style.use('seaborn')
##sns.set_style("dark")
##sns.set(color_codes=True)

class ChooseModel:
    def __init__(self):
        self.bestModel = None
        self.lastScores = []

    def chooseBest(self, x, y, mode=['lin', 'knn', 'pol', 'tree']):
        X = sm.add_constant(x)

        polynomial_features = PolynomialFeatures(degree=3)
        xPoly = polynomial_features.fit_transform(X)

        scores = []
        times = 3

        if 'tree' in mode:
            tree = DecisionTreeRegressor()
            treeScores = cross_val_score(tree, X, y, cv=times)
            scores.append((treeScores.mean(), "DecisionTreeReg", tree))
        if 'knn' in mode:
            knn = KNeighborsRegressor()
            knnScores = cross_val_score(knn, X, y, cv=times)
            scores.append((knnScores.mean(), "K Nearest Neighbors", knn))
        if 'pol' in mode:
            polyReg = LinearRegression()
            polScores = cross_val_score(polyReg, xPoly, y, cv=times)
            scores.append((polScores.mean(), "PolynomialRegression", polyReg))
        if 'lin' in mode:
            linReg = LinearRegression()
            linScores = cross_val_score(linReg, X, y, cv=times)
            scores.append((linScores.mean(), "LinearRegression", linReg))

        scores.sort(reverse=True)
        self.lastScores = scores
        self.bestModel = scores[0]
        if scores[0][1] == "PolynomialRegression":
            X = xPoly

        return scores[0][2].fit(X, y)

    def getBest(self):
        return self.bestModel

    def getBestName(self):
        return self.bestModel[1]

    def printScores(self):
        for i in self.lastScores:
            print(i[0])
            print(i[1])    