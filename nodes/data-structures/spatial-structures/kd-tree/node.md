---
tag: 39PCSM
kind: data-structure
slug: kd-tree
name: k-d tree
aliases:
- 2d-tree
- k-dimensional tree
- kd-tree
area: data-structures/spatial-structures
level: core
summary: Binary tree that splits k-dimensional points by cycling through the coordinate axes at each level.
implements: [spatial-index]
model: real-ram
complexity:
  vars: {n: the number of points, k: the dimension, h: the height of the tree, r: the number of reported points}
  time: {build: O(n log n), insert: O(h), search: O(h), delete: O(n^(1-1/k)), range_search: O(n^(1-1/k) + r), nearest: O(n)}
  space: {total: Θ(n)}
history:
  year: 1975
  people: [Jon Louis Bentley]
  note: Bentley introduced the multidimensional binary search tree, with insertion, deletion, exact and region search, in Communications of the ACM in 1975.
prereqs: [binary-search-tree, median-finding, orthogonal-range-searching]
see_also: [kd-tree-range-query-complexity, kd-tree-range-search, kd-tree-nearest-neighbor-search, range-tree, quadtree, kd-b-tree, bsp-tree, nearest-neighbor-search]
sources:
  - paper: doi:10.1145/361002.361007
    title: Jon Louis Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 1975
    locator: pages 509 to 517 (the definition with discriminators that cycle through the keys, superkeys, insertion, deletion with the search for a minimum, and the optimized tree built by medians)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Orthogonal Range Searching, Section 5.2 Kd-Trees (construction by medians in O(n log n) time, linear storage, and the O(√n + k) query bound in the plane)
  - paper: doi:10.1007/BF00263763
    title: D. T. Lee and C. K. Wong, Worst-case analysis for region and partial region searches in multidimensional binary search trees and balanced quad trees, Acta Informatica 9(1), 1977
    locator: pages 23 to 29 (the O(k n^(1-1/k)) bound for region queries)
  - paper: doi:10.1145/355744.355745
    title: Jerome H. Friedman, Jon Louis Bentley and Raphael Ari Finkel, An algorithm for finding best matches in logarithmic expected time, ACM Transactions on Mathematical Software 3(3), 1977
    locator: the branch-and-bound nearest neighbor search and its expected cost
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 1, Multidimensional Point Data, the section on k-d trees (insertion, deletion, search and the variants)
---

A k-d tree is a [binary search tree](/binary-search-tree/) for points in $k$ dimensions in which the nodes at depth $t$ compare points by coordinate $t \bmod k$: the root splits by the first coordinate, its children by the second, and so on, round and round. Each node holds one point and its splitting hyperplane. Built with [medians](/median-finding/), the tree has height $\lfloor \lg n \rfloor + 1$, takes $O(n \log n)$ time to build, and answers an [orthogonal range query](/orthogonal-range-searching/) in $O(n^{1 - 1/k} + r)$ time, which is $O(\sqrt n + r)$ in the plane. It also supports insertion, deletion and [nearest neighbor search](/nearest-neighbor-search/). Bentley introduced it in 1975, and it is still the most used point index in memory.

## In plain words

A binary search tree sorts numbers: smaller ones go left, others go right. Points on a map have two numbers, east and north.

A k-d tree takes turns. The top point cuts the map with a vertical line: points to the west go left, points to the east go right. One level down, each point cuts its half with a horizontal line: south goes left, north goes right. The next level uses vertical lines again. So each node owns a rectangle of the map, and its children own the two halves.

To find all points in a box, you only go into a child whose half can touch the box. To find the point nearest to a spot, you look first on the side of the spot, and look at the other side only if the line is closer than the best point found so far.

## The abstract type

A k-d tree implements a [spatial index](/spatial-index/) for points: `build(P)`, `insert(T, p)`, `delete(T, p)`, `contains(T, p)`, `range_search(T, ℓ, h)` that reports each point $p$ with $\ell_i \le p_i \le h_i$ on each axis $i$, and `nearest(T, q)`, which returns a point at the least Euclidean distance from $q$. For $k = 1$ it is a plain binary search tree.

## Representation

Each node $t$ holds a point $t.point \in \mathbb{R}^k$, an axis $t.axis \in \{0, \ldots, k-1\}$, and two children $t.left$ and $t.right$. The axis of a node at depth $t$ is $t \bmod k$.

To compare two points on axis $a$, the tree uses the *superkey* order $<_a$: compare $(p_a, p_{a+1}, \ldots, p_{k-1}, p_0, \ldots, p_{a-1})$ lexicographically. Two points are equal in this order only if they are the same point. So points with the same coordinate on axis $a$ still have an order, and the median split stays balanced.

**Invariant (K).** At each node $t$ with axis $a$, each point $p$ in the left subtree has $p <_a t.point$, and each point $p$ in the right subtree has $p \ge_a t.point$.

Since $p <_a q$ implies $p_a \le q_a$, the points of the left subtree have $p_a \le t.point_a$ and those of the right subtree have $p_a \ge t.point_a$. So each node owns a closed box, its *region*: the root owns $\mathbb{R}^k$, and the hyperplane $x_a = t.point_a$ cuts the region of $t$ into the regions of its two children.

## Operations

BUILD splits by the median, and RANGE-SEARCH goes into each child whose side of the hyperplane can meet the query box.

```pseudo id=main
BUILD(P, depth)                            ▷ a tree on the multiset P of points
L1  if P = ∅ then return nil
L2  a ← depth mod k
L3  m ← the point of rank ⌊|P|/2⌋ of P in the order <a      ▷ linear-time selection
L4  t ← a new node with point m and axis a
L5  t.left ← BUILD({p ∈ P : p <a m}, depth + 1)
L6  t.right ← BUILD(P without one copy of m and without the points <a m, depth + 1)
L7  return t

RANGE-SEARCH(t, ℓ, h)                      ▷ report each p with ℓi ≤ pi ≤ hi for all i
L8  if t = nil then return
L9  if ℓi ≤ t.point_i ≤ hi for each axis i then report t.point
L10 a ← t.axis
L11 if ℓa ≤ t.point_a then RANGE-SEARCH(t.left, ℓ, h)
L12 if ha ≥ t.point_a then RANGE-SEARCH(t.right, ℓ, h)
```

Line L3 takes the median by a [selection](/selection-problem/) algorithm, such as [median of medians](/median-of-medians/) in linear worst-case time or [quickselect](/quickselect/) in linear expected time. Lines L5 and L6 send the smaller points left and the others right, as (K) requires. For $n$ distinct points the left part has $\lfloor |P|/2 \rfloor$ points and the right part $\lceil |P|/2 \rceil - 1$, so every subtree at depth $t$ has at most $n / 2^t$ points, and the tree has height $\lfloor \lg n \rfloor + 1$ (counted in nodes).

RANGE-SEARCH tests the point of each node it visits. A point of the query box in the left subtree has $\ell_a \le p_a \le t.point_a$, so line L11 goes left whenever the left subtree can hold an answer; line L12 is the mirror image. Each call costs $O(k)$ time.

**Insertion** follows the search path and adds a leaf.

```pseudo id=insert
INSERT(T, p)
L13 if T.root = nil then T.root ← a new node with point p and axis 0; return
L14 t ← T.root; repeat with a ← t.axis:
L15     if p <a t.point then (if t.left = nil then t.left ← a new node (p, (a+1) mod k), stop; else t ← t.left)
L16     else (if t.right = nil then t.right ← a new node (p, (a+1) mod k), stop; else t ← t.right)
```

It takes $O(h)$ time. Insertion does not rebalance, so $n$ insertions in a bad order give a path of height $n$; inserted in random order, the tree has the shape of a random binary search tree, with $O(\log n)$ expected depth.

**Nearest neighbor search** is a branch and bound. The global variables $best$ and $d^*$ start as nil and $\infty$.

```pseudo id=nearest
NEAREST(t, q)
L17 if t = nil then return
L18 if dist(q, t.point) < d* then best ← t.point; d* ← dist(q, t.point)
L19 a ← t.axis; δ ← q_a − t.point_a
L20 if δ < 0 then (near, far) ← (t.left, t.right) else (near, far) ← (t.right, t.left)
L21 NEAREST(near, q)
L22 if |δ| < d* then NEAREST(far, q)
```

Each point on the far side is on the other side of the hyperplane $x_a = t.point_a$ from $q$, or on it, so its distance from $q$ is at least $|\delta|$. Line L22 skips the far side when no point there can beat $d^*$. The [k-d tree nearest neighbor search](/kd-tree-nearest-neighbor-search/) page treats the method and its $k$-nearest form in full.

**Deletion** cannot cut out an inner node as a binary search tree does, because a node's successor on its own axis does not respect the axes of the levels below. Instead it replaces the point by the least point on the node's axis from a subtree, and deletes that point from the subtree.

```pseudo id=delete
DELETE(T, p)
L23 find a node t with t.point = p by the search of INSERT; if there is none, return false
L24 if t.right ≠ nil then m ← FIND-MIN(t.right, t.axis); t.point ← m.point; t ← m; go to L24
L25 if t.left ≠ nil then m ← FIND-MIN(t.left, t.axis); t.point ← m.point; t.right ← t.left; t.left ← nil; t ← m; go to L24
L26 remove the leaf t from its parent; return true

FIND-MIN(u, a)                             ▷ a node of least point in the order <a in the subtree u
L27 return the least of u, FIND-MIN(u.left, a), and, only if u.axis ≠ a, FIND-MIN(u.right, a)
```

When the node has a right subtree, line L24 takes its least point $m$ in the order $<_a$: the left subtree is below the old point and so below $m$, and the rest of the right subtree is at least $m$. When it has only a left subtree, line L25 takes the least point of that subtree and moves the subtree to the right side, where (K) asks for points $\ge_a m$. Line L27 skips the right subtree of a node with axis $a$, since by (K) it holds no smaller point on that axis.

## Example

Build the tree on the six points $(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)$, with $k = 2$, axis 0 being $x$ and axis 1 being $y$. A tree is written as (left, point, right), and a leaf as its point.

| step | what happens | tree after |
|---|---|---|
| build, root | in $x$ order the points are (2,3), (4,7), (5,4), (7,2), (8,1), (9,6); rank 3 is (7,2) | (7,2) with left {(2,3), (4,7), (5,4)} and right {(8,1), (9,6)} |
| build, depth 1 | left in $y$ order: (2,3), (5,4), (4,7), rank 1 is (5,4); right in $y$ order: (8,1), (9,6), rank 1 is (9,6) | (((2,3), (5,4), (4,7)), (7,2), ((8,1), (9,6), nil)) |
| range $[3, 8] \times [1, 5]$ | visits all six nodes; at (2,3) it skips the left side ($3 > 2$), at (9,6) the right side ($5 < 6$) | reports (7,2), (5,4), (8,1) |
| nearest to $(9, 2)$ | (7,2) gives $d^* = 2$; near side right: (9,6) gives 4; its near side (8,1) gives $\sqrt 2$; back at the root, $\lvert\delta\rvert = 2 \ge \sqrt 2$, so the left subtree is skipped | returns (8,1) after 3 nodes |
| insert (6,3) | $6 \ge 7$ fails: left; at (5,4) on $y$, $3 < 4$: left; at (2,3) on $x$, $6 \ge 2$: right | (((nil, (2,3), (6,3)), (5,4), (4,7)), (7,2), ((8,1), (9,6), nil)) |
| delete (7,2) | the root has a right subtree; its least point in $x$ is (8,1), which moves up; the leaf (8,1) is cut off | (((nil, (2,3), (6,3)), (5,4), (4,7)), (8,1), (9,6)) |
| delete (5,4) | its right subtree is the leaf (4,7), which moves up and is cut off | (((nil, (2,3), (6,3)), (4,7), nil), (8,1), (9,6)) |

After the last step, the node (4,7) has axis $y$, and its left subtree holds (2,3) and (6,3), both with $y = 3 < 7$, as (K) requires.

## Correctness

Each operation keeps (K) and the rule that a node at depth $t$ has axis $t \bmod k$. BUILD makes (K) true by the choice of the two sets in lines L5 and L6. INSERT puts the new point on the side that (K) asks for at each node of its path. DELETE puts at $t$ the least point of the subtree on the side it uses, which is above every point of the left subtree and at most every point that stays on the right; and it moves points only upward inside their own subtree, so the constraints of the ancestors still hold. RANGE-SEARCH reports exactly the points in the box: it tests each visited point, and by (K) it never skips a subtree that holds an answer. NEAREST returns a closest point, since it skips only subtrees whose points are at distance at least $d^*$. The full proof is in the proofs folder.

## Complexity

The model is the [real RAM](/real-ram/) with $k$ fixed; each comparison of two points costs $O(k)$.

- **Build.** Line L3 costs $O(|P|)$ with a linear-time selection, and so do lines L5 and L6. The parts at one depth are disjoint, so each depth costs $O(n)$ in total, and there are $\lfloor \lg n \rfloor + 1$ depths: $O(n \log n)$ time in the worst case. With quickselect it is $O(n \log n)$ expected.
- **Insert and search.** One path from the root: $O(h)$. After BUILD, $h = \lfloor \lg n \rfloor + 1$.
- **Range search.** For a tree built by BUILD on points whose coordinates are distinct on each axis, with $k \ge 2$, RANGE-SEARCH visits $O(n^{1 - 1/k} + r)$ nodes in the worst case. A visited node either has its region inside the query box, and then it reports its own point, or its region meets the boundary of the box, which lies in $2k$ hyperplanes. A hyperplane $x_a = c$ meets at most one child region at a node with axis $a$ (apart from one node), and both at the other nodes, so it meets at most about $2^{t(1 - 1/k)}$ regions at depth $t$; summed over the $\lg n$ depths, this is $O(n^{1-1/k})$. The full proof and a matching lower bound are on the page [k-d tree range query complexity](/kd-tree-range-query-complexity/). For $k = 2$, a query box with no point in it can still visit $\Theta(\sqrt n)$ nodes.
- **Delete.** Line L23 costs $O(h)$. FIND-MIN at a node of height $g$ goes into one child at the levels with axis $a$ and into two at the others, so it visits at most $\sum_{j=0}^{g} 2^{\,j - \lfloor j/k \rfloor} = O(2^{g(1 - 1/k)})$ nodes. Each step of lines L24 and L25 moves $t$ at least one level down, so the costs of the successive calls form a geometric sum, and the total is $O(2^{h(1 - 1/k)})$, which is $O(n^{1 - 1/k})$ when $h \le \lg n + O(1)$, as after BUILD. On an unbalanced tree it can be far more.
- **Nearest neighbor.** In the worst case NEAREST visits each node, $O(n)$, for example when all points lie on a circle around $q$. Friedman, Bentley and Finkel showed a logarithmic expected time for points from a smooth distribution and fixed $k$; the constant grows exponentially in $k$.
- **Space.** One node per point: $\Theta(n)$.

| operation | time | case |
|---|---|---|
| build | $O(n \log n)$ | worst, with linear-time selection |
| insert, search | $O(h)$ | worst; $h = \lfloor \lg n \rfloor + 1$ after build |
| delete | $O(n^{1 - 1/k})$ | worst, when $h \le \lg n + O(1)$ |
| range_search | $O(n^{1 - 1/k} + r)$ | worst, built tree, distinct coordinates |
| nearest | $O(n)$ | worst; logarithmic expected on smooth random data |
| space | $\Theta(n)$ | total |

## Variants

- **Points in the leaves.** de Berg and others store the points only in the leaves and a split value in each inner node. The bounds are the same.
- **Split rules.** Instead of cycling, split the axis of largest spread, or cut the longest side of the cell at its middle (the sliding midpoint rule). These adapt to the data and help nearest neighbor search.
- **Buckets.** Leaves that hold up to $b$ points make the tree shallower and faster in practice.
- **Rebalancing.** A k-d tree cannot be rotated as a binary search tree can, because a rotation changes the axis of the nodes. Dynamic versions rebuild subtrees that become unbalanced (as in a [scapegoat tree](/scapegoat-tree/)), or use the logarithmic method.
- **On disk.** The [k-d-B tree](/kd-b-tree/) puts many splits in one page and keeps all leaves at one depth.
- **Other space-splitting trees.** A [quadtree](/quadtree/) cuts every axis at once; a [BSP tree](/bsp-tree/) cuts by hyperplanes of any direction. A [range tree](/range-tree/) answers range queries in $O(\log^{k} n + r)$ time, or $O(\log^{k-1} n + r)$ with fractional cascading, with $O(n \log^{k-1} n)$ space.

## When to use it

Use a k-d tree for points in a small dimension, up to about 10, held in memory, when you need range queries and nearest neighbor queries with linear space. It is simple, compact and fast in practice. Use a [range tree](/range-tree/) when worst-case polylogarithmic range queries are worth more space. Use an [R-tree](/r-tree/) or a [k-d-B tree](/kd-b-tree/) for data on disk, and for objects with extent. In high dimensions the tree degrades toward a scan, and approximate methods such as [locality-sensitive hashing](/locality-sensitive-hashing/) work better.

## Pitfalls

- **Ties on the splitting axis.** If the split compares only $p_a$ and puts all equal values on one side, many equal coordinates make a deep, unbalanced tree, and a deletion can break the order. Compare by the superkey $<_a$, as lines L3, L5 and L15 do.
- **Pruning with the wrong test.** In RANGE-SEARCH, writing `ℓa < t.point_a` in line L11 misses the points of the left subtree with $p_a = \ell_a = t.point_a$. The test must allow equality on both sides, as lines L11 and L12 do. A test with many equal coordinates catches this.
- **Deleting like a binary search tree.** Replacing a node by its in-order successor on the root's axis breaks (K) at the levels below. Lines L24 and L25 search for the least point on the axis of the node itself.
- **Recursion depth.** After many insertions in sorted order the tree is a path, and recursive code overflows the stack. Use loops and an explicit stack, as the implementation does.
- **Skipping the far side too early.** Line L22 must search the far side whenever $|\delta| < d^*$. Code that skips it as soon as the near side gives any point returns a wrong answer for queries near a splitting line.

## Implementations

## History

Jon Louis Bentley described the multidimensional binary search tree, which he called the k-d tree, in Communications of the ACM in 1975, from his work as a student at Stanford. The paper gave insertion, deletion, exact and partial match search, and the balanced tree built by medians. Friedman, Bentley and Finkel gave the nearest neighbor search with logarithmic expected time in 1977. In the same year Lee and Wong proved the worst-case bound $O(k\, n^{1 - 1/k})$ for region queries.

## References
