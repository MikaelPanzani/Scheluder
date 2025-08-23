from datetime import datetime, timedelta
from PySide6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableView
import os
from tools_function import loadUI
from PySide6.QtGui import QIcon, QBrush, QColor
from datetime import date
from tools_function import sendQuery, records_query_parser,dict_to_uiTable
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel

class StatWidget(QWidget):

    def __init__(self):
        super(StatWidget, self).__init__()

        self.setWindowTitle("Stat Window")
        self.setGeometry(0, 0, 1850, 800)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"stat.ui")

        #mappage
        tab_stat_slot = self.findChild(QVBoxLayout, "stat_slot")
        if tab_stat_slot is None: print("Le QVBoxLayout 'stat_slot' est introuvable")
        else: self.tabStat_slot: QVBoxLayout = tab_stat_slot

        stat_slot_pro_op = self.findChild(QVBoxLayout, "stat_slot_pro_op")
        if stat_slot_pro_op is None: print("Le QVBoxLayout 'stat_slot_pro_op' est introuvable")
        else: self.stat_slot_pro_op: QVBoxLayout = stat_slot_pro_op

        #Configurations
        self.tablist = []
        self.tabStat = QTableWidget()
        self.tablist.append(self.tabStat)
        self.tabStat_projet_operateur = QTableWidget()
        self.tablist.append(self.tabStat_projet_operateur)
        # Generate date range: 10 days before today to 50 days after
        pastcast = 9
        forecast = 51
        start_date = datetime.today() - timedelta(days=pastcast)
        end_date = datetime.today() + timedelta(days=forecast)
        
        total_days = (end_date - start_date).days

        # Set number of columns based on the date range
        self.tabStat.setColumnCount(total_days)
        self.tabStat_projet_operateur.setColumnCount(total_days)

        # Create headers with formatted date strings
        headers = [(start_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(total_days)]
        self.tabStat.setHorizontalHeaderLabels(headers)
        self.tabStat_projet_operateur.setHorizontalHeaderLabels(headers)

        self.flagToday(pastcast,self.tablist) #Mets aujourd'hui en orange sur les différents tableau, ne pas oublier d'ajouter un tableau si nouveau

        self.tabStat.setRowCount(len(["Temps passé - temps alloué", "Charge/Capacité"]))
        self.tabStat.setVerticalHeaderLabels(["Temps passé - temps alloué", "Charge/Capacité"])
        
        self.tabStat_slot.addWidget(self.tabStat)

        #Filling first tab
        for col in range(self.tabStat.columnCount()): 
            # print(f"l'header de la col : {self.tabStat.horizontalHeaderItem(col).text()}, et la date d'aujourdh'ui : {date.today().strftime('%d-%m-%Y')}")
            # print(self.tabStat.horizontalHeaderItem(col).text() == date.today().strftime('%d-%m-%Y')) #Renvoie bien true

            #On passe la date de la colonne en object de type date pour ensuite changer son format pour l'envoyer en db
            date_object = datetime.strptime(self.tabStat.horizontalHeaderItem(col).text(), "%d-%m-%Y").date()
            date_object.strftime('%Y-%m-%d')

            # Temps passe
            sql_pour_temps_passe = f"SELECT count(*) FROM public.assignments Where start_date <= '{date_object}' and end_date >= '{date_object}'"
            # print(sql_pour_temps_passe)
            query  = sendQuery(sql_pour_temps_passe,self)
            query.next()
            record_tempsPasse = query.record()
            for row  in range(self.tabStat.rowCount()):
                if row == 0 : 
                    #Temps passé / temps alloué 
                    newItem = QTableWidgetItem()
                    newItem.setText(str(record_tempsPasse.value(0)*8)) # x8 Pour un contrat normale !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.tabStat.setItem(row,col,newItem)


        # Filling second tab
        self.stat_slot_pro_op.addWidget(self.tabStat_projet_operateur)

        #
        sql = f'SELECT distinct "Projet","SousEnsemble" from tasks'
        query = sendQuery(sql)
        row_headers = []
        while query.next():
            hel = f"{query.value(0)}:{query.value(1)}"
            row_headers.append(hel)
        #
        self.tabStat_projet_operateur.setRowCount(len(row_headers))
        self.tabStat_projet_operateur.setVerticalHeaderLabels(row_headers)





        for col in range(self.tabStat_projet_operateur.columnCount()):
            #J'appel la fonction qui me renvoi le dico avec les projet sousensemble et nbrope
            date_object = datetime.strptime(self.tabStat.horizontalHeaderItem(col).text(), "%d-%m-%Y").date()
            date_object.strftime('%Y-%m-%d')
            for row in range(self.tabStat_projet_operateur.rowCount()):
                query = QSqlQuery()
                projet = f"{str(row_headers[row]).split(':')[0]}"
                sous_ensemble = f"{str(row_headers[row]).split(':')[1]}"
                query.prepare("SELECT * FROM public.get_operators_by_project_and_subset(:date, :projet, :sous_ensemble)")
                query.bindValue(":date" , str(date_object) )
                query.bindValue(":projet", projet)
                query.bindValue(":sous_ensemble", sous_ensemble)
                if not query.exec():
                    print("Erreur lors de l'exécution de la requête")
                    return
                query.next()
                newItem = QTableWidgetItem()
                newItem.setText(str(query.record().value(2)))
                self.tabStat_projet_operateur.setItem(row,col,newItem)

            

    def flagToday(self, pastcast, tabList : list[QTableWidget]):

        for tab in tabList:
            newItemc = tab.horizontalHeaderItem(pastcast)
            newItemc.setBackground(QBrush(QColor('orange')))
            newItemc.setText(datetime.today().strftime("%d-%m-%Y"))
        

