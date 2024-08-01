from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
import logging
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



english = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Full textbook")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


API_TOKEN = '7357998875:AAF66o7BFnNZSvWSJDi1w4loCklSgTYHl00'
CHANNELS = ['-1002174544605']  # Channels to subscribe to

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def on_startup(dispatcher):
    logging.info("Bot is starting...")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if await check_subscription(user_id):
        await message.answer("You are subscribed to the required channels!", reply_markup=english)
    else:
        keyboard = InlineKeyboardMarkup(row_width=1)  # 1 button per row
        subscribe_button = InlineKeyboardButton(
            text="Join Our Channel 📢",
            url="https://t.me/+9BHjNg7-zCI0NDg6"  # Adjust URL to your channel or a group link
        )
        submit_button = InlineKeyboardButton(
            text="Submit ✔️",
            callback_data='submit'
        )
        keyboard.add(subscribe_button, submit_button)
        await message.answer(
            "Please subscribe to our channels to access this bot. Click the buttons below to join and submit your response:",
            reply_markup=keyboard
        )

@dp.callback_query_handler(lambda c: c.data == 'submit')
async def process_callback_submit(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if await check_subscription(user_id):
        await bot.answer_callback_query(callback_query.id, text="Thank you for your submission!")
        await bot.send_message(user_id, "Your subscription has been confirmed!", reply_markup=english)
    else:
        await bot.answer_callback_query(callback_query.id, text="Please subscribe to the channels first.")
        await bot.send_message(user_id, f"You need to subscribe to the required channels before submitting.")

async def check_subscription(user_id):
    for channel in CHANNELS:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ('member', 'administrator', 'creator'):
            return False
    return True

@dp.message_handler(commands=['somecommand'])
async def some_command(message: types.Message):
    user_id = message.from_user.id
    if await check_subscription(user_id):
        await message.answer("You have access to this command!")
    else:
        await message.answer("You need to subscribe to the required channels first.")



@dp.message_handler(Text(equals="Full textbook"))
async def get_menyu(message: Message, state: FSMContext):
    await message.answer(
        text=f"♾Siz 550,000 so’mlik darslarimizni🎓 bepul qolga kirtingiz tabriklaymiz!✔️.\n\n❗️Sizga bir martalik link 🔗 beriladi!\n\nhttps://t.me/+NSRSCnHDaYU1NDRi\n✅Yaqin orada zayavkangiz qabul qilinadi!", reply_markup=english
    )




if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
