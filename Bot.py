import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

# Links de checkout
CHECKOUT_PACKFOTOS = "https://checkoutseguro.ru/checkout/cmrog32sy0loz01ogz2ci42j4?offer=5Y7M6GF"
CHECKOUT_PACKVIDEOS = "https://checkoutseguro.ru/checkout/cmrok48yp0dpf01pvzttrv2ws?offer=2ZOBQKH"
CHECKOUT_VIP = "https://checkoutseguro.ru/checkout/cmrom633j0nzn01ogc77yyrcg?offer=9P6A7UA"


@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    markup.add(types.InlineKeyboardButton("📸 100 Fotos Pelada - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos Gemendo - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 VIP Vitalício - Acesso para Sempre - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo Hot - R$20,00", callback_data="callvideo"))

    bot.send_message(message.chat.id,
        "😈 <b>Amandinhaa Safadinhaa</b> 🔥\n\n"
        "💦 Tá com tesão e quer se divertir comigo?\n\n"
        "<b>Escolhe seu desejo abaixo safado 😏</b>",
        parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # === PACK 100 FOTOS ===
    if call.data == "packfotos":
        bot.send_message(call.message.chat.id,
            "🔥 <b>PACK 100 FOTOS PELADA</b> 😈\n\n"
            "💦 100 fotos exclusivas, bem safadas e sem censura...\n"
            "Só pra você se deliciar quantas vezes quiser!\n\n"
            "🚀 <b>Quer ver tudo agora?</b>\n\n"
            "🔗 <b>Clique no link e libere seu pack na hora:</b>\n\n"
            f"{CHECKOUT_PACKFOTOS}\n\n"
            "😏 Corre que tá quente demais...",
            disable_web_page_preview=False, parse_mode='HTML')
        return

    # === PACK FOTOS + VÍDEOS ===
    if call.data == "packvideos":
        bot.send_message(call.message.chat.id,
            "💥 <b>PACK COMPLETO - FOTOS + VÍDEOS</b> 😈💦\n\n"
            "📸 Fotos exclusivas + 📹 Vídeos meus gemendo bem gostoso\n\n"
            "🔥 <b>Imagina eu gemendo seu nome só pra você...</b>\n\n"
            "🔗 <b>Clique abaixo e vem se satisfazer agora:</b>\n\n"
            f"{CHECKOUT_PACKVIDEOS}\n\n"
            "😈 Tô molhadinha te esperando...",
            disable_web_page_preview=False, parse_mode='HTML')
        return

    # === GRUPO VIP VITALÍCIO ===
    if call.data == "vip":
        bot.send_message(call.message.chat.id,
            "👑 <b>GRUPO VIP VITALÍCIO</b> 🔥😈\n\n"
            "✅ Acesso para sempre\n"
            "✅ Conteúdos novos toda semana\n"
            "✅ Fotos, vídeos exclusivos e conversas diárias\n\n"
            "💰 Valor: <b>R$ 23,90</b>\n\n"
            "🔥 <b>Quer ter acesso ilimitado a mim?</b>\n\n"
            "🔗 <b>Clique no link e garanta seu VIP vitalício agora:</b>\n\n"
            f"{CHECKOUT_VIP}\n\n"
            "😏 Te espero lá dentro bem safada...",
            disable_web_page_preview=False, parse_mode='HTML')
        return

    # === CHAMADAS DE VÍDEO ===
    if call.data == "callvideo":
        bot.send_message(call.message.chat.id,
            "📹 <b>5 CHAMADAS DE VÍDEO HOT</b> 😈💦\n\n"
            "Você comanda e eu realizo todas as suas fantasias ao vivo...\n\n"
            "🔥 Até você gozar gostoso várias vezes\n\n"
            "🔗 <b>Clique abaixo para pagar e agendar:</b>\n\n"
            "https://checkoutseguro.ru/checkout/cmr9fvt3t0bh601o85363wyez?code=8pow9qx&offer=LZRMXM1\n\n"
            "😏 Tô ansiosa pra te ver...",
            disable_web_page_preview=False, parse_mode='HTML')
        return


print("😈 Amandinhaa Safadinhaa está online...")
bot.infinity_polling()
