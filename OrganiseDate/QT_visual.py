from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys
import pandas as pd
import numpy as np

class Table(QTableWidget):

    def __init__(self,df):

        QMainWindow.__init__(self)
        self.setWindowTitle('DataFrame Viewer')
        self.resize(1500, 800)
        self.setRowCount(len(df.columns))
        self.setColumnCount(len(df.index))

        self.table = QTableWidget()
        self.tableItem = QTableWidgetItem()

        # set label
        self.setHorizontalHeaderLabels(df.columns.tolist())
        # table.setVerticalHeaderLabels(QString("V1;V2;V3;V4").split(";"))
        
        # set data
        print 'Generating table...'
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.setItem(i,j,QTableWidgetItem( str(df.iloc[i][j]) ))

 
def main(df):
    # app = QApplication(sys.argv)
    gui = Table(df)
    gui.show()
    # app.exec_()
    
def main_separate(df):
    app = QApplication(sys.argv)
    gui = Table(df)
    gui.show()
    app.exec_()

if __name__=="__main__":
    df1 = pd.DataFrame(np.random.randn(5,2), columns=list('AB'))
    # print df1
    main_separate(df1)