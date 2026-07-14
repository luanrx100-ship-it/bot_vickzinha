"""
database.py
Banco de dados SQLite
"""

import sqlite3
from datetime import datetime
from config import DATABASE


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(
            DATABASE,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.criar_tabelas()

    def criar_tabelas(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            transaction_id TEXT UNIQUE,

            nome TEXT,

            email TEXT,

            telefone TEXT,

            cpf TEXT,

            valor INTEGER,

            status TEXT,

            referencia TEXT,

            criado_em TEXT

        )
        """)

        self.conn.commit()

    # ----------------------------------

    def nova_venda(
        self,
        transaction_id,
        nome,
        email,
        telefone,
        cpf,
        valor,
        status,
        referencia
    ):

        self.cursor.execute("""

        INSERT INTO vendas(

        transaction_id,

        nome,

        email,

        telefone,

        cpf,

        valor,

        status,

        referencia,

        criado_em

        )

        VALUES (?,?,?,?,?,?,?,?,?)

        """, (

            transaction_id,

            nome,

            email,

            telefone,

            cpf,

            valor,

            status,

            referencia,

            datetime.now().isoformat()

        ))

        self.conn.commit()

    # ----------------------------------

    def atualizar_status(

        self,

        transaction_id,

        status

    ):

        self.cursor.execute("""

        UPDATE vendas

        SET status=?

        WHERE transaction_id=?

        """,

        (

            status,

            transaction_id

        ))

        self.conn.commit()

    # ----------------------------------

    def buscar(self, transaction_id):

        self.cursor.execute("""

        SELECT *

        FROM vendas

        WHERE transaction_id=?

        """,

        (

            transaction_id,

        ))

        return self.cursor.fetchone()

    # ----------------------------------

    def listar(self):

        self.cursor.execute("""

        SELECT *

        FROM vendas

        ORDER BY id DESC

        """)

        return self.cursor.fetchall()

    # ----------------------------------

    def total_vendas(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM vendas

        """)

        return self.cursor.fetchone()[0]

    # ----------------------------------

    def vendas_pagas(self):

        self.cursor.execute("""

        SELECT COUNT(*)

        FROM vendas

        WHERE status='PAID'

        """)

        return self.cursor.fetchone()[0]

    # ----------------------------------

    def receita_total(self):

        self.cursor.execute("""

        SELECT SUM(valor)

        FROM vendas

        WHERE status='PAID'

        """)

        resultado = self.cursor.fetchone()[0]

        if resultado is None:
            return 0

        return resultado
