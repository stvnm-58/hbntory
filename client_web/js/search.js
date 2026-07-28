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
    produitCell.textContent = item.produit;

    const succursaleCell = document.createElement("td");
    succursaleCell.textContent = item.id;

    const quantiteCell = document.createElement("td");
    quantiteCell.textContent = item.quantite;

    const detailsCell = document.createElement("td");
    const detailsBtn = document.createElement("button");
    detailsBtn.type = "button";
    detailsBtn.className = "link-btn";
    detailsBtn.textContent = "Voir";
    detailsBtn.dataset.id = item.id;
    detailsCell.appendChild(detailsBtn);

    row.append(produitCell, succursaleCell, quantiteCell, detailsCell);
    tbody.appendChild(row);
  });
}

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

  input.addEventListener("input", async () => {
    const query = input.value.trim();

    if (!query) {
      emptyState.textContent = "Aucun résultat pour l'instant. Lancez une recherche.";
      renderResults([]);
      return;
    }

    const results = await fetchResults(query);
    if (!results.length) {
      emptyState.textContent = "Aucun résultat trouvé.";
    }
    renderResults(results);
  });
});
