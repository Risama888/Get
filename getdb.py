import sqlite3

# Nama database
sqlite_db = 'telegram_filtered.db'

# Koneksi & cursor
conn = sqlite3.connect(sqlite_db)
cursor = conn.cursor()

# Membuat tabel
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
conn.close()

print(f"Database '{sqlite_db}' berhasil dibuat dengan tabel 'messages'.")
