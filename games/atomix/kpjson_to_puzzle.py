# coding: utf-8

"""
Conversion d'un fichier JSON contenant la description de niveaux "kp-atomic" vers un fichier PuzzleSalad/PuzzleScript.
"""

# TODO : faire le code.

import json

FILEPATH_KPATOMIC_JSON = "draknek_levels_json.js"


def read_json_file(filepath_json):
	with open(filepath_json, 'r', encoding='utf-8') as file_json:
		str_json = file_json.read()
	data_json = json.loads(str_json)
	return data_json


def main():
	print("hellow")
	kplevels_json = read_json_file(FILEPATH_KPATOMIC_JSON)
	print(kplevels_json["levels"][1])


if __name__ == '__main__':
	main()

