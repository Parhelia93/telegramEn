from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from util.keyboard import generate_keyboard
from logic.show_words import ShowDataSet


class ShowWords(StatesGroup):
    show_words = State()


async def start_show_words(message: types.Message, state: FSMContext):
    await state.finish()
    await ShowWords.show_words.set()
    data_set = ShowDataSet(message.from_user.id)
    await state.update_data(data_set=data_set)
    word = data_set.get_new_word()
    if word is not None:
        keyboard = generate_keyboard()
        file_path = f'files/audio/{word.word}.mp3'
        text_message = f'Cлово: {word.word} - {word.word_translate}\n' \
                       f'Пример: {word.example_using}'
        try:
            await message.answer_voice(voice=open(file_path, "rb"),
                                       caption=text_message,
                                       reply_markup=keyboard)
        except:
            await message.answer(text_message, reply_markup=keyboard)
    else:
        await message.answer("Вы выучили все слова")


async def chose_word_result(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    data_set = user_data['data_set']
    word = data_set.user_choice(call.data)
    if word is not None:
        keyword = generate_keyboard()
        file_path = f'files/audio/{word.word}.mp3'
        text_message = f'Cлово: {word.word} - {word.word_translate}\n' \
                       f'Пример: {word.example_using}'
        try:
            await call.message.answer_voice(voice=open(file_path, "rb"),
                                            caption=text_message,
                                            reply_markup=keyword)
        except:
            await call.message.answer(text_message,
                                      reply_markup=keyword)
        await state.update_data(data_set=data_set)
    else:
        await state.finish()
        await call.message.answer('Приступайте к тренировке')
    await call.answer(show_alert=False)


def register_handlers_words(dp: Dispatcher):
    dp.register_message_handler(start_show_words, commands="words", state="*")
    dp.register_callback_query_handler(chose_word_result, lambda c: c.data and c.data.startswith('button'),
                                       state=ShowWords.show_words)