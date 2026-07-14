import telebot
from telebot import types
import os
from dotenv import load_dotenv
import requests

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
CHAVE_PIX = os.getenv("CHAVE_PIX")

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo - R$20,90", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Vickzinhaa Safadinha</b> 🔥\n\n"
        "Oi safado... pronto pra se divertir comigo? 🔥\n"
        "Escolhe o que você quer:",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "packfotos":
        send_payment(call.message, "Pack 100 Fotos Pelada", 14.90)
    elif call.data == "packvideos":
        send_payment(call.message, "Pack Fotos + Vídeos Gemendo", 19.90)
    elif call.data == "vip":
        send_payment(call.message, "Grupo VIP Completo", 23.90)
    elif call.data == "callvideo":
        send_payment(call.message, "5 Chamadas de Vídeo", 20.90)

def send_payment(message, produto, valor):
    texto = f"""😈 <b>Pedido Recebido!</b>

🛍️ Produto: <b>{produto}</b>
💰 Valor: R$ {valor:.2f}

Assim que eu confirmar o pagamento, te libero o conteúdo na hora 🔥"""

    bot.send_message(message.chat.id, texto, parse_mode='HTML')

print("😈 Vickzinhaa Safadinha está online...")
bot.infinity_polling()
