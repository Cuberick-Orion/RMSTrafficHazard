from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys
import pandas as pd
import numpy as np
from datetime import datetime, date


class Window(QWidget):
    def __init__(self,date,df1,df2, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle("Event Viewer " + date.strftime('%m/%d/%Y'))
        self.resize(1500, 800)

        layout = QHBoxLayout(self)
        if len(df1.columns) != 0:
            self.tableWidget1 = QTableWidget()
            self.tableWidget1.setRowCount(len(df1.columns))
            self.tableWidget1.setColumnCount(len(df1.index))
            layout.addWidget(self.tableWidget1)

            self.tableWidget1.setVerticalHeaderLabels(df1.columns.tolist())
            self.tableWidget1.setHorizontalHeaderLabels(QStringList(df1.index.format()))

            print 'Generating table...'
            for i in range(len(df1.index)):
                for j in range(len(df1.columns)):
                    self.tableWidget1.setItem(i,j,QTableWidgetItem( str(df1.iloc[i][j]) ))

        else:
            pass

        self.tableWidget2 = QTableWidget()
        self.tableWidget2.setRowCount(len(df2.columns))
        self.tableWidget2.setColumnCount(len(df2.index))
        
        layout.addWidget(self.tableWidget2)
        self.setLayout(layout)

        # set label
        self.tableWidget2.setHorizontalHeaderLabels(df2.columns.tolist())

        # set data
        print 'Generating table...'
        for i in range(len(df2.index)):
            for j in range(len(df2.columns)):
                self.tableWidget2.setItem(i,j,QTableWidgetItem( str(df2.iloc[i][j]) ))
 
def main(date,df1,df2):
    w = Window(date,df1,df2)
    w.show()
    app.exec_()
    
def main_lone(date,df1,df2):
    app = QApplication(sys.argv)
    w = Window(date,df1,df2)
    w.show()
    app.exec_()

if __name__=="__main__":
    dfa = pd.DataFrame(np.random.randn(5,2), columns=list('AB'))
    datea = date(2017,1,1)
    main_lone(datea,dfa,dfa)
    