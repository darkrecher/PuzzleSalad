# coding: utf-8

import json

from char_matrix import CharMatrix, filled_chars
from kpjson_to_puzzle import (
	PS_SYMB_WALL, CM_BACKGROUND_DIAGONAL_BARS,
	generator_ps_legend_characters, legendify_atoli,
	get_positions_background_cropping, almost_random,
	str_ps_legend, build_ps_level,
)

def test_get_positions_background_cropping():
	cm_background = CharMatrix(["--....", ".-....", "......", ".....-"])
	iter_pos = get_positions_background_cropping(cm_background, '-', True)
	positions_data = list(iter_pos)
	positions_reference = [
		(0, 0), (1, 0), (2, 0),
		(0, 1), (1, 1), (2, 1),
		(0, 2), (1, 2), (2, 2),
		(4, 2), (5, 2),
		(4, 3), (5, 3),
	]
	# On trie avant de comparer, parce qu'on se fiche complètement de l'ordre dans lequel ça arrive,
	# et on n'a pas envie de tester ça.
	assert sorted(positions_data) == sorted(positions_reference)

def test_almost_random():
	assert almost_random("Blarg", 50) == 38
	assert almost_random("Blarg", 10000) == 488

def test_kpjson_to_puzzle_on_walls():
	"""
	Test de génération d'un seul level, sans les ajouts d'espaces, et sur le background de walls.
	"""

	CM_BACKGROUND_WALLS = CharMatrix(filled_chars(PS_SYMB_WALL, (100, 100)))
	kplevel_str = """
	{
		"name": "Formaldehyde",
		"id": "1",
		"atoms": {
			"1": ["3", "B"],
			"2": ["2", "Dbd"],
			"3": ["1", "f"],
			"4": ["1", "h"]
		},
		"arena": [
			"...####",
			"...#.3#",
			"####..#",
			"#..2.1#",
			"####..#",
			"...#.4#",
			"...####"
		],
		"molecule": [
			"..3",
			"12.",
			"..4"
		]
	}
	"""

	kplevel_json = json.loads(kplevel_str)
	ps_legend_characters = generator_ps_legend_characters()
	ps_legend_from_atoli = {}
	for atom_key in sorted(kplevel_json["atoms"]):
		kpjson_atom = kplevel_json["atoms"][atom_key]
		legendify_atoli(
			kpjson_atom,
			ps_legend_from_atoli,
			ps_legend_characters
		)
	assert str_ps_legend(ps_legend_from_atoli) == '\n'.join((
		"a = Oxygen and LinkRightDouble",
		"b = Carbon and LinkLeftDouble and LinkUpRightSimple and LinkDownRightSimple",
		"c = Hydrogen and LinkDownLeftSimple",
		"d = Hydrogen and LinkUpLeftSimple",
	))
	ps_level = build_ps_level(
		kplevel_json,
		ps_legend_from_atoli,
		CM_BACKGROUND_WALLS
	)
	assert str(ps_level) == '\n'.join((
		"################",
		"################",
		"#######...######",
		"#######...#.c###",
		"###########..###",
		"########.*b.a###",
		"##..c######..###",
		"##ab.##...#.d###",
		"##..d##...######",
		"################",
		"################",
	))


def test_kpjson_to_puzzle_with_transparency():
	"""
	un test avec les ajouts d'espace, et sur le background de barres obliques, avec le cropping positionné en semi-random.
	"""

	CM_BACKGROUND_WALLS_BLACK = CharMatrix(filled_chars(',', (100, 100)))
	kplevel_str = """
	{
		"name": "Dihydrogen",
		"id": "1",
		"atoms": {
			"1": ["3", "B"],
			"2": ["3", "D"]
		},
		"arena": [
			"...######...",
			"..##..21##..",
			"###......###",
			"#...####...#",
			"#...####...#",
			"#...####...#",
			"###......###",
			"..##....##..",
			"...######..."
		],
		"molecule": [
			"12"
		]
	}
	"""

	kplevel_json = json.loads(kplevel_str)
	ps_legend_characters = generator_ps_legend_characters()
	ps_legend_from_atoli = {}
	for atom_key in sorted(kplevel_json["atoms"]):
		kpjson_atom = kplevel_json["atoms"][atom_key]
		legendify_atoli(
			kpjson_atom,
			ps_legend_from_atoli,
			ps_legend_characters
		)
	ps_level = build_ps_level(
		kplevel_json,
		ps_legend_from_atoli,
		CM_BACKGROUND_WALLS_BLACK,
		True
	)
	assert str(ps_level) == '\n'.join((
		",,,,,,,,,,,,,,,,,,,,",
		",,,,,,,,,,,,,,,,,,,,",
		",,,,,,,,,######,,,,,",
		",,,,,,,,##..ba##,,,,",
		",,,,,,###......###,,",
		",,,,,,#...####...#,,",
		",,,,,,#...#,,#.*.#,,",
		",,,,,,#...####...#,,",
		",,,,,,###......###,,",
		",,,,,,,,##....##,,,,",
		",,ab,,,,,######,,,,,",
		",,,,,,,,,,,,,,,,,,,,",
		",,,,,,,,,,,,,,,,,,,,",
	))

def test_kpjson_to_puzzle_with_pretty_background():
	"""
	Test avec les ajouts d'espace, et sur un background de virgules.
	"""

	CM_BACKGROUND_WALLS_BLACK = CharMatrix(filled_chars(',', (100, 100)))
	kplevel_str = """
	{
		"name": "Dihydrogen",
		"id": "1",
		"atoms": {
			"1": ["3", "B"],
			"2": ["3", "D"]
		},
		"arena": [
			"...######...",
			"..##..21##..",
			"###......###",
			"#...####...#",
			"#...####...#",
			"#...####...#",
			"###......###",
			"..##....##..",
			"...######..."
		],
		"molecule": [
			"12"
		]
	}
	"""

	kplevel_json = json.loads(kplevel_str)
	ps_legend_characters = generator_ps_legend_characters()
	ps_legend_from_atoli = {}
	for atom_key in sorted(kplevel_json["atoms"]):
		kpjson_atom = kplevel_json["atoms"][atom_key]
		legendify_atoli(
			kpjson_atom,
			ps_legend_from_atoli,
			ps_legend_characters
		)
	interesting_positions = list(get_positions_background_cropping(
		CM_BACKGROUND_DIAGONAL_BARS,
		'-',
		True
	))
	ps_level = build_ps_level(
		kplevel_json,
		ps_legend_from_atoli,
		CM_BACKGROUND_DIAGONAL_BARS,
		True,
		interesting_positions
	)
	assert str(ps_level) == '\n'.join((
		",,/%\\/%\\/%\\/%\\/%\\/%\\",
		",,-\\,-\\/%\\/%\\/%\\/%\\/",
		"+,/+,,,-\\######/%\\/%",
		"\\/%\\/+,,##..ba##\\/%\\",
		"/%\\/%\\###......###\\/",
		"%\\/%\\/#...####...#/%",
		"\\/%\\/%#...#,-#.*.#%\\",
		"/%\\/%\\#...####...#\\/",
		"%\\/%\\/###......###,-",
		"\\/%\\/%\\/##....##,,,,",
		"/%ab%\\/%\\######/+,,,",
		"%\\/%\\/%\\/%\\/%\\/%\\/+,",
		"\\/%\\/%\\/%\\/%\\/%\\/%\\/",
	))
