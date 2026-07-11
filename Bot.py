import telebot
from telebot import types
import os
import requests
import sqlite3
import logging
import hashlib
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
import json

# ================= CONFIGURAÇÕES =================
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("PAYMENT_API_KEY")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
CONTENT_CHANNEL = os.getenv("CONTENT_CHANNEL")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT")

if not all([BOT_TOKEN, API_KEY, ADMIN_IDS]):
    logger.error("Variáveis de ambiente obrigatórias não configuradas!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# ================= BANCO DE DADOS =================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('content_bot.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        # Tabela de usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                age_verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP
            )
        ''')
        
        # Tabela de produtos/conteúdo
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                content_type TEXT,
                file_path TEXT,
                download_link TEXT,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de compras
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                amount REAL,
                payment_status TEXT DEFAULT 'pending',
                payment_id TEXT,
                delivered INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                delivered_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Tabela de códigos de acesso
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                code TEXT UNIQUE,
                expires_at TIMESTAMP,
                used INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id: int, username: str, first_name: str):
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name, last_active) VALUES (?, ?, ?, ?)",
                (user_id, username, first_name, datetime.now())
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Erro ao adicionar usuário: {e}")
    
    def verify_age(self, user_id: int):
        try:
            self.cursor.execute(
                "UPDATE users SET age_verified = 1, last_active = ? WHERE user_id = ?",
                (datetime.now(), user_id)
            )
            self.conn.commit()
        except Exception as e:
            logger.error(f"Erro ao verificar idade: {e}")
    
    def is_age_verified(self, user_id: int) -> bool:
        try:
            self.cursor.execute(
                "SELECT age_verified FROM users WHERE user_id = ?",
                (user_id,)
            )
            result = self.cursor.fetchone()
            return result and result[0] == 1
        except Exception as e:
            logger.error(f"Erro ao verificar idade: {e}")
            return False
    
    def get_products(self, active_only: bool = True) -> List[Dict]:
        try:
            query = "SELECT id, name, description, price, content_type FROM products"
            if active_only:
                query += " WHERE active = 1"
            self.cursor.execute(query)
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "content_type": row[4]
                }
                for row in self.cursor.fetchall()
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar produtos: {e}")
            return []
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        try:
            self.cursor.execute(
                "SELECT id, name, description, price, content_type, file_path, download_link FROM products WHERE id = ?",
                (product_id,)
            )
            row = self.cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "content_type": row[4],
                    "file_path": row[5],
                    "download_link": row[6]
                }
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar produto: {e}")
            return None
    
    def create_purchase(self, user_id: int, product_id: int, amount: float, payment_id: str) -> Optional[int]:
        try:
            self.cursor.execute(
                "INSERT INTO purchases (user_id, product_id, amount, payment_id) VALUES (?, ?, ?, ?)",
                (user_id, product_id, amount, payment_id)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"Erro ao criar compra: {e}")
            return None
    
    def confirm_purchase(self, purchase_id: int) -> bool:
        try:
            self.cursor.execute(
                "UPDATE purchases SET payment_status = 'paid', delivered_at = ? WHERE id = ?",
                (datetime.now(), purchase_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao confirmar compra: {e}")
            return False
    
    def get_pending_purchase(self, user_id: int) -> Optional[Dict]:
        try:
            self.cursor.execute(
                """SELECT p.id, p.product_id, p.amount, p.payment_id, pr.name, pr.price 
                   FROM purchases p 
                   JOIN products pr ON p.product_id = pr.id 
                   WHERE p.user_id = ? AND p.payment_status = 'pending' 
                   ORDER BY p.created_at DESC LIMIT 1""",
                (user_id,)
            )
            row = self.cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "product_id": row[1],
                    "amount": row[2],
                    "payment_id": row[3],
                    "product_name": row[4],
                    "price": row[5]
                }
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar compra pendente: {e}")
            return None
    
    def has_purchased(self, user_id: int, product_id: int) -> bool:
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM purchases WHERE user_id = ? AND product_id = ? AND payment_status = 'paid'",
                (user_id, product_id)
            )
            return self.cursor.fetchone()[0] > 0
        except Exception as e:
            logger.error(f"Erro ao verificar compra: {e}")
            return False
    
    def generate_access_code(self, user_id: int, product_id: int, hours_valid: int = 24) -> str:
        try:
            code = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=hours_valid)
            self.cursor.execute(
                "INSERT INTO access_codes (user_id, product_id, code, expires_at) VALUES (?, ?, ?, ?)",
                (user_id, product_id, code, expires_at)
            )
            self.conn.commit()
            return code
        except Exception as e:
            logger.error(f"Erro ao gerar código de acesso: {e}")
            return ""
    
    def validate_access_code(self, code: str) -> Optional[Dict]:
        try:
            self.cursor.execute(
                """SELECT user_id, product_id, expires_at, used 
                   FROM access_codes 
                   WHERE code = ? AND used = 0 AND expires_at > ?""",
                (code, datetime.now())
            )
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute(
                    "UPDATE access_codes SET used = 1 WHERE code = ?",
                    (code,)
                )
                self.conn.commit()
                return {
                    "user_id": row[0],
                    "product_id": row[1],
                    "expires_at": row[2]
                }
            return None
        except Exception as e:
            logger.error(f"Erro ao validar código: {e}")
            return None
    
    def get_user_purchases(self, user_id: int) -> List[Dict]:
        try:
            self.cursor.execute(
                """SELECT p.id, pr.name, p.amount, p.delivered_at 
                   FROM purchases p 
                   JOIN products pr ON p.product_id = pr.id 
                   WHERE p.user_id = ? AND p.payment_status = 'paid'
                   ORDER BY p.created_at DESC""",
                (user_id,)
            )
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "amount": row[2],
                    "delivered_at": row[3]
                }
                for row in self.cursor.fetchall()
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar compras do usuário: {e}")
            return []

db = Database()

# ================= SISTEMA DE PAGAMENTO =================
class PaymentSystem:
    @staticmethod
    def create_payment(amount: float, description: str, user_id: int) -> Optional[Dict]:
        """
        Integração com gateway de pagamento
        Substitua pela API do seu gateway (Mercado Pago, PagSeguro, Stripe, etc)
        """
        try:
            # Exemplo com Mercado Pago (adaptar para seu gateway)
            url = "https://api.mercadopago.com/checkout/preferences"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            preference = {
                "items": [{
                    "title": description,
                    "quantity": 1,
                    "unit_price": amount
                }],
                "back_urls": {
                    "success": f"https://t.me/{bot.get_me().username}?start=success",
                    "failure": f"https://t.me/{bot.get_me().username}?start=failure",
                    "pending": f"https://t.me/{bot.get_me().username}?start=pending"
                },
                "auto_return": "approved",
                "external_reference": f"user_{user_id}_{int(datetime.now().timestamp())}"
            }
            
            response = requests.post(url, headers=headers, json=preference, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "payment_id": data.get("id"),
                "payment_link": data.get("init_point"),
                "qr_code": data.get("qr_code")
            }
        except Exception as e:
            logger.error(f"Erro ao criar pagamento: {e}")
            return None
    
    @staticmethod
    def verify_payment(payment_id: str) -> bool:
        """Verifica se o pagamento foi aprovado"""
        # Implementar verificação real com seu gateway
        # Por enquanto, retorna False (admin confirma manualmente)
        return False

# ================= FUNÇÕES AUXILIARES =================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def format_currency(value: float) -> str:
    return f"R$ {value:.2f}".replace(".", ",")

def send_content_to_user(user_id: int, product: Dict):
    """Envia o conteúdo para o usuário após pagamento confirmado"""
    try:
        # Gera código de acesso único
        access_code = db.generate_access_code(user_id, product["id"])
        
        if product.get("download_link"):
            # Envia link de download
            message = f"""✅ <b>Pagamento Confirmado!</b>

📦 Produto: {product['name']}
🔗 Link de acesso: {product['download_link']}

🔐 Código de acesso: <code>{access_code}</code>
⏰ Válido por 24 horas

⚠️ Não compartilhe este link ou código!"""
            bot.send_message(user_id, message, parse_mode='HTML')
        
        elif product.get("file_path") and os.path.exists(product["file_path"]):
            # Envia arquivo diretamente
            bot.send_message(user_id, f"✅ Pagamento confirmado! Enviando seu conteúdo...")
            
            with open(product["file_path"], 'rb') as file:
                if product["content_type"] == "photo":
                    bot.send_photo(user_id, file, caption=f"📸 {product['name']}")
                elif product["content_type"] == "video":
                    bot.send_video(user_id, file, caption=f"🎥 {product['name']}")
                else:
                    bot.send_document(user_id, file, caption=f"📦 {product['name']}")
            
            # Envia código de acesso adicional
            bot.send_message(
                user_id,
                f"🔐 Código de acesso: <code>{access_code}</code>\n⏰ Válido por 24 horas",
                parse_mode='HTML'
            )
        
        else:
            # Conteúdo indisponível
            bot.send_message(
                user_id,
                "❌ Desculpe, ocorreu um erro ao entregar seu conteúdo. Entre em contato com o suporte."
            )
            logger.error(f"Conteúdo não encontrado para produto {product['id']}")
    
    except Exception as e:
        logger.error(f"Erro ao enviar conteúdo: {e}")
        bot.send_message(user_id, "❌ Erro ao entregar conteúdo. Entre em contato com o suporte.")

# ================= HANDLERS =================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username, message.from_user.first_name)
    
    # Verifica se vem de um pagamento
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if args and args[0] in ['success', 'failure', 'pending']:
        status = args[0]
        if status == 'success':
            bot.send_message(user_id, "✅ Pagamento recebido! Processando...")
            # Aqui você pode adicionar lógica para verificar pagamento automaticamente
        elif status == 'failure':
            bot.send_message(user_id, "❌ Pagamento falhou. Tente novamente.")
        elif status == 'pending':
            bot.send_message(user_id, "⏳ Pagamento em análise. Você será notificado quando for aprovado.")
        return
    
    # Verifica verificação de idade
    if not db.is_age_verified(user_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Tenho 18+ anos", callback_data="age_verify"))
        markup.add(types.InlineKeyboardButton("❌ Sou menor de idade", callback_data="age_deny"))
        
        bot.send_message(
            user_id,
            "⚠️ <b>AVISO IMPORTANTE</b>\n\n"
            "Este bot contém conteúdo adulto (+18).\n"
            "Ao continuar, você declara ter 18 anos ou mais.\n\n"
            "Confirme sua idade para continuar:",
            parse_mode='HTML',
            reply_markup=markup
        )
        return
    
    # Menu principal
    show_menu(user_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('age_'))
def age_verification(call):
    user_id = call.from_user.id
    
    if call.data == "age_verify":
        db.verify_age(user_id)
        bot.answer_callback_query(call.id, "✅ Idade verificada!")
        show_menu(user_id)
    elif call.data == "age_deny":
        bot.answer_callback_query(call.id, "❌ Acesso negado!")
        bot.send_message(
            user_id,
            "Você deve ter 18 anos ou mais para acessar este conteúdo."
        )

def show_menu(user_id: int):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔥 Ver Conteúdo", callback_data="view_content"),
        types.InlineKeyboardButton("📦 Minhas Compras", callback_data="my_purchases"),
        types.InlineKeyboardButton("💬 Suporte", callback_data="support")
    )
    
    bot.send_message(
        user_id,
        "😈 <b>Bem-vindo ao Conteúdo Exclusivo</b> 🔥\n\n"
        "Escolha uma opção:",
        parse_mode='HTML',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if not db.is_age_verified(user_id):
        bot.answer_callback_query(call.id, "⚠️ Verifique sua idade primeiro!")
        return
    
    if call.data == "view_content":
        show_products(user_id)
    elif call.data == "my_purchases":
        show_my_purchases(user_id)
    elif call.data == "support":
        bot.send_message(
            user_id,
            f"💬 Para suporte, entre em contato:\n\n@{SUPPORT_CHAT.replace('@', '')}"
        )
    elif call.data.startswith("buy_"):
        product_id = int(call.data.split("_")[1])
        initiate_purchase(user_id, product_id)

def show_products(user_id: int):
    products = db.get_products()
    
    if not products:
        bot.send_message(user_id, "❌ Nenhum conteúdo disponível no momento.")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for product in products:
        markup.add(
            types.InlineKeyboardButton(
                f"{product['name']} - {format_currency(product['price'])}",
                callback_data=f"buy_{product['id']}"
            )
        )
    
    bot.send_message(
        user_id,
        "🔥 <b>CONTEÚDO DISPONÍVEL</b>\n\nSelecione o que deseja comprar:",
        parse_mode='HTML',
        reply_markup=markup
    )

def initiate_purchase(user_id: int, product_id: int):
    # Verifica se já comprou
    if db.has_purchased(user_id, product_id):
        bot.send_message(
            user_id,
            "✅ Você já possui este conteúdo! Verifique em 'Minhas Compras'."
        )
        return
    
    product = db.get_product(product_id)
    if not product:
        bot.send_message(user_id, "❌ Produto não encontrado.")
        return
    
    # Verifica se tem compra pendente
    pending = db.get_pending_purchase(user_id)
    if pending:
        bot.send_message(
            user_id,
            f"⚠️ Você já tem uma compra pendente:\n\n"
            f"Produto: {pending['product_name']}\n"
            f"Valor: {format_currency(pending['amount'])}\n\n"
            f"Aguarde a confirmação ou entre em contato com o suporte."
        )
        return
    
    # Cria pagamento
    payment = PaymentSystem.create_payment(product['price'], product['name'], user_id)
    
    if payment and payment.get('payment_link'):
        purchase_id = db.create_purchase(user_id, product_id, product['price'], payment['payment_id'])
        
        if purchase_id:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("💳 Pagar Agora", url=payment['payment_link']))
            
            bot.send_message(
                user_id,
                f"🛒 <b>Finalizar Compra</b>\n\n"
                f"Produto: {product['name']}\n"
                f"Valor: {format_currency(product['price'])}\n\n"
                f"Clique no botão abaixo para pagar:",
                parse_mode='HTML',
                reply_markup=markup
            )
        else:
            bot.send_message(user_id, "❌ Erro ao processar compra. Tente novamente.")
    else:
        bot.send_message(user_id, "❌ Erro ao gerar pagamento. Tente novamente.")

def show_my_purchases(user_id: int):
    purchases = db.get_user_purchases(user_id)
    
    if not purchases:
        bot.send_message(user_id, "📦 Você ainda não possui compras.")
        return
    
    texto = "📦 <b>SUAS COMPRAS</b>\n\n"
    for purchase in purchases:
        texto += f"✅ {purchase['name']} - {format_currency(purchase['amount'])}\n"
    
    texto += "\n💡 Para acessar novamente, entre em contato com o suporte."
    bot.send_message(user_id, texto, parse_mode='HTML')

@bot.message_handler(commands=['compras'])
def my_purchases_cmd(message):
    if not db.is_age_verified(message.from_user.id):
        return bot.send_message(message.chat.id, "⚠️ Verifique sua idade primeiro com /start")
    show_my_purchases(message.from_user.id)

# ================= COMANDOS ADMIN =================
@bot.message_handler(commands=['add_product'])
def add_product(message):
    if not is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ Acesso negado!")
    
    bot.send_message(
        message.chat.id,
        "📝 <b>Adicionar Produto</b>\n\n"
        "Envie os dados no formato:\n"
        "<code>nome | preço | tipo | link_arquivo</code>\n\n"
        "Exemplo:\n"
        "<code>Pack Fotos | 19.90 | photo | https://exemplo.com/pack.zip</code>\n\n"
        "Tipos: photo, video, document",
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda m: is_admin(m.from_user.id) and '|' in m.text)
def process_new_product(message):
    try:
        parts = [p.strip() for p in message.text.split('|')]
        
        if len(parts) != 4:
            return bot.send_message(message.chat.id, "❌ Formato inválido!")
        
        name, price, content_type, file_info = parts
        price = float(price)
        
        # Determina se é link ou arquivo local
        if file_info.startswith('http'):
            download_link = file_info
            file_path = None
        else:
            file_path = file_info
            download_link = None
        
        db.cursor.execute(
            """INSERT INTO products (name, description, price, content_type, file_path, download_link) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (name, name, price, content_type, file_path, download_link)
        )
        db.conn.commit()
        
        bot.send_message(message.chat.id, f"✅ Produto '{name}' adicionado com sucesso!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro ao adicionar produto: {e}")

@bot.message_handler(commands=['list_products'])
def list_products(message):
    if not is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ Acesso negado!")
    
    products = db.get_products(active_only=False)
    
    if not products:
        return bot.send_message(message.chat.id, "📦 Nenhum produto cadastrado.")
    
    texto = "📦 <b>PRODUTOS CADASTRADOS</b>\n\n"
    for product in products:
        texto += f"ID {product['id']}: {product['name']} - {format_currency(product['price'])}\n"
    
    bot.send_message(message.chat.id, texto, parse_mode='HTML')

@bot.message_handler(commands=['stats'])
def stats(message):
    if not is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ Acesso negado!")
    
    db.cursor.execute("SELECT COUNT(*) FROM users WHERE age_verified = 1")
    total_users = db.cursor.fetchone()[0]
    
    db.cursor.execute("SELECT COUNT(*) FROM purchases WHERE payment_status = 'paid'")
    total_sales = db.cursor.fetchone()[0]
    
    db.cursor.execute("SELECT SUM(amount) FROM purchases WHERE payment_status = 'paid'")
    total_revenue = db.cursor.fetchone()[0] or 0
    
    db.cursor.execute("SELECT COUNT(*) FROM purchases WHERE payment_status = 'pending'")
    pending = db.cursor.fetchone()[0]
    
    texto = f"""📊 <b>ESTATÍSTICAS</b>

👥 Usuários verificados: {total_users}
💰 Vendas realizadas: {total_sales}
💵 Faturamento total: {format_currency(total_revenue)}
⏳ Pedidos pendentes: {pending}"""
    
    bot.send_message(message.chat.id, texto, parse_mode='HTML')

@bot.message_handler(commands=['approve'])
def approve_purchase(message):
    if not is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "❌ Acesso negado!")
    
    try:
        purchase_id = int(message.text.split()[1])
        
        db.cursor.execute(
            "SELECT user_id, product_id, amount FROM purchases WHERE id = ?",
            (purchase_id,)
        )
        row = db.cursor.fetchone()
        
        if not row:
            return bot.send_message(message.chat.id, "❌ Compra não encontrada!")
        
        user_id, product_id, amount = row
        
        if db.confirm_purchase(purchase_id):
            product = db.get_product(product_id)
            send_content_to_user(user_id, product)
            
            bot.send_message(message.chat.id, f"✅ Compra {purchase_id} aprovada e conteúdo entregue!")
            bot.send_message(user_id, "✅ Seu pagamento foi confirmado! Acessando seu conteúdo...")
        else:
            bot.send_message(message.chat.id, "❌ Erro ao aprovar compra!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro: {e}")

# ================= INICIALIZAÇÃO =================
if __name__ == "__main__":
    logger.info("🔥 Bot de Conteúdo Adulto iniciando...")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
