""
Module contenant les opérations morphologiques pour le traitement d'images.
"""

import cv2
import numpy as np

def get_kernel(shape=cv2.MORPH_RECT, size=(3, 3)):
    """
    Crée un noyau structurant pour les opérations morphologiques.
    
    Args:
        shape: Forme du noyau (cv2.MORPH_RECT, cv2.MORPH_ELLIPSE, cv2.MORPH_CROSS)
        size: Taille du noyau (largeur, hauteur)
        
    Returns:
        numpy.ndarray: Noyau structurant
    """
    return cv2.getStructuringElement(shape, size)

def apply_erosion(image, kernel_size=3, iterations=1):
    """
    Applique une opération d'érosion à l'image binaire.
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau d'érosion
        iterations (int): Nombre d'itérations
        
    Returns:
        numpy.ndarray: Image érodée
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def apply_dilation(image, kernel_size=3, iterations=1):
    """
    Applique une opération de dilatation à l'image binaire.
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau de dilatation
        iterations (int): Nombre d'itérations
        
    Returns:
        numpy.ndarray: Image dilatée
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)

def apply_opening(image, kernel_size=3):
    """
    Applique une opération d'ouverture (érosion suivie de dilatation).
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau
        
    Returns:
        numpy.ndarray: Image après ouverture
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def apply_closing(image, kernel_size=3):
    """
    Applique une opération de fermeture (dilatation suivie d'érosion).
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau
        
    Returns:
        numpy.ndarray: Image après fermeture
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def apply_gradient(image, kernel_size=3):
    """
    Applique un gradient morphologique (différence entre dilatation et érosion).
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau
        
    Returns:
        numpy.ndarray: Gradient morphologique
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

def apply_tophat(image, kernel_size=3):
    """
    Applique un Top-Hat (différence entre l'image et son ouverture).
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau
        
    Returns:
        numpy.ndarray: Résultat du Top-Hat
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

def apply_blackhat(image, kernel_size=3):
    """
    Applique un Black-Hat (différence entre la fermeture et l'image).
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        kernel_size (int): Taille du noyau
        
    Returns:
        numpy.ndarray: Résultat du Black-Hat
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)

def skeletonize(image):
    """
    Réduit les régions d'une image binaire à des squelettes d'un pixel de large.
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        
    Returns:
        numpy.ndarray: Image squelettisée
    """
    # Vérifier si l'image est binaire
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Initialiser le squelette
    skeleton = np.zeros(binary.shape, dtype=np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    
    while True:
        # Étape 1: Ouverture
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, element)
        # Étape 2: Soustraction
        temp = cv2.subtract(binary, opened)
        # Étape 3: Érosion
        eroded = cv2.erode(binary, element)
        # Étape 4: Copier le squelette
        skeleton = cv2.bitwise_or(skeleton, temp)
        # Étape 5: Itération
        binary = eroded.copy()
        # Condition d'arrêt
        if cv2.countNonZero(binary) == 0:
            break
            
    return skeleton

def distance_transform(image):
    """
    Calcule la transformée de distance d'une image binaire.
    
    Args:
        image (numpy.ndarray): Image binaire d'entrée
        
    Returns:
        numpy.ndarray: Transformée de distance normalisée
    """
    # Assurez-vous que l'image est binaire
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Calculer la transformée de distance
    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    
    # Normalisation pour l'affichage
    return cv2.normalize(dist, None, 0, 1.0, cv2.NORM_MINMAX)
