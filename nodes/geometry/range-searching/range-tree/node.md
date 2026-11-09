---
tag: XGPFAM
kind: data-structure
slug: range-tree
name: Range tree
aliases:
- 2D range tree
- multi-level range tree
- multilevel range tree
- Bentley range tree
area: geometry/range-searching
level: core
summary: Balanced search tree on one coordinate whose nodes store secondary trees on the remaining coordinates; O(log^d n) query time in d dimensions.
implements: [range-query-structure]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of reported points}
  time: {build: O(n log^(d-1) n) worst case, report: O(log^d n + k) worst case, count: O(log^d n) worst case}
  space: {total: O(n log^(d-1) n) worst case}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1979
  people: [Jon Louis Bentley, George S. Lueker, D. T. Lee, C. K. Wong, Dan E. Willard]
  note: The range tree was found independently around 1978 to 1980 by Bentley, by Lueker, by Lee and Wong, and by Willard.
prereqs: [orthogonal-range-searching, balanced-binary-search-tree, bst-range-search]
see_also: [range-tree-query, layered-range-tree, kd-tree, segment-tree, two-dimensional-segment-tree, merge-sort-tree, decomposable-searching-problem, orthogonal-range-counting]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.3, Range Trees (Lemma 5.6, Theorem 5.8) and Section 5.4, Higher-Dimensional Range Trees (Theorem 5.11); notes in Section 5.7
  - paper: doi:10.1016/0020-0190(79)90117-0
    title: Jon Louis Bentley, Decomposable searching problems, Information Processing Letters 8(5), 1979, pages 244 to 251
    locator: the range tree as an example of a decomposable structure (DOI to be checked)
  - paper: doi:10.1145/358841.358850
    title: Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4), 1980, pages 214 to 229
    locator: range trees in d dimensions and their recurrences
  - paper: doi:10.1109/SFCS.1978.1
    title: George S. Lueker, A data structure for orthogonal range queries, 19th Annual Symposium on Foundations of Computer Science, 1978, pages 28 to 34
    locator: the multi-level structure with dynamic updates (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (range trees, multi-level structures and Table 40.2.1)
---

A range tree is a static structure for [orthogonal range searching](/orthogonal-range-searching/) on a set $P$ of $n$ points in $\mathbb{R}^d$. Its first level is a balanced binary search tree on the first coordinate, and each node of it carries an associated range tree, on the remaining $d - 1$ coordinates, of the points in its subtree; the last level is a sorted array. A query box is cut into $O(\log n)$ canonical subtrees per level, so a query reports the $k$ points of the box in $O(\log^{d} n + k)$ time and counts them in $O(\log^{d} n)$ time, with $O(n \log^{d-1} n)$ space and preprocessing.

## In plain words

To find all points in a rectangle, first find the points whose left-to-right position is right, then among those keep the ones whose height is right. A search tree sorted by left-to-right position splits any stretch of positions into a few blocks that the tree already has as whole branches. If every branch also keeps its own points sorted by height, each block can be searched by height directly.

So the structure is a tree of points sorted one way, and every branch of it holds a second sorted list of the same points sorted the other way. A point appears once in each level of the first tree, so the memory grows by a factor equal to the number of levels. In more dimensions the idea repeats: each branch holds a whole structure for the remaining directions.

## The abstract type

The range tree is a static [range query structure](/range-query-structure/). It is built from a multiset $P$ of $n$ points in $\mathbb{R}^d$ and answers, for a closed box $Q = [a_1, b_1] \times \dots \times [a_d, b_d]$:

- **REPORT(Q)**: all points of $P \cap Q$, each copy once;
- **COUNT(Q)**: $|P \cap Q|$;
- more generally, the sum of semigroup weights over $P \cap Q$, if each canonical node stores the sum of its weights.

**Notation.** $P$ is the input point set, $n = |P|$, $d$ the dimension, $p = (p_1, \dots, p_d)$ a point, with $p = (x, y)$ when $d = 2$, and $k = |P \cap Q|$ the output size of REPORT. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/), and only comparisons of coordinates are made.

**Degenerate input.** No general position is assumed. Each level orders its points by the composite key $(p_j, \text{index})$, so the order is total even when coordinates repeat. A query side $[a_j, b_j]$ becomes the block of positions from the first point with $p_j \ge a_j$ to the last point with $p_j \le b_j$, found by a lower bound and an upper bound [binary search](/binary-search/). This is equivalent to de Berg's composite numbers (Section 5.5), and points on the boundary of $Q$ are reported.

## Representation

The structure for coordinates $j, j+1, \dots, d$ over a list $L$ of $m$ points sorted by $(p_j, \text{index})$ is:

- if $j = d$, the sorted array $L$ itself, with its keys $p_d$;
- otherwise, the array $L$ and a balanced binary tree $T$ over the positions $0, \dots, m - 1$: the root covers the block $[0, m)$, and a node covering $[lo, hi)$ with $hi - lo \ge 2$ has a left child covering $[lo, mid)$ and a right child covering $[mid, hi)$, where $mid = \lfloor (lo + hi)/2 \rfloor$. Every node $v$ stores $\mathrm{assoc}(v)$, the structure for coordinates $j + 1, \dots, d$ over the points of its block. The set of these points is the *canonical subset* $P(v)$.

The code numbers the nodes as in a heap (root 1, children $2v$ and $2v + 1$), so the tree needs no pointers. The tree has height $\lceil \log_2 m \rceil$. In the plane, $\mathrm{assoc}(v)$ is just the array of $P(v)$ sorted by $y$, and the structure is a [merge sort tree](/merge-sort-tree/) over the $x$-order.

**Invariant.** (1) Each level array is sorted by its composite key. (2) For every node $v$ of a level-$j$ tree, $\mathrm{assoc}(v)$ is the level-$(j+1)$ structure of exactly the points of the block of $v$.

## Operations

```pseudo id=main
BUILD(L, j)
L1  if j = d or L is empty then return the sorted array L
L2  T ← the balanced tree on the positions of L; a node covering [lo, hi) with hi − lo ≥ 2 has children covering [lo, mid) and [mid, hi), mid = ⌊(lo + hi)/2⌋
L3  for each node v of T in post-order do
L4      Y(v) ← [L[lo]] if v is a leaf, else MERGE(Y(left(v)), Y(right(v))) by (p_{j+1}, index)
L5      assoc(v) ← BUILD(Y(v), j + 1)
L6  return the array L with the tree T and the associated structures
```

The whole range tree is BUILD$(L_1, 1)$, where $L_1$ is $P$ sorted by $(p_1, \text{index})$. Line L4 is the merge step of merge sort, so the lists $Y(v)$ come out sorted by the next coordinate without a separate sort.

```pseudo id=query
QUERY(S, j, Q)
L7  lo ← the first position of S with p_j ≥ a_j; hi ← the first position with p_j > b_j
L8  if j = d then report S[lo .. hi − 1] (or add hi − lo to the count) and return
L9  for each canonical node v of the block [lo, hi) in the tree of S do
L10     QUERY(assoc(v), j + 1, Q)
```

The canonical nodes of a block $[lo, hi)$ are the maximal nodes whose block lies inside $[lo, hi)$. They are found as in a [segment tree](/segment-tree/) query: start at the root, skip a node disjoint from $[lo, hi)$, take a node inside it, and descend into both children of any other node. The [range tree query](/range-tree-query/) page gives the equivalent split-node walk of de Berg et al. in detail.

## Example

Take the points $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ and the query $Q = [3, 7] \times [2, 6]$. Sorted by $x$, the points are

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| point | $(2,3)$ | $(3,8)$ | $(4,7)$ | $(5,4)$ | $(6,6)$ | $(7,2)$ | $(8,1)$ | $(9,6)$ |

Line L7 at level 1 gives $lo = 1$ (the first $x \ge 3$) and $hi = 6$ (the first $x > 7$). The block $[1, 6)$ has three canonical nodes:

| canonical node | block | its points sorted by $y$ (the associated array) | positions with $2 \le y \le 6$ | reported |
|---|---|---|---|---|
| heap node 9 | $[1, 2)$ | $(3,8)$ | none | none |
| heap node 5 | $[2, 4)$ | $(5,4), (4,7)$ | $[0, 1)$ | $(5,4)$ |
| heap node 6 | $[4, 6)$ | $(7,2), (6,6)$ | $[0, 2)$ | $(7,2), (6,6)$ |

The query reports $(5,4), (7,2), (6,6)$, and the count is $0 + 1 + 2 = 3$. The structure stores $8$ entries in the $x$-array and $8$ entries on each of the $4$ levels of the $x$-tree, $40$ entries in all, which is $n(\log_2 n + 2)$.

## Correctness

The canonical nodes of $[lo, hi)$ have disjoint blocks whose union is $[lo, hi)$, and the block $[lo, hi)$ of a level-$j$ array is exactly the set of its points with $a_j \le p_j \le b_j$, since the array is sorted by $p_j$. By induction on $d - j$, QUERY$(S, j, Q)$ reports exactly the points of $S$ that satisfy the constraints on coordinates $j, \dots, d$, each once. The proof, with the bounds on canonical nodes, space and time, is in [the correctness proof](proofs/correctness/).

## Complexity

| operation or measure | cost | case |
|---|---|---|
| space, $d = 2$ | at most $n(\lceil \log_2 n \rceil + 2)$ entries, $O(n \log n)$ | worst case |
| space, $d \ge 2$ | $O(n \log^{d-1} n)$ | worst case |
| BUILD, $d \ge 2$ | $O(n \log^{d-1} n)$ after an $O(n \log n)$ sort | worst case |
| canonical nodes per block | at most $2 \lceil \log_2 m \rceil$ | worst case |
| REPORT | $O(\log^{d} n + k)$ | worst case |
| COUNT | $O(\log^{d} n)$ | worst case |
| REPORT with [fractional cascading](/layered-range-tree/) | $O(\log^{d-1} n + k)$ | worst case |
| INSERT or DELETE with weight-balanced trees and partial rebuilding | $O(\log^{d} n)$ | amortized |

Each point lies in one canonical subset per level of the first tree, which gives the factor $\lceil \log_2 n \rceil$ per dimension after the first. A query does two binary searches at each of the $O(\log^{d-1} n)$ associated structures it reaches, which gives $O(\log^{d} n)$, plus $O(1)$ per reported point. All bounds are on the [real RAM](/real-ram/) with exact comparisons.

## Variants

- **Layered range tree.** In the plane, replace the binary searches in the associated arrays by pointers between the arrays of a node and its children. Only the root array is searched, and a query takes $O(\log n + k)$ time; see [layered range tree](/layered-range-tree/) and [fractional cascading](/multiple-list-search/).
- **Counting and semigroup sums.** Store prefix sums of the weights in each associated array; a canonical node then contributes the difference of two prefix sums. For a semigroup without subtraction, store a [segment tree](/segment-tree/) or a [Fenwick tree](/fenwick-tree/) on each associated array.
- **Dynamic range trees.** Lueker (1978) and Willard and Lueker (1985) use weight-balanced trees ([BB[α] trees](/weight-balanced-tree/)) and rebuild a subtree with its associated structures when it becomes unbalanced; updates take $O(\log^{d} n)$ amortized time. See [dynamic range searching](/dynamic-range-searching/).
- **Two-dimensional segment tree.** A [segment tree whose nodes hold segment trees](/two-dimensional-segment-tree/) has the same shape on a grid and supports point updates.
- **Space-saving variants.** Chazelle's compressed range tree uses $O(n)$ words in the plane and counts in $O(\log n)$ time on the word RAM.

## When to use it

Use a range tree when the point set is static, the dimension is small (two to four), and the worst case query time matters more than memory. In the plane, $n \log_2 n$ entries is acceptable for millions of points. When memory is tight, use a [kd-tree](/kd-tree/) with $O(\sqrt{n} + k)$ query time, and when only counts are needed and the queries are known in advance, use the [offline sweep](/offline-orthogonal-range-counting/).

## Pitfalls

- **Bisect with the wrong side on line L7.** Computing `hi ← the first position with p_j ≥ b_j` drops the points with $p_j = b_j$, and `lo ← the first position with p_j > a_j` drops those with $p_j = a_j$. For a closed box, line L7 must use the lower bound for $a_j$ and the upper bound for $b_j$.
- **Sorting the associated lists by coordinate alone.** Two levels that order equal coordinates differently are still correct for reporting, but a structure that relies on positions, such as the pointers of the layered range tree, needs one consistent total order. Use $(p_j, \text{index})$ at every level, as line L4 does.
- **Building each associated structure by sorting.** Sorting $P(v)$ again at every node costs $O(n \log^2 n)$ in the plane. Line L4 merges the children's lists, which keeps the build at $O(n \log n)$.
- **Searching the associated structure of a node that is not canonical.** A query that walks the path to $a_1$ and the path to $b_1$ and searches the associated structure of every node on the paths reports points outside the box. Only maximal nodes whose block lies inside $[lo, hi)$ are searched (line L9).

## Implementations

## History

The range tree was discovered independently at the end of the 1970s by Jon Bentley (1979), George Lueker (1978), D. T. Lee and C. K. Wong (1980) and Dan Willard (1979), as recorded in the notes of de Berg et al., Section 5.7. Bentley's 1980 paper on multidimensional divide and conquer analysed it in $d$ dimensions. Lueker, and later Willard and Lueker (1985), made it dynamic with weight-balanced trees. Willard and Lueker, and independently Chazelle and Guibas through fractional cascading (1986), removed one logarithmic factor from the query time.

## References
