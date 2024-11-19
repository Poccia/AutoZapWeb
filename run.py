import pandas as pd
from main import format_name_phone, _web, close_tab, copy_image, send_message, get_last_index, save_last_index, send_whatsmessage

message = ("""🍫✨ Olá, {}! ✨🍫

Esta é uma mensagem teste.""")

#image = r".\Panfleto_Fondue.jpeg"

path_contacts_csv = r".\lista_teste.csv"

limit = 2000

df_contacts = pd.read_csv(
    path_contacts_csv,
    sep=",",
    encoding="utf-8",
    dtype={"TELEFONE": str}
)

send_whatsmessage(df_contacts, message, limit)