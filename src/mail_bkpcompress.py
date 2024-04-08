import os
import lzma
import shutil

class FileCompression:
    def __init__(self):
        self.files = [
            # Lista de arquivos para compactar ou descompactar
            "bkp_email1.mbox",
            "bkp_email2.mbox",
            "bkp_email_exemplo_3.mbox"
        ]

    def compactar_arquivo(self, arquivo_origem):
        with open(arquivo_origem, 'rb') as f_in:
            with lzma.open(arquivo_origem + '.xz', 'wb', preset=9) as f_out:
                shutil.copyfileobj(f_in, f_out)
        return arquivo_origem + '.xz'

    def descompactar_arquivo(self, arquivo_compactado):
        nome_arquivo, _ = os.path.splitext(arquivo_compactado)
        arquivo_destino = nome_arquivo
        with lzma.open(arquivo_compactado, 'rb') as f_in:
            with open(arquivo_destino, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return arquivo_destino

    def compactar_ou_descompactar_arquivo(self, caminho_arquivo):
        if os.path.exists(caminho_arquivo):
            nome_arquivo, extensao = os.path.splitext(caminho_arquivo)
            if extensao == '.xz':
                arquivo_descompactado = self.descompactar_arquivo(caminho_arquivo)
                print(f'Arquivo descompactado: {arquivo_descompactado}')
            else:
                arquivo_compactado = self.compactar_arquivo(caminho_arquivo)
                print(f'Arquivo compactado: {arquivo_compactado}')
        else:
            print(f'Arquivo não encontrado: {caminho_arquivo}')

    def run_compress(self):
        for file in self.files:
            if not os.path.exists('BackupsEmail'):
                os.makedirs('BackupsEmail')
                
            caminho_arquivo = os.path.join('BackupsEmail', file)
            self.compactar_ou_descompactar_arquivo(caminho_arquivo)

if __name__ == "__main__":
    compressor = FileCompression()
    compressor.run_compress()
