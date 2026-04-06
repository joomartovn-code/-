import random
import time

class RussianRouletteGame:
    def __init__(self, p1_id, p2_id):
        self.chambers = [0, 0, 0, 0, 0, 1]
        random.shuffle(self.chambers)
        self.current_index = 0
        self.is_active = True
        self.players = [
            {'id': p1_id, 'name': "Абдурахим"},
            {'id': p2_id, 'name': "Эльдар"}
        ]
        self.turn = random.randint(0, 1)
        self.turn_start_time = time.time()

    def shoot(self, user_id):
        if not self.is_active:
            return "Игра окончена. Перезарядите барабан."

        current_player = self.players[self.turn]
        
        if time.time() - self.turn_start_time > 5:
            self.is_active = False
            return f"Время вышло! {current_player['name']} проиграл."

        if user_id != current_player['id']:
            return f"Не твой ход! Сейчас очередь {current_player['name']}."

        if self.chambers[self.current_index] == 1:
            self.is_active = False
            return f"💥 БАХ! {current_player['name']} выбывает. Игра окончена."
        
        self.current_index += 1
        self.turn = 1 - self.turn
        self.turn_start_time = time.time()
        
        next_player = self.players[self.turn]
        return f"Щелчок... {current_player['name']} жив.  Очередь {next_player['name']}! (5 сек)"

    def reset(self):
        random.shuffle(self.chambers)
        self.current_index = 0
        self.is_active = True
        self.turn = random.randint(0, 1)
        self.turn_start_time = time.time()
        return f"Револьвер перезаряжен! Начинает {self.players[self.turn]['name']}."