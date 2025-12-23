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
        
        root.minsize(1000, 700)
        
        app = MainWindow(root)
        
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 5])
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        raise

if __name__ == "__main__":
    main()
