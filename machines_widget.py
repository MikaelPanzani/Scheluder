from PySide6.QtWidgets import QWidget, QTableWidget
import os
from tools_function import loadUI, records_table_paser, dict_to_uiTable
from PySide6.QtGui import QIcon

class MachinesWidget(QWidget):
    def __init__(self):
        super(MachinesWidget, self).__init__()

        self.setWindowTitle("Moyens de production")
        self.setGeometry(0, 0, 1850, 800)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"machines.ui")

        # Find widgets in the loaded UI
        self.table_widget = self.findChild(QTableWidget,"table_machine")


        if self.table_widget:
            self.table_widget.setColumnCount(2)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Nom"])

            # Assuming records_table_paser and dict_to_uiTable are defined in tools_function
            dic_operators_data,cop = records_table_paser("Machines")
            dict_to_uiTable(dic_operators_data, self.table_widget)
        else :
            print("Pas de machines enregistrées...")
