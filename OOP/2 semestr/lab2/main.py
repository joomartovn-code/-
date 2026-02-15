import telebot
from telebot import types
from data.questions import QUESTIONS
from database.db_manager import Database
from models.quiz import QuizGame

TOKEN = "8378188677:AAGCIuRZ_63SiFwDcKHmlvvogu2JnNs7F3Q"

class ClassmateBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.db = Database()
        self.user_data = {}

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.user_data[message.chat.id] = {"user_id": message.chat.id}
            msg = self.bot.send_message(message.chat.id, "Начинаем регистрацию!\n1. Введите ФИО:")
            self.bot.register_next_step_handler(msg, self.step_1)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.process_quiz(call)

   
    def step_1(self, m): self.next_step(m, 'fio', "2. Возраст?")
    def step_2(self, m): self.next_step(m, 'age', "3. Шифр группы?")
    def step_3(self, m): self.next_step(m, 'group_code', "4. Телефон?")
    def step_4(self, m): self.next_step(m, 'phone', "5. Email?")
    def step_5(self, m): self.next_step(m, 'email', "6. GitHub?")
    def step_6(self, m): self.next_step(m, 'github', "7. Язык программирования?")
    def step_7(self, m): self.next_step(m, 'lang', "8. Опыт работы?")
    def step_8(self, m): self.next_step(m, 'experience', "9. Хобби?")
    def step_9(self, m): self.next_step(m, 'hobby', "10. Город?")
    
    def step_10(self, m):
        self.user_data[m.chat.id]['city'] = m.text
        self.db.add_student(self.user_data[m.chat.id])
        self.bot.send_message(m.chat.id, "✅ Регистрация завершена! Данные в БД.\nНачинаем квиз!")
        self.user_data[m.chat.id]['game'] = QuizGame(QUESTIONS)
        self.send_question(m.chat.id)

    def next_step(self, message, field, next_text):
        self.user_data[message.chat.id][field] = message.text
        current_step_num = int(list(self.user_data[message.chat.id].keys()).index(field))
        next_methods = [self.step_1, self.step_2, self.step_3, self.step_4, self.step_5, 
                        self.step_6, self.step_7, self.step_8, self.step_9, self.step_10]
        
        msg = self.bot.send_message(message.chat.id, next_text)
        self.bot.register_next_step_handler(msg, next_methods[current_step_num])

    def send_question(self, user_id):
        game = self.user_data[user_id]['game']
        q = game.get_current_question()
        if not q:
            self.bot.send_message(user_id, f"Конец! Результат: {game.correct_answers}/15")
            return
        
        markup = types.InlineKeyboardMarkup()
        for i, opt in enumerate(q['options']):
            markup.add(types.InlineKeyboardButton(text=opt, callback_data=str(i)))
        self.bot.send_message(user_id, q['text'], reply_markup=markup)

    def process_quiz(self, call):
        user_id = call.message.chat.id
        game = self.user_data[user_id]['game']
        if game.check_answer(call.data):
            self.bot.answer_callback_query(call.id, "Верно!")
        else:
            self.bot.answer_callback_query(call.id, "Ошибка!")
        
        self.bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup=None)
        game.current_index += 1
        self.send_question(user_id)

    def run(self):
        self.bot.infinity_polling()

if __name__ == "__main__":
    ClassmateBot().run()