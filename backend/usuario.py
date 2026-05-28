from flask import request, session
from banco import bd, cursor


def cadastrarUsuario():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["senha"]

    cursor.execute(
        """INSERT INTO usuarios (
        email, nome, senha)
        VALUES (?, ?, ?)
        """,
        (email, nome, senha),
    )

    bd.commit()


def verificarUsuario():

    if "usuario_id" not in session:
        return None

    idUsuario = session["usuario_id"]

    cursor.execute(
        """
        SELECT * FROM usuarios
        WHERE id = ?
    """,
        (idUsuario,),
    )

    usuario = cursor.fetchone()

    if not usuario:
        session.clear()
        return None

    return usuario


def fazerLogin():
    email = request.form["email"]
    senha = request.form["senha"]

    cursor.execute(
        """SELECT * FROM usuarios
                WHERE email = ? AND senha = ?
                """,
        (email, senha),
    )

    usuario = cursor.fetchone()

    return usuario


def buscarUsuarioPeloId(id_usuario):

    cursor.execute(
        """
        SELECT * FROM usuarios
        WHERE id = ?
        """,
        (id_usuario,),
    )

    usuario = cursor.fetchone()

    return usuario


def contarConversas(id):
    cursor.execute(
        """
        SELECT COUNT(*) FROM conversas
        WHERE usuario_id = ?
        """,
        (id,),
    )

    return cursor.fetchone()[0] or 0
