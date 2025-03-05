from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QTableWidget
from PyQt5.QtCore import QTimer, QTime
from PyQt5 import QtGui
from sys import argv
import password
import database 
from datetime import datetime
from user import User
from random import choice, randint

class MainScreenWindow(QMainWindow):
    
    UI_PATH = "..\\ui\\main_window.ui" #arayüz dosya yolu
    
    TABLE_EDIT = False
    QUICK_MODE = False
    LOGIN_TIME = str(datetime.now().strftime("%y/%m/%d - %H:%M:%S"))

    def __init__(self):

        super().__init__()

        uic.loadUi(MainScreenWindow.UI_PATH, self) #arayüzü içeriye aktarır. 
    
        #buton fonksiyonları 
        self.generatePushButton.clicked.connect(self.generatePushButtonClicked)

        self.searchDataPushButton.clicked.connect(self.searchPushButtonClicked)
        
        self.appendDataPushButton.clicked.connect(self.appendPushButtonClicked)
        
        self.updateDataPushButton.clicked.connect(self.updatePushButtonClicked)
        
        self.deleteDataPushButton.clicked.connect(self.deletePushButtonClicked)
        
        self.listAllDataPushButton.clicked.connect(self.listAllPushButtonClicked)

        self.getSelectedRowDataPushButton.clicked.connect(self.getSelectedRowDataPushButtonClicked)
        
        self.logOutPushButton.clicked.connect(self.logOutPushButtonClicked)

        self.setTableEditPushButton.clicked.connect(self.setTableEditPushButtonClicked)
        
        self.refreshTableWidgetPushButton.clicked.connect(self.refreshTableWidgetPushButtonClicked)

        self.setQuickModePushButton.clicked.connect(self.setQuickModePushButtonClicked)

        self.truncateTablePushButton.clicked.connect(self.truncateTablePushButtonClicked)

        # kontrol kutucukları fonksiyonları

        self.numbersCheckBox.stateChanged.connect(self.numbersCheckBoxClicked)
        
        self.charactersCheckBox.stateChanged.connect(self.charactersCheckBoxClicked)
        
        self.specialCharactersCheckBox.stateChanged.connect(self.specialCharactersCheckBoxClicked)

        self.numbersCheckBox.setChecked(True)

        self.charactersCheckBox.setChecked(True)

        self.specialCharactersCheckBox.setChecked(True)
        
        # veri tablo sütun boyutlarını kilitler.
        self.dataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.dataTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        self.dataTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        #veri tablosunu oluşturur.
        
        self.selectedDataTableWidget.setRowCount(5)
        
        self.selectedDataTableWidget.setColumnCount(1)

        self.selectedDataTableWidget.setHorizontalHeaderLabels(["VALUES"])

        self.selectedDataTableWidget.setVerticalHeaderLabels(["USER", "ID", "TITLE", "DESC", "DATE", "POWER", "LENGTH"])

        # seçilen verinin bilgilerini gösteren tablonun özellikleri
        self.selectedDataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.selectedDataTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.selectedDataTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.selectedDataTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.selectedDataTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # oturum bilgilerinin sürekli olarak güncellenmesi için tanımlamalar. 
        self.sessionTimeInfo = QTimer(self)
        self.liveTimeInfo = QTime()

        self.sessionTimeInfo.timeout.connect(self.updateSessionInfo)
        self.sessionTimeInfo.start(1000)
        self.updateSessionInfo()

        self.setWindowStyleSheets()

        self.selectedRowData = []

    # oturum bilgilerini ve saati günceller. 
    def updateSessionInfo(self): self.loginDataLabel.setText(f""" id : {User.USER_ID} user: {User.USER_NICKNAME} login-time : {MainScreenWindow.LOGIN_TIME} | {QTime.currentTime().toString("HH:mm:ss")}""")

    #tablodan seçili satırın verisini alır. 
    def getSelectedRowDataPushButtonClicked(self): 

        selectedRow = self.dataTableWidget.currentRow()
        self.selectedRowData = []

        for selectedColumn in range(6): 
            
            if not self.dataTableWidget.item(selectedRow, selectedColumn) == None: 
                
                self.selectedRowData.append(str(self.dataTableWidget.item(selectedRow, selectedColumn).text()))
        
        try:

            self.passwordTitleLineEdit.setText(self.selectedRowData[2])
            self.passwordDataLineEdit.setText(self.selectedRowData[3])
        
        except Exception: pass

        self.updateSelectedDataTableWidget(self.selectedRowData)

        return self.selectedRowData 

       
    #arayüz görünümünü günceller.
    def setWindowStyleSheets(self): self.setWindowIcon(QtGui.QIcon("..\\images\\PASSWORD_MANAGER_LOGO.jpg"))

    def setQuickModePushButtonClicked(self): 
        if self.setQuickModePushButton.text() == "QUICK MODE - OFF": 
            database.DatabaseManager.executeSQLQuery("PRAGMA synchronous = OFF;")
            database.DatabaseManager.executeSQLQuery("PRAGMA journal_mode = MEMORY;")
            
            self.setQuickModePushButton.setText("QUICK MODE - ON")
        
        else: self.setQuickModePushButton.setText("QUICK MODE - OFF")
            

    #tablonun düzenlenme özelliğini açıp kapatır. 
    def setTableEditPushButtonClicked(self): 
        
        if self.setTableEditPushButton.text() == "TABLE EDIT - OFF": 
            self.setTableEditPushButton.setText("TABLE EDIT - ON") 
            self.dataTableWidget.setEditTriggers(QTableWidget.AllEditTriggers)

        else: 
            self.setTableEditPushButton.setText("TABLE EDIT - OFF")  
            self.dataTableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

    #tabloyu okuyup yeniden yazar.
    def refreshTableWidgetPushButtonClicked(self): 

        database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)
        database.DatabaseManager.fetchAllResults()

        self.updateTableWidget(database.DatabaseManager.QUERY_RESULTS, len(database.DatabaseManager.QUERY_RESULTS))

        '''
        tableData = []
        
        #tablodaki tüm veriyi oku 
        def readAllData():
            rowData = []
            
            for rowCount in range(self.dataTableWidget.rowCount()):
                for columnCount in range(self.dataTableWidget.columnCount()):
    
                    dataTableWidgetItem = self.dataTableWidget.item(rowCount, columnCount)
                    rowData.append(dataTableWidgetItem.text() if dataTableWidgetItem else "")
                
                tableData.append(rowData)
        
        def writeAllData():
            for rowCount, rowData in enumerate(tableData):
                for columnCount, columnData in enumerate(rowData): self.dataTableWidget.setItem(rowCount, columnCount, QTableWidgetItem(columnData))

        readAllData()
        writeAllData()
        '''

    #tabloyu tamamen silme fonksiyonu 
    def truncateTablePushButtonClicked(self): 

        database.DatabaseManager.executeSQLQuery("DELETE FROM PASSWORDS")        
        database.DatabaseManager.commitDatabase()

        database.DatabaseManager.fetchAllResults()

        self.updateTableWidget(database.DatabaseManager.QUERY_RESULTS, len(database.DatabaseManager.QUERY_RESULTS))

    #tabloda seçili veri ile ilgili parametreleri günceller. 
    def updateSelectedDataTableWidget(self, selectedData = None):
           
            if not selectedData == []:
                
                for rowCount in range(0,5): self.selectedDataTableWidget.setItem(0, rowCount, QTableWidgetItem(str(selectedData[rowCount])))
           
            else: pass

    #tabloyu düzenler ve verileri listeler
    def updateTableWidget(self, queryData, rowCount, columnCount = 5): 

        if queryData == []: pass

        self.dataTableWidget.setRowCount(rowCount)
        self.dataTableWidget.setColumnCount(columnCount)

        self.dataTableWidget.setHorizontalHeaderLabels(["USER-ID", "LOG-ID", "LOG-TITLE", "LOG-DESC", "LOG-DATE"]) #tablo sütun başlıkları

        for rowCount, rowData in enumerate(queryData):
            for columnCount, columnData in enumerate(queryData[rowCount]):
                self.dataTableWidget.setItem(rowCount, columnCount, QTableWidgetItem(str(columnData)))

        #tablo sütun genişlikleri
        self.dataTableWidget.setColumnWidth(0, 50)
        self.dataTableWidget.setColumnWidth(1, 70)
        self.dataTableWidget.setColumnWidth(2, 180)
        self.dataTableWidget.setColumnWidth(3, 509)
        self.dataTableWidget.setColumnWidth(4, 120)

    #append butonu fonksiyonu 
    def appendPushButtonClicked(self): 
        
        if self.passwordTitleLineEdit.text() == '' or self.passwordDataLineEdit.text() == '': return False

        #TEMP_TITLE_LIST = ["Instagram","LinkedIn", "Twitter", "Steam", "Pinterest", "Facebook", "Reddit", "E-Devlet", "AKBANK", "VakıfBank", "YapıKredi", "Ziraat Bankası", "Ekşi Sözlük", "OBS", "iCloud","Google","Gmail","Telegram", "GSB Wifi", "BTK Akademi", "Epic Games", "VALORANT", "League of Legends", "Grand Theft Auto V", "DenizBank", "OBilet", "Juzdan", "Papara", "Sahibinden.com", "Turk Telekom", "Dolap", "GSB Biz"]
    
        database.DatabaseManager.SQL_QUERY = f""" INSERT INTO PASSWORDS (USER_ID, PASSWORD_TITLE, PASSWORD_DATA, LOG_DATE) VALUES ('{User.USER_ID}', '{self.passwordTitleLineEdit.text()}', '{self.passwordDataLineEdit.text()}', '{str(datetime.now().strftime("%y/%m/%d - %H:%M:%S"))}') """
        database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)    

        database.DatabaseManager.commitDatabase()
    
        self.listAllPushButtonClicked()
    
        return True

    #arama butonu fonksiyonu
    def searchPushButtonClicked(self): 

        if self.searchInputLineEdit.text() == '': return False

        else: 
            
            database.DatabaseManager.SQL_QUERY = f""" SELECT * FROM PASSWORDS WHERE PASSWORD_TITLE LIKE '{self.searchInputLineEdit.text()}%' AND USER_ID = {User.USER_ID} """

            database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)
            
            database.DatabaseManager.fetchAllResults()

            self.updateTableWidget(database.DatabaseManager.QUERY_RESULTS, len(database.DatabaseManager.QUERY_RESULTS))

            return True

    #güncelleme butonu fonksiyonu 
    def updatePushButtonClicked(self): 
    


        if self.selectedRowData != [] and (self.passwordTitleLineEdit.text() != self.selectedRowData[2] or self.passwordDataLineEdit.text() != self.selectedRowData[3]): 
           
            database.DatabaseManager.SQL_QUERY = f""" UPDATE PASSWORDS SET PASSWORD_TITLE = '{self.passwordTitleLineEdit.text()}', PASSWORD_DATA = '{self.passwordDataLineEdit.text()}', LOG_DATE = '{str(datetime.now().strftime("%y/%m/%d - %H:%M:%S"))}' WHERE USER_ID = {User.USER_ID} AND PASSWORD_ID = {self.selectedRowData[1]} AND PASSWORD_TITLE = '{self.selectedRowData[2]}' AND PASSWORD_DATA = '{self.selectedRowData[3]}' """

            database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)

            database.DatabaseManager.commitDatabase()

            self.listAllPushButtonClicked()

            self.getSelectedRowDataPushButtonClicked()

    #silme butonu fonksiyonu
    def deletePushButtonClicked(self): 
        
        if not self.passwordTitleLineEdit.text() == '': 
            
            database.DatabaseManager.SQL_QUERY = f""" DELETE FROM PASSWORDS WHERE PASSWORD_TITLE = '{self.passwordTitleLineEdit.text()}' AND USER_ID = '{User.USER_ID}' AND PASSWORD_ID = '{self.selectedRowData[1]}' """

            database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)
            
            database.DatabaseManager.commitDatabase()

            self.listAllPushButtonClicked()

            return True
        
        else: return False 

    #tüm verileri listeleme fonksiyonu 
    def listAllPushButtonClicked(self): 

        database.DatabaseManager.SQL_QUERY = f""" SELECT * FROM PASSWORDS WHERE USER_ID = '{User.USER_ID}' """
        
        database.DatabaseManager.executeSQLQuery(database.DatabaseManager.SQL_QUERY)
        
        database.DatabaseManager.fetchAllResults()

        self.updateTableWidget(database.DatabaseManager.QUERY_RESULTS, len(database.DatabaseManager.QUERY_RESULTS))

        return True
    
    #şifre üretme butonu fonksiyonu
    def generatePushButtonClicked(self): 
        
        self.checkCheckBoxes()
        
        try: int(self.lengthInputLineEdit.text())
        
        except Exception: self.lengthInputLineEdit.setText('16')
        
        finally: 
            self.generateResultLineEdit.setText(password.generatePassword(int(self.lengthInputLineEdit.text())))
            self.passwordDataLineEdit.setText(str(self.generateResultLineEdit.text()))
    
    # çıkış tuşu tıklanınca çalıştırılacak işlemler. 
    def logOutPushButtonClicked(self): self.close() #uygulamayı kapat.

    # oluşturulacak şifrenin içerdiği karakterleri düzenleyen fonksiyonlar
    
    def numbersCheckBoxClicked(self): #sayıları ekler.

        if self.numbersCheckBox.isChecked(): password.INCLUDE_DICTIONARY['NUMBERS'] = True        
        else: password.INCLUDE_DICTIONARY['NUMBERS'] = False

    def charactersCheckBoxClicked(self): #karakterleri ekler.

        if self.charactersCheckBox.isChecked(): password.INCLUDE_DICTIONARY['CHARACTERS'] = True
        else: password.INCLUDE_DICTIONARY['CHARACTERS'] = False

    def specialCharactersCheckBoxClicked(self): #özel karakterleri ekler. 
        
        if self.charactersCheckBox.isChecked(): password.INCLUDE_DICTIONARY['SPECIAL_CHARACTERS'] = True
        else: password.INCLUDE_DICTIONARY['SPECIAL_CHARACTERS'] = False

    def checkCheckBoxes(self): #tüm karakterleri kontrol eder. 
        
        if not (self.numbersCheckBox.isChecked() or self.charactersCheckBox.isChecked() or self.specialCharactersCheckBox.isChecked()): 
            self.numbersCheckBox.setChecked(True)
            self.charactersCheckBox.setChecked(True)
            self.specialCharactersCheckBox.setChecked(True)
