import mail_backup
import mail_bkpcompress

# Fazer backup dos e-mails
backup = mail_backup.Backup()
backup.run_backup()

print('*' * 10, 'Backup concluído', '*' * 10)
print('*' * 10, 'Iniciando compressão dos arquivos', '*' * 10)

# Comprimir arquivos de backup .mbox
compress = mail_bkpcompress.FileCompression()
compress.run_compress()
