import numpy as np
from numpy import pi
import scipy.signal as ss
import matplotlib.pyplot as plt


class Filter:
    """
    AntiAliasFilter:

    
    """
    def __init__(self):

        self.transferFunc = ss.ZerosPolesGain([], [1], 1)

        self.fp = 1e3
        self.ap = 3

        self.fa = 2e3
        self.aa = 40

        self.approx = "cheby2"      # [butter, cheby1, cheby2, ellip]

    def updateFilter(self, fp, ap, fa, aa, approx):
        """
        Updates filter parameters
            [butter, cheby1, cheby2, ellip]

        """
        self.fp = fp
        self.ap = ap

        self.fa = fa
        self.aa = aa

        self.approx = approx

        self.transferFunc = self.buildFilter()

    def getBode(self, w = None, n = 500):
        """
        Input:
                w: array of frequencies
                n: number of points

        Output:
                w, mag, phase of Bode
        """
        w, mag, phase = ss.bode(self.transferFunc, w = w, n = n)
        return w, mag, phase
    
    def getTempResponse(self, t, y):
        t_out, y_out, x_out = ss.lsim(self.transferFunc, y, t)
        return t_out, y_out


######################################################
######################################################
######################################################
######################################################
######################################################
    """
        Métodos privados
    
    """
    def buildFilter(self):
        """
        Calculates filter

        """
        z,p,k = [], [1], 1

        if self.approx == "butter":
            N, Wn = ss.buttord(self.fp * 2 * pi, self.fa * 2 * pi, self.ap, self.aa, analog = True)
            z, p, k = ss.butter(N, Wn, btype='low', analog=True, output='zpk')         
                        

        elif self.approx == "cheby1":
            N, Wn = ss.cheb1ord(self.fp * 2 * pi, self.fa * 2 * pi, self.ap, self.aa, analog = True)
            z, p, k = ss.cheby1(N, self.ap, Wn, btype='low', analog=True, output='zpk')         

        elif self.approx == "cheby2":
            N, Wn = ss.cheb2ord(self.fp * 2 * pi, self.fa * 2 * pi, self.ap, self.aa, analog = True)
            z, p, k = ss.cheby2(N, self.aa, Wn, btype='low', analog=True, output='zpk')        

        elif self.approx == "ellip":
            N, Wn = ss.ellipord(self.fp * 2 * pi, self.fa * 2 * pi, self.ap, self.aa, analog = True)
            z, p, k = ss.ellip(N, self.ap, self.aa, Wn, btype='low', analog=True, output='zpk')         

        else:
            pass

        return ss.ZerosPolesGain(z,p,k)


filtro = Filter()

filtro.updateFilter(fp=1e3, ap=3, fa=2e3, aa=40, approx="cheby2")
'''
w, mag, phase = filtro.getBode()
plt.figure()
plt.semilogx(w/(2*pi), mag)    # Bode magnitude plot
plt.figure()
plt.semilogx(w/(2*pi), phase)  # Bode phase plot
plt.show()
'''
t = np.linspace(0, 0.01, 1000)
y = np.append(np.zeros(10), np.ones(990))
y = np.cos(2*pi*1000*t) + np.cos(2*pi*1300*t + 1) 

t_out, y_out = filtro.getTempResponse(t, y)

fig, ax = plt.subplots()

ax.plot(t_out, y_out)
ax.plot(t, y)
plt.show()


