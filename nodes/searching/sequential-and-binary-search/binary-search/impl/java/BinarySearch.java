// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

/** Binary search in a sorted array. */
public final class BinarySearch {
    private BinarySearch() {}

    /** Returns an index i with a[i] == x, or -1 when x is not in a. The array must be sorted. */
    public static int search(long[] a, long x) {
        int lo = 0, hi = a.length;                // @line L1
        while (lo < hi) {                         // @line L2
            int mid = lo + (hi - lo) / 2;         // @line L3
            if (a[mid] < x) {                     // @line L4
                lo = mid + 1;                     // @line L5
            } else if (a[mid] > x) {              // @line L6
                hi = mid;                         // @line L7
            } else {
                return mid;                       // @line L8
            }
        }
        return -1;                                // @line L9
    }

    /** The same search for any type with a natural order. */
    public static <T extends Comparable<? super T>> int search(T[] a, T x) {
        int lo = 0, hi = a.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int c = a[mid].compareTo(x);
            if (c < 0) {
                lo = mid + 1;
            } else if (c > 0) {
                hi = mid;
            } else {
                return mid;
            }
        }
        return -1;
    }
}
