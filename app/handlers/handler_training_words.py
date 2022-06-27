from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from util.keyboard import generate_type_training, generate_know_training, generate_word_info
from logic.training_words import DataSet


class ShowWords(StatesGroup):
    train_words = State()


async def start_train_words(message: types.Message, state: FSMContext):
    await state.finish()
    keyword = generate_type_training()
    await message.answer(f'Выберите тип тренировки', reply_markup=keyword)


async def process_callback_type_train(callback_query: types.CallbackQuery, state: FSMContext):
    await ShowWords.train_words.set()
    dataset = DataSet(callback_query.from_user.id, callback_query.data)
    new_word = dataset.get_new_word()
    keyword_info = generate_word_info()
    await state.update_data(dataset=dataset, new_word=new_word)
    if new_word is not None:
        await callback_query.message.answer(f'Как переводится слово: {new_word.word}', reply_markup=keyword_info)
    else:
        await callback_query.message.answer('Словарь пуст', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    await callback_query.answer(show_alert=False)


async def train_words(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    data_set = user_data['dataset']
    if message.text.lower() == 'пример':
        example = data_set.get_current_word()
        await message.answer(f'{example.word_example}')
        return
    if message.text.lower() == 'значение':
        example = data_set.get_current_word()
        await message.answer(f'{example.word_mean}')
        return
    response = data_set.check_answer(message.text.lower())
    keyword_info = generate_word_info()
    if response is not None:
        if response.answer_result == 0:
            await state.update_data(dataset=data_set, new_word=response)
            await message.answer(f'Как переводится слово: {response.word}', reply_markup=keyword_info)
        elif response.answer_result == 1:
            keyword = generate_know_training()
            await state.update_data(dataset=data_set, new_word=response)
            await message.answer('Верно', reply_markup=keyword)
        elif response.answer_result == 2:
            await message.answer('Try again')
            await state.update_data(dataset=data_set, new_word=response)
        elif response.answer_result == 3:
            last_word = data_set.get_last_word()
            await message.answer(f'Слово: {last_word.word}, перевод: {last_word.word_translate}')
            await state.update_data(dataset=data_set, new_word=response)
            await message.answer(f'Как переводится слово: {response.word}', reply_markup=keyword_info)
        elif response.answer_result == 4:
            last_word = data_set.get_last_word()
            await message.answer(f'Слово: {last_word.word}, перевод: {last_word.word_translate}')
            await state.update_data(dataset=data_set, new_word=response)
            await message.answer(f'Как переводится слово: {response.word}', reply_markup=keyword_info)
    else:
        await state.finish()
        await message.answer('Training done', reply_markup=types.ReplyKeyboardRemove())


async def process_callback_know_train(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    keyword_info = generate_word_info()
    dataset = user_data['dataset']
    new_word = dataset.check_user_choice(callback_query.data)
    await state.update_data(dataset=dataset, new_word=new_word)
    if new_word is not None:
        await callback_query.message.answer(f'Как переводится слово: {new_word.word}', reply_markup=keyword_info)
    else:
        await callback_query.message.answer(f'Training done', reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    await callback_query.answer(show_alert=False)


def register_handlers_training(dp: Dispatcher):
    dp.register_message_handler(start_train_words, commands="training", state="*")
    dp.register_callback_query_handler(process_callback_type_train, lambda c: c.data and c.data.startswith('button'),
                                       state='*')
    dp.register_callback_query_handler(process_callback_know_train, lambda c: c.data and c.data.startswith('know'),
                                       state=ShowWords.train_words)
    dp.register_message_handler(train_words, state=ShowWords.train_words)