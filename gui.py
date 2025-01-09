import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db_managment import DbManagment


class Gui:

    def __init__(self):

        self.db = DbManagment()
        self.user_id = 1

        self.orderby = "title"
        self.order = "ASC"

        self.login_root = None
        self.main_root = None

        self.tree = None
        self.count_in_tree = 1

        self.title_entry = None
        self.date_entry = None
        self.score_entry = None
        self.note_text = None
        self.console_entry = None

        self.contextual_menu = None
        
    
    def start_main_root(self):
        """Iniciate the main root"""
        self.main_root = tk.Tk()
        self.main_root.title("Game List")
        self.main_root.geometry("800x500")

        top_frame = tk.Frame(self.main_root, bg="gray22")
        top_frame.pack(fill="x")

        add_button = tk.Button(top_frame, text="+ADD", fg="white", bg="green", command=self.start_add_window)
        add_button.pack(padx=8,pady=8,side="left")

        def change_filter_mode(events):
            option = filter_combobox.get()
            values = {
                "Título":"title",
                "Fecha":"date",
                "Consola":"console",
                "Puntaje":"score"
            }
            self.orderby = values[option]
            self.update_tree()

        filter_combobox = ttk.Combobox(top_frame, values=["Título", "Fecha", "Consola", "Puntaje"], state="readonly")
        filter_combobox.set("Título")
        filter_combobox.pack(padx=8,pady=8,side="right")
        filter_combobox.bind("<<ComboboxSelected>>", change_filter_mode)

        def toggle_order():
            self.order = "ASC" if self.order == "DESC" else "DESC"
            asc_desc_button.config(text=self.order)
            self.update_tree()

        asc_desc_button = tk.Button(top_frame, text="ASC", bg="lightgray", command=toggle_order)
        asc_desc_button.pack(padx=5,pady=8, side="right")

        def click_MBR(event):
            row = self.tree.identify_row(event.y)
            if row:
                self.tree.selection_set(row)
                self.show_contextual_menu(event)

        self.tree = ttk.Treeview(self.main_root)
        self.tree.bind("<Double-1>", lambda x :self.start_add_window(True))
        self.tree.bind("<Button-3>", lambda event:click_MBR(event))

        self.tree["columns"] = ("title", "date", "console", "score", "note")
        self.tree.column("#0",width=50 ,minwidth=50, anchor="w")
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

        def delete():
            result = messagebox.askokcancel("Confirmar", "¿Desea eliminar los datos?\nya no se podrán recuperar")
            if result:
                idx = self.tree.selection()
                title = self.tree.item(idx[0],"values")[0]
                self.delete_in_db(title)
                self.update_tree()

        self.contextual_menu = tk.Menu(self.main_root, tearoff=0)
        self.contextual_menu.add_command(label="Editar", command=lambda:self.start_add_window(modify=True))
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="Eliminar", command=delete)

        self.update_tree()

        self.main_root.mainloop()

    def start_add_window(self, modify:bool = False):
        root = tk.Toplevel(self.main_root)

        root.grab_set() #Bloquea la ventana principal
        
        title_label = tk.Label(root,text="Título:")
        title_label.grid(row=0,column=0,padx=10,pady=5, sticky="w")
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=1,column=0,columnspan=2, sticky="we", padx=10)

        date_label = tk.Label(root,text="Fecha:")
        date_label.grid(row=2,column=0, sticky="w",padx=10)
        self.date_entry = DateEntry(root, locale="es_ES", date_pattern="dd-mm-y", state="readonly")
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

        if not modify:
            #Si es para añadir un juego
            cancel_button = tk.Button(root,text="Cancelar", fg="white", bg="red",width=15,command=lambda:root.destroy())
            cancel_button.grid(row=8,column=0, pady=10)

            accept_button = tk.Button(root, text="Añadir", fg="white", bg="green",width=15,command=lambda : add())
            accept_button.grid(row=8, column=1, pady=10)

            def add():
                self.add_game()
                root.destroy()
        else:
            #Para modificar un juego
            idx = self.tree.selection()
            data = self.tree.item(idx[0],"values")
            title = data[0]
            date = data[1]
            console = data[2]
            score = data[3]
            note = data[4]

            self.title_entry.insert(0,title)
            self.date_entry.set_date(date)
            self.console_entry.insert(0,console)
            self.score_entry.insert(0,score)
            self.note_text.insert("1.0",note)

            frame_buttons = tk.Frame(root)
            frame_buttons.grid(row=8, column=0, columnspan=2, padx=10)

            cancel_button = tk.Button(frame_buttons,text="Cancelar", fg="white", bg="red",width=15,command=lambda:root.destroy())
            cancel_button.grid(row=0,column=0, pady=10, padx=5)

            def eliminate():
                result = messagebox.askokcancel("Confirmar", "¿Desea eliminar los datos?\nya no se podrán recuperar")
                if result:
                    self.delete_in_db(title)
                    root.destroy()
                    self.update_tree()

            delete_button = tk.Button(frame_buttons,text="Eliminar", fg="white", bg="red",width=15,command=eliminate)
            delete_button.grid(row=0,column=1, pady=10, padx=5)

            def update():
                data = self.get_data_entry()
                self.db.update_game(old_title=title, new_title=data[0],
                                     new_date=data[1], new_console=data[2], 
                                     new_score=data[3], new_note=data[4])
                root.destroy()
                self.update_tree()


            save_button = tk.Button(frame_buttons,text="Guardar", fg="white", bg="green",width=15,command=update)
            save_button.grid(row=0,column=2, pady=10, padx=5)

    def show_contextual_menu(self, event):
        """Pop up the contextual menu edit/delete"""
        self.contextual_menu.tk_popup(event.x_root, event.y_root)

    def delete_in_db(self,title):
        """Delete an element in db with the title"""
        self.db.eliminate_game_in_db(title)

    def insert_to_tree(self, title, date, console, score, note):
        """Insert an item in the tree"""
        idx = str(self.count_in_tree)
        self.tree.insert("", "end", idx, text=idx, values=(title, date, console,score,note))
        self.count_in_tree += 1

    def get_data_entry(self):
        """Return the data from the entrys (title, date, console, score, note)"""
        t = self.title_entry.get()
        d = self.date_entry.get()
        c = self.console_entry.get()
        s = self.score_entry.get()
        n = self.note_text.get("1.0", "end")
        return (t,d,c,s,n)

    def add_game(self):
        """Add a game automatically to db"""
        data = self.get_data_entry()
        self.db.insert_to_db(data[0], data[1], data[2],data[3],data[4], self.user_id)
        self.update_tree()

    def delete_tree_item(self, idx):
        """delete an item in the tree with the index"""
        self.tree.delete(idx)

    def clear_tree(self):
        """Clear all the items in the tree"""
        for i  in range(self.count_in_tree - 1):
            self.delete_tree_item(str(i+1))
        self.count_in_tree = 1

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