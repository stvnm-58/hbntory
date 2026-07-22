// TODO: remplacer par l'URL du serveur MCP (HTTP) fourni par l'équipe backend.
// Exemple : "http://localhost:8000"
const API_BASE_URL = "";

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    throw new Error(`Erreur API (${response.status}) sur ${path}`);
  }

  return response.json();
}
