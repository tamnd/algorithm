---
tag: 9KXYQ9
kind: problem
slug: longest-increasing-subsequence
name: Longest increasing subsequence
aliases:
- LIS
area: sequences/subsequence-problems
level: intro
summary: Given a sequence, find a longest strictly increasing subsequence.
prereqs: [subsequence, binary-search, tabulation]
see_also: [patience-sorting, erdos-szekeres-theorem, dilworth-theorem, longest-common-subsequence, hunt-szymanski, young-tableau, dag-longest-path, colinear-chaining]
sources:
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 6.2, Longest increasing subsequences (the DAG view and the quadratic dynamic program)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4 and its exercises on the longest monotonically increasing subsequence, in O(n^2) and in O(n lg n) time
  - paper: "David Aldous and Persi Diaconis, Longest increasing subsequences: from patience sorting to the Baik-Deift-Johansson theorem, Bulletin of the American Mathematical Society 36(4), 1999, 413-432"
    locator: Section 1 (patience sorting and the pile lemma), Section 2 (the limit 2 sqrt(n) of Vershik-Kerov and Logan-Shepp) and the statement of the Baik-Deift-Johansson theorem
  - paper: "Michael L. Fredman, On computing the length of longest increasing subsequences, Discrete Mathematics 11(1), 1975, 29-35"
    locator: the upper and lower bounds on the number of comparisons, about n lg n - n lg lg n
  - paper: "C. Schensted, Longest increasing and decreasing subsequences, Canadian Journal of Mathematics 13, 1961, 179-191"
    locator: the main theorem (the length of the first row of the insertion tableau is the length of a longest increasing subsequence)
---

The longest increasing subsequence (LIS) problem takes a sequence of $n$ items from a total order and asks for a longest [subsequence](/subsequence/) whose items strictly increase. A [dynamic program](/tabulation/) solves it in $O(n^2)$ time, and the greedy pile method of [patience sorting](/patience-sorting/), with [binary search](/binary-search/), solves it in $O(n \log n)$ time, which is optimal for comparison algorithms. For a random permutation the answer is close to $2\sqrt{n}$. LIS is also the engine inside the [Hunt-Szymanski](/hunt-szymanski/) algorithm for the [longest common subsequence](/longest-common-subsequence/).

## In plain words

You have a row of numbers. You may cross out any of them, but you may not move them. You want the numbers that are left to go up from left to right, each one bigger than the one before. The question is how many numbers you can keep.

In the row 3, 1, 4, 1, 5, 9, 2, 6 you can keep four: 1, 4, 5, 9. You cannot keep five. A slow method looks at each number and asks how long an increasing run can end there, using the answers for the numbers before it. A fast method deals the numbers onto piles, like cards, and the number of piles is the answer.

## Definition

**Input.** A sequence $A = \langle a_1, \ldots, a_n \rangle$ of items from a totally ordered set.

**Output.** Indices $1 \le i_1 < i_2 < \cdots < i_k \le n$ with

$$a_{i_1} < a_{i_2} < \cdots < a_{i_k}$$

and $k$ as large as possible. The maximum $k$ is written $L(A)$. The length-only version outputs $L(A)$. For $n = 0$, $L(A) = 0$; for $n \ge 1$, $1 \le L(A) \le n$.

The problem is a longest path problem in a [directed acyclic graph](/dag-longest-path/): the vertices are the positions $1, \ldots, n$, and there is an edge $j \to i$ when $j < i$ and $a_j < a_i$. Each increasing subsequence is a path, and each path is an increasing subsequence.

## Variants

- **Non-decreasing.** Replace $<$ by $\le$. The fast method then searches for the first pile top that is strictly greater, not greater or equal.
- **Longest decreasing subsequence.** Reverse the order, or negate the numbers.
- **Counting.** Count the longest increasing subsequences (as index sets). The quadratic DP carries a count next to each length. An $O(n \log n)$ method keeps prefix sums of counts on each pile.
- **Weighted LIS.** Each item has a weight, and the goal is an increasing subsequence of maximum total weight. A [Fenwick tree](/fenwick-tree/) over the ranks of the values gives $O(n \log n)$ time.
- **Longest bitonic subsequence.** First increasing, then decreasing. Combine the LIS ending at each position with the longest decreasing subsequence starting there.
- **Two dimensions.** Pairs $(x, y)$ that must increase in both coordinates (the nesting of boxes or envelopes). Sort by $x$, break ties by $y$ in decreasing order, then run LIS on $y$.
- **Ulam's problem.** The distribution of $L(\pi)$ for a uniform random permutation $\pi$ of $\{1, \ldots, n\}$. See the Bounds section.

## Examples

Take $A = \langle 3, 1, 4, 1, 5, 9, 2, 6 \rangle$, so $n = 8$. Then $L(A) = 4$. There are four index sets that reach length 4, with the values $\langle 3,4,5,9 \rangle$, $\langle 3,4,5,6 \rangle$, $\langle 1,4,5,9 \rangle$ and $\langle 1,4,5,6 \rangle$. The longest non-decreasing subsequence also has length 4.

**The quadratic DP.** Let $\ell_i$ be the length of a longest increasing subsequence that ends at position $i$. Then $\ell_i = 1 + \max\{\ell_j : j < i,\ a_j < a_i\}$, with $\max \emptyset = 0$, and $L(A) = \max_i \ell_i$.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $a_i$ | 3 | 1 | 4 | 1 | 5 | 9 | 2 | 6 |
| $\ell_i$ | 1 | 1 | 2 | 1 | 3 | 4 | 2 | 4 |

**The pile method.** Keep an array $T$, where $T[k]$ is the smallest last item of an increasing subsequence of length $k+1$ seen so far. For each item $x$, find the first $k$ with $T[k] \ge x$ by binary search and set $T[k] = x$, or append $x$ if there is no such $k$.

| item | position $k$ | $T$ after the step |
| --- | --- | --- |
| 3 | 0 | [3] |
| 1 | 0 | [1] |
| 4 | 1 | [1, 4] |
| 1 | 0 | [1, 4] |
| 5 | 2 | [1, 4, 5] |
| 9 | 3 | [1, 4, 5, 9] |
| 2 | 1 | [1, 2, 5, 9] |
| 6 | 3 | [1, 2, 5, 6] |

The final length of $T$ is $L(A) = 4$. The final $T = [1, 2, 5, 6]$ is not an increasing subsequence of $A$ (the 2 comes after the 5), which is the classic pitfall below.

**Random permutations.** The exact mean of $L(\pi)$ over all $n!$ permutations, for small $n$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\mathbb{E}[L]$ | 1 | 3/2 | 2 | 29/12 | 67/24 | 2261/720 | 499/144 | 7601/2016 |

And the mean over random permutations (seed 1; 2000, 500, 100 and 20 runs) against $2\sqrt{n}$:

| $n$ | 100 | 1000 | 10000 | 100000 |
| --- | --- | --- | --- | --- |
| mean of $L$ | 16.79 | 58.15 | 192.85 | 619.95 |
| $2\sqrt{n}$ | 20.00 | 63.25 | 200.00 | 632.46 |

The gap is of order $n^{1/6}$, as the Baik-Deift-Johansson theorem predicts.

## Known algorithms

**Quadratic DP.** Compute $\ell_1, \ldots, \ell_n$ in order with the recurrence above, and keep for each $i$ the index $j$ that gave the maximum. Follow these links back from an $i$ with $\ell_i = L(A)$ to recover the subsequence. This takes $\Theta(n^2)$ time and $\Theta(n)$ space. It is the version in DPV Section 6.2, where it is a longest path in the DAG of the Definition. It needs only comparisons, and it extends to the weighted and counting variants.

**Binary search on pile tops ($O(n \log n)$).** This is the pile method of the Examples, the first phase of [patience sorting](/patience-sorting/).

```pseudo id=lis
LIS-LENGTH(A[1 .. n])
L1  T ← empty array                      ▷ T[k] = least tail of an increasing subsequence of length k + 1
L2  for i ← 1 to n do
L3      k ← the least index with T[k] ≥ A[i], or |T| if there is none
L4      if k = |T| then append A[i] to T
L5      else T[k] ← A[i]
L6  return |T|
```

The invariant is: after step $i$, $T$ is strictly increasing, and for each $k < |T|$, $T[k]$ is the least possible last item of an increasing subsequence of length $k + 1$ in $A[1 \ldots i]$, and no increasing subsequence of $A[1 \ldots i]$ is longer than $|T|$. Line L3 is a binary search because $T$ is sorted. If $A[i]$ can extend a subsequence of length $k$ with tail $T[k-1] < A[i]$, it gives a subsequence of length $k + 1$ with tail $A[i] \le T[k]$, and it cannot extend any longer one, because $T[k] \ge A[i]$ and the later tails are larger. So the update keeps the invariant. The [patience sorting](/patience-sorting/) page proves the equivalent pile lemma in full. To output a subsequence, store with each item the index of the item at $T[k-1]$ when it was placed, and follow these links back from the last item of $T$. The time is $O(n \log L(A))$ and the space $O(n)$.

**Through LCS.** $L(A)$ is the length of a [longest common subsequence](/longest-common-subsequence/) of $A$ and the sorted sequence of the distinct values of $A$. This takes $O(n^2)$ time with the [LCS table](/lcs-dynamic-programming/), so it is a reduction, not a fast method.

**Young tableaux.** Schensted's insertion builds a [Young tableau](/young-tableau/) from $A$; the first row is exactly the array $T$ above, and its length is $L(A)$. The number of rows is the length of a longest decreasing subsequence.

## Bounds

- **Comparison lower bound.** Fredman (1975) proved that computing $L(A)$ needs about $n \lg n - n \lg \lg n$ comparisons in the worst case, and that the pile method with a careful search reaches this, up to $O(n)$. So $\Theta(n \log n)$ is tight for comparison algorithms.
- **Output-sensitive.** The pile method takes $O(n \log L(A))$ comparisons, because $|T| \le L(A)$ at each step.
- **Integer inputs.** When the items are integers in a small range, the search of line L3 is a predecessor query, and faster integer data structures beat $n \log n$. This does not contradict Fredman's bound, which is for comparisons only.
- **Monotone subsequences always exist.** By the [Erdős-Szekeres theorem](/erdos-szekeres-theorem/), each sequence of $n$ distinct items has an increasing or a decreasing subsequence of length at least $\lceil \sqrt{n} \rceil$. More exactly, $L_{\text{inc}}(A) \cdot L_{\text{dec}}(A) \ge n$.
- **Random permutations.** For a uniform random permutation, $\mathbb{E}[L] / \sqrt{n} \to 2$ (Vershik and Kerov, and Logan and Shepp, both 1977). Baik, Deift and Johansson (1999) proved that $(L - 2\sqrt{n}) / n^{1/6}$ converges in distribution to the Tracy-Widom distribution of the largest eigenvalue of a random Hermitian matrix. Aldous and Diaconis survey both results.

## Reductions

- **LIS to longest path in a DAG.** The graph of the Definition has $n$ vertices and up to $\binom{n}{2}$ edges; see [DAG longest path](/dag-longest-path/).
- **LIS to LCS.** As in Known algorithms, $L(A) = |\mathrm{LCS}(A, \mathrm{sort}(A))|$ with duplicates removed from the sorted copy.
- **LCS to LIS.** For two sequences $X$ and $Y$, list the matching pairs $(i, j)$ with $x_i = y_j$, in increasing order of $i$ and, for equal $i$, in decreasing order of $j$. A longest strictly increasing subsequence of the $j$ values is an LCS. This is the [Hunt-Szymanski](/hunt-szymanski/) algorithm, fast when there are few matches.
- **Chain partitions.** By Mirsky's theorem, the dual of [Dilworth's theorem](/dilworth-theorem/), for the order "$i < j$ and $a_i < a_j$", the least number of non-increasing subsequences that cover $A$ equals $L(A)$. The piles of patience sorting are such a cover.

## Applications

- **Patience diff.** A line-based diff that first matches the lines that occur exactly once in each file, then keeps a longest increasing subsequence of these matches, so that the matched lines stay in order.
- **Sparse LCS and chaining.** In [colinear chaining](/colinear-chaining/) of genome alignments, a chain of anchors that increase in both sequences is a two-dimensional LIS.
- **Nesting problems.** Boxes, envelopes and intervals that must nest in a chain reduce to the two-dimensional variant.
- **Sortedness measures.** For distinct items, $n - L(A)$ is the least number of items to remove to make $A$ sorted, and also the least number of items to take out and insert at another place.

## References
