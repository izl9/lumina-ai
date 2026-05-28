from banco import bd, cursor

cursor = bd.cursor()


def registrarConversa(idUsuario, pergunta, resposta):
    cursor.execute(
        """
        INSERT INTO conversas (
        usuario_id, pergunta, resposta
        )
        VALUES (?, ?, ?)
        """,
        (idUsuario, pergunta, resposta),
    )

    bd.commit()
