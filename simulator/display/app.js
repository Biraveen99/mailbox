const SERVER_URL =
    `${window.location.protocol}//${window.location.hostname}:8000`;

const POLL_INTERVAL = 2000;


const card =
    document.getElementById(
        "message-card"
    );

const titleElement =
    document.getElementById(
        "message-title"
    );

const bodyElement =
    document.getElementById(
        "message-body"
    );

const typeElement =
    document.getElementById(
        "message-type"
    );

const iconElement =
    document.getElementById(
        "message-icon"
    );

const statusElement =
    document.getElementById(
        "status"
    );

const ackButton =
    document.getElementById(
        "ack-button"
    );

const heartsElement =
    document.getElementById(
        "ambient-hearts"
    );


let currentMessage = null;


/*
 * Display themes
 */

const themes = {

    message: {
        label: "MELDING",
        icon: "💌",
        className:
            "theme-message",
    },

    compliment: {
        label: "KOMPLIMENT",
        icon: "💕",
        className:
            "theme-compliment",
    },

    date: {
        label: "DATE PLAN",
        icon: "🌹",
        className:
            "theme-date",
    },

    surprise: {
        label: "SURPRISE",
        icon: "✨",
        className:
            "theme-surprise",
    },

};


/*
 * API
 */

async function getLatestMessage() {

    const response =
        await fetch(
            `${SERVER_URL}/messages/latest`
        );

    if (!response.ok) {
        throw new Error(
            `Backend returned ${response.status}`
        );
    }

    return response.json();
}


async function acknowledgeMessage(
    messageId
) {

    const response =
        await fetch(
            `${SERVER_URL}/messages/${messageId}/ack`,
            {
                method: "POST",
            }
        );

    if (!response.ok) {
        throw new Error(
            `Could not acknowledge message ${messageId}`
        );
    }

    return response.json();
}


/*
 * Display
 */

function resetTheme() {

    card.classList.remove(
        "theme-idle",
        "theme-message",
        "theme-compliment",
        "theme-date",
        "theme-surprise",
        "message-arrived",
        "surprise-active",
    );
}


function displayMessage(message) {

    currentMessage = message;

    const theme =
        themes[message.type]
        ?? themes.message;


    resetTheme();


    card.classList.add(
        theme.className
    );


    if (
        message.type === "surprise"
    ) {
        card.classList.add(
            "surprise-active"
        );
    }


    iconElement.textContent =
        theme.icon;

    typeElement.textContent =
        theme.label;

    titleElement.textContent =
        message.title;

    bodyElement.textContent =
        message.body;


    ackButton.hidden = false;


    heartsElement.classList.add(
        "hearts-active"
    );


    /*
     * Restart arrival animation
     */

    void card.offsetWidth;

    card.classList.add(
        "message-arrived"
    );
}


function clearMessage() {

    currentMessage = null;

    resetTheme();

    card.classList.add(
        "theme-idle"
    );


    iconElement.textContent =
        "💗";

    typeElement.textContent =
        "LOVE BOX";

    titleElement.textContent =
        "Love Box ❤️";

    bodyElement.textContent =
        "Venter på en melding...";


    ackButton.hidden = true;


    heartsElement.classList.remove(
        "hearts-active"
    );
}


/*
 * Polling
 */

async function pollBackend() {

    try {

        statusElement.textContent =
            "● Tilkoblet";

        statusElement.classList.add(
            "connected"
        );


        /*
         * Don't fetch another message
         * while one is being displayed.
         */

        if (
            currentMessage !== null
        ) {
            return;
        }


        const message =
            await getLatestMessage();


        if (
            message !== null
        ) {
            displayMessage(
                message
            );
        }

    } catch (error) {

        statusElement.textContent =
            "● Frakoblet";

        statusElement.classList.remove(
            "connected"
        );

        console.error(
            error
        );
    }
}


/*
 * ACK button
 */

ackButton.addEventListener(
    "click",

    async () => {

        if (
            currentMessage === null
        ) {
            return;
        }


        try {

            ackButton.disabled =
                true;

            ackButton.textContent =
                "Sender ❤️...";


            await acknowledgeMessage(
                currentMessage.id
            );


            console.log(
                `Message #${currentMessage.id} acknowledged`
            );


            clearMessage();


        } catch (error) {

            console.error(
                error
            );


        } finally {

            ackButton.disabled =
                false;

            ackButton.textContent =
                "❤️ Sett";
        }

    }
);


/*
 * Start device
 */

pollBackend();


setInterval(
    pollBackend,
    POLL_INTERVAL
);