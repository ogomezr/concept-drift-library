import time
import numpy as np
import conceptdrift.alg.AdaptativeChange as ac
from conceptdrift.gen.gen import genDataLine, genDataPol

## Caso 4 Outliers - Prueba 2 - Outliers dispersos
if __name__ == "__main__":
    print('Caso 4 Outliers - Prueba de robustez}')
    print('Prueba 2 - Outliers dispersos')
    np.random.seed(2) 
    xbuild, ybuild = genDataLine(4, 10, 300, 0, 3)
    x, y = genDataLine(4, 10, 1000, 0, 3)
    y[500] = 47
    y[600] = 15
    y[650] = 10
    y[720] = 30

    plt.scatter(x,y)
    plt.show()

    print('\u03BB = 20')
    alg = ac.DetectChangeAlg(300, 100, xbuild, ybuild, 0.2, 20)
    alg.addData(x, y)
    alg.plotErrorAcum()
    print('Change Points: ' + str(alg.changePoints))

    print('\u03BB = 40')
    alg = ac.DetectChangeAlg(300, 100, xbuild, ybuild, 0.2, 40)
    alg.addData(x, y)
    alg.plotErrorAcum()
    print('Change Points: ' + str(alg.changePoints))

    print('\u03BB = 100')
    alg = ac.DetectChangeAlg(300, 100, xbuild, ybuild, 0.2, 100)
    alg.addData(x, y)
    alg.plotErrorAcum()
    print('Change Points: ' + str(alg.changePoints))

