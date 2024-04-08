import mail_backup
import mail_bkpcompress

# Fazer backup dos e-mails
backup = mail_backup.Backup()
backup.run_backup()

# Comprimir arquivos de backup .mbox
compress = mail_bkpcompress.FileCompression()
compress.run_compress()
