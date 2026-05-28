from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
chave_api = os.getenv("GROQ_API_KEY")


modelo = ChatGroq(model="llama-3.3-70b-versatile")
parser = StrOutputParser()

template_mensagem = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Você é a Lumina AI, uma inteligência artificial criada por Izael Carvalho da Silva.

                Seu objetivo é ajudar usuários com:
                - programação
                - estudos
                - produtividade
                - tecnologia
                - inteligência artificial

                Você responde de forma:
                - amigável
                - moderna
                - clara
                - objetiva

                Nunca diga que é o ChatGPT.
                """,
        ),
        (
            "user",
            """
        Histórico da conversa:
        {contexto}

        Pergunta atual:
        {texto}
        """,
        ),
    ]
)

chain = template_mensagem | modelo | parser


def gerarResposta(pergunta, contexto):
    resposta = chain.invoke({"texto": pergunta, "contexto": contexto})

    return resposta
