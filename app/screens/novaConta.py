from tkinter.constants import END
from tkinter.ttk import Combobox

from app.services.api.client import Client
from app.widgets.defaults.DefaultFrame import Frame
from app.widgets.defaults.DefaultButton import Button
from app.widgets.defaults.DefaultEntry import Entry
from app.widgets.defaults.DefaultLabel import Label


class NovaContaScreen(Frame):
    title = "Nova Conta"
    METODOS_DE_PAGAMENTO = ("Cartão", "A vista", "A prazo")
    METODOS_DE_PAGAMENTO_DICT = {
        "Cartão": "cartao",
        "A vista": "a_vista",
        "A prazo": "a_prazo",
    }
    inputs = []
    form_fields = [
        ("Comprador", "entry", "comprador"),
        ("Loja", "entry", "loja"),
        ("Produto", "entry", "produto"),
        ("Método de Pagamento", "", ""),
        ("Valor", "int_entry", "valor"),
        ("Parcelas", "int_entry", "parcelas"),
        ("Data de Pagamento", "entry", "data_de_pagamento"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = Client(token=self.master.auth.access)

    def build_widgets(self):
        for i, data in enumerate(self.form_fields):
            x, y = 130, (i * 50) + 80
            if i / 4 >= 1:
                x, y = 370, y - 200

            Label(self, text=data[0]).place(x=x, y=y + 5, height=20)
            widget_kwargs = {}
            widget = Entry

            if 'int' in data[1]:
                widget_kwargs['validatecommand'] = (
                    self.master._validations['only_number'],
                    "%s",
                )

            if data[1]:
                initialized_widget = widget(self, **widget_kwargs)
                initialized_widget.place(x=x, y=y + 25, height=25, width=200)

                self.inputs.append({data[2]: initialized_widget})

        pagamentoCombobox = Combobox(self, values=self.METODOS_DE_PAGAMENTO)
        pagamentoCombobox.place(x=130, y=(3 * 50) + 105, width=200)
        self.inputs.append({"metodo_de_pagamento": pagamentoCombobox})

        submit = Button(self, text="Salvar", command=self.submit_form)
        submit.place(x=240, y=300, width=100, height=30)
        voltar = Button(
            self, text="Voltar", command=lambda: self.switch_screen(to='home')
        )
        voltar.place(x=360, y=300, width=100, height=30)

    def submit_form(self):
        data = self.validate_form()
        if data:
            data['metodo_de_pagamento'] = self.METODOS_DE_PAGAMENTO_DICT[
                data['metodo_de_pagamento']
            ]
            self.client.conta.create(data=data)
            self.clean_form()
            self.switch_screen(to="home")

    def clean_form(self):
        for field in self.inputs:
            field_name = list(field.keys())[0]
            field[field_name].delete(0, END)

    def validate_form(self):
        is_null = lambda char: not char
        is_digit = lambda char: not (
            char.isnumeric() or char.replace(".", "").isnumeric()
        )
        is_valid_option = lambda char, options: char not in options
        is_date = lambda char: not (
            len(char) == 10 and char[2] == '/' and char[5] == '/'
        )

        all_data = {}

        for field in self.inputs:
            field_name = list(field.keys())[0]
            try:
                data = field[field_name].get()

            except TypeError:
                data = field[field_name].current()

            if is_null(data):
                self.master.show_message("Todos os campos são obrigatórios")
                return False

            if field_name == 'metodo_de_pagamento' and is_valid_option(
                data, self.METODOS_DE_PAGAMENTO
            ):
                self.master.show_message("Método de Pagamento Inválido")
                return False

            if field_name == 'data_de_pagamento' and is_date(data):
                self.master.show_message("Data deve ter o padrão 01/01/2000")
                return False

            if field_name in ('valor', 'parcelas') and is_digit(data):
                self.master.show_message(f"O campo {field_name} deve ser numérico")
                return False

            all_data[field_name] = data

        return all_data
