from bravopay import BravoPay

api = BravoPay()

resultado = api.criar_pix(
    amount_cents=1990,
    nome="João da Silva",
    email="joao@email.com",
    telefone="5511999999999",
    cpf="12345678900",
    external_reference="pedido_001"
)

print(resultado)
