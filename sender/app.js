const SERVER_URL =
    `${window.location.protocol}//${window.location.hostname}:8000`;

const typeButtons =
    document.querySelectorAll(
        ".type-button"
    );

const titleInput =
    document.getElementById(
        "title"
    );

const bodyInput =
    document.getElementById(
        "body"
    );

const sendButton =
    document.getElementById(
        "send-button"
    );

const statusElement =
    document.getElementById(
        "status"
    );


let selectedType =
    "message";


typeButtons.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                typeButtons.forEach(
                    item =>
                        item.classList.remove(
                            "active"
                        )
                );


                button.classList.add(
                    "active"
                );


                selectedType =
                    button.dataset.type;

            }
        );

    }
);


async function sendMessage() {

    const title =
        titleInput.value.trim();

    const body =
        bodyInput.value.trim();


    if (!title || !body) {

        statusElement.textContent =
            "Fyll inn tittel og melding ❤️";

        statusElement.className =
            "status error";

        return;
    }


    sendButton.disabled =
        true;

    sendButton.textContent =
        "Sender...";


    statusElement.textContent =
        "";


    try {

        const response =
            await fetch(
                `${SERVER_URL}/messages`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            type:
                                selectedType,

                            title:
                                title,

                            body:
                                body
                        })
                }
            );


        if (!response.ok) {

            const error =
                await response.text();

            throw new Error(
                error
            );
        }


        const message =
            await response.json();


        statusElement.textContent =
            `Sendt ❤️ (#${message.id})`;

        statusElement.className =
            "status success";


        titleInput.value =
            "";

        bodyInput.value =
            "";


    } catch (error) {

        console.error(
            error
        );


        statusElement.textContent =
            "Kunne ikke sende 💔";

        statusElement.className =
            "status error";


    } finally {

        sendButton.disabled =
            false;

        sendButton.textContent =
            "Send ❤️";
    }
}


sendButton.addEventListener(
    "click",
    sendMessage
);