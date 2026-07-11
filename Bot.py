import telebot
from telebot import types
import os
import requests
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

BRAVO_KEY = "bp_live_xNIkbn_Z_vsF9miIxndj7zNc8XMxK5BN0QO43A"

def gerar_pix(valor, descricao, user_id):
    url = "https://bravopay.club/api/v1/transactions"
    headers = {
        "Authorization": f"Bearer {BRAVO_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "amount_cents": valor,
        "method": "pix",
        "external_reference": f"vick_{user_id}"
    }
    
    try:
        r = requests.post(url, headers=headers, json=data)
        print("Status:", r.status_code)
        print("Resposta:", r.text)
        return r.json() if r.ok else None
    except Exception as e:
        print("Erro:", e)
        return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Use /packfotos para testar")

@bot.message_handler(commands=['packfotos'])
def packfotos(message):
    bot.send_message(message.chat.id, "Gerando Pix...")
    result = gerar_pix(1490, "Pack 100 Fotos", message.from_user.id)
    
    if result and 'pix' in result:
        bot.send_message(message.chat.id, f"✅ Pix:\n\n{result['pix'].get('copy_paste', 'Sem código')}")
    else:
        bot.send_message(message.chat.id, "❌ Falhou. Me manda o que apareceu no terminal.")

print("Bot rodando...")
bot.infinity_polling()
