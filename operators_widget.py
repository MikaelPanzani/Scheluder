from PySide6.QtWidgets import QWidget, QTableWidget, QPushButton, QVBoxLayout, QTableWidgetItem
import os
from tools_function import loadUI, records_table_paser, dict_to_uiTable, sendQuery
from PySide6.QtGui import QIcon

class OperatorsWidget(QWidget):
    def __init__(self):
        super(OperatorsWidget, self).__init__()

        self.setWindowTitle("Operators Window")
        self.setGeometry(0, 0, 1850, 800)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"Operators.ui")

        # Find widgets in the loaded UI

        table_widget = self.findChild(QTableWidget, "table_op")
        if table_widget is None:
            print("Le table_widget table_op est introuvable")
        else:
            self.table_widget: QTableWidget = table_widget

        table_widget_skill = self.findChild(QTableWidget, "table_skill")
        if table_widget_skill is None:
            print("Le QTableWidget table_skill est introuvable")
        else:
            self.table_widget_skill: QTableWidget = table_widget_skill

        pushButton_attrib = self.findChild(QPushButton, "pushButton_attrib")
        if pushButton_attrib is None:
            print("Le QPushButton pushButton_attrib est introuvable")
        else:
            self.pushButton_attrib: QPushButton = pushButton_attrib

        skillASlot = self.findChild(QVBoxLayout, "verticalLayout_5")
        if skillASlot is None:
            print("Le QVBoxLayout verticalLayout_5 est introuvable")
        else:
            self.skillASlot: QVBoxLayout = skillASlot


        self.actualiser()



        if self.table_widget:
            self.table_widget.setColumnCount(2)
            self.table_widget.setHorizontalHeaderLabels(["ID", "Nom"])

            # Assuming records_table_paser and dict_to_uiTable are defined in tools_function
            dic_operators_data,cop = records_table_paser("Operators")
            dict_to_uiTable(dic_operators_data, self.table_widget)
        else :
            print("Pas d'op")

        if self.table_widget_skill:
            self.table_widget_skill.setColumnCount(2)
            self.table_widget_skill.setHorizontalHeaderLabels(["ID", "Nom"])

            # Assuming records_table_paser and dict_to_uiTable are defined in tools_function
            dic_operators_data,cop = records_table_paser("Skills")
            dict_to_uiTable(dic_operators_data, self.table_widget_skill)
        else :
            print("Pas de skills")

        self.pushButton_attrib.pressed.connect(lambda: sendQuery(self.getSelectedData_writeSQL()))
        self.pushButton_attrib.pressed.connect(lambda: OperatorsWidget.actualiser(self))
        

    def actualiser(self):
        if (self.skillASlot.count() == 2):
            self.skillASlot.removeWidget(self.table_widget_skillA)
        self.table_widget_skillA = QTableWidget()
        self.table_widget_skillA.setColumnCount(2)
        self.table_widget_skillA.setHorizontalHeaderLabels(["ID operator", "ID skill"])
        dic,casop = records_table_paser("SkillAssignments")
        dict_to_uiTable(dic, self.table_widget_skillA)
        self.skillASlot.addWidget(self.table_widget_skillA)

    def getSelectedData_writeSQL(self):
        #Je dois récupérer l'id des op et l'id des skill puis insert pour chaque couple
        listOp : list[QTableWidgetItem] = self.table_widget.selectedItems()
        listSkill : list[QTableWidgetItem] = self.table_widget_skill.selectedItems()
        sql : str = "INSERT INTO SkillAssignments (op_id, s_id) VALUES "
        if listOp and listSkill :
            for op in listOp:
                #Pour chaque opérateurs
                if (id_op_test := self.table_widget.item(op.row(), 0)) is None: print("Cellule introuvable")
                else: id_op: str = id_op_test.text()

                for s in listSkill:
                    #Pour chaque skill
                    if (item := self.table_widget_skill.item(s.row(), 0)) is None: print("Cellule introuvable dans table_widget_skill")
                    else: id_s: str = item.text()

                    sql_values = "("+str(id_op)+","+str(id_s)+"),"
                    sql += sql_values
            indiceLast = len(sql)-1
            sql = sql[:indiceLast] + ";"
        del listOp,listSkill
        return sql