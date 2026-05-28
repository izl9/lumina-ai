import sqlite3

bd = sqlite3.connect("Lumina.bd", check_same_thread=False)

cursor = bd.cursor()
