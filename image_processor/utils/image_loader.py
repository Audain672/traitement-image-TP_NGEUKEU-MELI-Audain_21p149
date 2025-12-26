"""
Module utilitaire pour le chargement et la sauvegarde d'images.
"""

import os
import cv2
import numpy as np
from typing import Tuple, Optional

def is_image_file(filename: str) -> bool:
    """
    Vérifie si le fichier est une image supportée.
    
    Args:
        filename (str): Chemin vers le fichier
        
    Returns:
        bool: True si le fichier est une image supportée, False sinon
    """
    if not os.path.isfile(filename):
        return False
    
    # Extensions d'images supportées
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']
    
    # Vérifier l'extension du fichier
    _, ext = os.path.splitext(filename.lower())
    return ext in image_extensions

def load_image(
    filepath: str, 
    mode: str = 'color', 
    target_size: Optional[Tuple[int, int]] = None
) -> Tuple[np.ndarray, str]:
    """
    Charge une image à partir d'un fichier.
    
    Args:
        filepath (str): Chemin vers le fichier image
        mode (str): Mode de chargement ('color', 'grayscale' ou 'unchanged')
        target_size (tuple, optional): Taille cible (largeur, hauteur)
        
    Returns:
        tuple: (image, error_message) où error_message est None si succès
    """
    if not os.path.exists(filepath):
        return None, f"Le fichier n'existe pas: {filepath}"
    
    if not is_image_file(filepath):
        return None, "Format d'image non supporté"
    
    try:
        # Déterminer le mode de chargement OpenCV
        if mode == 'color':
            flags = cv2.IMREAD_COLOR
        elif mode == 'grayscale':
            flags = cv2.IMREAD_GRAYSCALE
        else:  # 'unchanged'
            flags = cv2.IMREAD_UNCHANGED
        
        # Charger l'image
        image = cv2.imread(filepath, flags)
        
        if image is None:
            return None, "Impossible de charger l'image. Format non supporté ou fichier corrompu."
        
        # Convertir de BGR à RGB si c'est une image couleur
        if mode == 'color' and len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Redimensionner si nécessaire
        if target_size is not None and len(target_size) == 2:
            image = cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
        
        return image, None
        
    except Exception as e:
        return None, f"Erreur lors du chargement de l'image: {str(e)}"

def save_image(
    image: np.ndarray, 
    filepath: str, 
    quality: int = 95,
    convert_to_bgr: bool = True
) -> str:
    """
    Enregistre une image dans un fichier.
    
    Args:
        image (numpy.ndarray): Image à enregistrer
        filepath (str): Chemin de destination
        quality (int): Qualité de l'image (0-100)
        convert_to_bgr (bool): Si True, convertit de RGB à BGR avant l'enregistrement
        
    Returns:
        str: Message d'erreur ou None si succès
    """
    if image is None:
        return "Aucune image à enregistrer"
    
    try:
        # Créer le répertoire parent si nécessaire
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # Convertir en BGR si nécessaire (pour la compatibilité avec OpenCV)
        save_image = image.copy()
        if convert_to_bgr and len(save_image.shape) == 3 and save_image.shape[2] == 3:
            save_image = cv2.cvtColor(save_image, cv2.COLOR_RGB2BGR)
        
        # Déterminer l'extension du fichier
        _, ext = os.path.splitext(filepath.lower())
        
        # Paramètres de compression en fonction du format
        params = []
        if ext in ['.jpg', '.jpeg']:
            params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        elif ext == '.png':
            # Pour PNG, la qualité est un nombre entre 0 et 9 (compression sans perte)
            png_quality = min(9, max(0, int((100 - quality) / 10)))
            params = [cv2.IMWRITE_PNG_COMPRESSION, png_quality]
        
        # Enregistrer l'image
        success = cv2.imwrite(filepath, save_image, params)
        
        if not success:
            return "Échec de l'enregistrement de l'image"
            
        return None
        
    except Exception as e:
        return f"Erreur lors de l'enregistrement de l'image: {str(e)}"

def load_image_for_display(
    filepath: str, 
    max_size: Optional[Tuple[int, int]] = None
) -> Tuple[np.ndarray, str]:
    """
    Charge une image pour l'affichage dans une interface utilisateur.
    
    Args:
        filepath (str): Chemin vers le fichier image
        max_size (tuple, optional): Taille maximale (largeur, hauteur)
        
    Returns:
        tuple: (image, error_message) où error_message est None si succès
    """
    image, error = load_image(filepath, mode='color')
    
    if error:
        return None, error
    
    # Redimensionner si nécessaire pour l'affichage
    if max_size is not None and len(max_size) == 2:
        h, w = image.shape[:2]
        max_w, max_h = max_size
        
        # Calculer les nouvelles dimensions en conservant le ratio
        if w > max_w or h > max_h:
            ratio = min(max_w / w, max_h / h)
            new_size = (int(w * ratio), int(h * ratio))
            image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    
    return image, None

def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convertit une image en niveaux de gris.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR ou RGB)
        
    Returns:
        numpy.ndarray: Image en niveaux de gris
    """
    if len(image.shape) == 2:
        return image.copy()
    
    if image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    
    return image
