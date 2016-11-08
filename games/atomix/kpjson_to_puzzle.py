# coding: utf-8

"""
Conversion d'un fichier JSON contenant la description de niveaux "kp-atomix" vers un fichier PuzzleSalad/PuzzleScript.
"""

import json

from bat_belt import enum

FILEPATH_KPATOMIC_JSON = "draknek_levels_json.js"


ATOM = enum(
	"ATOM",
	"HYDROGEN",
	"CARBON",
	"OXYGEN",
	"NITROGEN",
	# TODO : ajouter les autres atomes
)
at = ATOM

LINK_DIR = enum(
	"LINK_DIR",
	"UP",
	"DOWN",
	"LEFT",
	"RIGHT",
	"UP_RIGHT",
	"RIGHT_DOWN",
	"DOWN_LEFT",
	"LEFT_UP",
)
ld = LINK_DIR

LINK_STRENGTH = enum(
	"LINK_STRENGTH",
	"SIMPLE",
	"DOUBLE",
	"TRIPLE",
)
ls = LINK_STRENGTH

# Correspondance. Clé : identifiant de l'atome dans les fichiers json de kp-atomix. Valeur : atome correspondant.
ATOM_FROM_KP_JSON = {
	"1" : at.HYDROGEN,
	"2" : at.CARBON,
	"3" : at.OXYGEN,
	"4" : at.NITROGEN,
}

# Correspondance des liaisons. TODO.
# liaisons simples :
# hab
# g c
# fed
# liaisons doubles (pas de diagonales) :
#  A
# D B
#  C
# liaisons triples (pas de diagonales non plus) :
#  E
# H F
#  G

# Vocabulaire des structure de données
# Un link : un tuple de deux éléments :
#  - une valeur de type enum.LINK_DIR
#  - une valeur de type enum.LINK_STRENGTH
# Un atoli (atom + link) : un tuple avec les éléments suivants :
#  - une valeur de type enum.ATOM
#  - 0, un ou plusieurs link.
# Exemple d'atoli, présent dans le niveau 8 du pack de niveau de draknek (Ethylène) : =/\
# (at.CARBON, (ld.LEFT, ls.DOUBLE), (ld.UP_RIGHT, ls.SIMPLE), (ld.RIGHT_DOWN, ls.SIMPLE))

# Correspondance entre un atoli et son caractère utilisé dans la légende de PuzzleSalad.
# clé : un atoli. valeur : une string de un seul caractère.
ps_legend_from_atoli = {}


# TODO : une fonction qui construit ps_legend_from_atoli et qui en même temps modifie data_json,
# en ajoutant à chaque définition d'atome de chaque level, le caractère de légende dans PuzzleSalad.


def read_json_file(filepath_json):
	with open(filepath_json, 'r', encoding='utf-8') as file_json:
		str_json = file_json.read()
	data_json = json.loads(str_json)
	return data_json


def main():
	print("hellow")
	kplevels_json = read_json_file(FILEPATH_KPATOMIC_JSON)
	print(kplevels_json["levels"][1])
	for level in kplevels_json["levels"]:
		for atom_key, atom_val in level["atoms"].items():
			print(atom_val)


if __name__ == '__main__':
	main()

