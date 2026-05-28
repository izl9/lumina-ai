document.addEventListener("DOMContentLoaded", () => {

    const chatData =
        document.getElementById("chatData");



    /*
    =====================================
    SE NÃO FOR A PÁGINA DO CHAT
    PARA O SCRIPT
    =====================================
    */

    if (!chatData) return;



    const container =
        document.getElementById("chatContainer");

    const scroll =
        document.getElementById("chatScroll");

    const input =
        document.getElementById("chatInput");

    const sendBtn =
        document.getElementById("sendBtn");

    const stopBtn =
        document.getElementById("stopBtn");

    const clearBtn =
        document.getElementById("clearBtn");

    const backdrop =
        document.getElementById("modalBackdrop");



    const usuario =
        chatData.dataset.usuario;

    const limparUrl =
        chatData.dataset.limparUrl;



    let abortCtrl = null;

    let isTyping = false;



    /*
    =====================================
    SCROLL
    =====================================
    */

    function toBottom() {

        scroll.scrollTo({

            top: scroll.scrollHeight,

            behavior: "smooth"

        });

    }



    toBottom();



    /*
    =====================================
    AUTO HEIGHT INPUT
    =====================================
    */

    input.addEventListener("input", () => {

        input.style.height = "auto";

        input.style.height =
            Math.min(
                input.scrollHeight,
                140
            ) + "px";

    });



    /*
    =====================================
    ENTER PARA ENVIAR
    =====================================
    */

    input.addEventListener("keydown", (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            send();

        }

    });



    sendBtn.addEventListener("click", send);



    /*
    =====================================
    CRIAR BOLHA
    =====================================
    */

    function createBubble(type) {

        const wrap =
            document.createElement("div");

        wrap.className =
            `msg msg--${type}`;



        if (type === "ai") {

            const avatar =
                document.createElement("div");

            avatar.className =
                "msg__avatar";

            avatar.textContent = "L";

            wrap.appendChild(avatar);

        }



        const body =
            document.createElement("div");

        body.className =
            "msg__body";



        if (type === "user") {

            body.style.alignItems =
                "flex-end";

        }



        const name =
            document.createElement("span");

        name.className =
            "msg__name";

        name.textContent =
            type === "ai"
                ? "Lumina"
                : usuario;



        const bubble =
            document.createElement("div");

        bubble.className =
            "msg__bubble";



        body.appendChild(name);

        body.appendChild(bubble);

        wrap.appendChild(body);

        container.appendChild(wrap);



        toBottom();



        return bubble;

    }



    /*
    =====================================
    TYPING
    =====================================
    */

    function showTyping() {

        const wrap =
            document.createElement("div");

        wrap.className =
            "msg msg--ai";

        wrap.id =
            "typingWrap";



        const avatar =
            document.createElement("div");

        avatar.className =
            "msg__avatar";

        avatar.textContent = "L";



        const body =
            document.createElement("div");

        body.className =
            "msg__body";



        const name =
            document.createElement("span");

        name.className =
            "msg__name";

        name.textContent =
            "Lumina";



        const bubble =
            document.createElement("div");

        bubble.className =
            "msg__bubble typing-bubble";

        bubble.innerHTML =
            "<span></span><span></span><span></span>";



        body.appendChild(name);

        body.appendChild(bubble);

        wrap.appendChild(avatar);

        wrap.appendChild(body);

        container.appendChild(wrap);



        toBottom();

    }



    function hideTyping() {

        const typing =
            document.getElementById(
                "typingWrap"
            );



        if (typing) {

            typing.remove();

        }

    }



    /*
    =====================================
    EFEITO DE ESCRITA
    =====================================
    */

    async function typewrite(
        element,
        text
    ) {

        for (
            let i = 0;
            i < text.length;
            i++
        ) {

            if (!isTyping) break;



            element.textContent += text[i];



            toBottom();



            await new Promise(resolve =>

                setTimeout(resolve, 15)

            );

        }

    }



    /*
    =====================================
    ENVIAR MENSAGEM
    =====================================
    */

    async function send() {

        const pergunta =
            input.value.trim();



        if (
            !pergunta ||
            isTyping
        ) return;



        input.value = "";

        input.style.height =
            "auto";



        createBubble("user")
            .textContent = pergunta;



        showTyping();



        isTyping = true;



        sendBtn.style.display =
            "none";

        stopBtn.style.display =
            "flex";



        abortCtrl =
            new AbortController();



        try {

            const response =
                await fetch("/api/chat", {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        pergunta: pergunta

                    }),

                    signal:
                        abortCtrl.signal

                });



            const data =
                await response.json();



            hideTyping();



            const bubble =
                createBubble("ai");



            await typewrite(

                bubble,

                data.resposta

            );

        }

        catch (erro) {

            hideTyping();



            if (
                erro.name !==
                "AbortError"
            ) {

                createBubble("ai")
                    .textContent =

                    "Erro ao conectar.";

            }

        }



        isTyping = false;



        sendBtn.style.display =
            "flex";

        stopBtn.style.display =
            "none";

    }



    /*
    =====================================
    PARAR RESPOSTA
    =====================================
    */

    stopBtn.addEventListener("click", () => {

        isTyping = false;



        if (abortCtrl) {

            abortCtrl.abort();

        }



        hideTyping();



        sendBtn.style.display =
            "flex";

        stopBtn.style.display =
            "none";

    });



    /*
    =====================================
    LIMPAR CHAT
    =====================================
    */

    clearBtn.addEventListener("click", () => {

        backdrop.classList.add("show");

    });



    document
        .getElementById("modalCancel")
        .addEventListener("click", () => {

            backdrop.classList.remove("show");

        });



    backdrop.addEventListener("click", (event) => {

        if (
            event.target === backdrop
        ) {

            backdrop.classList.remove("show");

        }

    });



    document
        .getElementById("modalConfirm")
        .addEventListener("click", () => {

            window.location.href =
                limparUrl;

        });





    /*
    =====================================
    PERGUNTA INICIAL
    =====================================
    */

    const perguntaInicial =
        localStorage.getItem(
            "perguntaInicial"
        );



    if (perguntaInicial) {

        input.value =
            perguntaInicial;



        send();



        localStorage.removeItem(
            "perguntaInicial"
        );

    }

});