from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class CreditCardPayment(Payment):
    def pay(self, amount):
        print(f"Оплата {amount} через кредитную карту прошла успешно.")

    def refund(self, amount):
        print(f"Возврат {amount} на кредитную карту выполнен.")

class CryptoPayment(Payment):
    def pay(self, amount):
        print(f"Перевод {amount} в криптовалюте отправлен.")

    def refund(self, amount):
        print(f"Возврат {amount} криптовалютой выполнен.")


payments = [CreditCardPayment(), CryptoPayment()]
for p in payments:
    p.pay(100)
    p.refund(100)



class Course(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_materials(self):
        pass

    @abstractmethod
    def end(self):
        pass

class PythonCourse(Course):
    def start(self):
        print("Python курс начат!")

    def get_materials(self):
        return ["Основы Python", "ООП"]

    def end(self):
        print("Python курс завершён!")

class MathCourse(Course):
    def start(self):
        print("Курс математики начат!")

    def get_materials(self):
        return ["Алгебра", "Геометрия"]

    def end(self):
        print("Курс математики завершён!")


class Delivery(ABC):
    @abstractmethod
    def calculate_cost(self, distance):
        pass

    @abstractmethod
    def deliver(self):
        pass

class AirDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 5

    def deliver(self):
        print("Доставка самолётом отправлена!")

class GroundDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 2

    def deliver(self):
        print("Доставка по земле отправлена!")

class SeaDelivery(Delivery):
    def calculate_cost(self, distance):
        return distance * 3

    def deliver(self):
        print("Доставка морем отправлена!")



class BankAccount:
    def __init__(self, owner, balance, pin):
        self.__owner = owner
        self.__balance = balance
        self.__pin = pin

    def deposit(self, amount, pin):
        if pin != self.__pin:
            print("Неверный PIN.")
            return
        if amount <= 0:
            print("Сумма должна быть положительной.")
            return
        self.__balance += amount
        print(f"Пополнено: {amount}. Баланс: {self.__balance}")

    def withdraw(self, amount, pin):
        if pin != self.__pin:
            print("Неверный PIN.")
            return
        if amount > self.__balance:
            print("Недостаточно средств.")
            return
        self.__balance -= amount
        print(f"Снято: {amount}. Баланс: {self.__balance}")

    def change_pin(self, old_pin, new_pin):
        if old_pin != self.__pin:
            print("Неверный текущий PIN.")
            return
        self.__pin = new_pin
        print("PIN успешно изменён.")



class UserProfile:
    def __init__(self, email, password):
        self.__email = email
        self.__password = password
        self._status = "Free"

    def login(self, email, password):
        if email == self.__email and password == self.__password:
            print("Вход выполнен.")
        else:
            print("Неверные данные. Доступ запрещён.")

    def upgrade_to_premium(self):
        self._status = "Premium"
        print("Статус обновлён до Premium.")

    def get_info(self):
        return {"email": self.__email, "status": self._status}



class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.__discount = 0

    def get_price(self):
        return self.price * (1 - self.__discount / 100)

    def set_discount(self, percent, is_admin=False):
        if is_admin:
            self.__discount = percent
        else:
            print("Недостаточно прав для изменения скидки.")



class TextFile:
    def open(self):
        print("Открыт текстовый файл.")

class ImageFile:
    def open(self):
        print("Открыто изображение.")

class AudioFile:
    def open(self):
        print("Открыт аудиофайл.")

def open_all(files):
    for f in files:
        f.open()



class Car:
    speed = 80
    def move(self, distance):
        return distance / self.speed

class Truck:
    speed = 60
    def move(self, distance):
        return distance / self.speed

class Bicycle:
    speed = 20
    def move(self, distance):
        return distance / self.speed

def simulate_transport(transport_list, distance):
    for t in transport_list:
        print(f"{t.__class__.__name__}: время в пути = {t.move(distance)} часов")



class Student:
    def access_portal(self):
        print("Доступ: расписание учебы.")

class Teacher:
    def access_portal(self):
        print("Доступ: выставление оценок.")

class Administrator:
    def access_portal(self):
        print("Доступ: управление пользователями.")

portal_users = [Student(), Teacher(), Administrator()]
for u in portal_users:
    u.access_portal()
