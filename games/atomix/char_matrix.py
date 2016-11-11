# coding: utf-8

"""
Gestion d'un tableau de caractères en deux dimensions, un peu comme si c'était un tableau de pixels.
"""

# TODO : fonctions pour gérer des rectangles de strings comme des matrix :
#  - copie d'un rectangle de string dans un autre rectangle, à une coordonnée indiquée. On blitte pas les espaces.
#  - crop d'un rectangle de string (générique : x, y, w, h).
#  - recherche de tous les éléments d'un char spécifique.

def _get_coords_around(coord):
	yield (coord[0]-1, coord[1]-1)
	yield (coord[0],   coord[1]-1)
	yield (coord[0]+1, coord[1]-1)
	yield (coord[0]-1, coord[1])
	yield (coord[0]+1, coord[1])
	yield (coord[0]-1, coord[1]+1)
	yield (coord[0],   coord[1]+1)
	yield (coord[0]+1, coord[1]+1)

class CharMatrix():

	def __init__(self, char_matrix):
		self.char_matrix = char_matrix

	def __str__(self):
		return '\n'.join(self.char_matrix)

	def verify_matrix(self):
		"""
		Génère une exception si la matrix de caractères n'est pas de forme rectangulaire.
		"""
		if len(self.char_matrix) == 0:
			return
		supposed_width = len(self.char_matrix[0])
		for line in self.char_matrix:
			if len(line) != supposed_width:
				raise Exception("La ligne suivante n'a pas la bonne longueur : " + str(line))

	def dimensions(self):
		"""
		:return: La largeur et la hauteur de la char_matrix.
		:rtype: Un tuple de deux entiers
		"""
		# On part du principe que la char_matrix est correcte. Donc on peut ne consulter que la width de la première ligne.
		# Si on n'est pas sûr que ce soit correcte, le code extérieur n'a qu'à exécuter verify_matrix.
		if len(self.char_matrix) == 0:
			return (0, 0)
		return (len(self.char_matrix[0]), len(self.char_matrix))

	def in_dimensions(self, coord, raise_exception=False):
		"""
		Vérifie que les coordonnées spécifiées sont bien dans les dimensions de la matrice.
		:param coord: coordonnée (x, y) à vérifier.
		:param raise_exception: indique le comportement si les coordonnées spécifiées sont en dehors des dimensions de la matrice.
		:type coord: tuple de deux entiers.
		:type raise_exception: boolean
		:return: True si c'est dans les dimensions, False si hors dimensions et que raise_exception=False.
		:rtype: boolean.
		"""
		# FUTURE : tiens, ce serait classe un décorateur qui catche tout et qui renvoie None quand ça merde.
		dim = self.dimensions()
		if not(0 <= coord[0] < dim[0] and 0 <= coord[1] < dim[1]):
			if raise_exception:
				raise Exception(
					"".join((
						"Les coordonnées ",
						str(coord),
						" sont en dehors de la CharMatrix ",
						str(dim),
						"."
					))
				)
			else:
				return False
		return True

	def get_char(self, coord, raise_exception=False):
		"""
		Renvoie le caractère aux coordonnées spécifiées. Contrôle les coordonnées par rapport au dimensions de la matrice.
		:param coord: coordonnée (x, y) du caractère qu'on veut récupérer dans la matrice.
		:param raise_exception: indique le comportement si les coordonnées spécifiées sont en dehors des dimensions de la matrice.
		:type coord: tuple de deux entiers.
		:type raise_exception: boolean.
		:return: le caractère demandé, ou None si hors dimensions et que raise_exception=False.
		:rtype: une string de un seul caractère, ou None.
		"""
		if self.in_dimensions(coord, raise_exception):
			# Ça va systématiquement raiser une exception si la ligne est trop courte.
			# Ce genre de cas ne peut arriver que si la char_matrix n'est pas rectangulaire.
			# C'est un cas anormal, qui mérite une exception.
			# (Pour s'en prévenir, il suffit de préalablement appeler verify_matrix).
			x, y = coord
			return(self.char_matrix[y][x])
		return None

	def get_coords_around(self, coord):
		"""
		Itére sur les coordonnées autour des coordonnées spécifiées (diagonales comprises).
		Tient compte des dimensions de la matrice.
		:param coord: coordonnée (x, y) de la position dont on veut récupérer les coordonnées alentours.
		:type coord: tuple de deux entiers.
		:return: une itération sur des coordonnées
		:rtype: tuples de deux entiers, les uns après les autres.
		"""
		for coord_around in _get_coords_around(coord):
			if self.in_dimensions(coord_around):
				yield coord_around

	def get_chars_around(self, coord):
		"""
		Itére sur les coordonnées autour des coordonnées spécifiées (diagonales comprises) et renvoie les char correspondants.
		Tient compte des dimensions de la matrice.
		:param coord: coordonnée (x, y) de la position dont on veut récupérer les chars alentours.
		:type coord: tuple de deux entiers.
		:return: une itération sur des string de un seul caractère
		:rtype: strings de un seul caractère, les unes après les autres.
		"""
		for coord_around in _get_coords_around(coord):
			char = self.get_char(coord_around)
			if char is not None:
				yield char

	def replace(self, before, after):
		self.char_matrix = [
			line.replace(before, after)
			for line in self.char_matrix
		]



