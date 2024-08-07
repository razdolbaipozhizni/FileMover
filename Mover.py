import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


class FileMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Mover")

        self.source_folder = ""
        self.destination_folder = ""
        self.selected_files = []

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Source Folder:").pack(pady=5)
        self.source_entry = tk.Entry(self.root, width=50)
        self.source_entry.pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_source).pack(pady=5)

        tk.Label(self.root, text="Destination Folder:").pack(pady=5)
        self.destination_entry = tk.Entry(self.root, width=50)
        self.destination_entry.pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_destination).pack(pady=5)

        tk.Button(self.root, text="Select Files", command=self.select_files).pack(pady=10)
        tk.Button(self.root, text="Move Files", command=self.move_files).pack(pady=10)

        self.log_text = tk.Text(self.root, height=15, width=70)
        self.log_text.pack(pady=10)

    def browse_source(self):
        self.source_folder = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, self.source_folder)

    def browse_destination(self):
        self.destination_folder = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, self.destination_folder)

    def select_files(self):
        files = filedialog.askopenfilenames(initialdir=self.source_folder)
        self.selected_files.extend(files)

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Selected Files:\n")
        for file in self.selected_files:
            self.log_text.insert(tk.END, file + "\n")

    def move_files(self):
        if not self.source_folder or not self.destination_folder:
            messagebox.showerror("Error", "Please specify both source and destination folders.")
            return

        if not self.selected_files:
            messagebox.showerror("Error", "No files selected to move.")
            return

        moved_files = []
        failed_files = []

        for file in self.selected_files:
            try:
                shutil.move(file, self.destination_folder)
                moved_files.append(file)
            except Exception as e:
                failed_files.append((file, str(e)))

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "Move Operation Report:\n\n")

        if moved_files:
            self.log_text.insert(tk.END, "Successfully Moved Files:\n")
            for file in moved_files:
                self.log_text.insert(tk.END, f"{file} -> {self.destination_folder}\n")

        if failed_files:
            self.log_text.insert(tk.END, "\nFailed to Move Files:\n")
            for file, error in failed_files:
                self.log_text.insert(tk.END, f"{file}: {error}\n")

        messagebox.showinfo("Report", f"Total files moved: {len(moved_files)}\nFailed: {len(failed_files)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileMoverApp(root)
    root.mainloop()
