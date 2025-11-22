#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point d'entrée principal de l'application Image Processor.
"""

import sys
import os

# Ajouter le répertoire parent au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Maintenant, nous pouvons importer le module image_processor
from image_processor.main import main

if __name__ == "__main__":
    main()
