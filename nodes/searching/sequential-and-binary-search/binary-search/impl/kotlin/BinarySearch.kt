// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

/** Returns an index i with a[i] == x, or -1 when x is not in a. The list must be sorted. */
fun <T : Comparable<T>> binarySearch(a: List<T>, x: T): Int {
    var lo = 0 // @line L1
    var hi = a.size
    while (lo < hi) { // @line L2
        val mid = lo + (hi - lo) / 2 // @line L3
        val c = a[mid].compareTo(x)
        if (c < 0) { // @line L4
            lo = mid + 1 // @line L5
        } else if (c > 0) { // @line L6
            hi = mid // @line L7
        } else {
            return mid // @line L8
        }
    }
    return -1 // @line L9
}
