import os

def fixPath(caminho_generico):
    # Extraia o diretório do caminho genérico
    diretorio = os.path.dirname(caminho_generico)

    # Verifique se o diretório existe e crie-o, se necessário
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
