#!/bin/bash

# Script d'aide pour lancer l'application Image Processor avec Docker
# Compatible Linux, macOS et WSL2

set -e

echo "🚀 Image Processor - Lancement avec Docker"
echo "=========================================="

# Détection du système d'exploitation
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Système détecté: Linux"
    DISPLAY_VAR="${DISPLAY:-:0}"
    
    # Autoriser l'accès X11
    echo "🔓 Autorisation de l'accès X11..."
    xhost +local:docker 2>/dev/null || echo "⚠️  xhost peut nécessiter des permissions sudo"
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Système détecté: macOS"
    DISPLAY_VAR="host.docker.internal:0"
    
    # Vérifier si XQuartz est installé
    if ! command -v xquartz &> /dev/null; then
        echo "⚠️  XQuartz n'est pas installé. Installation recommandée:"
        echo "   brew install --cask xquartz"
    fi
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "📦 Système détecté: Windows (WSL2/Cygwin)"
    # Pour WSL2, récupérer l'IP du serveur X
    DISPLAY_VAR=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
    echo "🖥️  Display: $DISPLAY_VAR"
else
    echo "⚠️  Système non reconnu, utilisation de DISPLAY par défaut"
    DISPLAY_VAR="${DISPLAY:-:0}"
fi

# Créer le dossier images s'il n'existe pas
mkdir -p images

echo ""
echo "🔨 Construction de l'image Docker..."
docker build -t image-processor:latest .

echo ""
echo "▶️  Lancement de l'application..."
echo "   Display: $DISPLAY_VAR"
echo ""

# Lancer avec docker-compose si disponible, sinon avec docker run
if command -v docker-compose &> /dev/null; then
    DISPLAY=$DISPLAY_VAR docker-compose up --build
else
    echo "⚠️  docker-compose non trouvé, utilisation de docker run"
    docker run -it --rm \
        -e DISPLAY=$DISPLAY_VAR \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -v "$(pwd)/images:/app/images:rw" \
        -v "$HOME:/host/home:rw" \
        -v "$(pwd):/host/project:rw" \
        --network host \
        image-processor:latest
fi

echo ""
echo "✅ Application fermée"

