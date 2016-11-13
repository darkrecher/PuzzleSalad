# python -m py.test
# (y compris dans la console de mingw64)

from char_matrix import CharMatrix


def test_init():
	cm = CharMatrix( ["ab", "cd"])
	cm.verify_matrix()
	assert str(cm) == "ab\ncd"

# RECTODO : tester le verify_matrix qui raise une Exception

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

def test_replace():
	cm = CharMatrix( ["001", "210"])
	cm.replace('1', 'z')
	str_cm_final = '\n'.join((
		"00z",
		"2z0",
	))
	assert str(cm) == str_cm_final

def test_cropped():
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"])
	cm_cropped = cm.cropped((1, 2), (4, 2))
	str_cm_cropped_final = '\n'.join((
		"uvwx",
		"*-+,",
	))
	assert str(cm_cropped) == str_cm_cropped_final
	cm_cropped_all = cm.cropped((0, 0), cm.dimensions())
	assert str(cm_cropped_all) == str(cm)

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
	cm = CharMatrix( ["0123456", "abcdefg", "tuvwxyz", "/*-+,.!"])
	cm_to_blit = CharMatrix( ["ij", " l", "m "], ' ')
	cm.blit(cm_to_blit, (4, 1))
	str_cm_blitted_final = '\n'.join((
		"0123456",
		"abcdijg",
		"tuvwxlz",
		"/*-+m.!",
	))

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
