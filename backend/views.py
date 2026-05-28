from backend.main import app
from banco import cursor
from flask import render_template, request, redirect, url_for, session, jsonify
from memoria import buscarHistoricoCompleto, buscarMemoria, montarContexto
from usuario import (
    cadastrarUsuario,
    verificarUsuario,
    fazerLogin,
    buscarUsuarioPeloId,
    contarConversas,
)
from perguntas import processarPergunta, limparHistorico


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/chat")
def chat():

    usuario = verificarUsuario()

    if not usuario:
        return redirect(url_for("login"))

    idUsuario = usuario[0]

    historico = buscarHistoricoCompleto(idUsuario)

    return render_template("chat.html", historico=historico)


@app.route("/aprendizado")
def aprendizado():
    return render_template("aprendizado.html")


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/usuarios/<int:id>")
def usuarios(id):

    usuario = verificarUsuario()

    if not usuario:
        return redirect(url_for("login"))

    if usuario[0] != id:
        return redirect(url_for("usuarios", id=usuario[0]))

    usuario_perfil = buscarUsuarioPeloId(id)

    if not usuario_perfil:
        return redirect(url_for("chat"))

    total_conversas = contarConversas(id)

    return render_template(
        "usuarios.html",
        usuario=usuario_perfil,
        total_conversas=total_conversas,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        usuario = fazerLogin()

        if usuario:
            session["usuario_id"] = usuario[0]
            session["nome_usuario"] = usuario[1]

            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", erro="Email ou senha incorretos.")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        cadastrarUsuario()
        return render_template(
            "cadastro.html", cadastro="Usuário cadastrado com sucesso!"
        )

    return render_template("cadastro.html")


@app.route("/limpar_conversa")
def limpar_conversa():

    usuario = verificarUsuario()

    if not usuario:
        return redirect(url_for("login"))

    limparHistorico(usuario[0])

    return redirect(url_for("chat"))


@app.route("/api/chat", methods=["POST"])
def api_chat():
    usuario = verificarUsuario()

    if not usuario:
        return jsonify({"resposta": "Você precisa fazer login primeiro."}), 401

    dados = request.get_json()

    pergunta = dados.get("pergunta", "")

    if not pergunta.strip():

        return jsonify({"resposta": "Pergunta inválida."}), 400

    try:

        resposta = processarPergunta(usuario[0], pergunta)

        return jsonify({"resposta": resposta})

    except Exception as erro:

        print("ERRO NA API DO CHAT:", erro)

        return jsonify({"resposta": "Erro interno ao gerar resposta."}), 500


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("homepage"))
