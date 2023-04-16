import random
from aiogram import *
from aiogram.types import *
TOKEN_BOT = "6249406770:AAE8SOaU8DgdH9E8U9bHYi2NWexljTBZ4PU"
hello = ["CAACAgIAAxkBAAEImolkO9NBdyvYsZPsR5Z2BCFh8t_BbAACjxIAAg_baErnmSd7h7_6fS8E", "CAACAgIAAxkBAAEIm1BkO_bcmQg7EH7PV3hVE4x5B-eBhwACxRQAAvwXYUp3rqvvQQmQFy8E",
         "CAACAgIAAxkBAAEIm1JkO_lLqKgf0UJRl64DPvokv_UbgQACChUAAlbjYErbZPspKioqbC8E", "CAACAgIAAxkBAAEIm1RkO_mikxsOT3QlaZS0Lb4QGDMzIAACGw8AAseraUr4_E2EmatxdC8E"]
thinking = ["CAACAgIAAxkBAAEImpRkO9QCA_JWUQ27cndH4aR3zYK7DwACwBYAAksMaEowP3dTRHrdMy8E", "CAACAgIAAxkBAAEIm1ZkO_qBJ5BjYwgHYH35I-JswD0znwAC1xMAAmlxYUqc8C9Y00Fy4S8E",
            "CAACAgIAAxkBAAEIm1hkO_rXoR-FJYoLUGVTA9FNDMEP-gACGREAAtEYYUrhNe9nUVED9C8E", "CAACAgIAAxkBAAEIm1pkO_r-IOV5Ff0dF1UIY1sa6X76CwACphQAAv3YYUoB0w92Eg5kti8E"]
wins = ["CAACAgIAAxkBAAEImphkO9Tud2rWl1rNGmgUR61eWnPengACUBUAAibGYUqjxUzZqcTGni8E", "CAACAgIAAxkBAAEIm15kO_wMomAVKbBySYed2TiRSqT7uQACmRQAAuhGaUosP4xpVDKWiy8E",
        "CAACAgIAAxkBAAEIm2BkO_wpUHUnGQfsIVrwYFhjhATAcgAC6xIAAh_lYEpaX_QyDBOumi8E", "CAACAgIAAxkBAAEIm2JkO_2Ss9KWHDoNYNYfxjnVe_JQOAACTBEAAmUlYUoO-5s00KvT5S8E"]
fails = ["CAACAgIAAxkBAAEIm21kPAABJ8V-ZbOTyMQTZHTeMTFXd0cAAs0UAAJ29WFKDDJtfGAvP74vBA", "CAACAgIAAxkBAAEImppkO9Uiqeiti7_ri0C-qQEIHoxW9QACzBYAAjkjaUpmBoYjs1dw4i8E",
         "CAACAgIAAxkBAAEIm29kPAABWLUUpHxXQziVH4oVFRypYHgAAmEQAAIfnGFKivO-YUvGMLMvBA"]
exits = ["CAACAgIAAxkBAAEIm3VkPAABuNuvQTM1_e68wPhIT-gJ6HkAApoTAAJ-zGhKEA8xm0AXuDMvBA", "CAACAgIAAxkBAAEIm3dkPAAB1Nh5QY4XG1uwS4rnXlcjBN8AAuMTAAMaaUr7tMvKPHcb6S8E",
         "CAACAgIAAxkBAAEIm3NkPAABrGfhNEsxHqQDJZn2wRlzlYAAApAQAALmRmFKdEVPTuY-gisvBA", "CAACAgIAAxkBAAEIm3FkPAABpfBTPZFISkd8yk6lAcJwsBkAAvETAALDcWBKS5Vvxn6XzOAvBA",
         "CAACAgIAAxkBAAEImpxkO9VEVggoOU0YXlaGhe3mPfuAegAClBQAAkrfaEqmCCUKim7WLi8E"]
bot = Bot(TOKEN_BOT)
dp = Dispatcher(bot)


user = {'game': False, 'secretNumber': 0, 'try': 0}

@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton("Играть", callback_data="b_yes")
    button_no = InlineKeyboardButton("Не хочу играть", callback_data="b_no")
    markup.add(button_yes, button_no)
    await bot.send_sticker(message.from_user.id, sticker = hello[random.randint(0, 3)])
    await message.answer("Привет, Хочешь сыграть?", reply_markup=markup)
@dp.callback_query_handler(lambda call: call.data == "b_yes")
async def bot_game(callback: types.callback_query):
    user['game'] = True
    user['try'] = 9
    user['secretNumber'] = random.randint(1, 1000)
    await bot.send_sticker(callback.from_user.id,
                           sticker=thinking[random.randint(0, 3)])

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
                await bot.send_sticker(message.from_user.id, sticker= wins[random.randint(0, 3)])
                await message.answer("Поздравляю, вы выиграли\n Сыграем ещё? ", reply_markup=markup)
            else:
                await bot.send_sticker(message.from_user.id, sticker=fails[random.randint(0, 2)])
                await message.answer("Хи-хи-хи) Не повезло , вы проиграли \n Может сыграем ещё?", reply_markup=markup)

        elif user['secretNumber'] < number:
            user['try'] -= 1
            await message.answer(f"Моё число меньше \n Oсталось попыток: {user['try']+1}")
        elif user['secretNumber'] > number:
            user['try'] -= 1
            await message.answer(f"Моё число больше \n Oсталось попыток: {user['try']+1}")


@dp.callback_query_handler(lambda call: call.data == "b_no")
async def bot_not_game(callback: types.callback_query):
    user['game'] = False
    await bot.send_sticker(callback.from_user.id, sticker=exits[random.randint(0, 4)])
    await callback.message.answer("Очень жаль.. :(\nЕсли понадоблюсь отправь /start")


def BOT():
    try:
        executor.start_polling(dp)
    except:
        print("TOKEN_Err0r")