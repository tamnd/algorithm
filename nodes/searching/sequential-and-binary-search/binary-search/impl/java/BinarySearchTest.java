// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Arrays;
import java.util.Random;
import org.junit.jupiter.api.Test;

class BinarySearchTest {
    @Test
    void examples() {
        long[] a = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
        assertEquals(5, BinarySearch.search(a, 23));
        assertEquals(0, BinarySearch.search(a, 2));
        assertEquals(9, BinarySearch.search(a, 91));
        assertEquals(-1, BinarySearch.search(a, 30));
        assertEquals(-1, BinarySearch.search(a, 1));
        assertEquals(-1, BinarySearch.search(a, 100));
    }

    @Test
    void edges() {
        assertEquals(-1, BinarySearch.search(new long[0], 1));
        assertEquals(0, BinarySearch.search(new long[] {7}, 7));
        assertEquals(1, BinarySearch.search(new String[] {"ant", "bee", "cat"}, "bee"));
    }

    @Test
    void randomAgainstLinearScan() {
        Random rng = new Random(2150);
        for (int t = 0; t < 2000; t++) {
            long[] a = new long[rng.nextInt(31)];
            for (int i = 0; i < a.length; i++) a[i] = rng.nextInt(41) - 20;
            Arrays.sort(a);
            long x = rng.nextInt(51) - 25;
            int got = BinarySearch.search(a, x);
            boolean found = Arrays.stream(a).anyMatch(v -> v == x);
            if (found) assertEquals(x, a[got]);
            else assertEquals(-1, got);
        }
    }
}
