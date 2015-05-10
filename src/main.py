import sys
from win import windows
from conductfile import CreateDirectory
from PyQt5 import QtWidgets
from GetCompsInfo import CGetCompsInfo
from Spider import CSpider

    ### get company 's url
    #spider = CSpider() 
    #spider.getAllCityUrl()
    #spider.getCitiesPage()
    #spider.downloadPages()
    
    ### get company 's information
    # comp = CGetCompsInfo()
    # comp.startThread()
    # comp.storeWebIndex() 
data = CreateDirectory()
app = QtWidgets.QApplication(sys.argv)    
win = windows()
win.SetWindow(len(data[0]), data[2])
win.ReflushAxis(data, button_width = 50, spacing = 50)
win.show()
win.ReflushInformationLabel(data = data)
sys.exit(app.exec_())
