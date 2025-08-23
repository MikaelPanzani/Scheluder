from datetime import datetime
import os
from PySide6.QtSql import QSqlQuery, QSqlDatabase
from PySide6.QtWidgets import QTableWidgetItem, QWidget, QMessageBox
import numpy as np
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QDate, QFileDevice, QIODevice
import socket


@DeprecationWarning
def connect_to_sqlite():
    if QSqlDatabase.contains("qt_sql_default_connection"):
        QSqlDatabase.removeDatabase("qt_sql_default_connection")
    db = QSqlDatabase.addDatabase("QSQLITE") #Ajout du driver
    db.setDatabaseName("workforce.db")  # Creates the file if it doesn’t exist

    if not db.open():
        print("Failed to connect:", db.lastError().text())
        return None
    else:
        #print("Connected to SQLite")
        query = QSqlQuery(db) # Juste pour sql lite !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        query.exec_("PRAGMA foreign_keys = ON;") # Juste pour sql lite !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return db

def print_table_records(db, table_name):
    query = QSqlQuery(db)
    query.exec_(f"SELECT * FROM {table_name}")

    # Check if the query was successful
    if query.lastError().isValid():
        print("Query error:", query.lastError().text())
        return

    # Get the number of columns in the result
    record = query.record()
    num_columns = record.count()

    # Print header
    headers = [record.fieldName(i) for i in range(num_columns)]
    print("\t".join(headers))

    # Print records
    while query.next():
        row = [str(query.value(i)) for i in range(num_columns)]
        print("\t".join(row))

def records_table_paser(table_name):
    #Converti la table en un dictionnaire de dictionnaire, la cle du premier dictionnaire est l'indice dans la table : 0 = premier enregistrement (pas entête)
    #Les valeurs du premier dictionnaire sont des dictionnaires dont les cle sont le noms des colonne et les valeur les éléments correspondant à une cellule
    
    query = sendQuery(f"SELECT * FROM {table_name}",)

    counter = 0 
    output = {}

    while query.next():
        
        record = query.record() #record est un Qsqlrecord objet 
        

        #Faire une fonction de la boucle cette boucle a été copié collé dans assignments_widget : il faut faire une fonction !
        nombre_de_colonne = record.count() #Nombre de col du record (et donc de la table) en paramètre
        sous_dict = {} #Creation d'un sous dictionnaire pour un record ou les cle sont les noms des colonnes et les valeurs les éléments de chaque colonne
        for i in range(nombre_de_colonne):
            nom = record.fieldName(i)
            sous_dict[nom] = record.value(i)
        #Faire une fonction de la boucle cette boucle a été copié collé dans assignments_widget : il faut faire une fonction !

        output[counter] = sous_dict
        counter += 1
    return output, counter

def records_query_parser(sql:str) -> tuple[dict,int] :
    #Envoie une la requete passée en parametre puis renvoie le résultat sous forme de dictionnaire (meme chose que records_table_parser- mais avec une requête variable)

    query = sendQuery(sql)
    counter = 0 
    output = {}

    while query.next():
        
        record = query.record() #record est un Qsqlrecord objet 
        

        #Faire une fonction de la boucle cette boucle a été copié collé dans assignments_widget : il faut faire une fonction !
        nombre_de_colonne = record.count() #Nombre de col du record (et donc de la table) en paramètre
        sous_dict = {} #Creation d'un sous dictionnaire pour un record ou les cle sont les noms des colonnes et les valeurs les éléments de chaque colonne
        for i in range(nombre_de_colonne):
            nom = record.fieldName(i)
            sous_dict[nom] = record.value(i)
        #Faire une fonction de la boucle cette boucle a été copié collé dans assignments_widget : il faut faire une fonction !

        output[counter] = sous_dict
        counter += 1

    return output, counter

def dict_to_uiTable(dic_operators_data, table_widget):
    for id_enregistrement, dictData in dic_operators_data.items():
        #Pour chaque record
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)
        c = 0
        for nomCol, valeur in dictData.items():
            table_widget.setItem(row_position, c, QTableWidgetItem(str(valeur)))
            table_widget.setItem(row_position, c, QTableWidgetItem(str(valeur)))
            c += 1


def conversionTableAssignementEnTableItem(lignes: int, colonnes: int, dic_assignement_data: dict, date0: datetime, dic_operators_data: dict):
    #Converti la table assignement en matrice 2D op date d'élément item

    idOpList = [operatorData_dictionarie.get("id") for operatorData_dictionarie in dic_operators_data.values()]
    matrix = np.full((lignes, colonnes, 2), -1)
    for cle,assignmentData_dictionarie in dic_assignement_data.items():
        idOP =  assignmentData_dictionarie.get("operator_id")
        idTA =  assignmentData_dictionarie.get("task_id")
        idMa = assignmentData_dictionarie.get("machine_id")
        start =  QDate(assignmentData_dictionarie.get("start_date")) #Qdate
        start_dt = datetime.strptime(start.toString("dd-MM-yyyy"),"%d-%m-%Y") #Attention au format : conversion pour opération
        end =  QDate(assignmentData_dictionarie.get("end_date")) #Qdate
        end_dt = datetime.strptime(end.toString("dd-MM-yyyy"),"%d-%m-%Y") #Attention au format : conversion pour opération
        indiceStart = (start_dt-date0).days +1 #indice du jour de debut de l'assignation
       
        if indiceStart < 0 :
            indiceStart = 0
        indiceEnd = (end_dt-date0).days + 2 #indice du jour de fin de l'assignation
        #print(f"indiceStart : {indiceStart} indiceEnd : {indiceEnd} IdTA : {int(idTA)} iDOP : {idOP} IndiceOP : {idOpList.index(idOP)}")
        vector = np.array([int(idTA),int(idMa)])
        matrix[idOpList.index(idOP),indiceStart:indiceEnd] = vector
    np.set_printoptions(precision=0, suppress=True, linewidth=400, threshold=int(1e9))
    #print(matrix)
    return matrix

def getTaskSTR(id: int, dic_tasks_data: dict ):

    outSTR = 'Unkown task'
    #print(dic_tasks_data)
    for cle,taskDic  in dic_tasks_data.items() :
        idTask =  taskDic.get("ID")
        
        if idTask == id : 
            aTask =  taskDic.get("Projet")
            seTask =  taskDic.get("SousEnsemble")
            oTask =  taskDic.get("Operation_titre")
            outSTR = f"{idTask}\n{aTask}\n{seTask}\n{oTask}\n"
            color = taskDic.get("Couleur")
            return outSTR, color
    return outSTR


def getMachineSTR(id: int, dic_machine_data: dict ) -> str:
    #Retourne un str avec les données de la machine
    for cle,maDic  in dic_machine_data.items() :
        maID =  maDic.get("id")
        if maID == id : 
            return f"\nMachine : {str(maID)}\n{maDic.get("name")}"
    return ''





def loadUI(currentWidget: QWidget,fileName: str):
    # Load the UI file
        loader = QUiLoader()
        ui_file_path = os.path.join(os.path.dirname(__file__), "ui/"+fileName)
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            print("Cannot open .ui file:", ui_file.errorString())
            return
        currentWidget.ui = loader.load(ui_file,currentWidget)  # type: ignore
        currentWidget.resize(1850, 800)
        ui_file.close()

def sendQuery(query_sql: str, widget : QWidget|None = None) -> QSqlQuery:
    #Envoie une requete en db et print si erreur, si un widget est donné en argument, une message box s'ouvre pour le montrer à l'utilisateur
    db = connect_to_PostgreSQL()
    query = QSqlQuery(db)
    query.exec_(query_sql) # qt.sql.qsqlquery: QSqlQuery::exec: database not open mais c'est pas vrai
    if query.lastError().isValid():
        if widget != None :
            QMessageBox.critical(widget, "Erreur", f"Query error: {query.lastError().text()}")
        print("Query error:", query.lastError().text())
    db.close
    return query 

def connect_to_PostgreSQL() -> QSqlDatabase:
    connection_name = "qt_sql_default_connection"
    if QSqlDatabase.contains(connection_name):
        #QSqlDatabase.removeDatabase(connection_name)
        db = QSqlDatabase.database()
        return db
    else:
        print(f"My adress is : {get_local_ip()}")
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setDatabaseName("workforce_planification_db")  
        #db.setHostName("localhost")
        #db.setHostName("10.41.25.219")
        db.setHostName("10.41.122.210")
        db.setUserName("postgres")
        db.setPassword("L0030922")
        db.setPort(5432)
        if not db.open():
            error_message = db.lastError().text()
            print(f"Failed to connect: {error_message}")
            raise Exception(f"Database connection failed: {error_message}")
        else :
            print(f"Connected to {db.databaseName()} database.\nHostname : {db.hostName()}.\nPort number : {db.port()}.\nMy username is : {db.userName()}.\nMy password is : **********")
            return db


def get_local_ip():
    #By chat gpt
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # On ne contacte rien réellement, juste pour obtenir l'IP liée à la route
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def records_to_Ldict_SELECT(sql : str) -> list[dict]:
    data_from_db = sendQuery(sql)
    list_dict : list[dict] = []
    while data_from_db.next():
        record  = data_from_db.record()
    
        #Faire une fonction de la boucle copié collé from tools_function !!! Faire une FONCTION !!!!!!!!!!!!!!!!!!!!
        sous_dict = {} #Creation d'un sous dictionnaire pour un record ou les cle sont les noms des colonnes et les valeurs les éléments de chaque colonne
        nombre_de_colonne = record.count() #Nombre de col du record (et donc de la table) en paramètre
        for i in range(nombre_de_colonne):
            nom = record.fieldName(i)
            sous_dict[nom] = record.value(i)
        list_dict.append(sous_dict)
    #print(list_dict)
    return list_dict








    