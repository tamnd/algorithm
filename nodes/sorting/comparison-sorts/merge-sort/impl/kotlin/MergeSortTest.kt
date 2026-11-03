// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

import kotlin.random.Random
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class MergeSortTest {
    @Test
    fun example() {
        val a = mutableListOf(38, 27, 43, 3, 9, 82, 10)
        mergeSort(a)
        assertEquals(listOf(3, 9, 10, 27, 38, 43, 82), a)
    }

    @Test
    fun edges() {
        for (a in listOf(listOf(), listOf(1), listOf(2, 1), listOf(1, 1, 1), listOf(3, 2, 1))) {
            val b = a.toMutableList()
            mergeSort(b)
            assertEquals(a.sorted(), b)
        }
    }

    @Test
    fun randomAgainstSorted() {
        val rng = Random(2150)
        repeat(500) {
            val a = MutableList(rng.nextInt(61)) { rng.nextInt(101) - 50 }
            val want = a.sorted()
            mergeSort(a)
            assertEquals(want, a)
        }
    }
}
