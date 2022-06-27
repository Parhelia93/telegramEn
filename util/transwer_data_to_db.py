from db.db_model import init_db, get_engine, Word
from sqlalchemy.orm import Session

words = []
with open('text/words_data.txt', mode='r',encoding='utf-8') as file:
    arr = file.readlines()
    for i in arr:
        src = i.replace('\n','')
        word_data = src.split('---')
        word = Word(
            word=word_data[0],
            word_translate=word_data[3],
            meaning_of_word=word_data[1],
            example_using=word_data[2]
        )
        words.append(word)

init_db()
engine = get_engine()

with Session(bind=engine) as ses:
    ses.add_all(words)
    ses.commit()