// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import java.util.Arrays;
import java.util.Random;
import org.junit.jupiter.api.Test;

class InsertionSortTest {
    @Test
    void example() {
        long[] a = {5, 2, 4, 6, 1, 3};
        InsertionSort.sort(a);
        assertArrayEquals(new long[] {1, 2, 3, 4, 5, 6}, a);
    }

    @Test
    void edges() {
        long[] e = {};
        InsertionSort.sort(e);
        assertArrayEquals(new long[] {}, e);
        String[] w = {"pear", "fig", "apple"};
        InsertionSort.sort(w);
        assertArrayEquals(new String[] {"apple", "fig", "pear"}, w);
    }

    @Test
    void randomAgainstArraysSort() {
        Random rng = new Random(2150);
        for (int t = 0; t < 500; t++) {
            long[] a = new long[rng.nextInt(41)];
            for (int i = 0; i < a.length; i++) a[i] = rng.nextInt(101) - 50;
            long[] want = a.clone();
            Arrays.sort(want);
            InsertionSort.sort(a);
            assertArrayEquals(want, a);
        }
    }
}
