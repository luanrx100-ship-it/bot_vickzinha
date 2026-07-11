import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo - R$20,90", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    user_id = call.from_user.id

    if data == "packfotos":
        send_pix(call.message, "Pack 100 Fotos Pelada", 14.90)
    elif data == "packvideos":
        send_pix(call.message, "Pack Fotos + Vídeos Gemendo", 19.90)
    elif data == "vip":
        send_pix(call.message, "Grupo VIP Completo", 23.90)
    elif data == "callvideo":
        send_pix(call.message, "5 Chamadas de Vídeo", 20.90)

def send_pix(message, produto: str, valor: float):
    texto = f"""😈 <b>Pedido Recebido!</b>

Produto: <b>{produto}</b>
💰 Valor: R$ {valor:.2f}

Faça o Pix e mande o comprovante aqui que eu libero tudo bem safadinha pra você 🔥"""

    bot.send_message(message.chat.id, texto, parse_mode='HTML')

print("😈 Vickzinhaa Safadinha online...")
bot.infinity_polling()
