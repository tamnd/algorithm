---
tag: GXNZ91
kind: algorithm
slug: kd-tree-nearest-neighbor-search
name: Nearest neighbor search in a kd-tree
aliases:
- Nearest-neighbor search in a k-d tree
- kd-tree NN search
- branch and bound nearest neighbor search
area: geometry/proximity
level: core
summary: Descend the kd-tree to the query's cell, then backtrack and prune subtrees that cannot contain a closer point.
solves: [nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points in the tree, d: the dimension}
  time: {worst: O(n), average: O(log n)}
  space: {extra: O(log n)}
properties: {online: true, deterministic: true, recursive: true}
history:
  year: 1977
  people: [Jerome H. Friedman, Jon Louis Bentley, Raphael Ari Finkel]
  note: Friedman, Bentley and Finkel gave the branch and bound search for best matches in a kd-tree in 1977 and showed logarithmic expected time for fixed dimension under mild assumptions on the distribution.
prereqs: [kd-tree, nearest-neighbor-search, euclidean-distance]
see_also: [kd-tree-traversal, approximate-nearest-neighbor, voronoi-diagram, all-nearest-neighbors, locality-sensitive-hashing, quadtree, spatial-index]
sources:
  - paper: doi:10.1145/355744.355745
    title: Jerome H. Friedman, Jon Louis Bentley and Raphael Ari Finkel, An algorithm for finding best matches in logarithmic expected time, ACM Transactions on Mathematical Software 3(3), 1977, 209-226
    locator: the search with the bounds-overlap-ball test, the optimized tree, and the analysis of the expected number of records examined
  - paper: doi:10.1145/361002.361007
    title: Jon Louis Bentley, Multidimensional binary search trees used for associative searching, Communications of the ACM 18(9), 1975, 509-517
    locator: the kd-tree with cycling discriminators on which the search runs
  - paper: doi:10.1145/293347.293348
    title: Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998, 891-923
    locator: the priority search over a tree of boxes and the (1 + epsilon) stopping rule, contrasted with exact kd-tree search
  - paper: "Robert F. Sproull, Refinements to nearest-neighbor searching in k-dimensional trees, Algorithmica 6, 1991, 579-589"
    locator: experiments showing how the number of examined points grows with the dimension
---

Nearest neighbor search in a [kd-tree](/kd-tree/) answers the query "which stored point is closest to $q$?" by branch and bound. It first walks down the tree to the region that contains $q$, as in an exact-match search, which gives a good first candidate. Then, while returning up the tree, it visits the other side of a split only if the splitting line or plane is closer to $q$ than the best point found so far. On well-spread data in a fixed low dimension the search looks at a small number of nodes and takes $O(\log n)$ expected time (Friedman, Bentley and Finkel, 1977); in the worst case it can visit every node. All tests compare squared distances, so it is exact on integer input.

## In plain words

A kd-tree cuts space in half again and again, alternating between vertical and horizontal cuts, and keeps one point at each cut.

To find the point nearest to a query, first go down the tree the way the query falls: left or right of each cut. The points you pass on the way are good guesses, and you remember the best one.

Then go back up. At each cut, ask: could anything on the other side be closer than my best guess? Anything on the other side is at least as far away as the cut itself. If the cut is farther than your best guess, skip that whole half. Otherwise search it too. Most halves are skipped when the points are spread out.

## The problem

**Input.** A kd-tree $T$ built on a set $P$ of $n$ points in $\mathbb{R}^d$, and a query point $q \in \mathbb{R}^d$. Coordinates are integers or rationals for exact answers. Duplicates are allowed.

**Output.** A point $p \in P$ minimizing $\|q - p\|^2$, together with that squared distance; none if $P$ is empty. If several points tie, any one of them is correct.

**The tree.** Each node $v$ stores a point $v.p$ and an axis $v.a$ (the depth modulo $d$). Every point in the left subtree has coordinate $a$ at most $v.p[a]$, and every point in the right subtree has coordinate $a$ at least $v.p[a]$. Points equal to $v.p[a]$ in coordinate $a$ may be on either side. Building the tree by medians gives height $\lceil \lg (n+1) \rceil$ or less.

## The algorithm

```pseudo id=main
NEAREST(T, q)
L1  best ← (∞, none)
L2  SEARCH(T.root)
L3  return best

SEARCH(v)
L4  if v = nil then return
L5  p ← v.point; a ← v.axis
L6  if ‖q − p‖² < best.d2 then best ← (‖q − p‖², p)
L7  diff ← q[a] − p[a]
L8  if diff < 0 then (near, far) ← (v.left, v.right) else (near, far) ← (v.right, v.left)
L9  SEARCH(near)
L10 if diff² < best.d2 then SEARCH(far)
```

Line L9 searches the side of the split that contains $q$ first, so $best$ is usually small by the time line L10 is reached. Line L10 is the pruning test: every point $r$ on the far side lies on the other side of the hyperplane $x_a = p[a]$ from $q$ (or on it), so $\|q - r\|^2 \ge (q[a] - r[a])^2 \ge \mathrm{diff}^2$. If $\mathrm{diff}^2 \ge best.d2$, no point there is strictly closer, and the subtree is skipped. The test uses the squared difference, so no square root is taken.

## Example

The tree for $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)\}$ built by medians has root $(7,2)$ (split on $x$), whose left child $(5,4)$ (split on $y$) has children $(2,3)$ and $(4,7)$, and whose right child $(9,6)$ (split on $y$) has left child $(8,1)$. Query $q = (3,6)$:

| node | axis | $\|q - p\|^2$ | best after L6 | diff | near, far | far side searched? |
| --- | --- | --- | --- | --- | --- | --- |
| $(7,2)$ | $x$ | $32$ | $32$, $(7,2)$ | $3 - 7 = -4$ | left, right | after the left side, $16 \ge 2$: no |
| $(5,4)$ | $y$ | $8$ | $8$, $(5,4)$ | $6 - 4 = 2$ | right, left | after the right side, $4 \ge 2$: no |
| $(4,7)$ | $x$ | $2$ | $2$, $(4,7)$ | $3 - 4 = -1$ | both empty | |

The search visits 3 of the 6 nodes and returns $(4,7)$ with squared distance $2$. The subtree of $(2,3)$ is skipped because the line $y = 4$ is at squared distance $4$ from $q$, more than $2$, and the whole right half is skipped because the line $x = 7$ is at squared distance $16$.

## Correctness

The search keeps the invariant that $best$ is the closest point among the visited nodes. A subtree is skipped only by line L10, and only when every point in it is at squared distance at least $\mathrm{diff}^2 \ge best.d2$ from $q$, so it contains no strictly closer point. Every node is either visited or in a skipped subtree, so at the end no point is strictly closer than $best$. The full proof is in the correctness proof below.

## Complexity

- **Worst case.** $O(n)$ time per query: each node is visited at most once and costs $O(d)$. The bound is reached: for the lattice points on a circle and the query at its center, every point is at the same distance, line L10 can skip only empty subtrees, and the search visits every node.
- **Expected case.** For a fixed dimension $d$, points drawn from a distribution with a smooth density, and a tree built by medians, Friedman, Bentley and Finkel showed that the expected number of points examined is bounded by a constant depending on $d$, so a query takes $O(\log n)$ expected time, the cost of the descent. The constant grows exponentially with $d$; in high dimensions most of the tree is visited (Sproull, 1991).
- **Space.** $O(\log n)$ for the recursion on a tree built by medians, plus the tree itself.

The tests count visited nodes: 300 random queries on 4096 spread-out points visit fewer than 100 nodes on average, while the circle example visits all of them. The details are in the complexity proof below.

## Properties

- **Exact.** Only differences, squares, sums and comparisons. No root.
- **Online.** Queries can be answered one at a time, and the tree supports insertion.
- **Any dimension and any $L_p$ metric.** The same pruning test works with $|\mathrm{diff}|^p$ for $L_p$ distances; only the cost changes with $d$.
- **First answer quickly.** After the first descent the candidate is often already the answer; the rest of the search proves it.

## Variants and improvements

- **Bounding-box distance.** Keep the distance from $q$ to the whole cell of the far child, not only to its splitting plane. This prunes more, and Arya and Mount's incremental distance computation does it in $O(1)$ per node.
- **k nearest neighbors.** Keep the $k$ best points in a max-[heap](/heap/) and prune against the largest of them; the search returns the $k$ nearest points.
- **Best-first search.** Visit nodes in order of their cell distance from $q$ with a [priority queue](/priority-queue/), and stop when the next cell is farther than the best point. With the rule "stop when the next cell is farther than $best/(1 + \varepsilon)$", this is the [approximate nearest neighbor](/approximate-nearest-neighbor/) search of Arya et al.
- **Fixed-radius and range queries.** Replace $best$ by a fixed radius to report all points within it; see [kd-tree traversal](/kd-tree-traversal/).
- **Worst-case guarantees.** For the exact problem in the plane, a [Voronoi diagram](/voronoi-diagram/) with a point location structure answers queries in $O(\log n)$ worst-case time with $O(n)$ space.

## When to use it

Use a kd-tree search for many nearest neighbor queries on a fixed or slowly changing set of points in low dimension, about $d \le 10$, when data is spread out and the worst case is unlikely. It is simple, needs linear space, and is the default in many libraries. For guaranteed $O(\log n)$ queries in the plane, use a Voronoi diagram with point location. In high dimensions, use approximate methods such as [locality-sensitive hashing](/locality-sensitive-hashing/) or a linear scan, since the tree visits most nodes anyway.

## Pitfalls

- **Pruning with the wrong inequality.** Writing $|\mathrm{diff}| \le \sqrt{best.d2}$ in floating point can round in the wrong direction and skip a subtree that holds the answer. Line L10 compares $\mathrm{diff}^2$ with $best.d2$ exactly.
- **Skipping the far side when $\mathrm{diff} = 0$.** Points equal to $p[a]$ in coordinate $a$ can be on either side, so a query on the splitting plane must still be allowed to search the far side; line L10 does, since $0 < best.d2$ unless an exact match was found.
- **Searching the far side first.** Swapping the two calls of lines L9 and L10 is still correct, but $best$ is still large when the far test is made, so much less is pruned.
- **Recursion depth on unbalanced trees.** A tree built by inserting sorted points has height $n$, and a recursive search overflows the stack. Build by medians, or use an explicit stack.
- **Expecting logarithmic time in high dimension.** The expected-time result holds for fixed $d$ and $n$ large compared with $2^d$; for $d = 50$ and $n = 10^6$ almost every leaf is visited.

## Implementations

## History

Bentley introduced the kd-tree in 1975, with exact-match and region searches. Friedman, Bentley and Finkel published the nearest neighbor search in 1977, with the "bounds overlap ball" test that this page writes as line L10, and proved that for fixed dimension the expected number of points examined does not grow with $n$. Sproull (1991) measured how the method degrades as the dimension grows. Arya, Mount and coauthors (1998) turned the best-first variant into an approximate search with guaranteed bounds, the basis of the ANN library.

## References
