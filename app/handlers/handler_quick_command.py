from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from db.db_access import add_new_user, get_word, add_new_user_word, get_leaned_words, get_word_info, delete_word


async def cmd_show_learned_words(message: types.Message, state: FSMContext):
    await state.finish()
    msg = 'Изученные слова:\n'
    user_id = message.from_user.id
    learned_words = get_leaned_words(int(user_id))
    for learned_word in learned_words:
        word_info = get_word_info(learned_word)
        ms = f'{word_info.word} - {word_info.word_translate}\n'
        msg += ms
    await message.answer(msg)


async def delete_user_word(message: types.Message):
    word_info = message.text.replace('/del', '').strip().lower()

    word = get_word(word_info)

    if len(word) > 0:
        try:
            delete_word(word[0], int(message.from_user.id))
            await message.answer('Слово удалено из изученных')
        except:
            await message.answer('В вашем словаре нет таких слов')
    else:
        await message.answer('В словаре нет таких слов')


def register_handlers_quick(dp: Dispatcher):
    dp.register_message_handler(cmd_show_learned_words, commands='learned', state="*")
    dp.register_message_handler(delete_user_word, lambda message: message.text.startswith('/del'), state="*")