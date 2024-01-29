import json

import aiofiles


async def carregar_configuracoes(caminho_arquivo="config.json"):
    async with aiofiles.open(caminho_arquivo, "r") as arquivo:
        conteudo = await arquivo.read()

    configuracoes = json.loads(conteudo)
    return configuracoes
