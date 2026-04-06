import flet as ft
from database.db_manager import DBManager
from ui.components import EmployeeTable

def main(page: ft.Page):
    page.title = "Система учета кадров 2.0"
    page.window_width = 800
    db = DBManager()

    # Поля ввода
    fio_input = ft.TextField(label="ФИО", expand=True)
    job_input = ft.TextField(label="Должность", expand=True)
    salary_input = ft.TextField(label="Зарплата", width=120)
    
    search_box = ft.TextField(label="Поиск...", expand=True)
    sort_dropdown = ft.Dropdown(
        width=150,
        value="fio",
        options=[
            ft.dropdown.Option("fio", "По имени"),
            ft.dropdown.Option("money", "По зарплате")
        ]
    )

    def on_delete(idx):
        db.delete_user(idx)
        load_data()

    table = EmployeeTable(delete_callback=on_delete)

    def load_data(e=None):
        data = db.get_users(search_box.value, sort_dropdown.value)
        table.update_rows(data)
        page.update()

    def add_clicked(e):
        if fio_input.value and job_input.value:
            try:
                db.add_user(fio_input.value, job_input.value, float(salary_input.value))
                fio_input.value = job_input.value = salary_input.value = ""
                load_data()
            except: pass

    search_box.on_change = load_data
    sort_dropdown.on_change = load_data

    page.add(
        ft.Row([fio_input, job_input, salary_input]),
        ft.ElevatedButton("Добавить сотрудника", on_click=add_clicked),
        ft.Divider(),
        ft.Row([search_box, sort_dropdown]),
        ft.Column([table], scroll=ft.ScrollMode.ALWAYS, expand=True)
    )
    load_data()

if __name__ == "__main__":
    ft.app(target=main)