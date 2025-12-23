#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de démarrage simplifié pour l'application Image Processor.
"""

import sys
import os
from tkinter import Tk

# Ajouter le répertoire courant au chemin de recherche Python
sys.path.insert(0, os.path.abspath('.'))

# Importer l'application
from image_processor.gui.main_window import MainWindow

def main():
    """Point d'entrée principal de l'application."""
    try:
        # Création de la fenêtre principale
        root = Tk()
        root.title("Image Processor - Traitement d'images")
        
        # Configuration de la taille minimale de la fenêtre
        root.minsize(1000, 700)
        
        # Création de l'interface utilisateur
        app = MainWindow(root)
        
        # Démarrage de la boucle principale
        root.mainloop()
        
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
