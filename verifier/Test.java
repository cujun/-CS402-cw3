public class Test{
	public void testMe(int x, int y) {
		int z = x + 3 - 32 * y;
		x = x + 3;
		y = z - x;
		assert(z - y > 0 && x > 0);
	}
}
