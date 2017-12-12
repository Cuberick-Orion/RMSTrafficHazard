from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys
import pandas as pd
import numpy as np


class Window(QWidget):
    def __init__(self,df1,df2, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle('DataFrame Viewer')
        self.resize(1500, 800)
        self.tableWidget1 = QTableWidget()
        self.tableWidget2 = QTableWidget()

        self.tableWidget1.setRowCount(len(df1.columns))
        self.tableWidget2.setRowCount(len(df2.columns))
        self.tableWidget1.setColumnCount(len(df1.index))
        self.tableWidget2.setColumnCount(len(df2.index))
        self.tableWidget1.resize(300,800)

        layout = QHBoxLayout(self)
        layout.addWidget(self.tableWidget1)
        layout.addWidget(self.tableWidget2)

        self.setLayout(layout)

        # set label
        self.tableWidget1.setVerticalHeaderLabels(df1.columns.tolist())
        self.tableWidget1.setHorizontalHeaderLabels(QStringList(df1.index.format()))
        self.tableWidget2.setHorizontalHeaderLabels(df2.columns.tolist())

        # set data
        print 'Generating table...'
        for i in range(len(df1.index)):
            for j in range(len(df1.columns)):
                self.tableWidget1.setItem(i,j,QTableWidgetItem( str(df1.iloc[i][j]) ))

        print 'Generating table...'
        for i in range(len(df2.index)):
            for j in range(len(df2.columns)):
                self.tableWidget2.setItem(i,j,QTableWidgetItem( str(df2.iloc[i][j]) ))

        # self.sliderBar1 = self.tableWidget1.verticalScrollBar()
        # self.sliderBar2 = self.tableWidget2.verticalScrollBar()

        # QObject.connect(self.sliderBar1, SIGNAL("actionTriggered(int)"), self.SyncScroll)


# class Table(QTableWidget):

#     def __init__(self,df1,df2):

#         QMainWindow.__init__(self)
#         self.setWindowTitle('DataFrame Viewer')
#         self.resize(1500, 800)
#         self.setRowCount(len(df.columns))
#         self.setColumnCount(len(df.index))

#         self.table = QTableWidget()
#         self.tableItem = QTableWidgetItem()

#         # set label
#         self.setHorizontalHeaderLabels(df.columns.tolist())
        
        
#         # set data
#         print 'Generating table...'
#         for i in range(len(df.index)):
#             for j in range(len(df.columns)):
#                 self.setItem(i,j,QTableWidgetItem( str(df.iloc[i][j]) ))

 
def main(df1,df2):
    # app2 = QApplication(sys.argv)
    # gui = Table(df)
    # gui.show()
    w = Window(df1,df2)
    w.show()
    sys.exit(app.exec_())
    
def main_lone(df1,df2):
    app = QApplication(sys.argv)
    w = Window(df1,df2)
    w.show()
    # gui = Table(df)
    # gui.show()
    app.exec_()
    # sys.exit(app.exec_())

if __name__=="__main__":
    dfa = pd.DataFrame(np.random.randn(5,2), columns=list('AB'))
    
    # print df1
    main_lone(dfa,dfa)
    