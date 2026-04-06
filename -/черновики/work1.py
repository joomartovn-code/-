flags = {
    'ru': {'red blue', 'white'},
    'kg': {"red yellow", 'red'},
    'ua': {"red blue", 'red', 'blue'},
    'uk': {"yellow", "blue"},
    'kz': {'blue yellow', 'blue'},
    'ge': {'red', 'black', 'yellow'},
    'fr': {'blue', 'white', 'red'},
    'jp': {'white',"red"}
}


while True:
    Gnomik_tupoi = input("Введите exit для выхода, или же введите цвет. Цвет:  ")
    if Gnomik_tupoi == "exit":
        print("Вы вышли из программы...")
        break
    
    found = []
    for domain, colors in flags.items():
        if Gnomik_tupoi in colors:
            found.append(domain)

    if found:
        print(f"Страны с цветом:  {Gnomik_tupoi}:", ", ".join(found))
    else:
        print(f"Нет стран с этим цветом :( {Gnomik_tupoi}")
        