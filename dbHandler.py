import sqlite3

class DbHandler:


    def add(self, label: str, x:int, y:int, z:int, createdBy:str):
        try:
            #connect to DB
            connection = sqlite3.connect('coords.db')
            cursor = connection.cursor()
            print('connection successful')

            #if table does not exist, create one 
            cursor.execute("CREATE TABLE IF NOT EXISTS coords (id INTEGER PRIMARY KEY, label TEXT, x INT, y INT, z INT, created_by TEXT)")

            #insert query
            insertQuery = "INSERT INTO coords (label, x, y, z, created_by) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(insertQuery, (label, x, y, z, createdBy))

            #save changes
            connection.commit()
            print('record saved!')
            return 1
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return e


    def remove(self, label, createdBy):
        try:
           #connect to DB
            connection = sqlite3.connect('coords.db')
            cursor = connection.cursor()
            print('connection successful')

            #if table does not exist, create one 
            cursor.execute("CREATE TABLE IF NOT EXISTS coords (id INTEGER PRIMARY KEY, label TEXT, x INT, y INT, z INT, created_by TEXT)")

            #if the row doesnt exist return and send error message
            amount = self.howManyRows(label, createdBy)
            
            if (amount < 1):
                print("looks like there isn't an entry like this!")
                return 0

            removeQuery = "DELETE FROM coords WHERE label=(?) AND created_by=(?)"
            cursor.execute(removeQuery, (label, createdBy))

            connection.commit()
            return f'Removed {label} created by {createdBy}'
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0

    def howManyRows(self, label, createdBy):
        try:
            #connect to DB
            connection = sqlite3.connect('coords.db')
            cursor = connection.cursor()
            print('connection successful')

            #if table does not exist, create one 
            cursor.execute("CREATE TABLE IF NOT EXISTS coords (id INTEGER PRIMARY KEY, label TEXT, x INT, y INT, z INT, created_by TEXT)")

            selectQuery = "SELECT * FROM coords WHERE label=(?) AND created_by=(?)"
            cursor.execute(selectQuery, (label, createdBy))
            rows = cursor.fetchall()
            print(len(rows))
            return 1
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0
    def list(self): 
        try:
            #connect to DB
            connection = sqlite3.connect('coords.db')
            cursor = connection.cursor()
            print('connection successful')

            #if table does not exist, create one 
            cursor.execute("CREATE TABLE IF NOT EXISTS coords (id INTEGER PRIMARY KEY, label TEXT, x INT, y INT, z INT, created_by TEXT)")

            selectQuery = "SELECT * FROM coords"
            cursor.execute(selectQuery)
            res= cursor.fetchall()
            concatStr=''
            for line in res:
                concatStr += f'**{line[1]}**: x:{line[2]} y:{line[3]}, z:{line[4]}    ({line[5]})\n'

            print(concatStr)
            return concatStr
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0
#add("hello", 0, 0,0,"ryan")
# add("hello", 0, 0,0,"ryan")

# remove('hello', 'ryan')
#DbHandler.howManyRows('hello', 'ryan')
#DbHandler.list()
