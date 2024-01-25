# Реализовать прототип консольной программы - проводника, для работы с файлами.
# Создать функции создания, удаления, перемещения, копирования(файла, папки)
# с использованием системы контроля версий git. Зарегистрироваться на Github
# и выгрузить с помощью git программу в созданный репозиторий. Прикрепить ссылку на репозиторий.

import tkinter as ttk
import os


class App(ttk.Tk):
    def __init__(self):
        super().__init__()

        # Устанавливаем параметры окна
        self.title('File Commander')
        self.geometry('1000x600+50+50')
        self.resizable(0, 0)

        # Создаём виджеты кнопок
        Button_panel(self)
        # Создаём виджеты файловых панелей
        File_panel(self, 0)
        File_panel(self, 1)



class Button_panel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=0, y=570, width=1000, height=30)
        # Запускаем создание виджетов и их размещение
        self.create_widgets()
        self.create_layout()

    # Создание виджетов
    def create_widgets(self):
        self.button_create_file = ttk.Button(self, text='Создать файл')
        self.button_create_dir = ttk.Button(self, text='Создать папку')
        self.button_delete = ttk.Button(self, text='Копировать')
        self.button_remove = ttk.Button(self, text='Переместить')
        self.button_copy = ttk.Button(self, text='Удалить')

    # Размещение виджетов
    def create_layout(self):
        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')
        self.rowconfigure((0), weight=1, uniform='a')

        self.button_create_file.grid(row=0, column=0, sticky='nswe')
        self.button_create_dir.grid(row=0, column=1, sticky='nswe')
        self.button_delete.grid(row=0, column=2, sticky='nswe')
        self.button_remove.grid(row=0, column=3, sticky='nswe')
        self.button_copy.grid(row=0, column=4, sticky='nswe')

class File_panel(ttk.Frame):
    def __init__(self, parent, panel_number):
        super().__init__(parent)
        if panel_number == 0:
            panel_x = 0
            panel_color = '#C0C0C0'
        else:
            panel_x = 500
            panel_color = '#E0E0E0'
        # Указываем размещение нашего фрейма на главном окне
        self.place(x=panel_x, y=0, width=500, height=570)
        self.columnconfigure((0), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18),
                          weight=1, uniform='a')

        for row_files in range(19):
            self.panel = ttk.Label(self, background=panel_color, text=row_files, anchor="w")
            self.panel.grid(row=row_files, column=0, sticky='nswe')




if __name__ == "__main__":
    app = App()
    app.mainloop()
