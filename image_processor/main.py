"""
Image Processor - Application principale
Un outil interactif pour le traitement d'images avec interface graphique.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from gui.main_window import MainWindow

def main():
    """Point d'entrée principal de l'application."""
    try:
        root = tk.Tk()
        root.title("Image Processor - Traitement d'images")
        
        # Configuration de la fenêtre
        root.minsize(1000, 700)
        root.configure(bg='#F5F8FA')  # Fond gris-bleu très doux
        
        # Créer l'application
        app = MainWindow(root)
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        raise

if __name__ == "__main__":
    main()
