import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import conceptdrift.alg.AdaptativeChange as ac
from conceptdrift.gen.gen import genDataLine, genDataPol

## Caso 1 Tipo Abrupto/Repentino - Aumento de pendiente
if __name__ == "__main__":
    print('Caso 1 Tipo Abrupto/Repentino - Aumento de pendiente')
    np.random.seed(1) 
    xbuild, ybuild = genDataLine(4, 10, 500, 0, 3)
    x0, y0 = genDataLine(4, 10, 500, 0, 3)
    x1, y1 = genDataLine(10, 10, 75, 0, 3)
    x2, y2 = genDataLine(10, 10, 425, 0, 3)
    x = x0 + x1
    y = y0 + y1

    dfList =  list(zip(x0,y0))
    data0 = pd.DataFrame(dfList, columns = ['x' , 'y']) 

    sns.lmplot(x="x", y="y", data=data0, line_kws = {'color':'cyan'})
    plt.scatter(x1+x2,y1+y2)
    plt.show()

    alg = ac.DetectChangeAlg(300, 100, xbuild, ybuild, 0.2, 20)
    alg.printModel()
    start = time.time()
    alg.addData(x, y)
    time1 = time.time()-start
    alg.printModel()
    start = time.time()
    alg.addData(x2, y2)
    print(f"Add data Time Taken: {(time.time() - start)+time1:.3f} sec")
    alg.plotResiduals()
    alg.plotErrorAcum()
    alg.printModel()
    alg.mae()
    print('Change Points: ' + str(alg.changePoints))
