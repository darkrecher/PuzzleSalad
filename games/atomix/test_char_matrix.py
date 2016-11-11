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

def test_replace():
	cm = CharMatrix( ["001", "210"])
	cm.replace('1', 'z')
	str_cm_final = '\n'.join((
		"00z",
		"2z0",
	))
	assert str(cm) == str_cm_final


