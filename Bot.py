import telebot
from telebot import types
import os
import requests
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
BRAVO_KEY = os.getenv("BRAVO_KEY")

def criar_pix_bravo(valor_cents, descricao, user_id):
    url = "https://bravopay.club/api/v1/transactions"
    headers = {
        "Authorization": f"Bearer {BRAVO_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "amount_cents": valor_cents,
        "method": "pix",
        "external_reference": f"vick_{user_id}",
        "customer": {"name": "Cliente"}
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Status: {r.status_code} | Resposta: {r.text[:300]}")
        if r.status_code in (200, 201):
            return r.json()
        return None
    except Exception as e:
        print(f"Erro Bravo Pay: {e}")
        return None

# ================= MENU E COMANDOS =================
@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas Vídeo - R$20,90", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    produtos = {
        "packfotos": ("Pack 100 Fotos Pelada", 1490),
        "packvideos": ("Pack Fotos + Vídeos", 1990),
        "vip": ("Grupo VIP Completo", 2390),
        "callvideo": ("5 Chamadas de Vídeo", 2090)
    }
    
    if call.data in produtos:
        nome, valor = produtos[call.data]
        bot.send_message(call.message.chat.id, f"⏳ Gerando Pix para {nome}...")
        
        result = criar_pix_bravo(valor, nome, call.from_user.id)
        
        if result and result.get("pix", {}).get("copy_paste"):
            pix_code = result["pix"]["copy_paste"]
            bot.send_message(call.message.chat.id, "✅ Pix gerado! Copie o código abaixo:")
            bot.send_message(call.message.chat.id, f"<code>{pix_code}</code>", parse_mode='HTML')
            bot.send_message(call.message.chat.id, "Pague e mande o comprovante aqui que eu libero na hora 🔥")
        else:
            bot.send_message(call.message.chat.id, "❌ Erro ao gerar Pix automático.\nUse Pix manual por enquanto.")

print("😈 Vickzinhaa Safadinha com Bravo Pay está online...")
bot.infinity_polling()
