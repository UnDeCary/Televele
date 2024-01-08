import xml.dom.minidom

from aiogram import Bot, Dispatcher
import asyncio
from aiogram import types
from aiogram.filters import CommandStart,Command
from random import randint
import  json



bot= Bot(token='6631494300:AAGfvjcqtqTHY-JIzfvzvDKrSov0bP69lMY')

dp= Dispatcher()

def read()->dict:
    with open("data.json", "r") as file:
        data = json.load(file)
        return data
def write(data:dict):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

async def start():
    await dp.start_polling(bot)

@dp.message(Command("top"))
async def main(message: types.Message):
    data=read()
    ansmer=f"Топ:\n"
    for i in data:
        ansmer+=f"*[{data[i][3]}](https://t.me/{data[i][3]})* прошел за *{data[i][2]}* попытки\n"
    await message.answer(ansmer,parse_mode='MarkdownV2',disable_web_page_preview=True)

@dp.message(CommandStart())
async def main(message: types.Message):
    data=read()
    id = str(message.from_user.id)
    if id in data:
        if data[id][0]:
            await message.answer("Число уже загадано")
            return
        data[id]=[randint(1, 100), 0, data[id][2],message.from_user.username]

    else:
        data[id] = [randint(1, 100), 0, 999,message.from_user.username]
    await message.answer( "Я загадал число от 1 до 100 угадай его")

    write(data)



@dp.message()
async def ges(message: types.Message):

    id = str(message.from_user.id)


    if message.from_user.is_bot:
        return
    data=read()
    if id in data:
        if not data[id][0]:
            return
    else:
        return


    ges = message.text


    if not ges.isdigit():
        return
    ges=int(ges)


    if data[id][0]==ges:
        if data[id][1]<data[id][2]:
            data[id][2]=data[id][1]+1
        await message.answer(f"Поздравляю ты угадал с {data[id][1]} попытки, моё число действительно {data[id][0]}!")
        data[id][0] = None
        write(data)
        await main(message)



    elif data[id][0]>ges:
        await message.answer( "Не угадал, мое число больше")
        data[id][1] += 1



    elif data[id][0]<ges:

        await message.answer( "Не угадал, мое число меньше")
        data[id][1] += 1

    write(data)


if __name__=="__main__":
    asyncio.run(start())



