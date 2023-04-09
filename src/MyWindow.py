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

        node_1 = self.combo_node_1.currentText()
        value_1 = [0,0]
        if node_1 == 'Xin':
            value_1 = self.system.getXin()
        if node_1 == 'Node1':
            value_1 =self.system.getNode_1()
        if node_1 == 'Node2':
            value_1 =self.system.getNode_2()
        if node_1 == 'Node3':
            value_1 =self.system.getNode_3()
        if node_1 == 'Node4':
            value_1 =self.system.getNode_4()

        node_2 = self.combo_node_2.currentText()
        value_2 = [0,0]
        if node_2 == 'Xin':
            value_2 = self.system.getXin()
        if node_2 == 'Node1':
            value_2 =self.system.getNode_1()
        if node_2 == 'Node2':
            value_2 =self.system.getNode_2()
        if node_2 == 'Node3':
            value_2 =self.system.getNode_3()
        if node_2 == 'Node4':
            value_2 =self.system.getNode_4()


        self.multipleViews.plot(value_1[0] , value_2[0] , value_1[1])
        self.Tau.plot(dut)
        return



    def plotGraphs(self):

        self.update()

        dut = self.strToFloat(self.text_duty.text()) / 100

        node = self.getNode()
        value = [0,0]
        if node == "Xin":
            value = self.system.getXin()
        if node == "Node1":
            value =self.system.getNode_1()
        if node == "Node2":
            value =self.system.getNode_2()
        if node == "Node3":
            value =self.system.getNode_3()
        if node == "Node4":
            value =self.system.getNode_4()

        

        self.Scope.plot(value[0], value[1])
        self.Tau.plot(dut)

    def update(self):
        y, t = self.getUserFunction()

        fp = 20e3
        ap = 1
        fa = 2*fp
        aa = 40

        fs = self.strToFloat(self.text_fs.text()) * mul[self.mulBox1.currentText()]
        dut = self.strToFloat(self.text_duty.text()) / 100

        self.system.updateStages(fp, ap, fa, aa, "ellip", fs, dut)

        self.system.updateSignals(y, t, self.getCheckList())



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

        Nperiods = 10

        fb = self.strToFloat(self.signalFrequency.text()) * mul[self.mulBoxSignal_3.currentText()]
        A = self.strToFloat(self.signalAmplitude.text())
        pha = self.strToFloat(self.signalPhase.text())
        dut = self.strToFloat(self.signalDuty.text()) / 100
        off = self.strToFloat(self.signalOffset.text())

        t = np.linspace(0, Nperiods*1/fb, 1000)

        if self.XinSelect.currentText() == "Sin":
            y = A * np.sin(2 * np.pi * fb * t + pha) + off

        elif self.XinSelect.currentText() == "Square":
            y = A * ss.square(2 * np.pi * fb * t + pha, duty = dut) + off

        elif self.XinSelect.currentText() == "Triangle":
            y = A * ss.sawtooth(2 * np.pi * fb * t + pha, width = dut) + off

        elif self.XinSelect.currentText() == "Saw Tooth":
            y = A * ss.sawtooth(2 * np.pi * fb * t + pha, width = 1) + off

        else:
            print("Mismatch between signals")

        return y, t