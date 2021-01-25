# Easing functions all receive one float between 0 and 1 inclusive.

import numpy as np
elasticPeriod = 0.3
backConst = 1.70158
bounceN = 7.5625
bounceD = 2.75

# Base functions (in functions)
def linearBase(x):
    return x
def polyBase(x, deg): 
    return x**deg
def quadBase(x):
    return polyBase(x, 2)
def cubicBase(x):
    return polyBase(x, 3)
def quartBase(x):
    return polyBase(x, 4)
def quintBase(x):
    return polyBase(x, 5)
def sineBase(x):
    return 1 - np.cos((x*np.pi)/2)
def expoBase(x):
    return np.piecewise(x, [x<=0, x>0], [lambda x: 0, lambda x: pow(2, 10*(x-1))])
def circBase(x):
    return 1 - np.sqrt(1 - x**2)
def backBase(x):
    return x*x * ((backConst+1)*x - backConst)
def elasticBaseCore(x, p):
    y = x-1
    return -1 * pow(2, 10*y) * np.sin((y-p*0.25)*(2*np.pi/p))
def elasticBase(x):
    return elasticBaseCore(x, elasticPeriod)
def bounceBaseCore(x, d, n):
    return np.piecewise(x, [x<1/d, (x>=1/d)&(x<2/d), (x>=2/d)&(x<2.5/d), x>=2.5/d], 
    [lambda x: n*x**2, lambda x: n*(x-1.5/d)**2+0.75, lambda x: n*(x-2.25/d)**2+0.9375, lambda x: n*(x-2.625/d)**2+0.984375])
def bounceBase(x):
    return 1 - bounceBaseCore(1-x, bounceD, bounceN)

# Lists for options
easingList = ["linear", "quad", "cubic", "quart", "quint", "sine", "expo", "circ", "back", "elastic", "bounce"]
easingDict = {"linear":linearBase, "quad":quadBase, "cubic":cubicBase, "quart":quartBase, "quint":quintBase, "sine":sineBase, "expo":expoBase, "circ":circBase, "back":backBase, "elastic":elasticBase, "bounce":bounceBase}

# Complete function
def ease(x, option="linear", io="i"):
    if io == "i":
        return easingDict[option](x)
    elif io == "o":
        return 1 - easingDict[option](1-x)
    elif io == "io":
        s = np.where(x < 0.5)[0]
        b = np.where(x >= 0.5)[0]
        y = x*2
        y[s] = easingDict[option](y[s]) * 0.5
        y[b] = -easingDict[option](2-y[b]) * 0.5 + 1
        return y

# For tests
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    x = np.linspace(0, 1, 10001)
    y = ease(x, "bounce", "i")
    plt.plot(x, y)
    plt.show()
