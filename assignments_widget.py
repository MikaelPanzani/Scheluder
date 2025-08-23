from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QTextEdit, QTableWidgetItem, QMessageBox, QCompleter, QLabel, QCheckBox
import os
from gannt import Gannt
from tools_function import loadUI, records_table_paser, sendQuery, records_to_Ldict_SELECT
from my_errors import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QDate

class AssignmentsWidget(QWidget):
    def __init__(self):
        super(AssignmentsWidget, self).__init__()

        self.setWindowTitle("Assignments Window")
        self.setGeometry(0, 0, 1850, 900)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"assignments.ui")

        gannt_slot = self.findChild(QVBoxLayout,"ganntSlot")
        if gannt_slot is None:
            print('gannt_slot introuvable')
        else:
            self.gannt_slot:QVBoxLayout = gannt_slot

        self.gannt = Gannt(modifiable=True)

        #self.gannt.setSelectionMode(QAbstractItemView.ExtendedSelection)


        self.gannt_slot.addWidget(self.gannt)

        # Find widgets in the loaded UI
        #mappage
        combo  = self.findChild(QComboBox,"comboBox")
        if combo is None:
            print('comboBox introuvable')
        else:
            self.combo : QComboBox = combo
        
        comboBox_Project  = self.findChild(QComboBox,"comboBox_Project")
        if comboBox_Project is None:
            print('comboBox introuvable')
        else:
            self.comboBox_Project : QComboBox = comboBox_Project

        comboBox_SousEnsemble  = self.findChild(QComboBox,"comboBox_SousEnsemble")
        if comboBox_SousEnsemble is None:
            print('comboBox introuvable')
        else:
            self.comboBox_Project : QComboBox = comboBox_SousEnsemble

        comboBox_Bundle  = self.findChild(QComboBox,"comboBox_Bundle")
        if comboBox_Bundle is None:
            print('comboBox introuvable')
        else:
            self.comboBox_Project : QComboBox = comboBox_Bundle

        comboBox_SN  = self.findChild(QComboBox,"comboBox_SN")
        if comboBox_SN is None:
            print('comboBox introuvable')
        else:
            self.comboBox_Project : QComboBox = comboBox_SN

        load_button = self.findChild(QPushButton,"load_button")
        if load_button is None : 
            print('load_button introuvable')
        else : self.load_button : QPushButton = load_button

        submit_button = self.findChild(QPushButton,"submit_button")
        if submit_button is None : 
            print('submit_button introuvable')
        else : self.submit_button : QPushButton = submit_button

        delete_Button = self.findChild(QPushButton,"delete_Button")
        if delete_Button is None : 
            print('delete_Button introuvable')
        else : self.delete_Button : QPushButton = delete_Button

        self.sql_query : str = ''

        displayAffaire = self.findChild(QLabel, "displayAffaire")
        if displayAffaire is None:
            print('QLabel not found displayAffaire')
        else :  self.displayAffaire : QLabel = displayAffaire

        displayArticle = self.findChild(QLabel, "displayArticle")
        if displayArticle is None:
            print('QLabel not found displayArticle')
        else :  self.displayArticle : QLabel = displayArticle

        displayOperation = self.findChild(QLabel, "displayOperation")
        if displayOperation is None:
            print('QLabel not found displayOperation')
        else :  self.displayOperation : QLabel = displayOperation

        displayTAlloue = self.findChild(QLabel, "displayTAlloue")
        if displayTAlloue is None:
            print('QLabel not found displayTAlloue')
        else :  self.displayTAlloue : QLabel = displayTAlloue

        displayTPasse = self.findChild(QLabel, "displayTPasse")
        if displayTPasse is None:
            print('QLabel not found displayTPasse')
        else :  self.displayTPasse : QLabel = displayTPasse

        displayTAttri = self.findChild(QLabel, "displayTAttri")
        if displayTAttri is None:
            print('QLabel not found displayTAttri')
        else :  self.displayTAttri : QLabel = displayTAttri

        displayRAT = self.findChild(QLabel, "displayRAT")
        if displayRAT is None:
            print('QLabel not found displayRAT')
        else :  self.displayRAT : QLabel = displayRAT

        combo_machine = self.findChild(QComboBox, "combo_machine")
        if combo_machine is None:
            print('QLabel not found combo_machine')
        else :  self.combo_machine : QComboBox = combo_machine

        checkBox_isMachineAssigned = self.findChild(QCheckBox, "checkBox_isMachineAssigned")
        if checkBox_isMachineAssigned is None:
            print('QLabel not found checkBox_isMachineAssigned')
        else :  self.checkBox_isMachineAssigned : QCheckBox = checkBox_isMachineAssigned

        displayNomMachine = self.findChild(QLabel, "displayNomMachine")
        if displayNomMachine is None:
            print('QLabel not found displayNomMachine')
        else :  self.displayNomMachine : QLabel = displayNomMachine

        displayMachineOP = self.findChild(QLabel, "displayMachineOP")
        if displayMachineOP is None:
            print('QLabel not found displayMachineOP')
        else :  self.displayMachineOP : QLabel = displayMachineOP

        displayMachineOPmax = self.findChild(QLabel, "displayMachineOPmax")
        if displayMachineOPmax is None:
            print('QLabel not found displayMachineOPmax')
        else :  self.displayMachineOPmax : QLabel = displayMachineOPmax


        

        #Configurations
        #Ajout des tâches à la combo box : task_id : nameTask
        dic_tasks_data,ct = records_table_paser("Tasks")
        items : list[str] = []
        for id_enregistrement, task_data in dic_tasks_data.items():
                toCombo = str(task_data['ID']) +" : "+ task_data['Projet'] + " - " + task_data['SousEnsemble']+ " - " + task_data['Operation_titre'] + " - " + task_data['SN']
                items.append(toCombo)
                self.combo.addItem(toCombo)
        # Q completer pour avoir combo liste interactive
        self.combo.setEditable(True)
        completer = QCompleter(items, self.combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.combo.setCompleter(completer)

        #Ajout des machines à la combo box : 
        #Code copier coller au dessus (ajout des tâches à la combo)
        dic_m_data,ct = records_table_paser("Machines")
        items : list[str] = []
        for id_enregistrement, m_data in dic_m_data.items():
                combo_machine = str(m_data['id']) +" : "+ m_data['name'] + " - " + str(m_data['max_operators'])
                items.append(combo_machine)
                self.combo_machine.addItem(combo_machine)
        # Q completer pour avoir combo liste interactive
        self.combo_machine.setEditable(True)
        completer_machine = QCompleter(items, self.combo_machine)
        completer_machine.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer_machine.setFilterMode(Qt.MatchFlag.MatchContains)
        self.combo_machine.setCompleter(completer_machine)
        

        
        self.load_button.pressed.connect(lambda: AssignmentsWidget.actualizeTasknMachineInfo(self))
        self.load_button.pressed.connect(lambda: AssignmentsWidget.writeInsertQuery_multipleOP(self))
        self.submit_button.pressed.connect(lambda: sendQuery(self.sql_query,self))
        self.submit_button.pressed.connect(lambda: AssignmentsWidget.actualiser(self))
        self.delete_Button.pressed.connect(lambda: AssignmentsWidget.deleteAssignement(self))
        #self.gannt.cellClicked.connect(lambda: AssignmentsWidget.getSelectedData(self))

    
    def actualizeTasknMachineInfo(self):
        # Stratégie : questionner la db ou boucler sur les données déjà charger... pour l'instant on interroge
        task_id = self.combo.currentText().split(":")[0] #Id de la tâche selectionnée
        sql = f"SELECT * FROM TASKS WHERE {'"ID"'} = {task_id}"
        dict_task = records_to_Ldict_SELECT(sql)[0]
        ta = dict_task['Temps_alloue']
        tp = dict_task["Temps_passe"]
        self.displayAffaire.setText(dict_task['Projet'])
        self.displayArticle.setText(dict_task['SousEnsemble'])
        self.displayOperation.setText(dict_task['Operation_titre'])
        self.displayTAlloue.setText(str(ta))
        self.displayTPasse.setText(str(tp))
        
        if self.checkBox_isMachineAssigned.isChecked():
            #Récupération des données de machine - 1 record
            machine_id = self.combo_machine.currentText().split(":")[0] #Id de la machine selectionnée
            sql = f"SELECT * FROM machines WHERE id = {machine_id}"
            dictMachine = records_to_Ldict_SELECT(sql)[0]
            self.displayNomMachine.setText(str(dictMachine['name']))
            nbOpMax = dictMachine['max_operators']
            self.displayMachineOPmax.setText(str(nbOpMax))
        else:
            pass


        #Récupération des données d'attributions - plusieurs record - info sur les tâches et machine
        sql = f"SELECT * FROM ASSIGNMENTS WHERE task_id = {task_id}"
        tempsAttrib = 0
        assignement_dict_list : list[dict] = records_to_Ldict_SELECT(sql)
        for dictA in assignement_dict_list:
                tempsAttrib += (QDate(dictA['start_date']).daysTo(QDate(dictA['end_date'])) +1) * 7
        self.displayTAttri.setText(str(tempsAttrib))
        self.displayRAT.setText(str(ta-tp-tempsAttrib))
        #Rajouter ici le 
        if self.checkBox_isMachineAssigned.isChecked():
            id_op,name_op,str_sdate,str_edate,empty_cells, isPast, listID_OP = self.getSelectedData()
            sql = f"WITH date_series AS (SELECT generate_series('{str_sdate}'::DATE,'{str_edate}'::DATE,INTERVAL '1 day')::DATE AS day)\nSELECT ds.day,COUNT(DISTINCT a.operator_id) AS distinct_operator_count FROM date_series ds LEFT JOIN assignments a ON ds.day BETWEEN a.start_date AND a.end_date WHERE a.machine_id = {machine_id} GROUP BY ds.day ORDER BY ds.day;"
            assignement_dict_list_machine = records_to_Ldict_SELECT(sql)
            nombre_dop_par_jour : list[int] = [item['distinct_operator_count'] for item in assignement_dict_list_machine]
            #J'ai la liste des attributions qui concerne la machine selectionné et dont les dates sont comprises dans les dates sélectionnés sous forme de dictionnaire, une attrib = un dict
            self.displayMachineOP.setText(nombre_dop_par_jour.__str__())
        else:
            pass
        

        
    def getSelectedData(self):
        listItems : list[QTableWidgetItem] = self.gannt.selectedItems()
        #Check id selected data contient des cellules non vide
        empty_cells : bool = True
        self.isCellselected = True
        listOP_ID : list[int] = [] # A REFLECHIR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Est ce que je garde cette fonctionalité là ou pas (beaucoup d'erreurs peuvent être générées possiblement)
        for item  in listItems :
            #On créer une liste avec les différent OP id s'il y en a
            #récupération de la ligne courante
            row = item.row()
            str_op = self.gannt.verticalHeaderItem(row).text() #récupération du str header verticial "id : nom prenom"
            id_op = int(str_op.split(':')[0]) #extraction de l'id
            if id_op not in listOP_ID:
                listOP_ID.append(id_op) #J'ajoute l'id seulement s'il n'est déjà pas présent dans la list
            #Check si les cellules contiennent déjà du texte
            if item.text() != '' : 
                empty_cells =False
        #listID_OP est maintenant la list  des id des opé sélectionnés
        try :
           
            firstItem = listItems[0]
            lastitem = listItems[-1]
            li_col = lastitem.column()
            fi_col = firstItem.column()
            fi_row = firstItem.row()
            str_sdate = self.gannt.horizontalHeaderItem(fi_col).text()
            if li_col != fi_col:
                str_edate = self.gannt.horizontalHeaderItem(li_col).text()
            else :
                str_edate = str_sdate
            str_op = self.gannt.verticalHeaderItem(fi_row).text()
            id_op = str_op.split(':')[0]
            name_op = str_op.split(':')[1]

            #On regarde si la date de start est dans le passé
            date_parts = str_sdate.split('-')
            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])
            sdate = QDate(year, month, day)
            today = QDate.currentDate()
            if sdate < today:
                isPast = True
            else :
                isPast = False
            
            return id_op,name_op,str_sdate,str_edate,empty_cells, isPast, listOP_ID
        except:
            QMessageBox.critical(self, "Erreur", "Aucune cellule sélectionnée") 
            self.isCellselected = False
            raise ValueError("Aucune cellule sélectionnée")
            
        
    
    def writeInsertQuery(self):
        data = self.getSelectedData()
        int_idop,str_sdate, str_edate, isPast  = data[0],data[2], data[3], data[5]
        task_id = self.combo.currentText().split(":")[0]
        if self.checkBox_isMachineAssigned.isChecked():
            machine_id = self.combo_machine.currentText().split(":")[0] #Id de la machine selectionnée
        else :
            machine_id = None

        if self.isCellselected:
            if not(isPast):
                if machine_id is None :
                    sql = f"INSERT INTO Assignments (name, operator_id, task_id, start_date, end_date) VALUES ('Mon Assignement !', {int_idop}, {task_id}, '{str_sdate}', '{str_edate}')"
                else :
                    sql = f"INSERT INTO Assignments (name, operator_id, task_id, start_date, end_date, machine_id) VALUES ('Mon Assignement !', {int_idop}, {task_id}, '{str_sdate}', '{str_edate}', {machine_id})"

                self.sql_query = sql
            else :
                QMessageBox.critical(self, "Attribution sur un jour passé", "Attention ! Vous voulez attribuer un opérateur sur un jour passé.")

            #pop up d'avertissement 
            if not(data[4]):
                QMessageBox.information(self, "Modifier attributions", "Attention ! Vous allez modifier une attribution, vous pouvez confirmer en appuyant sur Valider.")

    def writeInsertQuery_multipleOP(self):
        #Copier coller de writeInsertQuery au départ
        data = self.getSelectedData()
        int_idop,str_sdate, str_edate, isPast, listID_OP  = data[0],data[2], data[3], data[5], data[6]
        task_id = self.combo.currentText().split(":")[0] #Extraction de l'id de la tâche
        if self.checkBox_isMachineAssigned.isChecked():
            machine_id = self.combo_machine.currentText().split(":")[0] #Id de la machine selectionnée
        else :
            machine_id = None

        if self.isCellselected:
            if not(isPast):
                if machine_id is None :
                    sql  = "INSERT INTO Assignments (name, operator_id, task_id, start_date, end_date) VALUES"
                    for idop in listID_OP:
                        #Pour chaque id dans la list des id operateur 
                        sql += f"('Mon Assignement !', {idop}, {task_id}, '{str_sdate}', '{str_edate}'),"
                else :
                    sql  = "INSERT INTO Assignments (name, operator_id, task_id, start_date, end_date, machine_id) VALUES"
                    for idop in listID_OP:
                        #Pour chaque id dans la list des id operateur 
                        sql += f"('Mon Assignement !', {idop}, {task_id}, '{str_sdate}', '{str_edate}', {machine_id}),"
                
                sql = sql[:-1] + ";"   
                self.sql_query = sql
            else :
                QMessageBox.critical(self, "Attribution sur un jour passé", "Attention ! Vous voulez attribuer un opérateur sur un jour passé.")

            #pop up d'avertissement 
            if not(data[4]):
                QMessageBox.information(self, "Modifier attributions", "Attention ! Vous allez modifier une attribution, vous pouvez confirmer en appuyant sur Valider.")

    def actualiser(self):
        current_postion_h = self.gannt.horizontalScrollBar().value()
        current_postion_v = self.gannt.verticalScrollBar().value()
        self.gannt_slot.removeWidget(self.gannt)
        self.gannt = Gannt(modifiable=True)
        self.gannt.setVHSliderPosition(current_postion_h,current_postion_v)
        self.gannt_slot.addWidget(self.gannt)


    def deleteAssignement(self):
        data = self.getSelectedData()
        int_idop,str_nameop,str_sdate, str_edate  = data[0],data[1],data[2], data[3]
        sql = f"DELETE FROM ASSIGNMENTS WHERE operator_id = {int_idop} and ('{str_sdate}' between  start_date  and end_date)"
        sendQuery(sql,self)
        self.actualiser()