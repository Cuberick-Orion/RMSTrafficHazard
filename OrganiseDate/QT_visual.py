import sys
from PyQt4 import QtGui, QtCore
import pandas as pd
import numpy as np
 
data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}
df = pd.DataFrame(np.random.randn(5,2), columns=list('AB'))

class MyTable(QtGui.QTableWidget):
    def __init__(self):
        QtGui.QTableWidget.__init__(self)
        # self.data = data
        # self.setmydata()
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        self.datatable = QtGui.QTableWidget(parent=self)
        self.datatable.setColumnCount(len(df.columns))
        self.datatable.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.datatable.setItem(i,j,QtGui.QTableWidgetItem(str(df.iget_value(i, j))))
 
    # def setmydata(self):
 
    #     horHeaders = []
    #     for n, key in enumerate(sorted(self.data.keys())):
    #         horHeaders.append(key)
    #         for m, item in enumerate(self.data[key]):
    #             newitem = QtGui.QTableWidgetItem(item)
    #             self.setItem(m, n, newitem)
    #     self.setHorizontalHeaderLabels(horHeaders)
 
def main():
    app = QtGui.QApplication(sys.argv)
    gui = MyTable()
    gui.show()
    app.exec_()
    # table = MyTable(data, 5, 3)
    # datatable.show()
    # sys.exit()
 
if __name__=="__main__":
    main()