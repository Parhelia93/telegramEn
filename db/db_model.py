from sqlalchemy import create_engine, Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy_utils import database_exists


engine = create_engine('sqlite:////home/aleksey/Documents/Projects/tegEn/db/en.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), unique=True)


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer(), primary_key=True)
    word = Column(String(30), nullable=False)
    word_translate = Column(String(30), nullable=False)
    meaning_of_word = Column(String(300), nullable=False)
    example_using = Column(String(300), nullable=False)


class UserWord(Base):
    __tablename__ = 'user_words'
    id = Column(Integer(), primary_key=True)
    word_id = Column(Integer(), ForeignKey('words.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))
    true_answer = Column(Integer(), default=0)
    false_answer = Column(Integer(), default=0)
    learn_stage = Column(Integer(), default=0)
    date_placed = Column(DateTime(), default=datetime.now)
    users = relationship('User')
    words = relationship('Word')


def init_db():
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)


def get_engine():
    return engine
