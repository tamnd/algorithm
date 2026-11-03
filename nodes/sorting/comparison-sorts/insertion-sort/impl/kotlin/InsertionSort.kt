// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

/** Sorts a in place, in non-decreasing order. The sort is stable. */
fun <T : Comparable<T>> insertionSort(a: MutableList<T>) {
    for (i in 1 until a.size) { // @line L1
        val key = a[i] // @line L2
        var j = i - 1 // @line L3
        while (j >= 0 && a[j] > key) { // @line L4
            a[j + 1] = a[j] // @line L5
            j-- // @line L6
        }
        a[j + 1] = key // @line L7
    }
}
