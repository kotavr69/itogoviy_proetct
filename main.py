import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()
        self.view_records()

    # метод инициализации виджетов
    def init_main(self):
        # тулбар
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # кнопка добавления
        # PhotoImage - добавленное изображение
        self.add_img = tk.PhotoImage(file='./img/add.png')
        # image - картинка, которая размещена на кнопке
        # bg - фон
        # bd - граница
        btn_add = tk.Button(toolbar, text='Добавить',
                            image=self.add_img,
                            bg='#d7d7d7', bd=0,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # кнопка редактирования
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, image=self.upd_img,
                            bg='#d7d7d7', bd=0,
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)

        # кнопка удаления
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, image=self.del_img,
                            bg='#d7d7d7', bd=0,
                            command=self.del_records)
        btn_del.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, image=self.search_img,
                               bg='#d7d7d7', bd=0,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, image=self.refresh_img,
                                bg='#d7d7d7', bd=0,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # таблица для вывода информации для сотрудников
        self.tree = ttk.Treeview(self,
                                 columns=('ID', 'name', 'phone', 'email', 'sallary'),
                                 show='headings', height=20)
        # настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('phone', width=100, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('sallary', width=150, anchor=tk.CENTER)

        # задаём подписи столбцам
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Email')
        self.tree.heading('sallary', text='Зарплата')

        self.tree.pack()

        # создание скроллбара
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # метод добавления в базу данных (посредник)
    def record(self, name, phone, email, sallary):
        self.db.insert_data(name, phone, email, sallary)
        self.view_records()

    # метод редактирования
    def upd_record(self, name, phone, email, sallary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE users SET name = ?, phone = ?, email = ?, sallary = ?
            WHERE id = ?
            ''', (name, phone, email, sallary, id))
        self.db.conn.commit()
        self.view_records()

    # метод удаления
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM users WHERE id = ?',
                                (self.tree.set(i, '#1'), ))
        self.db.conn.commit()
        self.view_records()
        
    # метод поиска
    def search_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users WHERE name LIKE ?', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM users')
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # метод открытия окна добавления
    def open_child(self):
        Child()

    # метод открытия окна редактирования
    def open_update(self):
        Update()

    # метод открытия окна поиска
    def open_search(self):
        Search()


# класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
       super().__init__(root)
       self.view = app
       self.init_child()

    # метод для создания виджетов дочернего окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('450x260')
        self.resizable(False, False)
        # перехватываем события, происходящии в приложении
        self.grab_set()
        # перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Email')
        label_sallary = tk.Label(self, text='Зарплата')

        label_name.place(x=60, y=50)
        label_phone.place(x=60, y=80)
        label_email.place(x=60, y=110)
        label_sallary.place(x=60, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_sallary = tk.Entry(self)

        self.entry_name.place(x=220, y=50)
        self.entry_phone.place(x=220, y=80)
        self.entry_email.place(x=220, y=110)
        self.entry_sallary.place(x=220, y=140)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=220, y=170)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.view.record(self.entry_name.get(),
                                                     self.entry_phone.get(),
                                                     self.entry_email.get(),
                                                     self.entry_sallary.get()))
        self.btn_ok.place(x=290, y=170)


# класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.defoult_data()

    def init_update(self):
        self.title('Редактирование данных о сотруднике')
        self.btn_ok.destroy()
        self.btn_upd = tk.Button(self, text='Сохранить')
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.view.upd_record(self.entry_name.get(),
                                                          self.entry_phone.get(),
                                                          self.entry_email.get(),
                                                          self.entry_sallary.get()))
        self.btn_upd.bind('<Button-1>',
                          lambda ev: self.destroy(),
                          add='+')
        self.btn_upd.place(x=290, y=170)

    # метод автозаполнения формы
    def defoult_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', id)
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_sallary.insert(0, row[4])


# класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
       super().__init__(root)
       self.view = app
       self.init_search()

    # метод для создания виджетов дочернего окна
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        # перехватываем события, происходящии в приложении
        self.grab_set()
        # перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=40, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=140, y=20)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=130, y=70)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',
                             lambda ev: self.destroy(),
                             add='+')
        self.btn_ok.place(x=220, y=70)


# класс базы данных
class Db:
    # создание соединения, курсоров и таблицы (если её нет)
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         sallary TEXT
            )''')

    # метод добавления в базу данных
    def insert_data(self, name, phone, email, sallary):
        self.cur.execute('''
                INSERT INTO users (name, phone, email, sallary)
                VALUES (?, ?, ?, ?)
        ''', (name, phone, email, sallary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()

    root.mainloop()
