import pandas as pd
from main import format_name_phone, _web, close_tab, copy_image, send_image, get_last_index, save_last_index, send_whatsmessage

message = ("""🍫✨ Olá, {}! ✨🍫

Temos uma super novidade para você! 😍 A nossa loja, que antes estava no Shopping Marechal Plaza, agora está de cara nova em um lugar ainda mais especial, esperando por você no endereço: Rua Padre Lustosa, 172 - Centro de São Bernardo do Campo! 🏠

E para comemorar essa mudança, preparamos uma promoção imperdível: apresentando esta imagem na loja, você garante 15% de desconto no nosso delicioso fondue! 😋🍓🍫

Venha nos visitar e aproveitar essa delícia com quem você ama! Estamos ansiosos para receber você e tornar seu momento ainda mais doce! 💛

📍 Novo endereço: Rua Padre Lustosa, 172 - Centro, São Bernardo do Campo
⏰ Horário de funcionamento: Seg a Sáb, das 9h às 19h!

Te esperamos aqui! 🥳""")

image = r".\Panfleto_Fondue.jpeg"

path_contacts_csv = r".\Lovers_Loja_3131.csv"

df_contacts = pd.read_csv(
    path_contacts_csv,
    sep=";",
    encoding='latin1',
    dtype={'TELEFONE': str}
)

send_whatsmessage(df_contacts, message, image)