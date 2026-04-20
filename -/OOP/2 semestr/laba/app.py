import flet as ft
from ui import UI
import smtplib
from email.message import EmailMessage

class ProfileApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.ui = UI()
        
        self.page.overlay.append(self.ui.file_picker) 
        self.build_event()
        self.page.add(ft.Column(self.ui.build(), scroll=ft.ScrollMode.AUTO))

    def build_event(self):
        self.ui.button.on_click = self.create_profile
        self.ui.age.on_change = self.update_age
        self.ui.theme_btn.on_click = self.toggle_theme
        self.ui.upload_btn.on_click = lambda _: self.ui.file_picker.pick_files()
        self.ui.file_picker.on_result = self.on_file_result

    def toggle_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.ui.theme_btn.icon = ft.icons.DARK_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.ui.theme_btn.icon = ft.icons.SUNNY
        self.page.update()

    def on_file_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.ui.photo_path.value = e.files[0].name
            self.page.update()

    def update_age(self, e):
        self.ui.age_text.value = f'Возраст: {int(self.ui.age.value)}'
        self.page.update()

    def send_email(self, content):
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = 'Новая анкета резюме'
        msg['From'] = "YOUR_EMAIL@gmail.com"  
        msg['To'] = "TARGET_EMAIL@gmail.com"  

        try:
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("YOUR_EMAIL@gmail.com", "YOUR_APP_PASSWORD")
                smtp.send_message(msg)
        except Exception as ex:
            print(f"Ошибка почты: {ex}")

    def create_profile(self, e):
        
        errors = False
        if not self.ui.name.value:
            self.ui.name.error_text = "Введите имя!"
            errors = True
        else:
            self.ui.name.error_text = None

        if not self.ui.city.value:
            self.ui.result.value = "Пожалуйста, выберите город"
            self.ui.result.color = ft.colors.RED
            errors = True
        
        if errors:
            self.page.update()
            return

        
        skills = [s.label for s in [self.ui.skill1, self.ui.skill2, self.ui.skill3] if s.value]
        
        profile_data = (
            f"Имя: {self.ui.name.value}\n"
            f"Город: {self.ui.city.value}\n"
            f"Возраст: {int(self.ui.age.value)}\n"
            f"Навыки: {', '.join(skills)}\n"
            f"Уровень: {self.ui.level.value}\n"
            f"Фото: {self.ui.photo_path.value}"
        )

        
        self.ui.result.value = "Анкета успешно создана и отправлена!"
        self.ui.result.color = ft.colors.GREEN
        self.send_email(profile_data) 
        self.page.update()