import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover")

        self.files = []
        self.target_directory = ""

        self.create_widgets()

    def create_widgets(self):
        # Настройка столбцов grid для Canvas и Scrollbar
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Создаем область прокрутки
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=2, column=0, columnspan=8, sticky="nsew")
        self.scrollbar.grid(row=2, column=8, sticky="ns")

        # Заголовки столбцов
        tk.Label(self.scrollable_frame, text="Файл").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.scrollable_frame, text="Текущее расположение").grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.scrollable_frame, text="Перенести в").grid(row=0, column=3, padx=10, pady=5)
        tk.Label(self.scrollable_frame, text="Статус").grid(row=0, column=6, padx=10, pady=5)

        # Кнопка для выбора целевой директории
        self.set_target_dir_button = tk.Button(self.root, text="Выбрать целевую папку", command=self.set_target_directory)
        self.set_target_dir_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Кнопка для добавления файлов
        self.add_file_button = tk.Button(self.root, text="Добавить файлы", command=self.add_files)
        self.add_file_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Кнопка для переноса всех файлов
        self.move_all_button = tk.Button(self.root, text="Перенести все файлы", command=self.move_all_files)
        self.move_all_button.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Кнопка для удаления всех файлов
        self.delete_all_button = tk.Button(self.root, text="Удалить все файлы", command=self.delete_all_files)
        self.delete_all_button.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        # Список для хранения виджетов
        self.file_widgets = []

    def set_target_directory(self):
        self.target_directory = filedialog.askdirectory()
        if self.target_directory:
            # Устанавливаем целевую директорию для каждого файла
            for file_widgets in self.file_widgets:
                file_widgets['target_path_label'].config(text=self.target_directory)

    def add_files(self):
        filepaths = filedialog.askopenfilenames()
        for filepath in filepaths:
            if filepath:
                filename = os.path.basename(filepath)
                file_widgets = {}

                row = len(self.file_widgets) + 1

                file_widgets['filename_label'] = tk.Label(self.scrollable_frame, text=filename)
                file_widgets['filename_label'].grid(row=row, column=0, padx=10, pady=5)

                file_widgets['current_path_label'] = tk.Label(self.scrollable_frame, text=filepath)
                file_widgets['current_path_label'].grid(row=row, column=1, padx=10, pady=5)

                file_widgets['target_path_label'] = tk.Label(self.scrollable_frame, text=self.target_directory)
                file_widgets['target_path_label'].grid(row=row, column=3, padx=10, pady=5)

                file_widgets['select_button'] = tk.Button(self.scrollable_frame, text="Изменить папку", command=lambda fw=file_widgets: self.select_directory(fw))
                file_widgets['select_button'].grid(row=row, column=4, padx=10, pady=5)

                file_widgets['move_button'] = tk.Button(self.scrollable_frame, text="Перенести", command=lambda fw=file_widgets, fp=filepath: self.move_file(fw, fp))
                file_widgets['move_button'].grid(row=row, column=5, padx=10, pady=5)

                file_widgets['status_label'] = tk.Label(self.scrollable_frame, text="Не выполнено")
                file_widgets['status_label'].grid(row=row, column=6, padx=10, pady=5)

                file_widgets['delete_button'] = tk.Button(self.scrollable_frame, text="Удалить", command=lambda fw=file_widgets: self.delete_file(fw))
                file_widgets['delete_button'].grid(row=row, column=7, padx=10, pady=5)

                self.file_widgets.append(file_widgets)

    def select_directory(self, file_widgets):
        directory = filedialog.askdirectory()
        if directory:
            file_widgets['target_path_label'].config(text=directory)

    def move_file(self, file_widgets, filepath):
        target_dir = file_widgets['target_path_label'].cget("text")
        if os.path.isdir(target_dir):
            try:
                shutil.move(filepath, target_dir)
                # Обновляем текущее расположение
                new_path = os.path.join(target_dir, os.path.basename(filepath))
                file_widgets['current_path_label'].config(text=new_path)
                # Сбрасываем значение "Перенести в" и статус
                file_widgets['target_path_label'].config(text="")
                file_widgets['status_label'].config(text="Успешно", fg="green")
            except Exception as e:
                file_widgets['status_label'].config(text=f"Ошибка: {e}", fg="red")
        else:
            messagebox.showerror("Ошибка", "Указанная директория не существует")
            file_widgets['status_label'].config(text="Не выполнено", fg="red")

    def move_all_files(self):
        for file_widgets in self.file_widgets:
            filepath = file_widgets['current_path_label'].cget("text")
            self.move_file(file_widgets, filepath)

    def delete_file(self, file_widgets):
        for widget in file_widgets.values():
            widget.grid_forget()
            widget.destroy()
        self.file_widgets.remove(file_widgets)
        self.refresh_grid()

    def delete_all_files(self):
        for file_widgets in self.file_widgets[:]:
            self.delete_file(file_widgets)

    def refresh_grid(self):
        for i, file_widgets in enumerate(self.file_widgets):
            row = i + 1
            file_widgets['filename_label'].grid(row=row, column=0, padx=10, pady=5)
            file_widgets['current_path_label'].grid(row=row, column=1, padx=10, pady=5)
            file_widgets['target_path_label'].grid(row=row, column=3, padx=10, pady=5)
            file_widgets['select_button'].grid(row=row, column=4, padx=10, pady=5)
            file_widgets['move_button'].grid(row=row, column=5, padx=10, pady=5)
            file_widgets['status_label'].grid(row=row, column=6, padx=10, pady=5)
            file_widgets['delete_button'].grid(row=row, column=7, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()
