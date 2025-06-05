from telethon.sync import TelegramClient
from telethon.tl.types import Message
import sqlite3
import asyncio
import re

# === KONFIGURASI ===
api_id = YOUR_API_ID         # Ganti dengan API ID Anda
api_hash = 'YOUR_API_HASH'   # Ganti dengan API Hash Anda
channel_username = 'nama_channel_anda'  # Tanpa @
sqlite_db = 'telegram_filtered.db'

# Kata kunci penting
keywords = ['buy', 'sell', 'tp', 'sl', 'take profit', 'stop loss', 'btc', 'eth', 'bnb']
coins = ['BTC', 'ETH', 'BNB']
message_limit = 1000

# === INISIALISASI DATABASE ===
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    date TEXT,
    sender_id TEXT,
    message TEXT,
    coin TEXT,
    take_profit TEXT,
    stop_loss TEXT
)
''')
conn.commit()

# === LOGIKA FILTER & SIMPAN ===
async def main():
    async with TelegramClient('anon', api_id, api_hash) as client:
        print(f"Mengambil pesan dari @{channel_username} ...")
        channel = await client.get_entity(channel_username)

        matched = 0

        async for message in client.iter_messages(channel, limit=message_limit):
            if isinstance(message, Message) and message.text:
                text = message.text
                text_lower = text.lower()

                if any(kw in text_lower for kw in keywords):
                    take_profit = extract_value(text, ['take profit', 'tp'])
                    stop_loss = extract_value(text, ['stop loss', 'sl'])
                    coin = extract_coin(text, coins)

                    cursor.execute('''
                        INSERT OR IGNORE INTO messages (id, date, sender_id, message, coin, take_profit, stop_loss)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        message.id,
                        message.date.strftime('%Y-%m-%d %H:%M:%S'),
                        str(message.sender_id),
                        text,
                        coin,
                        take_profit,
                        stop_loss
                    ))
                    matched += 1

        conn.commit()
        print(f"Selesai. {matched} pesan cocok disimpan ke {sqlite_db}.")

# === EKSTRAK NILAI TP / SL ===
def extract_value(text, keywords):
    for kw in keywords:
        pattern = re.compile(rf"{kw}[^\d]*(\d+(\.\d+)?)", re.IGNORECASE)
        match = pattern.search(text)
        if match:
            return match.group(1)
    return None

# === EKSTRAK COIN ===
def extract_coin(text, coin_list):
    for coin in coin_list:
        if re.search(rf'\b{coin}\b', text, re.IGNORECASE):
            return coin.upper()
    return None

# === JALANKAN ===
asyncio.run(main())
conn.close()
