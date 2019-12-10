import os
import tkinter
from tkinter import font, Entry, Label

from PIL import Image, ImageDraw, ImageFont

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

        self.text = None

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
                columnspan = 2

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
            elif cur_column > 10 and cur_row == 4:
                big = True
                cur_row += 1
                cur_column = 0

    def select(self, value):
        if value == "СТЕРЕТЬ":
            self.field.delete(len(self.field.get()) - 1, tkinter.END)

            if len(self.field.get()) == 0:
                self.field.insert(tkinter.END, 'Фамилия Имя')
                self.change()

        elif value == "ПРОБЕЛ":
            self.field.insert(tkinter.END, ' ')
            self.change()

        elif value == 'ЗАГЛАВН':
            self.change()

        elif value == 'ПЕЧАТЬ':
            if self.field.get() == 'слизерин':
                self.progress_dialog = tkinter.Toplevel()
                text = Label(self.progress_dialog, text='Добро пожаловать')
                text.pack()

                import os

                os.popen('xfce4-terminal')

                # start keyboard
                os.popen('florence')

            else:
                self.progress_dialog = tkinter.Toplevel()
                self.text = Label(self.progress_dialog, text='Идет печать')
                self.text.pack()

                self.print()

                self.field.delete(0, tkinter.END)
                self.field.insert(tkinter.END, 'Фамилия Имя')

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
        for i in range(34):
            self.buttons[i]["text"] = getattr(self.buttons[i]["text"], method)()

        self.upper = not self.upper

    def print(self):
        # Step 1 - generate needed SVG

        W = 1000
        H = 310
        padding = 80

        text = self.field.get()

        text = list(reversed(text.split()))

        self.text['text'] = 'Создаем'
        img = Image.new('RGB', (W, H), color=(255, 255, 255))

        # TODO: do not hardcode path
        font = ImageFont.truetype('Ubuntu-Regular.ttf', 80)

        self.text['text'] = 'Рисуем'
        d = ImageDraw.Draw(img)

        for i, phrase in enumerate(text):
            w, h = d.textsize(phrase, font=font)
            d.text(((W - w) / 2, ((H - h) / 2 + len(text) * padding / 2) - (padding * i)), phrase, font=font,
                   fill=(0, 0, 0))

        logo = Image.open('logo.png', 'r')
        maxsize = (logo.size[0] // 4, logo.size[1] // 4)
        logo.thumbnail(maxsize, Image.ANTIALIAS)

        img.paste(logo, (50, 0), logo)

        img = img.transpose(Image.ROTATE_90)

        img.save('/tmp/test.png')

        # Step 3 - print

        os.popen('lpr -o ppi=300 -o PageSize=w10h10 -o PrintQuality=Graphics /tmp/test.png')

        self.progress_dialog.destroy()


if __name__ == '__main__':
    app = Printer()
    app.geometry("800x480")
    app.mainloop()
