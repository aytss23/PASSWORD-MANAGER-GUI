import sqlite3 as SQLiteDatabase


class DatabaseManager:

    #veritabanı için sabitler.
    DATABASE_NAME = "..\\database\\PASSWORD_MANAGER.db"

    USERS_TABLE_QUERY = """ CREATE TABLE IF NOT EXISTS "USERS" ("USER_ID" INTEGER NOT NULL UNIQUE, "USER_NICKNAME" TEXT NOT NULL, "USER_PASSWORD" TEXT NOT NULL, PRIMARY KEY("USER_ID" AUTOINCREMENT)) """
    PASSWORDS_TABLE_QUERY = """ CREATE TABLE IF NOT EXISTS "PASSWORDS" ("USER_ID" INTEGER, "PASSWORD_ID" INTEGER NOT NULL UNIQUE, "PASSWORD_TITLE" TEXT NOT NULL, "PASSWORD_DATA" TEXT NOT NULL, "LOG_DATE" TEXT NOT NULL, PRIMARY KEY("PASSWORD_ID" AUTOINCREMENT)) """

    DATABASE_CONNECTION = None #veritabanı bağlantı değişkeni
    DATABASE_CURSOR = None #veritabanı imleç değişkeni
    
    SQL_QUERY = None #veritabanında çalıştırılmak üzere sorgu değişkeni 

    QUERY_RESULTS = None #sorgu sonuçları değişkeni 

    def __init__(self): self.connectToDatabase() #yapıcı fonksiyon

    def connectToDatabase(self): #veritabanı bağlantısını gerçekleştirir.
        
        try: 
            DatabaseManager.DATABASE_CONNECTION = SQLiteDatabase.connect(DatabaseManager.DATABASE_NAME)
            DatabaseManager.DATABASE_CURSOR = DatabaseManager.DATABASE_CONNECTION.cursor()

        except Exception: print("[ERROR]: Unable to connect database.")
    
    def checkPrerequisities(self): #veritabanı için ön yeterlilikleri kontrol eder. eğer eksiklik varsa veritabanı ve tabloları oluşturur.
    
        self.executeSQLQuery(DatabaseManager.USERS_TABLE_QUERY)
        self.executeSQLQuery(DatabaseManager.PASSWORDS_TABLE_QUERY)

        self.commitDatabase()
    
    @staticmethod
    def fetchAllResults(): DatabaseManager.QUERY_RESULTS = DatabaseManager.QUERY_RESULTS.fetchall() #veritabanındaki sorgu sonuçlarının tamamını çeker. Varsa [()], Yoksa [] döndürür.
    
    @staticmethod
    def fetchOneResult(): return DatabaseManager.QUERY_RESULTS.fetchone() #veritabanındaki sorgu sonuçlarından sadece birini çeker. Varsa (), Yoksa None döndürür.

    @staticmethod
    def disconnectFromDatabase(): DatabaseManager.DATABASE_CONNECTION.close()#veritabanı bağlantısını sonlandırır.

    @staticmethod
    def commitDatabase(): DatabaseManager.DATABASE_CONNECTION.commit() #veritabanındaki değişiklikleri günceller.

    @staticmethod
    def executeSQLQuery(SQL_QUERY): DatabaseManager.QUERY_RESULTS = DatabaseManager.DATABASE_CURSOR.execute(SQL_QUERY) #veritabanında sorgu çalıştırır.