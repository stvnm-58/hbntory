# Client Web

Interface web du projet HBntory : recherche de produits/stock, assistant IA en chat flottant, et un espace authentifié (admin / employé) pour la gestion du stock et des employés.

HTML / CSS / JS simple, sans framework ni dépendance, sans étape de build.

## Structure

```
client_web/
├── index.html                 # connexion (email/nom + mot de passe) — page servie à la racine "/"
├── catalogue.html              # page publique : recherche + chat (pas de connexion requise)
├── admin.html                    # espace admin : stock en lecture seule + gestion des employés
├── stock.html                     # espace employé : stock avec ajout / modification / suppression
├── css/
│   └── style.css                   # feuille de style unique, partagée par toutes les pages
├── js/
│   ├── app.js                       # config partagée (API_BASE_URL), apiFetch, gestion de session
│   ├── auth.js                       # formulaire de connexion (index.html)
│   ├── search.js                      # tableau de résultats de recherche (catalogue.html)
│   ├── chat.js                         # bulle déplaçable + panneau de chat (catalogue.html)
│   ├── admin.js                         # stock en lecture seule + CRUD employés (admin.html)
│   └── stock-manager.js                  # CRUD stock (stock.html)
└── assets/                            # vide pour l'instant (images, icônes…)
```

Chaque page HTML charge `js/app.js` en premier (il définit `API_BASE_URL` et les helpers de session utilisés par tous les autres scripts), suivi du/des script(s) propre(s) à la page.

## Lancer en local

Le plus simple est de lancer toute la stack depuis la racine du projet :

```bash
./dev.sh
```

Ça démarre en parallèle `api_extern` (Docker, port 5001), `backoffice` (port 5050), `product_mcp_server` (port 8000) et ce dossier `client_web` via :

```bash
python3 -m http.server 8080
```

Puis ouvrir `http://localhost:8080` dans un navigateur.

## Pages et rôles

| Page | Accès | Rôle requis | Contenu |
|---|---|---|---|
| `index.html` | public | aucun | connexion, redirige selon le rôle après succès |
| `catalogue.html` | public | aucun | recherche produits/stock + chat IA |
| `admin.html` | authentifié | `admin` | stock en **lecture seule** + liste des employés (ajout / suppression) |
| `stock.html` | authentifié | `employee` | stock en **lecture/écriture** (ajout, modification de quantité, suppression) |

Un admin ne peut pas modifier le stock directement — seulement consulter et gérer les comptes employés. Un employé ne voit pas la gestion des employés — seulement le stock, avec droit d'écriture complet.

**Navigation entre les pages** : `catalogue.html` a un lien vers `index.html` (« Connexion »), et `index.html` a un lien retour vers `catalogue.html` (« Consulter le stock sans compte »). `index.html` étant le fichier servi à la racine du site (`/`), c'est la page de connexion qui s'affiche par défaut sur `http://localhost:8080/`, avec un accès direct au catalogue public pour les visiteurs sans compte.

### Connexion

Le champ « Identifiant » accepte un email ou un nom d'utilisateur libre. Un nom (sans `@`) est limité à 12 caractères ; un email n'a pas de limite de longueur.

Comptes de test (créés par `backoffice/database/seed.py`) :

| Identifiant | Mot de passe | Rôle |
|---|---|---|
| `admin@hbntory.com` | `admin123` | admin |
| `employee@hbntory.com` | `employee123` | employee |

### Session

Après connexion, `js/app.js` stocke `{ token, user }` dans `localStorage` (clé `hbntory_auth`). Toutes les requêtes faites via `apiFetch` (dans `app.js`) attachent automatiquement le header `Authorization: Bearer <token>` si une session existe, et redirigent vers `index.html` en cas de réponse `401`.

`requireSession(role)` (dans `app.js`) protège `admin.html` et `stock.html` : sans session valide ou avec le mauvais rôle, l'utilisateur est redirigé vers la page appropriée (`index.html`, `admin.html` ou `stock.html`).

## Exemples de questions (chat)

- **Détails produit** : « Donne-moi les détails du produit XX. »
- **Disponibilité par succursale** : « Quelle succursale a le stock du produit X ? »
- **Produits d'une succursale** : « Quels produits puis-je trouver dans la succursale Y ? »
- **Liste d'achats** : « Si je veux acheter 3 unités de X, 2 unités de Y et 4 unités de Z, quelle(s) succursale(s) devrais-je visiter ? »

## État de l'intégration

- La recherche (`js/search.js`, sur `catalogue.html`) appelle `GET /api/search` sur le backoffice (`API_BASE_URL`, port 5050) ; un champ vide renvoie tout le catalogue, trié par nom. Le backoffice relaie lui-même vers l'API produits externe (`api_extern`, port 5001) puis croise avec le stock local.
- Le chat (`js/chat.js`, sur `catalogue.html`) appelle `POST /ask` sur `product_mcp_server` (`AI_SERVICE_URL`, port 8000, en dur dans le fichier).
- La connexion (`js/auth.js`), le stock (`js/admin.js`, `js/stock-manager.js`) et les employés (`js/admin.js`) passent tous par le backoffice via `apiFetch` (`/api/auth`, `/api/stocks`, `/api/users`).

Les trois services (`backoffice`, `api_extern`, `product_mcp_server`) doivent tourner en parallèle pour que le front soit pleinement fonctionnel — voir `./dev.sh` à la racine du projet.

### Bug backend connu (bloquant pour le login)

Le hashing des mots de passe (`werkzeug.security.check_password_hash`, côté `backoffice`) utilise `scrypt` par défaut, qui n'est pas supporté par la version d'OpenSSL/LibreSSL de l'environnement Python actuel — le login échoue avec `AttributeError: module 'hashlib' has no attribute 'scrypt'`. Rien à corriger côté front : ce point est purement backend (voir `backoffice/models/user.py`), et pas encore résolu au moment de la rédaction de ce README.
