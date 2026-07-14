from database import Database

db = Database()

db.nova_venda(

    transaction_id="tx_123",

    nome="Luan",

    email="luan@email.com",

    telefone="5514999999999",

    cpf="12345678900",

    valor=4990,

    status="PENDING",

    referencia="pedido001"

)

print(db.listar())

print(db.total_vendas())

print(db.vendas_pagas())

print(db.receita_total())
