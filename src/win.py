#encoding='utf-8'
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from conductdata import GetMostPopularLanguage, GetMostPopularSkillGroup
from conductfile import CreateDictionary, CreateDirectory
#from PyQt5 import QtCore as QtCore


class windows(QtWidgets.QWidget):
    
    blue    = [0, 160, 255]
    orange  = [255, 184, 18]
    cyan    = [188, 210, 50]
    red     = [251, 111, 32]
    color_list = {'blue'    : [0, 160, 255],
                  'orange'  : [255, 184, 18],
                  'cyan'    : [188, 210, 50],
                  'red'     : [251, 111, 32]
                  }
    
    def __init__(self):
        super(windows, self).__init__()
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
    def SetWindow(self, languagecount, count): 
        self.__setbackgroup()
        self.__setWindowLayout(languagecount = languagecount, count = count)
        self.comboBox_filter.currentIndexChanged.connect(self.__SlotCombox)
        self.relatedskill_lineedit.textChanged.connect(self.__SlotForLineedit)
        
        
    
    def ReflushAxis(self, data, button_width = 50, spacing = 50) :
        count = data[2]
        self.count_label.setText("{0}".format(count))
        self.count_label.adjustSize()
        self.__ReflushHistogram(data = data, button_width = button_width, spacing = spacing)
        
    def ReflushInformationLabel(self, data):
        self.__ReflushInformationLabel(data = data)
            
    def __setbackgroup(self):
        pltt = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QPixmap('../img/backgroup.jpg'))
        pltt.setBrush(self.backgroundRole(), brush)
        self.setPalette(pltt)
    #This function is used to create some label
    #to show the result
    def __CreateInformationLable(self):
        self.MPL_label = QtWidgets.QLabel("最受欢迎的语言", self)
        self.MPL_label.setGeometry(self.__GetOrigin_X(), self.__GetOrigin_Top() - 20, 20, 20)
        self.MPL_label.adjustSize()
        
        MPL_label_rect = QtCore.QRect(self.MPL_label.geometry())
        self.MPSG_lable = QtWidgets.QLabel("最佳技能组合", self)
        self.MPSG_lable.setGeometry(MPL_label_rect.right() + 20, MPL_label_rect.top(), 20, 20)
        self.MPSG_lable.adjustSize()
     
    #用这个函数可以创建自己的按钮
    #r, g, b三个参数必须为整型参数
    def __CreateButton(self, r, g, b):
        button = QtWidgets.QPushButton("", self.Axis)
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
        self.comboBox_filter.addItem("相关技能", userData=None)
        #self.comboBox_filter.addItem("类型", userData=None)
        self.comboBox_filter.setGeometry(20, origin[1] + 10, self.comboBox_width, self.comboBox_height)
        
#         self.comboBox_color = QtWidgets.QComboBox(self)
#         self.comboBox_color.resize(self.comboBox_width, self.comboBox_height)
#         self.comboBox_color.addItem("彩色", userData=None)
#         self.comboBox_color.addItem("蓝色", userData=None)
#         self.comboBox_color.addItem("橙色", userData=None)
#         self.comboBox_color.addItem("青色", userData=None)
#         self.comboBox_color.setGeometry(20 * 2 + self.comboBox_width, origin[1] + 10, self.comboBox_width, self.comboBox_height)
#      
    #创建输入栏，输入柱状图种的柱子的宽度
    def __CreatLineEdit(self):    
        origin = []
        origin.append(self.__GetOrigin_X())
        origin.append(self.__GetOrigin_Y())
        
        relatedskill_width = 300
        relatedskill_heigth = 20
        self.relatedskill_lineedit = QtWidgets.QLineEdit("查找与一门技能相关的其他技能", self)
        self.relatedskill_lineedit.setGeometry(20 * 3 + self.comboBox_width * 2, origin[1] + 10, relatedskill_width, relatedskill_heigth)
        self.relatedskill_lineedit.setStyleSheet("background-color:rgba(255, 255, 255, 255)")
        self.relatedskill_lineedit.setEnabled(False)
        
    #下拉框设置部分代码结束
    
    #初始化柱状图，参数尚未确定呢，待定的代码
    def __InitHistogram(self, languagecount = 0, button_width = 50, spacing = 50):
        self.button_list = []
        self.count_label_list  = []
        self.key_label_list = []
        color_count = len(self.color_list)
        hrect = QtCore.QRect(self.hline.geometry())
        self.hline_top = hrect.top()
        self.hline_bottom = hrect.bottom()
        for i in range(0, languagecount):
            if 0 == i % color_count :
                self.button_list.append(self.__CreateButton(self.color_list['blue'][0], 
                                                            self.color_list['blue'][1], 
                                                            self.color_list['blue'][2]))
            elif 1 == i % color_count :
                self.button_list.append(self.__CreateButton(self.color_list['orange'][0], 
                                                            self.color_list['orange'][1], 
                                                            self.color_list['orange'][2]))
            elif 2 == i % color_count :
                self.button_list.append(self.__CreateButton(self.color_list['cyan'][0], 
                                                            self.color_list['cyan'][1], 
                                                            self.color_list['cyan'][2]))
            elif 3 == i % color_count :
                self.button_list.append(self.__CreateButton(self.color_list['red'][0], 
                                                            self.color_list['red'][1], 
                                                            self.color_list['red'][2]))
            self.count_label_list.append(QtWidgets.QLabel("0", self.Axis))
            self.key_label_list.append(QtWidgets.QLabel("", self.Axis))
    
        button_heigth = 10
        for i in range(0, languagecount):
            self.button_list[i].setGeometry(spacing * (i + 1) + i * button_width, 
                                            self.hline_top - button_heigth, 
                                            button_width, 
                                            button_heigth)
            self.count_label_list[i].setGeometry(spacing * (i + 1) + i * button_width, 
                                            self.hline_top - button_heigth + 20, 
                                            button_width, 
                                            0)
            self.count_label_list[i].adjustSize()
            
            self.key_label_list[i].setGeometry(spacing * (i + 1) + i * button_width, 
                                            self.hline_bottom + 5, 
                                            button_width, 
                                            0)
            self.key_label_list[i].adjustSize()
            
        
#         button = self.__CreateButton(255, 255, 255)
#         button.setGeometry(spacing + 10, 10, self.button_width, 10)    
    #这个函数使用来设置坐标轴的，一般情况下heigth是固定的
    def __CreatAxis(self, button_width = 50, spacing = 50 , languagecount = 0, heigth = 430):
        origin = []
        origin.append(self.__GetOrigin_X())
        origin.append(self.__GetOrigin_Y())
        width = (spacing + button_width) * (languagecount + 1)

        if width < self.window_width - origin[0]:
            width = self.window_width - origin[0]
            
        self.Axis = QtWidgets.QWidget(self)
        self.Axis.setMinimumSize(width, heigth)
        self.Axis.setStyleSheet("background-color:rgba(255, 255, 255, 255)")
        
        self.scrollarea = QtWidgets.QScrollArea(self);
        self.scrollarea.setWidget(self.Axis)
        self.scrollarea.setGeometry(self.__GetOrigin_X(), self.__GetOrigin_Top(), self.window_width - origin[0], heigth + 20)#这里+20为纵坐标轴的高度加上水平滚动条的高度
        self.scrollarea.setWidgetResizable(True)
             
        self.hline = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img/horizentalarrow.png")), "", self.Axis)
        self.hline.setGeometry(0, heigth - 30, width, 5)
        #self.hline.setIconSize(Qt.QSize(width, 5))
        self.hline.setStyleSheet("background-color:rgba(0, 0, 0, 255)")
        
        self.vline = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap("../img/verticalarrow.png")), "", self.Axis)
        self.vline.setGeometry(0, 0, 5, heigth)
        #self.vline.setIconSize(Qt.QSize(5, heigth))
        self.vline.setStyleSheet("background-color:rgba(0, 0, 0, 255)")
        
        self.__InitHistogram(languagecount = languagecount, button_width = button_width, spacing = spacing)
        
    def __GetOrigin_X(self):    
        rect = QtCore.QRect(self.count_label.geometry())
        return rect.right() + 5
    
    def __GetOrigin_Y(self):
        rect = QtCore.QRect(self.count_label.geometry())
        return rect.top() +  450
    
    def __GetOrigin_Top(self):
        rect = QtCore.QRect(self.count_label.geometry())
        return rect.top()
    
    def __setWindowLayout(self, languagecount = 0, count = 0):
        #这是柱状图
        #self.languagecount = languagecount
        self.count_label = QtWidgets.QLabel('1000',self)
        self.count_label.setGeometry(20, 100, 10, 10)
        self.count_label.setText("{0}".format(count))
        self.count_label.adjustSize()
        self.__CreateInformationLable()            
        self.__CreatComboBox()
        self.__CreatAxis(languagecount = languagecount)
        self.__CreatLineEdit()
        
    def __ReflushHistogram(self, data, button_width = 50, spacing = 50):
        keyseq = data[0]
        keydirctory = data[1]
        keycount = len(keyseq)
        count = data[2]
        for i in range(0, keycount) :
            button_heigth = keydirctory[keyseq[i]] / count * self.hline_top
            self.button_list[i].setGeometry(spacing * (i + 1) + i * button_width,
                                            self.hline_top - button_heigth,
                                            button_width,
                                            button_heigth)
            
            self.count_label_list[i].setGeometry(spacing * (i + 1) + i * button_width,
                                            self.hline_top - button_heigth - 20,
                                            button_width,
                                            0)
            self.count_label_list[i].setText("{0}".format(keydirctory[keyseq[i]]))
            self.count_label_list[i].adjustSize()
            
            self.key_label_list[i].setGeometry(spacing * (i + 1) + i * button_width,
                                            self.hline_bottom + 5,
                                            button_width,
                                            0)
            self.key_label_list[i].setText("{0}".format(keyseq[i]))
            self.key_label_list[i].adjustSize()
            
            self.button_list[i].show()
            self.key_label_list[i].show()
            self.count_label_list[i].show()
            
        for i in range(keycount, len(self.button_list)) :
            self.button_list[i].hide()
            self.key_label_list[i].hide()
            self.count_label_list[i].hide()
    
    def __ReflushInformationLabel(self, data):
        self.MPL_label.setText("最受欢迎的语言为：{0}".format(str(GetMostPopularLanguage(data))))
        self.MPL_label.adjustSize()
        
        self.MPSG_lable.setText("最佳技能组合：{0}".format(str(GetMostPopularSkillGroup(data))))
        MPL_label_rect = QtCore.QRect(self.MPL_label.geometry())
        self.MPSG_lable.setGeometry(MPL_label_rect.right() + 20, MPL_label_rect.top(), 20, 20)
        self.MPSG_lable.adjustSize()
        
    def __SlotCombox(self, index):
        if 0 == index :
            self.ReflushAxis(data = CreateDirectory())
            self.relatedskill_lineedit.setText("查找与一门技能相关的其他技能")
            self.relatedskill_lineedit.setEnabled(False)
        elif 1 == index :
            self.relatedskill_lineedit.setEnabled(True)
            
        self.Axis.hide()
        self.Axis.show()
    
    def __SlotForLineedit(self, keyword):
        keyword = keyword.upper().replace(' ', '')
        data = CreateDictionary(keyword)
        self.__ReflushHistogram(data)
        self.count_label.setText("{0}".format(data[2]))