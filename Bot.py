import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
CHAVE_PIX = os.getenv("CHAVE_PIX", "sua_chave_pix_aqui")

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo - R$20,00", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Amandinhaa Safadinhaa</b> 🔥\n\n"
        "Tá com tesão? Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "callvideo":
        bot.send_message(call.message.chat.id,
            "📹 5 Chamadas de Vídeo ate vc gozar gostoso 😈💦\n\n"
                         
            "Valor: R$ 20,90\n\n"
            "🔗 Clique no link abaixo para pagar e agendar suas chamadas:\n\n"
            "https://checkoutseguro.ru/checkout/cmr9fvt3t0bh601o85363wyez?code=8pow9qx&offer=LZRMXM1",
            disable_web_page_preview=False)
        return

    # Outros produtos (Pix normal)
    produtos = {
        "packfotos": ("Pack 100 Fotos Pelada", 14.90),
        "packvideos": ("Pack Fotos + Vídeos Gemendo", 19.90),
        "vip": ("Grupo VIP Completo", 23.90)
    }
    
    if call.data in produtos:
        nome, valor = produtos[call.data]
        texto = f"""😈 <b>Pedido Recebido!</b>

Produto: <b>{nome}</b>
💰 Valor: R$ {valor:.2f}

Faça o Pix e manda o comprovante aqui que eu libero tudo rapidinho 🔥

Chave Pix: <code>{CHAVE_PIX}</code>"""
        
        bot.send_message(call.message.chat.id, texto, parse_mode='HTML')

print("😈 Amandinhaa Safadinhaa está online...")
bot.infinity_polling()
