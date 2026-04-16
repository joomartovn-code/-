import random

class RouletteGame:
    def __init__(self, slots=6, bullets=1, max_lives=3):
        self.slots = slots
        self.bullets_count = bullets
        self.lives = max_lives
        self.drum = []
        self.reload()

    def reload(self):
        # Создаем барабан: 1 - пуля, 0 - пусто
        self.drum = [1] * self.bullets_count + [0] * (self.slots - self.bullets_count)
        random.shuffle(self.drum)

    def pull_trigger(self):
        if not self.drum:
            self.reload()
        return self.drum.pop()