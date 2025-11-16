from scenes import room_start, corridor_left, corridor_right

def start_game():
    life = 5

    while life > 0:
        print(f"\nУ тебя осталось жизней: {life}")
        print("Вы просыпаетесь в тёмном помещении. И едва замечаете два тёмных прохода перед вами.")
        print("Ваши действия: 1) Осмотреть комнату 2) Пойти налево 3) Пойти направо")

        choice = input("Что ты выберешь? (1/2/3): ")

        if choice == "1":
            life = room_start(life)

        elif choice == "2":
            life = corridor_left(life)

        elif choice == "3":
            result = corridor_right(life)
            if result == "win":
                break
            else:
                life = result

        if life <= 0:
            print("\nУ тебя больше нет жизней. Конец игры! (Концовка смертника)")
            break
