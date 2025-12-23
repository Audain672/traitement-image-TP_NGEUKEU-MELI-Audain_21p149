""
Module contenant les opérations de transformation d'images.
"""

import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    """
    Ajuste la correction gamma d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        gamma (float): Valeur gamma (1.0 = aucun changement)
        
    Returns:
        numpy.ndarray: Image avec correction gamma
    """
    # Éviter la division par zéro
    inv_gamma = 1.0 / gamma if gamma != 0 else 0
    
    # Créer une table de correspondance
    table = np.array([((i / 255.0) ** inv_gamma) * 255 
                     for i in np.arange(0, 256)]).astype("uint8")
    
    # Appliquer la correction gamma
    return cv2.LUT(image, table)

def adjust_contrast(image, alpha=1.0):
    """
    Ajuste le contraste d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        alpha (float): Facteur de contraste (1.0 = aucun changement)
        
    Returns:
        numpy.ndarray: Image avec contraste ajusté
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

def adjust_brightness(image, beta=0):
    """
    Ajuste la luminosité d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        beta (int): Valeur à ajouter (peut être négative)
        
    Returns:
        numpy.ndarray: Image avec luminosité ajustée
    """
    return cv2.convertScaleAbs(image, alpha=1.0, beta=beta)

def adjust_saturation(image, saturation=1.0):
    """
    Ajuste la saturation d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR)
        saturation (float): Facteur de saturation (1.0 = aucun changement)
        
    Returns:
        numpy.ndarray: Image avec saturation ajustée
    """
    # Convertir en espace de couleur HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    
    # Ajuster la saturation
    hsv[..., 1] = hsv[..., 1] * saturation
    hsv[..., 1] = np.clip(hsv[..., 1], 0, 255)
    
    # Reconvertir en BGR
    return cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

def adjust_hue(image, hue_shift=0):
    """
    Ajuste la teinte d'une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée (BGR)
        hue_shift (int): Décalage de teinte (0-180)
        
    Returns:
        numpy.ndarray: Image avec teinte ajustée
    """
    # Convertir en espace de couleur HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    
    # Ajuster la teinte (module 180 car la teinte est dans [0, 180])
    hsv[..., 0] = (hsv[..., 0] + hue_shift) % 180
    
    # Reconvertir en BGR
    return cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

def equalize_histogram(image):
    """
    Applique l'égalisation d'histogramme à une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée (niveaux de gris ou couleur)
        
    Returns:
        numpy.ndarray: Image avec histogramme égalisé
    """
    if len(image.shape) == 2:  # Image en niveaux de gris
        return cv2.equalizeHist(image)
    else:  # Image couleur
        # Convertir en espace de couleur YCrCb (Y = luminance)
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        
        # Égaliser le canal Y (luminance)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        
        # Reconvertir en BGR
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

def clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """
    Applique l'égalisation adaptative de l'histogramme (CLAHE) à une image.
    
    Args:
        image (numpy.ndarray): Image d'entrée (niveaux de gris ou couleur)
        clip_limit (float): Seuil de contraste
        tile_grid_size (tuple): Taille des tuiles pour l'égalisation locale
        
    Returns:
        numpy.ndarray: Image avec CLAHE appliqué
    """
    clahe = cv2.createCLAHE(
        clipLimit=clip_limit, 
        tileGridSize=tile_grid_size
    )
    
    if len(image.shape) == 2:  # Image en niveaux de gris
        return clahe.apply(image)
    else:  # Image couleur
        # Convertir en espace de couleur LAB (L = luminance)
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Appliquer CLAHE sur le canal L
        lab[..., 0] = clahe.apply(lab[..., 0])
        
        # Reconvertir en BGR
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def apply_affine_transform(image, angle=0, scale=1.0, tx=0, ty=0):
    """
    Applique une transformation affine à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        angle (float): Angle de rotation en degrés
        scale (float): Facteur d'échelle
        tx (int): Translation en x
        ty (int): Translation en y
        
    Returns:
        numpy.ndarray: Image transformée
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Matrice de rotation et d'échelle
    M = cv2.getRotationMatrix2D(center, angle, scale)
    
    # Ajouter la translation
    M[0, 2] += tx
    M[1, 2] += ty
    
    # Appliquer la transformation
    return cv2.warpAffine(
        image, M, (w, h), 
        flags=cv2.INTER_LINEAR, 
        borderMode=cv2.BORDER_REFLECT_101
    )

def apply_perspective_transform(image, src_points, dst_points):
    """
    Applique une transformation de perspective à l'image.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        src_points (numpy.ndarray): Points sources (4 points)
        dst_points (numpy.ndarray): Points de destination (4 points)
        
    Returns:
        numpy.ndarray: Image transformée
    """
    # Calculer la matrice de transformation
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # Appliquer la transformation
    h, w = image.shape[:2]
    return cv2.warpPerspective(
        image, M, (w, h), 
        flags=cv2.INTER_LINEAR, 
        borderMode=cv2.BORDER_REFLECT_101
    )

def apply_log_transform(image, c=1):
    """
    Applique une transformation logarithmique à l'image.
    Utile pour améliorer les détails dans les zones sombres.
    
    Args:
        image (numpy.ndarray): Image d'entrée
        c (float): Constante de mise à l'échelle
        
    Returns:
        numpy.ndarray: Image transformée
    """
    # Convertir en flottant et normaliser
    img_float = image.astype(np.float32) / 255.0
    
    # Appliquer la transformation logarithmique
    log_transformed = c * np.log1p(img_float)
    
    # Normaliser pour l'affichage
    log_transformed = (log_transformed / log_transformed.max()) * 255.0
    
    return log_transformed.astype(np.uint8)

def apply_power_law_transform(image, gamma=1.0, c=1):
    """
    Applique une transformation en loi de puissance (correction gamma).
    
    Args:
        image (numpy.ndarray): Image d'entrée
        gamma (float): Paramètre gamma
        c (float): Constante de mise à l'échelle
        
    Returns:
        numpy.ndarray: Image transformée
    """
    # Convertir en flottant et normaliser
    img_float = image.astype(np.float32) / 255.0
    
    # Éviter les valeurs négatives
    img_float = np.maximum(img_float, 0)
    
    # Appliquer la transformation en loi de puissance
    power_transformed = c * np.power(img_float, gamma)
    
    # Normaliser pour l'affichage
    power_transformed = np.clip(power_transformed * 255.0, 0, 255)
    
    return power_transformed.astype(np.uint8)

def apply_histogram_matching(source, reference):
    """
    Applique la correspondance d'histogramme entre l'image source et l'image de référence.
    
    Args:
        source (numpy.ndarray): Image source
        reference (numpy.ndarray): Image de référence
        
    Returns:
        numpy.ndarray: Image source avec l'histogramme correspondant à la référence
    """
    def get_lookup_table(source_channel, reference_channel):
        """Calcule la table de correspondance des valeurs d'intensité."""
        # Calculer les histogrammes cumulatifs normalisés
        src_hist, _ = np.histogram(source_channel.flatten(), 256, [0, 256])
        ref_hist, _ = np.histogram(reference_channel.flatten(), 256, [0, 256])
        
        src_cdf = src_hist.cumsum()
        src_cdf = src_cdf / src_cdf[-1]  # Normaliser
        
        ref_cdf = ref_hist.cumsum()
        ref_cdf = ref_cdf / ref_cdf[-1]  # Normaliser
        
        # Créer la table de correspondance
        lookup_table = np.zeros(256, dtype=np.uint8)
        
        for i in range(256):
            # Trouver l'indice j où ref_cdf[j] est le plus proche de src_cdf[i]
            j = np.argmin(np.abs(ref_cdf - src_cdf[i]))
            lookup_table[i] = j
            
        return lookup_table
    
    if len(source.shape) == 2:  # Niveaux de gris
        return get_lookup_table(source, reference)[source]
    else:  # Couleur
        # Traiter chaque canal séparément
        result = np.zeros_like(source)
        for i in range(3):
            lookup_table = get_lookup_table(source[..., i], reference[..., i])
            result[..., i] = lookup_table[source[..., i]]
        return result
