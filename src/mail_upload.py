import imaplib
import email
import time
import codecs
import base64

def main():
    imap_host = 'email-ssl.com.br'
    imap_port = 993

    # Fazer upload no email abaixo
    username = 'email1@exemplo.com.br'
    password = 'SenhaDoEmail123'
    
    # Backup que vai subir pro email
    mbox_file_path = r'BackupsEmail\bkp_email1.mbox'

    # Conectar ao servidor IMAP
    mail = imaplib.IMAP4_SSL(imap_host, imap_port)
    mail.login(username, password)

    # Ler o arquivo .mbox
    with codecs.open(mbox_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        mbox_content = f.read()

    # Dividir o conteúdo em e-mails individuais
    messages = mbox_content.split('From ')

    # Conjunto para armazenar o conteúdo dos e-mails já processados
    processed_emails = set()

    # Contador de e-mails enviados com sucesso
    success_count = 0

    # Total de e-mails a serem enviados
    total_emails = len(messages) - 1  # Exclui o cabeçalho

    # Para cada e-mail, analisar e enviar para o servidor IMAP
    for idx, msg in enumerate(messages):
        try:
            # Ignorar linhas em branco ou inválidas
            if not msg.strip():
                continue

            # Analisar o e-mail
            parsed_email = email.message_from_string('From ' + msg)

            # Obter a representação em string do e-mail
            email_string = parsed_email.as_string()

            # Verificar se o conteúdo do e-mail já foi processado antes
            if email_string in processed_emails:
                continue

            # Adicionar o conteúdo do e-mail ao conjunto de e-mails processados
            processed_emails.add(email_string)

            # Determinar a pasta destino com base na pasta atual do e-mail
            folder = parsed_email.get('X-Source', 'INBOX')  # Pasta padrão é a caixa de entrada (inbox)
            
            if folder:
                # Verificar se a pasta destino existe; se não, criar a pasta
                folders = mail.list()[1]
                if folder not in [folder_info.decode('utf-8').split(' "." ')[1] for folder_info in folders]:
                    mail.create(folder)
                    print(f"Pasta '{folder}' criada com sucesso")

                # Selecionar a pasta destino no servidor IMAP
                mail.select(folder)

                # Decodificar e anexar os anexos codificados em base64
                for part in parsed_email.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Transfer-Encoding') == 'base64':
                        attachment_content_base64 = part.get_payload()
                        attachment_content = base64.b64decode(attachment_content_base64)
                        part.set_payload(attachment_content)

                # Enviar o e-mail para a pasta correspondente no servidor IMAP
                mail.append(folder, '', imaplib.Time2Internaldate(time.time()), email_string.encode('utf-8'))

                success_count += 1

                print(f"E-mail enviado com sucesso ({success_count}/{total_emails})...")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")

    # Fechar conexão com o servidor IMAP
    mail.logout()

if __name__ == "__main__":
    main()
