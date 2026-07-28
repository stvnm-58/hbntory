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

function requireSession(role) {
  const session = getSession();

  if (!session) {
    window.location.href = "login.html";
    return null;
  }

  if (role && session.user.role !== role) {
    window.location.href = session.user.role === "admin" ? "admin.html" : "stock.html";
    return null;
  }

  return session;
}

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
    window.location.href = "login.html";
    throw new Error("Session expirée, veuillez vous reconnecter.");
  }

  if (!response.ok) {
    throw new Error(`Erreur API (${response.status}) sur ${path}`);
  }

  return response.json();
}
