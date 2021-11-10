from tkinter import Entry


class Entry(Entry):
    def __init__(self, *args, placeholder="", font=("monospace", 9), **kwargs):
        super().__init__(*args, font=font, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = "grey"
        self.placeholder_font = ("monospace", 7)
        self.placeholder_on = True

        self.default_fg_color = self['fg']
        self.default_font = font

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def place(self, *args, width=200, height=30, **kwargs):
        return super().place(*args, width=width, height=height, **kwargs)

    def get(self, *args, **kwargs):
        if self.placeholder_on:
            return ""
        else:
            return super().get(*args, **kwargs)

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
        self.configure(font=self.placeholder_font)

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self.configure(font=self.default_font)
            self.placeholder_on = False

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self.placeholder_on = True
            self.configure(font=self.placeholder_font)
