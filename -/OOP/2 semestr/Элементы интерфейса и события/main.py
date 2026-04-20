import flet as ft
from app import ProfileApp

def main(page: ft.Page):
    page.window_width = 500
    page.window_height = 800 
    ProfileApp(page)

ft.app(target=main)