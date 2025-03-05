import database
 
class User:

    USER_NICKNAME = None
    USER_PASSWORD = None
    USER_ID = None

    def __init__(self):
        while not self.loginUser(): continue 
        
    def checkUser(self): #ilgili parametreleri veritabanında aratır. 
        
        database.DatabaseManager.executeSQLQuery(f"SELECT * FROM USERS WHERE USER_NICKNAME = '{User.USER_NICKNAME}' AND USER_PASSWORD = '{User.USER_PASSWORD}'")
        database.DatabaseManager.QUERY_RESULTS = database.DatabaseManager.QUERY_RESULTS.fetchone()
        
        if database.DatabaseManager.QUERY_RESULTS == None: return False
        return True

    def getUserID(self): return database.DatabaseManager.QUERY_RESULTS[0] #kullanıcının ID değerini tespit eder.

    def createUser(self): #kullanıcı adı başında '@' karakteri ile girilirse yeni kullanıcı oluşturması için bu fonksiyon çalıştırılır.
        
        database.DatabaseManager.executeSQLQuery(f"INSERT INTO USERS (USER_NICKNAME, USER_PASSWORD) VALUES ('{User.USER_NICKNAME.lstrip("@")}', '{User.USER_PASSWORD}')")
        database.DatabaseManager.commitDatabase()
    
    def loginUser(self): #kullanıcı girişi için gerekli parametreleri alır ve kontrol eder. 
        
        def getUserNickname(): return str(input("\n\n#username(@nick for register): ")) #kullanıcı adı girişini sağlar.
        def getUserPassword(): return str(input("#password: ")) #şifre girişini sağlar.

        User.USER_NICKNAME = getUserNickname() #admin
        User.USER_PASSWORD = getUserPassword() #password

        if User.USER_NICKNAME.startswith("@"): self.createUser()

        if self.checkUser(): 
            User.USER_ID = self.getUserID()
            return True

        return False

    def logOutUser(self): pass #kullanıcının uygulamadan çıkış işlemlerini içerir.

