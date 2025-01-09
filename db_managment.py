import sqlite3

class DbManagment:

    def __init__(self):
        self.path = ("videogames.db")
        self.conn = sqlite3.connect(self.path)

    def get_from_db(self, orderby = "title", order = "ASC"):
        """Return all values of the table games"""

        query = f'''
        SELECT title, date, console, score, note FROM games ORDER BY {orderby} {order}
        '''

        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error:
            print("Error con sqlite")

    def insert_to_db(self, title, date, console, score, note, userid = 1):
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

    def update_game(self, old_title, new_title, new_date, new_console, new_score, new_note):
        query='''
        UPDATE games SET title = ?, date = ?, console = ?, score = ?, note = ? WHERE title = ?
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(query,(new_title, new_date, new_console, new_score, new_note, old_title))
            self.conn.commit()
            cursor.close()
        except sqlite3.Error:
            print("Error con sqlite")