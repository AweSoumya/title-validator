const verifyBtn = document.getElementById("verifyBtn");
const titleInput = document.getElementById("titleInput");
const progressBar = document.getElementById("progressBar");
const resultCard = document.getElementById("resultCard");
const toast = document.getElementById("toast");

verifyBtn.addEventListener("click", verifyTitle);
titleInput.addEventListener("keypress", e => {
    if (e.key === "Enter") verifyTitle();
});

async function verifyTitle() {

    const title = titleInput.value.trim();

    if (!title) {
        showToast("Please enter a title name.");
        return;
    }

    toggleLoading(true);

    try {
        // ✅ Correct endpoint (matches routes.py)
        const response = await fetch("/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();
        console.log("Backend Response:", data); // Debug (can remove later)

        displayResults(data);

    } catch (err) {
        console.error(err);
        showToast("Server connection error.");
    }

    toggleLoading(false);
}

function toggleLoading(state) {
    progressBar.classList.toggle("hidden", !state);
}

function displayResults(data) {

    // Convert decimal (0–1) to percentage (0–100)
    const similarity = (data.similarity_score ?? 0) * 100;
    const probability = (data.verification_probability ?? 0) * 100;

    document.getElementById("similarity").textContent =
        similarity.toFixed(2) + "%";

    document.getElementById("probability").textContent =
        probability.toFixed(2) + "%";

    document.getElementById("reason").textContent =
        data.reason ?? "No remarks provided.";

    const statusBox = document.getElementById("statusBox");
    const statusText = document.getElementById("statusText");

    statusBox.className = "status-box";

    // Decision logic based on percentage
    if (similarity < 30) {
        statusBox.classList.add("available");
        statusText.textContent = "🟢 Title Available for Registration";
    }
    else if (similarity < 70) {
        statusBox.classList.add("review");
        statusText.textContent = "🟡 Requires Manual Review";
    }
    else {
        statusBox.classList.add("not-available");
        statusText.textContent = "🔴 Title Not Available (Similar Title Exists)";
    }

    resultCard.classList.remove("hidden");
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.remove("hidden");

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}