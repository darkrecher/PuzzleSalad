# coding: utf-8

"""
Gestion d'un tableau de caractères en deux dimensions, un peu comme si c'était un tableau de pixels.
"""

import re


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

	def __init__(self, char_matrix, transparent_char=None):
		"""
		:param char_matrix:
			Tableau de caractères en deux dimensions, représentant le contenu de la matrice.
			(Un caractère = une cellule).
		:param transparent_char:
			Caractère définissant la transparence. Utilisé par la fonction blit().
			Si None : cette matrice n'a pas de transparence et sera blittée intégralement sur la matrice de destination.
		:type char_matrix:
			Liste de strings. Toutes les strings sont censées avoir la même taille.
			Pour le vérifier, utiliser la fonction self.verify_matrix().
		:type transparent_char:
			String de un seul caractère, ou None.
		"""
		self.char_matrix = char_matrix
		self.transparent_char = transparent_char

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
				raise Exception("".join((
					"La ligne suivante n'a pas la bonne longueur : ",
					 str(line))
				))

	def dimensions(self):
		"""
		:return: la largeur et la hauteur de la char_matrix.
		:rtype: un tuple de deux entiers positifs ou nuls.
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
		:return: une itération sur des coordonnées.
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

	def translate(self, intab, outtab):
		"""
		Remplace des chars par d'autres sur l'ensemble de la matrice.
		Voir built-in fonction str.translate.
		:param intab: string contenant les caractères de départ, ceux qu'il faut remplacer.
		:param outtab: string contenant les caractères d'arrivée, ceux qui seront mis à la place de ceux remplacés.
		:type intab: string. Le nombre de caractères doit être le même dans intab et outtab.
		:type outtab: string. Le nombre de caractères doit être le même dans intab et outtab.
		"""
		translation_tab = str.maketrans(intab, outtab)
		self.char_matrix = [
			line.translate(translation_tab)
			for line in self.char_matrix
		]

	def cropped(self, corner_up_left, dimensions):
		"""
		Renvoie une partie de la matrice. Génère une exception si les paramètres spécifiés sont hors limite de la matrice.
		:param corner_up_left: cordonnées (x, y) du coin haut gauche de la partie de matrice demandée.
		:param dimensions: taille (largeur, hauteur) de la partie de matrice demandée.
		:type corner_up_left: tuple de deux entiers.
		:type dimensions: tuple de deux entiers positifs ou nuls.
		:return: la matrice demandée.
		:rtype: instance de CharMatrix.
		"""
		# FUTUR : repositionner le corner_up_left et/ou diminuer les dimensions si elles sont hors limites,
		# afin de renvoyer la partie existante de la matrice, au lieu de raiser des exceptions comme un bourrin.
		self.in_dimensions(corner_up_left, True)
		corner_down_right = (
			corner_up_left[0] + dimensions[0] - 1,
			corner_up_left[1] + dimensions[1] - 1)
		self.in_dimensions(corner_down_right, True)
		x1, y1 = corner_up_left
		x2, y2 = corner_down_right
		str_cropped = [
			line[x1:x2+1]
			for line
			in self.char_matrix[y1:y2+1]
		]
		return CharMatrix(str_cropped)

	def blit(self, source_matrix, corner_up_left):
		"""
		Modifie la matrice en y recopiant dedans la source_matrix, aux coordonnées spécifiées.
		Si source_matrix possède un transparent_char différent de None, tous les caractères de source_matrix égaux à transparent_char
		ne seront pas recopiés. (Comme si c'était des pixels transparents).
		:param source_matrix: la matrice à recopier.
		:param corner_up_left: cordonnées (x, y) du coin haut gauche, dans self.char_matrix, où sera recopié source_matrix.
		:type corner_up_left: tuple de deux entiers.
		:type source_matrix: instance de CharMatrix.
		"""
		# FUTUR : blitter une source_matrix cropped au cas où le corner_up_left et/ou les dimensions sont hors limites,
		# au lieu de raiser des exceptions comme un bourrin.
		# D'ailleurs, je raise même pas tout ce que je pourrais raiser. Bon, bref...
		self.in_dimensions(corner_up_left, True)
		dimensions = source_matrix.dimensions()
		for y_source in range(dimensions[1]):
			line_source = source_matrix.char_matrix[y_source]
			y_dest = corner_up_left[1] + y_source
			unpacked_line_dest = list(self.char_matrix[y_dest])
			for x_source in range(dimensions[0]):
				char_source = line_source[x_source]
				if char_source != source_matrix.transparent_char:
					x_dest = x_source + corner_up_left[0]
					unpacked_line_dest[x_dest] = char_source
			line_dest = "".join(unpacked_line_dest)
			self.char_matrix[y_dest] = line_dest

	def get_char_positions(self, char):
		"""
		Itère sur les positions (x, y) de toutes les occurrences de char dans self.char_matrix
		:param char: le caractère à chercher.
		:type char: string de un seul caractère.
		:return: une itération sur des coordonnées.
		:rtype: tuples de deux entiers, les uns après les autres.
		"""
		for y, line in enumerate(self.char_matrix):
			# http://stackoverflow.com/a/13009866/6241709
			# http://stackoverflow.com/questions/4202538/python-escape-regex-special-characters
			for x in re.finditer(re.escape(char), line):
				yield(x.start(), y)
