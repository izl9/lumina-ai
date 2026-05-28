document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("formInicio");

    if (!form) return;



    form.addEventListener("submit", (event) => {

        event.preventDefault();



        const pergunta =
            document
                .getElementById("comecarChat")
                .value;



        if (pergunta.trim()) {

            localStorage.setItem(
                "perguntaInicial",
                pergunta
            );



            window.location.href = "/chat";

        }

    });

});