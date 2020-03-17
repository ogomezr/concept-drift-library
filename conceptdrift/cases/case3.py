import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import conceptdrift.alg.AdaptativeChange as ac
from conceptdrift.gen.gen import genDataLine, genDataPol

## Caso 3 Tipo Gradual - Cambio de forma.
if __name__ == "__main__":
    print('Caso 3 Tipo Gradual - Cambio de forma')
    np.random.seed(5) 
    a, b, c, d = -0.4, 2, 10, 20

    aArray = np.full(125,0,float)
    bArray = np.full(125,0,float)
    cArray = np.full(125,4,float)
    dArray = np.full(125,10,float)

    aArray2 = np.full(375,a,float)
    bArray2 = np.full(375,b,float)
    cArray2 = np.full(375,c,float)
    dArray2 = np.full(375,d,float)

    nS = 125

    for i in range(nS):
        if i< (nS/10):
            aArray[i]=a
            bArray[i]=b
            cArray[i]=c
            dArray[i]=d
        elif i < (nS/10)*2 :
            aArray[i]=0
            bArray[i]=0
            cArray[i]=4
            dArray[i]=10
        elif i< (nS/10)*4:
            aArray[i]=a
            bArray[i]=b
            cArray[i]=c
            dArray[i]=d
        elif i < (nS/10)*6:
            aArray[i]=0
            bArray[i]=0
            cArray[i]=4
            dArray[i]=10
        else :
            aArray[i]=a
            bArray[i]=b
            cArray[i]=c
            dArray[i]=d
            
    aArrayMix = np.concatenate((aArray,aArray2),axis=None)
    bArrayMix = np.concatenate((bArray,bArray2),axis=None)
    cArrayMix = np.concatenate((cArray,cArray2),axis=None)
    dArrayMix = np.concatenate((dArray,dArray2),axis=None)


    xbuild, ybuild = genDataLine(4, 10, 500, 0, 3)
    x0, y0 = genDataLine(4, 10, 500, 0, 3)
    x1, y1 = genDataPol(aArray, bArray, cArray, dArray, 125, 0, 3)
    x = x0 + x1
    y = y0 + y1
    x2, y2 = genDataPol(aArray2, bArray2, cArray2, dArray2, 375, 0, 3)

    dfList =  list(zip(x0,y0))
    data0 = pd.DataFrame(dfList, columns = ['x' , 'y']) 

    sns.lmplot(x="x", y="y", data=data0, line_kws = {'color':'cyan'})
    plt.scatter(x1,y1)
    plt.scatter(x2,y2)
    plt.show()

    alg = ac.DetectChangeAlg(300, 100, xbuild, ybuild, 0.2, 50)
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
    print(f"Total Time Taken: {time.time() - start:.3f} sec")

