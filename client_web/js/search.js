// Contrôleur de la recherche publique (catalogue.html). Dépend de app.js
// pour apiFetch ; ne nécessite pas de session (page publique).

function renderResults(results) {
  const tbody = document.getElementById("results-body");
  const emptyState = document.getElementById("empty-state");

  tbody.innerHTML = "";

  if (!results.length) {
    emptyState.hidden = false;
    return;
  }
  emptyState.hidden = true;

  results.forEach((item) => {
    const row = document.createElement("tr");

    const produitCell = document.createElement("td");
    produitCell.textContent = item.name; 

    const succursaleCell = document.createElement("td");
    succursaleCell.textContent = item.branch_name ?? "—";

    const quantiteCell = document.createElement("td");
    quantiteCell.textContent = item.quantity;

    const detailsCell = document.createElement("td");
    const detailsBtn = document.createElement("button");
    detailsBtn.type = "button";
    detailsBtn.className = "link-btn";
    detailsBtn.textContent = "Voir";
    detailsBtn.addEventListener("click", () => openDetailsModal(item));
    detailsCell.appendChild(detailsBtn);

    row.append(produitCell, succursaleCell, quantiteCell, detailsCell);
    tbody.appendChild(row);
  });
}

// Modal de détails (bouton "Voir") : affiche les champs déjà présents dans
// le résultat de recherche, sans appel réseau supplémentaire.
function openDetailsModal(item) {
  document.getElementById("details-name").textContent = item.name;
  document.getElementById("details-sku").textContent = item.sku;
  document.getElementById("details-category").textContent = item.category ?? "—";
  document.getElementById("details-price").textContent =
    item.unit_price != null ? `${item.unit_price} €` : "—";
  document.getElementById("details-branch").textContent = item.branch_name ?? "—";
  document.getElementById("details-quantity").textContent = item.quantity;

  document.getElementById("details-overlay").hidden = false;
}

function closeDetailsModal() {
  document.getElementById("details-overlay").hidden = true;
}

// GET /api/search?q=... : renvoie [] (plutôt que de faire planter l'UI) si
// le backoffice ou l'API produits externe qu'il interroge est indisponible.
async function fetchResults(query) {
  try {
    return await apiFetch(`/api/search?q=${encodeURIComponent(query)}`);
  } catch (error) {
    console.error(error);
    return [];
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search-input");
  const emptyState = document.getElementById("empty-state");

  async function performSearch(query) {
    const results = await fetchResults(query);
    emptyState.textContent = "Aucun résultat trouvé.";
    renderResults(results);
  }

  // Pas de debounce : chaque frappe déclenche un appel réseau. Volontairement
  // simple ici, mais à surveiller si le catalogue devient volumineux.
  input.addEventListener("input", () => {
    performSearch(input.value.trim());
  });

  // Charge le catalogue complet au chargement de la page (query vide).
  performSearch("");

  const overlay = document.getElementById("details-overlay");
  document.getElementById("details-close").addEventListener("click", closeDetailsModal);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) closeDetailsModal();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !overlay.hidden) closeDetailsModal();
  });
});
