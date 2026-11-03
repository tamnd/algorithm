// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

/** Insertion sort. */
public final class InsertionSort {
    private InsertionSort() {}

    /** Sorts a in place, in non-decreasing order. */
    public static void sort(long[] a) {
        for (int i = 1; i < a.length; i++) {      // @line L1
            long key = a[i];                      // @line L2
            int j = i - 1;                        // @line L3
            while (j >= 0 && a[j] > key) {        // @line L4
                a[j + 1] = a[j];                  // @line L5
                j--;                              // @line L6
            }
            a[j + 1] = key;                       // @line L7
        }
    }

    /** Sorts a in place by the natural order of its items. The sort is stable. */
    public static <T extends Comparable<? super T>> void sort(T[] a) {
        for (int i = 1; i < a.length; i++) {
            T key = a[i];
            int j = i - 1;
            while (j >= 0 && a[j].compareTo(key) > 0) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
    }
}
