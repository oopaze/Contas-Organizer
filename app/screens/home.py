from datetime import datetime, timedelta
from random import randint
from tkinter.constants import CENTER, END, NO
from tkinter.ttk import Treeview

from app.widgets.defaults.DefaultFrame import Frame
from app.widgets.defaults.DefaultButton import Button
from app.src.settings import APP_HEIGHT, APP_WIDTH


class HomeScreen(Frame):
    def __init__(self, *args, **kwargs):
        self.columns = [
            ("ID", "id"),
            ("Comprador", "comprador"),
            ("Valor", "valor"),
            ("Data de Compra", "data_de_compra"),
            ("Data de Pagamento", "data_de_pagamento"),
        ]

        super().__init__(*args, **kwargs)

    def build_widgets(self, *args, **kwargs):
        sair = Button(self, text="Sair", command=self.perform_sair)
        sair.place(x=510, y=10, width=80, height=25)

        self.table = Treeview(self)
        self.table.place(x=10, y=80, width=APP_WIDTH - 20, height=APP_HEIGHT - 120)
        self.configure_treeview()
        self.add_treeview_data()

    def perform_sair(self):
        self.master.show_message('Usuário deslogado com sucesso.', flag="success")
        self.switch_screen('login')

    def configure_treeview(self):
        self.table['columns'] = tuple(map(lambda column: column[1], self.columns))

        self.table.column("#0", width=0, stretch=NO)
        for column in self.table['columns']:
            width = 50

            if column == 'id':
                width = 20
            elif 'data' in column:
                width = 120
            elif column == 'valor':
                width = 40

            self.table.column(column, anchor=CENTER, width=width)

        self.table.heading("#0", text="", anchor=CENTER)
        for title, name in self.columns:
            self.table.heading(name, text=title, anchor=CENTER)

    def add_treeview_data(self, *args, **kwargs):
        for i, conta in enumerate(self.get_contas()):
            values = (
                conta['id'],
                conta['comprador'],
                conta['valor'],
                f"{conta['data_de_compra']: %d/%m/%Y}",
                f"{conta['data_de_pagamento']: %d/%m/%Y}",
            )
            self.table.insert(parent='', index=END, iid=i, text='', values=values)

    def get_contas(self):
        return [
            {
                "id": i,
                "comprador": "José Pedro",
                "valor": randint(1000, 10000) / 10,
                "data_de_compra": datetime.today(),
                "data_de_pagamento": datetime.today()
                + timedelta(days=randint(30, 150)),
            }
            for i in range(0, 50, 1)
        ]
