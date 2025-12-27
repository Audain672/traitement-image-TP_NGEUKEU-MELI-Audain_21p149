""""
Module contenant les opérations de segmentation d'images.
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans

def threshold_otsu(image):
    """
    Applique un seuillage automatique d'Otsu à l'image.
    
    Args:
        image (numpy.ndarray): Image en niveaux de gris
        
    Returns:
        tuple: (image binaire, seuil optimal)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary, _

def adaptive_threshold(image, block_size=11, c=2):
    """
    Applique un seuillage adaptatif à l'image.
    
    Args:
        image (numpy.ndarray): Image en niveaux de gris
        block_size (int): Taille du voisinage pour le calcul du seuil (doit être impair)
        c (int): Constante soustraite de la moyenne
        
    Returns:
        numpy.ndarray: Image binaire
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    return cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, block_size, c
    )

def kmeans_segmentation(image, k=3, attempts=10):
    """
    Effectue une segmentation par k-moyennes (k-means) sur l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR)
        k (int): Nombre de clusters
        attempts (int): Nombre d'essais pour la convergence
        
    Returns:
        tuple: (image segmentée, centres des clusters)
    """
    # Redimensionner l'image pour accélérer le traitement
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    
    # Critères d'arrêt
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    # Appliquer k-means
    _, labels, centers = cv2.kmeans(
        pixel_values, k, None, criteria, attempts, cv2.KMEANS_RANDOM_CENTERS
    )
    
    # Convertir les centres en entiers 8 bits
    centers = np.uint8(centers)
    
    # Mapper les étiquettes aux centres
    segmented_image = centers[labels.flatten()]
    
    # Remettre à la forme de l'image originale
    segmented_image = segmented_image.reshape(image.shape)
    
    return segmented_image, centers

def watershed_segmentation(image):
    """
    Effectue une segmentation par ligne de partage des eaux.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR)
        
    Returns:
        numpy.ndarray: Image segmentée avec les régions colorées
    """
    # Convertir en niveaux de gris et appliquer un flou
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Seuillage d'Otsu
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Suppression du bruit
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Zone de fond sûre
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # Trouver la zone de premier plan sûr
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    
    # Trouver la région inconnue
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # Marquage des marqueurs
    _, markers = cv2.connectedComponents(sure_fg)
    
    # Ajouter 1 à toutes les étiquettes pour que le fond soit à 1
    markers = markers + 1
    
    # Marquage de la région inconnue avec 0
    markers[unknown == 255] = 0
    
    # Appliquer la transformation de la ligne de partage des eaux
    markers = cv2.watershed(image, markers)
    
    # Colorer les régions
    image[markers == -1] = [255, 0, 0]  # Bordures en bleu
    
    return image

def grabcut_segmentation(image, rect=None):
    """
    Effectue une segmentation par GrabCut.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR)
        rect (tuple): Région d'intérêt (x, y, largeur, hauteur)
        
    Returns:
        numpy.ndarray: Masque binaire du premier plan
    """
    if rect is None:
        rect = (50, 50, image.shape[1]-100, image.shape[0]-100)
    
    # Créer les masques nécessaires
    mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Appliquer GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
    
    # Créer un masque où 0 et 2 sont le fond, 1 et 3 sont le premier plan
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Appliquer le masque à l'image
    result = image * mask2[:, :, np.newaxis]
    
    return result

def find_contours(binary_image):
    """
    Trouve les contours dans une image binaire.
    
    Args:
        binary_image (numpy.ndarray): Image binaire
        
    Returns:
        list: Liste des contours trouvés
    """
    # Trouver les contours
    contours, _ = cv2.findContours(
        binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours

def draw_contours(image, contours, color=(0, 255, 0), thickness=2):
    """
    Dessine les contours sur une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        contours (list): Liste des contours à dessiner
        color (tuple): Couleur des contours (B, G, R)
        thickness (int): Épaisseur des contours
        
    Returns:
        numpy.ndarray: Image avec les contours dessinés
    """
    result = image.copy()
    cv2.drawContours(result, contours, -1, color, thickness)
    return result

def connected_components(image):
    """
    Étiquette les composantes connexes dans une image binaire.
    
    Args:
        image (numpy.ndarray): Image binaire
        
    Returns:
        tuple: (nombre de labels, image des labels, statistiques, centroïdes)
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    else:
        binary = image
    
    # Appliquer l'étiquetage des composantes connexes
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary, connectivity=8
    )
    
    # Créer une image colorée pour les étiquettes
    colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
    colors[0] = [0, 0, 0]  # Fond noir
    
    # Colorier les composantes
    colored = colors[labels]
    
    return num_labels, colored, stats, centroids
