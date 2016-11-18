# python -m py.test
# (y compris dans la console de mingw64)

from char_matrix import CharMatrix

# FUTURE : simple quotes là où il le faudrait.

def test_init():
	cm = CharMatrix( ["ab", "cd"])
	cm.verify_matrix()
	assert str(cm) == "ab\ncd"

# FUTURE : tester le verify_matrix qui raise une Exception

def test_dimensions():
	cm = CharMatrix( ["0123456", "abcdefg", "-------"])
	cm.verify_matrix()
	assert cm.dimensions() == (7, 3)

def test_in_dimensions():
	cm = CharMatrix( ["0123456", "abcdefg", "-------"])
	assert cm.in_dimensions((0, 0))
	assert cm.in_dimensions((2, 1))
	assert cm.in_dimensions((6, 0))
	assert cm.in_dimensions((0, 2))
	assert not(cm.in_dimensions((-1, 0)))
	assert not(cm.in_dimensions((0, -1)))
	assert not(cm.in_dimensions((7, 0)))
	assert not(cm.in_dimensions((0, 3)))

def test_get_char():
	cm = CharMatrix( ["0123456", "abcdefg", "-------"])
	assert cm.get_char((0, 0)) == "0"
	assert cm.get_char((2, 1)) == "c"
	assert cm.get_char((6, 0)) == "6"
	assert cm.get_char((0, 2)) == "-"
	assert cm.get_char((-1, 0)) is None
	assert cm.get_char((0, -1)) is None
	assert cm.get_char((7, 0)) is None
	assert cm.get_char((0, 3)) is None

def test_set_char():
	cm = CharMatrix( ["0123456", "abcdefg"])
	cm.set_char((0, 0), '@')
	str_cm_set = '\n'.join((
		"@123456",
		"abcdefg",
	))
	assert str(cm) == str_cm_set
	pos_down_right = cm.dimensions()
	pos_down_right = (pos_down_right[0]-1, pos_down_right[1]-1)
	cm.set_char(pos_down_right, '+')
	str_cm_set = '\n'.join((
		"@123456",
		"abcdef+",
	))
	assert str(cm) == str_cm_set

def test_get_unique_chars():
	cm = CharMatrix( ["-------", "0122456", "abcdaag", "*******"])
	unique_chars = cm.get_unique_chars()
	assert sorted(unique_chars) == sorted(list('-012456abcdg*'))

def test_get_coords_around():
	cm = CharMatrix( ["0123456", "abcdefg", "-------", "*******"])
	assert tuple(cm.get_coords_around((2, 2))) == (
		(1, 1), (2, 1), (3, 1),
		(1, 2), (3, 2),
		(1, 3), (2, 3), (3, 3),
	)
	assert tuple(cm.get_coords_around((0, 0))) == (
		(1, 0),
		(0, 1), (1, 1),
	)
	assert tuple(cm.get_coords_around((6, 3))) == (
		(5, 2), (6, 2),
		(5, 3),
	)
	assert tuple(cm.get_coords_around((10, 10))) == ()

def test_get_chars_around():
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"])
	assert "".join(cm.get_chars_around((2, 2))) == "bcduw*-+"
	assert "".join(cm.get_chars_around((0, 0))) == "1ab"
	assert "".join(cm.get_chars_around((6, 3))) == "yz."
	assert "".join(cm.get_chars_around((10, 10))) == ""

def test_translate():
	cm = CharMatrix( ["001", "210"])
	cm.translate('1', 'z')
	str_cm_final = '\n'.join((
		"00z",
		"2z0",
	))
	assert str(cm) == str_cm_final
	cm = CharMatrix( ["001", "210"])
	cm.translate('01234', 'abcde')
	str_cm_final = '\n'.join((
		"aab",
		"cba",
	))
	assert str(cm) == str_cm_final

def test_cropped():
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"], '%')
	cm_cropped = cm.cropped((1, 2), (4, 2))
	str_cm_cropped_final = '\n'.join((
		"uvwx",
		"*-+,",
	))
	assert str(cm_cropped) == str_cm_cropped_final
	assert cm_cropped.transparent_char == '%'
	cm_cropped_all = cm.cropped((0, 0), cm.dimensions())
	assert str(cm_cropped_all) == str(cm)
	assert cm_cropped_all.transparent_char == '%'

def test_blit():
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"])
	cm_to_blit = CharMatrix( ["ij", "kl", "m "])
	cm.blit(cm_to_blit, (4, 1))
	str_cm_blitted_final = '\n'.join((
		"0123456",
		"abcdijg",
		"tuvwklz",
		"/*-+m !",
	))
	assert str(cm) == str_cm_blitted_final
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"])
	cm_to_blit = CharMatrix( ["ij", " l", "m "], ' ')
	cm.blit(cm_to_blit, (4, 1))
	str_cm_blitted_final = '\n'.join((
		"0123456",
		"abcdijg",
		"tuvwxlz",
		"/*-+m.!",
	))
	assert str(cm) == str_cm_blitted_final

def test_get_char_positions():
	cm = CharMatrix( ["@12345@", "ab@@@fg", "tuvwxyz", "/@-+,.@"])
	char_positions = cm.get_char_positions('@')
	assert tuple(char_positions) == (
		(0, 0), (6, 0),
		(2, 1), (3, 1), (4, 1),
		(1, 3), (6, 3),
	)
	char_positions = cm.get_char_positions('!')
	assert tuple(char_positions) == ()
	char_positions = cm.get_char_positions('.')
	assert tuple(char_positions) == ((5, 3), )
