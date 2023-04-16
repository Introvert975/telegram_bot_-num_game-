import random
from aiogram import *
from aiogram.types import *
TOKEN_BOT = ""

bot = Bot(TOKEN_BOT)
dp = Dispatcher(bot)


user = {'game': False, 'secretNumber': 0, 'try': 0}

@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton("Играть", callback_data="b_yes")
    button_no = InlineKeyboardButton("Не хочу играть", callback_data="b_no")
    markup.add(button_yes, button_no)
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEImolkO9NBdyvYsZPsR5Z2BCFh8t_BbAACjxIAAg_baErnmSd7h7_6fS8E")
    await message.answer("Привет, Хочешь сыграть?", reply_markup=markup)
@dp.callback_query_handler(lambda call: call.data == "b_yes")
async def bot_game(callback: types.callback_query):
    user['game'] = True
    user['try'] = 9
    user['secretNumber'] = random.randint(1, 1000)
    await bot.send_sticker(callback.from_user.id,
                           sticker="CAACAgIAAxkBAAEImpRkO9QCA_JWUQ27cndH4aR3zYK7DwACwBYAAksMaEowP3dTRHrdMy8E")

    await callback.message.answer("Я загадал число от 1 до 1000 \n У тебя есть 10 попыток")


@dp.message_handler()
async def in_game(message: types.Message):
    if user['game'] == True:
        number = int(message.text)
        if (user['secretNumber'] == number) or (user['try'] == 0):

            user['game'] = False
            markup = InlineKeyboardMarkup()
            button_yes = InlineKeyboardButton("Да", callback_data="b_yes")
            button_no = InlineKeyboardButton("Нет", callback_data="b_no")
            markup.add(button_yes, button_no)
            if user['secretNumber'] == number:
                await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEImphkO9Tud2rWl1rNGmgUR61eWnPengACUBUAAibGYUqjxUzZqcTGni8E")
                await message.answer("Поздравляю, вы выиграли\n Сыграем ещё? ", reply_markup=markup)
            else:
                await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEImppkO9Uiqeiti7_ri0C-qQEIHoxW9QACzBYAAjkjaUpmBoYjs1dw4i8E")
                await message.answer("Не повезло , вы проиграли \n Может сыграем ещё?", reply_markup=markup)

        elif user['secretNumber'] < number:
            user['try'] -= 1
            await message.answer(f"Моё число меньше \n Oсталось попыток: {user['try']+1}")
        elif user['secretNumber'] > number:
            user['try'] -= 1
            await message.answer(f"Моё число больше \n Oсталось попыток: {user['try']+1}")


@dp.callback_query_handler(lambda call: call.data == "b_no")
async def bot_not_game(callback: types.callback_query):
    user['game'] = False
    await bot.send_sticker(callback.from_user.id, sticker="CAACAgIAAxkBAAEImpxkO9VEVggoOU0YXlaGhe3mPfuAegAClBQAAkrfaEqmCCUKim7WLi8E")
    await callback.message.answer("Очень жаль.. :(\nЕсли понадоблюсь отправь /start")


def BOT():
    try:
        executor.start_polling(dp)
    except:
        print("TOKEN_Err0r")