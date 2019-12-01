import tkinter
from tkinter import font, Entry

master = tkinter.Tk()
master.geometry("800x480")
font = font.Font(family="dejavu sans", size=20)
master.option_add("*Font", font)

buttons = [
    'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'СТЕРЕТЬ',
    'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'SHIFT',
    'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'ПРОБЕЛ',
]

bg_color = '#3c4987'
fg_color = '#ffffff'
active_color = fg_color
fg_active_color = bg_color

button_size = 3
big_button_size = 6
padx = 1
pady = 1  # on css words = margin
bd = 1  # ???


def select(value):
    if value == "BACK":
        field.delete(len(field.get()) - 1, tkinter.END)

    elif value == "SPACE":
        field.insert(tkinter.END, ' ')
    elif value == " Tab ":
        field.insert(tkinter.END, '    ')
    else:
        field.insert(tkinter.END, value)


def keyboard_draw():
    cur_row = 2
    varColumn = 0

    for button in buttons:
        command = lambda x=button: select(x)

        button = tkinter.Button(master, text=button, width=button_size, bg=bg_color, fg=fg_color,
                                activebackground=active_color, activeforeground=fg_active_color, relief='raised',
                                padx=padx,
                                pady=pady, bd=bd, command=command).grid(row=cur_row, column=varColumn)

        varColumn += 1

        if varColumn > 12 and cur_row == 2:
            varColumn = 0
            cur_row += 1
        if varColumn > 11 and cur_row == 3:
            varColumn = 0
            cur_row += 1


if __name__ == '__main__':
    master.resizable(0, 0)

    global field

    field = Entry(master, width=50)
    field.insert(0, 'username')

    keyboard_draw()
    master.mainloop()
