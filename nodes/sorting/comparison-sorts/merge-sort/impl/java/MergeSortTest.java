// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import java.util.Arrays;
import java.util.Random;
import org.junit.jupiter.api.Test;

class MergeSortTest {
    @Test
    void example() {
        long[] a = {38, 27, 43, 3, 9, 82, 10};
        MergeSort.sort(a);
        assertArrayEquals(new long[] {3, 9, 10, 27, 38, 43, 82}, a);
    }

    @Test
    void edges() {
        for (long[] a : new long[][] {{}, {1}, {2, 1}, {1, 1, 1}, {3, 2, 1}}) {
            long[] want = a.clone();
            Arrays.sort(want);
            MergeSort.sort(a);
            assertArrayEquals(want, a);
        }
    }

    @Test
    void randomAgainstArraysSort() {
        Random rng = new Random(2150);
        for (int t = 0; t < 500; t++) {
            long[] a = new long[rng.nextInt(61)];
            for (int i = 0; i < a.length; i++) a[i] = rng.nextInt(101) - 50;
            long[] want = a.clone();
            Arrays.sort(want);
            MergeSort.sort(a);
            assertArrayEquals(want, a);
        }
    }

    @Test
    void words() {
        String[] w = {"pear", "fig", "apple", "fig"};
        MergeSort.sort(w);
        assertArrayEquals(new String[] {"apple", "fig", "fig", "pear"}, w);
    }
}
