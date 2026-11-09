---
tag: FZS9WJ
kind: definition
slug: polygon
name: Polygon
aliases:
- simple polygon boundary
- closed polygonal chain
- closed polyline
- polygonal curve
area: geometry/polygons
level: intro
summary: A closed sequence of line segments (edges) joined at vertices.
prereqs: [point-and-vector]
see_also: [simple-polygon, convex-polygon, polygon-with-holes, polygon-orientation, shoelace-formula, point-in-polygon, polygon-simplicity-test, winding-number-algorithm]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.1, the definition of a polygon as a closed chain of segments and of its vertices, edges and boundary
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1, Guarding and triangulations (simple polygons, their vertices and diagonals)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1, Section 1.3, the definitions of a polygon, a simple polygon and a convex polygon
---

A polygon is a closed chain of straight segments in the plane: a cyclic list of points, the vertices, in which each vertex is joined to the next by an edge and the last vertex is joined back to the first. It is the basic input of most of computational geometry. The list alone fixes the boundary, its direction and its length; whether the polygon also has a well-defined inside depends on whether the chain crosses itself, and for that case the stronger notion is the [simple polygon](/simple-polygon/).

## Definition

Let $n \ge 3$ and let $v_0, v_1, \ldots, v_{n-1}$ be points of $\mathbb{R}^2$, the **vertices**. Indices are taken mod $n$, so $v_n = v_0$ and $v_{-1} = v_{n-1}$.

- The **polygon** $P = (v_0, \ldots, v_{n-1})$ is the cyclic sequence of vertices. Two lists that differ by a cyclic shift, $(v_k, v_{k+1}, \ldots, v_{k-1})$, are the same polygon. The reversed list $(v_{n-1}, \ldots, v_0)$ has the same boundary traversed in the opposite direction.
- The **edges** are the closed segments $e_i = v_i v_{i+1} = \{(1 - \lambda) v_i + \lambda v_{i+1} : 0 \le \lambda \le 1\}$ for $0 \le i < n$, directed from $v_i$ to $v_{i+1}$. The edges $e_{i-1}$ and $e_i$ are **neighbors** and share the vertex $v_i$.
- The **boundary** $\partial P = e_0 \cup \cdots \cup e_{n-1}$ is a closed polygonal curve, the image of the closed path that runs through $e_0, e_1, \ldots, e_{n-1}$ in order. Its length is $\sum_i |v_{i+1} - v_i|$.
- The **turn** at $v_i$ is the sign of $\mathrm{orient}(v_{i-1}, v_i, v_{i+1})$, the [orientation](/orientation-test/) of the three points: positive for a left turn, negative for a right turn, zero when the three points are collinear.

The word *polygon* is also used for a region of the plane. For a simple polygon this region is the closed bounded set enclosed by $\partial P$, which exists by the [Jordan curve theorem](/jordan-curve-theorem/). For a polygon that crosses itself, the boundary does not fix a region alone, and one is chosen by a fill rule from the [winding number](/winding-number-algorithm/) $w_P(q)$ of the boundary around each point $q \notin \partial P$: the [nonzero rule](/nonzero-winding-rule/) takes $\{q : w_P(q) \ne 0\}$ and the [even-odd rule](/even-odd-fill-rule/) takes $\{q : w_P(q) \text{ odd}\}$. In every case the [signed area](/shoelace-formula/) $\frac12 \sum_i v_i \times v_{i+1}$ equals $\iint w_P(q)\, dq$.

A computer stores a polygon as an array of its $n$ vertices in boundary order, and the closing edge $v_{n-1} v_0$ is implicit. Some formats repeat $v_0$ at the end; the repeated point is not a vertex.

**General position and degenerate polygons.** The definition allows repeated vertices, three collinear consecutive vertices, edges that overlap, and even all vertices on one line. Algorithms state which of these they accept. A common normalization removes a vertex $v_i$ with $v_i = v_{i+1}$, and a vertex where the boundary goes straight on ($\mathrm{orient}(v_{i-1}, v_i, v_{i+1}) = 0$ with $v_i$ between its neighbors); both changes keep the boundary as a point set.

## Examples and non-examples

- **A triangle.** $(0,0), (4,0), (0,3)$ is a polygon with three edges of lengths 4, 5 and 3. Every turn is a left turn.
- **A square in two lists.** $(0,0), (1,0), (1,1), (0,1)$ and $(1,1), (0,1), (0,0), (1,0)$ are the same polygon, shifted by two places. $(0,1), (1,1), (1,0), (0,0)$ is its reverse: the same boundary, traversed clockwise.
- **A concave polygon.** $(0,0), (6,0), (6,4), (3,1), (0,4)$ has a right turn at $(3,1)$, where the boundary bends inward. It is simple.
- **A self-crossing polygon.** The bowtie $(0,0), (2,2), (2,0), (0,2)$ is a polygon whose edges $e_0$ and $e_2$ cross at $(1,1)$. Its signed area is 0: the winding number is $-1$ in one triangle and $+1$ in the other.
- **A pentagram.** The five points of a regular pentagon, listed by taking every second one, form a polygon whose boundary crosses itself five times. When the pentagon is counterclockwise, the winding number of the pentagram is 2 in the central pentagon and 1 in the five tips.
- **A degenerate polygon.** $(0,0), (2,0), (1,0)$ satisfies the definition, but its boundary is the segment from $(0,0)$ to $(2,0)$ traversed back and forth, and it encloses nothing.
- **Not a polygon: an open chain.** The points $(0,0), (1,0), (1,1)$ joined only by the segments $(0,0)$-$(1,0)$ and $(1,0)$-$(1,1)$ form a polyline, not a polygon, since the chain is not closed.
- **Not a polygon: a curved boundary.** A disk is not a polygon, though a regular polygon with many vertices approximates it.

## Related definitions

- **[Simple polygon](/simple-polygon/).** A polygon whose boundary does not touch or cross itself; then $\partial P$ is a Jordan curve with a well-defined inside.
- **[Convex polygon](/convex-polygon/).** A simple polygon whose region is a [convex set](/convex-set/); all its turns have the same sign.
- **[Polygon orientation](/polygon-orientation/).** Whether the vertices of a simple polygon are listed counterclockwise or clockwise, given by the sign of the signed area.
- **[Polygon with holes](/polygon-with-holes/).** A region bounded by one outer simple polygon and several inner ones.
- **[Monotone polygon](/monotone-polygon/), [star-shaped polygon](/star-shaped-polygon/) and [rectilinear polygon](/rectilinear-polygon/).** Special classes of simple polygons, used because some problems are easier on them.
- **[Polygon mesh](/polygon-mesh/) and [planar subdivision](/planar-subdivision/).** Many polygons glued along shared edges, in space or in the plane.

## References
