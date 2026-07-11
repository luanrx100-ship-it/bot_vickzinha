import telebot
from telebot import types
import os
import requests
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

BRAVO_API_KEY = "bp_live_xNIkbn_Z_vsF9miIxndj7zNc8XMxK5BN0QO43A"

def criar_pix_bravo(valor_cents, descricao, user_id):
    url = "https://bravopay.club/api/v1/transactions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BRAVO_API_KEY}"
    }
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"[DEBUG] Status: {response.status_code}")
        print(f"[DEBUG] Resposta: {response.text[:500]}")  # limita pra não poluir
        
        if response.status_code in (200, 201):
            return response.json()
        else:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

# ================= BOT =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack + Vídeos", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 VIP", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Video Calls", callback_data="callvideo"))

    bot.send_message(message.chat.id, "😈 Vickzinhaa Safadinha online... Escolhe seu desejo 🔥", reply_markup=markup)

@bot.message_handler(commands=['packfotos','packvideos','vip','callvideo'])
def compra(message):
    cmd = message.text.replace('/', '')
    valores = {"packfotos": (1490, "Pack 100 Fotos"), "packvideos": (1990, "Pack Fotos + Vídeos"), "vip": (2390, "Grupo VIP"), "callvideo": (2090, "5 Video Calls")}
    
    valor, nome = valores.get(cmd, (1490, "Produto"))
    bot.send_message(message.chat.id, f"⏳ Gerando Pix de R$ {valor/100:.2f}...")
    
    result = criar_pix_bravo(valor, nome, message.from_user.id)
    
    if result and 'pix' in result:
        bot.send_message(message.chat.id, "✅ Pix gerado!\n\n" + result['pix'].get('copy_paste', 'Código não encontrado'))
    else:
        bot.send_message(message.chat.id, "❌ Erro ao gerar Pix.\n\nMe manda o erro que apareceu no terminal.")

print("Bot rodando...")
bot.infinity_polling()
