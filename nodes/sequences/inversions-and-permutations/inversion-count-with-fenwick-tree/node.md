---
tag: XH0RVP
kind: algorithm
slug: inversion-count-with-fenwick-tree
name: Counting inversions with a Fenwick tree
aliases:
- BIT inversion count
area: sequences/inversions-and-permutations
level: core
summary: Scan left to right and count larger earlier values with a binary indexed tree.
solves: [counting-inversions]
model: word-ram
complexity:
  vars: {n: the number of items, m: the number of distinct values}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [fenwick-tree, inversion, coordinate-compression]
see_also: [counting-inversions, inversion-count-by-merge-sort, lehmer-code, order-statistic-tree, dominance-counting, kendall-tau-distance]
sources:
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the tree of partial sums, the update and the prefix sum in O(log n) time
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 9 (range queries, the binary indexed tree)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 5.3 (the counting inversions problem and its O(n log n) bound)
---

Counting inversions with a Fenwick tree scans the array from left to right and, for each item, asks how many earlier items are larger than it. A [Fenwick tree](/fenwick-tree/) over the values holds how many times each value has been seen, so the question is one prefix sum, and recording the item is one point update. Each costs $O(\log m)$ time for $m$ distinct values, so the whole count takes $O(n \log n)$ time, the same as the [merge sort method](/inversion-count-by-merge-sort/). It does not move the data, it gives the count of every prefix on the way, and its code is a few lines. Values that are not small integers are first replaced by their ranks with [coordinate compression](/coordinate-compression/).

## In plain words

Walk along the list. Keep a tally sheet with one box for each possible value, and put a mark in the box of each number you pass. When you reach a new number, the out-of-order pairs that end at it are the earlier numbers that are bigger. That is the number of marks so far minus the number of marks in the boxes up to its own value.

Counting the marks in the first boxes one box at a time is slow. A Fenwick tree keeps a few partial totals so that this count, and adding one mark, each take only about as many steps as the number of binary digits of the number of boxes. If the values are large or not whole numbers, first replace each one by its place in the sorted list of values.

## The problem

The input is an array $A[1 \ldots n]$ of items from a [total order](/total-order/). The output is $\operatorname{inv}(A) = |\{(p, q) : p < q,\ A[p] > A[q]\}|$, the [counting inversions](/counting-inversions/) problem. Equal items do not form an inversion.

## The algorithm

Lines L1 and L2 compress the values to ranks $1$ to $m$, where equal items get equal ranks. Lines L3 to L7 do the scan. PREFIX and ADD are the two operations of the [Fenwick tree](/fenwick-tree/), with $\operatorname{lowbit}(i) = i \wedge (-i)$, the lowest set bit of $i$.

```pseudo id=main
COUNT-INVERSIONS-BIT(A[1 .. n])
L1  V ← the distinct values of A, sorted increasingly; m ← |V|
L2  for j ← 1 to n do r[j] ← the position of A[j] in V   ▷ binary search, 1 ≤ r[j] ≤ m
L3  T[1 .. m] ← 0, c ← 0
L4  for j ← 1 to n do
L5      c ← c + (j − 1) − PREFIX(T, r[j])                 ▷ earlier items larger than A[j]
L6      ADD(T, m, r[j], 1)
L7  return c

PREFIX(T, i)                                             ▷ number of seen items with rank ≤ i
L8  s ← 0
L9  while i > 0 do s ← s + T[i], i ← i − lowbit(i)
L10 return s

ADD(T, m, i, d)                                          ▷ record d more items of rank i
L11 while i ≤ m do T[i] ← T[i] + d, i ← i + lowbit(i)
```

Before step $j$, the tree holds the $j - 1$ items $A[1], \ldots, A[j-1]$. PREFIX$(T, r[j])$ counts those of them that are at most $A[j]$, so $(j - 1) - \mathrm{PREFIX}(T, r[j])$ counts those that are strictly larger. These are exactly the inversions $(p, j)$ with right end $j$. Line L6 adds $A[j]$ to the tree for the later steps. When $A$ is already a [permutation](/permutation/) of $[n]$, lines L1 and L2 are not needed: take $r = A$ and $m = n$.

**Scanning the other way.** A scan from right to left that adds PREFIX$(T, r[j] - 1)$, the number of later items that are strictly smaller, counts the same pairs from their left end. Its per-item counts are the [Lehmer code](/lehmer-code/) of a permutation.

## Example

Count the inversions of the permutation $A = [3, 1, 6, 2, 5, 4]$, so $r = A$ and $m = 6$. The column $T$ is the tree array after line L6.

| $j$ | $A[j]$ | PREFIX$(T, A[j])$ | larger earlier items | $c$ | $T[1 \ldots 6]$ after the update |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 0 | 0 | 0 0 1 1 0 0 |
| 2 | 1 | 0 | 1 (the 3) | 1 | 1 1 1 2 0 0 |
| 3 | 6 | 2 | 0 | 1 | 1 1 1 2 0 1 |
| 4 | 2 | 1 | 2 (3, 6) | 3 | 1 2 1 3 0 1 |
| 5 | 5 | 3 | 1 (6) | 4 | 1 2 1 3 1 2 |
| 6 | 4 | 3 | 2 (6, 5) | 6 | 1 2 1 4 1 2 |

The answer is 6. At step 4, PREFIX$(T, 2)$ reads only $T[2] = 1$, because the cell $T[2]$ covers the ranks 1 and 2, and it finds that one earlier item is at most 2.

**Repeated values.** For $A = [40, 10, 40, 30, 10]$, line L1 gives $V = [10, 30, 40]$ and line L2 gives the ranks $r = [3, 1, 3, 2, 1]$. The scan returns 6. At $j = 3$, PREFIX$(T, 3) = 2$ counts both earlier items, the 40 and the 10, as at most 40, so the equal 40 is not counted as larger.

## Correctness

The scan keeps this [loop invariant](/loop-invariant/): before step $j$, the tree represents the frequency array $f$ with $f[v] = |\{p < j : r[p] = v\}|$, and $c$ is the number of inversions $(p, q)$ with $q < j$. The Fenwick tree lemma, proved on the [Fenwick tree](/fenwick-tree/) page, says that PREFIX$(T, i)$ returns $f[1] + \cdots + f[i]$ and that ADD$(T, m, i, d)$ adds $d$ to $f[i]$. Because the compression preserves order and equality, $A[p] > A[j]$ holds exactly when $r[p] > r[j]$. So line L5 adds the number of inversions with right end $j$, and line L6 restores the invariant for $j + 1$. The full proof is below.

## Complexity

**Compression.** Line L1 sorts $n$ items, in $O(n \log n)$ time. Line L2 does $n$ binary searches in $V$, in $O(n \log m)$ time. With a hash map from values to ranks, line L2 takes $O(n)$ expected time instead.

**Scan.** Each PREFIX and ADD runs its loop at most $\lfloor \lg m \rfloor + 1$ times, because PREFIX clears one set bit of $i$ at each step and ADD at least doubles $\operatorname{lowbit}(i)$ at each step. The scan does $n$ of each, so it takes $O(n \log m)$ time.

**Total.** $O(n \log n)$ time in the worst case, since $m \le n$. The bound is tight up to a constant factor for inputs with $m = \Theta(n)$ distinct values. The extra space is $\Theta(n + m) = \Theta(n)$ words for $r$, $V$ and $T$.

**Model.** The scan uses ranks as array indices, so it runs in the [word RAM](/word-ram/) and not in the pure comparison model. Only the compression compares keys. When the input is a permutation of $[n]$, the compression is not needed, but the scan is still $\Theta(n \log n)$ in the worst case. Faster word-RAM methods exist, see [counting inversions](/counting-inversions/).

## Properties

- **Online.** After step $j$, $c$ is the inversion count of the prefix $A[1 \ldots j]$. If the ranks are known in advance, for example for a permutation of $[n]$, the items can arrive one at a time.
- **Does not move the data.** The array $A$ is read only.
- **Exact for repeated keys.** Equal keys get equal ranks, and the count uses PREFIX$(T, r[j])$, which includes the equal ones as not larger.
- **Per-item counts.** The amount added at line L5 is the number of larger earlier items of $A[j]$, with no extra work.

## Variants and improvements

- **Order-statistic tree.** A balanced [order-statistic tree](/order-statistic-tree/) of the seen keys answers "how many are larger than $x$" in $O(\log n)$ time without compression, and works when the values are not known in advance.
- **Linear-time build.** If the frequencies of all values are known, the Fenwick tree can be built in $O(m)$ time. That does not help this scan, which needs the frequencies of each prefix.
- **Range of values.** If the keys are integers in $[1, U]$ with $U$ not much larger than $n$, skip the compression and use a tree of size $U$. The time is $O(n \log U)$.
- **Inversions in a window.** With an ADD of $-1$ when an item leaves, the tree maintains the count of a sliding window, at $O(\log m)$ per step.
- **Segment tree.** A [segment tree](/segment-tree/) over the values does the same job with a larger constant factor.

## When to use it

Use it when the keys are integers in a small range, or a permutation, or when you want the count of each prefix. It is short, it does not change the input, and it is easy to get right. Use the [merge sort method](/inversion-count-by-merge-sort/) when the keys can only be compared, when the range of values is huge and you do not want to compress, or when you also want the sorted order.

## Pitfalls

- **Counting earlier items that are smaller.** Line L5 must add $(j - 1) - \mathrm{PREFIX}(T, r[j])$, the earlier items that are larger. Adding PREFIX$(T, r[j] - 1)$ in a left-to-right scan counts the earlier smaller items, which are non-inversions.
- **Ties.** Subtracting PREFIX$(T, r[j] - 1)$ instead of PREFIX$(T, r[j])$ in line L5 counts the earlier equal items as larger.
- **Rank 0.** A Fenwick tree is 1-based. With rank 0, ADD at index 0 never ends, because $\operatorname{lowbit}(0) = 0$. Line L2 must give ranks from 1 to $m$.
- **Compression with duplicates.** Ranks from a sort of the items, not of the *distinct* values, give equal keys different ranks, and the tie pitfall returns.
- **A 32-bit counter.** The count can reach $\binom n2$. Use a 64-bit integer.

## Implementations

## History

Fenwick introduced the tree in 1994 to keep cumulative frequency tables for arithmetic coding. Counting inversions with it is a standard exercise of competitive programming, and the Competitive Programmer's Handbook treats the tree in its chapter on range queries.

## References
