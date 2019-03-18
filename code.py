import csv
import pandas as pd
from PyQt5.QtGui import QIcon
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d,UnivariateSpline

from matplotlib.lines import Line2D      



from PyQt5 import QtCore, QtGui, QtWidgets

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
        self.img=plt
        

        #self.tableView = QtWidgets.QTableView(self)
        
        
        #self.tableView.setModel(self.model)
        #self.tableView.horizontalHeader().setStretchLastSection(True)
        
        self.menubar = QtWidgets.QMenuBar()
        fileMenu = self.menubar.addMenu('File')
        
        impMenu = QtWidgets.QAction('load', self)
        impMenu.triggered.connect(self.on_pushButtonLoad_clicked)
        editMenu = QtWidgets.QAction('edit', self)
        editMenu.triggered.connect(self.on_pushButtonWrite_clicked)
        addmenu = QtWidgets.QAction('add row', self)
        addmenu.triggered.connect(self.on_pushButtonadd_clicked)
        plotmenu = QtWidgets.QAction('plot scatter', self)
        plotmenu.triggered.connect(self.on_pushButtonplot_clicked)
        plotmenu1 = QtWidgets.QAction('plot lines', self)
        plotmenu1.triggered.connect(self.on_pushButtonplot1_clicked)
        plotmenu2 = QtWidgets.QAction('plot scatter1', self)
        plotmenu2.triggered.connect(self.on_pushButtonplot2_clicked)
        selmenu = QtWidgets.QAction('sel', self)
        selmenu.triggered.connect(self.on_pushButtonsel_clicked)
        savemenu = QtWidgets.QAction('save as png', self)
        savemenu.triggered.connect(self.on_pushButtonsave_clicked)
        #impAct = QAction('Import mail', self) 
        #impMenu.addAction(impAct)
        
        #newAct = QAction('New', self)        
        
        #fileMenu.addAction(newAct)
        fileMenu.addAction(impMenu)
        fileMenu.addAction(addmenu)
        fileMenu.addAction(plotmenu)
        fileMenu.addAction(plotmenu1)
        fileMenu.addAction(plotmenu2)

        fileMenu.addAction(selmenu)
        fileMenu.addAction(editMenu)
        fileMenu.addAction(savemenu)

        
        self.tabs = QtWidgets.QTabWidget(self)
        tab_bar = QtWidgets.QTabBar(self.tabs)
        self.tab_1=QtWidgets.QWidget()
        

        
        
        #self.tab_1=tab_bar.addTab("Main")
        #self.tab_2 = tab_bar.addTab("Description")
        self.tabs.addTab(self.tab_1,"tab1")

        self.tab_1.layout=QtWidgets.QVBoxLayout(self)
        self.tab_1.setLayout(self.tab_1.layout)
        
        
                

        
        
        #self.model.setMaximumWidth(1000);
        #self.model.setMinimumWidth(1000);
        #self.model.setMaximumHeight(1000);
        #self.model.setMinimumHeight(1000); 
        

        #self.pushButtonLoad = QtWidgets.QPushButton(self)
        #self.pushButtonLoad.setText("Load Csv File!")
        #self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        #self.pushButtonWrite = QtWidgets.QPushButton(self)
        #self.pushButtonWrite.setText("Write Csv File!")
        #self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        
        #self.pushButtonadd = QtWidgets.QPushButton(self)
        #self.pushButtonadd.setText("add data!")
        #self.pushButtonadd.clicked.connect(self.on_pushButtonadd_clicked)
        
        #self.pushButtonplot = QtWidgets.QPushButton(self)
        #self.pushButtonplot.setText("plot selected data!")
        #self.pushButtonplot.clicked.connect(self.on_pushButtonplot_clicked)

        
        #self.layoutVertical.add
        #self.layout.addWidget(self.pushButtonWrite)
        #self.layout.addWidget(self.pushButtonadd)
        self.layout.addWidget(self.menubar)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        #self.layoutVertical.addWidget(self.pushButtonplot)



    def loadCsv(self, fileName):
        fileInput=pd.read_csv(fileName)
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
                r1.setFlags(r1.flags() & Qt.ItemIsEditable)
        data = []
        for r in range(self.model.rowCount()):
            data.append([])
            for column in range(self.model.columnCount()):
                r1 = self.model.item(r, column)
                data[r].append(float(r1.data(0)))
        out = open('out.csv', 'w')
        for r2 in data:
            for co in r2:
                out.write(co,delim=';')
            out.write('\n')
        out.close()
     #   with open(fileName, "w") as fileOutput:
      #      writer = csv.writer(fileOutput)
       #     for rowNumber in range(self.model.rowCount()):
        #        fields = [
         #           self.model.data(
          #              self.model.index(rowNumber, columnNumber),
           #             QtCore.Qt.DisplayRole
            #        )
             #       for columnNumber in range(self.model.columnCount())
              #  ]
               # writer.writerow(fields)
                
    def adddata(self,fileName):
        #it=[]
        self.row=self.row+1
        self.model.setRowCount(self.row)
        #for i in range(self.leng):
        #    it.append(QtWidgets.QTableWidgetItem(0))
        #self.model.insertRow(it)
        
        
    def plotdata(self,fileName):
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
        
        #fig = Figure(figsize=(5, 4), dpi=100)
        #self.axes = fig.add_subplot(111)
        #ax = FigureCanvas.figure.add_subplot(111)
        #ax.scatter(data1,data2)
        #ax.set_title('PyQt Matplotlib Example')
        #self.draw()
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1
        
    def plotdata1(self,fileName):
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
       
        #fig = Figure(figsize=(5, 4), dpi=100)
        #self.axes = fig.add_subplot(111)
        #ax = FigureCanvas.figure.add_subplot(111)
        #ax.scatter(data1,data2)
        #ax.set_title('PyQt Matplotlib Example')
        #self.draw()
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1
        
    def plotdata2(self,fileName):
        t=0
        for i in self.model.selectedItems():
            if t%2==0:
                col1.append(float(i.data(0)))
            else:
                col2.append(float(i.data(0)))
            t=t+1
        
        #fig = Figure(figsize=(5, 4), dpi=100)
        #self.axes = fig.add_subplot(111)
        #ax = FigureCanvas.figure.add_subplot(111)
        #ax.scatter(data1,data2)
        #ax.set_title('PyQt Matplotlib Example')
        #self.draw()
        tab_x=QtWidgets.QWidget()
        self.tabs.addTab(tab_x,'tab'+str(self.tabnumber))
        tab_x.layout=QtWidgets.QVBoxLayout(self)
        tab_x.setLayout(tab_x.layout)
        m = PlotCanvas(self, width=5, height=4)
        tab_x.layout.addWidget(m)
        self.tabnumber=self.tabnumber+1


        
                
        
    def seldata(self,fileName):
        rows=[]
        t=len(self.model)
        t2=len(self.model.selectedItems())
        t3=t/t2
        k=0
        for i in self.model.selectedItems():
            rows.append(float(i.data(0)))
        print(rows)
         
    def savedata(self,fileName):
        self.img.savefig('abc.png')
        

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
 
        #FigureCanvas.setSizePolicy(self,
        #        QSizePolicy.Expanding,
        #        QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        
 
 
    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.scatter(self.data1,self.data2)
        ax.set_title('scatter')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.img=ax
        self.draw()
        
class PlotCanvas1(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        #FigureCanvas.setSizePolicy(self,
        #        QSizePolicy.Expanding,
        #        QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        
 
 
    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.plot(self.data1,self.data2)
        ax.set_title('line')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        self.img=ax
        self.draw()
        
class PlotCanvas2(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        #FigureCanvas.setSizePolicy(self,
        #        QSizePolicy.Expanding,
        #        QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.data1=col1
        self.data2=col2
        self.plot()
        
 
 
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
        self.img=ax
        self.draw()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    
    

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
