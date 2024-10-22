import os
import time
import pyperclip
import webbrowser
from pyautogui import hotkey, press

def format_name_phone(row):
    name, phone = row['NOME'], row['TELEFONE']
    #name = " ".join([item.capitalize() for item in name.split(' ')])
    name = name.split(' ')[0].capitalize()
    phone = "+" + phone
    return name, phone

def _web(receiver: str) -> None:
    """Abre o WhatsApp Web baseado no número de envio"""
    webbrowser.open(
        "https://web.whatsapp.com/send?phone="
        + receiver
    )
    
def close_tab() -> None:
    """Fecha a aba ou janela aberta para envio da mensagem"""

    time.sleep(2)
    hotkey("ctrl", "w")

def copy_image(path: str) -> None:
    """Copia a imagem para a área de transferência. Funciona apenas em Windows"""

    from io import BytesIO
    import win32clipboard  # pip install pywin32
    from PIL import Image

    image = Image.open(path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    
def send_image(path: str, caption: str, receiver: str) -> None:
    """Envia uma mensagem para um contato ou um grupo"""

    # Abre uma janela do WhatsApp web com o contato
    _web(receiver=receiver)
    time.sleep(20)
    
    # Cola a mensagem escolhida
    pyperclip.copy(caption)
    hotkey("ctrl", "v")
    time.sleep(1)
    
    # Cola a imagem escolhida
    copy_image(path=path)
    hotkey("ctrl", "v")
    time.sleep(1)
    
    # Envia a mensagem e imagem
    press("enter")
    time.sleep(1)
    
# Função para carregar o último índice salvo
def get_last_index():
    if os.path.exists(r'./last_index.txt'):
        with open(r'./last_index.txt', 'r') as f:
            return int(f.read().strip())
    return 0

# Função para salvar o índice atual
def save_last_index(index):
    with open(r'./last_index.txt', 'w') as f:
        f.write(str(index))

def send_whatsmessage(df_contacts, message: str, image_path: str):
    """Envia uma imagem com uma mensagem escrita para uma lista de contatos"""
    count = 0
    start_index = get_last_index()  # Pega o último índice salvo
    for i, row in df_contacts.iterrows():
        if count == 1:
            break
        if i <= start_index:
            continue
        name, phone = format_name_phone(row)
        formatted_message = message.format(name)
        send_image(
        path=image_path, 
        caption=formatted_message, 
        receiver=phone,
        )
        close_tab()
        save_last_index(i)
        count += 1
        
'''if __name__ == '__main__':
    # Código para testar as funções (opcional)
    df_contacts = pd.read_csv(...)
    message = "..."
    image = "..."
    send_whatsmessage(df_contacts, message, image)'''