from tkinter.constants import END
from app.screens.home import HomeScreen

from app.widgets.defaults import DefaultButton, DefaultEntry, DefaultLabel, DefaultFrame
from app.src.settings import APP_HEIGHT, APP_WIDTH


class LoginScreen(DefaultFrame.Frame):
    title = "Log In"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_widgets(self):
        self.username_l = DefaultLabel.Label(self, text="Username")
        self.username_e = DefaultEntry.Entry(
            self, placeholder="Type your username here"
        )
        self.username_l.place(x=200, y=90)
        self.username_e.place(x=200, y=110)

        self.password_l = DefaultLabel.Label(self, text="Password")
        self.password_e = DefaultEntry.Entry(self, placeholder="********", show="*")
        self.password_l.place(x=200, y=160)
        self.password_e.place(x=200, y=180)

        self.button = DefaultButton.Button(
            self, text="Entrar", command=self.perform_login
        )
        self.button.place(x=200, y=240)

    def clean_entries(self):
        self.password_e.delete(0, END)

    def perform_login(self):
        username = self.username_e.get()
        password = self.password_e.get()

        is_authenticated = self.master.auth.login(username, password)

        if not (username and password):
            self.master.show_message("Os campos username e password são obrigatórios")

        elif is_authenticated:
            self.clean_entries()
            self.switch_screen(to="home")
            self.master.show_message("Usuário logado com sucesso", flag="info")

        else:
            self.master.show_message("Credenciais incorretas")
            self.clean_entries()
