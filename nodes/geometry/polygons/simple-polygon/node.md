---
tag: 94Y8NQ
kind: definition
slug: simple-polygon
name: Simple polygon
aliases:
- non-self-intersecting polygon
- Jordan polygon
- simple closed polygon
area: geometry/polygons
level: intro
summary: A polygon whose edges meet only at shared endpoints of consecutive edges.
prereqs: [polygon, jordan-curve-theorem]
see_also: [polygon-simplicity-test, convex-polygon, polygon-with-holes, polygon-triangulation, two-ears-theorem, point-in-polygon, polygon-orientation, monotone-polygon]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1, Theorem 3.1 (every simple polygon has a triangulation, with n − 2 triangles) and its proof by a diagonal from the leftmost vertex
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Sections 1.1 and 1.2, the definition of a simple polygon, the existence of a diagonal, and the sum of the interior angles
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1, Section 1.3, the definitions of a polygon, a simple polygon and a convex polygon
---

A simple polygon is a [polygon](/polygon/) whose boundary never touches or crosses itself: two edges meet only when they are consecutive, and then only at their shared vertex. Its boundary is then a closed curve without self-intersections, so by the [Jordan curve theorem](/jordan-curve-theorem/) it splits the plane into a bounded inside and an unbounded outside. Most polygon algorithms, among them [triangulation](/polygon-triangulation/), [point in polygon](/point-in-polygon/) by crossing parity, and [area](/polygon-area/) by the shoelace formula, assume this, and the [simplicity test](/polygon-simplicity-test/) checks it in $O(n \log n)$ time.

## Definition

Let $P = (v_0, \ldots, v_{n-1})$ be a polygon with edges $e_i = v_i v_{i+1}$, indices mod $n$. $P$ is **simple** if

1. $n \ge 3$ and the vertices $v_0, \ldots, v_{n-1}$ are pairwise distinct;
2. each two consecutive edges meet only at their shared vertex: $e_{i-1} \cap e_i = \{v_i\}$;
3. each two edges that are not consecutive are disjoint: $e_i \cap e_j = \emptyset$ when $j \notin \{i - 1, i, i + 1\}$.

Equivalently, the closed path through $v_0, v_1, \ldots, v_{n-1}, v_0$ is injective except at its common start and end point, so $\partial P$ is a **Jordan curve**, the image of a circle under a continuous injective map. The Jordan curve theorem, which for polygons has an elementary proof by the parity of ray crossings, gives a bounded open set $\operatorname{int} P$ and an unbounded open set $\operatorname{ext} P$ with $\mathbb{R}^2 \setminus \partial P = \operatorname{int} P \cup \operatorname{ext} P$, each with boundary $\partial P$. The **region** of $P$ is the compact set $\operatorname{int} P \cup \partial P$, and the word *polygon* often means this region.

**Orientation and turns.** The vertices of a simple polygon are in **counterclockwise** order when $\operatorname{int} P$ lies to the left of every directed edge, and in clockwise order otherwise; the sign of the [shoelace formula](/shoelace-formula/) tells which ([polygon orientation](/polygon-orientation/)). The **interior angle** at $v_i$ is the angle of the region at $v_i$, between $0$ and $2\pi$. A vertex is **convex** if its interior angle is less than $\pi$ and **reflex** if it is more than $\pi$. In counterclockwise order, a convex vertex is a left turn, $\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) > 0$, and a reflex vertex is a right turn.

A **diagonal** is a segment $v_i v_j$ between two vertices that lies in the region and meets $\partial P$ only at $v_i$ and $v_j$.

**Theorem 1.** Every simple polygon with $n \ge 4$ vertices has a diagonal.

*Proof.* Let $v$ be the lexicographically smallest vertex (smallest $x$, then smallest $y$), with neighbors $u$ and $w$. All of the region lies in $\{x > v_x\} \cup \{x = v_x, y \ge v_y\}$, so the interior angle at $v$ is less than $\pi$ and $u$, $v$, $w$ are not collinear. If no vertex other than $u, v, w$ lies in the closed triangle $uvw$, then no edge can enter the triangle: it would have to cross the edges $uv$ or $vw$ of $P$, or end inside. So $uw$ meets $\partial P$ only at $u$ and $w$, and it lies in the region because the triangle near $v$ does; it is a diagonal. Otherwise, among the vertices in the triangle other than $u, v, w$, take a vertex $x$ farthest from the line $uw$. The triangle cut off by the parallel to $uw$ through $x$, on the side of $v$, contains no vertex in its interior, and the same argument shows that $vx$ is a diagonal. $\square$

**Theorem 2.** A simple polygon with $n$ vertices can be cut by $n - 3$ diagonals into $n - 2$ triangles, and the sum of its interior angles is $(n - 2)\pi$.

*Proof.* By induction on $n$. A triangle has one triangle, no diagonal, and angle sum $\pi$. For $n \ge 4$, a diagonal $v_i v_j$ from Theorem 1 splits $P$ into two simple polygons $(v_i, \ldots, v_j)$ and $(v_j, \ldots, v_i)$ with $n_1$ and $n_2$ vertices, $n_1, n_2 < n$ and $n_1 + n_2 = n + 2$. By the hypothesis they have $(n_1 - 2) + (n_2 - 2) = n - 2$ triangles and $(n_1 - 3) + (n_2 - 3) + 1 = n - 3$ diagonals together with the splitting one. The interior angles of $P$ at $v_i$ and $v_j$ are the sums of the angles of the two parts there, so the angle sum is $(n_1 - 2)\pi + (n_2 - 2)\pi = (n - 2)\pi$. $\square$

**Corollary.** A simple polygon has at most $n - 3$ reflex vertices, so at least three convex ones. *Proof.* With $r$ reflex vertices, the angle sum is more than $r\pi$, so $(n - 2)\pi > r\pi$. $\square$

**Degenerate input.** Condition 2 allows a vertex where the boundary goes straight on, with interior angle exactly $\pi$; such a vertex is neither convex nor reflex, and many programs remove it first. Condition 1 forbids a vertex visited twice, so a figure eight that touches itself at a vertex is not simple.

## Examples and non-examples

- **Convex polygons.** Every triangle with non-collinear vertices, every square, and every [convex polygon](/convex-polygon/) is simple.
- **A concave polygon.** $(0,0), (6,0), (6,4), (3,1), (0,4)$ is simple, with one reflex vertex $(3,1)$. Its interior angles add up to $3\pi$, and the diagonals $(6,0)$-$(3,1)$ and $(3,1)$-$(0,0)$ cut it into three triangles.
- **A notch on one line.** $(0,0), (3,0), (3,3), (0,3), (0,2), (1,2), (1,1), (0,1)$ is simple: the edges $(0,3)$-$(0,2)$ and $(0,1)$-$(0,0)$ lie on one line but do not meet.
- **Non-example: a bowtie.** $(0,0), (2,2), (2,0), (0,2)$ is not simple: $e_0$ and $e_2$ cross at $(1,1)$.
- **Non-example: a vertex on an edge.** $(0,0), (4,0), (4,4), (2,0), (0,4)$ is not simple: $v_3 = (2,0)$ lies on $e_0$, so two non-consecutive edges touch without crossing.
- **Non-example: a fold.** $(0,0), (4,0), (2,0), (2,3)$ is not simple: consecutive edges overlap along $(2,0)$-$(4,0)$.
- **Non-example: a repeated vertex.** $(0,0), (4,0), (4,4), (0,0), (0,4)$ passes through $(0,0)$ twice; its boundary is a figure eight.

## Related definitions

- **[Polygon](/polygon/).** The general closed chain, with no condition on crossings.
- **[Convex polygon](/convex-polygon/), [monotone polygon](/monotone-polygon/), [star-shaped polygon](/star-shaped-polygon/) and [rectilinear polygon](/rectilinear-polygon/).** Special simple polygons.
- **[Polygon with holes](/polygon-with-holes/).** An outer simple polygon minus the insides of disjoint inner simple polygons.
- **Weakly simple polygon.** A polygon that may touch itself but can be made simple by an arbitrarily small perturbation, such as a polygon with a slit; clipping often produces these.
- **[Two ears theorem](/two-ears-theorem/).** Every simple polygon with $n \ge 4$ vertices has two non-overlapping ears, a strengthening of Theorem 1 used by [ear clipping](/ear-clipping/).
- **[Polygon simplicity test](/polygon-simplicity-test/).** The problem of checking the definition for a given vertex list.

## References
