flags = {
    'ru': {'red', 'blue', 'white'},     
    'kg': {"red", "yellow"},             
    'ua': {"red", "blue"},               
    'uk': {"yellow", "blue"},             
    'kz': {"blue", "yellow"},             
    'ge': {"red", "black", "yellow"},     
    'fr': {"blue", "white", "red"},
    'jp': {"white", "red"}              
}

print("=== Программа поиска стран по цвету флага ===")
print("Примеры цветов: red, blue, white, yellow, black")
print("Вы можете ввести один цвет, например: red")
print("Или несколько цветов через пробел, например: red yellow")
print("Для выхода введите: exit")

while True:
    user_input = input("\nВведите цвет(а): ").lower().strip()
    if user_input == "exit":
        print("Вы вышли из программы...")
        break

    input_colors = set(user_input.split())   
    found = []

    for domain, colors in flags.items():
        if input_colors.issubset(colors):  
            found.append(domain)

    if found:
        print("Страны с такими цветами:", ", ".join(found))
    else:
        print("Нет стран с такими цветами.")