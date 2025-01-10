import sqlite3
import sys
import os
import shutil
from datetime import datetime

class DbManagment:

    def __init__(self):
        
        base_dir = os.path.join(os.getenv('APPDATA'), "GameList")
        os.makedirs(base_dir, exist_ok=True)

        self.path = os.path.join(base_dir, "database.db")

        if not os.path.exists(self.path):
            if getattr(sys, 'frozen', False):
                original_db = os.path.join(sys._MEIPASS, "database.db")
            else:
                original_db = os.path.join(
                    os.path.dirname(__file__), "database.db")
                
            shutil.copyfile(original_db, self.path)

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
        date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
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