// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

/** Sorts a in place, in non-decreasing order. The sort is stable. */
fun <T : Comparable<T>> mergeSort(a: MutableList<T>) {
    sort(a, 0, a.size)
}

private fun <T : Comparable<T>> sort(a: MutableList<T>, lo: Int, hi: Int) {
    if (hi - lo <= 1) return // @line L1
    val mid = lo + (hi - lo) / 2 // @line L2
    sort(a, lo, mid) // @line L3
    sort(a, mid, hi) // @line L4
    merge(a, lo, mid, hi) // @line L5
}

private fun <T : Comparable<T>> merge(a: MutableList<T>, lo: Int, mid: Int, hi: Int) {
    val b = a.subList(lo, mid).toList() // @line L6
    var i = 0 // @line L7
    var j = mid
    var k = lo
    while (i < b.size && j < hi) { // @line L8
        if (b[i] <= a[j]) { // @line L9
            a[k] = b[i++]
        } else {
            a[k] = a[j++] // @line L10
        }
        k++ // @line L11
    }
    while (i < b.size) { // @line L12
        a[k++] = b[i++] // @line L13
    }
}
