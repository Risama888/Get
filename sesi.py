from telethon.sync import TelegramClient

# Ganti dengan API Anda
api_id = YOUR_API_ID        # Misal: 123456
api_hash = 'YOUR_API_HASH'  # Misal: '0123456789abcdef...'

# Nama file sesi (boleh disesuaikan, default: 'anon')
session_name = 'anon'

with TelegramClient(session_name, api_id, api_hash) as client:
    print("Sesi berhasil dibuat dan login berhasil!")
