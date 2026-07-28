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
    qtyCell.textContent = item.quantity;

    row.append(skuCell, branchCell, qtyCell);
    tbody.appendChild(row);
  });
}

function renderEmployees(employees) {
  const tbody = document.getElementById("employees-body");
  const emptyState = document.getElementById("employees-empty");
  tbody.innerHTML = "";

  emptyState.hidden = employees.length > 0;

  employees.forEach((user) => {
    const row = document.createElement("tr");

    const emailCell = document.createElement("td");
    emailCell.textContent = user.email;

    const branchCell = document.createElement("td");
    branchCell.textContent = user.branch_id ?? "-";

    const actionsCell = document.createElement("td");
    const deleteBtn = document.createElement("button");
    deleteBtn.type = "button";
    deleteBtn.className = "link-btn link-btn--danger";
    deleteBtn.textContent = "Supprimer";
    deleteBtn.addEventListener("click", () => deleteEmployee(user.id));
    actionsCell.appendChild(deleteBtn);

    row.append(emailCell, branchCell, actionsCell);
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

async function loadEmployees() {
  try {
    const users = await apiFetch("/api/users/");
    renderEmployees(users.filter((user) => user.role === "employee"));
  } catch (error) {
    console.error(error);
  }
}

async function deleteEmployee(userId) {
  if (!window.confirm("Supprimer cet employé ?")) return;

  try {
    await apiFetch(`/api/users/${userId}`, { method: "DELETE" });
    loadEmployees();
  } catch (error) {
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const session = requireSession("admin");
  if (!session) return;

  document.getElementById("logout-btn").addEventListener("click", () => {
    clearSession();
    window.location.href = "login.html";
  });

  const addForm = document.getElementById("add-employee-form");
  const errorEl = document.getElementById("employee-error");

  addForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorEl.hidden = true;

    const identifier = document.getElementById("employee-identifier").value.trim();
    const password = document.getElementById("employee-password").value;
    const branchValue = document.getElementById("employee-branch").value;

    if (!identifier.includes("@") && identifier.length > 12) {
      errorEl.textContent = "Un nom (sans email) ne doit pas dépasser 12 caractères.";
      errorEl.hidden = false;
      return;
    }

    try {
      await apiFetch("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email: identifier,
          password,
          role: "employee",
          branch_id: branchValue ? Number(branchValue) : null,
        }),
      });
      addForm.reset();
      loadEmployees();
    } catch (error) {
      errorEl.textContent = "Impossible d'ajouter l'employé (email déjà utilisé ?).";
      errorEl.hidden = false;
    }
  });

  loadStock();
  loadEmployees();
});
