# imports do celery vem primeiro
from __future__ import absolute_import, unicode_literals
from celery import shared_task

#imports do email
from email.message import EmailMessage
import smtplib
import ssl
import os
import time
import mimetypes
from dotenv import load_dotenv


@shared_task
def add(x=5, y=5):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)



@shared_task
def my_send_email():
    # Carregar variáveis de ambiente
    load_dotenv()

    password = os.getenv('SENHA_EMAIL')
    from_email = 'silviocoelho.udc@gmail.com'

    # Lista de destinatários
    to_emails = [
        'conejofoz@gmail.com',
        'silviocoelho.udc@gmail.com',
        'katiaespinola_xx_@gmai.com',
    ]

    subject = 'Proposta de parceria'
    # body = open('./corpo.txt', 'r', encoding='utf-8').read()

    # Caminho absoluto para o arquivo corpo.txt
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do arquivo atual
    file_path = os.path.join(base_dir, 'corpo.txt')  # Caminho completo para corpo.txt

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            body = file.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return False

    safe = ssl.create_default_context()

    # Capiturando o tempo de envio
    start_time = time.time()

    # Enviando e-mails individualmente
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as server:
        server.login(from_email, password)

        for email in to_emails:
            # Criar um novo email para cada destinatário
            message = EmailMessage()
            message['From'] = from_email
            message['To'] = email  # Agora definimos corretamente
            message['Subject'] = subject
            message.set_content(body)

            # Enviar email
            server.sendmail(from_email, email, message.as_string())
            print(f"E-mail enviado para: {email}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tempo de envio: {elapsed_time:.2f} segundos")        

    print("Todos os e-mails foram enviados com sucesso!")

    return True


@shared_task
def send_email_simples():
    print('Enviando email simples...')
    password = os.getenv('SENHA_EMAIL')
    from_email = 'silviocoelho.udc@gmail.com'
    to_email = 'silviocoelho.udc@gmail.com'
    subject = 'Proposta de parceria'
    # body = open('./corpo.txt', 'r', encoding='utf-8').read()
    # Caminho absoluto para o arquivo corpo.txt
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do arquivo atual
    file_path = os.path.join(base_dir, 'corpo.txt')  # Caminho completo para corpo.txt

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            body = file.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {file_path}")
        return False

    # Montando a estrutura do email
    message = EmailMessage()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.set_content(body)
    safe = ssl.create_default_context()

    # Enviando o email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as server:
        
        server.login(from_email, password)
        
        server.sendmail(
            from_email,
            to_email,
            message.as_string()
        )

    return True


@shared_task
def send_email_with_attachment():
    # Configurações de e-mail
    password = os.getenv('SENHA_EMAIL')
    from_email = 'silviocoelho.udc@gmail.com'

    # Lista de destinatários
    to_emails = [
        'conejofoz@gmail.com',
        'silviocoelho.udc@gmail.com',
        'katiaespinola_xx_@gmail.com',
    ]

    subject = 'Proposta de parceria customizada'

    # Caminhos absolutos para os arquivos
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do arquivo atual
    body_file_path = os.path.join(base_dir, 'index.html.txt')  # Caminho para o corpo do e-mail
    attachment_file_path = os.path.join(base_dir, 'corpo.txt')  # Caminho para o anexo

    # Verifica se os arquivos existem
    if not os.path.exists(body_file_path):
        print(f"Arquivo do corpo não encontrado: {body_file_path}")
        return False

    if not os.path.exists(attachment_file_path):
        print(f"Arquivo de anexo não encontrado: {attachment_file_path}")
        return False

    # Lê o conteúdo do corpo do e-mail
    try:
        with open(body_file_path, 'r', encoding='utf-8') as file:
            body = file.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo do corpo: {e}")
        return False

    # Configurações de segurança
    safe = ssl.create_default_context()

    # Captura o tempo de início do envio
    start_time = time.time()

    # Envia e-mails individualmente
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as server:
            server.login(from_email, password)

            for email in to_emails:
                # Cria uma nova mensagem para cada destinatário
                message = EmailMessage()
                message['From'] = from_email
                message['To'] = email
                message['Subject'] = subject
                message.add_alternative(body, subtype='html')  # Define o corpo como HTML

                # Adiciona o anexo
                mime_type, mime_subtype = mimetypes.guess_type(attachment_file_path)[0].split('/')
                with open(attachment_file_path, 'rb') as arquivo:
                    message.add_attachment(
                        arquivo.read(),
                        maintype=mime_type,
                        subtype=mime_subtype,
                        filename=os.path.basename(attachment_file_path)
                )

                # Envia o e-mail
                server.sendmail(from_email, email, message.as_string())
                print(f"E-mail enviado para: {email}")

    except Exception as e:
        print(f"Erro ao enviar e-mails: {e}")
        return False

    # Captura o tempo de término e calcula o tempo total
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Tempo de envio: {elapsed_time:.2f} segundos")
    print("Todos os e-mails foram enviados com sucesso!")

    return True