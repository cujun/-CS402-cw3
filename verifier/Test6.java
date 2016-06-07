public class Test6{
	public void testMe(int x, int y) {
		int z = x + 3 - 32 * y;
		x = x + 3;
		y = z - x;
        if (x > 0) {
            z = z + 1;
        }
        if (x -  y > 0) {
            y = y + 1;
        }
        if (z > 0) {
            z = z + 1;
        }
		assert((z - y > 0 && x > 0) || (y + 3 < x || x * y < z || z * z > -1));
	}
}
