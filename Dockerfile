# Image de base Python avec support GUI
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Image Processor Team"
LABEL description="Application de traitement d'images avec interface graphique"

# Variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:0

# Installation des dépendances système pour Tkinter et OpenCV
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgtk-3-0 \
    libgthread-2.0-0 \
    x11-apps \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY image_processor/ ./image_processor/
COPY start_app.py .

# Créer un répertoire pour les images (montage optionnel)
RUN mkdir -p /app/images

# Exposer le port X11 (optionnel, pour debug)
# EXPOSE 6000

# Point d'entrée
ENTRYPOINT ["python", "start_app.py"]

