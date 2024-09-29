import ccxt
import pandas as pd
import mplfinance as mpf
from io import BytesIO
import asyncio

from aiogram.types import BufferedInputFile

def create_chart(symbol, timeframe):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=15)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    image_stream = BytesIO()
    mpf.plot(df, type='candle', title=f'{symbol} Candlestick Chart', savefig=image_stream)

    image_stream.seek(0)

    return image_stream

async def check_candle(symbol, timeframe, message):
    exchange = ccxt.binance()
    last_checked = None  # Час останньої перевіреної свічки для конкретної валюти

    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=1)  # Отримуємо останню свічку
        latest_candle = ohlcv[-1]

        close_time = pd.to_datetime(latest_candle[0], unit='ms')

        # Перевіряємо, чи нова свічка закрилася
        if last_checked is None or close_time > last_checked:
            last_checked = close_time

            # Викликаємо функцію is_hammer_or_sword для перевірки свічки
            if is_hammer_or_sword(latest_candle[1], latest_candle[2], latest_candle[3], latest_candle[4]):
                # Якщо свічка відповідає умовам, надсилаємо графік
                chart_image = create_chart(symbol, timeframe)
                input_file = BufferedInputFile(chart_image.getvalue(), filename='candlestick_chart.png')

                # Надсилаємо зображення користувачу
                await message.answer_photo(input_file, caption=f"Графік для {symbol}")

        await asyncio.sleep(60)  # Чекаємо 60 секунд перед наступною перевіркою

async def monitor_candlesticks(symbols, timeframe, message):
    tasks = [check_candle(symbol, timeframe, message) for symbol in symbols]
    await asyncio.gather(*tasks)  # Запускаємо всі перевірки паралельно


def is_hammer_or_sword(o, h, l, c):
    upper_wick = h - max(c, o)
    body = abs(c - o)
    lower_wick = min(c, o) - l

    hammer = (upper_wick < body) & (lower_wick > 2 * body)
    sword = (lower_wick < body) & (upper_wick > 2 * body)
    return hammer | sword