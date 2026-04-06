def room_start(life):
    print("Вы обнаруживаете проход позади вас и записку.")
    print("Ваши действия: 1) Пойти к проходу 2) Прочитать записку")
    choice = input("(1/2): ")

    if choice == "1":
        print("Вы нашли минотавра. Вы мертвы.")
        return life - 1

    elif choice == "2":
        print("(Не смотри назад. На втором повороте...) Но вы слышите рёв и умираете.")
        return life - 1

    return life


def corridor_left(life):
    print("Вы идёте налево… тупик.")
    input("(1) Вернуться: ")
    print("Существо с рогами убивает вас.")
    return life - 1


def corridor_right(life):
    print("Вы идёте направо и приходите к развилке.")
    print("1) Повернуть налево 2) Пойти прямо 3) Вернуться")
    choice = input("(1/2/3): ")

    if choice == "1":
        return scene_right_left(life)

    elif choice == "2":
        return scene_right_forward(life)

    elif choice == "3":
        print("Вы встретили минотавра и умерли.")
        return life - 1


# ——— Подсцены ———

def scene_right_left(life):
    print("Новая развилка: 1) Налево 2) Направо")
    choice = input("(1/2): ")

    if choice == "1":
        print("Свет! Ты нашёл выход. (простая концовка)")
        return "win"

    elif choice == "2":
        print("Вы нашли скелет с мечом и броней.")
        print("1) Напасть на минотавра 2) Искать выход")
        choice2 = input("(1/2): ")

        if choice2 == "1":
            print("Вы убили минотавра! (концовка смельчака)")
            return "win"

        else:
            print("Вас обнаружили. Вы умерли.")
            return life - 1


def scene_right_forward(life):
    print("Вы дошли до развилки и видите надпись «иди налево — найдёшь выход».")
    print("1) Повернуть налево 2) Направо")
    choice = input("(1/2): ")

    if choice == "1":
        return scene_lair(life)
    else:
        print("Тупик. Минотавр убивает вас.")
        return life - 1


def scene_lair(life):
    print("Это логово минотавра. Куча трупов вокруг…")
    print("1) Убежать 2) Спрятаться")
    choice = input("(1/2): ")

    print("Минотавр вас заметил. Вы умерли.")
    return life - 1
