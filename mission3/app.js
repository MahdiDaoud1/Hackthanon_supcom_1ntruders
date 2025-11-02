// ==========================================================
// CONFIGURATION
// ==========================================================
// ⬇️ *** PASTE YOUR NEW URL FROM THE TERMINAL HERE *** ⬇️
const VERCEL_BASE_URL =
  "https://hackthanonsupcom1ntruders-mmwp902aq-mahdidaoud1s-projects.vercel.app";
const REFRESH_INTERVAL = 5000; // 5 seconds
// ==========================================================

// --- Get DOM Elements ---
const plantStatusMap = {
  tomato: document.getElementById("tomato-status"),
  onion: document.getElementById("onion-status"),
  mint: document.getElementById("mint-status"),
};
const plantButtonMap = {
  tomato: document.getElementById("tomato-button"),
  onion: document.getElementById("onion-button"),
  mint: document.getElementById("mint-button"),
};
const pumpStatusEl = document.getElementById("pump-status");
const allOffButton = document.getElementById("all-off-button");
const allButtons = [...Object.values(plantButtonMap), allOffButton];

// --- Status Dictionaries ---
const PLANT_STATE_TEXT = { 0: "WET", 1: "DRY", 2: "WARN" };
const PLANT_STATE_CLASS = {
  0: "status-wet",
  1: "status-dry",
  2: "status-warn",
};

async function fetchPlantStatus() {
  try {
    const response = await fetch(`${VERCEL_BASE_URL}/get_status`);
    if (!response.ok) throw new Error("Network error");
    const statusString = await response.text(); // "1,0,2"
    const [tomato, onion, mint] = statusString.split(",");
    updatePlantUI("tomato", tomato);
    updatePlantUI("onion", onion);
    updatePlantUI("mint", mint);
  } catch (error) {
    console.error("Error fetching plant status:", error);
    updatePlantUI("tomato", null);
    updatePlantUI("onion", null);
    updatePlantUI("mint", null);
  }
}

async function fetchPumpStatus() {
  try {
    const response = await fetch(`${VERCEL_BASE_URL}/valve_status`);
    if (!response.ok) throw new Error("Network error");
    const statusString = await response.text(); // "IDLE"
    updatePumpUI(statusString);
  } catch (error) {
    console.error("Error fetching pump status:", error);
    updatePumpUI("UNKNOWN");
  }
}

async function sendManualCommand(command) {
  console.log(`Sending command: ${command}`);
  try {
    const response = await fetch(`${VERCEL_BASE_URL}/manual_command`, {
      method: "POST",
      body: command,
    });
    if (!response.ok) throw new Error("Command failed to send");
    console.log("Command sent successfully.");
    // Immediately fetch the pump status to get the update
    fetchPumpStatus();
  } catch (error) {
    console.error("Error sending command:", error);
    alert("Error: Could not send command to server.");
  }
}

function updatePlantUI(plantName, statusKey) {
  const el = plantStatusMap[plantName];
  if (!el) return;
  if (statusKey === null) {
    el.textContent = "ERROR";
    el.className = "status-box";
    return;
  }
  el.textContent = PLANT_STATE_TEXT[statusKey] || "UNKNOWN";
  el.className = `status-box ${PLANT_STATE_CLASS[statusKey] || ""}`;
}

function updatePumpUI(status) {
  pumpStatusEl.textContent = status;
  if (status === "IDLE" || status === "UNKNOWN" || status === "ERROR") {
    pumpStatusEl.className = "status-box pump-idle";
    allButtons.forEach((btn) => (btn.disabled = false));
  } else {
    pumpStatusEl.className = "status-box pump-active";
    allButtons.forEach((btn) => (btn.disabled = true));
  }
}

plantButtonMap.tomato.addEventListener("click", () =>
  sendManualCommand("TOMATO_ON")
);
plantButtonMap.onion.addEventListener("click", () =>
  sendManualCommand("ONION_ON")
);
plantButtonMap.mint.addEventListener("click", () =>
  sendManualCommand("MINT_ON")
);
allOffButton.addEventListener("click", () => sendManualCommand("ALL_OFF"));

function startApp() {
  console.log("Starting Smart Farm Control Board...");
  fetchPlantStatus();
  fetchPumpStatus();
  setInterval(fetchPlantStatus, REFRESH_INTERVAL);
  setInterval(fetchPumpStatus, REFRESH_INTERVAL);
}
startApp();
