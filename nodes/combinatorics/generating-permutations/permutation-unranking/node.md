---
tag: 8H1DTS
kind: problem
slug: permutation-unranking
name: Unranking of a permutation
aliases:
- permutation from index
- k-th permutation
area: combinatorics/generating-permutations
level: core
summary: Given an index in 0 to n!-1, construct the permutation at that lexicographic position.
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: O(n log n)}
prereqs: [permutation, lexicographic-order, factorial-number-system, permutation-ranking]
see_also: [permutation-ranking, permutation-rank-unrank, lehmer-code, factorial-number-system, fenwick-tree, random-permutation, combinatorial-ranking-and-unranking, big-integer]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (unranking of permutations in lexicographic order and in Trotter-Johnson order)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (the correspondence between permutations and mixed-radix numbers)
  - paper: doi:10.1016/S0020-0190(01)00141-7
    title: Wendy Myrvold and Frank Ruskey, Ranking and unranking permutations in linear time, Information Processing Letters 79(6) (2001) 281-284
    locator: the whole paper (the O(n) unrank function, which makes n exchanges)
  - paper: doi:10.1007/978-3-540-75520-3_18
    title: Martin Mareš and Milan Straka, Linear-time ranking of permutations, Algorithms, ESA 2007, LNCS 4698, 187-193
    locator: the whole paper (lexicographic ranking and unranking with O(n) arithmetic operations)
---

Permutation unranking asks for the [permutation](/permutation/) of $[n] = \{1, \ldots, n\}$ at a given position $r$ in [lexicographic order](/lexicographic-order/), with $0 \le r < n!$. It is the inverse of [permutation ranking](/permutation-ranking/). Write $r$ in the [factorial number system](/factorial-number-system/); each digit then says which of the values not yet used goes into the next position. With a list of unused values this takes $O(n^2)$ time, with a [Fenwick tree](/fenwick-tree/) $O(n \log n)$, and in a suitable non-lexicographic order $O(n)$.

## In plain words

Imagine all orders of the numbers 1 to the number of items in a dictionary list, numbered from 0. You get a number and want the order at that place, without writing the list.

The orders that start with 1 fill the first block of the list, the orders that start with 2 fill the next block, and so on, and all blocks have the same size. Divide the number by the block size: the result tells you the first entry, and the remainder tells you the place inside that block. Do the same with the numbers that are left, with smaller and smaller blocks, until all places are filled.

## Definition

**Input.** An integer $n \ge 0$ and an integer $r$ with $0 \le r < n!$.

**Output.** The permutation $\pi$ of $[n]$ such that exactly $r$ permutations of $[n]$ are lexicographically smaller than $\pi$.

**Method.** Write $r$ in the mixed radix $(n, n-1, \ldots, 1)$:

$$r = \sum_{i=1}^{n} c_i\,(n - i)!, \qquad 0 \le c_i \le n - i.$$

The digits are unique, and $c_i = \lfloor r / (n-i)! \rfloor \bmod (n - i + 1)$. Then $\pi_i$ is the value of order $c_i$, counted from 0, among the values not in $\{\pi_1, \ldots, \pi_{i-1}\}$. The vector $(c_1, \ldots, c_n)$ is the [Lehmer code](/lehmer-code/) of $\pi$, so the rank formula of [permutation ranking](/permutation-ranking/) gives back $r$, and $\pi$ is correct.

In practice the digits come from the right by repeated division: for $j = 1, 2, \ldots, n$, set $c_{n-j+1} \leftarrow r \bmod j$ and $r \leftarrow \lfloor r / j \rfloor$. Then the values are chosen from the left.

## Variants

- **Ranking.** The inverse map. See [permutation ranking](/permutation-ranking/).
- **Other orders.** Unrank in the [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order or in colexicographic order. Kreher and Stinson give unranking for the Trotter-Johnson order.
- **A free order.** Myrvold and Ruskey unrank in their own order with $n$ exchanges: start from the identity in positions $0, \ldots, n-1$; for $m = n, n - 1, \ldots, 1$, exchange the entries at positions $m - 1$ and $r \bmod m$, then set $r \leftarrow \lfloor r / m \rfloor$.
- **Multisets.** Find the arrangement of a multiset at a given rank. See [multiset permutations](/multiset-permutations/).
- **Partial permutations.** Find the $r$-th sequence of $k$ distinct values from $[n]$, with digits in the radix $(n, n-1, \ldots, n-k+1)$.

## Examples

**Unrank 1000 for $n = 7$.** The digits in the radix $(7, 6, 5, 4, 3, 2, 1)$ are $1, 2, 1, 2, 2, 0, 0$, because $1 \cdot 720 + 2 \cdot 120 + 1 \cdot 24 + 2 \cdot 6 + 2 \cdot 2 = 1000$.

| $i$ | $c_i$ | unused values | $\pi_i$ |
|---|---|---|---|
| 1 | 1 | 1 2 3 4 5 6 7 | 2 |
| 2 | 2 | 1 3 4 5 6 7 | 4 |
| 3 | 1 | 1 3 5 6 7 | 3 |
| 4 | 2 | 1 5 6 7 | 6 |
| 5 | 2 | 1 5 7 | 7 |
| 6 | 0 | 1 5 | 1 |
| 7 | 0 | 5 | 5 |

So the permutation of rank 1000 is $2\,4\,3\,6\,7\,1\,5$.

**More values.** For $n = 7$, rank 2020 gives $3\,6\,7\,1\,5\,2\,4$. For $n = 10$, rank 999999 gives $3\,8\,9\,4\,10\,2\,6\,5\,7\,1$, the millionth permutation counted from 1.

**Myrvold and Ruskey order.** For $n = 3$ with values $0, 1, 2$, the ranks $0, \ldots, 5$ give $120$, $201$, $102$, $210$, $021$, $012$. This is not lexicographic, but it is a bijection, and each permutation takes 3 exchanges to build.

## Known algorithms

- **Direct.** Keep the unused values in a sorted list, and remove the value of order $c_i$ at step $i$. This takes $\Theta(n^2)$ time in the worst case, from the removals.
- **[Permutation rank and unrank algorithm](/permutation-rank-unrank/).** Keep a [Fenwick tree](/fenwick-tree/) over the values with a 1 for each unused value. A descent in the tree finds the value of order $c_i$ in $O(\log n)$ time. The total is $O(n \log n)$. An [order-statistic tree](/order-statistic-tree/) gives the same bound.
- **Linear time, lexicographic.** Mareš and Straka (2007) unrank in lexicographic order with $O(n)$ arithmetic operations on a RAM.
- **Linear time, another order.** The Myrvold and Ruskey method above makes $n$ exchanges and $n$ divisions.

## Bounds

- **Lower bound.** $\Omega(n)$ time, to write the output.
- **Upper bounds.** $O(n \log n)$ word operations by a Fenwick tree when $r$ fits in $O(1)$ words, and $O(n)$ arithmetic operations by the linear methods.
- **Big ranks.** $r$ has up to $\lceil \lg n! \rceil = n \lg n - \Theta(n)$ bits, so it needs a [big integer](/big-integer/) for $n > 20$. The digit extraction divides a number of $O(n \log n)$ bits by a small number $n$ times, which is $O(n^2 \log n / w)$ word operations with $w$-bit words.

## Reductions

- **Inverse of ranking.** unrank(rank$(\pi)) = \pi$ and rank(unrank$(r)) = r$.
- **Listing.** Unranking each of $0, \ldots, n! - 1$ solves [generating all permutations](/generating-all-permutations/), at a cost of $O(n \log n)$ per permutation instead of $O(1)$ amortized.
- **Random permutations.** If $r$ is uniform on $\{0, \ldots, n! - 1\}$, then unrank$(r)$ is a uniform [random permutation](/random-permutation/). The Myrvold and Ruskey unrank with digits chosen one at a time is the [Fisher-Yates shuffle](/fisher-yates-shuffle/).

## Applications

- **Jump to a position.** Start a listing at rank $r$, for example to split the work of a search over $n!$ orders among many processors.
- **Decode a stored permutation.** A permutation stored as its rank in $\lceil \lg n! \rceil$ bits is decoded by unranking.
- **State tables.** A table indexed by rank can be scanned in order, and each index turned back into the state it stands for.

## References
