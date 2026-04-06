import tkinter as tk
from tkinter import messagebox, ttk

class EmployeeApp:
    def __init__(self, root):
        self.window = root
        self.window.title("Каталог сотрудников")
        self.window.geometry("500x700")

        self.data_storage = []
        self.initialize_interface()

    def initialize_interface(self):
        self.top_panel = tk.Frame(self.window, padx=15, pady=15)
        self.top_panel.pack(side="top", fill="x")

        self.inputs = {}
        fields = [("Имя", "first_name"), ("Фамилия", "last_name"), ("Возраст", "age"), ("Зарплата", "salary")]

        for i, (label_text, key) in enumerate(fields):
            tk.Label(self.top_panel, text=f"{label_text}:").grid(row=i, column=0, sticky="w", pady=2)
            entry = tk.Entry(self.top_panel)
            entry.grid(row=i, column=1, sticky="we", pady=2)
            self.inputs[key] = entry

        tk.Label(self.top_panel, text="Должность:").grid(row=4, column=0, sticky="w")
        self.role_selector = ttk.Combobox(self.top_panel, values=["Разработчик", "Дизайнер", "Менеджер", "Тестировщик"], state="readonly")
        self.role_selector.current(0)
        self.role_selector.grid(row=4, column=1, sticky="we", pady=2)

        self.add_trigger = tk.Button(self.top_panel, text="Добавить сотрудника", command=self.handle_submission, bg="#2E7D32", fg="white")
        self.add_trigger.grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

        tk.Label(self.window, text="Список сотрудников (по возрастанию зарплаты)", font=("Segoe UI", 9, "bold")).pack()

        self.view_container = tk.Canvas(self.window)
        self.v_scroll = ttk.Scrollbar(self.window, orient="vertical", command=self.view_container.yview)
        self.list_frame = tk.Frame(self.view_container)

        self.list_frame.bind("<Configure>", lambda _: self.view_container.configure(scrollregion=self.view_container.bbox("all")))
        self.view_container.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.view_container.configure(yscrollcommand=self.v_scroll.set)

        self.view_container.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")

    def handle_submission(self):
        raw_data = {key: entry.get().strip() for key, entry in self.inputs.items()}
        raw_data['role'] = self.role_selector.get()

        if not all(raw_data.values()):
            messagebox.showwarning("Внимание", "Необходимо заполнить все поля")
            return

        try:
            formatted_entry = {
                "name": raw_data['first_name'],
                "surname": raw_data['last_name'],
                "age": int(raw_data['age']),
                "role": raw_data['role'],
                "salary": float(raw_data['salary'])
            }
            self.data_storage.append(formatted_entry)
            self.data_storage.sort(key=lambda item: item['salary'])
            
            self.reset_inputs()
            self.update_display()
        except ValueError:
            messagebox.showerror("Ошибка типа", "Проверьте корректность числовых полей")

    def reset_inputs(self):
        for entry in self.inputs.values():
            entry.delete(0, tk.END)

    def remove_entry(self, target):
        self.data_storage.remove(target)
        self.update_display()

    def update_display(self):
        for child in self.list_frame.winfo_children():
            child.destroy()

        for person in self.data_storage:
            is_high_paid = person['salary'] > 100000
            theme_color = "#FFF9C4" if is_high_paid else "#FAFAFA"
            
            row_item = tk.Frame(self.list_frame, bg=theme_color, highlightbackground="#BDBDBD", highlightthickness=1)
            row_item.pack(fill="x", padx=10, pady=3)

            desc = f"{person['name']} {person['surname']} | {person['age']} лет\n{person['role']}: {person['salary']:.2f} руб."
            tk.Label(row_item, text=desc, bg=theme_color, justify="left", font=("Arial", 9)).pack(side="left", padx=5, pady=5)

            tk.Button(row_item, text="✖", command=lambda p=person: self.remove_entry(p), bg="#D32F2F", fg="white", width=3).pack(side="right", padx=5)

if __name__ == "__main__":
    app_root = tk.Tk()
    EmployeeApp(app_root)
    app_root.mainloop()