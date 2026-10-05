/**
 * Pure dynamism layer — no phone-number logic lives here on purpose.
 * Detection happens server-side (see detector.py); this file just calls
 * the API and animates the existing markup to reflect what came back.
 * It never adds, removes, or restructures elements.
 */

const CHECK_URL_BASE = "/api/v1/phone/";

function qs(id) {
  return document.getElementById(id);
}

function showError(message) {
  const el = qs("error-msg");
  el.textContent = message;
  el.hidden = false;
}

function clearError() {
  const el = qs("error-msg");
  el.hidden = true;
  el.textContent = "";
}

function popResultCard() {
  const card = qs("result-card");
  card.classList.remove("nnd-pop");
  // Force a reflow so the animation replays on repeated lookups —
  // re-adding the same class name right after removing it is a no-op
  // without this.
  void card.offsetWidth;
  card.classList.add("nnd-pop");
}

function renderResult(data) {
  const network = data.original_network;
  const badge = qs("result-badge");
  const badgeLabel = badge.querySelector("span");

  badge.style.background = network.color;
  badgeLabel.textContent = network.name.split(" ")[0];
  badgeLabel.style.color = network.textColor;

  qs("result-name").textContent = network.name;
  qs("result-meta").textContent = `${data.phone_number} \u00b7 prefix ${data.prefix}`;

  popResultCard();
}

async function handleCheck() {
  clearError();

  const input = qs("phone-input");
  const button = qs("check-btn");
  const value = input.value.trim();

  if (!value) {
    showError("Enter a phone number to check.");
    return;
  }

  button.disabled = true;

  try {
    const response = await fetch(CHECK_URL_BASE + encodeURIComponent(value));
    const data = await response.json();

    if (!response.ok) {
      showError((data && data.error && data.error.message) || "Something went wrong checking that number.");
      return;
    }

    renderResult(data);
  } catch (networkError) {
    showError("Couldn't reach the server \u2014 check your connection and try again.");
  } finally {
    button.disabled = false;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  qs("check-btn").addEventListener("click", handleCheck);
  qs("phone-input").addEventListener("keydown", (event) => {
    if (event.key === "Enter") handleCheck();
  });
});
