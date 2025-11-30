# class name():
#     name = input('какое ваше имя? ')
#     def gg(name):
#         print("Привет,", name)
#     gg(name)



# for i in range(1, 6):
#     print(i)


# vozrast = input("Введите ваш возраст: ")

# vozrast = int(vozrast)
# NextYear = vozrast + 1

# print("Через год вам будет", NextYear)


# ktoto = input("Введите ваше имя: ")

# print("Здравстуйте,", ktoto + "!")




# class BankAccount:
#     def __init__(self):
#         self.balance = 0


#     def deposit(self, amount):
#         self.balance += amount
#         print(f"Вы внесли {amount}. Текущий баланс: {self.balance}")


#     def withdraw(self, amount):
#         if amount <= self.balance:
#             self.balance -= amount
#             print(f"Вы сняли {amount}. Текущий баланс: {self.balance}")
#         else:
#             print("Недостаточно средств!")

    
#     def show_balance(self):
#         print(f"Текущий баланс: {self.balance}")


# BankAcc = BankAccount()
# BankAcc.deposit(100)
# BankAcc.withdraw(50)
# BankAcc.show_balance()
# BankAcc.withdraw(100)




# students = {}

# students["Нурсултан"] = 148
# students["Иман"] = 186
# students["Абдурахим"] = 120
# students["Сезим"] = 197
# students["Имран"] = 155

# testik = sum(students.values()) / len(students)
# print("Средняя оценка:", testik)

# print("Студенты с оценкой выше средней:")
# for name, grade in students.items():
#     if grade > testik:
#         print(name, "-", grade)




# data = [1, 2, 3, 2, 4, 1, 5, 3]

# spisok = []
# for item in data:
#     if item not in spisok:
#         spisok.append(item)

# print("Список:", spisok)

# students = {}

# students["Нурсултан"] = 148
# students["Иман"] = 186
# students["Абдурахим"] = 120
# students["Сезим"] = 197
# students["Имран"] = 155

# total = 0
# for grade in students.values():
#     total += grade
# ОценкООО = total / len(students)
# print("Средняя оценка:", ОценкООО)

# print("Студенты с оценкой выше средней:")
# for name, grade in students.items():
#     if grade > ОценкООО:
#         print(name, "-", grade)







# stroka = input("Введите строку: ")
# spisok = "аеёиоуюяыэ"

# count = 0
# for letter in stroka.lower():
#     if letter in spisok:
    
#         count += 1
#     print("Количество гласных букв:", count)


# for i in range(1, 11):
#     print(f"5 x {i} = {5 * i}")


# U = int(input("Введите первое число: "))
# S = int(input("Введите второе число: "))
# A = int(input("Введите третье число: "))

# if U <= S and U <= A:
#     QQ = U
# elif S <= U and S <= A:
#     QQ = S
# else:
#     QQ = A
    
# print("Наименьшее число:", QQ)





# Nurs = int(input("Введите число: "))

# if Nurs == 0:
#     print("Чётное")
# else:
#     print("Нечётное")