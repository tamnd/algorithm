---
tag: XJ7XNM
kind: algorithm
slug: kd-tree-range-search
name: kd-tree range search
aliases:
- k-d tree orthogonal range query
- kd-tree range query
- SEARCHKDTREE
area: geometry/range-searching
level: core
summary: Descend the kd-tree and visit only the cells that intersect the query box; O(sqrt(n) + k) in the plane.
solves: [orthogonal-range-reporting, orthogonal-range-searching]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of reported points, d: the dimension}
  time: {build: O(n log n) worst case, query: O(n^(1/2) + k) worst case, query_d: O(n^(1-1/d) + k) worst case}
  space: {extra: O(n) worst case}
properties: {online: true, deterministic: true, recursive: true, static: true}
history:
  year: 1975
  people: [Jon Louis Bentley, D. T. Lee, C. K. Wong]
  note: Bentley introduced the kd-tree and its region search in 1975; Lee and Wong proved the O(n^(1-1/d) + k) worst case bound in 1977.
prereqs: [kd-tree, orthogonal-range-reporting]
see_also: [kd-tree-range-query-complexity, range-tree-query, bst-range-search, kd-tree-nearest-neighbor-search, quadtree, range-tree, orthogonal-range-counting, range-emptiness-query]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.2, Kd-Trees (algorithms BUILDKDTREE and SEARCHKDTREE, Lemma 5.4 and Theorem 5.5); Section 5.5 for composite numbers
  - paper: doi:10.1145/361002.361007
    title: Jon Louis Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 1975, pages 509 to 517
    locator: the kd-tree and its region search
  - paper: doi:10.1007/BF00263763
    title: D. T. Lee and C. K. Wong, Worst-case analysis for region and partial region searches in multidimensional binary search trees and balanced quad trees, Acta Informatica 9(1), 1977, pages 23 to 29
    locator: the worst case bound O(d n^(1-1/d) + k)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (kd-trees for orthogonal range searching)
---

kd-tree range search reports the points of a two-dimensional [kd-tree](/kd-tree/) that lie in a closed axis-parallel query box. It walks down the tree and, at each child, compares the child's cell with the box: a cell inside the box is reported whole, a cell that misses the box is skipped, and a cell that crosses the box boundary is searched further. In the plane the query takes $O(\sqrt{n} + k)$ time in the worst case, and in $d$ dimensions $O(n^{1-1/d} + k)$, with a structure of linear size. This page follows SEARCHKDTREE of de Berg et al., Section 5.2.

## In plain words

A kd-tree cuts the set of points in half by a vertical line, then cuts each half in half by a horizontal line, then vertically again, and so on, until each part holds one point. Every part of the tree is a rectangle on the map, and each tree node remembers the smallest rectangle around its points.

To answer a question about a box, start at the top and look at the two halves. If a half lies completely inside the box, all its points are answers, and they are listed without further checks. If a half lies completely outside the box, it is ignored. Only a half that sticks out across the edge of the box needs a closer look. Few rectangles cross the edge of the box, because each cut leaves an edge on one side only, and that keeps the search short.

## The problem

**Notation.** $P$ is the set of $n$ input points in the plane ($d = 2$), $p = (x, y)$ a point, and $k$ the output size, the number of reported points. Each node $v$ of the tree stores $\mathrm{box}(v) = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$, the bounding box of the points in its subtree. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

**Input.** A kd-tree on the multiset $P$ and a closed query box $R = [x_1, x_2] \times [y_1, y_2]$.

**Output.** All points $p \in P$ with $x_1 \le p_x \le x_2$ and $y_1 \le p_y \le y_2$, each copy once.

**The tree.** The tree is leaf based: each leaf holds one point and each internal node has two children. A node at even depth splits its points at the median of the $x$-order, a node at odd depth at the median of the $y$-order, and the left child gets the first $\lceil m/2 \rceil$ of the $m$ points.

**Degenerate input.** No general position is assumed. Repeated coordinates are made distinct by the composite keys of de Berg et al., Section 5.5: the $x$-order compares $(p_x, p_y, \text{index})$ and the $y$-order compares $(p_y, p_x, \text{index})$, both lexicographically. The tree stays balanced even if all points lie on one vertical line or coincide. The boxes are stored in the original coordinates, and all tests are exact comparisons of integers or fractions.

## The algorithm

```pseudo id=main
SEARCH-KD-TREE(v, R)
L1  if v is a leaf then
L2      if the point stored at v lies in R then report it
L3  else for each child c of v do
L4      if box(c) ⊆ R then REPORT-SUBTREE(c)
L5      else if box(c) ∩ R ≠ ∅ then SEARCH-KD-TREE(c, R)
```

REPORT-SUBTREE$(c)$ walks the subtree of $c$ and reports the point of every leaf.

- **Lines L1 and L2.** A leaf is reached by the search only if it is the root, that is $n = 1$; any other leaf has a one-point box, which is either inside $R$ or disjoint from it, so lines L4 and L5 handle it.
- **Line L4.** If the bounding box of $c$ lies inside $R$, every point below $c$ is an answer. The test is four comparisons: $x_1 \le x_{\min}$, $x_{\max} \le x_2$, $y_1 \le y_{\min}$ and $y_{\max} \le y_2$.
- **Line L5.** The two boxes intersect if and only if their $x$-intervals and their $y$-intervals intersect: $x_{\min} \le x_2$, $x_1 \le x_{\max}$, $y_{\min} \le y_2$ and $y_1 \le y_{\max}$. Otherwise no point below $c$ is in $R$, and $c$ is skipped.

de Berg et al. use the region of a node, the rectangle cut out by the splitting lines above it, instead of the bounding box. The bounding box lies inside the region, so it is inside $R$ whenever the region is, and it misses $R$ whenever the region does. So the bounding-box version searches a subset of the nodes that de Berg's version searches, and the same bound holds. The code runs the search with an explicit stack.

## Example

The points are $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ and the query box is $R = [3, 7] \times [2, 6]$. The root splits by $x$ into $\{(2,3), (3,8), (4,7), (5,4)\}$ and $\{(6,6), (7,2), (8,1), (9,6)\}$; the next level splits each half by $y$.

| step | node searched | child | box of child | test | action |
|---|---|---|---|---|---|
| 1 | root, box $[2,9] \times [1,8]$ | left | $[2,5] \times [3,8]$ | crosses $R$ | search it |
| | | right | $[6,9] \times [1,6]$ | crosses $R$ | search it |
| 2 | left | lower | $[2,5] \times [3,4]$, points $(2,3), (5,4)$ | crosses $R$ | search it |
| | | upper | $[3,4] \times [7,8]$, points $(4,7), (3,8)$ | $y_{\min} = 7 > 6$ | skip |
| 3 | left, lower | leaf $(2,3)$ | $[2,2] \times [3,3]$ | $x_{\max} = 2 < 3$ | skip |
| | | leaf $(5,4)$ | $[5,5] \times [4,4]$ | inside $R$ | report $(5,4)$ |
| 4 | right | lower | $[7,8] \times [1,2]$, points $(7,2), (8,1)$ | crosses $R$ | search it |
| | | upper | $[6,9] \times [6,6]$, points $(6,6), (9,6)$ | crosses $R$ | search it |
| 5 | right, lower | leaf $(7,2)$ | $[7,7] \times [2,2]$ | inside $R$, on two sides | report $(7,2)$ |
| | | leaf $(8,1)$ | $[8,8] \times [1,1]$ | outside | skip |
| 6 | right, upper | leaf $(6,6)$ | $[6,6] \times [6,6]$ | inside $R$, on the top side | report $(6,6)$ |
| | | leaf $(9,6)$ | $[9,9] \times [6,6]$ | outside | skip |

The search enters $6$ nodes and reports $(5,4), (7,2), (6,6)$. The points $(7,2)$ and $(6,6)$ lie on the boundary of $R$ and are reported because $R$ is closed.

## Correctness

**Invariant.** When SEARCH-KD-TREE$(v, R)$ is called, every point of $R$ below $v$ will be reported during this call, and no point outside $R$ will be. Line L4 reports a whole subtree only when its bounding box lies in $R$; line L5 skips a subtree only when its bounding box misses $R$; every other child is searched. Each leaf is reached by exactly one path, so each copy is reported once. The proof, with the bound on the number of searched nodes, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build.** Sorting by both composite orders takes $O(n \log n)$. Each level of the tree splits the sorted lists in $O(n)$ time, keeping both orders, and the tree has $\lceil \log_2 n \rceil$ levels, so the build takes $O(n \log n)$ time in the worst case, and the tree has $2n - 1$ nodes, which is $O(n)$ space.
- **Reported subtrees.** A subtree with $j$ leaves has $2j - 1$ nodes, so line L4 costs $O(k)$ in total.
- **Searched nodes.** A searched node other than the root has a box that meets $R$ without lying inside it, so its box, and hence its region, meets one of the four lines that carry the sides of $R$. A vertical line meets the regions of at most $Q(n)$ nodes, where $Q(n) = 2 + 2Q(n/4)$, because among the four grandchildren of a node that splits by $x$, the line meets at most two; so $Q(n) = O(\sqrt{n})$. The same holds for horizontal lines. Hence $O(\sqrt{n})$ nodes are searched, and the query takes $O(\sqrt{n} + k)$ time in the worst case. In $d$ dimensions the same argument gives $O(n^{1-1/d} + k)$; see [the kd-tree range query theorem](/kd-tree-range-query-complexity/).
- **Tightness.** A thin box that contains no point can cross $\Theta(\sqrt{n})$ cells, for example on a $\sqrt{n} \times \sqrt{n}$ grid with the box between two columns, so the bound is tight for this structure.

## Properties

- **Linear space.** The tree has $2n - 1$ nodes, against $O(n \log n)$ for a [range tree](/range-tree/).
- **Static.** Insertions and deletions break the balance; dynamic versions rebuild subtrees.
- **Flexible ranges.** The same descent works for any range shape with a test "cell inside range" and "cell meets range", for example disks, at the cost of the worst case guarantee.
- **Output order.** Points come out in tree order, not sorted.

## Variants and improvements

- **Counting.** Store the number of points in each node; line L4 then adds the count of $c$ instead of reporting, and a counting query takes $O(\sqrt{n})$ time.
- **Point-based kd-tree.** Bentley's original stores a point in every node; the [kd-tree](/kd-tree/) page uses that form, and the search tests the node's own point before its children.
- **Higher dimensions.** Cycle through $d$ axes; the query bound becomes $O(n^{1-1/d} + k)$, which is close to linear for large $d$.
- **Nearest neighbors.** The same tree answers [nearest neighbor](/kd-tree-nearest-neighbor-search/) queries by a best-first descent.
- **Range trees.** For $O(\log^2 n + k)$ query time at the cost of $O(n \log n)$ space, use the [range tree query](/range-tree-query/).

## When to use it

Use a kd-tree when memory is tight, when the points are many and the dimension is small, or when the same tree also serves nearest neighbor queries. In practice, queries on real data visit far fewer than $\sqrt{n}$ cells. When the worst case query time matters more than space, use a [range tree](/range-tree/) or a [layered range tree](/layered-range-tree/).

## Pitfalls

- **Strict comparisons in the intersection test.** Writing line L5 as `x_min < x2 and x1 < x_max and ...` skips a child whose box touches $R$ only along a side, and loses the points on the boundary of $R$. The right test uses $\le$: `x_min ≤ x2 and x1 ≤ x_max and y_min ≤ y2 and y1 ≤ y_max`.
- **Splitting by one coordinate when values repeat.** Splitting with "left = points with $p_x \le$ median" puts every copy of the median on one side. If all points have the same $x$, the left side gets all of them, the tree never splits, and the build does not terminate or the height becomes $n$. Split by position in the composite order $(p_x, p_y, \text{index})$, as the build does.
- **Pruning with the split value alone.** A version that stores only the split value $s$ and writes `if s < x2 then search the right child` loses points: the positional split can put copies of $s$ in the right child, and those points have $p_x = s = x_2$. Test the stored bounding box, as line L5 does, or write `if s ≤ x2`.
- **Recursion depth.** The tree depth is $\lceil \log_2 n \rceil$, so recursion is safe for balanced trees, but a tree built without composite keys can have depth $n$. The code uses an explicit stack.

## Implementations

## History

Jon Bentley introduced the multidimensional binary search tree, or kd-tree, in 1975 in the Communications of the ACM, together with the region search. D. T. Lee and C. K. Wong proved in 1977 that a region search in a balanced kd-tree on $n$ points in $d$ dimensions takes $O(d \, n^{1-1/d} + k)$ time in the worst case, and that this is tight. The presentation with bounding regions, the subtree report and the recurrence $Q(n) = 2 + 2Q(n/4)$ is the one of de Berg et al., Chapter 5.

## References
