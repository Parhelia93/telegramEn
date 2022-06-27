from db.db_access import get_new_user_words, add_new_user_word
from db.db_model import Word


class ShowDataSet:
    def __init__(self, user_id: str):
        self.user_id = int(user_id)
        self.counter = 0
        self.data_set = get_new_user_words(self.user_id)
        self.train_limit = len(self.data_set)

    def get_new_word(self) -> Word or None:
        if self.counter < self.train_limit:
            word = self.data_set[self.counter]
            self.counter += 1
            return word
        else:
            return None

    def user_choice(self, choice: str):
        code = choice[-1]
        current_word = self.data_set[self.counter-1]
        if code == '1':
            add_new_user_word(current_word, self.user_id, 1)
        elif code == '2':
            add_new_user_word(current_word, self.user_id, 0)
        return self.get_new_word()
