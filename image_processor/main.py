#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Processor - Application principale
Un outil interactif pour le traitement d'images avec interface graphique.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ajouter le répertoire courant au chemin de recherche Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import des modules personnalisés
from gui.main_window import MainWindow

def main():
    """Point d'entrée principal de l'application."""
    try:
        # Création de la fenêtre principale
        root = tk.Tk()
        root.title("Image Processor - Traitement d'images")
        
        # Configuration de la taille minimale de la fenêtre
        root.minsize(1000, 700)
        
        # Création de l'interface utilisateur
        app = MainWindow(root)
        
        # Configuration du style
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 5])
        
        # Démarrage de la boucle principale
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        raise

if __name__ == "__main__":
    main()
