# банк
class BankAccount:
    def __init__(self, number, balance, pin):
        self.__number = number
        self.__balance = balance
        self.__pin = pin

    def add_money(self, amount, entered_pin):
        if entered_pin == self.__pin:
            self.__balance += amount
        else:
            print("Неверный PIN")

    def take_money(self, amount, entered_pin):
        if entered_pin == self.__pin:
            if amount <= self.__balance:
                self.__balance -= amount
            else:
                print("Недостаточно средств")
        else:
            print("Неверный PIN")

    def check_balance(self, entered_pin):
        if entered_pin == self.__pin:
            return self.__balance
        else:
            return "Ошибка доступа"


account = BankAccount("1234567890", 3000, 1234)
user_pin = input("Введите PIN-код: ")

if user_pin == "1234":
    print(f"Ваш баланс: {account.check_balance(1234)} сом")
else:
    print("Неверный PIN!")


# товары и скидки

class Item:
    def __init__(self, title, price):
        self.title = title
        self.__price = price

    def apply_discount(self, percent):
        if percent < 0:
            print("Ошибка: скидка не может быть отрицательной!")
        else:
            updated_price = self.__price * (1 - percent / 100)
            self.__price = max(0, updated_price)

    def get_price(self):
        return round(self.__price, 2)


potato = Item("Картофель", 25)
potato.apply_discount(10)
print("Цена после скидки:", potato.get_price())


#курсы и студенты

class StudyCourse:
    def __init__(self, course_name, students, capacity):
        self.__course_name = course_name
        self.__students = students
        self.__capacity = capacity

    def enroll(self, student):
        if len(self.__students) < self.__capacity:
            self.__students.append(student)
            print(f"{student} успешно записан(а) на курс.")
        else:
            print("Мест больше нет!")

    def kick(self, student):
        if student in self.__students:
            self.__students.remove(student)
            print(f"{student} удалён из курса.")
        else:
            print("Такого студента нет в списке.")

    def list_students(self):
        return list(self.__students)


course = StudyCourse("OOP", [], 2)
course.enroll("Сезим")
course.enroll("Абдурахим")
course.enroll("Имран")
print(course.list_students())
course.kick("Абдурахим")
print(course.list_students())


#умные часы

class SmartWatch:
    def __init__(self, charge):
        self.__charge = charge

    def use(self, time_minutes):
        used = time_minutes / 10
        self.__charge = max(0, self.__charge - used)
        print(f"Остаток заряда: {self.__charge:.1f}%")

    def recharge(self, percent):
        self.__charge = min(100, self.__charge + percent)
        print(f"Заряд увеличен. Текущий уровень: {self.__charge:.1f}%")

    def status(self):
        return self.__charge


watch = SmartWatch(56)
watch.use(20)
print("Батарея:", watch.status())
watch.recharge(15)
print("Батарея:", watch.status())


#Транспорт

class Vehicle:
    def __init__(self, speed, capacity):
        self.speed = speed
        self.capacity = capacity

    def get_time(self, distance):
        return distance / self.speed


class Bus(Vehicle):
    pass


class Train(Vehicle):
    pass


class Plane(Vehicle):
    def get_time(self, distance):
        base_time = super().get_time(distance)
        return base_time * 0.8  # самолёт быстрее


bus = Bus(80, 45)
train = Train(120, 120)
plane = Plane(600, 200)
distance = 1800

print(bus.get_time(distance))
print(train.get_time(distance))
print(plane.get_time(distance))


#заказы

class Order:
    def __init__(self, meal, price):
        self.meal = meal
        self.price = price

    def total(self):
        return self.price


class DineIn(Order):
    def total(self):
        tip = self.price * 0.1
        return self.price + tip


class TakeAway(Order):
    def total(self):
        return self.price * 0.95


class Delivery(Order):
    def total(self):
        return self.price * 1.15


order1 = DineIn("Лагман", 250)
order2 = TakeAway("Лагман", 250)
order3 = Delivery("Лагман", 250)

print(order1.total())
print(order2.total())
print(order3.total())


#Персонажи

class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def attack(self):
        pass

    def __str__(self):
        return f"{self.name} HP: {self.hp}"


class Warrior(Character):
    def attack(self):
        print(f"{self.name} наносит удар мечом!")


class Mage(Character):
    def attack(self):
        print(f"{self.name} применяет заклинание!")


class Archer(Character):
    def attack(self):
        print(f"{self.name} стреляет из лука!")


yone = Warrior("Йоне", 2400, 90)
aurora = Mage("Аврора", 2400, 100)
aphelios = Archer("Афелий", 2300, 90)

for hero in (yone, aurora, aphelios):
    hero.attack()
    print(hero)


#Медиафайлы

class MediaFile:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    def play(self):
        pass


class Audio(MediaFile):
    def play(self):
        print(f"Играет аудио: {self.title} ({self.duration} мин)")


class Video(MediaFile):
    def play(self):
        print(f"Проигрывается видео: {self.title} ({self.duration} мин)")


class Podcast(MediaFile):
    def play(self):
        print(f"Слушаем подкаст: {self.title} ({self.duration} мин)")


song = Audio("Песня Егора Крида", 3)
clip = Video("Клип Егора Крида", 5)
talk = Podcast("Интервью Егора Крида", 40)

for media in (song, clip, talk):
    media.play()
