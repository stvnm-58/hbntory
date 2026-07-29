// Contrôleur de la page de connexion (index.html). Dépend de app.js chargé
// avant lui (API_BASE_URL, getSession/setSession).

document.addEventListener("DOMContentLoaded", () => {
  // Si une session existe déjà, on saute directement le formulaire pour
  // éviter de reconnecter un utilisateur déjà authentifié.
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

    const identifier = document.getElementById("identifier").value.trim();
    const password = document.getElementById("password").value;

    submitButton.disabled = true;

    try {
      // Appel direct (pas apiFetch) : il n'y a pas encore de session/token à
      // ce stade, et une erreur ici doit rester sur la page plutôt que
      // rediriger vers index.html comme le ferait apiFetch sur un 401.
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: identifier, password }),
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
