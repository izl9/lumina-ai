from backend.banco import cursor


def buscarHistoricoCompleto(usuario_id):

    cursor.execute(
        """
        SELECT pergunta, resposta
        FROM conversas
        WHERE usuario_id = ?
        ORDER BY id ASC
    """,
        (usuario_id,),
    )

    return cursor.fetchall()


def buscarMemoria(idUsuario):

    cursor.execute(
        """
        SELECT pergunta, resposta FROM conversas
        WHERE usuario_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (idUsuario,),
    )

    return cursor.fetchall()


def montarContexto(historico):

    contexto = ""

    for pergunta, resposta in historico:

        contexto += f"""
        Usuário: {pergunta}
        Lumina: {resposta}
        """

    return contexto
