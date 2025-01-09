import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from db_managment import DbManagment

class Gui:

    def __init__(self):

        self.db = DbManagment()
        self.user_id = 1

        self.orderby = "title"
        self.order = "DESC"

        self.login_root = None
        self.main_root = None

        self.tree = None
        self.count_in_tree = 1

        self.title_entry = None
        self.date_entry = None
        self.score_entry = None
        self.note_text = None
        self.console_entry = None
    
    def start_main_root(self):
        """Iniciate the main root"""
        self.main_root = tk.Tk()
        self.main_root.title("Game List")
        self.main_root.geometry("800x500")

        top_frame = tk.Frame(self.main_root, bg="gray22")
        top_frame.pack( fill="x")

        add_button = tk.Button(top_frame, text="+ADD", fg="white", bg="green", command=self.start_add_window)
        add_button.pack(padx=8,pady=8,side="left")

        filter_combobox = ttk.Combobox(top_frame, values=["Título", "Fecha", "Consola", "Puntaje"])
        filter_combobox.set("Título")
        filter_combobox.pack(padx=8,pady=8,side="right")
        #filter_combobox.bind("<<ComboboxSelected>>", pass)

        asc_desc_button = tk.Button(top_frame, text="ASC", bg="lightgray")
        asc_desc_button.pack(padx=5,pady=8, side="right")

        self.tree = ttk.Treeview(self.main_root)

        self.tree["columns"] = ("title", "date", "console", "score", "note")
        self.tree.column("#0",width=50 ,minwidth=50, anchor="w")  # Columna principal (la que no se nombra)
        self.tree.column("title", width=200,minwidth=200, anchor="center")
        self.tree.column("date", width=100,minwidth=100, anchor="center")
        self.tree.column("console", width=70,minwidth=70, anchor="center")
        self.tree.column("score", width=70,minwidth=70, anchor="center")
        self.tree.column("note", width=300,minwidth=300, anchor="center")

        self.tree.heading("#0", text="ID", anchor="center")
        self.tree.heading("title", text="Título", anchor="center")
        self.tree.heading("date", text="Fecha", anchor="center")
        self.tree.heading("console", text="Consola", anchor="center")
        self.tree.heading("score", text="Puntaje", anchor="center")
        self.tree.heading("note", text="Nota", anchor="center")

        self.tree.pack(fill="both", expand=1)

        self.update_tree()

        self.main_root.mainloop()

    def insert_to_tree(self, title, date, console, score, note):
        """Insert an item in the tree"""
        idx = str(self.count_in_tree)
        self.tree.insert("", "end", idx, text=idx, values=(title, date, console,score,note))
        self.count_in_tree += 1

    def add_game(self):
        """Add a game automatically to db"""
        title = self.title_entry.get()
        date = self.date_entry.get()
        score = self.score_entry.get()
        console = self.console_entry.get()
        note = self.note_text.get("1.0", "end")
        self.db.insert_to_db(title, date, score,console,note, self.user_id)
        self.update_tree()

    def clear_tree(self):
        """Clear all the items in the tree"""
        for i  in range(self.count_in_tree - 1):
            self.tree.delete(str(i + 1))
        self.count_in_tree = 1

    def start_add_window(self):
        root = tk.Toplevel(self.main_root)
        
        title_label = tk.Label(root,text="Título:")
        title_label.grid(row=0,column=0,padx=10,pady=5, sticky="w")
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=1,column=0,columnspan=2, sticky="we", padx=10)

        date_label = tk.Label(root,text="Fecha:")
        date_label.grid(row=2,column=0, sticky="w",padx=10)
        self.date_entry = DateEntry(root, locale="es_ES", date_pattern="dd-mm-y")
        self.date_entry.grid(row=3, column=0,padx=10, columnspan=2 ,sticky="we")

        score_label = tk.Label(root,text="Puntaje:")
        score_label.grid(row=4,column=0, sticky="w",padx=10)
        self.score_entry = tk.Entry(root)
        self.score_entry.grid(row=5,column=0, padx=10,sticky="we")

        console_label = tk.Label(root, text="Consola:")
        console_label.grid(row=4,column=1, sticky="w",padx=10)
        self.console_entry = tk.Entry(root)
        self.console_entry.grid(row=5,column=1,padx=10, sticky="we")

        note_label = tk.Label(root, text="Nota:")
        note_label.grid(row=6,column=0, sticky="w",padx=10)
        self.note_text = tk.Text(root,height=5,width=35)
        self.note_text.grid(row=7, column=0, columnspan=2, sticky="swen",padx=10,pady=5)

        cancel_button = tk.Button(root,text="Cancelar", fg="white", bg="red",width=15,command=lambda:root.destroy())
        cancel_button.grid(row=8,column=0, pady=10)

        accept_button = tk.Button(root, text="Añadir", fg="white", bg="green",width=15,command=lambda : add())
        accept_button.grid(row=8, column=1, pady=10)

        def add():
            self.add_game()
            root.destroy()

        

    def update_tree(self):
        """Update the tree with all the games in db"""
        self.clear_tree()
        games_list = self.db.get_from_db(self.orderby,self.order)
        for game in games_list:
            self.insert_to_tree(game[0], game[1], game[2], game[3], game[4])

    def start_login_root(self):
        """Iniciate the root for login"""
        self.login_root = tk.Tk()




        self.login_root.mainloop()

g = Gui()
g.start_main_root()