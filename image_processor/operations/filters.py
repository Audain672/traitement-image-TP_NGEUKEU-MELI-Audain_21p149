""""
Module contenant les opérations de filtrage d'images.
"""

import cv2
import numpy as np

def apply_gaussian_blur(image, kernel_size=(5, 5), sigma=0):
    """
    Applique un flou gaussien à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        kernel_size (tuple): Taille du noyau (largeur, hauteur)
        sigma (float): Écart-type du noyau gaussien
        
    Returns:
        numpy.ndarray: Image floutée
    """
    return cv2.GaussianBlur(image, kernel_size, sigma)

def apply_median_blur(image, ksize=5):
    """
    Applique un filtre médian à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        ksize (int): Taille du noyau (doit être impair)
        
    Returns:
        numpy.ndarray: Image filtrée
    """
    return cv2.medianBlur(image, ksize)

def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Applique un filtre bilatéral à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        d (int): Diamètre du voisinage
        sigma_color: Filtre sigma dans l'espace des couleurs
        sigma_space: Filtre sigma dans l'espace des coordonnées
        
    Returns:
        numpy.ndarray: Image filtrée
    """
    return cv2.bilateralFilter(image, d, sigma_color, sigma_space)

def apply_sobel(image, dx=1, dy=1, ksize=3):
    """
    Applique l'opérateur de Sobel pour détecter les contours.
    
    Args:
        image (numpy.ndarray): Image d'entrée (en niveaux de gris)
        dx (int): Ordre de la dérivée en x
        dy (int): Ordre de la dérivée en y
        ksize (int): Taille du noyau de Sobel
        
    Returns:
        numpy.ndarray: Image des contours détectés
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
    
    # Calcul de la magnitude du gradient
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    
    # Normalisation pour l'affichage
    return cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

def apply_laplacian(image, ksize=3):
    """
    Applique l'opérateur Laplacien pour détecter les contours.
    
    Args:
        image (numpy.ndarray): Image d'entrée (en niveaux de gris)
        ksize (int): Taille du noyau Laplacien
        
    Returns:
        numpy.ndarray: Image des contours détectés
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)
    return cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

def apply_canny(image, threshold1=100, threshold2=200):
    """
    Détecte les contours avec l'algorithme de Canny.
    
    Args:
        image (numpy.ndarray): Image d'entrée (en niveaux de gris)
        threshold1 (int): Premier seuil pour la procédure d'hystérésis
        threshold2 (int): Deuxième seuil pour la procédure d'hystérésis
        
    Returns:
        numpy.ndarray: Image des contours détectés
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return cv2.Canny(image, threshold1, threshold2)

def apply_custom_kernel(image, kernel):
    """
    Applique un noyau de convolution personnalisé à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        kernel (numpy.ndarray): Noyau de convolution
        
    Returns:
        numpy.ndarray: Image filtrée
    """
    return cv2.filter2D(image, -1, kernel)

def apply_sharpening(image):
    """
    Applique un filtre de netteté à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        
    Returns:
        numpy.ndarray: Image avec netteté améliorée
    """
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)

def apply_emboss(image):
    """
    Applique un effet d'embossage à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        
    Returns:
        numpy.ndarray: Image avec effet d'embossage
    """
    kernel = np.array([[-2, -1, 0],
                       [-1,  1, 1],
                       [ 0,  1, 2]])
    return cv2.filter2D(image, -1, kernel)
