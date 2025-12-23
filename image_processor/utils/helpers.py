""
Module contenant des fonctions utilitaires pour le traitement d'images.
"""

import os
import cv2
import numpy as np
from typing import Tuple, Union, List, Optional

def get_image_info(image: np.ndarray) -> dict:
    """
    Récupère les informations de base d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        
    Returns:
        dict: Dictionnaire contenant les informations de l'image
    """
    if image is None:
        return {
            'width': 0,
            'height': 0,
            'channels': 0,
            'dtype': 'None',
            'size': '0 bytes',
            'min': 0,
            'max': 0,
            'mean': 0,
            'std': 0
        }
    
    height, width = image.shape[:2]
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    
    # Calcul des statistiques
    min_val = np.min(image)
    max_val = np.max(image)
    mean_val = np.mean(image)
    std_val = np.std(image)
    
    # Taille en mémoire
    size_bytes = image.nbytes
    size_str = format_size(size_bytes)
    
    return {
        'width': width,
        'height': height,
        'channels': channels,
        'dtype': str(image.dtype),
        'size': size_str,
        'min': float(min_val),
        'max': float(max_val),
        'mean': float(mean_val),
        'std': float(std_val)
    }

def format_size(size_in_bytes: int) -> str:
    """
    Formate une taille en octets dans une chaîne lisible.
    
    Args:
        size_in_bytes (int): Taille en octets
        
    Returns:
        str: Taille formatée (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f} PB"

def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalise les valeurs de l'image entre 0 et 255.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        
    Returns:
        numpy.ndarray: Image normalisée (type uint8)
    """
    if image.dtype == np.uint8:
        return image.copy()
    
    # Convertir en flottant pour les calculs
    img_float = image.astype(np.float32)
    
    # Normaliser entre 0 et 1
    min_val = np.min(img_float)
    max_val = np.max(img_float)
    
    if max_val > min_val:
        img_norm = (img_float - min_val) / (max_val - min_val)
    else:
        img_norm = np.zeros_like(img_float)
    
    # Mettre à l'échelle à 0-255 et convertir en entier non signé 8 bits
    return (img_norm * 255).astype(np.uint8)

def overlay_image(background: np.ndarray, overlay: np.ndarray, x: int, y: int, alpha: float = 0.7) -> np.ndarray:
    """
    Superpose une image sur une autre avec transparence.
    
    Args:
        background (numpy.ndarray): Image de fond
        overlay (numpy.ndarray): Image à superposer
        x (int): Position x du coin supérieur gauche
        y (int): Position y du coin supérieur gauche
        alpha (float): Niveau de transparence (0.0 - 1.0)
        
    Returns:
        numpy.ndarray: Image résultante
    """
    # Faire une copie de l'image de fond
    result = background.copy()
    
    # Dimensions de l'image à superposer
    h, w = overlay.shape[:2]
    
    # Zone de l'image de fond où l'overlay sera placé
    y1, y2 = max(0, y), min(background.shape[0], y + h)
    x1, x2 = max(0, x), min(background.shape[1], x + w)
    
    # Si l'overlay dépasse les bords de l'image de fond
    if x1 >= x2 or y1 >= y2:
        return result
    
    # Découper l'overlay si nécessaire
    overlay_cropped = overlay[
        0:y2-y1 if y >= 0 else h+(y2-y1),
        0:x2-x1 if x >= 0 else w+(x2-x1)
    ]
    
    # Zone de destination dans l'image de fond
    bg_region = result[y1:y2, x1:x2]
    
    # Si l'overlay a un canal alpha
    if overlay_cropped.shape[2] == 4:
        # Extraire le masque alpha et normaliser
        alpha_mask = overlay_cropped[:, :, 3] / 255.0
        alpha_mask = alpha_mask[..., np.newaxis]
        
        # Fusionner avec transparence
        for c in range(3):
            bg_region[:, :, c] = (
                (1 - alpha * alpha_mask) * bg_region[:, :, c] + 
                alpha * alpha_mask * overlay_cropped[:, :, c]
            )
    else:
        # Fusionner sans canal alpha
        for c in range(3):
            bg_region[:, :, c] = (
                (1 - alpha) * bg_region[:, :, c] + 
                alpha * overlay_cropped[:, :, c]
            )
    
    result[y1:y2, x1:x2] = bg_region
    return result

def draw_text(
    image: np.ndarray, 
    text: str, 
    position: Tuple[int, int], 
    font_scale: float = 1.0,
    color: Tuple[int, int, int] = (255, 255, 255),
    thickness: int = 2,
    bg_color: Optional[Tuple[int, int, int]] = None,
    padding: int = 5
) -> np.ndarray:
    """
    Dessine du texte sur une image avec un fond optionnel.
    
    Args:
        image (numpy.ndarray): Image sur laquelle dessiner
        text (str): Texte à dessiner
        position (tuple): Position (x, y) du texte
        font_scale (float): Échelle de la police
        color (tuple): Couleur du texte (B, G, R)
        thickness (int): Épaisseur du texte
        bg_color (tuple, optional): Couleur de fond (B, G, R)
        padding (int): Marge intérieure du fond
        
    Returns:
        numpy.ndarray: Image avec le texte dessiné
    """
    result = image.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Obtenir la taille du texte
    (text_width, text_height), _ = cv2.getTextSize(
        text, font, font_scale, thickness
    )
    
    x, y = position
    
    # Dessiner le fond si nécessaire
    if bg_color is not None:
        cv2.rectangle(
            result,
            (x - padding, y - text_height - padding),
            (x + text_width + padding, y + padding),
            bg_color, -1
        )
    
    # Dessiner le texte
    cv2.putText(
        result, text, (x, y), 
        font, font_scale, color, thickness, cv2.LINE_AA
    )
    
    return result

def create_gradient(
    size: Tuple[int, int], 
    start_color: Tuple[int, int, int], 
    end_color: Tuple[int, int, int],
    direction: str = 'horizontal'
) -> np.ndarray:
    """
    Crée un dégradé de couleur.
    
    Args:
        size (tuple): Taille de l'image (largeur, hauteur)
        start_color (tuple): Couleur de départ (B, G, R)
        end_color (tuple): Couleur de fin (B, G, R)
        direction (str): Direction du dégradé ('horizontal' ou 'vertical')
        
    Returns:
        numpy.ndarray: Image avec le dégradé
    """
    width, height = size
    
    if direction == 'horizontal':
        # Créer un tableau de 0 à 1 pour l'interpolation
        t = np.linspace(0, 1, width).reshape(1, -1, 1)
        # Étendre pour avoir la même hauteur
        t = np.tile(t, (height, 1, 3))
    else:  # vertical
        # Créer un tableau de 0 à 1 pour l'interpolation
        t = np.linspace(0, 1, height).reshape(-1, 1, 1)
        # Étendre pour avoir la même largeur
        t = np.tile(t, (1, width, 3))
    
    # Interpoler entre les couleurs
    gradient = (1 - t) * np.array(start_color) + t * np.array(end_color)
    
    return gradient.astype(np.uint8)

def apply_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Applique un masque à une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        mask (numpy.ndarray): Masque binaire (0 ou 255)
        
    Returns:
        numpy.ndarray: Image masquée
    """
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # S'assurer que le masque est binaire
    _, mask_bin = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    
    # Appliquer le masque
    result = image.copy()
    result[mask_bin == 0] = 0
    
    return result

def resize_with_aspect_ratio(
    image: np.ndarray, 
    width: Optional[int] = None, 
    height: Optional[int] = None, 
    inter: int = cv2.INTER_AREA
) -> np.ndarray:
    """
    Redimensionne une image en conservant le rapport d'aspect.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        width (int, optional): Largeur cible
        height (int, optional): Hauteur cible
        inter (int): Méthode d'interpolation
        
    Returns:
        numpy.ndarray: Image redimensionnée
    """
    # Si aucune dimension n'est spécifiée, retourner l'image originale
    if width is None and height is None:
        return image
    
    # Dimensions de l'image d'origine
    (h, w) = image.shape[:2]
    
    # Si les deux dimensions sont spécifiées, redimensionner directement
    if width is not None and height is not None:
        return cv2.resize(image, (width, height), interpolation=inter)
    
    # Calculer les dimensions en conservant le rapport d'aspect
    if width is None:
        # Seule la hauteur est spécifiée
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    else:
        # Seule la largeur est spécifiée
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    
    # Redimensionner l'image
    return cv2.resize(image, dim, interpolation=inter)
