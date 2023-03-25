# PyQt5 modules
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox

# Project modules
from src.ui.mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

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
    

    
