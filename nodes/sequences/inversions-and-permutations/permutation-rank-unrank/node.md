---
tag: NW945N
kind: algorithm
slug: permutation-rank-unrank
name: Permutation rank and unrank algorithm
aliases:
- Lehmer code ranking
area: sequences/inversions-and-permutations
level: core
summary: Compute the rank of a permutation, or the permutation of a given rank, in O(n^2) or O(n log n) time.
solves: [permutation-ranking, permutation-unranking]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
prereqs: [lehmer-code, factorial-number-system, fenwick-tree]
see_also: [permutation-ranking, permutation-unranking, lexicographic-successor, inversion-table, order-statistic-tree, random-permutation, generating-all-permutations, big-integer]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2 (generating all permutations, and the correspondence between permutations and mixed-radix numbers)
  - paper: "Wendy Myrvold and Frank Ruskey, Ranking and unranking permutations in linear time, Information Processing Letters 79(6) (2001) 281-284"
    locator: the O(n) ranking and unranking in a non-lexicographic order
---

Ranking a [permutation](/permutation/) gives its position among all $n!$ permutations of $[n]$ in lexicographic order, counted from 0, and unranking turns a position back into the permutation. Both go through the [Lehmer code](/lehmer-code/): the rank is the code read as a number in the [factorial number system](/factorial-number-system/). A [Fenwick tree](/fenwick-tree/) over the unused values finds each digit, or the item that a digit selects, in $O(\log n)$ time, so both directions take $O(n \log n)$ time instead of the $O(n^2)$ of the direct method. The rank has about $n \lg n$ bits, so for $n > 20$ it is a [big integer](/big-integer/).

## In plain words

Write all arrangements of the numbers 1 to $n$ in dictionary order and number them from 0. Ranking asks for the number of a given arrangement, and unranking asks for the arrangement with a given number.

Count the arrangements that come before yours. They agree with yours up to some place and then have a smaller number there. At the first place, every unused number smaller than yours starts a whole block of arrangements, one for each order of the rest. Then go to the next place and do the same with the numbers that are left. The number of unused smaller numbers at each place is all you need, and a Fenwick tree counts it quickly.

Unranking runs the same steps backwards. Split the number into these counts, then at each place pick the unused number that has exactly that many unused numbers below it.

## The problem

**Ranking.** Given a permutation $a = a_1 \cdots a_n$ of $[n]$, return $\operatorname{rank}(a) = |\{\, b \in S_n : b < a \,\}|$, where $<$ is [lexicographic order](/lexicographic-order/). This is [permutation ranking](/permutation-ranking/).

**Unranking.** Given $n$ and an integer $0 \le r < n!$, return the permutation $a$ with $\operatorname{rank}(a) = r$. This is [permutation unranking](/permutation-unranking/).

## The algorithm

**The rank formula.** Let $c_i = |\{\, j > i : a_j < a_i \,\}|$ be the Lehmer code. Then
$$\operatorname{rank}(a) = \sum_{i=1}^{n} c_i\,(n-i)!.$$
A permutation $b < a$ first differs from $a$ at some position $i$, where $b_i < a_i$. The item $b_i$ must be one of the $c_i$ values smaller than $a_i$ that are not among $a_1, \ldots, a_{i-1}$, and the remaining $n - i$ positions can hold the remaining items in any of $(n-i)!$ orders. Summing over $i$ gives the formula.

**Ranking.** The value $c_i$ is the number of values smaller than $a_i$ that are still unused when position $i$ is reached. A Fenwick tree $T$ holds a count of 1 for each unused value, so $c_i$ is a prefix sum, and marking $a_i$ as used is a point update of $-1$. The rank is built by Horner's rule, multiplying by $n - i + 1$ before adding $c_i$, so that $c_i$ ends up with weight $(n-i)!$.

**Unranking.** Line L7 splits $r$ into its factorial-base digits, which are the Lehmer code $d_1, \ldots, d_n$ with $0 \le d_i \le n - i$. Then position $i$ gets the $(d_i + 1)$-th smallest unused value. SELECT finds it by a binary descent over the tree, which uses that the cell $T[p + s]$, for $p$ a multiple of $2s$ and $s$ a power of two, covers exactly the values $p + 1$ to $p + s$.

A full Fenwick tree in which every value has count 1 has $T[i] = \operatorname{lowbit}(i)$, the [lowest set bit](/lowest-set-bit/) of $i$, so lines L1 and L8 build it in $O(n)$ time.

```pseudo id=main
RANK(a[1 .. n])                                   ▷ a is a permutation of 1 .. n
L1  T[i] ← lowbit(i) for i ← 1 to n; r ← 0        ▷ every value is unused
L2  for i ← 1 to n do
L3      c ← PREFIX(T, a[i] − 1)                   ▷ unused values below a[i], the digit c_i
L4      ADD(T, a[i], −1)                          ▷ a[i] is used now
L5      r ← r · (n − i + 1) + c
L6  return r

UNRANK(r, n)                                      ▷ 0 ≤ r < n!
L7  for i ← n down to 1 do d[i] ← r mod (n − i + 1), r ← ⌊r / (n − i + 1)⌋
L8  T[i] ← lowbit(i) for i ← 1 to n
L9  for i ← 1 to n do
L10     a[i] ← SELECT(T, d[i] + 1)                ▷ the (d[i] + 1)-th smallest unused value
L11     ADD(T, a[i], −1)
L12 return a

SELECT(T, k)                                      ▷ 1 ≤ k ≤ number of unused values
L13 p ← 0, s ← the largest power of two that is at most n
L14 while s > 0 do (if p + s ≤ n and T[p + s] < k then p ← p + s, k ← k − T[p]), s ← s / 2
L15 return p + 1

PREFIX(T, i)                                      ▷ number of unused values in 1 .. i
L16 s ← 0; while i > 0 do s ← s + T[i], i ← i − lowbit(i)
L17 return s

ADD(T, i, δ)
L18 while i ≤ n do T[i] ← T[i] + δ, i ← i + lowbit(i)
```

## Example

**Ranking $a = 3\,1\,4\,5\,2$.** The tree starts as $T = (1, 2, 1, 4, 1)$, the counts of the values 1 to 5 grouped by the Fenwick cells.

| $i$ | $a_i$ | unused values before the step | $c_i$ | $r$ after line L5 |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 2 3 4 5 | 2 | $0 \cdot 5 + 2 = 2$ |
| 2 | 1 | 1 2 4 5 | 0 | $2 \cdot 4 + 0 = 8$ |
| 3 | 4 | 2 4 5 | 1 | $8 \cdot 3 + 1 = 25$ |
| 4 | 5 | 2 5 | 1 | $25 \cdot 2 + 1 = 51$ |
| 5 | 2 | 2 | 0 | $51 \cdot 1 + 0 = 51$ |

So $\operatorname{rank}(3\,1\,4\,5\,2) = 51 = 2 \cdot 4! + 0 \cdot 3! + 1 \cdot 2! + 1 \cdot 1! + 0 \cdot 0!$. At $i = 3$, PREFIX$(T, 3)$ reads $T[3] = 0$ and $T[2] = 1$, since the 1 and the 3 are used and the cell $T[2]$ covers the values 1 and 2.

**Unranking 51 with $n = 5$.** Line L7 divides by $1, 2, 3, 4, 5$: $51 \bmod 1 = 0$, $51 \bmod 2 = 1$ leaving 25, $25 \bmod 3 = 1$ leaving 8, $8 \bmod 4 = 0$ leaving 2, $2 \bmod 5 = 2$ leaving 0. So $d = (2, 0, 1, 1, 0)$. Then position 1 gets the 3rd smallest of $\{1, 2, 3, 4, 5\}$, which is 3; position 2 the 1st of $\{1, 2, 4, 5\}$, which is 1; position 3 the 2nd of $\{2, 4, 5\}$, which is 4; position 4 the 2nd of $\{2, 5\}$, which is 5; and position 5 gets 2. The result is $3\,1\,4\,5\,2$.

**One SELECT.** In the first step of this unranking, $k = 3$ and $s = 4$. The cell $T[4] = 4$ is not less than 3, so $p$ stays 0. With $s = 2$, $T[2] = 2 < 3$, so $p = 2$ and $k = 1$. With $s = 1$, $T[3] = 1$ is not less than 1. SELECT returns $p + 1 = 3$.

## Correctness

Ranking keeps two facts before step $i$: the tree holds count 1 exactly for the values not among $a_1, \ldots, a_{i-1}$, and $r = \sum_{k < i} c_k \prod_{t = k+1}^{i-1} (n - t + 1)$. So line L3 sets $c$ to the number of unused values below $a_i$, which are exactly the values after position $i$ that are smaller than $a_i$, the digit $c_i$. At the end each $c_k$ has the weight $\prod_{t=k+1}^{n} (n-t+1) = (n-k)!$, and the rank formula gives the result. Unranking produces the unique factorial-base digits of $r$, picks the items whose Lehmer code is that digit sequence, and so returns the permutation whose rank is $r$. The [full proof](proofs/correctness.md) also proves SELECT.

## Complexity

**Time.** Lines L1 and L8 take $O(n)$. Each PREFIX, ADD and SELECT runs at most $\lfloor \lg n \rfloor + 1$ rounds, and each direction makes $n$ calls of each kind it uses, so both take $O(n \log n)$ operations.

**Arithmetic on the rank.** The rank can be as large as $n! - 1$, with $\lceil \lg n! \rceil \approx n \lg n$ bits. If one arithmetic operation on such a number counts as one step, the bound above is the whole cost. With [big integers](/big-integer/), line L5 and line L7 each multiply or divide a number of $O(n \log n)$ bits by a small number, which costs $O(n \log n / w)$ word operations on $w$-bit words, for $O(n^2 \log n / w)$ in total. For $n \le 20$ every rank fits in 64 bits.

**Space.** $\Theta(n)$ words for $T$, the digits and the output.

**Lower bound and faster methods.** Ranking must read all $n$ items and unranking must write them, so $\Omega(n)$ is necessary. The digits $c_i$ are $n$ offline dominance counts, the same task as [counting inversions](/counting-inversions/) item by item, so word-RAM methods for offline range counting, such as the $O(n \sqrt{\log n})$ method of Chan and Pătraşcu, also compute them faster than $O(n \log n)$.

## Properties

- **Exact.** The rank is an integer with no rounding, and $\operatorname{unrank}(\operatorname{rank}(a)) = a$ for every permutation.
- **Order-preserving.** $a < b$ in lexicographic order exactly when $\operatorname{rank}(a) < \operatorname{rank}(b)$, so the rank of the [lexicographic successor](/lexicographic-successor/) is the rank plus 1.
- **By-product.** Ranking computes the whole Lehmer code, and so the number of [inversions](/inversion/), $\sum_i c_i$, at no extra cost.
- **Word RAM.** The values are used as array indices, so the method is not a comparison algorithm. For items from a general [total order](/total-order/), first replace them by their ranks.

## Variants and improvements

- **Direct $O(n^2)$ method.** Compute each $c_i$ by scanning the positions after $i$, and unrank with a plain list from which the chosen item is deleted. This is shorter and is faster for small $n$.
- **Order-statistic tree.** A balanced [order-statistic tree](/order-statistic-tree/) of the unused values gives the same $O(n \log n)$ bounds, with a larger constant.
- **Linear time in another order.** Myrvold and Ruskey rank and unrank in $O(n)$ arithmetic operations by using a different bijection between $[0, n!)$ and $S_n$, built from the swaps of a Fisher-Yates shuffle. The order is not lexicographic, but it is enough for storing permutations as numbers or indexing tables.
- **Inversion table instead of Lehmer code.** Using Knuth's [inversion table](/inversion-table/) as the digits gives another bijection with $[0, n!)$, which is the lexicographic rank of the inverse permutation.
- **Multisets.** For a sequence with repeated items, the number of arrangements before $a$ that first differ at position $i$ is a sum of multinomial coefficients, one for each smaller distinct unused value. This ranks [multiset permutations](/multiset-permutations/) in lexicographic order.
- **Partial permutations.** For ordered selections of $k$ of the $n$ items, the weight of position $i$ is $(n-i)!/(n-k)!$ instead of $(n-i)!$.

## When to use it

Use it to store a permutation in $\lceil \lg n! \rceil$ bits, to index an array of size $n!$ by permutations, to jump to the $k$-th permutation in lexicographic order, or to sample a uniform permutation from one uniform integer. For $n$ up to about 12 the direct $O(n^2)$ method is simpler and fast. If the order does not have to be lexicographic, the linear-time Myrvold-Ruskey method is faster for large $n$.

## Pitfalls

- **Rank from 0 or from 1.** This page counts from 0, so the identity has rank 0 and the reversal $n! - 1$. Many contest problems count from 1.
- **Overflow.** $20! < 2^{63} < 21!$. For $n \ge 21$ a 64-bit rank overflows, and the code must use big integers or arithmetic modulo a prime if only the rank modulo that prime is asked.
- **Digit order.** Line L7 produces the digits from the right, $d_n$ first. Filling them from the left gives a wrong permutation for most ranks.
- **Off by one in SELECT.** The digit $d_i$ asks for the $(d_i + 1)$-th smallest unused value. Calling SELECT$(T, d_i)$ fails when $d_i = 0$.
- **Values out of range.** RANK assumes the values are exactly $1, \ldots, n$. A repeated value or a value 0 breaks the tree; validate or compress first.

## Implementations

## History

The code is named after D. H. Lehmer, who used it around 1960 to rank and unrank permutations by computer, and the method is a standard example in books on combinatorial algorithms. In 2001 Myrvold and Ruskey gave a linear-time ranking and unranking for a different order of the permutations.

## References
