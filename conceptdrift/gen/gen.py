import numpy as np

def genDataLine(m, n, nS, mu, sigma):
    epsilon = np.random.normal(mu, sigma, nS)
    x = np.random.rand(nS)*10
    y = m*x + n + epsilon
    return x.tolist(), y.tolist()      

def genDataPol(a, b, c, d ,nS,mu,sigma):
    epsilon = np.random.normal(mu, sigma, nS)
    x = np.random.rand(nS)*10
    y = (a * x**3) + (b * x**2) + c * x + d + epsilon
    return x.tolist(), y.tolist()   
