import flet as ft

class EmployeeTable(ft.DataTable):
    def __init__(self, delete_callback):
        super().__init__(
            columns=[
                ft.DataColumn(ft.Text("ФИО")),
                ft.DataColumn(ft.Text("Должность")),
                ft.DataColumn(ft.Text("Оклад")),
                ft.DataColumn(ft.Text("")),
            ],
            rows=[]
        )
        self.delete_callback = delete_callback

    def update_rows(self, data):
        self.rows.clear()
        for item in data:
            self.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item[1])),
                        ft.DataCell(ft.Text(item[2])),
                        ft.DataCell(ft.Text(f"{item[3]} руб.")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color="red",
                                on_click=lambda _, idx=item[0]: self.delete_callback(idx)
                            )
                        ),
                    ]
                )
            )