from banco import bd, cursor
from IA import registrarConversa
from chatbot import gerarResposta
from memoria import buscarMemoria, montarContexto


def processarPergunta(idUsuario, pergunta):

    historico_memoria = buscarMemoria(idUsuario)

    contexto = montarContexto(historico_memoria)

    resposta = gerarResposta(pergunta, contexto)

    registrarConversa(idUsuario, pergunta, resposta)

    return resposta


def limparHistorico(usuario_id):

    cursor.execute(
        """
        DELETE FROM conversas
        WHERE usuario_id = ?
    """,
        (usuario_id,),
    )

    bd.commit()
