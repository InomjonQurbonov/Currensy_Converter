from aiogram import Router
from aiogram.types import Message
import re
import requests
from config import courses

msg_router = Router()

def get_exchange_rate(date, currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        rate = data['rates']['UZS']
        return rate
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch exchange rate: {e}")

@msg_router.message()
async def convert_sum(message: Message):
    try:
        x = message.text

        if x.isdigit():
            amount = float(x)
            await handle_currency_conversion(message, amount)

        elif re.match(r'\d{4}-\d{2}-\d{2} [A-Z]{3}', x) or re.match(r'[A-Z]{3} \d{4}-\d{2}-\d{2}', x):
            parts = x.split(' ')
            date = parts[0] if parts[0].startswith('20') else parts[1]
            currency = parts[1] if parts[1].isalpha() else parts[0]
            rate = get_exchange_rate(date, currency)
            await message.reply(f"{date} sanasidagi {currency} kursi:\n\n\t - 1 {currency} = {rate:.2f} so'm")

        elif '$' in x:
            currency = 'USD'
            amount = float(x.replace('$', ''))
            await handle_currency_conversion(message, amount, currency)

        elif 'dollar' in x:
            currency = 'USD'
            amount = float(x.replace('dollar', ''))
            await handle_currency_conversion(message, amount, currency)

        elif 'yevro' in x:
            currency = 'EUR'
            amount = float(x.replace('yevro', ''))
            await handle_currency_conversion(message, amount, currency)

        elif 'rubl' in x or '🇷🇺' in x:
            currency = 'RUB'
            amount = float(x.replace('rubl', '').replace('🇷🇺', ''))
            await handle_currency_conversion(message, amount, currency)

        else:
            amount = float(x)
            await handle_currency_conversion(message, amount)

    except ValueError as e:
        await message.reply(f"---Uzur, xatolik yuz berdi: {e}---")
    except Exception as e:
        await message.reply(f"---Uzur, qandaydir xatolik yuz berdi: {e}---")

async def handle_currency_conversion(message, amount, currency='UZS'):
    if currency != 'UZS':
        amount_in_som = amount * courses[currency]
        await message.reply(f"{amount} {currency}:\n\n\t - {amount_in_som:.2f} so'm")
    else:
        s = f"{amount} so'm:\n\n"
        s += f"\t - {amount / courses['USD']:.2f} dollar\n"
        s += f"\t - {amount / courses['RUB']:.2f} rubl\n"
        s += f"\t - {amount / courses['EUR']:.2f} yevro\n"
        await message.reply(s)
