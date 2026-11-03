// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

import kotlin.random.Random
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test

class BinarySearchTest {
    @Test
    fun examples() {
        val a = listOf(2, 5, 8, 12, 16, 23, 38, 56, 72, 91)
        assertEquals(5, binarySearch(a, 23))
        assertEquals(0, binarySearch(a, 2))
        assertEquals(9, binarySearch(a, 91))
        assertEquals(-1, binarySearch(a, 30))
        assertEquals(-1, binarySearch(a, 1))
        assertEquals(-1, binarySearch(a, 100))
    }

    @Test
    fun edges() {
        assertEquals(-1, binarySearch(emptyList<Int>(), 1))
        assertEquals(0, binarySearch(listOf(7), 7))
        assertEquals(1, binarySearch(listOf("ant", "bee", "cat"), "bee"))
    }

    @Test
    fun randomAgainstLinearScan() {
        val rng = Random(2150)
        repeat(2000) {
            val a = List(rng.nextInt(31)) { rng.nextInt(41) - 20 }.sorted()
            val x = rng.nextInt(51) - 25
            val got = binarySearch(a, x)
            if (x in a) assertEquals(x, a[got]) else assertEquals(-1, got)
        }
    }
}
