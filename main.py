import os
import time
import pyperclip
import webbrowser
from pyautogui import hotkey, press
import logging
from datetime import datetime

"""
Definir configurações básicas do logging
"""
logger = logging.getLogger(__name__)
log_file_name = f"log_{datetime.now().strftime('%d_%m_%Y_%H_%M')}.log"
logging.basicConfig(
    filename=log_file_name, 
    encoding="utf-8", 
    level=logging.INFO, 
    format="[%(asctime)s] %(message)s"
)
logger.info(f"Execução iniciada!")

def format_name_phone(row):
    """Formata o nome e número de telefone para utilização.

    Args:
        row (series): Linha do dataframe de contatos contendo as informações e um contato

    Returns:
        str: Retorna o nome e número de telefone formatados.
    """
    
    try:
        name, phone = row["NOME"], row["TELEFONE"]
        name = name.split(" ")[0].capitalize()
        phone = "+" + phone
        logger.info("Nome e telefone extraídos e formatados com sucesso!")
        return name, phone
    
    except (KeyError, TypeError):
        logger.error("Não foi possível extrair e formatar nome e telefone do contato!")
        return None, None

def _web(receiver: str) -> None:
    """Abre o WhatsApp Web baseado no número de envio

    Args:
        receiver (str): Número de telefone do contato
    """
    webbrowser.open(
        "https://web.whatsapp.com/send?phone="
        + receiver
    )
    
def close_tab() -> None:
    """Fecha a aba ou janela aberta para envio da mensagem
    """
    time.sleep(2)
    hotkey("ctrl", "w")

def copy_image(path: str) -> None:
    """Copia a imagem para a área de transferência. Funciona apenas em Windows.

    Args:
        path (str): Caminho para a imagem
    """

    from io import BytesIO
    import win32clipboard  # pip install pywin32
    from PIL import Image

    try:
        image = Image.open(path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    except (FileNotFoundError, IOError) as e:
        logger.critical("Erro ao abrir a imagem, execução interrompida: {e}")
        exit()

    
def send_message(caption, receiver, image_path=None) -> None:
    """Envia uma mensagem para um contato

    Args:
        image_path (str): Caminho para a imagem a ser enviada
        caption (str): Mensagem a ser enviada
        receiver (str): Número do contato a ser enviada a mensagem
    """
    # Abre uma janela do WhatsApp web com o contato
    _web(receiver=receiver)
    time.sleep(20)
    
    # Cola a mensagem escolhida
    pyperclip.copy(caption)
    hotkey("ctrl", "v")
    time.sleep(1)
    
    # Cola a imagem escolhida
    if image_path:
        copy_image(path=image_path)
        hotkey("ctrl", "v")
        time.sleep(1)
    
    # Envia a mensagem e imagem
    press("enter")
    time.sleep(1)
    

def get_last_index():
    """Carregar o último índice salvo

    Returns:
        int: Índice do último contato para quem foi enviada uma mensagem
    """
    if os.path.exists(r"./last_index.txt"):
        with open(r"./last_index.txt", "r") as f:
            return int(f.read().strip())
    return 0

# Função para 
def save_last_index(index):
    """Salvar o índice atual

    Args:
        index (int): Índice do último contato utilizado
    """
    with open(r"./last_index.txt", "w") as f:
        f.write(str(index))
    logger.info(f"Último índice registrado!")

def send_whatsmessage(df_contacts, message, limit, image_path=None):
    """_summary_

    Args:
        df_contacts (DataFrame): DataFrame dos contatos para quem serão enviadas as mensagens
        message (str): Mensagem a ser enviada
        image_path (str): Caminho da imagem a ser enviada com a mensagem
        limit (int): Número máximo de mensagens a ser enviada
    """    
    count = 0 # Índice para registro do número de mensagens enviadas
    start_index = get_last_index()
    
    for i, row in df_contacts.iterrows():
        # Checar limite de mensagens
        if count == limit:
            break
        
        # Pular os contatos cuja mensagem já foi enviada
        i += 1
        if i <= start_index:
            continue
        
        logger.info(" ")
        logger.info(f"Iniciando execução na linha {start_index + i} da lista de transmissão!")
        
        name, phone = format_name_phone(row)
        
        if not name or not phone:
            save_last_index(i)
            continue
        
        formatted_message = message.format(name)
        send_message(
        caption=formatted_message, 
        receiver=phone,
        image_path=image_path
        )
        
        logger.info(f"Mensagem enviada com sucesso para {name}, número {phone}")
        
        close_tab()
        save_last_index(i)
        count += 1