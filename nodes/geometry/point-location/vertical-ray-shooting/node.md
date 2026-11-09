---
tag: FGATNS
kind: problem
slug: vertical-ray-shooting
name: Vertical ray shooting problem
aliases:
- vertical ray shooting
- vertical ray shooting query
- above-below query
area: geometry/point-location
level: advanced
summary: Find the first segment hit by a vertical ray shot upward or downward from a query point.
prereqs: [planar-subdivision, orientation-test]
see_also: [planar-point-location, trapezoidal-map, slab-method-point-location, sarnak-tarjan-point-location, seidel-point-location, sweep-line-technique, sweep-status-structure, crossing-number-algorithm]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 6, Sections 6.1 and 6.2 (the trapezoidal map, where each face is bounded by the segments directly above and below), and Section 6.3 (the shear transformation for vertical segments and equal x-coordinates)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, and the chapter on ray shooting and lines in space, by Marco Pellegrini (chapter number to be checked)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: the persistent sweep structure, which answers above and below queries (DOI to be checked)
  - paper: doi:10.1016/0925-7721(91)90012-4
    title: Raimund Seidel, A simple and fast incremental randomized algorithm for computing trapezoidal decompositions and for triangulating polygons, Computational Geometry 1(1), 1991
    locator: the trapezoidal decomposition and its query structure (DOI to be checked)
  - paper: doi:10.1007/BF01377183
    title: Bernard Chazelle, Herbert Edelsbrunner, Michelangelo Grigni, Leonidas Guibas, John Hershberger, Micha Sharir and Jack Snoeyink, Ray shooting in polygons using geodesic triangulations, Algorithmica 12, 1994
    locator: ray shooting in any direction inside a simple polygon in O(log n) time with O(n) space (DOI to be checked)
---

Vertical ray shooting asks, for a set of $n$ segments that do not cross and a query point $q$, which segment is hit first by the ray shot upward from $q$, and which by the ray shot downward. It is the form in which most planar point location structures answer: the face of $q$ in a [planar subdivision](/planar-subdivision/) is the face below the segment above $q$. The static problem takes $O(\log n)$ time per query after preprocessing in $O(n \log n)$ time and $O(n)$ space, and $\Omega(\log n)$ tests are needed in the algebraic decision tree model.

## In plain words

You stand at a point on a map full of straight walls that never cross. Look straight up: which wall do you see first? Look straight down: which wall do you see first? The two walls tell you which room you are in, since every room of the map lies between the walls just above and just below its points.

With the walls sorted from left to right and bottom to top in a good index, the question takes a few dozen small tests even with a million walls.

## Definition

**Notation.** $S$ is the set of segments and $P$ the set of their end points, $n = |S|$, $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. A query reports two segments, so $h = 2$. The predicate $\mathrm{incircle}$ is not used. Costs are on the [real RAM](/real-ram/).

**Input.** A set $S$ of $n$ closed segments in the plane such that two segments meet at most in a common end point.

**Query.** A point $q$. Let $\rho^+(q) = \{q + (0, t) : t > 0\}$ and $\rho^-(q) = \{q - (0, t) : t > 0\}$. The answer is the segment $s \in S$ that meets $\rho^+(q)$ at the smallest $t$ (the segment *above* $q$), or none, and the same for $\rho^-(q)$ (the segment *below* $q$). If $q$ lies on a segment or is an end point, report that instead.

**Degenerate cases.** A vertical segment can contain a part of the ray, and the ray can pass through an end point, so "the first segment" can be ambiguous: two segments with a common end point $v$ directly above $q$ are both hit at $v$. The pages on this site remove the ambiguity with the symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ for an infinitesimal $\varepsilon > 0$ (de Berg et al., Section 6.3). A vertical line of the sheared plane is the line $x + \varepsilon y = c$ of the original plane, so the ray up from $q$ leans infinitesimally to the left and the ray down leans infinitesimally to the right. Such a ray meets no end point other than $q$ and contains no part of a segment, so the answer is unique. In code, a segment $(a, b)$ with $a <_{\mathrm{lex}} b$ crosses the sheared vertical line of $q$ exactly when $a <_{\mathrm{lex}} q <_{\mathrm{lex}} b$, and $q$ is above it when $\mathrm{orient}(a, b, q) > 0$. If the ray up passes next to an end point $v$, it passes on the left of $v$, so it meets the segments that end at $v$, and of these the one with the largest slope is the lowest. The ray down passes on the right of $v$ and meets the segments that start at $v$, and of these the one with the largest slope is the highest. A vertical segment is never hit by the rays from a point on its line outside it. The reported segments still bound the correct face, since the shear changes no face.

**Costs.** As for [planar point location](/planar-point-location/): preprocessing time, space and query time, each worst case, expected or amortized.

## Variants

- **Planar point location.** The face version of the same question; see [planar point location](/planar-point-location/). Every vertical ray shooting structure gives a point location structure with $O(1)$ extra work per query, using the DCEL to read the face below the segment above.
- **Offline queries.** All $m$ query points are known in advance. A [sweep](/sweep-line-technique/) from left to right with a [balanced search tree](/sweep-status-structure/) of the active segments answers each query when the sweep line reaches it, in $O((n + m) \log n)$ total time and $O(n)$ space.
- **Crossing segments.** If segments may cross, the order of segments along a vertical line changes between crossings, and the sweep order is not one order. Ray shooting among arbitrary segments needs other tools, such as [segment trees](/segment-tree/) over the $x$-ranges, with polylogarithmic query time and near-linear or larger space; see the Handbook chapter on ray shooting.
- **Any direction.** Ray shooting in a direction given with the query. Inside a simple polygon with $n$ vertices, Chazelle et al. (1994) answer in $O(\log n)$ time with $O(n)$ space by geodesic triangulations.
- **Dynamic.** Segments are inserted and deleted. The structures for dynamic point location apply.
- **Orthogonal case.** All segments are horizontal. Then the query is a predecessor search among the segments whose $x$-range contains $q_x$, which an [interval tree](/interval-tree/) with sorted lists, or a persistent search tree, answers in $O(\log n)$.

## Examples

**Four segments.** Take $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$. For $q = (5, 3)$, the segments that cross the vertical line $x = 5$ are $s_0$, at $y = 2 \cdot 5 / 8 = 1.25$, $s_1$, at $y = 6 - (5 - 4) = 5$, and $s_3$, at $y = 8 - (5 - 2)/4 = 7.25$. So the ray up from $q$ hits $s_1$ at $(5, 5)$ and the ray down hits $s_0$ at $(5, 1.25)$. The orientation tests agree: $\mathrm{orient}((4,6), (8,2), (5,3)) = -8 < 0$, so $q$ is below $s_1$, and $\mathrm{orient}((0,0), (8,2), (5,3)) = 14 > 0$, so $q$ is above $s_0$.

**A query below a vertex.** For $q = (4, 2)$, the ray up passes through the end point $(4, 6)$ of $s_1$ and $s_2$. In the sheared order $(4,2) <_{\mathrm{lex}} (4,6)$, so the ray up passes on the left of $(4,6)$: $s_2$, which ends there, crosses the line of $q$, and $s_1$, which starts there, does not. The ray up hits $s_2$ and the ray down hits $s_0$. The query $(4, 7)$ is above $(4, 6)$, so its ray down passes on the right of $(4, 6)$: it hits $s_1$, and the ray up hits $s_3$.

**A vertical segment.** Add $s_4 = (9, 0)(9, 4)$. The query $(9, 2)$ is on $s_4$, and $(9, 4)$ is its end point. For $(9, 5)$ the ray down leans to the right and misses $s_4$, so no segment is below $(9, 5)$ and $s_3$ is above. For $(9, -1)$ the ray up leans to the left and also misses $s_4$, so $s_3$ is the segment above. In both cases the face is the unbounded face, as it is without the shear. The test files of the [slab method](/slab-method-point-location/) and the [trapezoidal map](/trapezoidal-map/) check such cases against a linear scan with the same convention.

## Known algorithms

| method | preprocessing | space | query |
|---|---|---|---|
| linear scan | none | $O(n)$ W | $O(n)$ W |
| [slab method](/slab-method-point-location/) | $O(n^2)$ W | $\Theta(n^2)$ W | $O(\log n)$ W |
| [persistent search tree](/sarnak-tarjan-point-location/) (Sarnak and Tarjan 1986) | $O(n \log n)$ W | $O(n)$ W | $O(\log n)$ W |
| [trapezoidal map](/trapezoidal-map/) by randomized incremental construction ([Seidel 1991](/seidel-point-location/)) | $O(n \log n)$ E | $O(n)$ E | $O(\log n)$ E, $O(\log n)$ W after rebuilding |
| [chain method](/chazelle-monotone-point-location/) after regularization | $O(n \log n)$ W | $O(n)$ W | $O(\log n)$ W with fractional cascading |
| offline sweep for $m$ queries | together $O((n + m) \log (n + m))$ W | $O(n + m)$ W | |

W means worst case and E expected over the random order, for every input and every fixed query point. All of the online methods return the segments above and below $q$ directly. [Kirkpatrick's method](/kirkpatrick-point-location/) returns a triangle of a triangulation, which answers point location but not vertical ray shooting, unless the triangulation refines the trapezoidal map.

## Bounds

**Lower bound.** Take $n$ horizontal segments $[0, 1] \times \{i\}$ for $i = 1, \ldots, n$. The open regions between consecutive segments over $0 < x < 1$, and the two regions above the top segment and below the bottom one, give $n + 1$ different answers, each on a set of positive area. In the [algebraic decision tree](/algebraic-decision-tree/) model with tests of nonzero polynomials in $(q_x, q_y)$, the points that ever take an "equal to zero" branch form a set of area zero, so these $n + 1$ answers need $n + 1$ leaves reached by paths of strict branches only, and the depth is at least $\lceil \log_2 (n + 1) \rceil$. This holds for any preprocessing and any space. So the $O(\log n)$ query time of the methods above is optimal.

**Upper bound.** The persistent search tree and the deterministic chain method give $O(\log n)$ query time, $O(n)$ space and $O(n \log n)$ preprocessing in the worst case. The offline sweep answers $m$ queries in $O((n + m) \log (n + m))$ total time, which matches the lower bound of $\Omega(m \log n)$ for $m$ queries that follows from the bound above.

## Reductions

**Point location to vertical ray shooting.** If the subdivision is stored as a DCEL, the face of $q$ is the face of the half-edge of the segment above $q$ that has the face below it on its left. If no segment is above, the face is the one above the segment below, and if neither exists the face is unbounded.

**Point in polygon.** For a simple polygon, $q$ is inside if and only if the number of edges that the ray up from $q$ crosses is odd; this is the [crossing number test](/crossing-number-algorithm/). Vertical ray shooting finds only the first edge: $q$ is inside exactly when the first edge above $q$ has the inside below it, which one orientation of that edge tells.

**Trapezoidal map.** The trapezoidal map of $S$ is defined by vertical ray shooting from every end point: each end point shoots up and down, and the two segments hit bound the vertical extensions. A sweep computes all $2n$ answers in $O(n \log n)$ time.

## Applications

- [Planar point location](/planar-point-location/) and all its applications.
- The [trapezoidal map](/trapezoidal-map/) and the triangulation of polygons through trapezoidal decompositions, as in [Seidel's polygon triangulation](/seidel-polygon-triangulation/).
- Map overlay and Boolean operations of polygons, to find the face of one map that contains a component of the other.
- Visibility from a point in a fixed direction, such as hidden-line computations in a scene of opaque segments.

## References
