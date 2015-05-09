import sys
from win import windows
from conductfile import CreateDirectory
from PyQt5 import QtWidgets
 
data = CreateDirectory()
app = QtWidgets.QApplication(sys.argv)    
win = windows()
win.SetWindow(len(data[0]), data[2])
win.show()
win.ReflushAxis(data, button_width = 50, spacing = 10)
sys.exit(app.exec_())
