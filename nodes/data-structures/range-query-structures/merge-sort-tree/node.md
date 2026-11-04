---
tag: 8KPVMD
kind: data-structure
slug: merge-sort-tree
name: Merge sort tree
aliases:
- range tree of sorted lists
area: data-structures/range-query-structures
level: advanced
summary: Segment tree whose nodes store sorted copies of their ranges, answering counting and k-th queries.
implements: [range-query-structure]
model: comparison-model
complexity:
  vars: {n: the length of the array}
  time: {worst: O(log² n)}
  space: {extra: Θ(n log n)}
prereqs: [segment-tree, merge-sort, binary-search]
see_also: [wavelet-tree, persistent-segment-tree, range-kth-smallest-query, multiple-list-search, range-tree, inversion-count-by-merge-sort, offline-query-processing, sqrt-tree]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 28, Segment trees revisited, Section 28.3 Data structures (a segment tree whose nodes hold data structures, and the memory cost O(n log n))
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the subsections Find the smallest number greater or equal to a specified number, without and with modification queries, and Acceleration with fractional cascading
  - paper: doi:10.1007/BF01840440
    title: "Bernard Chazelle and Leonidas J. Guibas, Fractional cascading: I. A data structuring technique, Algorithmica 1 (1986), 133-162"
    locator: the technique for searching the same key in many sorted lists along a path of a tree, used to remove one logarithmic factor
---

A merge sort tree is a [segment tree](/segment-tree/) in which each node stores the items of its range in sorted order. The lists of a node are the merge of the lists of its two children, exactly as in the recursion of [merge sort](/merge-sort/), so the whole tree is built in $O(n \log n)$ time and takes $\Theta(n \log n)$ space. A query on a range $[l, r)$ splits it into $O(\log n)$ nodes and does a [binary search](/binary-search/) in each, so counting the items of $A[l \ldots r-1]$ that are below $x$ takes $O(\log^2 n)$ time, and the $k$-th smallest item of a range takes $O(\log^3 n)$ by an outer binary search, or less with the refinements below. It is static: point updates need a balanced tree in each node.

## In plain words

Picture the steps of merge sort written down, not thrown away. At the bottom each item is alone. One level up, pairs are sorted. Above that, groups of four are sorted, and so on, until the top holds the whole array in sorted order.

To ask "how many numbers between position $l$ and position $r$ are smaller than 10?", cover the stretch with a few of these sorted groups, the same few that a segment tree would use. In each sorted group, finding how many are smaller than 10 is one binary search. Add up the counts.

## The abstract type

A static array $A[0 \ldots n-1]$ of items from a totally ordered set. The queries are:

- $\textsc{count}(l, r, x)$ with $0 \le l \le r \le n$: the number of $k \in [l, r)$ with $A[k] < x$; the forms "at most $x$" and "in $[x, y)$" follow by one or two calls;
- $\textsc{successor}(l, r, x)$: the least $A[k] \ge x$ with $k \in [l, r)$, or none;
- $\textsc{kth}(l, r, k)$ with $1 \le k \le r - l$: the $k$-th smallest item of $A[l \ldots r-1]$.

## Representation

Let $N$ be $n$ rounded up to a power of two. The nodes are numbered as in a bottom-up segment tree: node 1 is the root over $[0, N)$, node $v$ over $[lo, hi)$ has the children $2v$ over $[lo, mid)$ and $2v + 1$ over $[mid, hi)$, and leaf $N + i$ is position $i$. Node $v$ stores the sorted list $S_v$ of $\{A[k] : k \in [lo, hi), k < n\}$, with repeats. Each item is in exactly one list per level, so the lists have $n (\lg N + 1)$ items in total.

## Operations

```pseudo id=main
COUNT(l, r, x)                             ▷ #{k ∈ [l, r) : A[k] < x}
L1  c ← 0, l ← l + N, r ← r + N
L2  while l < r do
L3      if l is odd then c ← c + LOWER(S_l, x), l ← l + 1
L4      if r is odd then r ← r − 1, c ← c + LOWER(S_r, x)
L5      l ← l / 2, r ← r / 2
L6  return c
```

LOWER$(S, x)$ is the number of items of the sorted list $S$ that are less than $x$, found by binary search. Lines L2 to L5 visit the canonical nodes of $[l, r)$, at most two per level, as in the bottom-up segment tree.

```pseudo id=build
BUILD(A)
L7  for i ← 0 to n − 1 do S_(N+i) ← [A[i]]
L8  for v ← N − 1 down to 1 do S_v ← MERGE(S_(2v), S_(2v+1))
```

```pseudo id=kth
KTH(l, r, k)                               ▷ binary search over the root list
L9  lo ← 0, hi ← n − 1                     ▷ indices into S_1, the whole array sorted
L10 while lo < hi do
L11     m ← ⌊(lo + hi) / 2⌋
L12     if COUNT(l, r, S_1[m]) + #{items equal to S_1[m] in [l, r)} ≥ k then hi ← m else lo ← m + 1
L13 return S_1[lo]
```

In code, line L12 is one call that counts the items at most $S_1[m]$, by an upper-bound search instead of a lower-bound search in each node.

## Example

Take $A = [5, 2, 8, 6, 3, 7, 9, 1]$, so $n = N = 8$.

| level | lists |
|---|---|
| leaves | $[5]$, $[2]$, $[8]$, $[6]$, $[3]$, $[7]$, $[9]$, $[1]$ |
| pairs | $[2, 5]$, $[6, 8]$, $[3, 7]$, $[1, 9]$ |
| fours | $[2, 5, 6, 8]$, $[1, 3, 7, 9]$ |
| root | $[1, 2, 3, 5, 6, 7, 8, 9]$ |

$\textsc{count}(1, 7, 7)$ asks how many of $A[1 \ldots 6] = 2, 8, 6, 3, 7, 9$ are below 7. The canonical nodes of $[1, 7)$ are the leaf $[1, 2)$ with $[2]$, the pair $[2, 4)$ with $[6, 8]$, the pair $[4, 6)$ with $[3, 7]$ and the leaf $[6, 7)$ with $[9]$. The binary searches give $1 + 1 + 1 + 0 = 3$, for the items 2, 6 and 3.

$\textsc{kth}(1, 7, 3)$ searches the root list $1, 2, 3, 5, 6, 7, 8, 9$ for the least value $v$ with at least 3 items $\le v$ in the range: 5 gives 2 items (2 and 3), 6 gives 3, so the answer is 6, and indeed $2, 3, 6, 7, 8, 9$ is the range sorted.

## Correctness

Each list $S_v$ is the sorted multiset of its range, by induction from the leaves: MERGE of two sorted lists is the sorted union. The canonical nodes visited by lines L2 to L5 are disjoint and their union is $[l, r)$, as for any bottom-up segment tree, so the sum of LOWER over them counts each position of $[l, r)$ once, and exactly when its item is below $x$. KTH is a binary search for the least root item $v$ with $\#\{k \in [l, r) : A[k] \le v\} \ge k$; this count is non-decreasing in $v$, and the least such $v$ is the $k$-th smallest item, which is in the root list. The [proof](proofs/correctness.md) gives the details.

## Complexity

**Build.** Level by level, the merges cost $O(n)$ per level, $O(n \log n)$ in total, and the space is $n (\lceil \lg n \rceil + 1)$ items plus $O(N)$ list headers.

**Count and successor.** At most $2 \lg N$ canonical nodes, each with one binary search on at most $n$ items: $O(\log^2 n)$ time.

**K-th.** $O(\log n)$ steps of the outer search, each a count: $O(\log^3 n)$. A better method walks down from the root: with fractional cascading, or with the *rank of the split* stored at each node as in the [wavelet tree](/wavelet-tree/), the $k$-th smallest is found in $O(\log n)$, but then the structure is no longer a plain merge sort tree.

## Variants

- **Fractional cascading.** Store with each item of $S_v$ its position in $S_{2v}$ and in $S_{2v+1}$. Then one binary search at the root gives the position of $x$ in all lists on the way down, and COUNT takes $O(\log n)$ time; this is fractional cascading on the tree, a solution of the [multiple list search](/multiple-list-search/) problem, from Chazelle and Guibas, and cp-algorithms shows it for the merge sort tree.
- **Prefix sums in the nodes.** Store the prefix sums of each sorted list to answer "the sum of the items of $[l, r)$ below $x$" in the same $O(\log^2 n)$ time.
- **Updates.** Replace each sorted list by a balanced search tree or an order statistic tree; a point update changes $O(\log n)$ trees, at $O(\log^2 n)$ cost, and queries stay $O(\log^2 n)$.
- **Offline alternatives.** Sorting the queries by $x$ and adding the items to a Fenwick tree in increasing order answers all counting queries in $O((n + q) \log n)$ with $O(n)$ space, see [offline query processing](/offline-query-processing/).
- **Two-dimensional range tree.** The merge sort tree over the points sorted by $x$, with lists sorted by $y$, is the two-level [range tree](/range-tree/) for counting points in rectangles.
- **Persistent segment tree.** A [persistent segment tree](/persistent-segment-tree/) over the values answers counting and $k$-th queries online in $O(\log n)$ with $O(n \log n)$ space.

## When to use it

Use a merge sort tree for online counting or successor queries over ranges of a static array, such as "how many items of $A[l \ldots r]$ are in $[x, y]$" or "the smallest item at least $x$ in $A[l \ldots r]$", when its short code matters more than the logarithmic factors. For the $k$-th smallest, a wavelet tree or a persistent segment tree is faster. If the queries can be answered offline, a sweep with a Fenwick tree is faster and uses less memory.

## Pitfalls

- **Memory.** $n = 10^6$ with 8-byte items gives about 160 MB; a wavelet tree needs $n \lg \sigma$ bits plus small indexes instead.
- **Lower and upper bound.** "Below $x$" and "at most $x$" differ by the items equal to $x$; mixing them in KTH returns a neighbour of the right answer when there are duplicates.
- **The empty range.** COUNT with $l = r$ returns 0, and KTH must reject $k > r - l$.
- **Recursion in the build.** Building by recursion on $n$ items is fine for depth $\lg n$, but merging with list concatenation in a high-level language can cost $O(n \log^2 n)$; merge into a preallocated list.

## Implementations

## History

The structure is the range tree idea of storing a sorted list at each node of a balanced tree, used by Bentley and others for orthogonal range searching in the late 1970s, applied to the positions of an array. Its name comes from competitive programming, where it is taught as a segment tree whose nodes hold the sorted lists of merge sort. Chazelle and Guibas (1986) gave fractional cascading, which removes one logarithmic factor from searches along a path of such lists.

## References
