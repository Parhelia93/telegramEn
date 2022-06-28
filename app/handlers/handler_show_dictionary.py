from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from db.db_access import get_word, add_new_user_word
from aiogram.dispatcher.filters.state import State, StatesGroup


class ShowDict(StatesGroup):
    show_dict = State()


async def start_show_words(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f'обро пожаловать в словарь!\nВводите слова чтобы увидеть перевод\nДля выхода нажмите в меню \stop')
    await ShowDict.show_dict.set()


async def search_word(message: types.Message):
    user_id = message.from_user.id
    word = message.text.strip().lower()
    data = get_word(word)
    if len(data) != 0:
        file_path = f'files/audio/{data[0].word}.mp3'
        text_message = f'Cлово: {data[0].word} - {data[0].word_translate}\n' \
                       f'Пример: {data[0].example_using}'
        try:
            await message.answer_voice(voice=open(file_path, "rb"), caption=text_message)
        except:
            await message.answer('Что-то пошло не так...')
        add_new_user_word(data[0], user_id, 0)
    else:
        await message.answer('В словаре нет такого слова')


def register_handlers_show_dict(dp: Dispatcher):
    dp.register_message_handler(search_word, lambda message: message.text, state=ShowDict.show_dict)
    dp.register_message_handler(start_show_words, commands='dict', state='*')