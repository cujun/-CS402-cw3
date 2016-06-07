// example for tast 1

public class Test2 {
	public void testMe(int x, int y) {
		int t1 = x + y;
		int tmp = x;
		x = y;
		y = tmp;
		int t2 = x + y;
		assert(t1 > t2); // assertion is not valid
	}
}