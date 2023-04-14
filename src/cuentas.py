import numpy as np
from numpy import pi
import scipy.signal as ss
import scipy.fft as fft


class Filter:
    """
    Filter:

    
    """
    def __init__(self):

        self.transferFunc = ss.ZerosPolesGain([], [1], 1)

        self.fp = 1e3
        self.ap = 3

        self.fa = 2e3
        self.aa = 40

        self.approx = "cheby2"      # [butter, cheby1, cheby2, ellip]

        self.N = 1000               # cantidad de muestras por periodo
        self.T = 1/1000

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
    
    def getTempResponse(self, y,t):
        t_out, y_out, x_out = ss.lsim(self.transferFunc, y, t)
        return [y_out, t_out]


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



class SampleAndHold:
    """
    sampleAndHold:

    
    """
    def __init__(self):
        self.fs=1e3

    def updateSH(self, fs):
        self.fs = fs

    def getSampledSignal(self, y_in, t_in):
        sampledSignal = np.zeros(len(t_in))
        sampleT = 1 / self.fs
        timeInterval = t_in[1] - t_in[0]
        index = np.rint(sampleT / timeInterval)
        for i in range(len(t_in)):
            if i % (index) == 0:
                sampledSignal[i] = y_in[i]
            else:
                sampledSignal[i] = sampledSignal[i-1]
        return [sampledSignal, t_in]

class AnalogSwitch:
    """
    analog Switch

    """
    def __init__(self):
        self.fs = 1e3
        self.DC = 0.5
        self.tau = self.DC*1/self.fs
        self.state = True


    def updateSwitch(self,DC,fs):
        self.fs = fs
        self.DC = DC

    def getResampleSignal(self,y_in,t_in):
        resampledSignal = np.zeros(len(t_in))
        turnOffT = 1 / self.fs
        timeInterval = t_in[1] - t_in[0]
        T_index = np.rint(turnOffT / timeInterval)
        DC_index = np.rint(turnOffT / timeInterval*self.DC)
        for i in range(len(t_in)):
            if (i % T_index) < DC_index:
                resampledSignal[i] = y_in[i]
            else:
                resampledSignal[i] =  0
        return [resampledSignal, t_in]
        


class System:
    """
    System
    """
    def __init__(self):
        
        self.FAA = Filter()
        self.SH = SampleAndHold()
        self.AnalogSwitch = AnalogSwitch()
        self.FR = Filter()


        self.Xin = [0,0]
        self.XinSpectrum = [0,0]

        self.Node_1 = [0,0]
        self.Node_1_Spectrum = [0,0]

        self.Node_2 = [0,0]
        self.Node_2_Spectrum = [0,0]

        self.Node_3 = [0,0]
        self.Node_3_Spectrum = [0,0]

        self.Node_4 = [0,0]
        self.Node_4_Spectrum = [0,0]


    def updateStages(self, fp, ap, fa, aa, aprox, fs, DC):

        self.FAA.updateFilter(fp, ap, fa, aa, aprox)
        self.SH.updateSH(fs)
        self.AnalogSwitch.updateSwitch(DC, fs)
        self.FR.updateFilter(fp, ap, fa, aa, aprox)


    # Actualiza las señales en cada nodo
    def updateSignals(self, y_in, t_in, N, T, checkList):
        
        self.Xin = [y_in, t_in]


        if checkList["Filtro AA"]:
            self.Node_1= self.FAA.getTempResponse(self.Xin[0], self.Xin[1])
        else:
            self.Node_1 = self.Xin


        if checkList["Sample and Hold"]:
            self.Node_2= self.SH.getSampledSignal( self.Node_1[0],self.Node_1[1])
        else:
            self.Node_2 = self.Node_1


        if checkList["Analog Switch"]:
            self.Node_3= self.AnalogSwitch.getResampleSignal( self.Node_2[0],self.Node_2[1])
        else:
            self.Node_3 = self.Node_2


        if checkList["Filter"]:
            self.Node_4= self.FR.getTempResponse( self.Node_3[0],self.Node_3[1])
        else:
            self.Node_4 = self.Node_3

        self.updateSpectrums(N, T)

    # Actualiza los espectros
    def updateSpectrums(self, N, T):
        # tengo que tomar un periodo de la señal
        # T0 = N * T    es el periodo de la señal

        self.N = N
        self.T = T

        y, t = (self.Xin[0][-N:], self.Xin[1][-N:])
        yf = fft.fft(y)
        self.XinSpectrum[1] = fft.fftfreq(N, T)[:N//2]
        self.XinSpectrum[0] = 2.0/N * np.abs(yf[0:N//2])

        y, t = (self.Node_1[0][-N:], self.Node_1[1][-N:])
        yf = fft.fft(y)
        self.Node_1_Spectrum[1] = fft.fftfreq(N, T)[:N//2]
        self.Node_1_Spectrum[0] = 2.0/N * np.abs(yf[0:N//2])

        y, t = (self.Node_2[0][-N:], self.Node_2[1][-N:])
        yf = fft.fft(y)
        self.Node_2_Spectrum[1] = fft.fftfreq(N, T)[:N//2]
        self.Node_2_Spectrum[0] = 2.0/N * np.abs(yf[0:N//2])

        y, t = (self.Node_3[0][-N:], self.Node_3[1][-N:])
        yf = fft.fft(y)
        self.Node_3_Spectrum[1] = fft.fftfreq(N, T)[:N//2]
        self.Node_3_Spectrum[0] = 2.0/N * np.abs(yf[0:N//2])

        y, t = (self.Node_4[0][-N:], self.Node_4[1][-N:])
        yf = fft.fft(y)
        self.Node_4_Spectrum[1] = fft.fftfreq(N, T)[:N//2]
        self.Node_4_Spectrum[0] = 2.0/N * np.abs(yf[0:N//2])

    """
    Signal getters
    """
    def getXinSignal(self):
        return (self.Xin[0][-5 * self.N:], self.Xin[1][-5 *self.N:])
    
    def getNode1Signal(self):
        return (self.Node_1[0][-5 * self.N:], self.Node_1[1][-5 *self.N:])
    
    def getNode2Signal(self):
        return (self.Node_2[0][-5 * self.N:], self.Node_2[1][-5 *self.N:])
    
    def getNode3Signal(self):
        return (self.Node_3[0][-5 * self.N:], self.Node_3[1][-5 *self.N:])
    
    def getNode4Signal(self):
        return (self.Node_4[0][-5 * self.N:], self.Node_4[1][-5 *self.N:])
    
    def getXinSpectrum(self):
        return self.XinSpectrum
    
    def getNode1Spectrum(self):
        return self.Node_1_Spectrum
    
    def getNode2Spectrum(self):
        return self.Node_2_Spectrum
    
    def getNode3Spectrum(self):
        return self.Node_3_Spectrum
    
    def getNode4Spectrum(self):
        return self.Node_4_Spectrum