import cv2
import numpy as np

# Créer une image noire de taille 500x500
img = np.zeros((500, 500, 3), np.uint8)

# Définir les couleurs de fond et de contour
bg_color = (255, 255, 255)
fg_color = (0, 0, 0)

# Définir les positions et tailles des touches du clavier
key_width = 50
key_height = 50
key_spacing = 5

# Définir les lettres arabes pour chaque touche
key_letters =""

# Définir la position de la première touche
key_x = 25
key_y = 25

# Tracer chaque touche
for i in range(len(key_letters)):
    # Calculer la position de la touche actuelle
    key_row = i // 10
    key_col = i % 10
    key_x_pos = key_x + key_col * (key_width + key_spacing)
    key_y_pos = key_y + key_row * (key_height + key_spacing)

    # Remplir la touche avec la couleur de fond
    cv2.rectangle(img, (key_x_pos, key_y_pos), (key_x_pos + key_width, key_y_pos + key_height), bg_color, -1)

    # Tracer le contour de la touche
    cv2.rectangle(img, (key_x_pos, key_y_pos), (key_x_pos + key_width, key_y_pos + key_height), fg_color, 2)

    # Ajouter la lettre arabe au centre de la touche
    text_size, _ = cv2.getTextSize(key_letters[i], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    text_x = key_x_pos + (key_width - text_size[0]) // 2
    text_y = key_y_pos + (key_height + text_size[1]) // 2
    cv2.putText(img, key_letters[i], (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, fg_color, 1)

# Afficher l'image
cv2.imshow("Arabic Keyboard", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
