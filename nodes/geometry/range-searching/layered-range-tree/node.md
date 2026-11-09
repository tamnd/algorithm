---
tag: HMB009
kind: data-structure
slug: layered-range-tree
name: Layered range tree
aliases:
- fractional cascaded range tree
- range tree with fractional cascading
- layered range tree with cascading pointers
area: geometry/range-searching
level: advanced
summary: Range tree in which fractional cascading links the secondary structures, saving one log factor in the query time.
implements: [range-query-structure]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of reported points}
  time: {build: O(n log n) worst case, report: O(log n + k) worst case, count: O(log n) worst case, report_d: O(log^(d-1) n + k) worst case}
  space: {total: O(n log n) worst case, total_d: O(n log^(d-1) n) worst case}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1985
  people: [Dan E. Willard, George S. Lueker, Bernard Chazelle, Leonidas J. Guibas]
  note: Willard and Lueker linked the associated arrays of a range tree by pointers; Chazelle and Guibas made the idea general as fractional cascading in 1986.
prereqs: [range-tree, range-tree-query, multiple-list-search]
see_also: [range-tree, range-tree-query, multiple-list-search, fractional-cascading-bridge, merge-sort-tree, wavelet-tree, orthogonal-range-reporting, orthogonal-range-counting]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.6, Fractional Cascading (the layered range tree and its query); notes in Section 5.7
  - paper: doi:10.1137/0214019
    title: Dan E. Willard, New data structures for orthogonal range queries, SIAM Journal on Computing 14(1), 1985, pages 232 to 253
    locator: the pointers between the associated arrays and the O(log^(d-1) n + k) query (DOI to be checked)
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading. I. A data structuring technique, Algorithmica 1, 1986, pages 133 to 162
    locator: the general technique and its application to orthogonal range search (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (orthogonal range searching, Table 40.2.1)
---

A layered range tree is a two-dimensional [range tree](/range-tree/) in which every entry of the $y$-sorted array of a node knows where the same $y$-value would fall in the arrays of the node's two children. A query does one binary search for each end of $[y_1, y_2]$, at the split node, and then only follows these links down the two search paths, so it reports the $k$ points of a box in $O(\log n + k)$ time and counts them in $O(\log n)$ time in the worst case, with $O(n \log n)$ space. This is the special case of [fractional cascading](/multiple-list-search/) in which every list is a subset of its parent, so no fractional sampling is needed. In $d \ge 2$ dimensions, using it at the last two levels gives $O(\log^{d-1} n + k)$ query time.

## In plain words

A range tree answers a rectangle question by picking a few branches whose points have the right left-to-right position, then searching each branch's list, sorted by height, for the right heights. Every one of these searches looks for the same two heights, which is wasteful.

The fix is to search only once, in the list at the top, and to remember in every list, for each entry, where the same place is in the lists of the two branches below. Then moving down the tree also moves the search result down, for free. Each branch that is picked can be read off at once, without searching it again.

## The abstract type

The layered range tree is a static [range query structure](/range-query-structure/) for points in the plane. It is built from a multiset $P$ of $n$ points and answers, for a closed box $Q = [x_1, x_2] \times [y_1, y_2]$:

- **REPORT(Q)**: all points of $P \cap Q$, each copy once;
- **COUNT(Q)**: $|P \cap Q|$.

**Notation.** $n = |P|$, $p = (x, y)$ a point, $k = |P \cap Q|$. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/), and only coordinates are compared.

**Degenerate input.** No general position is assumed. The leaves follow the order of $(p_x, p_y, j)$ and the arrays the order of $(p_y, p_x, j)$, where $j$ is the position in $x$-order, so every key is distinct even when points repeat. Boundary points of $Q$ are reported.

## Representation

- **Primary tree.** A balanced leaf-based binary tree over the positions $0, \dots, n - 1$ of the $x$-order. A node covering $[lo, hi)$ with $hi - lo \ge 2$ has children covering $[lo, mid)$ and $[mid, hi)$, $mid = \lfloor (lo + hi)/2 \rfloor$. The code numbers the nodes as in a heap (root 1, children $2v$ and $2v + 1$).
- **Associated array.** Each node $v$ stores $A(v)$, the points of its block sorted by the key $(p_y, p_x, j)$, and their $y$-values.
- **Cascading array.** Each internal node stores $\mathrm{left}(v)[i]$ for $i = 0, \dots, |A(v)|$: the number of entries of $A(\mathrm{lc}(v))$ among the first $i$ entries of $A(v)$. The number of entries of $A(\mathrm{rc}(v))$ among them is $i - \mathrm{left}(v)[i]$.

Since the keys are distinct and $A(v)$ is sorted, the first $i$ entries of $A(v)$ are exactly the entries with key less than $A(v)[i]$. So $\mathrm{left}(v)[i]$ is the index in $A(\mathrm{lc}(v))$ of the first entry with key at least $A(v)[i]$. This is the pointer of de Berg et al., Section 5.6, stored as a count.

**Invariant.** (1) $A(v)$ is the block of $v$ sorted by $(p_y, p_x, j)$. (2) $\mathrm{left}(v)[0] = 0$, and $\mathrm{left}(v)[i+1] - \mathrm{left}(v)[i]$ is $1$ if $A(v)[i]$ lies in the left child's block and $0$ otherwise.

## Operations

```pseudo id=main
BUILD(P)
L1  sort P by (p_x, p_y, index); position j holds the j-th point
L2  for each node v of the primary tree in post-order do
L3      if v is a leaf at position j then A(v) ← [the point j]
L4      else merge A(lc(v)) and A(rc(v)) by (p_y, p_x, j) into A(v); left(v)[i] ← how many of the first i merged entries came from A(lc(v))
L5      store the y-values of A(v)
```

Line L4 is one merge, and the counts are written during it, so the build costs $O(n)$ per level of the tree.

```pseudo id=query
QUERY([x1, x2] × [y1, y2])
L6  lo ← first position with p_x ≥ x1; hi ← last position with p_x ≤ x2; if lo > hi or y1 > y2 then return
L7  v_split ← the deepest node whose block contains lo and hi
L8  s ← first index of A(v_split) with p_y ≥ y1; t ← first index with p_y > y2
L9  if v_split is a leaf then report A(v_split)[s .. t − 1] and return
L10 v ← lc(v_split); (s, t) ← (left(v_split)[s], left(v_split)[t])
L11 while v is not a leaf do
L12     if lo < the middle of v then report A(rc(v))[s − left(v)[s] .. t − left(v)[t] − 1]; v ← lc(v); (s, t) ← (left(v)[s], left(v)[t])
L13     else v ← rc(v); (s, t) ← (s − left(v)[s], t − left(v)[t])
L14 report A(v)[s .. t − 1]
L15 repeat lines L11 to L14 from v ← rc(v_split), (s, t) ← (s − left(v_split)[s], t − left(v_split)[t]) of line L8, with hi in place of lo and the roles of the children exchanged
L16 report A(v)[s .. t − 1] for the last leaf v of that path
```

In lines L12 and L13 the values $\mathrm{left}(v)[s]$ and $\mathrm{left}(v)[t]$ are read before $v$, $s$ and $t$ are updated. COUNT adds the lengths $t - s$ of the slices instead of reporting them. The walk is that of the [range tree query](/range-tree-query/); only lines L8, L10, L12, L13 and L15 differ.

## Example

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ and $Q = [3, 7] \times [2, 6]$. In $x$-order the points are $(2,3), (3,8), (4,7), (5,4), (6,6), (7,2), (8,1), (9,6)$, so $lo = 1$, $hi = 5$, and the root $[0, 8)$ is the split node. The root array and its counts are:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $A(\text{root})[i]$ | $(8,1)$ | $(7,2)$ | $(2,3)$ | $(5,4)$ | $(6,6)$ | $(9,6)$ | $(4,7)$ | $(3,8)$ | |
| child | right | right | left | left | right | right | left | left | |
| $\mathrm{left}[i]$ | 0 | 0 | 0 | 1 | 2 | 2 | 2 | 3 | 4 |

Line L8 gives $s = 1$ and $t = 6$, the only two binary searches. Then:

| step | node | $(s, t)$ on entry | action | slice reported |
|---|---|---|---|---|
| 1 | $[0, 4)$, $A = (2,3), (5,4), (4,7), (3,8)$ | $(0, 2)$ | $lo = 1 < 2$: report from $[2, 4)$, $A = (5,4), (4,7)$, at $(0, 1)$ | $(5,4)$ |
| 2 | $[0, 2)$, $A = (2,3), (3,8)$ | $(0, 1)$ | $lo = 1 \ge 1$: go right | |
| 3 | leaf $1$, $A = (3,8)$ | $(0, 0)$ | empty slice | |
| 4 | $[4, 8)$, $A = (8,1), (7,2), (6,6), (9,6)$ | $(1, 4)$ | $hi = 5 < 6$: go left | |
| 5 | $[4, 6)$, $A = (7,2), (6,6)$ | $(0, 2)$ | $hi = 5 \ge 5$: report from $[4, 5)$, $A = (6,6)$, at $(0, 1)$ | $(6,6)$ |
| 6 | leaf $5$, $A = (7,2)$ | $(0, 1)$ | | $(7,2)$ |

The query reports $(5,4), (6,6), (7,2)$, as the [range tree query](/range-tree-query/) does on the same input, but with $2$ binary searches by $y$ instead of $4$.

## Correctness

**Cascading step.** Let $s$ be the first index of $A(v)$ whose $y$-value is at least $y_1$. A point of the left child with $p_y \ge y_1$ appears in $A(v)$ at an index at least $s$, so its key is at least that of $A(v)[s]$; conversely, a key at least that of $A(v)[s]$ has $p_y \ge y_1$. So $\mathrm{left}(v)[s]$, the index of the first left-child entry with key at least $A(v)[s]$, is the first index of $A(\mathrm{lc}(v))$ with $p_y \ge y_1$. The same holds for the right child with $s - \mathrm{left}(v)[s]$, for $t$ and $p_y > y_2$, and for $s = |A(v)|$. By induction down the paths, at every node $v$ reached, $A(v)[s .. t - 1]$ is exactly the part of $A(v)$ with $y_1 \le p_y \le y_2$.

**Query.** The nodes whose slices are reported are the canonical subtrees and the two end leaves of the [range tree query](/range-tree-query/), which partition the positions from $lo$ to $hi$; its argument carries over with the binary search at each canonical node replaced by the cascading step. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

| operation or measure | cost | case |
|---|---|---|
| space, $d = 2$ | at most $n(\lceil \log_2 n \rceil + 1)$ array entries and $n \lceil \log_2 n \rceil + n - 1$ counts, $O(n \log n)$ | worst case |
| BUILD, $d = 2$ | $O(n \log n)$ | worst case |
| REPORT, $d = 2$ | $O(\log n + k)$ | worst case |
| COUNT, $d = 2$ | $O(\log n)$ | worst case |
| space and BUILD, $d \ge 2$ | $O(n \log^{d-1} n)$ | worst case |
| REPORT, $d \ge 2$ | $O(\log^{d-1} n + k)$ | worst case |

The query takes $O(\log n)$ for the two binary searches at line L8, $O(1)$ per node on the two paths, which have at most $\lceil \log_2 n \rceil$ nodes each, and $O(1)$ per reported point. In $d$ dimensions the first $d - 2$ levels are an ordinary range tree, which reaches $O(\log^{d-2} n)$ layered trees, each queried in $O(\log n)$ plus output.

## Variants

- **General fractional cascading.** When the lists along a path are not subsets of each other, Chazelle and Guibas sample every second element of each child list into its parent and keep bridges; see [fractional cascading](/multiple-list-search/) and [bridges](/fractional-cascading-bridge/).
- **Rank space and bit vectors.** In rank space the counts $\mathrm{left}(v)$ are the prefix ranks of one bit per entry. Storing the bits in a rank structure instead of the counts gives the [wavelet tree](/wavelet-tree/), with $O(n \log n)$ bits instead of words and $O(\log n)$ counting.
- **Higher space, faster.** Chazelle's filtering search and Alstrup, Brodal and Rauhe reach $O(\log n + k)$ or better with $O(n \log^{\varepsilon} n)$ words on the word RAM; see [orthogonal range reporting](/orthogonal-range-reporting/).
- **Dynamic layered range trees.** Mehlhorn and Näher's dynamic fractional cascading gives $O(\log n \log \log n + k)$ query and $O(\log n \log \log n)$ amortized update time in the plane.

## When to use it

Use a layered range tree for static planar box queries when the query time must be $O(\log n + k)$ in the worst case and $O(n \log n)$ words are affordable. For counting only, a [merge sort tree](/merge-sort-tree/) or a [wavelet tree](/wavelet-tree/) with the same cascade is simpler. If the queries are known in advance, the [offline sweep](/offline-orthogonal-range-counting/) uses linear space.

## Pitfalls

- **Ties in $y$ without a total key.** If the arrays are sorted by $p_y$ alone and the merge breaks ties inconsistently, the count $\mathrm{left}(v)[s]$ can point past a child entry with $p_y = y_1$. Use the total key $(p_y, p_x, j)$ in every array, as line L4 does.
- **Forgetting the sentinel index.** The cascading array has $|A(v)| + 1$ entries. A query whose $t$ equals $|A(v)|$ (every $y$-value $\le y_2$) reads $\mathrm{left}(v)[|A(v)|]$.
- **Updating $(s, t)$ before reading the counts.** Line L12 needs $\mathrm{left}(v)[s]$ for both the reported slice and the next pair. Reading them after $s$ has been overwritten gives wrong slices.
- **Searching again at each canonical node.** A layered tree whose query still bisects $A(\mathrm{rc}(v))$ is just a range tree with extra memory; the binary searches happen only at line L8.

## Implementations

## History

Willard, in work begun in 1978 and published in 1985, and Lueker (1978) observed that the associated arrays of a two-dimensional range tree are searched for the same values, and linked them by pointers to save a logarithmic factor. Chazelle and Guibas (1986) turned the idea into the general technique of fractional cascading, which also applies when the lists are not nested. The name *layered range tree* and the presentation through a single binary search at the split node are those of de Berg et al., Section 5.6.

## References
