"""
Module contenant les opérations de base de traitement d'images.
"""

import cv2
import numpy as np

def convert_to_grayscale(image):
    """
    Convertit une image en niveaux de gris.
    
    Args:
        image (numpy.ndarray): Image d'entrée au format BGR
        
    Returns:
        numpy.ndarray: Image en niveaux de gris
    """
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def resize_image(image, width=None, height=None, inter=cv2.INTER_LINEAR):
    """
    Redimensionne une image en conservant le rapport d'aspect.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        width (int, optional): Largeur souhaitée. Par défaut à None.
        height (int, optional): Hauteur souhaitée. Par défaut à None.
        inter (int, optional): Méthode d'interpolation. Par défaut à cv2.INTER_LINEAR.
        
    Returns:
        numpy.ndarray: Image redimensionnée
    """
    if width is None and height is None:
        return image
    
    h, w = image.shape[:2]
    
    if width is None:
        ratio = height / float(h)
        dim = (int(w * ratio), height)
    elif height is None:
        ratio = width / float(w)
        dim = (width, int(h * ratio))
    else:
        dim = (width, height)
    
    return cv2.resize(image, dim, interpolation=inter)

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """
    Ajuste la luminosité et le contraste d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        alpha (float): Contrôle le contraste (1.0 signifie aucun changement)
        beta (int): Contrôle la luminosité (0 signifie aucun changement)
        
    Returns:
        numpy.ndarray: Image avec luminosité et contraste ajustés
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def rotate_image(image, angle, center=None, scale=1.0):
    """
    Fait pivoter une image d'un angle donné autour d'un point central.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        angle (float): Angle de rotation en degrés
        center (tuple, optional): Point central de rotation. Si None, utilise le centre de l'image.
        scale (float, optional): Facteur d'échelle. Par défaut à 1.0.
        
    Returns:
        numpy.ndarray: Image pivotée
    """
    (h, w) = image.shape[:2]
    
    if center is None:
        center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, scale)
    return cv2.warpAffine(image, M, (w, h))

def flip_image(image, flip_code=1):
    """
    Retourne une image horizontalement, verticalement ou les deux.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        flip_code (int): 
            0 pour un retournement vertical,
            1 pour un retournement horizontal,
            -1 pour un retournement vertical et horizontal.
            
    Returns:
        numpy.ndarray: Image retournée
    """
    return cv2.flip(image, flip_code)

def crop_image(image, x, y, width, height):
    """
    Recadre une image à la position et aux dimensions spécifiées.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        x (int): Position x du coin supérieur gauche
        y (int): Position y du coin supérieur gauche
        width (int): Largeur de la zone de recadrage
        height (int): Hauteur de la zone de recadrage
        
    Returns:
        numpy.ndarray: Image recadrée
    """
    return image[y:y+height, x:x+width]

def normalize_image(image):
    """
    Normalise les valeurs de l'image entre 0 et 255.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        
    Returns:
        numpy.ndarray: Image normalisée
    """
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
