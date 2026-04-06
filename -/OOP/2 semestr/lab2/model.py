class QuizGame:
    def __init__(self, questions):
        self.questions = questions
        self.current_index = 0
        self.correct_answers = 0

    def get_current_question(self):
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def check_answer(self, selected_idx):
        if int(selected_idx) == self.questions[self.current_index]['correct_index']:
            self.correct_answers += 1
            return True
        return False