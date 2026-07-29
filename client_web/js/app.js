// Chargé en premier sur chaque page : config partagée + helpers de session/API
// utilisés ensuite par auth.js, search.js, chat.js, admin.js et stock-manager.js.

// Doit correspondre au port sur lequel tourne backoffice/app.py (voir dev.sh).
const API_BASE_URL = "http://localhost:5050";
const AUTH_STORAGE_KEY = "hbntory_auth";

function getSession() {
  const raw = localStorage.getItem(AUTH_STORAGE_KEY);
  if (!raw) return null;

  try {
    return JSON.parse(raw);
  } catch (error) {
    return null;
  }
}

function setSession(session) {
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(session));
}

function clearSession() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
}

// Garde d'accès appelée au chargement de admin.html/stock.html : redirige vers
// index.html si personne n'est connecté, ou vers l'espace correspondant si le
// rôle connecté ne correspond pas à celui attendu par la page.
function requireSession(role) {
  const session = getSession();

  if (!session) {
    window.location.href = "index.html";
    return null;
  }

  if (role && session.user.role !== role) {
    window.location.href = session.user.role === "admin" ? "admin.html" : "stock.html";
    return null;
  }

  return session;
}

// Wrapper fetch commun à tout le front : préfixe API_BASE_URL, attache le
// token JWT s'il y en a un, et déconnecte automatiquement sur un 401 (token
// expiré ou invalide) pour éviter de laisser l'utilisateur sur un état cassé.
async function apiFetch(path, options = {}) {
  const session = getSession();

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(session ? { Authorization: `Bearer ${session.token}` } : {}),
      ...(options.headers || {}),
    },
  });

  if (response.status === 401) {
    clearSession();
    window.location.href = "index.html";
    throw new Error("Session expirée, veuillez vous reconnecter.");
  }

  if (!response.ok) {
    throw new Error(`Erreur API (${response.status}) sur ${path}`);
  }

  return response.json();
}
