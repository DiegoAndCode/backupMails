import os
import lzma
import shutil

def compactar_arquivo(arquivo_origem):
    with open(arquivo_origem, 'rb') as f_in:
        with lzma.open(arquivo_origem + '.xz', 'wb', preset=9) as f_out:
            shutil.copyfileobj(f_in, f_out)
    return arquivo_origem + '.xz'

def descompactar_arquivo(arquivo_compactado):
    nome_arquivo, _ = os.path.splitext(arquivo_compactado)
    arquivo_destino = nome_arquivo
    with lzma.open(arquivo_compactado, 'rb') as f_in:
        with open(arquivo_destino, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return arquivo_destino

def compactar_ou_descompactar_arquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        nome_arquivo, extensao = os.path.splitext(caminho_arquivo)
        # Caso seja extensão .xz é pra descompactar
        if extensao == '.xz':
            arquivo_descompactado = descompactar_arquivo(caminho_arquivo)
            print(f'Arquivo descompactado: {arquivo_descompactado}')
        else:
            # Caso contrário é pra Compactar para .xz
            arquivo_compactado = compactar_arquivo(caminho_arquivo)
            print(f'Arquivo compactado: {arquivo_compactado}')
    else:
        print(f'Arquivo não encontrado: {caminho_arquivo}')

def main():
    files = [
        # Lista de arquivos para compactar ou descompactar
        "bkp_email1.mbox",
        "bkp_email2.mbox",
        "bkp_email_exemplo_3.mbox"
    ]


    for file in files:
        # Salvar em uma pasta separada
        if not os.path.exists('BackupsEmail'):
            os.makedirs('BackupsEmail')

        caminho_arquivo = f'BackupsEmail/{file}'
        compactar_ou_descompactar_arquivo(caminho_arquivo)

if __name__ == "__main__":
    main()
