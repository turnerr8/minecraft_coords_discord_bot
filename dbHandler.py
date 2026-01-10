import sqlite3

class DbHandler:

    def __init__(self, db_path="data/coords.db"):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        print(f'connection to {db_path} successful!')
        self._init_db()

    def _init_db(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS coords (id INTEGER PRIMARY KEY, label TEXT, x INT, y INT, z INT, created_by TEXT)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_coords_label_creator ON coords (label, created_by)")
        self.connection.commit()

    def close(self):
        self.connection.close()

    def add(self, label: str, x:int, y:int, z:int, createdBy:str):
        try:
           
            #insert query
            insertQuery = "INSERT INTO coords (label, x, y, z, created_by) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(insertQuery, (label, x, y, z, createdBy))

            #save changes
            self.connection.commit()
            print('record saved!')
            return 1
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return e


    def remove(self, label, createdBy):
        try:
          
            #if the row doesnt exist return and send error message
            amount = self.howManyRows(label, createdBy)
            
            if (amount < 1):
                print("looks like there isn't an entry like this!")
                return 0

            removeQuery = "DELETE FROM coords WHERE label=(?) AND created_by=(?)"
            self.cursor.execute(removeQuery, (label, createdBy))

            self.connection.commit()
            return f'Removed {label} created by {createdBy}'
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0

    def howManyRows(self, label, createdBy):
        try:
            
            selectQuery = "SELECT COUNT(*) FROM coords WHERE label=(?) AND created_by=(?)"
            self.cursor.execute(selectQuery, (label, createdBy))
            return self.cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0
    def list(self): 
        try:
           
            self.cursor.execute("SELECT label, x, y, z, created_by FROM coords")
            rows= self.cursor.fetchall()
            return "\n".join(
                f"**{label}**: x:{x} y:{y} z:{z} ({created_by})"
                for label, x, y, z, created_by in rows
            )
            
        except sqlite3.Error as e:
            print(f'error occured: {e}')
            return 0
        
    #find all matching entries
    def find(self, label:str):
        try:
            query = "SELECT label, x, y, z, created_by FROM coords WHERE label=(?)"

            self.cursor.execute(query, (label,))
            rows = self.cursor.fetchall()
            if len(rows) < 1:
                return "no entries matching that label"
            return "\n".join(
                f"**{label}**: x:{x} y:{y} z:{z} ({created_by})"
                for label, x, y, z, created_by in rows
            )
        except sqlite3.Error as e:
            print(f'{e}')
