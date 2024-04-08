import imaplib
import os
import email
import mailbox

class Backup:
    def __init__(self):
        self.imap_host = 'email-ssl.com.br'
        self.imap_port = 993
        self.emails = {
            'email1@exemplo.com.br' : 'SenhaDoEmail123', 
            'email2@exemplo.com.br' : 'SenhaDoEmail123',
            'email_exemplo3@exemplo.com.br' : 'SenhaDoEmail123'
        }
        
        # Obtém o diretório atual onde o script está sendo executado
        self.current_directory = os.path.dirname(os.path.abspath(__file__))

    def save_folder_emails(self, imap_conn, folder_name, mbox):
        # Selecionar a pasta
        status, messages = imap_conn.select(folder_name)
        if status != 'OK':
            print(f"Erro ao selecionar a pasta {folder_name}")
            return

        # Listar todos os e-mails na pasta
        status, messages = imap_conn.search(None, 'ALL')
        if status != 'OK':
            print(f"Erro ao listar e-mails na pasta {folder_name}")
            return

        # Baixar e salvar os e-mails
        for num in messages[0].split():
            try:
                # Baixar o e-mail
                status, data = imap_conn.fetch(num, '(RFC822)')
                if status == 'OK':
                    email_msg = email.message_from_bytes(data[0][1])

                    # Adicionar o cabeçalho X-Source ao e-mail
                    email_msg['X-Source'] = folder_name

                    # Adicionar o e-mail à caixa de correio mbox
                    mbox.add(email_msg)
                else:
                    print(f"Erro ao baixar e-mail {num}")
            except Exception as e:
                print(f"Erro ao processar e-mail {num}: {e}")

    def count_emails_in_folder(self, imap_conn, folder_name):
        # Selecionar a pasta
        status, messages = imap_conn.select(folder_name)
        if status != 'OK':
            print(f"Erro ao selecionar a pasta {folder_name}")
            return -1

        # Listar todos os e-mails na pasta
        status, messages = imap_conn.search(None, 'ALL')
        if status != 'OK':
            print(f"Erro ao listar e-mails na pasta {folder_name}")
            return -1

        # Contar a quantidade de e-mails
        count = len(messages[0].split())
        return count

    def save_all_folders_emails(self, imap_conn, mbox):
        # Salvar e-mails da caixa de entrada (INBOX)
        inbox_count = self.count_emails_in_folder(imap_conn, 'INBOX')
        if inbox_count >= 0:
            print(f"Processando pasta: Caixa de Entrada ({inbox_count} e-mails)...")
            self.save_folder_emails(imap_conn, 'INBOX', mbox)

        # Listar todas as pastas
        status, folders = imap_conn.list()
        if status != 'OK':
            print("Erro ao listar pastas")
            return

        # Decodificar e ordenar a lista de pastas em ordem alfabética
        folders_decoded = [folder.decode() for folder in folders]
        folders_sorted = sorted(folders_decoded)

        # Iterar sobre as pastas ordenadas
        for folder in folders_sorted[1:]:
            # Extrair o nome da pasta
            if ' "." ' in folder:
                folder_name = folder.split(' "." ')[1]
            else:
                continue

            # Contar a quantidade de e-mails na pasta
            folder_count = self.count_emails_in_folder(imap_conn, folder_name)
            if folder_count >= 0:
                print(f"Processando pasta: {folder_name} ({folder_count} e-mails)...")
                # Salvar e-mails da pasta
                self.save_folder_emails(imap_conn, folder_name, mbox)

    def run_backup(self):
        for user, password in self.emails.items():
            username = user.split('@')[0]

            # Criar o caminho do arquivo mbox
            mbox_path = os.path.join(self.current_directory, fr'BackupsEmail\bkp_{username}.mbox')

            # Verificar se o arquivo mbox já existe e, se sim, excluí-lo
            if os.path.exists(mbox_path):
                os.remove(mbox_path)

            print(f'-> {user} : Conectando...')

            # Conectar ao servidor IMAP
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(user, password)

            # Criar uma caixa de correio mbox
            mbox = mailbox.mbox(mbox_path)

            # Salvar e-mails de todas as pastas
            self.save_all_folders_emails(mail, mbox)

            # Fechar a caixa de correio mbox
            mbox.close()

            print(f'Arquivo .mbox salvo em: {mbox_path}')

            # Fechar conexão
            mail.logout()

if __name__ == "__main__":
    backup = Backup()
    backup.run_backup()
