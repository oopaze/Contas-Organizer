from abc import abstractclassmethod
from tkinter import Frame, font

from app.src.settings import APP_HEIGHT, APP_WIDTH
from .DefaultLabel import Label


class Frame(Frame):
    title = ""

    def __init__(self, *args, **kwargs):
        kwargs.update({'width': APP_WIDTH, 'height': APP_HEIGHT - 30})
        super().__init__(*args, **kwargs)

        self.id = list(self.master.children.keys())[-1]
        self.title = Label(self, text=self.title, font=("Monospace", 18))
        self.title.place(x=150, y=30, width=400, height=30)

        self.build_widgets()

    @property
    def name(self):
        return "!" + self.__class__.__name__.lower()

    @abstractclassmethod
    def build_widgets(self, *args, **kwargs):
        pass

    def place(self, *args, x=0, y=30, **kwargs):
        return super().place(*args, x=x, y=y, **kwargs)

    def switch_screen(self, to: str, **kwargs):
        self.destroy()
        screen_class = self.master.screens[to]
        screen_class(self.master).place(**kwargs)

    def logout_user(self):
        self.master.auth.access = ""
        self.master.auth.refresh = ""

        self.switch_screen(to="login")
