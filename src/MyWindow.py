#devolver seniales 
import numpy as np
from numpy import pi
import scipy.signal as ss


# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox

# Project modules
from src.ui.mainwindow import Ui_MainWindow
from src.MPLClases import ScopePlot , TauPlot , MultipleViews
from src.cuentas import System

mul = {
    'Hz' : 1,
    'KHz' : 10**3,
    'MHz' : 10**6,
    'GHz' : 10**9,
    'THz' : 10**12
}

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # asigno una clase para los layouts

        self.Scope  = ScopePlot(self.scopePlot)

        self.Tau = TauPlot(self.layout_osc)

        self.multipleViews = MultipleViews(self.layout_views)

        self.system = System()

        self.N = 1
        self.T = 1
        

        # Eventos

        self.text_fs.textChanged.connect(self.changeSamplingDial)
        self.dial_fs.valueChanged.connect(self.changeSamplingText)
        
        self.text_duty.textChanged.connect(self.changeDutyDial)
        self.dial_duty.valueChanged.connect(self.changeDutyText)

        '''self.freq_xin.textChanged.connect(self.changeSignalSlider)
        self.freq_xinSlider.sliderMoved.connect(self.changeSignalText)'''

        self.check_FAA.stateChanged.connect(self.changeCheckBoxColor1)
        self.check_analogswitch.stateChanged.connect(self.changeCheckBoxColor2)
        self.check_fr.stateChanged.connect(self.changeCheckBoxColor3)
        self.check_sh.stateChanged.connect(self.changeCheckBoxColor4)
        self.XinSelect.currentIndexChanged.connect(self.changeSignalStackedWidget)


        # Botón de graficar 

        self.button_plot.clicked.connect(self.plotGraphs)
        self.button_plot_multiple.clicked.connect(self.plotMultipleGraphs)
 


## defino la funcion que me plotea en el scope 
# """ 
#     def plotScope(self):
#         node = self.getNode()
#         if node == 0:
#             value = self.system.getXin()
#         if node == 1:
#             value =self.system.getNode_1()
#         if node == 2:
#             value =self.system.getNode_2()
#         if node == 3:
#             value =self.system.getNode_3()
#         if node == 4:
#             value =self.system.getNode_4()

#         self.Scope.plot(value[0],value[1])
#         return

#  """

    """
    Eventos
    """
    def changeSamplingDial(self, freqValueText):
       freqT = int(np.round(self.strToFloat(freqValueText)))
       self.dial_fs.setValue(freqT)

    def changeSamplingText(self, freqValueDial):
        freqD = str(freqValueDial)
        self.text_fs.setText(freqD)

    def changeDutyDial(self,dutyValueText):
       dutyT = self.strToInt(dutyValueText) 
       self.dial_duty.setValue(dutyT)

    def changeDutyText(self, dutyValueDial): 
        dutyD = str(dutyValueDial)
        self.text_duty.setText(dutyD)

    '''def changeSignalSlider(self, signalText):
        signalT = self.strToInt(signalText)
        self.freq_xinSlider.setValue(signalT)

    def changeSignalText(self, signalSlider):
        signalS = str(signalSlider)
        self.freq_xin.setText(signalS)'''


    def changeCheckBoxColor1 (self):
        if (self.check_FAA.isChecked()):
            self.check_FAA.setStyleSheet("color: green")

        else: 
            self.check_FAA.setStyleSheet("color: red")

    def changeCheckBoxColor2 (self):
        if (self.check_analogswitch.isChecked()):
            self.check_analogswitch.setStyleSheet("color: green")

        else: 
            self.check_analogswitch.setStyleSheet("color: red")

    def changeCheckBoxColor3 (self):
        if (self.check_fr.isChecked()):
            self.check_fr.setStyleSheet("color: green")

        else: 
            self.check_fr.setStyleSheet("color: red")

    def changeCheckBoxColor4 (self):
        if (self.check_sh.isChecked()):
            self.check_sh.setStyleSheet("color: green")

        else: 
            self.check_sh.setStyleSheet("color: red")

    def strToInt(self, string):
        res = 0
        try:
            if string == '':
                res = 0
            else:
                res = int(string)

        except ValueError:
            res = 0
            self.warningNotFloat()

        return res
    
    def strToFloat(self, string):  #ver esto, por ahora es solo int
        res = 0
        try:
            if string == '':
                res = 0
            else:
                res = float(string)

        except ValueError:
            res = 0
            self.warningNotFloat()

        return res
    
    def warningNotFloat(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Ingrese un número valido")
        msgBox.setWindowTitle("Advertencia")
        msgBox.exec()
        return
    
    """

    Lo que pasa uando apretas el boton de graficar

    """     
    
    def plotMultipleGraphs(self):

        self.update()

        dut = self.strToFloat(self.text_duty.text()) / 100

        fs = self.strToFloat(self.text_fs.text()) * mul[self.mulBox1.currentText()]

        node_1 = self.combo_node_1.currentText()
        value_1 = [0,0]
        if node_1 == 'Xin':
            value_1 = self.system.getXinSignal()
        if node_1 == 'Node1':
            value_1 =self.system.getNode1Signal()
        if node_1 == 'Node2':
            value_1 =self.system.getNode2Signal()
        if node_1 == 'Node3':
            value_1 =self.system.getNode3Signal()
        if node_1 == 'Node4':
            value_1 =self.system.getNode4Signal()

        node_2 = self.combo_node_2.currentText()
        value_2 = [0,0]
        if node_2 == 'Xin':
            value_2 = self.system.getXinSignal()
        if node_2 == 'Node1':
            value_2 =self.system.getNode1Signal()
        if node_2 == 'Node2':
            value_2 =self.system.getNode2Signal()
        if node_2 == 'Node3':
            value_2 =self.system.getNode3Signal()
        if node_2 == 'Node4':
            value_2 =self.system.getNode4Signal()


        self.multipleViews.plot(value_1[0] , value_2[0] , value_1[1])
        self.Tau.plot(dut, fs)
        return

    # Grafica la señal marcada
    def plotGraphs(self):

        self.update()

        dut = self.strToFloat(self.text_duty.text()) / 100
        fs = self.strToFloat(self.text_fs.text()) * mul[self.mulBox1.currentText()]

        node = self.getNode()
        value = [0,0]
        if node == "Xin":
            value = self.system.getXinSignal()
            spectrum = self.system.getXinSpectrum()

        if node == "Node1":
            value =self.system.getNode1Signal()
            spectrum = self.system.getNode1Spectrum()
            
        if node == "Node2":
            value =self.system.getNode2Signal()
            spectrum = self.system.getNode2Spectrum()

        if node == "Node3":
            value =self.system.getNode3Signal()
            spectrum = self.system.getNode3Spectrum()

        if node == "Node4":
            value =self.system.getNode4Signal()
            spectrum = self.system.getNode4Spectrum()

        db = True

        if self.linealButton.isChecked():
            db = False

        self.Scope.plot(value[0], value[1], spectrum[0], spectrum[1], db)
        self.Tau.plot(dut, fs)

    # Update del sistema
    def update(self):
        y, t = self.getUserFunction()

        fp = self.strToFloat(self.fpValue.text())
        ap = self.strToFloat(self.apValue.text())
        fa = self.strToFloat(self.faValue.text())
        aa = self.strToFloat(self.aaValue.text())

        fs = self.strToFloat(self.text_fs.text()) * mul[self.mulBox1.currentText()]
        dut = self.strToFloat(self.text_duty.text()) / 100

        approx = "ellip"

        if self.filterTypeBox.currentText() == "Butter":
            approx = "butter"

        elif self.filterTypeBox.currentText() == "Cheby1":
            approx = "cheby1"

        elif self.filterTypeBox.currentText() == "Cheby2":
            approx = "cheby2"

        elif self.filterTypeBox.currentText() == "Cauer":
            approx = "ellip"

        else:
            print("Mismatch between filter types")

        self.system.updateStages(fp, ap, fa, aa, approx, fs, dut)

        self.system.updateSignals(y, t, self.N, self.T, self.getCheckList())



    def getCheckList(self):
        checklist = {"Filtro AA": self.check_FAA.isChecked() ,
                     "Sample and Hold": self.check_sh.isChecked(),
                     "Analog Switch":self.check_analogswitch.isChecked(),
                     "Filter":self.check_fr.isChecked()}
        return checklist
    


    def getNode(self):
                
        ##son los nodos , no checkbox
        NodeList = {

            "Xin": self.radio_Xin_1.isChecked(),
            "Node1": self.radio_node1_1.isChecked(), 
            "Node2": self.radio_node2_1.isChecked(),
            "Node3": self.radio_node3_1.isChecked(), 
            "Node4": self.radio_node4_1.isChecked(), 

        } 
        
        for index in NodeList:
            if(NodeList[index]):
                return index
            

    def getUserFunction(self):

        Nperiods = 20

        fb = self.strToFloat(self.signalFrequency.text()) * mul[self.mulBoxSignal_3.currentText()]
        A = self.strToFloat(self.signalAmplitude.text())
        pha = self.strToFloat(self.signalPhase.text())
        dut = self.strToFloat(self.signalDuty.text()) / 100
        off = self.strToFloat(self.signalOffset.text())

        # para AM
        fm = self.strToFloat(self.envelopeFreq.text()) * mul[self.mulBoxSignal_4.currentText()]
        fp = self.strToFloat(self.carrierFreq.text()) * mul[self.mulBoxSignal_5.currentText()]
        Amp = self.strToFloat(self.amAmplitude.text())
        m = self.strToFloat(self.modulationIndex.text())

        # Definimos un periodo de muestreo y cuánto tiempo se muestrea (ventana)
        self.N = 1000   # número de muestras por periodo
        T0 = 1/fb                   # periodo de la muestra
        self.T = T0 / self.N        # espaciado entre muestras

        # tomo Nperiods de la muestra
        t = np.linspace(0, self.T * self.N * Nperiods, self.N * Nperiods, endpoint=False)

        if self.XinSelect.currentText() == "Sin":
            y = A * np.sin(2 * np.pi * fb * t + pha) + off

        elif self.XinSelect.currentText() == "Square":
            y = A * ss.square(2 * np.pi * fb * t + pha, duty = dut) + off

        elif self.XinSelect.currentText() == "Triangle":
            y = A * ss.sawtooth(2 * np.pi * fb * t + pha, width = dut) + off

        elif self.XinSelect.currentText() == "Saw Tooth":
            y = A * ss.sawtooth(2 * np.pi * fb * t + pha, width = 1) + off

        elif self.XinSelect.currentText() == "AM":
            
            # Definimos un periodo de muestreo y cuánto tiempo se muestrea (ventana)
            T1 = 1/fm                   # periodo de la muestra de la moduladora
            self.T = T1 / self.N        # espaciado entre muestras

            # tomo Nperiods de la muestra
            t = np.linspace(0, self.T * self.N * Nperiods, self.N * Nperiods, endpoint=False)

            y = (1 + m * np.cos(2 * np.pi * fm * t)) * Amp * np.cos(2 * np.pi * fp * t)

        elif self.XinSelect.currentText() == "Incomplete Sine":
            y = np.zeros(len(t))
            for i in range(len(y)):
                y[i] = self.senoPartidoPeriodico(t[i], 3/2 *fb, 1/fb, A)

        else:
            print("Mismatch between signals")

        return y, t
    
    def changeSignalStackedWidget(self, index):
        if index == 4:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)

    def periodicf(self, li,lf,f,x,freq, a,Amp):
        if x>=li and x<=lf :
            return f(x,freq,a,Amp)
        elif x>lf:
            x_new=x-(lf-li)
            return self.periodicf(li,lf,f,x_new, freq, a, Amp)
        elif x<(li):
            x_new=x+(lf-li)
            return self.periodicf(li,lf,f,x_new, freq, a, Amp)
        
    def senoPartido(self, x, freq, a, Amp):
        if x < -0 or x > a:
            return 0
        else:
            return Amp * np.sin(2*np.pi*freq*x)
        
    def senoPartidoPeriodico(self, x, freq, a, Amp):
        return self.periodicf(0, a, self.senoPartido, x, freq, a, Amp)
