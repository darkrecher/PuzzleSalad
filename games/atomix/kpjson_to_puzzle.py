# coding: utf-8

"""
Conversion d'un fichier JSON contenant la description de niveaux "kp-atomix" vers un fichier PuzzleSalad/PuzzleScript.
"""

import json

from bat_belt import enum
from char_matrix import CharMatrix, filled_chars

FILEPATH_KPATOMIC_JSON = "draknek_levels_json.js"

# Tous les symboles de bases, dans kpjson et PuzzleSalad.
KPJSON_SYMB_WALL = '#'
PS_SYMB_WALL = '#'
KPJSON_SYMB_EMPTY = '.'
PS_SYMB_EMPTY = '.'
PS_SYMB_PLAYER = '*'
SYMB_TRANSPARENT = ' '

ATOM = enum(
	'ATOM',
	'HYDROGEN',
	'CARBON',
	'OXYGEN',
	'NITROGEN',
	'SULFUR',
	'FLUORINE',
	'CHLORINE',
	'CRISTAL',
	'PHOSPHORE',
	'EMPTYATOM',
)
at = ATOM

LINK_DIR = enum(
	'LINK_DIR',
	'UP',
	'DOWN',
	'LEFT',
	'RIGHT',
	'UP_RIGHT',
	'DOWN_RIGHT',
	'UP_LEFT',
	'DOWN_LEFT',
)
ld = LINK_DIR

LINK_STRENGTH = enum(
	'LINK_STRENGTH',
	'SIMPLE',
	'DOUBLE',
	'TRIPLE',
)
ls = LINK_STRENGTH

# Correspondance. Clé : identifiant de l'atome dans les fichiers json de kp-atomix. Valeur : atome correspondant.
ATOM_FROM_KP_JSON = {
	'1' : at.HYDROGEN,
	'2' : at.CARBON,
	'3' : at.OXYGEN,
	'4' : at.NITROGEN,
	'5' : at.SULFUR,
	'6' : at.FLUORINE,
	'7' : at.CHLORINE,
	# Y'a pas de 8. Je n'ai pas trouvé d'exemple dans les fichiers kpjson que je connais. (source : http://figlief.pythonanywhere.com/)
	'9' : at.PHOSPHORE,
	'o' : at.CRISTAL,
	'A' : at.EMPTYATOM, # FUTURE : les EmptyAtom sont représentés bizarrement dans les fichiers kpjson. Ça n'a pas encore été testé.
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
	'a' : (ld.UP, ls.SIMPLE),
	'b' : (ld.UP_RIGHT, ls.SIMPLE),
	'c' : (ld.RIGHT, ls.SIMPLE),
	'd' : (ld.DOWN_RIGHT, ls.SIMPLE),
	'e' : (ld.DOWN, ls.SIMPLE),
	'f' : (ld.DOWN_LEFT, ls.SIMPLE),
	'g' : (ld.LEFT, ls.SIMPLE),
	'h' : (ld.UP_LEFT, ls.SIMPLE),
	'A' : (ld.UP, ls.DOUBLE),
	'B' : (ld.RIGHT, ls.DOUBLE),
	'C' : (ld.DOWN, ls.DOUBLE),
	'D' : (ld.LEFT, ls.DOUBLE),
	'E' : (ld.UP, ls.TRIPLE),
	'F' : (ld.RIGHT, ls.TRIPLE),
	'G' : (ld.DOWN, ls.TRIPLE),
	'H' : (ld.LEFT, ls.TRIPLE),
}

PS_NAME_FROM_ATOM = {
	at.HYDROGEN : 'Hydrogen',
	at.CARBON : 'Carbon',
	at.OXYGEN : 'Oxygen',
	at.NITROGEN : 'Nitrogen',
	at.SULFUR : 'Sulfur',
	at.FLUORINE : 'Fluorine',
	at.CHLORINE : 'Chlorine',
	at.PHOSPHORE : 'Phosphore',
	at.CRISTAL : 'Cristal',
	at.EMPTYATOM : 'EmptyAtom',
}

PS_NAME_FROM_LINK = {
	(ld.UP, ls.SIMPLE) : 'LinkUpSimple',
	(ld.UP_RIGHT, ls.SIMPLE) : 'LinkUpRightSimple',
	(ld.RIGHT, ls.SIMPLE) : 'LinkRightSimple',
	(ld.DOWN_RIGHT, ls.SIMPLE) : 'LinkDownRightSimple',
	(ld.DOWN, ls.SIMPLE) : 'LinkDownSimple',
	(ld.DOWN_LEFT, ls.SIMPLE) : 'LinkDownLeftSimple',
	(ld.LEFT, ls.SIMPLE) : 'LinkLeftSimple',
	(ld.UP_LEFT, ls.SIMPLE) : 'LinkUpLeftSimple',
	(ld.UP, ls.DOUBLE) : 'LinkUpDouble',
	(ld.RIGHT, ls.DOUBLE) : 'LinkRightDouble',
	(ld.DOWN, ls.DOUBLE) : 'LinkDownDouble',
	(ld.LEFT, ls.DOUBLE) : 'LinkLeftDouble',
	(ld.UP, ls.TRIPLE) : 'LinkUpTriple',
	(ld.RIGHT, ls.TRIPLE) : 'LinkRightTriple',
	(ld.DOWN, ls.TRIPLE) : 'LinkDownTriple',
	(ld.LEFT, ls.TRIPLE) : 'LinkLeftTriple',
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

# Représentation, dans PuzzleSalad, du background d'un level.
# Il comporte des barres obliques bleues, coupées à certains endroits, pour reproduire l'aspect du jeu Atomix original.
# Du point de vue des règles de Atomix dans PuzzleSalad, ces barres obliques se comportent comme des objets "Walls".
# Donc ça n'a aucune influence sur le jeu lui-même. (Pour plus de détails, voir fichier atomix.puz)
CM_BACKGROUND_DIAGONAL_BARS = CharMatrix(
	[
		"/+,,,-\\,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%",
		"%\\/+,/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\",
		"\\/%\\/%\\/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/",
		"/%\\/%\\/%\\,,,,/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%",
		"%\\/%\\/%\\/+,,,-\\,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\",
		"\\/%\\/%\\/%\\/+,/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/",
		"/%\\/%\\/%\\/%\\/%\\/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%",
		"%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\,,,,/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/",
		"/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%",
		"%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\,-\\/%\\/%\\/%\\/%\\/%\\/%\\",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,/+,,,-\\/%\\/%\\/%\\/%\\/%\\/",
		"/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\,,,,/%\\/%\\/%\\/%\\/%\\/%",
		"%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\,-\\/%\\/%\\/%\\/%\\",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,/+,,,-\\,-\\/%\\/%\\/",
		"/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,,,/%\\/%\\/%",
		"%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\/%\\/%\\",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\/%\\/",
		"/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\,,,,/%\\/%",
		"%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,,,-\\,-\\",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,/+,,,",
		"/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/+,",
		"%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/%\\/",
	]
)

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

def get_forbidden_chars(cm_background):
	"""
	RECTODO : docstring
	Exemple de caractères interdits () : #.*,/%\-+
	Détermine les caractères interdit à partir de la ps_legend en dur.
	Enlève aussi les caractères présents dans le backround.
	(c'est expliqué dans le mauvais sens)
	"""
	unique_chars = list(cm_background.get_unique_chars())
	unique_chars.extend([PS_SYMB_WALL, PS_SYMB_EMPTY, PS_SYMB_PLAYER])
	return unique_chars

def generator_ps_legend_characters(forbidden_chars):
	"""
	RECTODO : docstring
	"""
	# Caractères systématiquement interdits par PuzzleSalad, car faisant partie de la syntaxe du langage :
	# []() =<>-V^
	# La lettre "V" toute seule (minuscule ou majuscule) est interdite car elle représente la flèche vers le bas.
	# Ces caractères ne sont pas présents dans PS_LEGEND_CHARS.
	PS_LEGEND_CHARS = list(
		'abcdefghijklmnopqrstuwxyz0123456789{}_;:?!$&\'"#.*,/%\-+'
	)
	# FUTURE. C'est vilain de précalculer la liste des chars autorisés.
	# Ce serait plus "lazy-pythonien" de vérifier à chaque fois qu'il faut sortir le prochain caractère.
	ps_legend_chars_filtered = [
		char for char in PS_LEGEND_CHARS
		if char not in forbidden_chars
	]
	while ps_legend_chars_filtered:
		yield(ps_legend_chars_filtered.pop(0))
	raise Exception("Plus assez de caractères pour définir tous les atoli (combinaison atom + link) dans la partie 'légende' de PuzzleSalad.")

def get_positions_background_cropping(cm_background, char_spot, enable_around):
	"""
	Itère sur un ensemble de positions dans cm_background.
	Il s'agit de toutes les positions des cellules ayant le caractère char_spot,
	ainsi que les positions adjacentes (diagonales comprises) à ces positions char_spot.
	Chaque position n'est itérée qu'une seule fois, même si elle est adjacente à plusieurs char_spot.
	Cette fonction est utilisé pour lister les positions intéressantes du background comportant les barres obliques bleues.
	C'est intéressant aux endroits où les barres sont coupées (ça fait plus de diversité dans le background).
	Chaque level sera ensuite blitté sur l'une des parties intéressantes de ce background.
	"""
	existing_positions = []
	for pos in cm_background.get_char_positions(char_spot):
		if pos not in existing_positions:
			existing_positions.append(pos)
			yield pos
		for pos_around in cm_background.get_coords_around(pos):
			if pos_around not in existing_positions:
				existing_positions.append(pos_around)
				yield pos_around

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

def external_empty_tiles_transparented(cm_arena):
	"""
	Remplace les caractères de cases vides '.' qui sont à l'extérieur de l'arène, par des caractères de transparence ' '.
	RECTODO : docstring plus précise.
	"""
	# Algo (bourrin, mais osef) :
	#  - créer un CharMatrix avec que des espaces dedans, de dimensions (arena+2)
	#  - blitter l'arena dans ce CharMatrix, pour créer une "bordered arena" (cm_brd_arena).
	#  - parcourir les cases, plusieurs fois. changer en espace tous les '.' ayant au moins un espace autour.
	#    À refaire sur toute la CharMatrix, tant qu'on a fait au moins une transformation.
	#  - recropper la CharMatrix pour enlever les cases d'espaces environnantes.
	# FUTURE : ça risque de merder à cause des diagonales. En fait, faudrait pas propager la transparence avec les diagonales.
	# Et donc il faudrait une fonction get_chars_around qui ne prenne pas les diagonales. On fera ça plus tard.
	arena_w, arena_h = cm_arena.dimensions()
	cm_brd_arena = CharMatrix(
		filled_chars(SYMB_TRANSPARENT, (arena_w+2, arena_h+2)),
		SYMB_TRANSPARENT
	)
	cm_brd_arena.blit(cm_arena, (1, 1))
	change_made = True
	while change_made:
		change_made = False
		for pos_empty_tile in cm_brd_arena.get_char_positions(PS_SYMB_EMPTY):
			chars_around = cm_brd_arena.get_chars_around(pos_empty_tile)
			if SYMB_TRANSPARENT in chars_around:
				change_made = True
				# Du coup, on modifie l'arena alors qu'on est en train d'itérer dessus avec un filtre.
				# C'est pas génial, mais ça posera pas de problème,
				# vu qu'on modifie l'élément sur lequel on vient juste d'itérer.
				cm_brd_arena.set_char(pos_empty_tile, SYMB_TRANSPARENT)
	cm_arena_transparented = cm_brd_arena.cropped((1, 1), (arena_w, arena_h))
	return cm_arena_transparented

def transparencify_tiles_surrounded(cm_arena):
	"""
	mettre des espaces sur toutes les cases entourées de murs ou d'espace.
	 - parcourir l'arena (une seule fois). Tous les murs entourés uniquement de murs et d'espaces deviennent des espaces.
	 # RECTODO : docstring plus précise.
	"""
	# FUTURE : c'est pas homogène avec la fonction précédente. Celle-ci modifie in-place.
	# external_empty_tiles_transparented renvoie une CharMatrix modifiée.
	wall_and_transp = {'#', ' '}
	for pos_wall_tile in cm_arena.get_char_positions(PS_SYMB_WALL):
		set_chars_around = set(cm_arena.get_chars_around(pos_wall_tile))
		if set.union(wall_and_transp, set_chars_around) == wall_and_transp:
			cm_arena.set_char(pos_wall_tile, SYMB_TRANSPARENT)

def almost_random(str_seed, max):
	"""
	Génère un nombre "à peu près" aléatoire, mais pas tant que ça. (Il est "aléatoirement" aléatoire).
	La génération aléatoire est faite à partir de str_seed uniquement.
	Si on exécute plusieurs fois la fonction avec les mêmes paramètres, on récupère à chaque fois le même nombre aléatoire.
	:param str_seed: texte quelconque utilisé pour générer le nombre aléatoire.
	:param max: le nombre aléatoire sera compris entre 0 et max-1.
	:type str_seed: string.
	:type max: entier.
	:return: le nombre aléatoire.
	:rtype: entier.
	"""
	# Broumf broumf... "Aléatoire". On va dire que ça l'est...
	random_value = sum((ord(char) for char in str_seed))
	return random_value % max

def build_ps_level(
	kpjson_level_legendified,
	ps_legend_from_atoli,
	cm_background,
	transparencify=False,
	interesting_positions=None
):
	"""
	Renvoie un CharMatrix correspondant à la représentation dans PuzzleSalad du level d'atomix spécifié (kpjson_level_legendified).
	RECTODO : docstring plus précise.
	"""

	atoms_legendified = kpjson_level_legendified['atoms']
	cm_arena = CharMatrix(kpjson_level_legendified['arena'], SYMB_TRANSPARENT)
	cm_model = CharMatrix(kpjson_level_legendified['molecule'])
	cm_arena.verify_matrix()
	cm_model.verify_matrix()

	kpjson_chars = ''
	ps_legend_chars = ''
	for atom_key, atom_legendified in atoms_legendified.items():
		kpjson_chars += atom_key
		ps_legend_chars += ps_legend_from_atoli[atom_legendified[-1]]
	kpjson_chars += KPJSON_SYMB_WALL + KPJSON_SYMB_EMPTY
	ps_legend_chars += PS_SYMB_WALL + PS_SYMB_EMPTY
	cm_arena.translate(kpjson_chars, ps_legend_chars)
	cm_model.translate(kpjson_chars, ps_legend_chars)

	arena_w, arena_h = cm_arena.dimensions()
	model_w, model_h = cm_model.dimensions()
	global_w = 2 + model_w + 2 + arena_w + 2
	global_h = 2 + max(model_h, arena_h) + 2
	cm_background.in_dimensions((global_w-1, global_h-1), True)

	if transparencify:
		cm_arena = external_empty_tiles_transparented(cm_arena)
		transparencify_tiles_surrounded(cm_arena)

	# Placement du joueur où on peut (là où y'a ni mur ni atome), en prenant plus ou moins le milieu de l'arena.
	empty_tile_positions = tuple(cm_arena.get_char_positions(PS_SYMB_EMPTY))
	if not empty_tile_positions:
		raise Exception(''.join((
			"Niveau : ",
			kpjson_level_legendified['name'],
			"Il faut au moins une case vide pour placer le joueur.",
		)))
	player_position = empty_tile_positions[len(empty_tile_positions) // 2]
	cm_arena.set_char(player_position, PS_SYMB_PLAYER)

	if interesting_positions is None:
		# FUTURE : si le background est trop petit pour ce niveau, ça va raiser une exception plus tard
		# (au moment du cropping). Ce serait plus gentil de la raiser un peu avant, avec un message plus explicite.
		pos_crop_bg = (0, 0)
	else:
		# On croppe depuis un autre endroit que le coin sup gauche,
		# pour avoir des backgrounds différents à chaque level.
		background_w, background_h = cm_background.dimensions()
		limit_x, limit_y = background_w-global_w, background_h-global_h
		possible_pos = [
			pos for pos in interesting_positions
			if pos[0] <= limit_x and pos[1] <= limit_y
		]
		if not possible_pos:
			raise Exception(''.join((
				"Niveau : ",
				kpjson_level_legendified['name'],
				"Le background est trop petit pour ce niveau.",
			)))
		# Choix d'une pos parmi les possible_pos, en prenant un index pseudo-random, basé sur le nom du level.
		# C'est pas du vrai random, mais c'est pas grave.
		index_pos_crop_bg = almost_random(
			kpjson_level_legendified['name'],
			len(possible_pos))
		pos_crop_bg = possible_pos[index_pos_crop_bg]

	ps_level_map = cm_background.cropped(pos_crop_bg, (global_w, global_h))
	model_pos_up_left = (2, global_h-model_h-2)
	arena_pos_up_left = (2+model_w+2, 2)
	ps_level_map.blit(cm_model, model_pos_up_left)
	ps_level_map.blit(cm_arena, arena_pos_up_left)
	return ps_level_map

def str_from_atoli(atoli):
	atom, links = atoli
	str_atom = PS_NAME_FROM_ATOM[atom]
	str_links = [ PS_NAME_FROM_LINK[link] for link in links ]
	return ' and '.join([str_atom] + str_links)

def str_ps_legend(ps_legend_from_atoli):
	str_ps_legend_atoms = [
		'%s = %s' % (ps_legend_char, str_from_atoli(atoli))
		for atoli, ps_legend_char
		in ps_legend_from_atoli.items()
	]
	str_ps_legend_atoms.sort()
	return '\n'.join(str_ps_legend_atoms)

def read_json_file(filepath_json):
	with open(filepath_json, 'r', encoding='utf-8') as file_json:
		str_json = file_json.read()
	data_json = json.loads(str_json)
	return data_json


def main():

	# RECTODO : virer tout ce bastringue.
	# mettre en dur l'ordre des levels dans un autre fichier json.
	# itérer dans l'ordre spécifié, ou bien dans l'ordre simple si c'est pas spécifié
	# paramètre de la commande : fichier des levels, fichier d'ordre des levels (facultatif), background mur/noir/barres (facultatif, barres).

	# FUTURE : déterminer la longueur et hauteur max parmi les levels à faire, et générer le background mur ou noir selon ces dimensions max,
	# afin qu'il n'y ait plus de limite de taille pour les background simple.
	# Pour le background de barre obliques, la limite est toujours présentes.
	# FUTURE : générer automatiquement un background de barre obliques selon les dimensions demandées.
	# Pour ne plus avoir de limites même avec les barres obliques.

	print("hellow")
	first = True
	kplevels_json = read_json_file(FILEPATH_KPATOMIC_JSON)
	ps_legend_characters = generator_ps_legend_characters()

	for level in kplevels_json['levels']:
		for atom_key, kpjson_atom in level['atoms'].items():
			legendify_atoli(kpjson_atom, ps_legend_from_atoli, ps_legend_characters)

	print("")
	print("Légende des atoli")
	for atoli, ps_legend_char in ps_legend_from_atoli.items():
		print(ps_legend_char, ":", atoli)

	print("")
	print("Liste des atomes des levels, avec atoli correspondant")
	for level in kplevels_json['levels']:
		for atom_key, kpjson_atom in level['atoms'].items():
			print(kpjson_atom, " : ", ps_legend_from_atoli[kpjson_atom[2]])

	ps_level = build_ps_level(
		kplevels_json['levels'][0],
		ps_legend_from_atoli,
		CM_BACKGROUND_WALLS
	)
	print(str_ps_legend(ps_legend_from_atoli))
	print("")
	print(ps_level)


if __name__ == '__main__':
	main()

