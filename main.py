# Реализовать прототип консольной программы - проводника, для работы с файлами.
# Создать функции создания, удаления, перемещения, копирования(файла, папки)
# с использованием системы контроля версий git. Зарегистрироваться на Github
# и выгрузить с помощью git программу в созданный репозиторий. Прикрепить ссылку на репозиторий.

from tkinter import ttk
import tkinter as tk
import os


# Создаём класс основного окна
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Устанавливаем параметры окна
        self.title('File Commander')
        self.geometry('1000x600+1450+150')
        self.resizable(0, 0)
        self.put_frames()

    # Создаём фреймы основного окна
    def put_frames(self):
        self.add_left_panel = LeftPanel(self).place(x=0, y=0, width=500, height=570)
        self.add_right_panel = RightPanel(self).place(x=500, y=0, width=500, height=570)
        self.add_button_panel = ButtonPanel(self).place(x=0, y=570, width=1000, height=30)

    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()


class LeftPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure([i for i in range(20)], weight=1, uniform='a')
        self['background'] = '#C0C0C0'
        self['bd'] = 1
        self['relief'] = 'solid'
        self.put_widgets()

    def put_widgets(self):
        # Текущая директория
        self.show_path = ttk.Label(self, background='#C0C0C0', text=CurrentDirectory.left_panel,
                                   anchor="w", font=("Arial", 13))
        self.show_path.grid(row=0, column=0, sticky='nswe')

        # Выводим имена файлов
        for row_files in range(0, 19):
            self.panel = ttk.Label(self, background='#C0C0C0',
                                   text=files_list(CurrentDirectory.left_panel)[row_files],
                                   anchor="w", font=("Arial", 13))
            if Cursor.position == row_files and Cursor.panel == 0:
                self.panel.config(background='#99CCFF')
            self.panel.grid(row=row_files+1, column=0, sticky='nswe')


class RightPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure([i for i in range(20)], weight=1, uniform='a')
        self['background'] = '#C0C0C0'
        self['bd'] = 1
        self['relief'] = 'solid'
        self.put_widgets()

    def put_widgets(self):
        # Текущая директория
        self.show_path = ttk.Label(self, background='#C0C0C0', text=CurrentDirectory.right_panel,
                                   anchor="w", font=("Arial", 13))
        self.show_path.grid(row=0, column=0, sticky='nswe')

        # Выводим имена файлов
        for row_files in range(0, 19):
            self.panel = ttk.Label(self, background='#C0C0C0',
                                   text=files_list(CurrentDirectory.left_panel)[row_files],
                                   anchor="w", font=("Arial", 13))
            if Cursor.position == row_files and Cursor.panel == 1:
                self.panel.config(background='#99CCFF')
            self.panel.grid(row=row_files+1, column=0, sticky='nswe')

# Создаём класс кнопок управления
class ButtonPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=0, y=570, width=1000, height=30)
        # Запускаем создание виджетов и их размещение
        self.create_widgets()
        self.create_layout()

    # Создание виджетов
    def create_widgets(self):
        self.button_create_file = ttk.Button(self, text='F4. Создать файл')
        self.button_copy = ttk.Button(self, text='F5. Копировать')
        self.button_remove = ttk.Button(self, text='F6. Переместить')
        self.button_create_dir = ttk.Button(self, text='F7. Создать папку')
        self.button_delete = ttk.Button(self, text='F8. Удалить')

    # Размещение виджетов
    def create_layout(self):
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.rowconfigure((0), weight=1, uniform='a')

        self.button_create_file.grid(row=0, column=0, sticky='nswe')
        self.button_copy.grid(row=0, column=1, sticky='nswe')
        self.button_remove.grid(row=0, column=2, sticky='nswe')
        self.button_create_dir.grid(row=0, column=3, sticky='nswe')
        self.button_delete.grid(row=0, column=4, sticky='nswe')


class CurrentDirectory:
    left_panel = os.path.abspath(os.curdir)
    right_panel = os.path.abspath(os.curdir)


class Cursor:
    panel = 0
    position = 1
    max_position = 0

def files_list(cur_dir):
    # Создаём list из списка файлов текущей директории.
    panel_file_list = list(('...',))
    with os.scandir(cur_dir) as file_list:
        for file in file_list:
            if file.is_dir():
                panel_file_list.append('Папка: ' + file.name)
            else:
                panel_file_list.append('Файл: ' + file.name)
    panel_file_list.sort()

    Cursor.max_position = (len(panel_file_list)) - 1

    for i in range(1, 19):
        if i > len(panel_file_list) - 1:
            panel_file_list.append('')
    return panel_file_list

def cursor_move_down(event):
    if Cursor.position < Cursor.max_position:
        Cursor.position += 1
    app.refresh()


def cursor_move_up(event):
    if Cursor.position > 0:
        Cursor.position -= 1
    app.refresh()

def cursor_tab(event):
    if Cursor.panel == 0:
        Cursor.panel = 1
    else:
        Cursor.panel = 0
    app.refresh()


if __name__ == "__main__":
    app = App()
    app.bind('<Up>', cursor_move_up)
    app.bind('<Down>', cursor_move_down)
    app.bind('<Tab>', cursor_tab)
    app.mainloop()
