from PySide6.QtWidgets import QWidget, QPushButton, QTableWidget,QFormLayout,QProgressBar,QVBoxLayout, QLineEdit, QLabel
from PySide6.QtCore import QTimer, QSize
import os
from tools_function import loadUI, records_table_paser, dict_to_uiTable, sendQuery
from PySide6.QtGui import QIcon
from bs4 import BeautifulSoup
import csv
import random
from typing import cast
from typing import Optional
from PySide6.QtSql import QSqlQuery, QSqlDatabase

class TasksWidget(QWidget):
    def __init__(self):
        super(TasksWidget, self).__init__()

        self.setWindowTitle("Tasks Window")
        self.setGeometry(0, 0, 1850, 800)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"Tasks.ui")

        # mappage
        createTaskButton = self.findChild(QPushButton, "pushButton")
        if createTaskButton is None: print("Le QPushButton 'pushButton' est introuvable")
        else: self.createTaskButton: QPushButton = createTaskButton

        formLayoutTask = self.findChild(QFormLayout, "formLayout")
        if formLayoutTask is None: print("Le QFormLayout 'formLayout' est introuvable")
        else: self.formLayoutTask: QFormLayout = formLayoutTask

        submitButton = self.findChild(QPushButton, "submit")
        if submitButton is None: print("Le QPushButton 'submit' est introuvable")
        else: self.submitButton: QPushButton = submitButton

        pb_slot = self.findChild(QVBoxLayout, "PB_slot")
        if pb_slot is None: print("Le QVBoxLayout 'PB_slot' est introuvable")
        else: self.PB_slot: QVBoxLayout = pb_slot


        if pb_slot is None: print("Le QVBoxLayout 'PB_slot' est introuvable")
        else: self.PB_slot: QVBoxLayout = pb_slot

        #self.tasks_table = self.findChild(QTableWidget,"table_tasks")
        tasks_table_slot = self.findChild(QVBoxLayout, "tasks_table_slot")
        if tasks_table_slot is None: print("Le QVBoxLayout 'tasks_table_slot' est introuvable")
        else: self.tasks_table_slot: QVBoxLayout = tasks_table_slot




        #Configuration
        self.form_visible(False)
        self.createTaskButton.pressed.connect(lambda: TasksWidget.form_visible(self,visibleStatut = True))
        self.submitButton.pressed.connect(lambda: TasksWidget.progressBarAnimation(self))
        self.submitButton.pressed.connect(lambda: TasksWidget.form_visible(self,visibleStatut = False))
        self.submitButton.pressed.connect(lambda: TasksWidget.insertTask(self))
        self.submitButton.pressed.connect(lambda: TasksWidget.actualiser(self))


        self.last_id = self.actualiser() # à commenter avec la ligne du dessous
        self.load_tasks_from_SAP() #N'exécuter que en tant qu'admin ! 

        self.last_id = self.actualiser()


    def progressBarAnimation(self):
        PB = QProgressBar()
        self.PB_slot.addWidget(PB)
        PB.show()
        PB.setRange(0, 0)
        # Create a QTimer
        timer = QTimer(self)
        timer.setSingleShot(True)  # The timer will fire only once
        timer.timeout.connect(lambda: self.removeProgressBar(PB))
        timer.start(2000)  # Start the timer for 2000 milliseconds (2 seconds)

    def removeProgressBar(self, PB):
        # Remove the progress bar from the layout
        self.PB_slot.removeWidget(PB)
        PB.deleteLater()  # Schedule the progress bar for deletion
        
    def form_visible(self,visibleStatut: bool):
        #Cache ou montre le form
        for i in range(6):
            self.formLayoutTask.setRowVisible(i,visibleStatut)

    def insertTask(self): ###Non terminée
        task_data = {}  # Dictionary to store the values from QLineEdit widgets

        # Iterate over each row in the form layout
        for row in range(self.formLayoutTask.rowCount()):
            # Get the label and field items from the row
            label_item = self.formLayoutTask.itemAt(row, QFormLayout.ItemRole.LabelRole)
            field_item = self.formLayoutTask.itemAt(row, QFormLayout.ItemRole.FieldRole)


            if label_item and field_item:
                label_widget = label_item.widget()
                field_widget = field_item.widget()

                if label_widget and field_widget:
                    # Get the label text
                    label_html = label_widget.text() # type: ignore
                    soup = BeautifulSoup(label_html, 'html.parser')
                    label = soup.get_text(strip=True)

                # Get the field widget (assuming it's a QLineEdit)
                field_widget = field_item.widget()
                
                if isinstance(field_widget, QLineEdit):
                    soup = BeautifulSoup(field_widget.text(), 'html.parser')
                    task_data[label] = soup.get_text(strip=True)
                    # Store the label and corresponding QLineEdit value in the dictionary
        sql = "INSERT INTO Tasks (id,affaire, sousEnsemble, operation, periode, couleur) VALUES ('"+ str(self.last_id+1) +"','"+ str(task_data["Affaire"]) + "','" + str(task_data["Sous ensemble"]) + "','" + str(task_data["Opération"]) + "','" + str(task_data["Période"]) + "','" + str(task_data["Couleur"]) + "');"
        #sql = "INSERT INTO Tasks (affaire, sousEnsemble, operation, periode, couleur) VALUES ('"+ str(task_data["Affaire"]) + "','" + str(task_data["Sous ensemble"]) + "','" + str(task_data["Opération"]) + "','" + str(task_data["Période"]) + "','" + str(task_data["Couleur"]) + "');"

        sendQuery(sql)

    def actualiser(self) -> int :
        #Actualise et retourne l'id de la dernière tasks en db
        if (self.tasks_table_slot.count() == 2):
            self.tasks_table_slot.removeWidget(self.tasks_table)
        self.tasks_table  = QTableWidget()
        
        self.tasks_table.setColumnCount(9)
        size = QSize(200,100)
        self.tasks_table.size()
        self.tasks_table.setHorizontalHeaderLabels(["ID", "Projet", "Sous-Ensemble", "Bundle","OF","Opération","INDEX Opération","Couleur","Temps alloué","Temps passé (extract)"])

        # Assuming records_table_paser and dict_to_uiTable are defined in tools_function
        dic_tasks_data,cop = records_table_paser("Tasks")
        dict_to_uiTable(dic_tasks_data, self.tasks_table)
        self.tasks_table_slot.addChildWidget(self.tasks_table)
        try:
            last_key = list(dic_tasks_data)[-1]
        except:
            return 0
        return int(dic_tasks_data[last_key]['ID'])

    def load_tasks_from_SAP(self):
        path = os.path.join(os.path.dirname(__file__), "ressources", "data.csv")

        # Ouvrir le fichier csv
        with open(path, newline='', encoding='utf-8') as csvfile:
            data = csv.DictReader(csvfile,fieldnames=['Projet','SousEnsemble','Bundle','SN','OF','Opération','index operation','Temps alloué','Temps passé'])

            sql = """INSERT INTO tasks ("ID", "Projet", "SousEnsemble", "Bundle" , "SN" , "OF" , "Operation_titre" , "Operation_index", "Couleur", "Temps_alloue", "Temps_passe") VALUES"""
            next(data)  # Skip la première ligne qui contient les en-têtes déjà définies
            counter = 0
            for item in data:
                passe = '0' if item['Temps passé'] == '' else item['Temps passé']
                value = f"('{self.last_id+counter+1}','{item['Projet']}','{item['SousEnsemble']}','{item['Bundle']}','{item['SN']}','{item['OF']}','{item['Opération'].replace("'","''")}','{item['index operation']}','{"#{0:06x}".format(random.randint(0, 0xFFFFFF))}','{item['Temps alloué']}','{ passe }'),"
                sql += value
                counter += 1
            sql = sql[:-1] + ";"
            sendQuery(sql)
               
            



        
