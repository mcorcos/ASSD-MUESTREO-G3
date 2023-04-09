import numpy as np
from numpy import pi
import scipy.signal as ss
import matplotlib.pyplot as plt


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

    def getSampledSignal(self,y_in,t_in):
        sampledSignal=np.zeros(len(t_in))
        sampleT=1/self.fs
        timeInterval=t_in[1]-t_in[0]
        index=np.rint(sampleT/timeInterval)
        for i in range(len(t_in)):
            if i%(index)==0:
                sampledSignal[i]=y_in[i]
            else:
                sampledSignal[i]=sampledSignal[i-1]
        return [sampledSignal,t_in]

class AnalogSwitch:
    """
    analog Switch

    """
    def __init__(self):
        self.fs=1e3
        self.DC=0.5
        self.tau=self.DC*1/self.fs
        self.state=True


    def updateSwitch(self,DC,fs):
        self.fs=fs
        self.DC=DC

    def getResampleSignal(self,y_in,t_in):
        resampledSignal=np.zeros(len(t_in))
        turnOffT=1/self.fs
        timeInterval=t_in[1]-t_in[0]
        T_index=np.rint(turnOffT/timeInterval)
        DC_index=np.rint(turnOffT/timeInterval*self.DC)
        for i in range(len(t_in)):
            if (i%T_index)<DC_index:
                resampledSignal[i]=y_in[i]
            else:
                resampledSignal[i]=0
        return [resampledSignal,t_in]
        



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
        self.Node_1 = [0,0]
        self.Node_2 = [0,0]
        self.Node_3 = [0,0]
        self.Node_4 = [0,0]


    def updateStages(self, fp, ap, fa, aa, aprox, fs, DC):

        self.FAA.updateFilter(fp, ap, fa, aa, aprox)
        self.SH.updateSH(fs)
        self.AnalogSwitch.updateSwitch(DC, fs)
        self.FR.updateFilter(fp, ap, fa, aa, aprox)


    def updateSignals(self, y_in, t_in, checkList):
        
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

    """
    Signal getters
    """
    def getXin(self):
        return self.Xin
    
    def getNode_1(self):
        return self.Node_1
    
    def getNode_2(self):
        return self.Node_2
    
    def getNode_3(self):
        return self.Node_3
    
    def getNode_4(self):
        return self.Node_4