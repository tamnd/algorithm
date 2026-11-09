---
tag: T9F3Z9
kind: definition
slug: monotone-polygon
name: Monotone polygon
aliases:
- y-monotone polygon
- x-monotone polygon
- polygon monotone with respect to a line
area: geometry/polygons
level: core
summary: A polygon whose intersection with some line in a fixed direction is a single interval, so it splits into two monotone chains.
prereqs: [polygon, simple-polygon]
see_also: [monotone-polygon-partition, monotone-polygon-triangulation, monotone-subdivision, convex-polygon, star-shaped-polygon, rectilinear-polygon, sweep-line-technique, point-in-polygon]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.2 (y-monotone polygons, the five vertex types, and the lemma that a polygon without split and merge vertices is y-monotone) and Section 3.3 (triangulating a monotone polygon)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 (monotone partitioning, monotone chains and interior cusps)
  - paper: "Franco P. Preparata and Kenneth J. Supowit, Testing a simple polygon for monotonicity, Information Processing Letters 12(4), 1981, 161 to 164"
    locator: the linear time computation of all directions in which a simple polygon is monotone
  - paper: "Michael R. Garey, David S. Johnson, Franco P. Preparata and Robert E. Tarjan, Triangulating a simple polygon, Information Processing Letters 7(4), 1978, 175 to 179"
    locator: monotone polygons, their linear time triangulation, and the reduction of general polygons to monotone pieces
---

A simple polygon is *monotone* with respect to a line $\ell$ if every line perpendicular to $\ell$ meets it in a connected set: nothing, a point, or one segment. A polygon that is monotone with respect to the $y$-axis, so that every horizontal line meets it in one interval, is called *$y$-monotone*. Its boundary splits at a lowest and a highest vertex into two chains along which the height never decreases, one going up and one coming down. Monotone polygons sit between convex polygons, which are monotone in every direction, and general simple polygons; many problems are easier on them, and the standard way to [triangulate](/monotone-polygon-triangulation/) a simple polygon is to [cut it into monotone pieces](/monotone-polygon-partition/) first.

## Definition

**Notation.** A polygon is a cyclic sequence of points $v_0, \ldots, v_{n-1}$ with edges $v_i v_{i+1}$, indices modulo $n$. We assume the polygon is [simple](/simple-polygon/) and write $R$ for its closed region, the boundary together with the bounded part of its complement. For a nonzero vector $d$, the *height* of a point $p$ in direction $d$ is the dot product $d \cdot p$, and the lines perpendicular to $d$ are the level sets $\{p : d \cdot p = c\}$. For $d = (0, 1)$ the height is the $y$-coordinate and the level sets are horizontal lines.

**Definition.** The polygon is *monotone in direction $d$* (or with respect to a line $\ell$ parallel to $d$) if for every real $c$ the set $R \cap \{p : d \cdot p = c\}$ is connected. It is *$y$-monotone* if it is monotone in direction $(0, 1)$, and *$x$-monotone* if it is monotone in direction $(1, 0)$. Directions $d$ and $-d$ give the same condition.

**Monotone chains.** A polygonal chain $u_0, u_1, \ldots, u_k$ is *monotone in direction $d$* if the heights $d \cdot u_0, d \cdot u_1, \ldots, d \cdot u_k$ never decrease, or never increase. It is *strictly monotone* if they strictly increase or strictly decrease. A strictly monotone chain meets each perpendicular line at most once.

**Characterization by chains.** A simple polygon is monotone in direction $d$ if and only if its boundary is the union of two chains that are monotone in direction $d$, both from a vertex of least height to a vertex of greatest height. Equivalently, in the cyclic sequence of the signs of $d \cdot (v_{i+1} - v_i)$, with the zeros removed, the sign changes at most twice. The reason is the crossing count: a perpendicular line at a height strictly between two consecutive vertex heights meets each monotone chain in exactly one point, so it meets the boundary in exactly two points, and the region in the segment between them. If instead the signs change four times or more, there are two local maxima of the height, and a line just below the lower of the two, at a height that is not the height of a vertex, meets the boundary twice near that maximum and at least twice more on the rest of the boundary, which climbs to the other maximum and comes back down. A line that crosses the boundary four times meets the region in at least two pieces.

**Linear time test.** For one direction $d$, the sign test reads each edge once, so it takes $O(n)$ time, and with integer coordinates and an integer $d$ it is exact. Preparata and Supowit showed how to find all directions in which a simple polygon is monotone in $O(n)$ time as well. The set of good directions is a union of closed arcs, whose endpoints are normals of edges, and it can be empty or a single direction.

**Vertex types.** For a $y$-monotone polygon, de Berg and coauthors classify each vertex $v$ by its two neighbors, where *below* means a smaller $y$, or an equal $y$ and a larger $x$:

- a *start vertex* has both neighbors below and an interior angle less than $\pi$,
- a *split vertex* has both neighbors below and an interior angle greater than $\pi$,
- an *end vertex* has both neighbors above and an interior angle less than $\pi$,
- a *merge vertex* has both neighbors above and an interior angle greater than $\pi$,
- a *regular vertex* has one neighbor above and one below.

A split vertex or a merge vertex is the local obstacle to monotonicity, often called an interior cusp. If the polygon has no split vertex and no merge vertex, then it is $y$-monotone. If no edge is horizontal, the converse holds too: a $y$-monotone polygon has no split vertex and no merge vertex. With horizontal edges the converse can fail, because the tie rule in the order "below" treats the plane as if it were rotated by an infinitely small angle, and that rotated polygon may not be monotone; see the second example.

**Facts.**

- A convex polygon is monotone in every direction. Conversely, a simple polygon that is monotone in every direction is convex: at a reflex vertex $v$ with neighbors $u$ and $w$, the vectors $u - v$ and $w - v$ are not opposite, so some direction $d$ makes both neighbors lower than $v$, and then $v$ is a split vertex for $d$.
- Every [point in polygon](/point-in-polygon/) query on a $y$-monotone polygon takes $O(\log n)$ time after $O(n)$ preprocessing: split the boundary into its two chains, find by binary search the edge of each chain at the height of the query point, and compare.
- A $y$-monotone polygon can be triangulated in $O(n)$ time with a stack (Garey, Johnson, Preparata and Tarjan); see [triangulation of a monotone polygon](/monotone-polygon-triangulation/).

## Examples and non-examples

**An L-shape.** $(0,0), (4,0), (4,2), (1,2), (1,4), (0,4)$ is both $x$-monotone and $y$-monotone. The signs of the $y$-steps are $0, +, 0, +, 0, -$, which after removing zeros is $+, +, -$, with two cyclic sign changes. Its reflex vertex $(1,2)$ is a regular vertex: one neighbor, $(1,4)$, is above it, and the other, $(4,2)$, is below it by the tie rule.

**A mirrored L-shape.** $(0,0), (4,0), (4,4), (3,4), (3,2), (0,2)$ is also $y$-monotone: the horizontal line at height 2 meets it in the segment from $(0,2)$ to $(4,2)$, and lines above that height meet it in the segment from $x = 3$ to $x = 4$. The signs of the $y$-steps, without zeros, are $+, -, -$, again two sign changes. But the reflex vertex $(3,2)$ has both neighbors above it in the order with the tie rule, since $(0,2)$ has the same height and a smaller $x$. So it is a merge vertex, and an algorithm that partitions by the vertex types adds a diagonal there that is not needed.

**A U-shape.** $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ is $x$-monotone, as every vertical line meets it in one segment. It is not $y$-monotone: the line $y = 2$ meets the two arms in the separate segments $[0,1]$ and $[2,3]$. It is monotone in no other direction either. For a direction $d$ that is not along an axis, the lines perpendicular to $d$ are neither horizontal nor vertical. If they rise to the right, take the one through a point just left of the inner corner $(2,1)$ at height 1: going up from the bottom bar, it crosses the gap for a short way and then enters the right arm, so it meets the region in two pieces. If they rise to the left, use the corner $(1,1)$ and the left arm in the same way. So the set of good directions is the single direction $(1,0)$.

**A comb.** $(0,0), (5,0), (5,3), (4,3), (4,1), (3,1), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ is $x$-monotone. The line $y = 2$ meets its three teeth in three segments. The $y$-steps change sign six times, and the vertices $(4,1)$ and $(2,1)$ are merge vertices.

**Non-example in every direction.** The square $[0,6]^2$ with a slot cut down from the top and a slot cut in from the right,

$$(0,0), (6,0), (6,4), (4,4), (4,5), (6,5), (6,6), (3,6), (3,2), (2,2), (2,6), (0,6),$$

is monotone in no direction. By the argument for the U-shape, at the inner corners $(2,2)$ and $(3,2)$, the slot from the top breaks every direction except $(1,0)$, and the slot from the right breaks every direction except $(0,1)$. These two remaining directions fail too: the horizontal line $y = 4$ meets the polygon in $[0,2]$ and $[3,6]$, and the vertical line $x = 5$ meets it in $y \in [0,4]$ and $y \in [5,6]$.

**Non-example: a spiral.** A polygon that winds around a center more than once, like a coiled corridor, is monotone in no direction.

## Related definitions

- [Convex polygon](/convex-polygon/): the polygons that are monotone in every direction.
- [Star-shaped polygon](/star-shaped-polygon/): a different relaxation of convexity. A star-shaped polygon need not be monotone, and a monotone polygon need not be star-shaped; the comb is monotone but no point sees all three teeth.
- [Rectilinear polygon](/rectilinear-polygon/): a histogram polygon, a rectilinear polygon whose boundary is one straight base edge and a chain of horizontal and vertical edges above it, is monotone in the direction of its base.
- *Monotone mountain*: a monotone polygon one of whose chains is a single edge. It is triangulated by cutting off convex vertices of the other chain.
- [Monotone subdivision](/monotone-subdivision/): a planar subdivision whose faces are monotone polygons, the input of several point location structures.
- [Monotone polygon partition](/monotone-polygon-partition/): the problem of cutting a simple polygon into monotone pieces by diagonals, solved by a [sweep](/sweep-line-technique/) that adds one diagonal at each split vertex and each merge vertex.
- [Monotone polygon triangulation](/monotone-polygon-triangulation/): the linear time triangulation of one monotone piece.

## References
