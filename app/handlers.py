from aiogram import F, Router

from aiogram.types import Message
from aiogram.filters import CommandStart, Command


from app.utils import *

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт, давай я допоможу тобі ")


@router.message(Command("monitor"))
async def start_monitoring(message: Message):
    # symbols = [
    #     'BTC/USDT', 
    #     'ETH/USDT', 
    #     'LTC/USDT', 
    #     'XRP/USDT', 
    #     'BCH/USDT', 
    #     'DOT/USDT', 
    #     'LINK/USDT', 
    #     'SOL/USDT', 
    #     'ADA/USDT', 
    #     'DOGE/USDT', 
    #     'MATIC/USDT', 
    #     'AVAX/USDT', 
    #     'TRX/USDT', 
    #     'XLM/USDT', 
    #     'SHIB/USDT',
    #     'ATOM/USDT',  # Cosmos
    #     'NEAR/USDT',  # Near Protocol
    #     'FTM/USDT',   # Fantom
    #     'ICP/USDT',   # Internet Computer
    #     'SAND/USDT',  # Sandbox
    #     'AAVE/USDT',  # Aave
    #     'UNI/USDT',   # Uniswap
    #     'GRT/USDT',   # The Graph
    #     'ALGO/USDT',  # Algorand
    #     'VET/USDT',   # VeChain
    #     'AXS/USDT',   # Axie Infinity
    #     'EGLD/USDT',  # Elrond
    #     'FIL/USDT',   # Filecoin
    #     'KSM/USDT',   # Kusama
    #     'RUNE/USDT',  # THORChain
    #     'ENJ/USDT',   # Enjin Coin
    #     '1INCH/USDT', # 1inch
    #     'ZIL/USDT',   # Zilliqa
    #     'ZRX/USDT'    # 0x
    # ]

    symbols = ['BTC/USDT', 
        'ETH/USDT', 
        'LTC/USDT', 
        'XRP/USDT', 
        'BCH/USDT',]

    timeframe = '15m'
    await message.answer("Починаю моніторити..")
    try:
        await monitor_candlesticks(symbols, timeframe, message)
    except:
        await message.answer("Щось пішло не так..")


@router.message(F.text == "p")
async def send(message: Message):
    symbol = 'BTC/USDT'  # Список криптовалют для моніторингу
    timeframe = '15m'  # Таймфрейм свічок: 1h, 1m тощо
    await message.answer("Надсилаю..")

    chart_image = create_chart(symbol, timeframe)
    input_file = BufferedInputFile(chart_image.getvalue(), filename='candlestick_chart.png')

    # Надсилаємо зображення користувачу
    await message.answer_photo(input_file, caption=f"Графік для {symbol}")


@router.message()
async def message(message: Message):
    words = message.text.split(" ")
    await message.answer(words[-1])

