const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const analyzeButton = document.getElementById("analyzeButton");
const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("resultsSection");
const mainVibe = document.getElementById("mainVibe");
const vibesList = document.getElementById("vibesList");
const tracksList = document.getElementById("tracksList");
const uploadArea = document.getElementById("uploadArea")

console.log({
    imageInput,
    imagePreview,
    analyzeButton,
    statusMessage,
    resultsSection,
    mainVibe,
    vibesList,
    tracksList,
});

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (!file) {
        analyzeButton.disabled = true;
        imagePreview.classList.add("hidden");
        uploadArea.classList.remove("hidden");
        return;
    }

    const imageUrl = URL.createObjectURL(file);
    uploadArea.classList.add("hidden");
    imagePreview.src = imageUrl;
    imagePreview.classList.remove("hidden");
    analyzeButton.disabled = false;
    resultsSection.classList.add("hidden");
});

analyzeButton.addEventListener("click", async () => {
    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    showStatus("AI аналізує фото та шукає музику...");

    analyzeButton.disabled = true;
    resultsSection.classList.add("hidden");

    try {
        const response = await fetch("/analyze-image", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            throw new Error(
                data.detail || "Не вдалося проаналізувати фото"
            );
        }

        renderResults(data);
        hideStatus();
    } catch (error) {
        showStatus(`Помилка: ${error.message}`);
    } finally {
        analyzeButton.disabled = false;
    }
});

function renderResults(data) {
    mainVibe.textContent = data.main_vibe;

    vibesList.innerHTML = "";

    data.detected_vibes.forEach((item) => {
        const badge = document.createElement("span");

        badge.className = "vibe-badge";
        badge.textContent = `${item.vibe} — ${item.score}%`;

        vibesList.appendChild(badge);
    });

    tracksList.innerHTML = "";

    data.recommended_tracks.forEach((track) => {
        const card = document.createElement("article");
        card.className = "track-card";

        const coverUrl =
            track.cover_url ||
            "https://placehold.co/200x200?text=Music";

        card.innerHTML = `
            <img
                class="track-cover"
                src="${coverUrl}"
                alt="Обкладинка ${escapeHtml(track.title)}"
            >

            <div>
                <h3 class="track-title">
                    ${escapeHtml(track.title)}
                </h3>

                <p class="track-artist">
                    ${escapeHtml(track.artist)}
                </p>

                <a
                    class="track-link"
                    href="${track.youtube_url}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Відкрити на YouTube
                </a>
            </div>
        `;

        tracksList.appendChild(card);
    });

    resultsSection.classList.remove("hidden");
    resultsSection.scrollIntoView({
        behavior: "smooth",
    });
}

function showStatus(message) {
    statusMessage.textContent = message;
    statusMessage.classList.remove("hidden");
}

function hideStatus() {
    statusMessage.classList.add("hidden");
}

function escapeHtml(value) {
    const element = document.createElement("div");
    element.textContent = value ?? "";
    return element.innerHTML;
}