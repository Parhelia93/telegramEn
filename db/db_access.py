from db.db_model import get_engine, Word, UserWord, User
from sqlalchemy.orm import Session
import random
from typing import List
engine = get_engine()
DATASET_LEN = 5


def get_new_user_words(user_id: int) -> List[Word]:
    """Return dataset type Word of 10 random words"""
    with Session(bind=engine) as session:
        users_id = session.query(User.id).filter(User.user_id == user_id).all()
        user_id = users_id[0].id
        user_words = session.query(UserWord.word_id).filter(UserWord.user_id == user_id)
        user_words_lst = [user_word for (user_word,) in user_words]
        new_words = session.query(Word).filter(Word.id.not_in(user_words_lst)).all()
    if len(new_words) >= DATASET_LEN:
        return random.sample(new_words, DATASET_LEN)
    else:
        return random.sample(new_words, len(new_words))


def update_word_data(word: UserWord) -> None:
    """Update user_word info"""
    with Session(bind=engine) as session:
        session.add(word)
        session.commit()


def add_new_user(user_id: str) -> None:
    """Add new user on startup"""
    with Session(bind=engine) as session:
        user_exist = session.query(User).filter(User.user_id == int(user_id)).all()
        if len(user_exist) == 0:
            session.add(User(user_id=int(user_id)))
            session.commit()


def add_new_user_word(word: Word, user_id: int, stage: int) -> None:
    """Add new word in user_word table"""
    with Session(bind=engine) as session:
        check = session.query(UserWord).filter(UserWord.word_id == word.id).all()
        if len(check) == 0:
            session.add(UserWord(word_id=word.id, user_id=user_id, learn_stage=stage))
            session.commit()


def get_training_dataset(user_id: int) -> List[UserWord]:
    """Get dateset for training words"""
    with Session(bind=engine) as session:
        # return session.query(UserWord).filter(UserWord.user_id == user_id).filter(UserWord.learn_stage == 0).\
        #     limit(DATASET_LEN).all()
        train_data = session.query(UserWord).filter(UserWord.user_id == user_id).filter(UserWord.learn_stage == 0).all()
        if len(train_data) >= DATASET_LEN:
            return random.sample(train_data, DATASET_LEN)
        else:
            return random.sample(train_data, len(train_data))


def get_word_info(user_word: UserWord) -> Word:
    """GET description for user word"""
    with Session(bind=engine) as session:
        word_info = session.query(Word).filter(Word.id == user_word.word_id).all()
    return word_info[0]


def get_user_word(word_id: int) -> UserWord:
    with Session(bind=engine) as session:
        return session.query(UserWord).get(word_id)


def get_word(word: str) -> Word:
    with Session(bind=engine) as session:
        return session.query(Word).filter(Word.word == word).all()


def get_leaned_words(user_id: int) -> List[UserWord]:
    with Session(bind=engine) as session:
        return session.query(UserWord).filter(UserWord.user_id == user_id).filter(UserWord.learn_stage == 1)
