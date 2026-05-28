from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

load_dotenv()

app.secret_key = os.getenv("APP_SECRET_KEY")

from backend.views import *

if __name__ == "__main__":
    print("DB PATH:", os.path.abspath("Lumina.bd"))
    app.run()
