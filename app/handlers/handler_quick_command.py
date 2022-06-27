from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from db.db_access import add_new_user, get_word, add_new_user_word, get_leaned_words, get_word_info


# async def cmd_show_learned_words(message: types.Message, state: FSMContext):
#     await state.finish()
#     msg = 'Изученные слова:\n'
#     user_id = message.from_user.id
#     learned_words = get_leaned_words(int(user_id))
#     for learned_word in learned_words:
#         word_info = get_word_info(learned_word)
#         ms = f'{word_info.word} - {word_info.word_translate}'
#         msg += ms
#     await message.answer(msg)


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


def register_handlers_quick(dp: Dispatcher):
    dp.register_message_handler(search_word, lambda message: message.text, state="*")
    # dp.register_message_handler(cmd_show_learned_words, lambda message: message.text.startswith('/learned'), state="*")