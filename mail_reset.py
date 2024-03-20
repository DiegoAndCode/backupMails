import imaplib

def delete_all_messages_in_folder(imap_conn, folder_name):
    # Selecionar a pasta
    try:
        status, _ = imap_conn.select(folder_name)
        if status != 'OK':
            print(f"Erro ao selecionar a pasta {folder_name}")
            return -1
    except imaplib.IMAP4.error as e:
        print(e)
        return -1

    # Listar todas as mensagens na pasta
    status, messages = imap_conn.search(None, 'ALL')
    if status != 'OK':
        print(f"Erro ao listar e-mails na pasta {folder_name}")
        return -1

    # Excluir todas as mensagens
    for num in messages[0].split():
        imap_conn.store(num, '+FLAGS', '\\Deleted')
    imap_conn.expunge()

    #print(f"Todas as mensagens na pasta '{folder_name}' foram excluídas com sucesso.")

def main():
    imap_host = 'email-ssl.com.br'
    imap_port = 993

    # Email que será resetado (Apagar todas as pastas e todas as mensagens)    
    username = 'email1@exemplo.com.br'
    password = 'SenhaDoEmail123'

    # Lista de pastas padrão que serão mantidas
    pastas_padrao = ['INBOX', '"INBOX.Sent Items"', 'INBOX.lixo', 'INBOX.rascunho', 'INBOX.enviadas', 'INBOX.Mala_Direta']

    try:
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(imap_host, imap_port)
        mail.login(username, password)

        # Excluir todas as mensagens das pastas não padrão
        status, folders = mail.list()
        if status != 'OK':
            print("Erro ao listar pastas")
            return

        print('Excluindo mensagens da Caixa de Entrada...')
        delete_all_messages_in_folder(mail, 'INBOX')

        for folder_info in folders[1:]:
            folder_name = folder_info.decode('utf-8').split(' "." ')[1]
            print(f'Excluindo mensagens da pasta: {folder_name}...')

            delete_all_messages_in_folder(mail, folder_name)
        
        # Criar uma nova lista de pastas excluindo as pastas padrão
        pastas_nao_padrao = [folder_info.decode('utf-8').split(' "." ')[1] for folder_info in folders[1:] if folder_info.decode('utf-8').split(' "." ')[1] not in pastas_padrao]

        # Excluir as pastas não padrão
        for folder_name in pastas_nao_padrao:
            print(f'Deletando a pasta: {folder_name}...')
            mail.delete(folder_name)

        # Fechar conexão com o servidor IMAP
        mail.logout()

        print("Reset de e-mail concluído com sucesso.")
    except Exception as e:
        print(f"Erro ao resetar e-mail: {str(e)}")

if __name__ == "__main__":
    main()
