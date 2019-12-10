inventory={
	"toto":[16,22],
	"kinou":[12,18],
}

def test(inCle,inValue):
	global inventory
	inventory[inCle][1]=inValue
	
def test2(un,deux):
	print(un,deux)
		
		
test("toto", 18)

	



