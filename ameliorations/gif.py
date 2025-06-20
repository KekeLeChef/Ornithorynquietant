from PIL import Image
import os
def creer_gif(images, chemin_sortie, duree=500, boucle=0):
    """
    Crée un GIF à partir d'une liste d'images.

    :param images: Liste de chemins vers les images (dans l'ordre).
    :param chemin_sortie: Chemin du fichier GIF de sortie (ex: 'animation.gif').
    :param duree: Durée d'affichage de chaque image (en ms).
    :param boucle: Nombre de fois que le GIF boucle (0 = infini).
    """
    if not images:
        print("Erreur : aucune image fournie.")
        return

    # Ouvrir toutes les images
    frames = [Image.open(img).convert("RGBA") for img in images]

    # Sauvegarder sous forme de GIF
    frames[0].save(
        chemin_sortie,
        save_all=True,
        append_images=frames[1:],
        duration=duree,
        loop=boucle,
        optimize=True
    )

    print(f"GIF créé avec succès : {chemin_sortie}")

dossier = "Evolution_sur_24h"
images=sorted([
    os.path.join(dossier,f)
    for f in os.listdir(dossier)
    if f.endswith(('.png'))])

creer_gif(images,"gif.gif")

