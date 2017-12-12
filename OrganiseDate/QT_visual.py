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
        
        
        # set data
        print 'Generating table...'
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.setItem(i,j,QTableWidgetItem( str(df.iloc[i][j]) ))

 
def main(df):
    # app2 = QApplication(sys.argv)
    gui = Table(df)
    gui.show()
    sys.exit(app.exec_())
    
def main_lone(df):
    app = QApplication(sys.argv)
    gui = Table(df)
    gui.show()
    app.exec_()
    # sys.exit(app.exec_())

if __name__=="__main__":
    df1 = pd.DataFrame(np.random.randn(5,2), columns=list('AB'))
    
    # print df1
    main_lone(df1)
    