---
tag: Z9P5VW
kind: definition
slug: planar-subdivision
name: Planar subdivision
aliases:
- planar map
- polygonal subdivision
- planar straight-line graph
- PSLG
area: geometry/point-location
level: intro
summary: A partition of the plane into vertices, edges and faces, the input structure for point location.
prereqs: [planar-graph, polygon]
see_also: [doubly-connected-edge-list, euler-formula, planar-edge-bound, planar-face-finding, quad-edge-data-structure, planar-point-location, monotone-subdivision, trapezoidal-map]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.2 (the doubly-connected edge list and its records) and Section 2.3 (computing the overlay, the faces from the boundary cycles and the graph of boundary components)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1, Section 1.2.3 (the DCEL), and Chapter 2, Section 2.2 (planar subdivisions as the input of point location), to be checked
  - paper: doi:10.1016/0304-3975(78)90051-8
    title: David E. Muller and Franco P. Preparata, Finding the intersection of two convex polyhedra, Theoretical Computer Science 7(2), 1978
    locator: the doubly connected edge list (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 38, Point location, by Jack Snoeyink, Section 38.1 (subdivisions and their representation)
---

## Definition

**Notation.** $P$ is the set of vertices, $n$ the size of the subdivision (the number of vertices, edges and faces together), $p = (x, y)$ a point, and $d = 2$. $\mathrm{orient}(p, q, r)$ is the sign of $(q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$, positive when $p, q, r$ turn counterclockwise. The output size $h$ and the predicate $\mathrm{incircle}$ are not used on this page.

**Planar straight-line graph.** A *planar straight-line graph* (PSLG) is a pair $(V, E)$ of a finite set $V$ of points of the plane and a finite set $E$ of closed segments with end points in $V$, such that two segments of $E$ meet at most in a common end point, and no point of $V$ lies in the relative interior of a segment of $E$.

**Planar subdivision.** The *planar subdivision* of a PSLG is the partition of the plane into three kinds of pieces:

- the *vertices*, the points of $V$;
- the *edges*, the relative interiors of the segments of $E$ (open segments);
- the *faces*, the connected components of $\mathbb{R}^2 \setminus \bigcup E \setminus V$.

These pieces are pairwise disjoint and cover the plane. Exactly one face is unbounded; the others are bounded open sets. A face $f$ and an edge or a vertex $e$ are *incident* if $e$ is in the closure of $f$. Two faces are *adjacent* if they are incident to a common edge. An edge is incident to one or two faces: one when the same face lies on both sides, as for an edge that hangs into a face.

The *boundary* of a face is its closure minus the face. It is a union of edges and vertices, and it splits into *boundary components*, the connected components of the boundary. A bounded face has exactly one *outer* boundary component, the one that meets the unbounded component of the complement of the face; all other components are *inner* (holes). The unbounded face has only inner components.

**Combinatorial size (Euler's formula).** Let a PSLG have $V$ vertices, $E$ edges, $F$ faces (the unbounded face included) and $C$ connected components (an isolated vertex is a component). Then

$$V - E + F = 1 + C.$$

For a connected graph ($C = 1$) this is [Euler's formula](/euler-formula/) $V - E + F = 2$, which holds for every finite connected plane graph. The general form follows by adding $C - 1$ edges that connect the components inside common faces: each new edge joins two components and keeps the face count, so $V - (E + C - 1) + F = 2$. If $V \ge 3$, then $E \le 3V - 6$ and $F \le 2V - 4$ ([the planar edge bound](/planar-edge-bound/)), since a PSLG has no loops and no parallel edges. So a subdivision with $V$ vertices has size $n = O(V)$, and "the size of the subdivision" can be measured by any of $V$, $E$ or $V + E + F$ up to a constant factor.

**Doubly connected edge list.** A [doubly connected edge list](/doubly-connected-edge-list/) (DCEL), due to Muller and Preparata, stores a subdivision by its *half-edges*. Each segment $\{a, b\}$ of $E$ gives two half-edges, $a \to b$ and $b \to a$, which are *twins*. The face of a half-edge is the face on its left. The records are:

- for each vertex $v$, its coordinates and one half-edge with origin $v$;
- for each half-edge $e$, its origin, its twin, the next and the previous half-edge on the boundary of its face, and its face;
- for each face, one half-edge of its outer boundary component (none for the unbounded face) and one half-edge of each inner component.

The pointers must satisfy these invariants for every half-edge $e$:

1. $\mathrm{twin}(e) \ne e$ and $\mathrm{twin}(\mathrm{twin}(e)) = e$;
2. $\mathrm{origin}(\mathrm{next}(e)) = \mathrm{origin}(\mathrm{twin}(e))$, the head of $e$;
3. $\mathrm{prev}(\mathrm{next}(e)) = e$ and $\mathrm{next}(\mathrm{prev}(e)) = e$;
4. $\mathrm{face}(\mathrm{next}(e)) = \mathrm{face}(e)$;
5. $\mathrm{next}(e)$ is the half-edge leaving the head $v$ of $e$ that comes first in clockwise order after $\mathrm{twin}(e)$ around $v$.

Rule 5 is what makes the cycles of $\mathrm{next}$ the boundary components: when you walk along $e$ with the face on your left, the boundary turns at $v$ to the leftmost possible edge as seen from the face, which is the first one clockwise from the edge you came along. With rule 5, the cycle of the outer component of a bounded face runs counterclockwise (its signed area is positive), and the cycle of an inner component runs clockwise or has area zero (a tree of edges). This is how a DCEL is built from a list of segments: sort the outgoing half-edges of each vertex by angle with exact $\mathrm{orient}$ tests, set $\mathrm{next}$ by rule 5, trace the cycles, make one face for each cycle of positive area plus the unbounded face, and attach each other cycle to the face that contains it. To find that face, shoot a vertical ray up from the lexicographically smallest vertex of the component: the face below the first segment hit is the one, and if no segment is hit it is the unbounded face. Under the symbolic shear $(x, y) \mapsto (x + \varepsilon y, y)$ the ray never passes through a vertex. In a connected subdivision every cycle of area at most zero is the outer boundary of the whole graph, so this last step is needed only when $C > 1$.

## Examples and non-examples

**A triangle and a free segment.** Take the four segments $s_0 = (0,0)(8,2)$, $s_1 = (4,6)(8,2)$, $s_2 = (0,0)(4,6)$ and $s_3 = (2,8)(10,6)$, the running example of the [slab method](/slab-method-point-location/). There are $V = 5$ vertices, $E = 4$ edges, $C = 2$ components (the triangle and $s_3$), and $F = 2$ faces: the inside of the triangle and the unbounded face. Euler's formula gives $5 - 4 + 2 = 3 = 1 + 2$. Number the half-edges so that $2i$ runs from the lexicographically smaller end point of $s_i$ to the larger one and $2i + 1$ runs back. Rule 5 gives these $\mathrm{next}$ pointers, computed by the DCEL builder of the slab method implementation:

| half-edge | from | to | next | face |
|---|---|---|---|---|
| 0 | (0,0) | (8,2) | 3 | 1 |
| 1 | (8,2) | (0,0) | 4 | 0 |
| 2 | (4,6) | (8,2) | 1 | 0 |
| 3 | (8,2) | (4,6) | 5 | 1 |
| 4 | (0,0) | (4,6) | 2 | 0 |
| 5 | (4,6) | (0,0) | 0 | 1 |
| 6 | (2,8) | (10,6) | 7 | 0 |
| 7 | (10,6) | (2,8) | 6 | 0 |

There are three cycles. The cycle $0 \to 3 \to 5$ runs counterclockwise around the triangle ($\mathrm{orient}((0,0),(8,2),(4,6)) > 0$, twice the area is $40$) and is the outer component of face 1. The cycle $1 \to 4 \to 2$ runs clockwise and is an inner component of the unbounded face 0. The cycle $6 \to 7$ has area zero: it is the free segment $s_3$, also an inner component of face 0, since no segment lies above its smaller end point $(2,8)$. In general the number of cycles is $(F - 1) + C$ when there are no isolated vertices: one outer cycle for each bounded face and one cycle around each component. Here $1 + 2 = 3$.

**A face with a hole.** The square with corners $(0,0), (6,0), (6,6), (0,6)$ and the triangle $(2,2), (4,2), (3,4)$ inside it give $V = 7$, $E = 7$, $C = 2$ and $F = 3$: the unbounded face, the ring between the square and the triangle, and the inside of the triangle. Euler gives $7 - 7 + 3 = 3$. The ring is a face with an outer component (the square, counterclockwise) and one inner component (the triangle, traced clockwise by the half-edges that have the ring on their left). The vertical ray up from $(2,2)$ first meets the top side of the square, and the face below that side is the ring, so the clockwise triangle cycle is attached to the ring. A face is in general not simply connected, so a face record needs a list of inner components, not a single boundary.

**A tree.** A star of three segments from $(0,0)$ to $(2,0)$, $(0,2)$ and $(-2,-2)$ has $V = 4$, $E = 3$, $C = 1$ and one face. Its six half-edges form one cycle of area zero, and every edge has the unbounded face on both sides. Edges with the same face on both sides are allowed.

**Non-examples.** Two segments that cross at a point that is not an end point of both do not form a PSLG: the crossing point must be added as a vertex and both segments split first, as the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) does when it computes an overlay. A vertex in the relative interior of a segment is also not allowed; split the segment at it. Curved edges are outside this definition. The trapezoidal map and the slab method extend to edges that are $x$-monotone arcs, given constant-time predicates for the arcs.

**A pitfall in DCEL construction.** If you set $\mathrm{next}(e)$ to the first half-edge *counterclockwise* after $\mathrm{twin}(e)$, the cycles run the other way, and the face of each half-edge is the one on its right. Both conventions are consistent, but the area signs of the outer and inner cycles swap, so the rule for which cycles make faces must change with it. Mixing the two conventions gives faces whose cycles cross from one face into the next.

## Related definitions

A [planar graph](/planar-graph/) is a graph that has some crossing-free drawing; a PSLG fixes the drawing with straight edges. By Fáry's theorem every simple planar graph has a [straight-line drawing](/planar-straight-line-drawing/), so the combinatorial bounds are the same. The [faces](/planar-face/) of a plane graph and the [planar dual](/planar-dual-graph/) are defined for any embedding; [face finding](/planar-face-finding/) traces them by the rotation system, which is what rule 5 encodes. The [quad-edge structure](/quad-edge-data-structure/) of Guibas and Stolfi stores the subdivision and its dual together. A [polygon with holes](/polygon-with-holes/) is one bounded face with its boundary. A [triangulation](/triangulation/) is a subdivision in which every bounded face is a triangle; [Kirkpatrick's method](/kirkpatrick-point-location/) and the [triangle walk](/triangle-walk-point-location/) work on such subdivisions. A [monotone subdivision](/monotone-subdivision/) is one whose faces are monotone polygons; the [chain method](/chazelle-monotone-point-location/) needs that property. The [trapezoidal map](/trapezoidal-map/) of a PSLG is a refinement of its subdivision into trapezoids, and [planar point location](/planar-point-location/) asks for the face, edge or vertex that contains a query point.

## References
