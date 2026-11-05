---
tag: AQF46A
kind: problem
slug: sorting-by-adjacent-swaps
name: Sorting by adjacent swaps
aliases:
- minimum adjacent swaps to sort
area: sequences/inversions-and-permutations
level: intro
summary: The minimum number of adjacent transpositions needed to sort a permutation equals its number of inversions.
prereqs: [inversion, counting-inversions]
see_also: [bubble-sort, insertion-sort, kendall-tau-distance, cayley-distance, expected-number-of-inversions, odd-even-transposition-sort, mahonian-numbers, sorting-by-reversals]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.1 (inversions) and Section 5.2.2 (sorting by exchanging, bubble sort and the number of exchanges)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2, Problem 2-2 (correctness of bubble sort) and Problem 2-4 (inversions)
  - paper: "Richard P. Stanley, On the number of reduced decompositions of elements of Coxeter groups, European Journal of Combinatorics 5(4) (1984)"
    locator: the count of the shortest products of adjacent transpositions for the reversal permutation
---

Sorting by adjacent swaps asks for the fewest exchanges of two neighboring items that sort a sequence. The answer is exactly its number of [inversions](/inversion/): each adjacent swap changes the number of inversions by at most one, and swapping any neighboring pair that is out of order lowers it by exactly one. So the minimum is found by [counting inversions](/counting-inversions/) in $O(n \log n)$ time, and an optimal sequence of swaps is the one that [bubble sort](/bubble-sort/) or [insertion sort](/insertion-sort/) makes. The same number is the [Kendall tau distance](/kendall-tau-distance/) between two orders, and its average over random inputs, $n(n-1)/4$, is the reason why sorts that only move items by one place are quadratic.

## In plain words

People stand in a line, and you want them in order of height. The only move allowed is to let two neighbors trade places. How many moves do you need?

Count the pairs of people who are in the wrong order, a taller one before a shorter one, wherever they stand. A trade between neighbors fixes or breaks only the pair of those two people. Every other pair keeps its order. So each move fixes at most one wrong pair, and you need at least as many moves as there are wrong pairs. You never need more: as long as the line is not sorted, some two neighbors are in the wrong order, and trading them fixes exactly one wrong pair.

## Definition

**Input.** A sequence $a = (a_1, \ldots, a_n)$ of items from a [total order](/total-order/).

**Move.** An *adjacent swap* $s_k$, for $1 \le k < n$, exchanges the items in positions $k$ and $k + 1$. As a [permutation](/permutation/) of positions, $s_k$ is the transposition $(k\ \ k+1)$.

**Output.** The least $d$ such that some sequence of $d$ adjacent swaps turns $a$ into a non-decreasing sequence. In the search version, also output such a sequence of swaps.

**Theorem.** $d = \operatorname{inv}(a)$, the number of pairs $i < j$ with $a_i > a_j$. This holds with repeated items too.

*Proof.* *Lower bound.* A swap $s_k$ changes only the relative order of the two items in positions $k$ and $k + 1$. Every other pair of items keeps its two items in the same order, though one of them may move by one place. So the number of inversions changes by $+1$, $-1$ or $0$, the last when the two items are equal. A non-decreasing sequence has no inversions. So at least $\operatorname{inv}(a)$ swaps are needed.

*Upper bound.* If $a$ is not non-decreasing, there is a $k$ with $a_k > a_{k+1}$, because a sequence in which each item is at most the next one is non-decreasing. The swap $s_k$ removes the inversion of these two items and creates none, so it lowers the count by exactly 1. Repeat until the count is 0. This takes exactly $\operatorname{inv}(a)$ swaps. $\square$

## Variants

- **Transform $a$ into $b$.** Given two arrangements of the same distinct items, the fewest adjacent swaps that turn $a$ into $b$ is $\operatorname{inv}$ of $a$ relabeled by the positions in $b$. This is the [Kendall tau distance](/kendall-tau-distance/). With repeated items, match the $t$-th copy of each value in $a$ to the $t$-th copy in $b$; this matching keeps equal items in order and is optimal.
- **Any swaps.** If any two items may be exchanged, the minimum for a permutation is $n$ minus its number of [cycles](/permutation-cycles/), the [Cayley distance](/cayley-distance/). It is never more than the adjacent-swap minimum.
- **Reversals and prefix reversals.** Allowing a whole segment to be reversed in one move gives [sorting by reversals](/sorting-by-reversals/), and allowing only prefixes gives [pancake sorting](/pancake-sorting/). Block moves give [sorting by transpositions](/sorting-by-transpositions/).
- **Parallel swaps.** In one round, any set of disjoint adjacent pairs may be swapped. [Odd-even transposition sort](/odd-even-transposition-sort/) sorts every input in $n$ rounds, and the reversed input needs $n$ rounds for $n \ge 3$.
- **Circular arrangement.** If position $n$ is also adjacent to position 1, and every rotation of the sorted order is accepted, the answer is no longer a plain inversion count, and the minimum must be taken over the target rotations.
- **Counting the optimal sequences.** The shortest swap sequences of a permutation are its *reduced words*. For the reversal $n\,(n-1) \cdots 1$, Stanley proved that their number is $\binom n2! \,/\, \big(1^{n-1} 3^{n-2} 5^{n-3} \cdots (2n-3)^1\big)$.

## Examples

**A permutation.** $a = 3\,1\,4\,5\,2$ has the 4 inversions $(3, 1)$, $(3, 2)$, $(4, 2)$ and $(5, 2)$, so 4 swaps are needed and enough. One optimal sequence moves the 2 to the left and then fixes the front:

| swap | result | inversions left |
| --- | --- | --- |
| start | 3 1 4 5 2 | 4 |
| $s_4$ | 3 1 4 2 5 | 3 |
| $s_3$ | 3 1 2 4 5 | 2 |
| $s_1$ | 1 3 2 4 5 | 1 |
| $s_2$ | 1 2 3 4 5 | 0 |

A wrong move costs two swaps. From $3\,1\,2\,4\,5$, the swap $s_2$ exchanges $1$ and $2$, which are in order, and gives $3\,2\,1\,4\,5$ with 3 inversions, one more than before.

**Repeated items.** $(2, 1, 3, 1, 2)$ has 4 inversions: the first 2 with both 1s, and the 3 with the second 1 and the last 2. So 4 adjacent swaps are the minimum to reach $(1, 1, 2, 2, 3)$. Swapping two equal neighbors does not change the count and is never useful.

**The worst case.** The reversal $n\,(n-1) \cdots 1$ needs $\binom n2$ swaps, the most for any input. For $n = 5$ that is 10, the largest distance among all 120 permutations. The number of optimal swap sequences for the reversal is $1, 1, 2, 16, 768, 292864$ for $n = 1, \ldots, 6$.

## Known algorithms

- **The number only.** Count inversions with the [merge sort method](/inversion-count-by-merge-sort/) or the [Fenwick tree method](/inversion-count-with-fenwick-tree/), in $O(n \log n)$ time.
- **An optimal swap sequence.** [Bubble sort](/bubble-sort/) swaps only neighbors that are out of order, and so makes exactly $\operatorname{inv}(a)$ swaps. [Insertion sort](/insertion-sort/) moves each item left past the larger items before it, one place at a time, which is also a sequence of $\operatorname{inv}(a)$ adjacent swaps. Insertion sort lists them in $\Theta(n + \operatorname{inv}(a))$ time, which is optimal because the output has $\operatorname{inv}(a)$ swaps.

## Bounds

- **Exact value.** $d = \operatorname{inv}(a)$, between $0$ and $\binom n2$.
- **Average.** For a uniform random permutation, $\mathbb{E}[d] = n(n-1)/4$ with variance $n(n-1)(2n+5)/72$; see [expected number of inversions](/expected-number-of-inversions/). The number of permutations with $d = k$ is the [Mahonian number](/mahonian-numbers/) $M(n, k)$.
- **Cost of computing $d$.** $\Theta(n \log n)$ comparisons in the [comparison model](/comparison-model/), as shown on the [counting inversions](/counting-inversions/) page.
- **Cost of a sort that uses only adjacent swaps.** At least $\operatorname{inv}(a)$ swaps on each input, so $\Omega(n^2)$ in the worst case and on average. This lower bound covers bubble sort, insertion sort, [gnome sort](/gnome-sort/), [cocktail shaker sort](/cocktail-shaker-sort/) and odd-even transposition sort.

## Reductions

- **To counting inversions.** The minimum equals the inversion count, so the problem and [counting inversions](/counting-inversions/) are the same problem.
- **From Kendall tau distance.** Two rankings of the same $n$ items are at Kendall tau distance $k$ exactly when $k$ adjacent swaps turn one into the other, with $O(n)$ extra work to relabel.
- **The Cayley graph view.** The permutations of $[n]$, with an edge between two permutations that differ by one adjacent swap, form a graph of diameter $\binom n2$. The shortest path length from $\pi$ to the identity is $\operatorname{inv}(\pi)$.

## Applications

- **Analysis of simple sorts.** The theorem gives the exact number of exchanges of bubble sort and of shifts of insertion sort, and the lower bound for every sort that only swaps neighbors.
- **Puzzles and exercises.** "Minimum adjacent swaps to sort an array" and "to turn one string into another" are standard interview and contest problems, solved by counting inversions after a relabeling.
- **Comparing rankings.** The Kendall tau distance is the adjacent-swap distance between two rankings, used in statistics and in the evaluation of search results.
- **Wiring diagrams.** A shortest swap sequence for the reversal is a way to draw $n$ wires so that each pair crosses exactly once, which is the setting of Stanley's count of reduced words.

## References
