import time
import numpy as np
import conceptdrift.alg.AdaptativeChange as ac
from conceptdrift.gen.gen import gengenDataLine, genDataPol

## Caso 2 Tipo Incremental - Cambio eje de ordenadas. ONLINE
if __name__ == "__main__":
    print('Caso 2 Tipo Incremental - Cambio eje de ordenadas ONLINE')
    np.random.seed(1) 
    xbuild, ybuild = genDataLine(4, 10, 500, 0, 3)
    x0, y0 = genDataLine(4, 10, 500, 0, 3)
    nArray = np.linspace(10,25,100)
    x1, y1 = genDataLine(4, nArray, 100, 0, 3)
    x2, y2 = genDataLine(4, 25, 400, 0, 3)
    x = x0 + x1
    y = y0 + y1

    dfList =  list(zip(x0,y0))
    data0 = pd.DataFrame(dfList, columns = ['x' , 'y']) 

    sns.lmplot(x="x", y="y", data=data0, line_kws = {'color':'cyan'})
    plt.scatter(x1,y1)
    plt.scatter(x2,y2)
    plt.show()

    alg = ac.DetectChangeAlgOnline(300, 100, xbuild, ybuild, 0.2, 20)
    alg.printModel()
    start = time.time()
    alg.addData(x, y)
    alg.printModel()
    alg.addData(x2, y2)
    print(f"Add data Time Taken: {time.time() - start:.3f} sec")
    alg.plotResiduals()
    alg.plotErrorAcum()
    alg.printModel()
    alg.mae()
    print('Change Points: ' + str(alg.changePoints))
    print(f"Total Time Taken: {time.time() - start:.3f} sec")
