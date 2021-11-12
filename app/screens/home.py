from datetime import datetime, timedelta
from random import randint
from tkinter.constants import CENTER, END, NO
from tkinter.ttk import Treeview
from app.services.api.client import Client

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
        self.client = Client(token=self.master.auth.access)
        self.add_treeview_data()

    def build_widgets(self, *args, **kwargs):
        nova_conta = Button(
            self, text="Adicionar", command=lambda: self.switch_screen(to='novaConta')
        )
        nova_conta.place(x=10, y=10, width=80, height=25)

        sair = Button(self, text="Sair", command=self.perform_sair)
        sair.place(x=510, y=10, width=80, height=25)

        self.table = Treeview(self)
        self.table.place(x=10, y=80, width=APP_WIDTH - 20, height=APP_HEIGHT - 120)
        self.configure_treeview()

    def perform_sair(self):
        self.master.show_message('Usuário deslogado com sucesso.', flag="success")
        self.logout_user()

    def configure_treeview(self):
        self.table['columns'] = tuple(map(lambda column: column[1], self.columns))

        self.table.column("#0", width=0, stretch=NO)
        self.table.heading("#0", text="", anchor=CENTER)
        for title, column in self.columns:
            width = 50

            if column == 'id':
                width = 20
            elif 'data' in column:
                width = 120
            elif column == 'valor':
                width = 40

            self.table.column(column, anchor=CENTER, width=width)
            self.table.heading(column, text=title, anchor=CENTER)

    def add_treeview_data(self, *args, **kwargs):
        for i, conta in enumerate(self.get_contas()):
            values = (
                conta['id'],
                conta['comprador'],
                conta['valor'],
                conta['data_de_compra'],
                conta['data_de_pagamento'],
            )
            self.table.insert(parent='', index=END, iid=i, text='', values=values)

    def get_contas(self):
        if self.master.auth.check_token(self.logout_user):
            response = self.client.parcela.list()

            if response.status_code == 200:
                return response.json()

            return []
