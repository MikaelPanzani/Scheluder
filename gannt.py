from datetime import datetime, timedelta
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QSlider
from tools_function import conversionTableAssignementEnTableItem, getTaskSTR, records_table_paser, getMachineSTR
from PySide6.QtGui import QBrush, QColor, QMouseEvent
from PySide6.QtCore import Qt, QEvent
from jours_feries_france import JoursFeries



class Gannt(QTableWidget):
    def __init__(self, modifiable: bool = False):
            super(Gannt, self).__init__()

            self.vsliderPosition = 0
            self.hsliderPosition = 352

         # Generate date range: 10 days before today to 50 days after
            pastcast = 360
            forecast = 30*6
            start_date = datetime.today() - timedelta(days=pastcast)
            end_date = datetime.today() + timedelta(days=forecast)
            
            
            total_days = (end_date - start_date).days

            # Set number of columns based on the date range
            self.setColumnCount(total_days)

            # Create headers with formatted date strings
            headers = [(start_date + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(total_days)]
            self.setHorizontalHeaderLabels(headers)

            newItemc : QTableWidgetItem = self.horizontalHeaderItem(pastcast)
            newItemc.setBackground(QBrush(QColor('orange')))
            newItemc.setText(datetime.today().strftime("%d-%m-%Y"))

            ##Row & col managment
            dic_op_data,cop = records_table_paser("Operators")
            dic_assignement_data,ca = records_table_paser("Assignments")
            dic_tasks_data,ct = records_table_paser("Tasks")
            dic_machines_data,cm = records_table_paser("Machines")
            vertical_headers = []
            for id_enregistrement, dictData in dic_op_data.items():
                #Pour chaque record
                row_position = self.rowCount()
                self.insertRow(row_position)
                data_to_store = dictData['name'],dictData['id']
                vertical_headers.append(str(data_to_store[1]) +' : '+ str(data_to_store[0]))
            self.setVerticalHeaderLabels(vertical_headers)

            # Add a slider to the tab
            self.slider = QSlider(Qt.Orientation.Horizontal)
            self.slider.setMinimum(0)
            self.slider.setMaximum(100)
            self.slider.setValue(10)

            matrice_association = conversionTableAssignementEnTableItem(cop, forecast+pastcast, dic_assignement_data, start_date, dic_op_data)

            ##Filling gannt - par colonne
            #On récupère les jours ferie de l'année courante
            day_off_the_year : dict = JoursFeries.for_year(datetime.today().year)

            for num_col in range(forecast+pastcast) :
                #Date
                #Si la colonne correspond à une date invalide (week end jour férié on veut colorer en noir celle - ci)
                dateCourante = timedelta(days=num_col) + start_date
                isWeekend : bool = False
                ferie : bool = False
                if dateCourante.weekday() >= 5 :
                    isWeekend : bool = True
                elif dateCourante.date() in day_off_the_year.values() :
                    ferie : bool = True

                for num_row in range(cop) :
                    #Ope
                    newItem = QTableWidgetItem()
                    #Test si la colonne courante est un jour de week-end
                    if ferie :
                        newItem.setBackground(QBrush(QColor('black')))
                        newItem.setText("Férié") #Get tasks by id 
                        newItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    elif isWeekend :
                        newItem.setBackground(QBrush(QColor('black')))
                        newItem.setText("WeekEnd") #Get tasks by id 
                        newItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    else:
                         
                        if matrice_association[num_row,num_col][0] == -1:
                            newItem.setBackground(QBrush(QColor('green')))
                            
                        else:
                            
                            #newItem.setText(str(int(matrice_association[num_row,num_col]))) 
                            textItem,colorItem = getTaskSTR(int(matrice_association[num_row,num_col][0]), dic_tasks_data)
                            #J'enrichie textitem avec le str venant de la machine ID dans la cell de la matrice 
                            textItem += getMachineSTR(int(matrice_association[num_row,num_col][1]),dic_machines_data)
                            newItem.setText(textItem) #Get tasks by id 
                            newItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                            newItem.setBackground(QBrush(QColor(colorItem)))
                    #Perform test : does the current operator has a task on the current day ? yes - no
                    #If yes : the item shall represent the task
                    #If no : the item shall be green 
                    self.setItem(num_row,num_col,newItem)


            
            # Resize columns and rows to fit the contents
            self.resizeColumnsToContents()
            self.resizeRowsToContents()


    



            #Centre la vu de base sur aujourd'hui
            # today_position : int =  int(((351/517) * self.horizontalScrollBar().maximum())-10)
            """ self.horizontalScrollBar().setValue(hsliderPosition)
            print(vsliderPosition)
            self.verticalScrollBar().setValue(int(vsliderPosition))
            print(self.verticalScrollBar().value())"""
            #Example de connexion entre souris et slider
            #self.horizontalScrollBar().sliderMoved.connect(self.exemple_connect_souris_slider) 
            #print(f" valeur de la positon de la scrooll bar horizontale : {self.horizontalScrollBar().value()}")

    def exemple_connect_souris_slider(self):
        #Juste une fonction pour montrer comment on connecte la souris qui appui sur le slider voir audessus 
        print(self.horizontalScrollBar().value())

    def setVHSliderPosition(self, hsliderPosition : int, vsliderPosition : int ):
        self.hsliderPosition = hsliderPosition
        self.vsliderPosition = vsliderPosition
    
    def showEvent(self, event):
        super().showEvent(event)
        self.horizontalScrollBar().setValue(self.hsliderPosition)
        self.verticalScrollBar().setValue(self.vsliderPosition)