from tkinter import Button

from app.src import settings


class Button(Button):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                'fg': settings.DEFAULT_BUTTON_FG_COLOR,
                'bg': settings.DEFAULT_BUTTON_BG_COLOR,
            }
        )

        super().__init__(*args, **kwargs)

    def place(self, *args, width=200, height=45, **kwargs):
        return super().place(*args, width=width, height=height, **kwargs)
