---
tag: KVYDDR
kind: algorithm
slug: kirkpatrick-point-location
name: Kirkpatrick's point location
aliases:
- Kirkpatrick hierarchy
- triangulation hierarchy point location
- triangulation refinement method
area: geometry/point-location
level: advanced
summary: Build a hierarchy of triangulations, each a constant fraction smaller, and locate the point by descending it.
solves: [planar-point-location]
model: real-ram
complexity:
  vars: {n: the number of vertices of the triangulation}
  time: {build: O(n) worst case, query: O(log n) worst case}
  space: {extra: O(n) worst case}
properties: {online: false, deterministic: true, recursive: false, static: true}
history:
  year: 1983
  people: [David G. Kirkpatrick]
  note: Kirkpatrick published the triangulation hierarchy in the SIAM Journal on Computing in 1983, as an optimal point location method with O(log n) query time, O(n) space and a simple construction.
prereqs: [planar-point-location, triangulation, independent-set, euler-formula, ear-clipping, orientation-test]
see_also: [slab-method-point-location, sarnak-tarjan-point-location, trapezoidal-map, seidel-point-location, chazelle-monotone-point-location, triangle-walk-point-location, lipton-tarjan-separator, planar-graph]
sources:
  - paper: doi:10.1137/0212002
    title: David G. Kirkpatrick, Optimal search in planar subdivisions, SIAM Journal on Computing 12(1), 1983
    locator: the whole paper (DOI to be checked)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Section 2.2.2.3, the triangulation refinement method (section number to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.2
---

Kirkpatrick's method answers [planar point location](/planar-point-location/) queries in a [triangulation](/triangulation/). It removes an [independent set](/independent-set/) of vertices of small degree, fills each hole with new triangles, and repeats until one triangle is left. Each round removes a constant fraction of the vertices, so there are $O(\log n)$ levels, and each new triangle overlaps only a constant number of triangles of the level below. A query starts at the single top triangle and walks down, testing a constant number of children per level. The query takes $O(\log n)$ time in the worst case, and the structure takes $O(n)$ space and $O(n)$ time to build from the triangulation.

## In plain words

Picture a map cut into small triangles. Make a coarser copy of it: pick many corners that have few triangles around them and that are not next to each other, erase them, and fill each gap with a few larger triangles. Every large triangle remembers the small triangles under it. Do this again and again until one huge triangle covers everything.

To find a point, start with the huge triangle. Look at the few triangles under it and step into the one that contains the point. Repeat on each copy until you reach the original map. Each copy is smaller than the one before by a fixed share, so the number of copies grows slowly with the size of the map, and each step looks at only a handful of triangles.

## The problem

**Notation.** $n$ is the number of vertices of the triangulation, including the three outer corners $A$, $B$, $C$. $T_0$ is the input triangulation, $T_r$ the triangulation after $r$ rounds, $N_r$ its number of vertices, and $R$ the number of rounds (the depth). The degree $\deg(v)$ of an inner vertex is its number of neighbors, which equals the number of triangles around it. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$: positive when $p, q, r$ turn counterclockwise. A point $q$ is in the closed triangle $abc$, given counterclockwise, if all three of $\mathrm{orient}(a, b, q)$, $\mathrm{orient}(b, c, q)$, $\mathrm{orient}(c, a, q)$ are at least $0$. The output size of a query is $1$. Costs are on the [real RAM](/real-ram/).

The input is a triangle $ABC$ and a set of triangles with integer or rational vertices that tile it edge to edge: every two triangles meet in a common edge, a common vertex, or not at all, and every vertex other than $A$, $B$, $C$ lies strictly inside $ABC$. A query point $q$ gets one of four answers: the vertex $q$, the edge whose relative interior contains $q$, the input triangle whose interior contains $q$, or "outside".

A general [planar subdivision](/planar-subdivision/) with $n$ segments is first put inside a large triangle, and its faces are triangulated as [polygons with holes](/polygon-with-holes-triangulation/) in $O(n \log n)$ time. The triangulation has $O(n)$ vertices, and each triangle records the face it lies in, so the triangle answer gives the face.

**Degenerate input.** The method uses no vertical direction, so vertical edges and equal $x$-coordinates need no care and no symbolic shear is used. Three vertices of the input may be collinear, so a vertex can have a straight angle, and a hole can be a nonconvex polygon with collinear vertices on its boundary. The ear clipping of line L4 accepts an ear only if it turns strictly left and its closed triangle holds no other vertex of the hole, which handles both cases. A query point on an edge or a vertex is in several closed triangles. The descent may take any of them, since each one gives the same vertex or edge answer.

## The algorithm

```pseudo id=main
KIRKPATRICK-BUILD(T)
L1  while the current triangulation has more than one triangle do
L2      I ← ∅; for each inner vertex v in a fixed order: if deg(v) ≤ 8 and no neighbor of v is in I then add v to I
L3      for each v in I do
L4          delete v and the triangles around it; triangulate the hole by ear clipping
L5          each new triangle t gets as children the deleted triangles whose interiors meet the interior of t
KIRKPATRICK-QUERY(q)
L6  t ← the top triangle ABC; if q is not in the closed triangle t then return "outside"
L7  while t has children do
L8      t ← the first child of t whose closed triangle contains q
L9  return the vertex, the edge or the input triangle of t that contains q
```

- **Line L2** picks a maximal independent set among the inner vertices of degree at most $8$, greedily. The corners $A$, $B$, $C$ are never picked. The degree of each vertex is the size of its list of triangles, so the scan costs $O(N_r)$. The code scans the vertices in lexicographic order, which makes the hierarchy repeatable. It sorts once, in $O(n \log n)$ time, and filters the list in each round; any fixed order, such as the input order, gives the linear build.
- **Line L4.** The triangles around $v$ form a star whose outer boundary, the link of $v$, is a simple polygon with $\deg(v) \le 8$ vertices. Ear clipping triangulates it with $\deg(v) - 2$ triangles in $O(1)$ time, since the degree is bounded. Two vertices of $I$ are not adjacent, so their stars share no triangle and the holes are disjoint.
- **Line L5.** The new triangles cover exactly the old star, so each one is covered by the old triangles it overlaps, and it has at most $8$ children. The overlap test is the separating axis test for two triangles: their interiors are disjoint if and only if some edge line of one of them has the other triangle on its closed outer side.
- **Lines L6 to L8.** The invariant is "$q$ lies in the closed triangle $t$". The children of $t$ cover it, so some child contains $q$. A triangle that survives a round is the same record in both levels, so it has no new children there, and the descent continues through it.
- **Line L9.** When $t$ has no children, it is an input triangle that contains $q$. If $q$ is a corner of $t$, the answer is that vertex; if $q$ is on the line of an edge of $t$, it is on that edge; otherwise $q$ is in the open triangle $t$.

## Example

The outer triangle is $A = (0,0)$, $B = (12,0)$, $C = (0,12)$, and the inner vertices $(3,3)$, $(6,2)$, $(2,6)$, $(4,4)$ are inserted one after the other by splitting the triangle that contains them. This gives $9$ triangles, as $2n - 5 = 9$ for $n = 7$. Among them are triangle $1 = (6,2)(3,3)(0,0)$ and triangle $2 = (12,0)(0,12)(6,2)$.

| round | vertices removed | their degrees | triangles before | triangles after |
|---|---|---|---|---|
| 1 | $(2,6)$, $(6,2)$ | $4$, $5$ | $9$ | $5$ |
| 2 | $(3,3)$ | $4$ | $5$ | $3$ |
| 3 | $(4,4)$ | $3$ | $3$ | $1$ |

In round 1, the scan meets $(2,6)$ first. Its neighbors $(0,0)$, $(0,12)$, $(3,3)$, $(4,4)$ are blocked, so $(3,3)$ and $(4,4)$ wait, and $(6,2)$, not adjacent to $(2,6)$, is taken too. The level sizes are $9, 5, 3, 1$, and the hierarchy has $17$ triangle records, since triangle $(12,0)(0,12)(4,4)$ of level 1 survives into level 2.

The query $q = (4, 2)$ descends as follows.

| level | triangle $t$ | children tested | test results |
|---|---|---|---|
| 3 | $(0,0)(12,0)(0,12)$ | $(0,0)(4,4)(0,12)$, $(0,0)(12,0)(4,4)$ | no, yes |
| 2 | $(0,0)(12,0)(4,4)$ | $(3,3)(0,0)(12,0)$ | yes |
| 1 | $(3,3)(0,0)(12,0)$ | $(6,2)(3,3)(0,0)$ | yes |
| 0 | $(6,2)(3,3)(0,0)$ | none | |

The query makes $4$ child tests and returns triangle $1$. The query $(1, 1)$ returns the edge from $(0,0)$ to $(3,3)$, and $(5, 5)$ returns triangle $2$.

## Correctness

**Theorem.** For every triangulation of a triangle $ABC$ and every point $q$, KIRKPATRICK-BUILD terminates, and KIRKPATRICK-QUERY returns "outside" if $q \notin ABC$; otherwise the vertex $q$ if $q$ is a vertex; otherwise the edge that contains $q$ in its relative interior, if there is one; otherwise the input triangle whose interior contains $q$.

The proof has three parts. Each level is again a triangulation of $ABC$, since a hole is a simple polygon and ear clipping triangulates it without new vertices. Each round removes at least one vertex while more than one triangle is left, because a triangulation always has an inner vertex of degree at most $8$ (by [Euler's formula](/euler-formula/)), so the loop ends with the single triangle $ABC$. Finally, the children of a new triangle cover it, so the descent keeps $q$ inside the current closed triangle down to level $0$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Degrees.** A triangulation of a triangle with $N$ vertices has $3N - 6$ edges and $2N - 5$ triangles, so the degrees sum to $6N - 12$. The three corners have degree at least $2$ each, so the inner degrees sum to at most $6N - 18$. Every inner vertex has degree at least $3$, so at most $(N - 3)/2$ inner vertices have degree $9$ or more, and at least $(N - 3)/2$ have degree at most $8$.
- **Rounds.** Each vertex picked in line L2 blocks itself and at most $8$ neighbors, and every skipped low-degree inner vertex is blocked. So each round removes at least $(N_r - 3)/18$ vertices, $N_{r+1} - 3 \le \frac{17}{18}(N_r - 3)$, and the depth is $R \le \log_{18/17}(n - 3) + 1 = O(\log n)$.
- **Space.** Level $r$ has $2N_r - 5$ triangles, and the sum over all levels is at most $36(n - 3) + R + 1$. Each triangle has at most $8$ children, so the space is $O(n)$ in the worst case.
- **Build time.** Round $r$ costs $O(N_r)$ for the scan of line L2 and $O(1)$ per removed vertex for lines L4 and L5. The sum of $N_r$ is a geometric series, so the build takes $O(n)$ time in the worst case, given the triangulation.
- **Query time.** Each level costs at most $8$ triangle tests, each of three orientation tests, so a query takes $O(\log n)$ time in the worst case. This is optimal in the [algebraic decision tree](/algebraic-decision-tree/) model; see [planar point location](/planar-point-location/).

The full proofs are in [the complexity proof](proofs/complexity/). With integer coordinates of absolute value at most $M$, every orientation determinant has absolute value at most $8M^2$, so the predicates are exact in Python integers.

## Properties

- **Deterministic and worst case.** All three bounds hold for every input, with no randomization and no amortization.
- **Static.** The hierarchy is built once for a fixed triangulation.
- **Exact.** The only predicate is the orientation test, exact on integers or `fractions.Fraction`.
- **Large constants.** The bound $\log_{18/17} n$ is about $12 \log_2 n$, and each level may cost up to $8$ triangle tests. On random triangulations, rounds remove about $40\%$ of the vertices, much more than the $1/18$ of the proof, so the depth is about $1.4 \log_2 n$ to $1.5 \log_2 n$.

## Variants and improvements

- **Degree bound.** Any fixed degree bound of at least $6$ gives a constant fraction of low-degree vertices by the same count. A larger bound removes more vertices per round but gives more children per triangle. The constants on this page are not those of Kirkpatrick's paper.
- **Point location in a hierarchy of Delaunay triangulations.** Devillers's Delaunay hierarchy samples vertices at random instead of picking an independent set, and walks within each level; see [triangle walk](/triangle-walk-point-location/).
- **Polytope hierarchies.** Dobkin and Kirkpatrick apply the same idea to convex polytopes in three dimensions, removing an independent set of low-degree vertices and taking the convex hull, which gives $O(\log n)$ extreme point and intersection queries.
- **Other optimal methods.** The [planar separator](/lipton-tarjan-separator/) method of Lipton and Tarjan came first. The [persistent slabs](/sarnak-tarjan-point-location/) of Sarnak and Tarjan and the chain method with fractional cascading of [Edelsbrunner, Guibas and Stolfi](/chazelle-monotone-point-location/) reach the same bounds with smaller constants, and the [randomized trapezoidal map](/seidel-point-location/) is the simplest in practice.

## When to use it

Use Kirkpatrick's method when the input is already a triangulation, when worst-case guarantees matter, and when the idea of a hierarchy is needed elsewhere, as in the three-dimensional polytope version. For plain point location in a planar map, the [trapezoidal map](/trapezoidal-map/) and [Sarnak and Tarjan's](/sarnak-tarjan-point-location/) persistent slabs are usually faster, with smaller structures.

## Pitfalls

- **Removing an outer corner.** The corners $A$, $B$, $C$ must stay, or the last level is not a triangle that covers the whole input.
- **Adjacent vertices in one round.** If two removed vertices are adjacent, their stars share triangles and the holes overlap. Line L2 blocks all neighbors of each picked vertex.
- **Nonconvex holes.** The link of a vertex is star-shaped but often not convex, so a fan triangulation from one link vertex can leave the hole. Use ear clipping or another triangulation of simple polygons.
- **Collinear link vertices.** An ear test with $\mathrm{orient} \ge 0$ accepts a flat triangle. Require $\mathrm{orient} > 0$ and an empty closed triangle.
- **Children that only touch.** A deleted triangle that meets a new triangle only along an edge or at a vertex is not needed as a child. It does no harm to correctness, but it raises the number of tests per level.
- **Open triangle tests in the descent.** A point on an edge is in no open triangle. Test closed triangles in line L8, or the descent stops with no child.

## Implementations

## History

David Kirkpatrick introduced the triangulation hierarchy in his 1983 paper "Optimal search in planar subdivisions" in the SIAM Journal on Computing. Lipton and Tarjan had shown in 1977 that $O(\log n)$ query time and $O(n)$ space are possible, with the planar separator theorem, but their method was too complicated to use. Kirkpatrick's method was the first simple optimal one. Dobkin and Kirkpatrick used the same hierarchy for convex polytopes in three dimensions, and the idea of a sequence of coarser approximations with bounded overlap reappears in many later structures.

## References
