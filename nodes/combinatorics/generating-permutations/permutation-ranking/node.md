---
tag: 043TAT
kind: problem
slug: permutation-ranking
name: Permutation ranking and unranking
aliases:
- Ranking of a permutation
- lexicographic rank of a permutation
- permutation index
area: combinatorics/generating-permutations
level: core
summary: Map a permutation to its index in lexicographic order and back.
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: O(n log n)}
prereqs: [permutation, lexicographic-order, lehmer-code, factorial-number-system]
see_also: [permutation-unranking, permutation-rank-unrank, lexicographic-permutation-successor, inversion-table, fenwick-tree, combinatorial-ranking-and-unranking, multiset-permutations, big-integer]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (ranking and unranking of permutations in lexicographic order and in Trotter-Johnson order)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (the correspondence between permutations and mixed-radix numbers)
  - paper: doi:10.1016/S0020-0190(01)00141-7
    title: Wendy Myrvold and Frank Ruskey, Ranking and unranking permutations in linear time, Information Processing Letters 79(6) (2001) 281-284
    locator: the whole paper (the O(n) rank and unrank functions for a non-lexicographic order)
  - paper: doi:10.1007/978-3-540-75520-3_18
    title: Martin Mareš and Milan Straka, Linear-time ranking of permutations, Algorithms, ESA 2007, LNCS 4698, 187-193
    locator: the whole paper (lexicographic ranking and unranking with O(n) arithmetic operations)
---

Permutation ranking asks for the position of a [permutation](/permutation/) of $[n] = \{1, \ldots, n\}$ in the [lexicographic order](/lexicographic-order/) of all $n!$ permutations, counted from 0. The rank is the [Lehmer code](/lehmer-code/) of the permutation read as a number in the [factorial number system](/factorial-number-system/). The inverse problem is [unranking](/permutation-unranking/). A direct method takes $O(n^2)$ time, a [Fenwick tree](/fenwick-tree/) gives $O(n \log n)$, and $O(n)$ is possible with more advanced methods or with a non-lexicographic order.

## In plain words

Write down all orders of the numbers 1 to the number of items, sorted as in a dictionary, and number them 0, 1, 2 and so on. The rank of an order is its number in this list. You want to find it without writing the list.

Look at the first entry. Every order that starts with a smaller number comes earlier, and there are many such orders for each smaller number. Count them. Then fix the first entry and do the same for the second entry among the numbers that are left, and so on. The total count is the rank. Unranking is the same work in reverse: from the number, find the order.

## Definition

**Input.** A permutation $\pi = \pi_1 \pi_2 \cdots \pi_n$ of $[n]$.

**Output.** The rank $r(\pi) \in \{0, 1, \ldots, n! - 1\}$, the number of permutations of $[n]$ that are lexicographically smaller than $\pi$.

**Formula.** Let $c_i$ be the number of indices $j > i$ with $\pi_j < \pi_i$. The vector $(c_1, \ldots, c_n)$ is the Lehmer code, with $0 \le c_i \le n - i$. Then

$$r(\pi) = \sum_{i=1}^{n} c_i\, (n - i)!.$$

*Proof.* A permutation $\sigma < \pi$ first differs from $\pi$ at some position $i$, with $\sigma_i < \pi_i$. At position $i$, the values not used by $\pi_1, \ldots, \pi_{i-1}$ are the values $\pi_i, \ldots, \pi_n$, and $c_i$ of them are smaller than $\pi_i$. For each such value at position $i$, the last $n - i$ positions can hold the other values in any of $(n - i)!$ orders. So $c_i (n - i)!$ permutations first differ from $\pi$ at position $i$, and the sum over $i$ counts each $\sigma < \pi$ once. $\blacksquare$

The map from codes to ranks is a bijection from the vectors with $0 \le c_i \le n - i$ onto $\{0, \ldots, n! - 1\}$, because it writes the rank in the mixed radix $(n, n-1, \ldots, 1)$. Unranking inverts it.

The rank has $\lceil \lg n! \rceil = n \lg n - \Theta(n)$ bits. It fits in a 64-bit word for $n \le 20$, since $20! < 2^{63} < 21!$, and needs a [big integer](/big-integer/) for larger $n$.

## Variants

- **Unranking.** Given $n$ and $r$, find the permutation of rank $r$. See [permutation unranking](/permutation-unranking/).
- **Other orders.** Rank in the [Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/) order, in colexicographic order, or in any order with a recursive structure. Kreher and Stinson give rank and unrank for the Trotter-Johnson order in $O(n^2)$ time.
- **Any order with fast ranking.** If the order is free, Myrvold and Ruskey give an order in which both rank and unrank take $O(n)$ arithmetic operations.
- **Multisets.** Rank an arrangement among the distinct arrangements of a multiset. See [multiset permutations](/multiset-permutations/).
- **Partial permutations.** Rank a sequence of $k$ distinct values from $[n]$ among the $n!/(n-k)!$ such sequences. Position $i$ then has weight $(n - i)!/(n - k)!$.
- **Other objects.** Ranking of combinations uses the [combinatorial number system](/combinatorial-number-system/). The general method is [combinatorial ranking and unranking](/combinatorial-ranking-and-unranking/).

## Examples

| $\pi$ | Lehmer code | rank |
|---|---|---|
| 1 2 3 4 5 | 0 0 0 0 0 | 0 |
| 3 1 4 5 2 | 2 0 1 1 0 | $2 \cdot 24 + 1 \cdot 2 + 1 \cdot 1 = 51$ |
| 5 4 3 2 1 | 4 3 2 1 0 | $96 + 18 + 4 + 1 = 119$ |
| 4 1 3 6 2 5 | 3 0 1 2 0 0 | $3 \cdot 120 + 1 \cdot 6 + 2 \cdot 2 = 370$ |
| 2 4 1 3 6 5 | 1 2 0 0 1 0 | $120 + 2 \cdot 24 + 1 = 169$ |

For 3 1 4 5 2: the value 3 has 1 and 2 after it, so $c_1 = 2$. There are $2 \cdot 4! = 48$ permutations that start with 1 or 2. Then 1 has no smaller value after it. Then 4 has 2 after it, which gives 2 more. Then 5 has 2 after it, which gives 1 more. The last permutation $5\,4\,3\,2\,1$ has rank $5! - 1 = 119$, as it must.

## Known algorithms

- **Direct.** Compute each $c_i$ by a scan of the positions after $i$, or by a count of the unused smaller values. This takes $\Theta(n^2)$ time and $O(1)$ extra words.
- **[Permutation rank and unrank algorithm](/permutation-rank-unrank/).** Keep a [Fenwick tree](/fenwick-tree/) or an [order-statistic tree](/order-statistic-tree/) over the unused values. Then $c_i$ is the number of unused values below $\pi_i$, a prefix sum, in $O(\log n)$ time. The total is $O(n \log n)$.
- **Divide and conquer.** The Lehmer code is a count of [inversions](/inversion/) for each position, and the merge step of [merge sort](/merge-sort/) can count them for all positions in $O(n \log n)$ time, as in [counting inversions](/counting-inversions/).
- **Linear time, lexicographic.** Mareš and Straka (2007) rank and unrank in lexicographic order with $O(n)$ arithmetic operations on a RAM.
- **Linear time, another order.** Myrvold and Ruskey (2001) rank a permutation in their own order with $O(n)$ operations, with the help of the inverse permutation: record the value at the last position, exchange the largest value into the last position, and recurse on the first $n - 1$ positions. The rank is the mixed-radix number of the recorded values.

The digits combine into the rank by Horner's rule for the mixed radix: $r \leftarrow r \cdot (n - i + 1) + c_i$ for $i = 1, \ldots, n$. Each step multiplies a number of $O(n \log n)$ bits by a number below $n + 1$.

## Bounds

- **Lower bound.** $\Omega(n)$ time, to read the input. The output has $n \lg n - \Theta(n)$ bits.
- **Upper bounds.** $O(n \log n)$ word operations by a Fenwick tree when the rank fits in $O(1)$ words. $O(n)$ arithmetic operations, by Mareš and Straka for lexicographic order and by Myrvold and Ruskey for their order.
- **Big ranks.** For large $n$ the rank has $\Theta(n \log n)$ bits. With $w$-bit words, Horner's rule takes $n$ steps of $O(n \log n / w)$ word operations each, so $O(n^2 \log n / w)$ in total. This term is larger than the cost of the Lehmer code when $n$ is large.

## Reductions

- **To and from unranking.** Ranking and unranking are inverse maps. Each step of a [lexicographic successor](/lexicographic-permutation-successor/) is $\pi \mapsto$ unrank(rank$(\pi) + 1)$.
- **To inversion counting.** The sum $c_1 + \cdots + c_n$ is the number of inversions of $\pi$. So a rank algorithm that produces the Lehmer code also counts inversions, and the [sign](/permutation-sign/) of $\pi$ is $(-1)^{c_1 + \cdots + c_n}$.
- **To the factorial number system.** After the Lehmer code is known, ranking is the conversion of a [factorial number system](/factorial-number-system/) numeral to an integer.

## Applications

- **Perfect hashing of states.** A puzzle whose states are permutations, such as the 8-puzzle or the corners of a [Rubik's cube](/rubiks-cube-problem/), can store a value for each state in an array of size $n!$, indexed by the rank.
- **Compact storage.** The rank stores a permutation in $\lceil \lg n! \rceil$ bits, the least possible, instead of $n \lceil \lg n \rceil$ bits.
- **Parallel listing.** Split $0, \ldots, n! - 1$ into ranges, and let each processor unrank the start of its range and list from there with successor steps.
- **Comparisons of positions.** The rank tells how far apart two permutations are in lexicographic order.

## References
