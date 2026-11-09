---
tag: QTD7RG
kind: definition
slug: rectilinear-polygon
name: Rectilinear polygon
aliases:
- orthogonal polygon
- isothetic polygon
- axis-parallel polygon
area: geometry/polygons
level: intro
summary: A polygon whose edges are all horizontal or vertical.
prereqs: [simple-polygon]
see_also: [orthogonal-art-gallery-theorem, area-of-union-of-rectangles, orthogonal-segment-intersection, rectilinear-steiner-tree-problem, polygon-with-holes, shoelace-formula, convex-decomposition, polygon-union]
sources:
  - paper: doi:10.1137/0604020
    title: J. Kahn, M. Klawe and D. Kleitman, Traditional galleries require fewer watchmen, SIAM Journal on Algebraic and Discrete Methods 4(2), 194 to 206 (1983)
    locator: the whole paper (⌊n/4⌋ guards always suffice and are sometimes necessary for a rectilinear polygon with n vertices)
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 2, rectilinear polygons (the count of reflex vertices and the ⌊n/4⌋ theorem)
---

A rectilinear polygon is a [simple polygon](/simple-polygon/) whose edges are all horizontal or vertical, so every corner is a right angle, turning either inward or outward. Floor plans, circuit layouts, pixel regions and unions of axis-parallel rectangles have this shape. The restriction pins down its structure: the number of vertices is even, exactly $(n - 4)/2$ of them are reflex, and many problems become easier than on general polygons, such as guarding with $\lfloor n/4 \rfloor$ guards instead of $\lfloor n/3 \rfloor$.

## Definition

A simple polygon $P = (v_0, \ldots, v_{n-1})$ is **rectilinear** (or orthogonal) if every edge $e_i = v_i v_{i+1}$ is horizontal ($y_i = y_{i+1}$) or vertical ($x_i = x_{i+1}$), and consecutive edges alternate between the two, so no vertex has two horizontal or two vertical edges. Without the alternation, a vertex where the boundary goes straight on can be removed, and what remains alternates.

Each interior angle is then $\pi/2$ (a convex vertex) or $3\pi/2$ (a reflex vertex).

**Theorem.** A rectilinear polygon with $n$ vertices has $n$ even, $n \ge 4$, exactly $r = (n - 4)/2$ reflex vertices and $(n + 4)/2$ convex ones.

*Proof.* The edges alternate between horizontal and vertical around a cycle, so their number is even. The interior angles of a simple polygon sum to $(n - 2)\pi$ ([simple polygon](/simple-polygon/), Theorem 2). With $r$ reflex vertices this gives $(n - r)\frac{\pi}{2} + r\frac{3\pi}{2} = (n - 2)\pi$, so $n + 2r = 2n - 4$ and $r = (n - 4)/2 \ge 0$. $\square$

**Area.** In the [shoelace formula](/shoelace-formula/) written as the boundary integral $\oint x\, dy$, horizontal edges contribute nothing, so

$$A(P) = \sum_{e_i \text{ vertical}} x_i\, (y_{i+1} - y_i),$$

the signed area, positive in counterclockwise order. This is a sum over $n/2$ edges.

**Special classes.** A rectilinear polygon is **orthogonally convex** if every horizontal and every vertical line meets it in a single segment or not at all; this is weaker than being convex, since the only convex rectilinear polygons are rectangles. A **histogram** has one edge, the base, that every vertical line through the polygon meets.

## Examples and non-examples

- **A rectangle.** $(0,0), (4,0), (4,2), (0,2)$ has $n = 4$ and no reflex vertex.
- **An L-shape.** $(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)$ has $n = 6$ and one reflex vertex, $(1,1)$. Its vertical edges give the area $2 \cdot (1 - 0) + 1 \cdot (2 - 1) + 0 \cdot (0 - 2) = 3$.
- **A U-shape.** $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ has $n = 8$ and two reflex vertices, $(2,1)$ and $(1,1)$; its area is $9 - 2 = 7$. It is not orthogonally convex: the horizontal line $y = 2$ meets it in two segments.
- **A staircase.** $(0,0), (3,0), (3,1), (2,1), (2,2), (1,2), (1,3), (0,3)$ is orthogonally convex, with two reflex vertices and area 6.
- **Non-example: a diagonal edge.** $(0,0), (2,0), (2,1), (1,2), (0,2)$ has the edge from $(2,1)$ to $(1,2)$, which is neither horizontal nor vertical.
- **Non-example: a crossing walk.** $(0,1), (3,1), (3,2), (1,2), (1,0), (2,0), (2,3), (0,3)$ has only axis-parallel edges, but it is not simple: the edge from $(1,2)$ to $(1,0)$ crosses the edge from $(0,1)$ to $(3,1)$.

## Related definitions

- **[Simple polygon](/simple-polygon/).** The general class; rectilinear polygons are a special case.
- **[Polygon with holes](/polygon-with-holes/).** Rectilinear polygons with rectilinear holes model rooms with pillars and chip layers with cut-outs.
- **[Orthogonal art gallery theorem](/orthogonal-art-gallery-theorem/).** $\lfloor n/4 \rfloor$ guards always suffice and are sometimes necessary to see a rectilinear polygon with $n$ vertices (Kahn, Klawe and Kleitman, 1983).
- **[Area of union of rectangles](/area-of-union-of-rectangles/).** The union of axis-parallel rectangles is a set of rectilinear polygons with holes, and its area is found by a sweep.
- **[Orthogonal segment intersection](/orthogonal-segment-intersection/).** The edges of rectilinear polygons are horizontal and vertical segments, for which intersection problems have simpler sweeps.
- **[Rectilinear Steiner tree problem](/rectilinear-steiner-tree-problem/).** Network problems in the same axis-parallel metric.

## References
