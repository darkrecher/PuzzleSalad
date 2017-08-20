"""
Not documented at all. Sorry.
"""

from img_bourrinos import PIXELS


# https://stackoverflow.com/questions/18943387/how-to-analyse-bitmap-image-in-python-using-pil

def export_pixel_as_a_big_bourrin(img_filename):

	import PIL
	import PIL.Image

	img = PIL.Image.open(img_filename)
	rgb_im = img.convert('RGB')

	print(rgb_im.size)
	# Ça sort pas tout à fait les mêmes valeurs RGB que dans Paint.net.
	# Faudrait vraiment se poser la question de pourquoi ça fait ça, parce que c'est très étrange.
	# Mais pour l'instant, osef.
	print(rgb_im.getpixel((0, 0)))
	print(rgb_im.getpixel((1, 0)))
	print('')

	for y in range(rgb_im.size[1]):
		line = ', '.join([
			str(rgb_im.getpixel((x, y)))
			for x in range(rgb_im.size[0])
		])
		print('[' + line + '], ')


def to_black(pix, limit=25):
	if all((
		comp < limit
		for comp in pix
	)):
		return (0, 0, 0)
	else:
		return pix


def pre_process_tile_colors(pixels):
	"""
	Transforme tout ce qui est un inférieur à (25, 25, 25) en noir (à cause des approximations jpeg).
	Supprime les doublons.
	"""
	processed_pixels = set()
	for pix in pixels:
		processed_pixels.add(to_black(pix))
	return list(processed_pixels)


def dist(pix_1, pix_2):
	dist_components = [
		abs(component_1 - component_2)
		for (component_1, component_2) in
		zip(pix_1, pix_2)
	]

	prod = 1
	for comp in dist_components:
		prod *= comp
	return prod


def middle(pix_1, pix_2):
	components = [
		(component_1 + component_2) // 2
		for (component_1, component_2) in
		zip(pix_1, pix_2)
	]
	return components


def get_nearest_pixels(pixels):
	min_dist = 256 ** 3
	indexes_of_min = None
	for index_1, pix_1 in enumerate(pixels):
		for index_2 in range(index_1+1, len(pixels)):
			pix_2 = pixels[index_2]
			current_dist = dist(pix_1, pix_2)
			if min_dist > current_dist:
				min_dist = current_dist
				indexes_of_min = (index_1, index_2)
	return indexes_of_min


def reduce_colors(pixels, nb_limit=10):
	"""
	Diminue le nombre de couleurs différentes dans une liste de pixels,
	en remplaçant les couleurs proches par une couleur commune.
	Ça marche mieux si, au départ, il n'y a pas de doublons dans pixels.
	"""
	while len(pixels) > nb_limit:
		index_1, index_2 = get_nearest_pixels(pixels)
		pix_to_eliminate_1 = pixels[index_1]
		pix_to_eliminate_2 = pixels[index_2]
		pixels_to_eliminate = (pix_to_eliminate_1, pix_to_eliminate_2)
		pixels = [
			pix for pix in pixels
			if pix not in pixels_to_eliminate ]
		pixels.append(middle(pix_to_eliminate_1, pix_to_eliminate_2))

	return pixels


def cropped(pixels, x, y, w=5, h=5):
	cropped = []
	for index_y in range(y, y + h):
		cropped.append(pixels[index_y][x:x+w])
	return cropped


def get_palette_index(pix, palette):
	distance_and_indexes = [
		(dist(pix, palette_pix), index)
		for index, palette_pix
		in enumerate(palette)
	]
	min_dist = min(distance_and_indexes)
	return min_dist[1]


def str_from_pix(pix):
	"""
	(15, 130, 255) -> '#0F82FF'
	"""
	hex_components = [
		hex(component)[2:].rjust(2, '0').upper()
		for component in pix ]
	return '#' + ''.join(hex_components)


class TileDefinition():

	def __init__(self, pixels, legend_char, legend_name):

		self.legend_char = legend_char
		self.legend_name = legend_name

		flat_pixels = []
		for line in pixels:
			flat_pixels.extend(line)

		if len(flat_pixels) != 25:
			raise Exception("Le dessin d'une tile doit être un carré de 5*5 pixel")

		self.palette = pre_process_tile_colors(flat_pixels)
		self.palette = reduce_colors(self.palette, 10)
		self.palettized_pixels = [
			[
				get_palette_index(pix, self.palette)
				for pix in line
			] for line in pixels
		]

	def get_img_definition(self):
		str_palette = ' '.join([
			str_from_pix(pix) for pix in self.palette
		])
		str_palettized_lines = [
			''.join([
				str(char) for char in line
			]) for line in self.palettized_pixels
		]
		img_definition_lines = [ self.legend_name ] + [ str_palette ] + str_palettized_lines
		return '\n'.join(img_definition_lines) + '\n'


LEGEND_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ'
FORBIDDEN_LEGEND_CHARS = 'V.O#CJMB~WGZ'


def generator_authorized_legend_chars():

	for char in LEGEND_CHARS:
		if char not in FORBIDDEN_LEGEND_CHARS:
			yield char
	raise Exception("plus assez de caractères pour la légende.")


img_w = len(PIXELS[0])
img_h = len(PIXELS)
print(img_w, img_h)

if img_w % 5:
	raise Exception("La largeur de l'image doit être un multiple de 5. (La hauteur aussi, au passage).")

if img_h % 5:
	raise Exception("La hauteur de l'image doit être un multiple de 5.")

NAME_PREFIX_TILES = 'Madeleine_'

level_map = []
tile_defs = []
name_index = 0
authorized_legend_chars = generator_authorized_legend_chars()

for y_pix in range(0, img_h, 5):
	level_line = ''
	for x_pix in range(0, img_w, 5):
		tile_img = cropped(PIXELS, x_pix, y_pix)
		legend_char = next(authorized_legend_chars)
		legend_name = NAME_PREFIX_TILES + str(name_index).rjust(2, '0')
		tile_def = TileDefinition(tile_img, legend_char, legend_name)
		print(tile_def.get_img_definition())
		level_line += legend_char
		tile_defs.append(tile_def)
		name_index += 1
	level_map.append(level_line)


legend = '\n'.join([
	'%s = %s' % (tile_def.legend_char, tile_def.legend_name)
	for tile_def in tile_defs
])
print(legend)
print('')

collision_layers = ', '.join([
	tile_def.legend_name
	for tile_def in tile_defs
])
print(collision_layers)
print('')

level = '\n'.join(level_map)
print(level)
print('')

#pixels = pre_process_tile_colors(PIXELS[15])
#print(pixels)
#pixels = reduce_colors(pixels, 10)
#print(pixels)

