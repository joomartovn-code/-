import flet as ft
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "TODO Профи"
        self.page.window_width = 500
        self.page.window_height = 800
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.tasks = []
        self.load_tasks()

        self.build_ui()
        self.update_tasks()

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.tasks = json.load(f)

    def build_ui(self):
        self.task_input = ft.TextField(label="Что нужно сделать?", expand=True)
        self.search_input = ft.TextField(
            label="Поиск задач...", 
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.filter_tasks
        )
        
        self.priority = ft.Dropdown(
            label="Приоритет",
            width=150,
            options=[
                ft.dropdown.Option("Высокий"),
                ft.dropdown.Option("Средний"),
                ft.dropdown.Option("Низкий"),
            ],
        )

        self.deadline_input = ft.TextField(
            label="Дедлайн (ГГГГ-ММ-ДД)",
            hint_text="2026-12-31",
            width=200
        )

        self.stats_text = ft.Text(size=16, weight="bold", color="blue")
        add_btn = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_task)
        self.task_list = ft.Column(scroll=ft.ScrollMode.ADAPTIVE, expand=True)

        self.page.add(
            ft.Text("Мои Задачи", size=24, weight="bold"),
            self.stats_text,
            self.search_input,
            ft.Row([self.task_input, add_btn]),
            ft.Row([self.priority, self.deadline_input]),
            ft.Divider(),
            self.task_list
        )

    def add_task(self, e):
        if not self.task_input.value or not self.priority.value:
            return

        deadline = self.deadline_input.value if self.deadline_input.value else "Нет"

        task = {
            "title": self.task_input.value,
            "priority": self.priority.value,
            "completed": False,
            "deadline": deadline
        }

        self.tasks.append(task)
        self.save_tasks()
        self.task_input.value = ""
        self.deadline_input.value = ""
        self.update_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.update_tasks()

    def toggle_complete(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.update_tasks()

    def filter_tasks(self, e):
        self.update_tasks(self.search_input.value.lower())

    def check_deadline(self, deadline_str):
        if deadline_str == "Нет": return False
        try:
            deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            if deadline_date < datetime.now().date():
                return True
        except:
            return False
        return False

    def update_tasks(self, search_query=""):
        self.task_list.controls.clear()
        completed_count = 0

        for index, task in enumerate(self.tasks):
            if search_query and search_query not in task["title"].lower():
                continue
            
            if task["completed"]: completed_count += 1
            color = "red" if task["priority"] == "Высокий" else "orange" if task["priority"] == "Средний" else "green"
            is_expired = self.check_deadline(task["deadline"])
            
            self.task_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Checkbox(
                                value=task["completed"], 
                                on_change=lambda e, i=index: self.toggle_complete(i)
                            ),
                            ft.Column([
                                ft.Text(
                                    task["title"], 
                                    size=16, 
                                    weight="bold",
                                    style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH if task["completed"] else None)
                                ),
                                ft.Text(f"Приоритет: {task['priority']} | Срок: {task['deadline']}", size=12, color=color),
                            ], expand=True),
                            ft.IconButton(ft.Icons.DELETE, on_click=lambda e, i=index: self.delete_task(i))
                        ]
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.BLACK12),
                    border_radius=10,
                    bgcolor=ft.Colors.RED_50 if is_expired and not task["completed"] else None
                )
            )

            if is_expired and not task["completed"]:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"ВНИМАНИЕ: Срок задачи '{task['title']}' истек!"))
                self.page.snack_bar.open = True

        total = len(self.tasks)
        self.stats_text.value = f"Выполнено: {completed_count} из {total}"
        self.page.update()

def main(page: ft.Page):
    TodoApp(page)

if __name__ == "__main__":
    ft.app(target=main)