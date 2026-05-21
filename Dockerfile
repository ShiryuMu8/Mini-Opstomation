# On part d'une image Python officielle légère (slim = sans les outils inutiles)
# Chez Adeo : les images Docker doivent être légères pour déployer vite
FROM python:3.11-slim

# On définit le dossier de travail dans le conteneur
# Tous les fichiers copiés et commandes exécutées seront ici
WORKDIR /app

# On copie d'abord uniquement le fichier des dépendances
# Astuce : si app.py change mais pas requirements.txt,
# Docker réutilise le cache et ne réinstalle pas tout
COPY requirements.txt .

# On installe les dépendances Python dans le conteneur
# --no-cache-dir : évite de stocker le cache pip dans l'image = image plus légère
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le reste du code dans le conteneur
COPY . .

# On indique que l'application écoute sur le port 5000
# C'est juste de la documentation, ça n'ouvre pas réellement le port
EXPOSE 5000

# La commande qui démarre l'API quand le conteneur se lance
CMD ["python", "app.py"]