document.addEventListener("DOMContentLoaded", () => {
  const existing = getSession();
  if (existing) {
    window.location.href = existing.user.role === "admin" ? "admin.html" : "stock.html";
    return;
  }

  const form = document.getElementById("login-form");
  const errorEl = document.getElementById("login-error");
  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorEl.hidden = true;

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    submitButton.disabled = true;

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Identifiants invalides.");
      }

      setSession({ token: data.token, user: data.user });
      window.location.href = data.user.role === "admin" ? "admin.html" : "stock.html";
    } catch (error) {
      errorEl.textContent = error.message;
      errorEl.hidden = false;
    } finally {
      submitButton.disabled = false;
    }
  });
});
