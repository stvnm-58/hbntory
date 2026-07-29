// Contrôleur de stock.html (rôle "employee") : CRUD complet sur le stock, à
// la différence de admin.js qui n'affiche le stock qu'en lecture seule.

function renderStock(stocks) {
  const tbody = document.getElementById("stock-body");
  const emptyState = document.getElementById("stock-empty");
  tbody.innerHTML = "";

  emptyState.hidden = stocks.length > 0;

  stocks.forEach((item) => {
    const row = document.createElement("tr");

    const skuCell = document.createElement("td");
    skuCell.textContent = item.product_sku;

    const branchCell = document.createElement("td");
    branchCell.textContent = item.branch_id;

    const qtyCell = document.createElement("td");
    const qtyInput = document.createElement("input");
    qtyInput.type = "number";
    qtyInput.min = "0";
    qtyInput.value = item.quantity;
    qtyInput.className = "qty-input";
    qtyInput.addEventListener("change", () => updateQuantity(item.id, qtyInput));
    qtyCell.appendChild(qtyInput);

    const actionsCell = document.createElement("td");
    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "link-btn link-btn--danger";
    deleteBtn.textContent = "Supprimer";
    deleteBtn.addEventListener("click", () => deleteStock(item.id));
    actionsCell.appendChild(deleteBtn);

    row.append(skuCell, branchCell, qtyCell, actionsCell);
    tbody.appendChild(row);
  });
}

async function loadStock() {
  try {
    const stocks = await apiFetch("/api/stocks/");
    renderStock(stocks);
  } catch (error) {
    console.error(error);
  }
}

async function updateQuantity(stockId, input) {
  try {
    await apiFetch(`/api/stocks/${stockId}`, {
      method: "PUT",
      body: JSON.stringify({ quantity: Number(input.value) }),
    });
  } catch (error) {
    console.error(error);
    // En cas d'échec, on recharge depuis le serveur pour annuler la valeur
    // tapée localement et éviter que l'UI affiche une quantité non persistée.
    loadStock();
  }
}

async function deleteStock(stockId) {
  if (!window.confirm("Supprimer cet article du stock ?")) return;

  try {
    await apiFetch(`/api/stocks/${stockId}`, { method: "DELETE" });
    loadStock();
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const session = requireSession("employee");
  if (!session) return;

  document.getElementById("logout-btn").addEventListener("click", () => {
    clearSession();
    window.location.href = "index.html";
  });

  const addForm = document.getElementById("add-stock-form");
  const errorEl = document.getElementById("stock-error");

  addForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorEl.hidden = true;

    const product_sku = document.getElementById("stock-sku").value.trim();
    const branch_id = Number(document.getElementById("stock-branch").value);
    const quantity = Number(document.getElementById("stock-quantity").value || 0);

    try {
      await apiFetch("/api/stocks/", {
        method: "POST",
        body: JSON.stringify({ product_sku, branch_id, quantity }),
      });
      addForm.reset();
      document.getElementById("stock-quantity").value = "0";
      loadStock();
    } catch (error) {
      errorEl.textContent = "Impossible d'ajouter l'article.";
      errorEl.hidden = false;
    }
  });

  loadStock();
});
