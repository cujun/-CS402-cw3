public class Test5{
	public void testMe(int x, int y) {
		y = y + x;
        assert( (2 * y > y || y <= 0) && (x != -x));
	}
}
