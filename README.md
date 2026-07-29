# HBntory

HBntory est une application de gestion de stock et de catalogue produits pensée comme un projet multi-services. Elle combine un backoffice interne, une API externe de produits, un assistant IA et une interface web simple pour permettre la recherche, la consultation et la gestion du stock par succursale.

## Objectif du projet

Le but de cette plateforme est de fournir une vue unifiée sur :

- les produits disponibles dans un catalogue externe,
- le stock réel disponible dans différentes succursales,
- les opérations de gestion interne via un backoffice,
- une assistance IA permettant d’interroger le catalogue en langage naturel.

## Fonctionnalités principales

- Recherche de produits et de stock par succursale
- Authentification et rôles utilisateur (admin / employé)
- Gestion du stock côté backoffice
- API externe de catalogue produits
- Assistant IA via un serveur MCP et un agent conversationnel
- Interface web simple et autonome sans framework frontend lourd

## Architecture générale

Le projet est organisé autour de plusieurs services :

- Backoffice : application Flask pour la gestion interne, l’authentification et le stock
- API externe : service simulant un catalogue fournisseur
- Product MCP Server : service IA basé sur un agent et un outil MCP pour interroger le catalogue
- Client web : interface HTML/CSS/JS pour l’usage utilisateur

## Structure du dépôt

```text
hbntory/
├── api_extern/             # API externe de produits
├── backoffice/             # application Flask de gestion interne
├── client_web/             # interface web statique
├── docs/                   # documentation complémentaire
├── product_mcp_server/     # serveur MCP + agent IA
├── dev.sh                  # script de lancement de la stack complète
└── README.md               # ce fichier
```

## Prérequis

Avant de lancer le projet, il est recommandé d’avoir :

- Python 3.10+
- Docker et Docker Compose
- un environnement virtuel Python
- Ollama installé si vous souhaitez utiliser l’assistant IA de bout en bout

## Démarrage rapide

Depuis la racine du projet, vous pouvez lancer toute la stack avec :

```bash
./dev.sh
```

Ce script démarre en parallèle :

- l’API externe sur le port 5001,
- le backoffice sur le port 5050,
- le serveur MCP / agent IA sur le port 8000,
- le client web sur le port 8080.

## Accès locaux

Une fois la stack lancée :

- Interface web : http://localhost:8080
- Backoffice API : http://localhost:5050
- API externe produits : http://localhost:5001
- Service IA : http://localhost:8000

## Utilisation du front office

L’interface web permet :

- de consulter le catalogue public,
- de rechercher des produits et leur disponibilité,
- de chatter avec l’assistant IA,
- de se connecter en tant qu’admin ou employé selon les droits.

Comptes de test fournis par le backoffice :

- admin@hbntory.com / admin123
- employee@hbntory.com / employee123

## Développement par service

### Backoffice

Le backoffice est une API Flask qui gère :

- l’authentification,
- les utilisateurs,
- le stock,
- la recherche croisée avec le catalogue externe.

Pour plus de détails, voir le dossier [backoffice](backoffice).

### API externe

L’API externe simule un catalogue fournisseur et fournit les produits, catégories et fournisseurs. Elle est pensée pour être consommée par le backoffice et l’interface web.

Pour plus de détails, voir le dossier [api_extern](api_extern).

### Product MCP Server

Ce module expose un assistant IA capable de répondre à des questions naturelles sur les produits grâce à un outil MCP et un agent orchestré.

Pour plus de détails, voir le dossier [product_mcp_server](product_mcp_server).

### Client web

Le client web est une interface statique en HTML/CSS/JS sans build système. Elle sert de point d’entrée utilisateur pour consulter l’application.

Pour plus de détails, voir le dossier [client_web](client_web).

## Notes importantes

- Le projet est volontairement multi-services pour illustrer une architecture modulaire.
- L’API externe est conçue pour être consommée par d’autres composants, sans être modifiée directement.
- Selon l’environnement Python/OpenSSL utilisé, le login du backoffice peut rencontrer un problème lié au hashage des mots de passe. Ce point est à vérifier côté backend si vous rencontrez des erreurs d’authentification.

## Contribution

Si vous souhaitez étendre le projet, vous pouvez :

- ajouter de nouvelles routes et services dans le backoffice,
- enrichir l’API externe avec de nouveaux produits ou endpoints,
- améliorer l’agent IA avec de nouveaux outils ou scénarios,
- améliorer l’interface web avec de nouveaux écrans ou workflows.
