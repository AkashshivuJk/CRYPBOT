import sys
import os
import requests
from flask import Flask, render_template, request
from main import questions_and_answers

# Add root path for importing main.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set absolute paths for templates and static folders (important for Vercel)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, "templates")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/index')
def indexx():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']

    if "price of" in user_input.lower():
        crypto_name = user_input.lower().replace("price of", "").strip()
        answer = get_crypto_price(crypto_name)
    else:
        answer = get_answer(user_input)

    return render_template('index.html', user_input=user_input, answer=answer)

def get_answer(user_input):
    for qa in questions_and_answers:
        if user_input.lower() in qa["question"].lower():
            answer = qa["answer"]
            return answer() if callable(answer) else answer
    return "Sorry, I don't have an answer to that question."

def get_crypto_price(crypto_name):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name.lower()}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()

        if crypto_name.lower() in data:
            price = data[crypto_name.lower()]["usd"]
            return f"The current price of {crypto_name.capitalize()} is ${price:.2f} USD."
        else:
            return f"Sorry, I couldn't find the price for {crypto_name}. Please check the name and try again."
    except Exception:
        return "I'm having trouble fetching the price right now. Please try again later."

# Vercel handler
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)
