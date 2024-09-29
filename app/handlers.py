from aiogram import F, Router

from aiogram.types import Message, InputFile
from aiogram.filters import CommandStart

from app.utils import *

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт, давай я допоможу тобі ")




@router.message(F.text == "о")
async def start_monitoring(message: Message):
    symbols = [
        'BTC/USDT', 
        'ETH/USDT', 
        'LTC/USDT', 
        'XRP/USDT', 
        'BCH/USDT', 
        'DOT/USDT', 
        'LINK/USDT', 
        'SOL/USDT', 
        'ADA/USDT', 
        'DOGE/USDT', 
        'MATIC/USDT', 
        'AVAX/USDT', 
        'TRX/USDT', 
        'XLM/USDT', 
        'SHIB/USDT'
    ]  # Список криптовалют для моніторингу
    timeframe = '1m'  # Таймфрейм свічок: 1h, 1m тощо
    await message.answer("Надсилаю..")

    await monitor_candlesticks(symbols, timeframe, message)

@router.message(F.text == "p")
async def start_monitoring(message: Message):
    symbol = 'BTC/USDT'  # Список криптовалют для моніторингу
    timeframe = '1m'  # Таймфрейм свічок: 1h, 1m тощо
    await message.answer("Надсилаю..")

    chart_image = create_chart(symbol, timeframe)
    input_file = BufferedInputFile(chart_image.getvalue(), filename='candlestick_chart.png')

    # Надсилаємо зображення користувачу
    await message.answer_photo(input_file, caption=f"Графік для {symbol}")


