import flet as ft

class UI:
    def __init__(self):
        self.title = ft.Text('Создание пользователей', size=25, weight="bold")
        self.name = ft.TextField(label='Имя', width=300, error_text="") 
        self.city = ft.Dropdown(
            label='Город',
            width=300,
            options=[ft.dropdown.Option('Бишкек'), ft.dropdown.Option('Ош'), ft.dropdown.Option('Токмок')],
        )
        
        
        self.age_text = ft.Text('Возраст: 18')
        self.age = ft.Slider(min=10, max=60, divisions=50, value=18)

        
        self.skill1 = ft.Checkbox(label='Python')
        self.skill2 = ft.Checkbox(label='Django')
        self.skill3 = ft.Checkbox(label='Flet')
        self.level = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value='Jun', label='Junior'),
                ft.Radio(value='Mid', label='Middle'),
                ft.Radio(value='Sen', label='Senior'),
            ])
        )
        
        self.active = ft.Switch(label='Готов к работе')

        
        self.file_picker = ft.FilePicker()
        self.upload_btn = ft.ElevatedButton("Выбрать фото", icon=ft.icons.UPLOAD_FILE)
        self.photo_path = ft.Text("Файл не выбран", italic=True)
        
        self.theme_btn = ft.IconButton(ft.icons.SUNNY, tooltip="Сменить тему")
        self.button = ft.ElevatedButton('Отправить резюме', bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)
        self.result = ft.Text()

    def build(self):
        return [
            self.theme_btn,
            self.title,
            self.name,
            self.city,
            self.age_text,
            self.age,
            ft.Text('Навыки:', weight="bold"),
            self.skill1, self.skill2, self.skill3,
            ft.Text('Уровень:', weight="bold"),
            self.level,
            self.active,
            ft.Row([self.upload_btn, self.photo_path]),
            self.button,
            self.result,
            self.file_picker
        ]