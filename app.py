import tkinter
from tkinter import font, Entry

from config import *


class Printer(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.buttons = []
        self.upper = False

        new_font = font.Font(family="dejavu sans", size=20)
        self.option_add("*Font", new_font)

        self.field = Entry(self, width=30, font=font.Font(family="dejavu sans", size=30))
        self.field.insert(0, 'Фамилия Имя')
        self.field.grid(row=1, columnspan=16, pady=(10, 10), padx=x_padding)

        self.draw_keyboard()
        self.change()

    def draw_keyboard(self):
        cur_row = 2
        cur_column = 0
        big = False

        for button in buttons:
            columnspan = 1

            if big:
                columnspan = 3
            elif cur_row == 3:
                columnspan = 2
            elif cur_row == 4:
                columnspan = 4

            button = tkinter.Button(self, text=button,
                                    height=button_height,
                                    width=button_size if not big else big_button_size,
                                    bg=bg_color,
                                    fg=fg_color,
                                    activebackground=active_color,
                                    activeforeground=fg_active_color,
                                    relief='raised',
                                    padx=padx,
                                    pady=pady,
                                    bd=bd,
                                    command=lambda x=button: self.select(x))
            self.buttons.append(button)
            button.grid(row=cur_row,
                        column=cur_column,
                        columnspan=columnspan,
                        padx=0 if not cur_column == 0 else x_padding
                        )

            cur_column += 1 if not big else 3

            if cur_column > 11 and cur_row == 2:
                cur_column = 0
                cur_row += 1
            elif cur_column > 10 and cur_row == 3:
                cur_column = 0
                cur_row += 1
            elif cur_column > 8 and cur_row == 4:
                big = True
                cur_row += 1
                cur_column = 0

    def select(self, value):
        if value == "СТЕРЕТЬ":
            self.field.delete(len(self.field.get()) - 1, tkinter.END)

        elif value == "ПРОБЕЛ":
            self.field.insert(tkinter.END, ' ')
            self.change()

        elif value == 'ЗАГЛАВН':
            self.change()

        else:
            if self.field.get() == default:
                self.field.delete(0, tkinter.END)

            self.field.insert(tkinter.END, value if not self.upper else value.upper())

            if self.upper:
                self.change()

    def change(self):
        if self.upper:
            method = 'lower'
        else:
            method = 'upper'
        for i in range(32):
            self.buttons[i]["text"] = getattr(self.buttons[i]["text"], method)()

        self.upper = not self.upper


if __name__ == '__main__':
    app = Printer()
    app.geometry("800x480")
    app.mainloop()
