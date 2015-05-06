#encoding='utf-8'
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore, Qt
from asyncio.tasks import sleep
#from PyQt5 import QtCore as QtCore


class firstwindows(QtWidgets.QWidget):
    
    blue = []
    orange = []
    cyan = []
    
    def __init__(self):
        super(firstwindows, self).__init__()
        self.window_width = 750
        self.window_heigth = 600
        self.resize(self.window_width, self.window_heigth) 
        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        self.setMinimumSize(self.window_width, self.window_heigth);
        self.setMaximumSize(self.window_width, self.window_heigth);
        self.setWindowTitle("Python SEA")
        
#         self.button_close = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img.close.png")), "", self)
#         self.button_mini = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img/mini.png")), "", self)
#         self.button_close.setGeometry(self.window_width - 30, 0, 30, 30)
#         self.button_mini.setGeometry(self.window_width - 60, 0, 30, 30)
#         self.button_close.setIconSize(Qt.QSize(30, 30))
#         self.button_close.setStyleSheet("background-color:rgba(255, 255, 255, 100)")
#         self.button_mini.setIconSize(Qt.QSize(30, 30))
#         self.button_mini.setStyleSheet("background-color:rgba(255, 255, 255, 100)")
#         self.scrollbar = QtWidgets.QScrollBar(0x1, self)
#         self.scrollbar.setGeometry(0, self.window_heigth - 15, self.window_width, 15)
#         self.scrollbar.setRange(0, 99)
#         self.scrollbar.setPageStep(10)
#         self.scrollbar.setSingleStep(1)
#         self.scroll(0, 1)
                                  
    #通过调用这个函数可以完成窗口布局的设置     
    def SetWindow(self): 
        self.__setbackgroup()
        self.__setWindowLayout()
        self.__CreatArrow(500)
        self.__CreatComboBox()
        self.__CreatLineEdit()
        
    def __setbackgroup(self):
        pltt = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QPixmap('../img/backgroup.jpg'))
        pltt.setBrush(self.backgroundRole(), brush)
        self.setPalette(pltt)
     
    #用这个函数可以创建自己的按钮
    #r, g, b三个参数必须为整型参数
    def __CreateButton(self, r, g, b):
        button = QtWidgets.QPushButton("", self)
        rgb = "rgb({0}, {1}, {2})".format(r, g, b) 
        button.setStyleSheet("background-color: " + rgb)   
        return button
    
    #这里暂时做出了下拉框，但是布局还调整好，先留个坑~
    def __CreatComboBox(self):
        origin = []
        origin.append(self.__GetOrigin_X())
        origin.append(self.__GetOrigin_Y())
        
        self.comboBox_filter = QtWidgets.QComboBox(self)
        self.comboBox_width = 80
        self.comboBox_height = 20
        self.comboBox_filter.resize(self.comboBox_width, self.comboBox_height)
        self.comboBox_filter.addItem("语言", userData=None)
        self.comboBox_filter.addItem("框架", userData=None)
        self.comboBox_filter.addItem("类型", userData=None)
        self.comboBox_filter.setGeometry(20, origin[1] + 10, self.comboBox_width, self.comboBox_height)
        
        self.comboBox_color = QtWidgets.QComboBox(self)
        self.comboBox_color.resize(self.comboBox_width, self.comboBox_height)
        self.comboBox_color.addItem("彩色", userData=None)
        self.comboBox_color.addItem("蓝色", userData=None)
        self.comboBox_color.addItem("橙色", userData=None)
        self.comboBox_color.addItem("青色", userData=None)
        self.comboBox_color.setGeometry(20 * 2 + self.comboBox_width, origin[1] + 10, self.comboBox_width, self.comboBox_height)
     
    #创建输入栏，输入柱状图种的柱子的宽度
    def __CreatLineEdit(self):    
        origin = []
        origin.append(self.__GetOrigin_X())
        origin.append(self.__GetOrigin_Y())
        
        histogramsize_width = 300
        histogramsize_heigth = 20
        self.histogramsize = QtWidgets.QLineEdit("设置柱状图的宽度：数值只能在10~100之间", self)
        self.histogramsize.setGeometry(20 * 3 + self.comboBox_width * 2, origin[1] + 10, histogramsize_width, histogramsize_heigth)
        self.histogramsize.setStyleSheet("background-color:rgba(255, 255, 255, 255)")
    #下拉框设置部分代码结束
    
    #创建柱状图，参数尚未确定呢，待定的代码
    def __CreatHistogram(self, count  = 0, width = 0):
        pass
    
    #这个函数使用来设置坐标轴的，一般情况下heigth是固定的
    def __CreatArrow(self, width = 0, heigth = 450):
        origin = []
        origin.append(self.__GetOrigin_X())
        origin.append(self.__GetOrigin_Y())
        self.Arrow = QtWidgets.QWidget(self)
        self.Arrow.setMinimumSize(self.window_width - origin[0], heigth);
        self.Arrow.setStyleSheet("background-color:rgba(255, 255, 255, 255)")
        if width < self.window_width - origin[0]:
            width = self.window_width - origin[0]
        
        self.scrollarea = QtWidgets.QScrollArea(self);
        self.scrollarea.setWidget(self.Arrow)
        self.scrollarea.setGeometry(self.__GetOrigin_X(), self.__GetOrigin_Top(), width, heigth)
        self.scrollarea.setWidgetResizable(True)
        #self.scrollarea.setHorizontalScrollBarPolicy(Qt.QAbstractScrollArea.verticalScrollBar()) 
             
        self.hline = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img/horizentalarrow.png")), "", self.Arrow)
        self.hline.setGeometry(0, heigth-5, width, 5)
        self.hline.setIconSize(Qt.QSize(width, 5))
        self.hline.setStyleSheet("background-color:rgba(0, 0, 0, 255)")
        
        self.vline = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img/verticalarrow.png")), "", self.Arrow)
        self.vline.setGeometry(0, 0, 5, heigth)
        self.vline.setIconSize(Qt.QSize(5, heigth))
        self.vline.setStyleSheet("background-color:rgba(0, 0, 0, 255)")
        
    def __GetOrigin_X(self):    
        rect = QtCore.QRect(self.label.geometry())
        return rect.right() + 5
    
    def __GetOrigin_Y(self):
        rect = QtCore.QRect(self.label.geometry())
        return rect.top() +  450
    def __GetOrigin_Top(self):
        rect = QtCore.QRect(self.label.geometry())
        return rect.top()
    
    def __setWindowLayout(self):
        #这是柱状图
        self.label = QtWidgets.QLabel('1000',self)
        self.label.setGeometry(20, 90, 10, 10)
        self.label.adjustSize()            
        self.spacing = 10

def mainwindows():
    app = QtWidgets.QApplication(sys.argv)
    new = firstwindows()
    new.SetWindow()
    new.show()
    sys.exit(app.exec_())