# coding: utf-8

# RECTODO : faire un fichier pytest pour tous ce code.
#  - un test avec les ajouts d'espace, et sur un background de virgules.
#  - un test avec les ajouts d'espace, et sur le background de barres obliques, avec le cropping positionné en semi-random.

import json

from kpjson_to_puzzle import (
	CM_BACKGROUND_WALLS,
	generator_ps_legend_characters, legendify_atoli,
	str_ps_legend, build_ps_level,
)

def test_kpjson_to_puzzle_on_walls():
	"""
	test de génération d'un seul level, sans les ajouts d'espaces, et sur le background de walls.
	"""

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

