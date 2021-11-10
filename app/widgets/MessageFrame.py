from tkinter import Frame, Label, Button

from app.src.settings import APP_WIDTH


class MessageFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_widgets()

    def build_widgets(self):
        self.label = Label(self, text="")
        self.label.place(x=0, y=0, width=APP_WIDTH - 20, height=30)

        self.button = Button(
            self,
            text="x",
            borderwidth=0,
            highlightthickness=0,
            font=("monospace", 12),
            command=self.close,
        )
        self.button.place(x=APP_WIDTH - 30, y=5, width=20, height=20)

    def close(self):
        self.place_forget()

    def new_message(self, text, conf):
        self.label.configure(text=text, **conf)
        self.button.configure(**conf)
        self.configure(bg=conf['bg'])

    def place(self, *args, **kwargs):
        return super().place(*args, width=APP_WIDTH, height=30, **kwargs)
