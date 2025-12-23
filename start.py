#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de démarrage pour l'application Image Processor.
"""

import sys
import os

# Ajouter le répertoire courant au chemin de recherche Python
sys.path.insert(0, os.path.abspath('.'))

# Importer et exécuter le main
from image_processor.main import main

if __name__ == "__main__":
    main()
