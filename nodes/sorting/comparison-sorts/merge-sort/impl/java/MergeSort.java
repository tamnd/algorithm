// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

/** Merge sort. */
public final class MergeSort {
    private MergeSort() {}

    /** Sorts a in place, in non-decreasing order. */
    public static void sort(long[] a) {
        long[] b = new long[(a.length + 1) / 2];
        sort(a, 0, a.length, b);
    }

    private static void sort(long[] a, int lo, int hi, long[] b) {
        if (hi - lo <= 1) return;                 // @line L1
        int mid = lo + (hi - lo) / 2;             // @line L2
        sort(a, lo, mid, b);                      // @line L3
        sort(a, mid, hi, b);                      // @line L4
        merge(a, lo, mid, hi, b);                 // @line L5
    }

    private static void merge(long[] a, int lo, int mid, int hi, long[] b) {
        int m = mid - lo;
        System.arraycopy(a, lo, b, 0, m);         // @line L6
        int i = 0, j = mid, k = lo;               // @line L7
        while (i < m && j < hi) {                 // @line L8
            if (b[i] <= a[j]) {                   // @line L9
                a[k] = b[i++];
            } else {
                a[k] = a[j++];                    // @line L10
            }
            k++;                                  // @line L11
        }
        while (i < m) {                           // @line L12
            a[k++] = b[i++];                      // @line L13
        }
    }
}
