import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QAbstractItemView, QLabel, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys
from gannt import Gannt
from machines_widget import MachinesWidget
from stat_widget import StatWidget
from tools_function import *
from my_errors import *
from operators_widget import *
from assignments_widget import *
from PySide6.QtGui import QIcon, QPixmap
from tasks_widget import *



class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tetris 2.0 : Login')
        self.setGeometry(0, 0, 600, 200)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        loadUI(self,"login.ui")


        self.identificationsList : list[dict] = [{"username" : "admin","password" : "L0030922"},{"username":"invité","password":"invité"}]

        #mappage
        username = self.findChild(QLineEdit, "usernameLineEdit")
        if username is None: print("usernameLineEdit est introuvable")
        else: self.username: QLineEdit = username

        password = self.findChild(QLineEdit, "passwordLineEdit")
        if password is None: print("passwordLineEdit est introuvable")
        else: self.password: QLineEdit = password

        pushButton = self.findChild(QPushButton, "pushButton")
        if pushButton is None: print("pushButton est introuvable")
        else: self.pushButton: QPushButton = pushButton

        self.pushButton.pressed.connect(lambda: LoginWidget.connect(self))

        self.username.setText("admin")
        self.password.setText("L0030922")

    def connect(self):
        user : str  = self.username.text() 
        passs : str  = self.password.text() 
        user_ok : bool = False
        passs_ok : bool = False
        for itemList in self.identificationsList:
            if user == itemList['username']:
                user_ok = True
                if passs == itemList['password']:
                    passs_ok = True
                    break
        if user_ok and passs_ok :
            self.main_window = MainWindow(user_name=user)
            self.main_window.show()
            self.close()
        elif user_ok :
            print("Password error")
        else :
            print('Username error')


class MainWindow(QMainWindow):
    def __init__(self, user_name : str):
        super(MainWindow, self).__init__()
        self.user =  user_name

        print(f"Hi {self.user}")

        #TO Remove (just for debugging)
        # print('\n')
        # print(os.environ["PATH"])
        # print('\n')

        self.setGeometry(0, 0, 1850, 800)
        self.setWindowTitle("TETRIS 2.0")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ressources/puzzle.png")))

        # Load the .ui file
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "ui/Main_Window.ui")
        ui_file = QFile(path)
        self.ui = loader.load(ui_file)
        ui_file.close()
        self.setCentralWidget(self.ui)  # Set the loaded UI as the central widget

        #Welcoming -- Message Box exemple
        """self.welcomingMB = QMessageBox()
        self.welcomingMB.setWindowTitle('Welcome!')
        self.welcomingMB.setText("Welcome to the new Tetris ! ")
        x = self.welcomingMB.exec()"""

        #Logo
        logo = self.findChild(QLabel, "logo")
        if logo is None:
            raise RuntimeError("Le QLabel 'logo' est introuvable")
        self.logo: QLabel = logo 

        pixmapLogo : QPixmap = QPixmap("ressources/logo.jpg")
        self.logo.setPixmap(pixmapLogo)

        #Gannt
        gannt_slot = self.findChild(QVBoxLayout,"ganntSlot")
        if gannt_slot is None:
            raise RuntimeError("gannt_slot introuvable")
        self.gannt_slot : QVBoxLayout = gannt_slot

        self.gannt = Gannt()
        
        self.gannt_slot.addWidget(self.gannt)
        self.gannt.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        ##Button configuration
        self.buttons = self.findChildren(QPushButton)
        for button in self.buttons :
            if button.objectName() == 'pushButton_Tasks' :
                b_Tasks = button
            elif button.objectName() == 'pushButton_Assignments' :
                b_Assignments = button
            elif button.objectName() == 'pushButton_operators' :
                b_Operators = button
            elif button.objectName() == 'pushButton_machines' :
                b_Machines = button
            elif button.objectName() == 'pushButton_updateGannt' :
                b_updateGannt = button
            elif button.objectName() == 'pushButton_stat' :
                b_Stat = button
            else :
                raise unkownButton_error("The button named : " + str(button.objectName) + "is not configured in source code !")
                
        b_Operators.pressed.connect(lambda: self.open_second_widget("operators_widget")) 
        b_Assignments.pressed.connect(lambda: self.open_second_widget("assignments_widget")) 
        b_Tasks.pressed.connect(lambda: self.open_second_widget("tasks_widget")) 
        b_Machines.pressed.connect(lambda: self.open_second_widget("machines_widget")) 
        b_Stat.pressed.connect(lambda: self.open_second_widget("stat_widget")) 
        b_updateGannt.pressed.connect(lambda: self.actualiser()) 
                
    def open_second_widget(self,widget_name):
            # Create and show the second widget
            if widget_name == "operators_widget":
                self.second_widget = OperatorsWidget()
                self.second_widget.show()
            if widget_name == "assignments_widget":
                self.second_widget = AssignmentsWidget()
                self.second_widget.show()
            if widget_name == "tasks_widget":
                self.second_widget = TasksWidget()
                self.second_widget.show()
            if widget_name == "machines_widget":
                self.second_widget = MachinesWidget()
                self.second_widget.show()
            if widget_name == "stat_widget":
                self.second_widget = StatWidget()
                self.second_widget.show()

    def actualiser(self):
        self.gannt_slot.removeWidget(self.gannt)
        self.gannt = Gannt(modifiable=False)
        self.gannt_slot.addWidget(self.gannt)
                

# Execution
app = QApplication(sys.argv)
#main_window = MainWindow()
logwindow = LoginWidget()
logwindow.show()
sys.exit(app.exec())
