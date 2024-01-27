from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import os
import shutil


# Создаём класс основного окна
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Устанавливаем параметры окна
        self.title('File Commander')
        self.geometry('1000x630+50+50')
        self.resizable(0, 0)
        self.put_frames()

    # Создаём фреймы основного окна
    def put_frames(self):
        self.add_left_panel = LeftPanel(self).place(x=0, y=0, width=500, height=570)
        self.add_right_panel = RightPanel(self).place(x=500, y=0, width=500, height=570)
        self.add_button_panel = ButtonPanel(self).place(x=0, y=570, width=1000, height=30)
        self.add_help_panel = HelpPanel(self).place(x=0, y=600, width=1000, height=30)

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
        self.show_path = ttk.Label(self, borderwidth=1, relief='solid', text=CurrentDirectory.left_panel,
                                   anchor="w", background='#CCFFCC', font=("Arial", 13))
        self.show_path.grid(row=0, column=0, sticky='nswe')

        # Выводим имена файлов
        for row_files in range(0, 19):
            self.panel = ttk.Label(self,
                                   text=files_list(CurrentDirectory.left_panel)[row_files],
                                   anchor="w", font=("Arial", 13))
            if Cursor.position == row_files and Cursor.panel == 0:
                self.panel.config(background='#99CCFF')
            self.panel.grid(row=row_files + 1, column=0, sticky='nswe')


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
        self.show_path = ttk.Label(self, borderwidth=1, relief='solid', text=CurrentDirectory.right_panel,
                                   anchor="w", background='#CCFFCC', font=("Arial", 13))
        self.show_path.grid(row=0, column=0, sticky='nswe')

        # Выводим имена файлов
        for row_files in range(0, 19):
            self.panel = ttk.Label(self,
                                   text=files_list(CurrentDirectory.right_panel)[row_files],
                                   anchor="w", font=("Arial", 13))
            if Cursor.position == row_files and Cursor.panel == 1:
                self.panel.config(background='#99CCFF')

            self.panel.grid(row=row_files + 1, column=0, sticky='nswe')


# Создаём класс кнопок управления
class ButtonPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=0, y=570, width=1000, height=30)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        self.rowconfigure((0), weight=1, uniform='a')
        # Запускаем создание виджетов и их размещение
        self.create_widgets()
        self.create_layout()

    # Создание виджетов
    def create_widgets(self):
        self.button_help = ttk.Button(self, text='F1. Помощь')
        self.button_create_file = ttk.Button(self, text='F4. Создать файл')
        self.button_copy = ttk.Button(self, text='F5. Копировать')
        self.button_remove = ttk.Button(self, text='F6. Переместить')
        self.button_create_dir = ttk.Button(self, text='F7. Создать папку')
        self.button_delete = ttk.Button(self, text='F8. Удалить')

    # Размещение виджетов
    def create_layout(self):
        self.button_help.grid(row=0, column=0, sticky='nswe')
        self.button_create_file.grid(row=0, column=1, sticky='nswe')
        self.button_copy.grid(row=0, column=2, sticky='nswe')
        self.button_remove.grid(row=0, column=3, sticky='nswe')
        self.button_create_dir.grid(row=0, column=4, sticky='nswe')
        self.button_delete.grid(row=0, column=5, sticky='nswe')


class HelpPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure((0), weight=1, uniform='a')
        self.button_delete = ttk.Button(self, text='Навигация по панели: Стрелка Вверх, Стрелка Вниз / '
                                                   'Enter для перехода по директориям / '
                                                   'Tab для переключения между панелями')
        self.button_delete.grid(row=0, column=0, sticky='nswe')


class CurrentDirectory:
    left_panel = os.path.abspath(os.curdir)
    right_panel = os.path.abspath(os.curdir)
    new_obj_name = ''


class Cursor:
    panel = 0
    position = 0
    max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
    max_position_1 = len(os.listdir(CurrentDirectory.right_panel))


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

    for i in range(1, 19):
        if i > len(panel_file_list) - 1:
            panel_file_list.append('')
    return panel_file_list


def cursor_move_down(event):
    if Cursor.position < 18:
        if Cursor.panel == 0:
            if Cursor.position < Cursor.max_position_0:
                Cursor.position += 1
        if Cursor.panel == 1:
            if Cursor.position < Cursor.max_position_1:
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
    Cursor.position = 0
    app.refresh()


def cursor_enter(event):
    if Cursor.panel == 0:
        if Cursor.position == 0:
            CurrentDirectory.left_panel = os.path.split(CurrentDirectory.left_panel)[0]
        else:
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:5] == 'Папка':
                CurrentDirectory.left_panel += '\\'
                CurrentDirectory.left_panel += files_list(CurrentDirectory.left_panel)[Cursor.position][7:]
    if Cursor.panel == 1:
        if Cursor.position == 0:
            CurrentDirectory.right_panel = os.path.split(CurrentDirectory.right_panel)[0]
        else:
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:5] == 'Папка':
                CurrentDirectory.right_panel += '\\'
                CurrentDirectory.right_panel += files_list(CurrentDirectory.right_panel)[Cursor.position][7:]
    Cursor.position = 0
    Cursor.max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
    Cursor.max_position_1 = len(os.listdir(CurrentDirectory.right_panel))
    app.refresh()


def create_file(event):
    if Cursor.panel == 0:
        open(f'{CurrentDirectory.left_panel}\\test_file.txt', 'w')
    if Cursor.panel == 1:
        open(f'{CurrentDirectory.right_panel}\\test_file.txt', 'w')
    app.refresh()


def copy_obj(event):
    try:
        if Cursor.panel == 0 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.left_panel)
            filee = files_list(CurrentDirectory.left_panel)[Cursor.position]
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:4] == 'Файл':
                shutil.copy2((direct + '\\' + filee[6:]), CurrentDirectory.right_panel)
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:5] == 'Папка':
                shutil.copytree(direct + '\\' + filee[7:], CurrentDirectory.right_panel + '\\' + filee[7:])
        if Cursor.panel == 1 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.right_panel)
            filee = files_list(CurrentDirectory.right_panel)[Cursor.position]
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:4] == 'Файл':
                shutil.copy2((direct + '\\' + filee[6:]), CurrentDirectory.left_panel)
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:5] == 'Папка':
                shutil.copytree(direct + '\\' + filee[7:], CurrentDirectory.left_panel + '\\' + filee[7:])
    except:
        pass
    Cursor.position = 0
    Cursor.max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
    Cursor.max_position_1 = len(os.listdir(CurrentDirectory.right_panel))
    app.refresh()


def remove_obj(event):
    try:
        if Cursor.panel == 0 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.left_panel)
            filee = files_list(CurrentDirectory.left_panel)[Cursor.position]
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:4] == 'Файл':
                shutil.move((direct + '\\' + filee[6:]), CurrentDirectory.right_panel)
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:5] == 'Папка':
                shutil.move(direct + '\\' + filee[7:], CurrentDirectory.right_panel + '\\' + filee[7:])
        if Cursor.panel == 1 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.right_panel)
            filee = files_list(CurrentDirectory.right_panel)[Cursor.position]
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:4] == 'Файл':
                shutil.move((direct + '\\' + filee[6:]), CurrentDirectory.left_panel)
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:5] == 'Папка':
                shutil.move(direct + '\\' + filee[7:], CurrentDirectory.left_panel + '\\' + filee[7:])
    except:
        pass
    Cursor.position = 0
    Cursor.max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
    Cursor.max_position_1 = len(os.listdir(CurrentDirectory.right_panel))
    app.refresh()


def create_dir(event):
    try:
        if Cursor.panel == 0:
            os.mkdir(CurrentDirectory.left_panel + '\\Test_Dir')
        if Cursor.panel == 1:
            os.mkdir(CurrentDirectory.right_panel + '\\Test_Dir')
        Cursor.position = 0
        Cursor.max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
        Cursor.max_position_1 = len(os.listdir(CurrentDirectory.right_panel))
        app.refresh()
    except:
        pass


def delete_obj(event):
    if Cursor.panel == 0:
        if Cursor.panel == 0 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.left_panel)
            filee = files_list(CurrentDirectory.left_panel)[Cursor.position]
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:4] == 'Файл':
                os.remove(direct + '\\' + filee[6:])
            if files_list(CurrentDirectory.left_panel)[Cursor.position][:5] == 'Папка':
                shutil.rmtree(direct + '\\' + filee[7:])
        if Cursor.panel == 0 and Cursor.position != 0:
            direct = os.path.abspath(CurrentDirectory.right_panel)
            filee = files_list(CurrentDirectory.right_panel)[Cursor.position]
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:4] == 'Файл':
                os.remove(direct + '\\' + filee[6:])
            if files_list(CurrentDirectory.right_panel)[Cursor.position][:5] == 'Папка':
                shutil.rmtree(direct + '\\' + filee[7:])
    Cursor.position = 0
    Cursor.max_position_0 = len(os.listdir(CurrentDirectory.left_panel))
    Cursor.max_position_1 = len(os.listdir(CurrentDirectory.right_panel))
    app.refresh()


def show_info(event):
    showinfo(title="Информация", message="Разработчик: Борис Михайлов")


if __name__ == "__main__":
    app = App()
    app.bind('<Up>', cursor_move_up)
    app.bind('<Down>', cursor_move_down)
    app.bind('<Tab>', cursor_tab)
    app.bind('<Return>', cursor_enter)
    app.bind('<F1>', show_info)
    app.bind('<F4>', create_file)
    app.bind('<F5>', copy_obj)
    app.bind('<F6>', remove_obj)
    app.bind('<F7>', create_dir)
    app.bind('<F8>', delete_obj)
    app.mainloop()
