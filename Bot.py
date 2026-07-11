import telebot
from telebot import types
import os
import requests
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
BRAVO_KEY = os.getenv("BRAVO_KEY")

def criar_pix_bravo(valor_cents: int, descricao: str, user_id: int):
    url = "https://bravopay.club/api/v1/transactions"
    headers = {
        "Authorization": f"Bearer {BRAVO_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}_{int(os.times() [0])}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")
        return response.json() if response.ok else None
    except Exception as e:
        print(f"Erro: {e}")
        return None

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack + Vídeos", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Calls Vídeo", callback_data="callvideo"))

    bot.send_message(message.chat.id, "😈 Vickzinhaa Safadinha online... Escolhe seu desejo 🔥", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    cmds = {
        "packfotos": ("Pack 100 Fotos Pelada", 1490),
        "packvideos": ("Pack Fotos + Vídeos", 1990),
        "vip": ("Grupo VIP Completo", 2390),
        "callvideo": ("5 Chamadas de Vídeo", 2090)
    }
    if call.data in cmds:
        nome, valor = cmds[call.data]
        bot.send_message(call.message.chat.id, f"Gerando Pix para {nome}...")
        result = criar_pix_bravo(valor, nome, call.from_user.id)
        if result and result.get('pix'):
            bot.send_message(call.message.chat.id, f"✅ Pix gerado!\n\n{result['pix'].get('copy_paste', 'Sem código')}")
        else:
            bot.send_message(call.message.chat.id, "❌ Erro na Bravo Pay. Veja o terminal.")

print("Bot com Bravo Pay rodando...")
bot.infinity_polling()
