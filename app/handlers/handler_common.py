from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from db.db_access import add_new_user, get_word, add_new_user_word


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    add_new_user(message.from_user.id)
    await message.answer(
        "Вы в главном меню,\nдля просмотра слов воспульзуйтесь командой /words\nдля тренировки слов - /training",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_stop(state: FSMContext):
    await state.finish()


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_start, commands="stop", state="*")
