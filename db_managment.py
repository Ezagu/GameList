import sqlite3

class DbManagment:

    def __init__(self):
        self.path = ("videogames.db")
        self.conn = sqlite3.connect(self.path)

    def get_from_db(self, orderby = "title", order = "ASC"):
        """Return all values of the table games"""

        query = f'''
        SELECT title, date, score, console, note FROM games ORDER BY {orderby} {order}
        '''

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error:
            print("Error con sqlite")

    def insert_to_db(self, title, date, score, console, note, userid = 1):
        query = '''
        INSERT INTO games (title,date,score,console,note,user_id) VALUES(?,?,?,?,?,?)
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query,(title,date,score,console,note,userid))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error:
            print("Error con sqlite")

    def eliminate_game_in_db(self,title):
        query='''
        DELETE FROM games WHERE title = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query,(title,))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error:
            print("Error con sqlite")
