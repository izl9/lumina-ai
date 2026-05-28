from backend.banco import bd, cursor
from backend.IA import registrarConversa
from backend.chatbot import gerarResposta
from backend.memoria import buscarMemoria, montarContexto


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
