---
tag: P6SV6A
kind: theorem
slug: flip-graph-diameter-theorem
name: Flip graph diameter theorem
aliases:
- Sleator-Tarjan-Thurston flip bound
- diameter of the associahedron
- rotation distance bound 2n - 6
area: geometry/triangulations
level: research
summary: Any two triangulations of a convex n-gon are connected by at most 2n-10 flips for n at least 13.
prereqs: [flip-graph, edge-flip, catalan-triangulation-theorem]
see_also: [flip-distance, tree-rotation, binary-tree, triangulation-dual-tree, number-of-triangulations, convex-polygon, polygon-triangulation]
sources:
  - paper: "Daniel D. Sleator, Robert E. Tarjan and William P. Thurston, Rotation distance, triangulations, and hyperbolic geometry, Journal of the American Mathematical Society 1(3), 647 to 681 (1988)"
    locator: the upper bound 2n - 10 for n at least 13 by the fan argument, and the matching lower bound for all large n by hyperbolic volume
  - paper: "Lionel Pournin, The diameter of associahedra, Advances in Mathematics 259, 13 to 42 (2014)"
    locator: a combinatorial proof that the diameter is 2n - 10 for every n at least 13
  - paper: "Daniel D. Sleator, Robert E. Tarjan and William P. Thurston, Rotation distance, triangulations, and hyperbolic geometry, Proceedings of the 18th ACM Symposium on Theory of Computing, 122 to 135 (1986)"
    locator: the conference version
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: Chapter 3, the flip graph of a convex polygon and its diameter (section to be checked)
---

The flip graph diameter theorem says that any two triangulations of a convex polygon with $n$ vertices can be transformed into each other by at most $2n - 10$ [edge flips](/edge-flip/) when $n \ge 13$, and that this is the best possible: for every $n \ge 13$ some pair needs exactly $2n - 10$ flips. Equivalently, the 1-skeleton of the $(n-3)$-dimensional associahedron has diameter $2n - 10$, and two binary trees with $m$ internal nodes are at rotation distance at most $2m - 6$ for $m \ge 11$. The upper bound has a short counting proof. The lower bound was proved by Sleator, Tarjan and Thurston in 1988 for all sufficiently large $n$, with hyperbolic geometry, and by Pournin in 2014 for every $n \ge 13$, combinatorially.

## Statement

Let $P$ be a convex polygon with $n$ vertices, and let $d(T_1, T_2)$ be the [flip distance](/flip-distance/) between two triangulations of $P$, the distance in the [flip graph](/flip-graph/).

**Theorem.** For every $n \ge 13$ and all triangulations $T_1$, $T_2$ of $P$, $d(T_1, T_2) \le 2n - 10$. For every $n \ge 13$ there are triangulations with $d(T_1, T_2) = 2n - 10$.

**The same proof gives, for smaller $n$:** $d(T_1, T_2) \le 2n - 6 - \lceil 4 - 12/n \rceil$ for every $n \ge 4$, which is $2n - 9$ for $7 \le n \le 12$, $2n - 8$ for $n = 5, 6$, and $1$ for $n = 4$.

## In plain words

Take a shape with $n$ corners, all bulging outward, and two ways of cutting it into triangles. A move swaps one cutting line for the other diagonal of the four-sided piece around it. However different the two cuttings are, you never need more than about twice the number of corners in moves, and for large shapes some pairs need exactly that many.

The upper bound is easy: pick a corner that both cuttings use a lot, and turn both into the cutting where all lines start from that corner. The lower bound is hard and was first proved using geometry of curved space.

## Proof

Write the vertices of $P$ as $v_1, \ldots, v_n$, and for a triangulation $T$ let $\deg_T(v)$ be the number of diagonals of $T$ at $v$. Every triangulation has $n - 3$ diagonals. The **fan** $F_v$ is the triangulation whose $n - 3$ diagonals all end at $v$.

**Lemma 1.** $d(T, F_v) \le n - 3 - \deg_T(v)$ for every triangulation $T$ and vertex $v$.

*Proof.* By induction on $k = n - 3 - \deg_T(v)$, the number of diagonals of $T$ not at $v$. If $k = 0$, all diagonals are at $v$, so $T = F_v$. If $k > 0$, $T \ne F_v$, so some triangle $v a b$ of $T$ at $v$ has a side $ab$ that is a diagonal: otherwise every triangle at $v$ has its side opposite $v$ on the boundary, and these triangles, which surround $v$ inside $P$, would cover all of $P$, making all diagonals end at $v$. The diagonal $ab$ is a side of a second triangle $a b w$ with $w \ne v$. The quadrilateral $v a w b$ has its vertices among those of the convex polygon $P$, so it is convex, and flipping $ab$ replaces it with $vw$. The number of diagonals not at $v$ falls by one, and the induction hypothesis gives the rest. $\square$

**Lemma 2.** $d(T_1, T_2) \le 2n - 6 - \deg_{T_1}(v) - \deg_{T_2}(v)$ for every vertex $v$.

*Proof.* Flips are reversible, so $d(F_v, T_2) = d(T_2, F_v)$. Go from $T_1$ to $F_v$ and from $F_v$ to $T_2$, and apply Lemma 1 twice. $\square$

**Lemma 3.** $\sum_{v} \left( \deg_{T_1}(v) + \deg_{T_2}(v) \right) = 4n - 12$.

*Proof.* Each of the $n - 3$ diagonals of a triangulation has two end points, so the degrees of one triangulation add up to $2n - 6$. $\square$

**The upper bound.** Suppose $n \ge 13$. If every vertex had $\deg_{T_1}(v) + \deg_{T_2}(v) \le 3$, the sum in Lemma 3 would be at most $3n$, but $4n - 12 > 3n$ when $n > 12$. So some vertex has $\deg_{T_1}(v) + \deg_{T_2}(v) \ge 4$, and Lemma 2 gives $d(T_1, T_2) \le 2n - 10$. $\square$

**Smaller $n$.** The average of $\deg_{T_1}(v) + \deg_{T_2}(v)$ is $4 - 12/n$, so some vertex has degree sum at least $\lceil 4 - 12/n \rceil$. Lemma 2 then gives $d(T_1, T_2) \le 2n - 6 - \lceil 4 - 12/n \rceil$. The ceiling is 3 for $7 \le n \le 12$, 2 for $n = 5, 6$, and 1 for $n = 4$. $\square$

**The lower bound** is not proved here. Sleator, Tarjan and Thurston glue the triangulations along a flip sequence into a triangulated 3-dimensional polyhedron with $d$ tetrahedra, realize the polygon in hyperbolic space so that every tetrahedron has volume at most that of the regular ideal tetrahedron, and choose $T_1$, $T_2$ whose polyhedron has large volume. This gives $2n - 10$ for all large $n$. Pournin's proof works with the flip graph directly: it shows by induction on $n$ that a specific pair of triangulations has distance $2n - 10$, by contracting boundary edges of the polygon and counting how many flips each contraction can save.

## Consequences

- **Rotation distance.** Through the [dual tree](/triangulation-dual-tree/), triangulations of a convex $(m + 2)$-gon correspond to binary trees with $m$ internal nodes and flips to [rotations](/tree-rotation/). So any two binary trees with $m$ nodes are at most $2m - 6$ rotations apart for $m \ge 11$, and this is tight.
- **Associahedra.** The associahedron of dimension $n - 3$ has diameter $2n - 10$ for $n \ge 13$, linear in its dimension, much less than its $C_{n-2}$ vertices suggest.
- **Approximation.** Since $d \ge |T_1 \setminus T_2|$ and Lemma 2 gives $d \le 2(n - 3)$ on every piece between common diagonals, the number of differing diagonals is a 2-approximation of the flip distance in convex polygons.
- **Contrast with point sets.** For points in general position, not in convex position, flip distances can be $\Theta(n^2)$ (Hurtado, Noy and Urrutia), so the linear bound depends on convexity.

## Tightness

The constant $2n - 10$ is attained for every $n \ge 13$. Below 13 the diameter is not $2n - 10$. Breadth-first search over all triangulations gives:

| $n$ | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|
| triangulations | 2 | 5 | 14 | 42 | 132 | 429 | 1430 |
| diameter | 1 | 2 | 4 | 5 | 7 | 9 | 11 |
| bound $2n - 6 - \lceil 4 - 12/n \rceil$ | 1 | 2 | 4 | 5 | 7 | 9 | 11 |

The bound of the proof is attained for $4 \le n \le 10$. The values for $n = 11$ and $n = 12$ are 12 and 15 (to be checked), so the diameter equals $2n - 9$ at $n = 12$ and drops to $2n - 10$ only from $n = 13$ on. For $n = 6$, a pair at distance 4 is the triangulation with diagonals $v_1 v_5$, $v_2 v_4$, $v_2 v_5$ and the one with $v_0 v_3$, $v_0 v_4$, $v_1 v_3$, numbering the vertices $v_0, \ldots, v_5$.

## History

Culik and Wood (1982) observed the bound $2n - 6$ for rotation distance through fans. Sleator, Tarjan and Thurston (STOC 1986, journal 1988) proved the upper bound $2n - 10$ for $n \ge 13$ and, with hyperbolic volume, the matching lower bound for all $n$ beyond an unspecified threshold, and conjectured that the threshold is 13. Pournin settled the conjecture in 2014 with a purely combinatorial proof. The question had been studied in the language of rotations in binary search trees, motivated by splay trees.

## References
