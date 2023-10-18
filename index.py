from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatMember
from aiogram import types
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
import dotenv
import os
import asyncio

dotenv.load_dotenv()


dp = Dispatcher()
bot = Bot(os.getenv('BOT_TOKEN'))

@dp.message(Command('start'))
async def handle_start(msg: Message):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Забрать гайд", callback_data="cmd_getguide")],
            [types.InlineKeyboardButton(
                text="Сайт 1", url="https://www.google.com/")],
            [types.InlineKeyboardButton(
                text="Сайт 2", url="https://www.google.com/")],
        ])
        await bot.send_message(msg.chat.id, "Привет! Рада тебя видеть здесь! Выбери, что тебя интересует:", reply_markup=keyboard)

async def get_guide(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text="Подписаться", url="https://t.me/+OFaUBkDL3ullZDUy")],
        [types.InlineKeyboardButton(
            text="Забрать гайд", callback_data="cmd_check")],
        [types.InlineKeyboardButton(
            text="Назад", callback_data="cmd_main")],
    ])
    await bot.send_message(callback.message.chat.id, text="Проверь подписку на канал и получи материалы: ", reply_markup=keyboard)

@dp.callback_query(F.data.startswith('cmd'))
async def commands(callback: types.CallbackQuery):
    data = callback.data.split("_")
    action = data[1]

    if action == "main":
        await handle_start(callback.message)     
    if action == "getguide":
        await get_guide(callback)
    if action == "check":
        try:
            chat_member= await bot.get_chat_member(chat_id="-1001956578309", user_id=callback.from_user.id) 
            if chat_member.status == 'member' or chat_member.status == 'creator' or chat_member.status == 'administrator':
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [types.InlineKeyboardButton(
                        text="Назад", callback_data="cmd_main")]
                ])
                doc = FSInputFile('guide.pdf')
                await bot.send_document(callback.message.chat.id, document=doc, caption="Спасибо за подписку! Забирай гайд!", reply_markup=keyboard)
            else:
                await get_guide(callback)
        except:
            await get_guide(callback)


async def main():
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())