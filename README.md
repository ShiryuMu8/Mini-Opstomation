# Mini Opstomation

Projet créé avant un entretien chez Adeo pour comprendre et illustrer
la logique de leur outil **Opstomation** — réparer les serveurs automatiquement
sans intervention humaine.

---

## Le lien avec Adeo

Chez Adeo, l'équipe Event & Response traite 168 000 incidents par an grâce à Opstomation.
Quand un serveur plante, un script le répare tout seul.

Ce projet simule cette logique en miniature :
- détecter un incident → `/incidents`
- le réparer automatiquement → `/fix/<id>`
- vérifier que le service tourne → `/health`

En vrai chez Adeo : **ArgoWorkflow** déclenche le pipeline de réparation,
**Ansible** exécute les scripts sur les serveurs.

---

## Stack technique

- **Python + Flask** — l'API
- **Docker + Docker Compose** — la conteneurisation (base de Kubernetes)
- **GitHub Actions** — le pipeline CI/CD (équivalent d'ArgoWorkflow)

---

## Lancer le projet

### Avec Docker Compose
```bash
docker compose up --build
```

### Sans Docker
```bash
pip install -r requirements.txt
python app.py
```

L'API tourne sur `http://localhost:5000`

---

## Les routes

| Route | Méthode | Description |
|-------|---------|-------------|
| `/health` | GET | Vérifie que l'API tourne |
| `/incidents` | GET | Liste tous les incidents |
| `/fix/<id>` | POST | Répare automatiquement un incident |

---

## Lancer les tests

```bash
pytest test_app.py -v
```

---

## Le pipeline CI/CD

À chaque push sur `main`, GitHub Actions exécute automatiquement :

1. **Lint** — vérifie la qualité du code avec flake8
2. **Tests** — lance pytest, bloque le déploiement si un test échoue
3. **Build Docker** — construit l'image et vérifie que le conteneur démarre

C'est la même logique qu'ArgoWorkflow chez Adeo, avec GitHub Actions.