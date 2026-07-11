import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔥 Pack 100 Fotos", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP Completo", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo", callback_data="call"))

    texto = """😈 <b>Oi safado... bem vindo à Vickzinhaa Safadinha</b> 🔥

Tá com vontade de me ver peladinha? Escolhe o que quer fazer comigo 😏"""

    bot.send_message(message.chat.id, texto, parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "packfotos":
        bot.send_message(call.message.chat.id, "📸 <b>Pack 100 Fotos Pelada</b> — R$ 14,90\n\nDigite: /packfotos")
    elif call.data == "packvideos":
        bot.send_message(call.message.chat.id, "📹 <b>Pack Fotos + Vídeos Gemendo</b> — R$ 19,90\n\nDigite: /packvideos")
    elif call.data == "vip":
        bot.send_message(call.message.chat.id, "👑 <b>Grupo VIP Completo</b> — R$ 23,90\n\nDigite: /vip")
    elif call.data == "call":
        bot.send_message(call.message.chat.id, "📹 <b>5 Chamadas de Vídeo</b> — R$ 20,90\n\nDigite: /callvideo")

# ================= COMANDOS ESPECÍFICOS =================
@bot.message_handler(commands=['packfotos'])
def packfotos(message):
    send_payment_request(message, "Pack 100 Fotos Pelada", 14.90)

@bot.message_handler(commands=['packvideos'])
def packvideos(message):
    send_payment_request(message, "Pack Fotos + Vídeos Gemendo", 19.90)

@bot.message_handler(commands=['vip'])
def vip(message):
    send_payment_request(message, "Grupo VIP Completo", 23.90)

@bot.message_handler(commands=['callvideo'])
def callvideo(message):
    send_payment_request(message, "5 Chamadas de Vídeo", 20.90)

def send_payment_request(message, produto: str, valor: float):
    texto = f"""😈 <b>Você escolheu:</b> {produto}

💰 Valor: R$ {valor:.2f}

Faz o Pix agora que eu libero tudo bem safadinha pra você 🔥

Manda o comprovante aqui depois do pagamento..."""

    bot.send_message(message.chat.id, texto, parse_mode='HTML')

print("😈 Vickzinhaa Safadinha está online...")
bot.infinity_polling()
