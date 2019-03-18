import csv
import pandas as pd
from PyQt5.QtGui import QIcon
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d,UnivariateSpline

from matplotlib.lines import Line2D      

tra=0
from PyQt5 import QtCore, QtGui, QtWidgets,Qt

col1=[]
col2=[]

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        
        self.setGeometry(0,0,300,200)
        self.layout = QtWidgets.QVBoxLayout()
        self.model = QtWidgets.QTableWidget(self)
        self.fileName=""
        self.leng=0
        self.row=0
        self.col=0
        self.tabnumber=2
        self.head=[]

        self.menubar = QtWidgets.QMenuBar()
        fileMenu = self.menubar.addMenu('File')
        
        impMenu = QtWidgets.QAction('load', self)
        impMenu.triggered.connect(self.on_pushButtonLoad_clicked)
        editMenu = QtWidgets.QAction('edit', self)
        editMenu.triggered.connect(self.on_pushButtonWrite_clicked)
        addmenu = QtWidgets.QAction('add row', self)
        addmenu.triggered.connect(self.on_pushButtonadd_clicked)
        selmenu = QtWidgets.QAction('sel', self)
        selmenu.triggered.connect(self.on_pushButtonsel_clicked)
        savemenu = QtWidgets.QAction('save as png', self)
        savemenu.triggered.connect(self.on_pushButtonsave_clicked)

        fileMenu.addAction(impMenu)
        fileMenu.addAction(addmenu)
        fileMenu.addAction(selmenu)
        fileMenu.addAction(editMenu)
        fileMenu.addAction(savemenu)

        self.tabs = QtWidgets.QTabWidget(self)
        tab_bar = QtWidgets.QTabBar(self.tabs)
        self.tab_1=QtWidgets.QWidget()
        self.tabs.addTab(self.tab_1,"tab1")
        self.tab_1.layout=QtWidgets.QVBoxLayout(self)
        self.tab_1.setLayout(self.tab_1.layout)
         
        self.pushButtonplot = QtWidgets.QPushButton(self)
        self.pushButtonplot.setText("plot scatter")
        self.pushButtonplot.clicked.connect(self.on_pushButtonplot_clicked)
        
        self.pushButtonplot1 = QtWidgets.QPushButton(self)
        self.pushButtonplot1.setText("plot line")
        self.pushButtonplot1.clicked.connect(self.on_pushButtonplot1_clicked)
        
        self.pushButtonplot2 = QtWidgets.QPushButton(self)
        self.pushButtonplot2.setText("plot scatter line")
        self.pushButtonplot2.clicked.connect(self.on_pushButtonplot2_clicked)

        self.layout.addWidget(self.pushButtonplot)
        self.layout.addWidget(self.pushButtonplot1)
        self.layout.addWidget(self.pushButtonplot2)
        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def loadCsv(self, fileName):
        fileInput=pd.read_csv(fileName,sep=',')
        self.head=list(fileInput.keys())
        self.model.setHorizontalHeaderLabels(list(fileInput.keys()))
        for i in range(len(fileInput)):
            self.row=len(fileInput)
            self.col=len(fileInput.keys())
            self.model.setRowCount(len(fileInput))
            self.model.setColumnCount(len(fileInput.keys()))
            for j in range(len(fileInput.keys())): 
                self.model.setItem(i,j,QtWidgets.QTableWidgetItem(str(fileInput[fileInput.columns[j]][i])))
                
        self.model.move(0,0)
        self.tab_1.layout.addWidget(self.model)
        
    def writeCsv(self, fileName):
        for r in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                r1 = self.model.item(r, column)
                r1.setFlags(r1.flags() & QtCore.Qt.ItemIsEditable)
        data = []
        for r in range(self.model.rowCount()):
            data.append([])
            for column in range(self.model.columnCount()):
                r1 = self.model.item(r, column)
                data[r].append(str(r1.data(0)))
        out = open(fileName, 'w')
        abc=csv.writer(out,delimiter=',')
        abc.writerow(self.head)
        abc.writerows(data)
        out.close()
                
    def adddata(self,fileName):
        self.row=self.row+1
        self.model.setRowCount(self.row)       
        
    def plotdata(self,fileName):
        tra=0
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1
        
    def plotdata1(self,fileName):
        tra=1
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas1(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1
        
    def plotdata2(self,fileName):
        tra=2
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas2(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1
   
    def seldata(self,fileName):
        rows=[]
        t=self.row
        t2=len(self.model.selectedItems())
        t3=int(t2/t)
        k=0
        for i in range(t3):
            rows.append([])
        for i in self.model.selectedItems():
            for j in range(t3):
                rows[j].append(float(i.data(0)))
         
    def savedata(self,fileName):
        if tra==0:
            PlotCanvas01(self, width=5, height=4)
        if tra==1:
            PlotCanvas11(self, width=5, height=4)
        if tra==21:
            PlotCanvas21(self, width=5, height=4)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        name = QtWidgets.QFileDialog.getOpenFileName()
        self.fileName=name[0]
        self.loadCsv(self.fileName)
        self.layout.addWidget(self.model)
    
    @QtCore.pyqtSlot()
    def on_pushButtonadd_clicked(self):
        self.adddata(self.fileName)
        
    @QtCore.pyqtSlot()
    def on_pushButtonplot_clicked(self):
        self.plotdata(self.fileName)
        
    @QtCore.pyqtSlot()
    def on_pushButtonplot1_clicked(self):
        self.plotdata1(self.fileName)
        
    @QtCore.pyqtSlot()
    def on_pushButtonplot2_clicked(self):
        self.plotdata2(self.fileName)
        
    @QtCore.pyqtSlot()
    def on_pushButtonsel_clicked(self):
        self.seldata(self.fileName)
        
    @QtCore.pyqtSlot()
    def on_pushButtonsave_clicked(self):
        self.savedata(self.fileName)
        
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        img=fig

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.scatter(self.data1,self.data2)
        ax.set_title('scatter')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()
        
class PlotCanvas01(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)  
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        fig.savefig('123.png')

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.scatter(self.data1,self.data2)
        ax.set_title('scatter')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()
        
class PlotCanvas1(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        img=fig

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.plot(self.data1,self.data2)
        ax.set_title('line')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()
        
class PlotCanvas11(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        fig.savefig('123.png')
        
    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.plot(self.data1,self.data2)
        ax.set_title('line')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()
        
class PlotCanvas2(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        img=fig
        
    def plot(self):
        ax = self.figure.add_subplot(111)
        c=sorted(self.data1)
        c1=sorted(self.data2)
        line=Line2D(c,c1)
        ax.add_line(line)
        ax.scatter(self.data1,self.data2)
        ax.set_title('scatter line')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()
        
class PlotCanvas21(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        fig.savefig('123.png')
        
    def plot(self):
        ax = self.figure.add_subplot(111)
        c=sorted(self.data1)
        c1=sorted(self.data2)
        line=Line2D(c,c1)
        ax.add_line(line)
        ax.scatter(self.data1,self.data2)
        ax.set_title('scatter line')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.draw()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    
    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
