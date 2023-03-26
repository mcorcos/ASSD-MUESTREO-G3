# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox

# Project modules
from src.ui.mainwindow import Ui_MainWindow
from src.MPLClases import ScopePlot
from src.cuentas import System

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        ##asigno una clase para los layouts

        self.Scope  = ScopePlot(self.layout_scopeTemp)
        self.system = System()






        self.text_fs.textChanged.connect(self.changeSamplingDial)
        self.dial_fs.valueChanged.connect(self.changeSamplingText)
        
        self.text_duty.textChanged.connect(self.changeDutyDial)
        self.dial_duty.valueChanged.connect(self.changeDutyText)

        self.freq_xin.textChanged.connect(self.changeSignalSlider)
        self.freq_xinSlider.sliderMoved.connect(self.changeSignalText)

        self.check_FAA.stateChanged.connect(self.changeCheckBoxColor1)
        self.check_analogswitch.stateChanged.connect(self.changeCheckBoxColor2)
        self.check_fr.stateChanged.connect(self.changeCheckBoxColor3)
        self.check_sh.stateChanged.connect(self.changeCheckBoxColor4)
 





## defino la funcion que me plotea en el scope 

    def plotScope(self):
        node = self.getNode()
        if node == 0:
            value = self.system.getXin()
        if node == 1:
            value =self.system.getNode_1()
        if node == 2:
            value =self.system.getNode_2()
        if node == 3:
            value =self.system.getNode_3()
        if node == 4:
            value =self.system.getNode_4()

        self.Scope.plot(value[0],value[1])
        return




    def changeSamplingDial(self,freqValueText):
       freqT = self.strToInt(freqValueText) 
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

    def changeSignalSlider(self, signalText):
        signalT = self.strToInt(signalText)
        self.freq_xinSlider.setValue(signalT)

    def changeSignalText(self, signalSlider):
        signalS = str(signalSlider)
        self.freq_xin.setText(signalS)


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
    

##    lo que pasa uando apretas el boton de graficar
    


    def plotButton(self):
        y,t = self.getUserFunction()
        self.system.updateSignals(y,t,self.getCheckList())
        return


    def getCheckList(self):
        checklist = {"Filtro AA": self.check_FAA.isChecked() ,
                     "Sample and Hold": self.check_sh.isChecked(),
                     "Analog Switch":self.check_analogswitch.isChecked(),
                     "Filter":self.check_fr.isChecked()}
        return checklist
    



    def getNode(self):
                
        ##son los nodos , no checkbox
        NodeList = {} 
        

        for index in NodeList:
            if(NodeList[index]):
                return index
            
def getUserFunction(self):


    return y,t