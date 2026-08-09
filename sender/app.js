const DEFAULT_DEVICE_ID = "LB-000001";

const params = new URLSearchParams(window.location.search);
const DEVICE_ID = params.get("device") || DEFAULT_DEVICE_ID;

// For local development the API is normally on the same host at port 8000.
// When the sender is hosted publicly, set window.LOVEBOX_API_URL before app.js.
const SERVER_URL =
    window.LOVEBOX_API_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000`;

const typeButtons = document.querySelectorAll(".type-button");
const titleInput = document.getElementById("title");
const bodyInput = document.getElementById("body");
const sendButton = document.getElementById("send-button");
const statusElement = document.getElementById("status");

let selectedType = "message";


typeButtons.forEach(button => {
    button.addEventListener("click", () => {
        typeButtons.forEach(item => item.classList.remove("active"));
        button.classList.add("active");
        selectedType = button.dataset.type;
    });
});


async function sendMessage() {
    const title = titleInput.value.trim();
    const body = bodyInput.value.trim();

    if (!title || !body) {
        statusElement.textContent = "Fyll inn tittel og melding ❤️";
        statusElement.className = "status error";
        return;
    }

    sendButton.disabled = true;
    sendButton.textContent = "Sender...";
    statusElement.textContent = "";

    try {
        const response = await fetch(
            `${SERVER_URL}/devices/${encodeURIComponent(DEVICE_ID)}/messages`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    type: selectedType,
                    title,
                    body
                })
            }
        );

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        const message = await response.json();

        statusElement.textContent =
            `Sendt til ${message.device_id} ❤️ (#${message.id})`;
        statusElement.className = "status success";

        titleInput.value = "";
        bodyInput.value = "";
    } catch (error) {
        console.error(error);
        statusElement.textContent = "Kunne ikke sende 💔";
        statusElement.className = "status error";
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send ❤️";
    }
}


sendButton.addEventListener("click", sendMessage);


if ("serviceWorker" in navigator) {
    window.addEventListener("load", async () => {
        try {
            if (!window.isSecureContext) {
                console.log("Service worker skipped: insecure context");
                return;
            }

            const registration = await navigator.serviceWorker.register(
                "/service-worker.js"
            );

            console.log(
                "Service worker registered:",
                registration.scope
            );
        } catch (error) {
            console.error("Service worker registration failed:", error);
        }
    });
}
