import base64

from tkinter import Tk

from app.services.api.authentication import AuthUser

from .screens.home import HomeScreen
from .screens.login import LoginScreen
from .screens.novaConta import NovaContaScreen
from .widgets.MessageFrame import MessageFrame
from .widgets.defaults.DefaultEntry import Entry
from .src.settings import ALERTS, APP_WIDTH, APP_HEIGHT

from .services.api.client import Client


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_base()
        self.client = Client()
        self.auth = AuthUser(self.client, self)

        self.screens = {
            "home": HomeScreen,
            "login": LoginScreen,
            "novaConta": NovaContaScreen,
        }

        self.build_widgets()

    def configure_base(self):
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(0, 0)
        self.title("Contas Organizer - v1.0")

    def build_widgets(self):
        self.message_frame = MessageFrame(self)

        self.screens['login'](self).place()

    def show_message(self, text, flag='danger'):
        color_conf = ALERTS.get(flag, {})
        self.message_frame.new_message(text=text, conf=color_conf)
        self.message_frame.place(x=0, y=0)

    def run(self):
        self.mainloop()
