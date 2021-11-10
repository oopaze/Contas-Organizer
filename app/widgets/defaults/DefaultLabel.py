from tkinter import Label


class Label(Label):
    def __init__(self, *args, font=("Arial", 12), **kwargs):
        super().__init__(*args, font=font, **kwargs)
