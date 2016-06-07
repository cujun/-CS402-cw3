// example for tast 2

public class Test3 {
	public void testMe(int x, int y, int z) {
		int t = 0;
		if(x + y <= z || y + z <= x || z + x <= y)
			t = -1;
		else if(x == y && y == z)
			t = 1;
		assert(t == -1 || t == 0 || t == 1); // assertion is valid
	}
}