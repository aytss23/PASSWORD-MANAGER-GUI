import user
import database
import graphics


if __name__ == '__main__': 
    
    #veritabanı yönetimi değişkeni
    mainDatabase = database.DatabaseManager()
    mainDatabase.checkPrerequisities()

    #kullanıcı yönetimi değişkeni    
    mainUser = user.User()
    
    #uygulama döngüsü oluşturma.
    mainApp = graphics.QApplication(graphics.argv)    
    
    mainApp.aboutToQuit.connect(mainDatabase.disconnectFromDatabase) # uygulama kapanırken veritabanı bağlantısını kapat 
    
    #uygulama arayüzünü oluşturma
    mainWindow = graphics.MainScreenWindow()
    mainWindow.show()
    
    mainApp.exec_()
