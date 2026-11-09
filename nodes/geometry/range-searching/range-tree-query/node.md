---
tag: ZMJ28C
kind: algorithm
slug: range-tree-query
name: Range tree query
aliases:
- range tree orthogonal range search
- 2DRANGEQUERY
- split node range query
area: geometry/range-searching
level: core
summary: Search the outer tree, then query the inner trees at the O(log n) canonical nodes covering the range.
solves: [orthogonal-range-reporting, orthogonal-range-counting]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of reported points, d: the dimension}
  time: {report: O(log^2 n + k) worst case, count: O(log^2 n) worst case, report_d: O(log^d n + k) worst case}
  space: {extra: O(1) worst case}
properties: {online: true, deterministic: true, recursive: false, static: true}
history:
  year: 1979
  people: [Jon Louis Bentley, George S. Lueker, Dan E. Willard]
  note: The query walks the two search paths of the x-range and searches the associated structures of the subtrees between them; this is the query of the range trees of 1978 to 1980.
prereqs: [range-tree, bst-range-search]
see_also: [layered-range-tree, kd-tree-range-search, segment-tree, orthogonal-range-reporting, orthogonal-range-counting, merge-sort-tree, decomposable-searching-problem, range-searching-lower-bound]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.1 (FINDSPLITNODE, 1DRANGEQUERY, Lemma 5.1) and Section 5.3 (2DRANGEQUERY, Lemma 5.7, Theorem 5.8)
  - paper: doi:10.1145/358841.358850
    title: Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4), 1980, pages 214 to 229
    locator: the range tree query and its O(log^d n + k) analysis
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.1 (canonical subsets and multi-level structures) and Section 40.2
---

The range tree query answers a two-dimensional box query $[x_1, x_2] \times [y_1, y_2]$ on a [range tree](/range-tree/). It finds the *split node* where the search paths for $x_1$ and $x_2$ separate, walks down both paths, and for every subtree that hangs between the two paths searches the associated array of that subtree by $y$. The subtrees are the $O(\log n)$ canonical subsets of the $x$-range, so the query reports the $k$ points in $O(\log^2 n + k)$ time and counts them in $O(\log^2 n)$ time in the worst case. This is 2DRANGEQUERY of de Berg et al., Section 5.3.

## In plain words

The points are kept in a tree sorted from left to right, and every branch also keeps its points sorted from bottom to top. To answer a question about a rectangle, first find the branches whose points have the right left-to-right position. Search for the left edge and the right edge of the rectangle at the same time; the two searches follow the same path for a while, then part.

After they part, the search for the left edge goes down on the left side. Each time it turns left, the whole branch to its right lies between the two edges, so all its points have the right left-to-right position. That branch is then searched by height in its own sorted list. The search for the right edge does the same on the other side. Few branches are collected this way, one per step of each search.

## The problem

**Notation.** $P$ is the set of $n$ input points in the plane ($d = 2$), $p = (x, y)$ a point, and $k$ the output size. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/), and only coordinates are compared.

**Input.** A two-dimensional range tree on $P$: a balanced leaf-based binary tree $T$ over the points sorted by $x$, in which each node $v$ stores the array $A(v)$ of the points of its subtree sorted by $y$. A closed query box $Q = [x_1, x_2] \times [y_1, y_2]$.

**Output.** The points $p \in P$ with $x_1 \le p_x \le x_2$ and $y_1 \le p_y \le y_2$, each copy once; or their number.

**Degenerate input.** No general position is assumed. The leaves are in the order of $(p_x, p_y, \text{index})$, and the query works with positions in that order: $lo$ is the first position with $p_x \ge x_1$ and $hi$ the last position with $p_x \le x_2$. The two paths of the query lead to the leaves $lo$ and $hi$. This plays the role of de Berg's composite numbers (Section 5.5): ties in $x$ are broken consistently, and points on the boundary of $Q$ are reported.

## The algorithm

```pseudo id=main
2D-RANGE-QUERY(T, [x1, x2] × [y1, y2])
L1  lo ← first position with p_x ≥ x1; hi ← last position with p_x ≤ x2; if lo > hi then return
L2  v_split ← the deepest node whose subtree contains both leaves lo and hi
L3  if v_split is a leaf then report its point if y1 ≤ p_y ≤ y2
L4  else v ← lc(v_split)
L5      while v is not a leaf do
L6          if leaf lo is in the subtree of lc(v) then 1D-QUERY(A(rc(v)), [y1, y2]); v ← lc(v)
L7          else v ← rc(v)
L8      report the point of the leaf v if y1 ≤ p_y ≤ y2
L9      repeat lines L5 to L8 from v ← rc(v_split), with the leaf hi, the roles of lc and rc exchanged
L10     report the point of the last leaf if y1 ≤ p_y ≤ y2
```

1D-QUERY$(A, [y_1, y_2])$ finds the first index of $A$ with $p_y \ge y_1$ and the first with $p_y > y_2$ by binary search, and reports the slice between them; a counting query adds the length of the slice.

- **Line L1** turns the $x$-range into a range of leaves. All leaves from $lo$ to $hi$, and only they, have $x_1 \le p_x \le x_2$.
- **Line L2** is FINDSPLITNODE: start at the root and go to the left child while both leaves are in it, to the right child while both are in it, and stop when they separate or at a leaf.
- **Lines L5 to L7.** On the path from $v_{\mathrm{split}}$ to leaf $lo$, when the path turns left, the right child lies strictly between the two paths: all its leaves are after $lo$ and before $hi$. Its whole subtree is a canonical subset of the $x$-range, and only $y$ remains to be checked.
- **Lines L8 and L10.** The leaves $lo$ and $hi$ themselves are in the $x$-range, so only their $y$ is tested.
- **Line L9** is the mirror image: on the path to $hi$, when the path turns right, the left child is canonical.

## Example

The points are $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ and the query is $Q = [3, 7] \times [2, 6]$. In $x$-order the leaves are $(2,3), (3,8), (4,7), (5,4), (6,6), (7,2), (8,1), (9,6)$ at positions $0$ to $7$. Line L1 gives $lo = 1$ and $hi = 5$. The root covers positions $[0, 8)$ with children $[0, 4)$ and $[4, 8)$, which separate leaves $1$ and $5$, so the root is the split node.

| step | path | node (positions) | test | canonical subtree queried | reported |
|---|---|---|---|---|---|
| 1 | left | $[0, 4)$ | leaf 1 is in the left child $[0, 2)$ | $[2, 4)$, $A = (5,4), (4,7)$ | $(5,4)$ |
| 2 | left | $[0, 2)$ | leaf 1 is in the right child $[1, 2)$ | none | |
| 3 | left | leaf $1$, point $(3,8)$ | $y = 8 > 6$ | | |
| 4 | right | $[4, 8)$ | leaf 5 is in the left child $[4, 6)$ | none | |
| 5 | right | $[4, 6)$ | leaf 5 is in the right child $[5, 6)$ | $[4, 5)$, $A = (6,6)$ | $(6,6)$ |
| 6 | right | leaf $5$, point $(7,2)$ | $2 \le y \le 6$ | | $(7,2)$ |

The query reports $(5,4), (6,6), (7,2)$ with two one-dimensional queries and two leaf tests. The points $(6,6)$ and $(7,2)$ lie on the boundary of $Q$.

## Correctness

**Key invariant.** The subtrees queried at lines L6 and L9, together with the leaves $lo$ and $hi$, partition the leaves from $lo$ to $hi$: every leaf strictly between them lies in exactly one subtree that hangs off the inner side of one of the two paths. Each such subtree is searched by $y$ in its array $A$, which holds exactly its points. So each point with $x_1 \le p_x \le x_2$ is tested against $[y_1, y_2]$ exactly once. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Paths.** The tree has height $\lceil \log_2 n \rceil$, so line L2 and each of the two paths take $O(\log n)$ steps.
- **One-dimensional queries.** At most one per node on the two paths, so at most $2 \lceil \log_2 n \rceil$. Each costs $O(\log n)$ for the binary searches plus $O(1)$ per reported point.
- **Total.** Reporting takes $O(\log^2 n + k)$ time and counting $O(\log^2 n)$ time, in the worst case, with $O(1)$ extra space besides the output.
- **Higher dimensions.** The same walk at the first level, with a $(d-1)$-dimensional query on each canonical node, gives $O(\log^{d} n + k)$; see [range tree](/range-tree/).
- **One logarithmic factor less.** The $y$-searches in the $O(\log n)$ canonical arrays all search for the same values $y_1$ and $y_2$. With pointers from each array to its children's arrays, one search at the split node suffices, and the query takes $O(\log n + k)$; see [layered range tree](/layered-range-tree/).

## Properties

- **Canonical decomposition.** The query decomposes the $x$-range into $O(\log n)$ disjoint canonical subsets, which is the general pattern of multi-level structures in range searching.
- **Works for any decomposable question.** Counting, reporting, emptiness and semigroup sums all follow from the same decomposition, because each is a [decomposable searching problem](/decomposable-searching-problem/).
- **Read only.** The query does not change the structure.
- **Output order.** Points come out grouped by canonical subtree, each group in $y$-order.

## Variants and improvements

- **Recursive canonical decomposition.** The [range tree](/range-tree/) page finds the same canonical nodes top-down, as in a [segment tree](/segment-tree/) query, which is shorter to code; both find the maximal subtrees inside the leaf range.
- **Fractional cascading.** The [layered range tree](/layered-range-tree/) replaces the $O(\log n)$ binary searches by pointer steps; see also [fractional cascading](/multiple-list-search/).
- **Merge sort tree.** In rank space, the same structure is called a [merge sort tree](/merge-sort-tree/), and the query counts the elements of a value range in an index range.
- **Semigroup sums.** Store prefix sums (for a group) or a balanced tree of partial sums (for a semigroup) on each array $A(v)$.

## When to use it

Use this query on a static two-dimensional point set when the worst case query time must be polylogarithmic and $O(n \log n)$ space is affordable. If the set changes, use a dynamic range tree or a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) on a fixed grid; if memory is tight, use a [kd-tree](/kd-tree-range-search/).

## Pitfalls

- **Querying the wrong child on a path.** On the path to $lo$, the canonical subtree is the right child when the path goes left. Writing `if leaf lo is in lc(v) then 1D-QUERY(A(lc(v)))` searches the subtree that contains $lo$ itself and points left of $x_1$. Line L6 queries $A(\mathrm{rc}(v))$.
- **Forgetting the two end leaves.** The leaves $lo$ and $hi$ are in no canonical subtree. Dropping lines L8 and L10 loses up to two points, often exactly the points on the vertical sides of $Q$.
- **Computing the leaf range with strict tests.** Taking $hi$ as the last position with $p_x < x_2$ drops the points with $p_x = x_2$. Line L1 uses $\ge x_1$ and $\le x_2$.
- **Searching both paths below a leaf split node.** When $lo = hi$, the split node is a leaf; line L3 handles it, and walking two paths from it would report its point twice.

## Implementations

## History

The query was part of the range tree from its discovery at the end of the 1970s by Bentley, Lueker, Lee and Wong, and Willard. Bentley's 1980 paper on multidimensional divide and conquer gave the $O(\log^{d} n + k)$ analysis. The presentation with FINDSPLITNODE and the two paths, used on this page, is that of de Berg et al., Sections 5.1 and 5.3. Willard and Lueker, and Chazelle and Guibas with fractional cascading, later removed one logarithmic factor.

## References
