import sys
from win import windows
from conductfile import CreateDirectory
from PyQt5 import QtWidgets
 
data = CreateDirectory()
app = QtWidgets.QApplication(sys.argv)    
win = windows()
win.SetWindow(len(data[0]), data[2])
win.show()
win.ReflushAxis(data, button_width = 100, spacing = 10)
win.ReflushInformationLabel(data = data)
sys.exit(app.exec_())
