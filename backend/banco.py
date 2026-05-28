import sqlite3

bd = sqlite3.connect("Lumina.bd", check_same_thread=False)

cursor = bd.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    pergunta TEXT,
    resposta TEXT
)
""")

bd.commit()
