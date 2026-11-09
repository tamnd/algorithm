---
tag: ZHWQH0
kind: algorithm
slug: priority-search-tree-query
name: Priority search tree query
aliases:
- three-sided range reporting query
- QueryPrioSearchTree
- ReportInSubtree
area: geometry/range-searching
level: core
summary: Walk the priority search tree, pruning subtrees whose heap key exceeds the query bound.
solves: [three-sided-range-query]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of reported points}
  time: {query: O(log n + k) worst case}
  space: {extra: O(log n) worst case}
properties: {online: true, deterministic: true, recursive: false, static: true}
history:
  year: 1985
  people: [Edward M. McCreight]
  note: The query walks the two search paths and reports each subtree between them by heap order; McCreight proved the O(log n + k) bound.
prereqs: [priority-search-tree, three-sided-range-query]
see_also: [priority-search-tree, three-sided-range-query, range-tree-query, cartesian-tree, range-minimum-query, binary-heap, dominance-counting, orthogonal-range-reporting]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, Section 10.2, Priority Search Trees (REPORTINSUBTREE, QUERYPRIOSEARCHTREE and the O(log n + k) analysis)
  - paper: doi:10.1137/0214021
    title: Edward M. McCreight, Priority search trees, SIAM Journal on Computing 14(2), 1985, pages 257 to 276
    locator: the enumeration of the points in a three-sided range (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, three-sided queries
---

The priority search tree query reports the points of a [priority search tree](/priority-search-tree/) inside a three-sided range $[x_1, x_2] \times (-\infty, y_0]$. It follows the two search paths for the ends of $[x_1, x_2]$, tests the point stored at every node on them, and reports each subtree that hangs between the paths by a heap walk that stops at the first stored point above $y_0$. The paths cost $O(\log n)$, and the heap walks cost $O(1)$ per reported point plus $O(1)$ per subtree, so the query takes $O(\log n + k)$ time in the worst case. This is QUERYPRIOSEARCHTREE of de Berg et al., Section 10.2, with the coordinates swapped.

## In plain words

The tree sorts the points from left to right by branches, and every branch keeps its lowest remaining point at the top. To find the points between two vertical lines and below a height, first follow the searches for the two vertical lines from the top. The points held on these two routes may or may not be in range, so each is checked.

Every branch that hangs between the two routes lies entirely between the vertical lines. In such a branch only the height matters. Its top point is its lowest; if that is too high, the branch has nothing to give. Otherwise report it and look at the two branches below, in the same way. Every branch looked at either gives a point or is next to one that did.

## The problem

**Notation.** $P$ is the set of $n$ points in the plane ($d = 2$), $p = (p_x, p_y)$ a point, $k$ the output size, and $H = \lceil \log_2 n \rceil$ the height of the tree. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/), and only coordinates are compared.

**Input.** A priority search tree on $P$: a balanced binary tree over the positions $0, \dots, n - 1$ of the order of $(p_x, p_y, \text{index})$, in which node $v$ covers a block of positions and stores $\mathrm{pt}(v)$, the point of its block with the smallest key $(p_y, p_x, j)$ that is not stored higher up, or nothing. A closed three-sided range $[x_1, x_2] \times (-\infty, y_0]$.

**Output.** The points of $P$ with $x_1 \le p_x \le x_2$ and $p_y \le y_0$, each copy once.

**Degenerate input.** No general position is assumed. Coincident points are separate positions; the keys break ties in $y$. Points on the boundary are reported.

## The algorithm

```pseudo id=main
PST-QUERY(T, x1, x2, y0)
L1  lo ← first position with p_x ≥ x1; hi ← last position with p_x ≤ x2; if lo > hi then return
L2  for each node v on the search paths from the root to the leaves of lo and of hi (the shared part once), stopping a path at an empty node, do
L3      if lo ≤ pt(v) ≤ hi and pt(v)_y ≤ y0 then report pt(v)
L4      if v is below the split node on the path to lo, and the path goes on to lc(v), then REPORT-IN-SUBTREE(rc(v), y0)
L5      if v is below the split node on the path to hi, and the path goes on to rc(v), then REPORT-IN-SUBTREE(lc(v), y0)
```

```pseudo id=report
REPORT-IN-SUBTREE(u, y0)
L6  S ← a stack holding u
L7  while S is not empty do pop u from S
L8      if u is empty or pt(u)_y > y0 then continue
L9      report pt(u); push lc(u) and rc(u) onto S
```

- **Line L1** turns the $x$-range into the positions $lo$ to $hi$.
- **Line L2.** The paths are the same as in a [range tree query](/range-tree-query/): they share a prefix down to the split node, then go apart. A path stops at an empty node because everything under it is empty.
- **Line L3.** A node on a path stores a point that may be anywhere in its block, inside or outside the $x$-range, so both tests are needed.
- **Lines L4 and L5** pick the subtrees strictly between the two paths: their blocks lie inside $[lo, hi]$, so only $y$ matters there.
- **Lines L8 and L9.** By the heap order every point under $u$ is at least as high as $\mathrm{pt}(u)$, so a point above $y_0$ ends the walk in that subtree.

## Example

The tree on the points $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$ is the one built on the [priority search tree](/priority-search-tree/) page: in $x$-order the positions $0$ to $7$ hold $(2,3), (3,8), (4,7), (5,4), (6,6), (7,2), (8,1), (9,6)$, and the nodes store 1: $(8,1)$, 2: $(2,3)$, 3: $(7,2)$, 4: $(3,8)$, 5: $(5,4)$, 6: $(6,6)$, 7: $(9,6)$, 10: $(4,7)$. The query is $[3, 7] \times (-\infty, 6]$, so $lo = 1$ and $hi = 5$, and the root $[0, 8)$ is the split node.

| step | node (block) | stored point | action | reported |
|---|---|---|---|---|
| 1 | 1 $[0, 8)$, split | $(8,1)$, position 6 | outside $[1, 5]$ | |
| 2 | 2 $[0, 4)$, path to lo | $(2,3)$, position 0 | outside; path goes left, so REPORT-IN-SUBTREE(5) | |
| 3 | 5 $[2, 4)$, subtree | $(5,4)$ | $4 \le 6$: report, push 10 and 11 | $(5,4)$ |
| 4 | 10 $[2, 3)$ and 11 $[3, 4)$ | $(4,7)$ and none | $7 > 6$; empty | |
| 5 | 4 $[0, 2)$, path to lo | $(3,8)$, position 1 | in $[1, 5]$ but $8 > 6$; path goes right to the empty node 9 and stops | |
| 6 | 3 $[4, 8)$, path to hi | $(7,2)$, position 5 | in range | $(7,2)$ |
| 7 | 6 $[4, 6)$, path to hi | $(6,6)$, position 4 | in range; path goes right, so REPORT-IN-SUBTREE(12), which is empty | $(6,6)$ |

The answer is $(5,4), (7,2), (6,6)$. The paths visit $5$ nonempty nodes, and the two heap walks pop $4$ nodes, $3$ for the subtree of node 5 and $1$ for the empty node 12.

## Correctness

**Key invariant.** Every point is stored at exactly one node. If that node is on a search path, line L3 tests it against both conditions. If it is in a subtree hanging between the paths, its position is in $[lo, hi]$, and REPORT-IN-SUBTREE reaches it exactly when its $y$ is at most $y_0$, because every ancestor in the subtree stores a point at least as low. Any other node lies in a subtree hanging outside the paths, whose positions are all outside $[lo, hi]$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Paths.** Line L2 visits at most $2H + 1$ nodes, with $O(1)$ work each besides the subtree walks; lines L4 and L5 start at most $2H$ walks.
- **Heap walks.** A node popped in REPORT-IN-SUBTREE is either reported or skipped at line L8. A skipped node is the start of its walk or a child of a reported node, so the pops number at most $2H + 2k$.
- **Total.** $O(\log n + k)$ time in the worst case, with the two binary searches of line L1. The stack holds at most $O(H)$ nodes at a time if the child to be visited second is pushed first; the extra space is $O(\log n)$.

## Properties

- **Output sensitive.** The cost beyond $O(\log n)$ is proportional to the output, the same bound as for one-dimensional reporting.
- **Order of output.** Points of one subtree come out in heap order of their keys along each root path, not sorted by $x$ or by $y$.
- **Read only.** The query does not change the tree.

## Variants and improvements

- **Single traversal.** The same answer comes from one depth-first walk that skips a node if its block misses $[lo, hi]$ or its point is above $y_0$; the [priority search tree](/priority-search-tree/) page uses this form, with the same $O(\log n + k)$ bound.
- **Lowest point in an $x$-range.** Dropping $y_0$ and keeping the best point found, without descending into subtrees between the paths, finds the lowest point of $[x_1, x_2]$ in $O(\log n)$.
- **Cartesian tree and range minima.** On a static set, finding the minimum $y$ in $[lo, hi]$ with a [range minimum query](/range-minimum-query/) structure and recursing on both sides reports the answer in $O(1)$ per point after the binary searches; see [Cartesian tree](/cartesian-tree/).
- **Dominance reporting.** With $x_1 = -\infty$ the query is a two-sided dominance query, so the paths reduce to one; see [dominance counting](/dominance-counting/).

## When to use it

Use this query whenever a priority search tree is in place: for three-sided or two-sided reporting, for interval stabbing (intervals as points), and as the inner query of structures for four-sided ranges built on a [range tree](/range-tree/) with priority search trees at its nodes.

## Pitfalls

- **Skipping the points on the paths.** The points stored on the two search paths do not belong to any canonical subtree. Leaving out line L3 misses them; in the example it would lose $(7,2)$ and $(6,6)$.
- **Reporting a path point by $y$ alone.** A path node's point can lie outside $[x_1, x_2]$: node 1 in the example stores $(8,1)$, which is low but to the right of the range. Line L3 tests the position too.
- **Stopping a path at a point outside the $x$-range.** The point stored at a path node can be outside $[x_1, x_2]$ while points below it are inside: node 2 in the example stores $(2,3)$, and node 5 below it holds $(5,4)$. The path must go on; only an empty node ends it.
- **Recursion depth.** A recursive REPORT-IN-SUBTREE on a tree of height $H$ is fine, but on an unbalanced dynamic tree it can overflow the stack; lines L6 to L9 use an explicit stack.

## Implementations

## History

McCreight introduced the priority search tree and its three-sided query in a 1980 report and the 1985 SIAM Journal on Computing paper, with the $O(\log n + k)$ analysis. The split-node presentation with QUERYPRIOSEARCHTREE and REPORTINSUBTREE is that of de Berg et al., Section 10.2, who use a heap on $x$ and queries $(-\infty, q_x] \times [q_y, q_y']$; this page swaps the coordinates.

## References
