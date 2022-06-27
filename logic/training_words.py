from dataclasses import dataclass
from db.db_access import get_training_dataset, get_word_info, update_word_data, get_user_word


@dataclass
class NewWord:
    id: int
    word_id: int
    true_answer: int
    false_answer: int
    stage: int
    word: str
    word_translate: str
    word_example: str
    word_mean: str
    answer_result: int


class DataSet:
    def __init__(self, user_id: str, user_choice: str):
        self.limit = 10
        self.user_id = int(user_id)
        self.user_choice = user_choice[-1]
        self.counter = 0
        self.dataset = self.get_user_dataset()
        self.train_limit = len(self.dataset)
        self.wrong_answer = 0

    def get_user_dataset(self):
        data_set = []
        user_words = get_training_dataset(self.user_id)
        for user_word in user_words:
            word_info = get_word_info(user_word)
            word_question = word_info.word if self.user_choice == '1' else word_info.word_translate
            word_answer = word_info.word_translate if self.user_choice == '1' else word_info.word
            data_set.append(NewWord(id=user_word.id, word_id=word_info.id, true_answer=user_word.true_answer,
                                    false_answer=user_word.false_answer, stage=user_word.learn_stage,
                                    word=word_question, word_translate=word_answer,
                                    word_example=word_info.example_using,
                                    word_mean=word_info.meaning_of_word, answer_result=0))
        return data_set

    def get_new_word(self):
        self.wrong_answer = 0
        if self.counter < self.train_limit:
            word = self.dataset[self.counter]
            self.counter += 1
            return word
        else:
            return None

    def get_train_limit(self):
        return self.train_limit

    def get_current_word(self):
        return self.dataset[self.counter - 1]

    def get_last_word(self):
        return self.dataset[self.counter - 2]

    def check_answer(self, answer: str):
        current_word = self.get_current_word()
        current_word_arr = current_word.word_translate.split(', ')
        user_word = get_user_word(current_word.id)
        dont_know = ['не знаю', 'хз', 'Не знаю']
        if answer in current_word_arr and current_word.true_answer - current_word.false_answer < 2:
            current_word.true_answer += 1
            user_word.true_answer=current_word.true_answer
            update_word_data(user_word)
            new_word = self.get_new_word()
            return new_word
        elif answer in current_word_arr and current_word.true_answer - current_word.false_answer >= 2:
            current_word.true_answer += 1
            user_word.true_answer = current_word.true_answer
            update_word_data(user_word)
            current_word.answer_result = 1
            return current_word
        elif answer not in current_word_arr and self.wrong_answer < 2 and answer not in dont_know:
            self.wrong_answer += 1
            current_word.false_answer += 1
            current_word.answer_result = 2
            user_word.false_answer = current_word.false_answer
            update_word_data(user_word)
            return current_word
        elif answer not in current_word_arr and self.wrong_answer >= 2 and answer not in dont_know:
            current_word.false_answer += 1
            user_word.false_answer = current_word.false_answer
            update_word_data(user_word)
            new_word = self.get_new_word()
            if new_word is not None:
                new_word.answer_result = 3
            return new_word
        elif answer in dont_know:
            self.wrong_answer += 1
            current_word.false_answer += 1
            user_word = get_user_word(current_word.id)
            user_word.false_answer = current_word.false_answer
            update_word_data(user_word)
            new_word = self.get_new_word()
            if new_word is not None:
                new_word.answer_result = 4
            return new_word

    def check_user_choice(self, choice: str):
        user_choice = choice[-1]
        stage = 1 if user_choice == '1' else 0
        current_word = self.get_current_word()
        current_word.stage = stage
        user_word = get_user_word(current_word.id)
        user_word.learn_stage = current_word.stage
        update_word_data(user_word)
        return self.get_new_word()
