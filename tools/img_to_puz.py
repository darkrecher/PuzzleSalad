"""
Script permettant de sortir des définitions de sprites écrits en PuzzleScript, à partir d'un fichier image.

Chaque sprite est un carré de 5*5 pixels, avec :
 - le nom
 - la liste des couleurs présentes dans le sprites (pas plus de 10), sous forme de code RVB avec un dièse.
 - le mapping des pixels : 5 lignes de 5 chiffres chacune, correspondants aux index de couleurs.

À noter qu'on peut utiliser la couleur transparente dans ces sprites. Il faut indiquer un "." dans le mapping.
Donc un sprite peut avoir 11 couleurs : 10 couleurs + la couleur transparente.
Mais pour l'instant, ce script ne gère pas la transparence.

TODO : paramètre facultatif correspondant à la couleur de transparence.
Les pixels ayant cette couleur seront écrit avec "." dans la map PuzzleScript.

Exemple de sprites PuzzleScript :

diamond
#d1ffff #8cffff #00ffff
.....
.012.
01122
.112.
..1..

ground_01
#1aac47 #a3831a #ba8e1a #d1971a #d1ad1a
14322
33233
24321
30242
24332

Définition des paramètres d'entrée :
Ils ne peuvent pas être passé en ligne de commande (parce que je l'ai pas encore fait).
Il faut les définir directement dans le code.
Voir ci-dessous, les lignes définissant les variables "filepath_img et "prefix_name".

 - filepath_img : chemin et nom du fichier image qui sera lu par le script.
 - prefix_name : string utilisée pour les noms. Tous les noms des sprites seront :
   "prefix_name_01", "prefix_name_02", "prefix_name_03", ...

Le numéro indiqué après le préfixe est toujours sur 2 chiffres.
Si on veut générer plus de 100 sprites, ça fera n'importe quoi. Tant pis.

Le script découpe l'image en carré de 5*5 pixels, et génère un script pour chacun d'eux.
Les carrés sont lus de gauche à droite, et de haut en bas.

Si la hauteur ou la largeur de l'image n'est pas un multiple de 5, on ne prend pas en
compte les lignes ou colonnes de pixels en trop.

Si l'un des carrés de 5*5 pixels comporte plus de 10 couleurs, ça génère une exception
et ça arrête le traitement.
TODO : faire autrement, mieux, plus configurable.

"""

import itertools
# TODO : on utilise pygame juste pour lire le fichier image.
# Ce serait bien si ça pouvait fonctionner avec d'autres lib de lecture d'image :
# PIL, openCV, ...
# On teste les imports du plus possible de librairie, et on s'arrête à la première qui marche.
import pygame


PUZZLE_SCRIPT_SPRITE_WIDTH = 5
PUZZLE_SCRIPT_SPRITE_HEIGHT = 5

# TODO : ça, c'est des paramètres de ligne de commande.
filepath_img = "test.png"
prefix_name = "ground_"


class TooMuchColorException(Exception):
    """
    Exception qui se déclenche lorsqu'il y a plus de 10 couleurs différentes dans un sprite.
    """
    pass


def pixel_array_from_image_with_pygame(filepath_img):
    """
    Renvoie un tableau de pixels (pixel_array) à partir d'un fichier image.
    Le fichier image est ouvert à l'aide de la librairie pygame
    (les formats classiques sont reconnus : .png, .jpg, ...)

    La fonction renvoie un tuple de trois éléments :
     - la largeur de l'image
     - sa hauteur
     - les pixels, sous forme d'un sous-tuple de sous-sous-tuple.
       l'élément [0][0] correspond à la couleur du pixel en haut à gauche.
       Chaque élément de pixel est un sous-sous-sous-tuple de 3 octets,
       correspondants aux composantes RVB de la couleur.

    L'image initiale peut comporter des infos de transparence. Celle-ci ne sont pas récupérées.
    """
    pixel_array = []
    surface_img = pygame.image.load(filepath_img)
    width, height = surface_img.get_rect().size
    for y in range(height):
        current_pixel_line = []
        for x in range(width):
            # Pas optimisé du tout, parce que le get_at est très lent.
            # Mais on s'en fiche, c'est du one-shot.
            pix = surface_img.get_at((x, y))
            pix = pix[:3]
            current_pixel_line.append(pix)
        pixel_array.append(tuple(current_pixel_line))
    return width, height, tuple(pixel_array)


def extract_sprite(pixel_array, corner_x, corner_y):
    """
    Récupère un rectangle de pixels ayant la taille d'un sprite de PuzzleScript (5*5),
    à partir d'un rectangle de pixel plus grand.
    Les coordonnées du coin supérieur gauche du rectangle à récupérer sont déterminées
    par les paramètres corner_x, corner_y.
    La fonction renvoie un tuple de sous-tuple.
    l'élément [0][0] correspond à la couleur du pixel en haut à gauche du rectangle extrait.
    Chaque élément de pixel est un sous-sous tuple de 3 octets : les couleurs RVB.

    Aucune vérification n'est effectuée sur la position du rectangle à extraire
    par rapport à la taille du pixel_array. C'est au code extérieur de le faire.
    Par exemple, le pixel_array a une largeur de 47 et on veut extraire un rectangle
    à l'abscisse corner_x = 45.
    """
    sprite_array = []
    for y in range(corner_y, corner_y + PUZZLE_SCRIPT_SPRITE_HEIGHT):
        sprite_array.append(
            pixel_array[y][corner_x:corner_x + PUZZLE_SCRIPT_SPRITE_WIDTH]
        )
    return tuple(sprite_array)


def puzscript_from_sprite(sprite_array, sprite_name):
    """
    Renvoie une string sur plusieurs lignes, correspondant au code Puzzlescript
    définissant un sprite (voir exemple au début de ce script).
    Le nom du sprite est défini par le paramètre sprite_name.
    Son image est défini par le rectangle de pixels sprite_array.
    Les dimensions de sprite_array doivent correspondre à un sprite de PuzzleScript : 5*5.

    Cette fonction peut déclencher une exception TooMuchColorException.
    """

    # Construction de l'index des couleurs.
    legend_colors = set(
        itertools.chain.from_iterable(sprite_array)
    )
    if len(legend_colors) > 10:
        raise TooMuchColorException("Too much colors : " + str(legend_colors))
    # On trie l'index des couleurs, selon l'ordre croissant des composantes
    # R, puis V, puis B.
    # La méthode de tri, n'a pas d'importance. L'important c'est que legend_colors
    # soit trié, pour que les numéros d'index dans cette liste aient une signification.
    legend_colors = sorted(list(legend_colors))
    # dict_legend_colors définit la correspondance entre une couleur et son numéro d'index.
    # clé : un tuple de 3 éléments (3 octets) : les couleurs RVB.
    # valeur : une string contenant un chiffre (0 à 9) : le numéro d'index de la couleur
    # dans le code PuzzleScript de ce sprite.
    dict_legend_colors = {
        color: str(index)
        for index, color
        in enumerate(legend_colors)
    }

    # puzscript_map est une string sur plusieurs lignes.
    # Chaque ligne correspond à une ligne de pixels.
    # Chaque caractère de puzscript_map correspond à un index de pixel
    # dans dict_legend_colors.
    puzscript_map = ""
    for y in range(PUZZLE_SCRIPT_SPRITE_HEIGHT):
        for x in range(PUZZLE_SCRIPT_SPRITE_WIDTH):
            puzscript_map += dict_legend_colors[sprite_array[y][x]]
        puzscript_map += "\n"

    # Pour toutes les couleurs de la légende.
    # Conversion des tuples de composantes RVB vers une string au format
    # des codes couleurs HTML.
    # Dans cette string, deux codes couleurs HTML sont séparés par un espace.
    # exemple :
    # legend_colors = ((1, 2, 3), (150, 200, 250))
    # str_legend_colors = "#010203 #96c8fa"
    str_legend_colors = " ".join(
        "#%02x%02x%02x" % color
        for color in legend_colors
    )

    return "\n".join((
        sprite_name,
        str_legend_colors,
        puzscript_map,
    ))


def main():
    """
     - Lecture du fichier image,
     - découpage en rectangle de 5*5 pixels, (de gauche à droite et de haut en bas)
     - détermintation du code PuzzleScript de chacun des sprite correspondant
       à ces rectangles,
     - écriture, sur la sortie staandard, du code PuzzleScript de ces sprites.

    TODO : ce code peut thrower l'exception TooMuchColorException,
    mais elle n'est pas catchée.
    """

    width, height, pixel_array = pixel_array_from_image_with_pygame(filepath_img)
    sprite_index = 1
    for sprite_y in range(0, width, 5):
        for sprite_x in range(0, height, 5):
            sprite_array = extract_sprite(pixel_array, sprite_x, sprite_y)
            # TODO : le nom peut être sur 3 chiffres, ou plus, ou moins.
            puzscript = puzscript_from_sprite(
                sprite_array,
                "%s%02d" % (prefix_name, sprite_index)
            )
            print(puzscript)
            print()
            sprite_index += 1


if __name__ == "__main__":
    main()


