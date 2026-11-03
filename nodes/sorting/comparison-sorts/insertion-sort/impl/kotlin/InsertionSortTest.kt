// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

import kotlin.random.Random
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class InsertionSortTest {
    @Test
    fun example() {
        val a = mutableListOf(5, 2, 4, 6, 1, 3)
        insertionSort(a)
        assertEquals(listOf(1, 2, 3, 4, 5, 6), a)
    }

    @Test
    fun edges() {
        val e = mutableListOf<Int>()
        insertionSort(e)
        assertEquals(emptyList<Int>(), e)
        val w = mutableListOf("pear", "fig", "apple")
        insertionSort(w)
        assertEquals(listOf("apple", "fig", "pear"), w)
    }

    @Test
    fun randomAgainstSorted() {
        val rng = Random(2150)
        repeat(500) {
            val a = MutableList(rng.nextInt(41)) { rng.nextInt(101) - 50 }
            val want = a.sorted()
            insertionSort(a)
            assertEquals(want, a)
        }
    }
}
