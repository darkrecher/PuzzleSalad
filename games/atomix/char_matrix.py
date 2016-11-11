# coding: utf-8

"""
Gestion d'un tableau de caractères en deux dimensions, un peu comme si c'était un tableau de pixels.
"""

# TODO : fonctions pour gérer des rectangles de strings comme des matrix :
#  - copie d'un rectangle de string dans un autre rectangle, à une coordonnée indiquée. On blitte pas les espaces.
#  - crop d'un rectangle de string (générique : x, y, w, h).
#  - récupération d'un char.
#  - récupération de tous les chars autour d'un char.


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
		:rtype:
			Un tuple de deux entiers
		:return:
			La largeur et la hauteur de la char_matrix.
		"""
		# On part du principe que la char_matrix est correcte. Donc on peut ne consulter que la width de la première ligne.
		# Si on n'est pas sûr que ce soit correcte, le code extérieur n'a qu'à exécuter verify_matrix.
		if len(self.char_matrix) == 0:
			return (0, 0)
		return (len(self.char_matrix[0]), len(self.char_matrix))

	def replace(self, before, after):
		self.char_matrix = [
			line.replace(before, after)
			for line in self.char_matrix
		]

