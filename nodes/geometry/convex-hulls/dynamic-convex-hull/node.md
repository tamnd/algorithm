---
tag: WCEQ10
kind: data-structure
slug: dynamic-convex-hull
name: Dynamic convex hull
aliases:
- Overmars-van Leeuwen structure
- fully dynamic convex hull
- dynamic planar convex hull
area: geometry/convex-hulls
level: advanced
summary: Maintains the hull of a point set under insertions and deletions in O(log^2 n) time per update.
model: real-ram
complexity:
  vars: {n: the number of points in the set, h: the number of hull vertices}
  time: {insert: O(log^2 n) expected, delete: O(log^2 n) expected, query: O(h)}
  space: {extra: O(n log n) expected}
prereqs: [convex-hull-problem, upper-and-lower-hull, treap, path-copying]
see_also: [andrew-monotone-chain, kirkpatrick-seidel, convex-layers, persistent-treap, convex-hull-trick, decomposable-searching-problem, melkman-algorithm, point-in-convex-polygon]
sources:
  - paper: doi:10.1016/0022-0000(81)90012-X
    title: Mark H. Overmars and Jan van Leeuwen, Maintenance of configurations in the plane, Journal of Computer and System Sciences 23(2) (1981), 166-204
    locator: the tree of points in which each node keeps the bridge of its two children and the part of its hull not used by its parent, the bridge search by simultaneous descent, and the O(log^2 n) bound per update
  - paper: doi:10.1145/359131.359132
    title: Franco P. Preparata, An optimal real-time algorithm for planar convex hulls, Communications of the ACM 22(7) (1979), 402-405
    locator: the insertion-only hull in a balanced search tree with O(log n) time per insertion
  - paper: doi:10.1145/363647.363652
    title: Timothy M. Chan, Dynamic planar convex hull operations in near-logarithmic amortized time, Journal of the ACM 48(1) (2001), 1-12
    locator: the review of earlier dynamic hull bounds and the structure with near-logarithmic amortized update time
  - paper: doi:10.1109/SFCS.2002.1181985
    title: Gerth Stølting Brodal and Riko Jacob, Dynamic planar convex hull, Proceedings of the 43rd IEEE Symposium on Foundations of Computer Science (2002), 617-626
    locator: the structure with O(log n) amortized time per insertion and deletion
---

A dynamic convex hull keeps the [convex hull](/convex-hull-problem/) of a set of points in the plane while points are inserted and deleted. Overmars and van Leeuwen gave the first structure with $O(\log^2 n)$ time per update: a balanced tree over the points sorted by $x$ in which every node knows the hull of its subtree, built from the hulls of its two children by one bridge search. This page uses a treap version of that idea with persistent chains, which has the same bound in expectation and is short to write.

## In plain words

Sort the points from left to right and put them in a search tree. Every node of the tree keeps the top part and the bottom part of the hull of the points below it. The hull of a node comes from the hulls of its two children. Find the one segment that joins the left hull to the right hull with every point under it, keep the left hull up to that segment and the right hull from that segment, and join the two pieces. The segment is found by walking down both hulls at the same time, one step at a time.

When a point comes or goes, only the nodes on one path from the root change. Each of them builds its hull again from its children. The old hulls are never changed, so a new hull can share most of its pieces with old ones.

## The abstract type

The structure holds a finite set $S$ of distinct points with integer or rational coordinates. The operations are:

- **INSERT$(p)$.** Add $p$ to $S$. Return false, and change nothing, if $p \in S$.
- **DELETE$(p)$.** Remove $p$ from $S$. Return false if $p \notin S$.
- **CONTAINS$(p)$.** Whether $p \in S$.
- **HULL.** The vertices of $\operatorname{conv}(S)$, counterclockwise from the lexicographically smallest point.

Notation: $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$ is the [orientation test](/orientation-test/), positive for a left turn. Points are ordered lexicographically, by $x$ and then by $y$, and $p < q$ refers to this order. The upper chain $U(X)$ and the lower chain $\Lambda(X)$ of a set $X$ are the lists that [Andrew's monotone chain](/andrew-monotone-chain/) builds from $X$ in this order; they share their first and last points, and together they are the hull. No general position is needed. Points with equal $x$ are handled as if the plane were sheared by a very small amount, $x \mapsto x + \varepsilon y$, which keeps every orientation and makes the lexicographic order an order by $x$. So a vertical edge at the left end belongs to the upper chain and one at the right end to the lower chain. Points on a hull edge but not at a corner are not hull vertices. All tests are exact on integers, and the one intersection point of line L27 is a pair of fractions.

## Representation

- **Base treap.** A [treap](/treap/) whose keys are the points of $S$ in lexicographic order, with a random priority for each point. Node $v$ has a point, a priority, two children and the size of its subtree. Let $S_v$ be the points in the subtree of $v$; they form a contiguous range of $S$ in the order.
- **Chains at a node.** Node $v$ also stores $\mathrm{up}(v) = U(S_v)$ and $\mathrm{low}(v) = \Lambda(S_v)$. Each is a chain treap: a treap of the chain points in lexicographic order, where the node of point $p$ has the priority of $p$. A chain node also stores the first and the last point of its subtree, so the neighbors of a chain point are found in $O(1)$ from its subtree and two points tracked during a descent.
- **Persistence.** Base nodes and chain nodes are never changed after they are made. New versions are made by [path copying](/path-copying/), so the chain of a node can share most of its nodes with the chains of its children. This replaces the concatenable queues and the down-passing of the original structure.

## Operations

```pseudo id=main
INSERT(p)
L1  if p ∈ S then return false
L2  (X, Y) ← SPLIT(root, p)
L3  root ← JOIN(JOIN(X, NODE(p, random priority, nil, nil)), Y), return true
DELETE(p)                                   ▷ p ∈ S
L4  (X, Y) ← SPLIT(root, p)
L5  root ← JOIN(X, Y)
SPLIT(t, p)                                 ▷ the points < p and > p; p itself is dropped
L6  if t = nil then return (nil, nil)
L7  if t.p < p then (X, Y) ← SPLIT(t.right, p), return (NODE(t.p, t.prio, t.left, X), Y)
L8  if t.p > p then (X, Y) ← SPLIT(t.left, p), return (X, NODE(t.p, t.prio, Y, t.right))
L9  return (t.left, t.right)
JOIN(X, Y)                                  ▷ every point of X < every point of Y
L10 if X = nil or Y = nil then return the other one
L11 if X.prio > Y.prio then return NODE(X.p, X.prio, X.left, JOIN(X.right, Y))
L12 return NODE(Y.p, Y.prio, JOIN(X, Y.left), Y.right)
NODE(p, π, ℓ, ρ)                            ▷ a new base node; ℓ and ρ are its children
L13 up ← MERGE(MERGE(up(ℓ), ⟨p⟩, +1), up(ρ), +1), low ← the same with low and −1
L14 size ← 1 + size(ℓ) + size(ρ), return the node
MERGE(A, B, s)                              ▷ chains of L and R, every point of L < every point of R
L15 if A or B is empty then return the other one
L16 (l, r) ← BRIDGE(A, B, s)
L17 return CONCAT(the points of A up to l, the points of B from r)
BRIDGE(A, B, s)                             ▷ q is above the line ab when s · D(a, b, q) > 0
L18 α ← root of A, β ← root of B, r₀ ← first point of B
L19 loop
L20   a ← α.p, b ← β.p, with neighbors a⁻, a⁺ in A and b⁻, b⁺ in B
L21   if a⁻ or b⁺ is on or above the line ab then
L22     if a⁻ is on or above the line ab then α ← α.left
L23     if b⁺ is on or above the line ab then β ← β.right
L24   else if neither a⁺ nor b⁻ is strictly above ab then return (a, b)
L25   else if b⁻ is not strictly above ab then α ← α.right
L26   else if a⁺ is not strictly above ab then β ← β.left
L27   else z ← line(a, a⁺) ∩ line(b⁻, b), if z < r₀ then α ← α.right else β ← β.left
HULL
L28 return low(root), then up(root) backwards without its first and last points
```

Lines L1 to L12 are the usual treap insertion and deletion by [split](/treap-split/) and [join](/treap-merge/), with path copying. Every base node that they make gets its chains in line L13 from the chains of its children, so a node with a correct subtree always stores correct chains. Lines L15 to L17 merge two chains: the result is the left chain up to the bridge and the right chain from the bridge, cut and joined as chain treaps. Lines L18 to L27 find the bridge by the simultaneous descent of Overmars and van Leeuwen. In each round, a test on one chain alone moves that side when it is sure which way the bridge is. When both points still have a neighbor above the line $ab$, line L27 decides by the side on which the two edge lines cross.

## Example

The table inserts and deletes points one at a time and shows HULL after each step.

| step | operation | HULL |
| --- | --- | --- |
| 1 | insert $(0,0)$ | $(0,0)$ |
| 2 | insert $(6,0)$ | $(0,0), (6,0)$ |
| 3 | insert $(3,4)$ | $(0,0), (6,0), (3,4)$ |
| 4 | insert $(3,1)$ | $(0,0), (6,0), (3,4)$ |
| 5 | insert $(0,4)$ | $(0,0), (6,0), (3,4), (0,4)$ |
| 6 | insert $(7,3)$ | $(0,0), (6,0), (7,3), (3,4), (0,4)$ |
| 7 | delete $(3,4)$ | $(0,0), (6,0), (7,3), (0,4)$ |
| 8 | delete $(0,0)$ | $(0,4), (3,1), (6,0), (7,3)$ |
| 9 | delete $(3,1)$ | $(0,4), (6,0), (7,3)$ |

Step 4 adds a point inside the triangle, and the hull does not change. At step 8, $(3,1)$ comes back as a vertex: it was inside the hull for four steps, but it stayed in the base treap, and the chains of the nodes on the changed path are built again from their children. The structure never needs to remember which points were inside.

**One bridge search.** Let $L = \{(0,0), (1,3), (2,4), (3,3), (4,1)\}$ and $R = \{(5,0), (6,5), (8,6), (9,2)\}$. All points of each set are on its upper chain. In the chain treap of $A = U(L)$ the root is $(3,3)$, with left child $(1,3)$, whose children are $(0,0)$ and $(2,4)$, and right child $(4,1)$. In the chain treap of $B = U(R)$ the root is $(6,5)$, with left child $(5,0)$ and right child $(9,2)$, whose left child is $(8,6)$. The values are $D(a, b, q)$ for $s = +1$.

| round | $a$ | $b$ | $a^-$ | $a^+$ | $b^-$ | $b^+$ | line | move |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | $(3,3)$ | $(6,5)$ | $5$ | $-8$ | $-13$ | $-1$ | L22 | $\alpha$ to the left |
| 2 | $(1,3)$ | $(6,5)$ | $-13$ | $3$ | $-23$ | $1$ | L23 | $\beta$ to the right |
| 3 | $(1,3)$ | $(9,2)$ | $-25$ | $9$ | $31$ | none | L27 | $z = (36/5, 46/5) > (5,0)$, $\beta$ to the left |
| 4 | $(1,3)$ | $(8,6)$ | $-18$ | $4$ | $-1$ | $-31$ | L25 | $\alpha$ to the right |
| 5 | $(2,4)$ | $(8,6)$ | $-4$ | $-8$ | $-2$ | $-26$ | L24 | return |

The bridge is $(2,4)$ to $(8,6)$, so the merged upper chain is $(0,0), (1,3), (2,4), (8,6), (9,2)$. In round 3 both $a^+$ and $b^-$ are above the line, and the lines $y = x + 2$ and $y = 38 - 4x$ cross at $x = 36/5$, to the right of every point of $L$. So the bridge cannot end at $(9,2)$ or to its right, and $\beta$ goes left.

## Correctness

Three facts carry the proof. First, the upper chain of $L \cup R$, for $L$ before $R$ in the order, is the chain of $L$ up to the left end $l$ of the bridge, then the chain of $R$ from its right end $r$. Second, each move of the descent keeps $l$ in the subtree of $\alpha$ and $r$ in the subtree of $\beta$. Line L22 is safe because a point $a \le l$ is a vertex of the merged chain and its left neighbor must be strictly below every line from $a$ to a point on the right. Lines L25 and L26 compare slopes with the slope of the bridge. Line L27 uses the crossing $z$ of the two edge lines: if the bridge ended at or right of both $a$ and $b$, the edge lines and the bridge line would give an order that contradicts the side of $z$. Third, when no rule moves, the line $ab$ supports both sets, so it is the bridge line, and the strict tests make $a = l$ and $b = r$. The shear reduces equal $x$-coordinates to the case of distinct ones, and a reflection reduces lower chains to upper chains. The full proof is in the [correctness proof](proofs/correctness/).

## Complexity

Let $d$ be the largest depth of the base treap and of the chain treaps that occur in one operation.

- **Base treap.** SPLIT and JOIN follow one or two paths, so one update makes $O(d)$ new base nodes.
- **One base node.** Line L13 does four merges. Each BRIDGE moves one of $\alpha$, $\beta$ down in every round, so it takes at most $2d + 1$ rounds of $O(1)$ work, as line L27 is one exact intersection. The cut and the join of line L17 take $O(d)$. So one node costs $O(d)$.
- **Depth.** A chain treap holds $U(S_v)$ or a part of it with the priorities of its points, so it has the shape of a treap of that set. The sets $S_v$ are contiguous ranges of $S$, so there are $O(n^2)$ possible chain sets, and each is fixed by $S$ alone. For one fixed set, a treap with random priorities has depth $O(\log n)$ with probability $1 - O(n^{-c})$ for every constant $c$ with a suitable constant factor, as on the [treap](/treap/) page. A union bound over the $O(n^2)$ sets gives $d = O(\log n)$ with high probability. As one update costs at most $O(n^2)$ in any case, its expected time is $O(\log^2 n)$. This assumes that the updates do not depend on the priorities.
- **Queries.** CONTAINS costs $O(\log n)$ expected and HULL costs $O(h)$ to list the two chains of the root.
- **Space.** Each base node, when it is made, adds $O(\log n)$ chain nodes with high probability. So the reachable structure has $O(n \log n)$ nodes in expectation. Old versions that are no longer reachable are freed by the garbage collector.

The original structure of Overmars and van Leeuwen has $O(\log^2 n)$ time per update in the worst case and $O(n)$ space, at the cost of the concatenable queues and the step that passes hull pieces down the tree. Any structure that reports the hull after each insertion needs $\Omega(\log n)$ amortized time per operation, because $n$ insertions followed by one HULL sort the points on a parabola, by the [sorting lower bound for hulls](/convex-hull-lower-bound/).

## Variants

- **The original structure.** Overmars and van Leeuwen use a balanced leaf-search tree. Each internal node stores the bridge of its children and only the part of its subtree's chain that its parent does not use, in a concatenable queue. An update first passes the chains down along the path, then builds them again on the way up. This gives $O(\log^2 n)$ worst-case time and linear space.
- **Insertions only.** Preparata keeps the hull in a balanced search tree and inserts a point in $O(\log n)$ time by finding its two tangents and cutting out the part between them. This is a real-time algorithm: the hull is known after each insertion.
- **Deletions only.** A structure that only deletes can be faster. Chazelle used one to compute the [convex layers](/convex-layers/) of $n$ points in $O(n \log n)$ time, peeling one layer after another. With the structure of this page, peeling costs $O(n \log^2 n)$ expected: every point is deleted once.
- **Faster updates.** Chan gave a structure with $O(\log^{1 + \varepsilon} n)$ amortized time per update and $O(\log n)$ time for extreme-point queries. Brodal and Jacob reached $O(\log n)$ amortized time per update.
- **Queries on the hull.** The two root chains are search trees in the order of the hull, so a descent like BRIDGE answers in $O(\log n)$ expected time the extreme point in a direction, the tangents from an outside point, and whether a point lies inside the hull, as for a static [convex polygon](/point-in-convex-polygon/).
- **Envelopes of lines.** By point-line duality, the upper chain of points is the lower envelope of lines. So the structure also keeps a set of lines under insertions and deletions with fast queries for the lowest line at an $x$-coordinate. The [convex hull trick](/convex-hull-trick/) is the special case with insertions only.

## When to use it

Use a dynamic convex hull when insertions and deletions are mixed with hull queries online. If there are only insertions, a balanced tree of the current hull, or a [Li Chao tree](/li-chao-tree/) for the dual envelope problem, is simpler. If all updates are known in advance, an offline method can process them together. If only the final hull is needed, compute it once with [Andrew's monotone chain](/andrew-monotone-chain/) or [Kirkpatrick-Seidel](/kirkpatrick-seidel/).

## Pitfalls

- **Strict and non-strict tests.** Lines L21 to L23 move on a neighbor *on or above* the line, and lines L24 to L27 use *strictly above*. With other choices, collinear points can be kept as hull vertices, or the descent can leave the subtree that holds the bridge.
- **Equal $x$-coordinates.** Order the points lexicographically, never by $x$ alone, and do the same in line L27. Then a vertical edge needs no special case.
- **Exact arithmetic.** Line L27 compares a crossing point with $r_0$. With floating point, a crossing very close to $r_0$ can go to the wrong side, and the descent then leaves the subtree with the bridge and may return a wrong pair.
- **Shared nodes.** A chain node can be part of the chains of many base nodes. A change in place, as in an ordinary treap split, corrupts other chains. Every operation must copy the path it changes.
- **Recursion depth.** The depth is $O(\log n)$ only in expectation and with high probability. Fixed priorities, or priorities that an adversary can see, can make the trees deep.
- **Duplicates.** Insert a point only once. A second copy would break the strict order that the chains rely on.

## Implementations

## History

Franco Preparata gave a real-time algorithm for the planar hull under insertions in 1979. Mark Overmars and Jan van Leeuwen published the fully dynamic structure in 1981, in "Maintenance of configurations in the plane", with $O(\log^2 n)$ time per update. Their idea of storing at each node only what its parent does not use, and of passing it down before an update, was used for other planar problems as well. Bernard Chazelle used a deletion-only hull for the convex layers in 1985. Timothy Chan in 2001, and Gerth Stølting Brodal and Riko Jacob in 2002, reduced the amortized update time to near-logarithmic and then to logarithmic.

## References
