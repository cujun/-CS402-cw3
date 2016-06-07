// example for tast 1

public class Test1 {
	public void testMe(int x, int y, int z) {
		int x2 = x * x;
		int y2 = y * y;
		int z2 = z * z;
		assert(x2 + y2 == z2); // assertion is satisfiable, not valid
	}
}