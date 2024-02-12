import json
import aiofiles


async def carregar_configuracoes(caminho_arquivo="config.json"):
    with open(caminho_arquivo, "r") as arquivo:
        conteudo = arquivo.read()

    configuracoes = json.loads(conteudo)
    return configuracoes


