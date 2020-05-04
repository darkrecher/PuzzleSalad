"""
TODO : paramètre facultatif correspondant à la couleur de transparence.
Les pixels ayant cette couleur seront écrit avec "." dans l'image puzzlescript.
"""

import itertools
import pygame


PUZZLE_SCRIPT_SPRITE_WIDTH = 5
PUZZLE_SCRIPT_SPRITE_HEIGHT = 5

# TODO : ça, c'est des paramètres de ligne de commande.
filepath_img = "test.png"
prefix_name = "ground_"

class TooMuchColorException(Exception): pass


def pixel_array_from_image_with_pygame(filepath_img):
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
    sprite_array = []
    for y in range(corner_y, corner_y + PUZZLE_SCRIPT_SPRITE_HEIGHT):
        sprite_array.append(
            pixel_array[y][corner_x:corner_x + PUZZLE_SCRIPT_SPRITE_WIDTH]
        )
    return tuple(sprite_array)

def puzscript_from_sprite(sprite_array, sprite_name):
    legend_colors = set(
        itertools.chain.from_iterable(sprite_array)
    )
    if len(legend_colors) > 10:
        raise TooMuchColorException("Too much colors : " + str(legend_colors))
    legend_colors = sorted(list(legend_colors))
    dict_legend_colors = {
        color: str(index)
        for index, color
        in enumerate(legend_colors)
    }

    puzscript_map = ""
    for y in range(PUZZLE_SCRIPT_SPRITE_HEIGHT):
        for x in range(PUZZLE_SCRIPT_SPRITE_WIDTH):
            puzscript_map += dict_legend_colors[sprite_array[y][x]]
        puzscript_map += "\n"

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


