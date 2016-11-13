# coding: utf-8

"""
Conversion d'un fichier JSON contenant la description de niveaux "kp-atomix" vers un fichier PuzzleSalad/PuzzleScript.
"""

import json

from bat_belt import enum
from char_matrix import CharMatrix

FILEPATH_KPATOMIC_JSON = "draknek_levels_json.js"
CM_BACKGROUND_WALLS = CharMatrix(['#' * 100] * 100)

ATOM = enum(
	"ATOM",
	"HYDROGEN",
	"CARBON",
	"OXYGEN",
	"NITROGEN",
	# RECTODO : ajouter les autres atomes
)
at = ATOM

LINK_DIR = enum(
	"LINK_DIR",
	"UP",
	"DOWN",
	"LEFT",
	"RIGHT",
	"UP_RIGHT",
	"DOWN_RIGHT",
	"UP_LEFT",
	"DOWN_LEFT",
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
	# RECTODO : ajouter les autres atomes ici aussi
}

# Correspondance. Clé : identifiant du link dans les fichiers json de kp-atomix. Valeur : link correspondant.
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
LINK_FROM_KP_JSON = {
	"a" : (ld.UP, ls.SIMPLE),
	"b" : (ld.UP_RIGHT, ls.SIMPLE),
	"c" : (ld.RIGHT, ls.SIMPLE),
	"d" : (ld.DOWN_RIGHT, ls.SIMPLE),
	"e" : (ld.DOWN, ls.SIMPLE),
	"f" : (ld.DOWN_LEFT, ls.SIMPLE),
	"g" : (ld.LEFT, ls.SIMPLE),
	"h" : (ld.UP_LEFT, ls.SIMPLE),
	"A" : (ld.UP, ls.DOUBLE),
	"B" : (ld.RIGHT, ls.DOUBLE),
	"C" : (ld.DOWN, ls.DOUBLE),
	"D" : (ld.LEFT, ls.DOUBLE),
	"E" : (ld.UP, ls.TRIPLE),
	"F" : (ld.RIGHT, ls.TRIPLE),
	"G" : (ld.DOWN, ls.TRIPLE),
	"H" : (ld.LEFT, ls.TRIPLE),
}

# Vocabulaire des structure de données
# Un link : un tuple de deux éléments :
#  - une valeur de type enum.LINK_DIR
#  - une valeur de type enum.LINK_STRENGTH
# Un atoli (atom + link) : un tuple avec les éléments suivants :
#  - une valeur de type enum.ATOM
#  - 0, un ou plusieurs link.
# Exemple d'atoli, présent dans le niveau 8 du pack de niveau de draknek (Ethylène) : =/\
# (at.CARBON, (ld.LEFT, ls.DOUBLE), (ld.UP_RIGHT, ls.SIMPLE), (ld.DOWN_RIGHT, ls.SIMPLE))

def atoli_from_kpjson(kpjson_atom):
	# Ça va thrower des exception si le json contient un identifant d'atome ou de link inconnu.
	# C'est ce qu'on veut. (Car on veut pas s'embêter à gérer un message d'erreur spécifique pour ça).
	atom = ATOM_FROM_KP_JSON[kpjson_atom[0]]
	links = tuple(
		LINK_FROM_KP_JSON[data_kpjson_link]
		for data_kpjson_link
		in kpjson_atom[1]
	)
	return (atom, links)

def generator_ps_legend_characters():
	# Charactères interdits : #.*,/%\-+
	# RECTODO : determiner les charactères interdit à partir de la ps_legend en dur (qui n'est pas encore faite).
	PS_LEGEND_CHARACTERS = list("abcdefghijklmnopqrstuvwxyz0123456789={}_;:?!$&'\"")
	while PS_LEGEND_CHARACTERS:
		yield(PS_LEGEND_CHARACTERS.pop(0))
	raise Exception("Plus assez de caractères pour définir tous les atoli (combinaison atom + link) dans la partie 'légende' de PuzzleSalad.")

# Correspondance entre un atoli et son caractère utilisé dans la légende de PuzzleSalad.
# clé : un atoli. valeur : une string de un seul caractère.
ps_legend_from_atoli = {}

def legendify_atoli(kpjson_atom, ps_legend_from_atoli, ps_legend_characters):
	"""
	Effectue deux actions :
	 - Ajout d'un élément dans ps_legend_from_atoli, si nécessaire.
	 - Modifie kpjson_atom, en ajoutant au bout de la liste l'atoli correspondant.
	"""
	atoli = atoli_from_kpjson(kpjson_atom)
	if not atoli in ps_legend_from_atoli:
		ps_legend_char = next(ps_legend_characters)
		ps_legend_from_atoli[atoli] = ps_legend_char
	kpjson_atom.append(atoli)

def build_ps_level(kpjson_level_legendified, ps_legend_from_atoli, cm_background):
	"""
	Renvoie un CharMatrix correspondant à la représentation dans PuzzleSalad du level d'atomix spécifié (kpjson_level_legendified).
	RECTODO : docstring plus précise.
	"""

	atoms_legendified = kpjson_level_legendified["atoms"]
	cm_arena = CharMatrix(kpjson_level_legendified["arena"], ' ')
	cm_model = CharMatrix(kpjson_level_legendified["molecule"])
	cm_arena.verify_matrix()
	cm_model.verify_matrix()
	kpjson_atoms = ""
	ps_legend_atoms = ""
	for atom_key, atom_legendified in atoms_legendified.items():
		kpjson_atoms += atom_key
		ps_legend_atoms += ps_legend_from_atoli[atom_legendified[-1]]

	cm_arena.translate(kpjson_atoms, ps_legend_atoms)
	cm_model.translate(kpjson_atoms, ps_legend_atoms)

	arena_w, arena_h = cm_arena.dimensions()
	model_w, model_h = cm_model.dimensions()
	global_w = 2 + model_w + 2 + arena_w + 2
	global_h = 2 + max(model_h, arena_h) + 2
	cm_background.in_dimensions((global_w-1, global_h-1), True)

	# RECTODO : mettre des caractères espaces sur les cases extérieures
	# remplacer par un espace les murs entourés entièrement de murs. (mais c'est pas exactement ça).

	# RECTODO : placement du joueur où on peut (là où y'a ni mur ni atome), en cherchant en priorité au milieu de l'arena.

	model_pos_up_left = (2, global_h-model_h-2)
	arena_pos_up_left = (2+model_w+2, 2)
	# RECTODO : cropper depuis un autre endroit que le coin sup gauche, pour avoir des background différents selon les niveaux.
	ps_level_map = cm_background.cropped((0, 0), (global_w, global_h))
	ps_level_map.blit(cm_model, model_pos_up_left)
	ps_level_map.blit(cm_arena, arena_pos_up_left)
	return ps_level_map

def read_json_file(filepath_json):
	with open(filepath_json, 'r', encoding='utf-8') as file_json:
		str_json = file_json.read()
	data_json = json.loads(str_json)
	return data_json


def main():

	print("hellow")
	first = True
	kplevels_json = read_json_file(FILEPATH_KPATOMIC_JSON)
	ps_legend_characters = generator_ps_legend_characters()

	for level in kplevels_json["levels"]:
		for atom_key, kpjson_atom in level["atoms"].items():
			legendify_atoli(kpjson_atom, ps_legend_from_atoli, ps_legend_characters)

	print("")
	print("Légende des atoli")
	for atoli, ps_legend_char in ps_legend_from_atoli.items():
		print(ps_legend_char, ":", atoli)

	print("")
	print("Liste des atomes des levels, avec atoli correspondant")
	for level in kplevels_json["levels"]:
		for atom_key, kpjson_atom in level["atoms"].items():
			print(kpjson_atom, " : ", ps_legend_from_atoli[kpjson_atom[2]])

	ps_level = build_ps_level(
		kplevels_json["levels"][0],
		ps_legend_from_atoli,
		CM_BACKGROUND_WALLS
	)
	print(ps_level)

if __name__ == '__main__':
	main()

