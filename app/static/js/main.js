let map;
let markers = [];
const locations = [];

function initMap() {
  map = L.map("map").setView([-23.5505, -46.6333], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
  }).addTo(map);
}

function addLocation(data) {
  const timestamp = new Date().toLocaleString();
  locations.unshift({
    latitude: data.latitude,
    longitude: data.longitude,
    timestamp: timestamp,
  });

  updateLocationsList();
  updateMap(data.latitude, data.longitude);
}

function updateLocationsList() {
  const container = document.getElementById("locations-list");
  container.innerHTML = locations
    .map(
      (loc, index) => `
        <div class="location-item ${index === 0 ? "new" : ""}">
            <strong>Latitude:</strong> ${loc.latitude}<br>
            <strong>Longitude:</strong> ${loc.longitude}<br>
            <small class="text-muted">${loc.timestamp}</small>
        </div>
    `
    )
    .join("");
}

function updateMap(lat, lng) {
  // Remove a animação de pulso do marcador anterior
  if (markers.length > 0) {
    const lastMarker = markers[markers.length - 1];
    const lastEl = lastMarker.getElement();
    if (lastEl) {
      lastEl.querySelector(".marker-pulse").classList.add("static");
    }
  }

  // Adiciona o novo marcador com pulso
  const marker = L.marker([lat, lng], {
    icon: L.divIcon({
      className: "custom-marker",
      html: `<div class="marker-pulse active"></div>`,
      iconSize: [20, 20],
    }),
  }).addTo(map);

  markers.push(marker);
  map.setView([lat, lng], 13);
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  initMap();
});

// WebSocket para dados em tempo real
const ws = new WebSocket(`ws://${window.location.host}/ws`);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  addLocation(data);
};
