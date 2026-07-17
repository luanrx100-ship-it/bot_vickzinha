import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))
CHAVE_PIX = os.getenv("CHAVE_PIX", "sua_chave_pix_aqui")

# Links de checkout
CHECKOUT_PACKFOTOS = "https://checkoutseguro.ru/checkout/cmrog32sy0loz01ogz2ci42j4?offer=5Y7M6GF"
CHECKOUT_PACKVIDEOS = "https://checkoutseguro.ru/checkout/cmrok48yp0dpf01pvzttrv2ws?offer=2ZOBQKH"
CHECKOUT_VIP = "https://checkoutseguro.ru/checkout/cmrom633j0nzn01ogc77yyrcg?offer=9P6A7UA"


@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("📸 Pack 100 Fotos - R$14,90", callback_data="packfotos"))
    markup.add(types.InlineKeyboardButton("📹 Pack Fotos + Vídeos - R$19,90", callback_data="packvideos"))
    markup.add(types.InlineKeyboardButton("👑 Grupo VIP Vitalício - R$23,90", callback_data="vip"))
    markup.add(types.InlineKeyboardButton("📹 5 Chamadas de Vídeo - R$20,00", callback_data="callvideo"))
    
    bot.send_message(message.chat.id,
        "😈 Amandinhaa Safadinhaa 🔥\n\n"
        "Tá com tesão? Escolhe o que você quer fazer comigo hoje safado 😏",
        parse_mode='HTML', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    
    # === PACK 100 FOTOS ===
    if call.data == "packfotos":
        bot.send_message(call.message.chat.id,
            "🔥 Pack 100 Fotos Pelada 😈\n\n"
            "💦 100 fotos bem safadas, sem censura e só pra você...\n\n"
            "🚀 Quer ver tudinho agora?\n\n"
            "🔗 Clique no link abaixo e libera o pack na hora:\n\n"
            f"{CHECKOUT_PACKFOTOS}\n\n"
            "😏 Corre que tá quente...",
            disable_web_page_preview=False)
        return

    # === PACK FOTOS + VÍDEOS ===
    if call.data == "packvideos":
        bot.send_message(call.message.chat.id,
            "💥 Pack Completo: Fotos + Vídeos Gemendo 😈💦\n\n"
            "📸 + 📹 O pacote mais quente que eu tenho...\n"
            "Fotos exclusivas + vídeos meus gemendo bem gostoso pra você\n\n"
            "🔥 Imagina eu gemendo seu nome enquanto você me assiste...\n\n"
            "🔗 Clique aqui e vem se satisfazer agora:\n\n"
            f"{CHECKOUT_PACKVIDEOS}\n\n"
            "Não perca tempo safado, tô molhadinha te esperando 🔥",
            disable_web_page_preview=False)
        return

    # === GRUPO VIP VITALÍCIO ===
    if call.data == "vip":
        bot.send_message(call.message.chat.id,
            "👑 Grupo VIP Vitalício 🔥😈\n\n"
            "Acesso para sempre + conteúdos novos toda semana\n"
            "Fotos, vídeos exclusivos, conversas diárias e muito mais safadeza...\n\n"
            "💰 Valor: R$ 23,90\n\n"
            "🔥 Quer acesso ilimitado a mim?\n\n"
            "🔗 Clique no link abaixo e garanta seu VIP vitalício agora:\n\n"
            f"{CHECKOUT_VIP}\n\n"
            "😏 Te espero lá dentro safado...",
            disable_web_page_preview=False)
        return

    # === CHAMADAS DE VÍDEO ===
    if call.data == "callvideo":
        bot.send_message(call.message.chat.id,
            "📹 5 Chamadas de Vídeo Hot 😈💦\n\n"
            "Você manda e eu realizo todas as suas fantasias ao vivo...\n\n"
            "🔥 Até você gozar gostoso várias vezes\n\n"
            "🔗 Clique abaixo para pagar e agendar suas chamadas:\n\n"
            "https://checkoutseguro.ru/checkout/cmr9fvt3t0bh601o85363wyez?code=8pow9qx&offer=LZRMXM1\n\n"
            "😏 Tô ansiosa pra te ver...",
            disable_web_page_preview=False)
        return


print("😈 Amandinhaa Safadinhaa está online...")
bot.infinity_polling()
