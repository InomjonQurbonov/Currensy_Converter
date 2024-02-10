from datetime import date, timedelta
import json
import requests
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import courses

cmd_router = Router()


@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    s = "Salom! Men sizni so'qqangizni:\n\n" \
        "\t- USD💸\n" \
        "\t- EURO💸\n" \
        "\t- RUBL💸\n\n" \
        "ga almashtirishga yordam beraman.\n" \
        "👌 Barcha ma'lumotlar O'zbekiston Markaziy Bankidan olingan.\n" \
        "👨‍💻 Botdan to'liq foydalanish uchun /help buyrug'ini bosing 👨‍💻"
    await message.answer(s)

@cmd_router.message(Command('help'))
async def cmd_help(message: Message):
    s = "👇 Quyidagi kommandalar orqali botdan samarali foydalanishingiz mumkin 👇\n" \
        "\t - /kurslar = Valyuta kurslarini bilish\n" \
        "\t - /usd = Dollar kursini bilish\n" \
        "\t - /rubl = Rubl kursini bilish\n" \
        "\t - /euro = Yevro kursini bilish\n" \
        "\t - /ads = Botga reklama joylash\n" \
        "Agar biror bir summani jo'natsangiz, bot uni turli valyutalarda qiymatini qaytaradi (Masalan: 1000000)"
    await message.answer(s)

@cmd_router.message(Command('kurslar'))
async def cmd_kurslar(message: Message):
    response = requests.get("https://cbu.uz/oz/arkhiv-kursov-valyut/json/")
    s = "Bugungi valyuta kurslari:\n"
    for kurs in response.json():
        if kurs['Ccy'] in courses:
            courses[kurs['Ccy']] = float(kurs['Rate'])
            s += f"1 {kurs['CcyNm_UZ']} - {kurs['Rate']} so'm\n"
    await message.answer(s)

@cmd_router.message(Command('usd'))
async def cmd_usd(message: Message):
    s = f"1 AQSH dollari {courses['USD']} so'mga teng"
    await message.reply(s)

@cmd_router.message(Command('rubl'))
async def cmd_rubl(message: Message):
    s = f"1 Rossiya rubli {courses['RUB']} so'mga teng"
    await message.reply(s)

@cmd_router.message(Command('euro'))
async def cmd_euro(message: Message):
    s = f"1 Yevro {courses['EUR']} so'mga teng"
    await message.reply(s)

@cmd_router.message(Command('ads'))
async def cmd_ads(message: Message):
    s = "Salom! Reklama bo'yicha Admin bilan bog'laning\n👨‍💻 Admin: @deLONEWOLFuz"
    await message.answer(s)

@cmd_router.message(Command('hafta'))
async def cmd_hafta(message: Message):
    today = date.today()
    start_week = today - timedelta(today.weekday())
    end_week = start_week + timedelta(7)
    weekly_rates = {'USD': [], 'EUR': [], 'RUB': []}

    for i in range((end_week - start_week).days):
        day = start_week + timedelta(days=i)
        response = requests.get(f"https://cbu.uz/oz/arkhiv-kursov-valyut/json/{day}/")

        if response.ok:
            rates = json.loads(response.text)
            for rate in rates:
                if rate['Ccy'] in weekly_rates:
                    weekly_rates[rate['Ccy']].append(float(rate['Rate']))

    s = "Joriy haftadagi valyuta kurslari:\n"
    for currency, rates in weekly_rates.items():
        if rates:
            average_rate = sum(rates) / len(rates)
            s += f"1 {currency} - {average_rate} so'm\n"
        else:
            s += f"1 {currency} - No data available\n"

    await message.answer(s)
