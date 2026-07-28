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
    succursaleCell.textContent = item.branch_name;

    const quantiteCell = document.createElement("td");
    quantiteCell.textContent = item.quantity;

    const detailsCell = document.createElement("td");
    const detailsBtn = document.createElement("button");
    detailsBtn.type = "button";
    detailsBtn.className = "link-btn";
    detailsBtn.textContent = "Voir";
    detailsBtn.dataset.id = item.sku;
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

  async function performSearch(query) {
    const results = await fetchResults(query);
    emptyState.textContent = "Aucun résultat trouvé.";
    renderResults(results);
  }

  input.addEventListener("input", () => {
    performSearch(input.value.trim());
  });

  performSearch("");
});
