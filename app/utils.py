import ccxt
import pandas as pd
import mplfinance as mpf
from io import BytesIO
import asyncio

from aiogram.types import BufferedInputFile


async def monitor_candlesticks(symbols, timeframe, message):
    tasks = [check_candle(symbol, timeframe, message) for symbol in symbols]  # Запускаємо всі перевірки паралельно
    await asyncio.gather(*tasks)


async def check_candle(symbol, timeframe, message):
    exchange = ccxt.binance()
    last_checked = None  # Час останньої перевіреної свічки для конкретної валюти

    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=4)  # Отримуємо останню свічку
        latest_candle = ohlcv[-1]

        close_time = pd.to_datetime(latest_candle[0], unit='ms')

        # Перевіряємо, чи нова свічка закрилася
        if last_checked is None or close_time > last_checked:
            last_checked = close_time

            # Викликаємо функцію is_hammer_or_sword для перевірки свічки
            if is_hammer_or_sword(latest_candle) and check_three_candles(ohlcv[:3]):
                # Якщо свічка відповідає умовам, надсилаємо графік
                chart_image = create_chart(symbol, timeframe)
                input_file = BufferedInputFile(chart_image.getvalue(), filename='candlestick_chart.png')

                # Надсилаємо зображення користувачу
                await message.answer_photo(input_file, caption=f"Графік для {symbol}")

        await asyncio.sleep(60)  # Чекаємо 60 секунд перед наступною перевіркою


def is_hammer_or_sword(latest_candle):
    o, h, l, c = latest_candle[1], latest_candle[2], latest_candle[3], latest_candle[4]

    upper_wick = h - max(c, o)
    body = abs(c - o)
    lower_wick = min(c, o) - l

    hammer = (upper_wick < body) & (lower_wick > 2 * body)
    sword = (lower_wick < body) & (upper_wick > 2 * body)
    return hammer | sword


# Функція для перевірки, чи три свічки підряд зелені або червоні
def check_three_candles(candles):
    first_candle, second_candle, third_candle = candles[0], candles[1], candles[2]

    # Визначаємо, чи кожна свічка зелена або червона
    is_green = lambda candle: candle[4] > candle[1]  # Ціна закриття більше ціни відкриття
    is_red = lambda candle: candle[4] < candle[1]    # Ціна закриття менше ціни відкриття

    all_green = is_green(first_candle) and is_green(second_candle) and is_green(third_candle)
    all_red = is_red(first_candle) and is_red(second_candle) and is_red(third_candle)

    return all_green or all_red


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