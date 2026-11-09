---
tag: TNRE54
kind: problem
slug: polygon-with-holes-triangulation
name: Triangulation of a polygon with holes
aliases:
- Polygon with holes triangulation
- triangulating a multiply connected polygon
area: geometry/triangulations
level: advanced
summary: Triangulate a polygon with interior holes, typically by joining holes to the outer boundary with bridge edges.
model: real-ram
complexity:
  vars: {n: the total number of vertices, h: the number of holes}
  time: {worst: Θ(n log n)}
prereqs: [polygon-with-holes, polygon-triangulation, ear-clipping, monotone-polygon-triangulation]
see_also: [constrained-triangulation, seidel-polygon-triangulation, chazelle-polygon-triangulation, minimum-steiner-triangulation, trapezoidal-map, art-gallery-theorem, euler-formula, constrained-delaunay-triangulation]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Sections 3.2 and 3.3 (the sweep works for polygons with holes) and the exercises of Chapter 3
  - paper: "Takao Asano, Tetsuo Asano and Ron Y. Pinter, Polygon triangulation, efficiency and minimality, Journal of Algorithms 7(2), 221 to 231 (1986)"
    locator: the Ω(n log n) lower bound for polygons with holes (to be checked)
  - paper: "Reuven Bar-Yehuda and Bernard Chazelle, Triangulating disjoint Jordan chains, International Journal of Computational Geometry and Applications 4(4), 475 to 481 (1994)"
    locator: the O(n + h log^(1+ε) h) bound for h holes
  - url: https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
    title: David Eberly, Triangulation by Ear Clipping, Geometric Tools
    locator: Sections 4 and 5 (finding a mutually visible pair for a bridge, and nested holes)
  - paper: "Martin Held, FIST, Fast industrial-strength triangulation of polygons, Algorithmica 30(4), 563 to 596 (2001)"
    locator: bridges for holes in an ear clipping triangulator
---

A polygon with holes is a region bounded by an outer simple polygon with disjoint simple polygons removed from its inside. Triangulating it means cutting it into triangles by diagonals between its vertices. With $n$ vertices in total and $h$ holes, every triangulation has exactly $n + 2h - 2$ triangles and $n + 3h - 3$ diagonals. There are two standard approaches: run a plane sweep, which handles holes with no change, in $O(n \log n)$ time; or cut a **bridge** from each hole to the outside, which turns the region into one weakly simple polygon that [ear clipping](/ear-clipping/) can process. Unlike simple polygons, polygons with holes need $\Omega(n \log n)$ time in the algebraic decision tree model.

## In plain words

Picture a slice of cheese with holes in it. You want to cut it into triangles with straight cuts from corner to corner, never crossing a hole. One trick: make one cut from each hole to the outer edge. Now the slice is one long strip that winds around the holes, with no holes left, and you can trim off triangles one by one as for an ordinary shape.

Each hole costs two extra triangles. With holes, a fast computer method must in effect sort the holes, so it cannot be faster than sorting.

## Definition

**Input.** An outer simple polygon $P_0$ and simple polygons $H_1, \ldots, H_h$ (the holes) that lie in the interior of $P_0$, with disjoint closures. Let $n$ be the total number of vertices. The region is $R = P_0 \setminus \bigcup_i \mathrm{int}(H_i)$.

**Output.** A set of diagonals, segments between vertices whose relative interiors lie in the interior of $R$, that cut $R$ into triangles; or the list of triangles.

**Counts.** The angles of the triangles add up to the interior angles of $R$: $(|P_0| - 2)\pi$ for the outer polygon plus $(|H_i| + 2)\pi$ for each hole, measured inside $R$. So the number of triangles is $t = n + 2h - 2$. Each triangle has 3 sides, each of the $n$ boundary edges is a side of one triangle and each diagonal of two, so the number of diagonals is $d = (3t - n)/2 = n + 3h - 3$. Both follow also from [Euler's formula](/euler-formula/).

## Variants

- **Constrained triangulation.** A polygon with holes is a planar straight-line graph whose outside and hole faces are dropped; see [constrained triangulation](/constrained-triangulation/). The [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) gives the best angles.
- **Nested holes and islands.** A hole can contain a new outer polygon, as in font glyphs or maps. Each region between consecutive levels is triangulated on its own.
- **Holes that touch.** If a hole touches the outer boundary or another hole at a vertex, the region is no longer a polygon with holes in the strict sense. The sweep still works if the shared vertex is treated as two vertices, one per boundary, and the counts change because the region has fewer independent holes.
- **Steiner points.** Allowed in [mesh generation](/mesh-generation/); for counts they never help; see [minimum Steiner triangulation](/minimum-steiner-triangulation/).

## Examples

- **A square with a square hole.** The outer square $(0,0)$, $(6,0)$, $(6,6)$, $(0,6)$ and the hole $(2,2)$, $(4,2)$, $(4,4)$, $(2,4)$ give $n = 8$, $h = 1$, so $t = 8$ triangles and $d = 8$ diagonals. One triangulation joins each hole corner to the two nearest outer corners: $(2,2)$ to $(0,0)$, $(4,2)$ to $(6,0)$, $(4,4)$ to $(6,6)$, $(2,4)$ to $(0,6)$, which cuts the ring into four trapezoids, each split by one more diagonal.
- **A bridge.** In the same example, the bridge from the rightmost hole vertex $(4,2)$ to the outer vertex $(6,0)$ is a diagonal. Cutting along it in both directions gives the weakly simple polygon $(0,0)$, $(6,0)$, $(4,2)$, $(2,2)$, $(2,4)$, $(4,4)$, $(4,2)$, $(6,0)$, $(6,6)$, $(0,6)$ with 10 vertices, whose ear clipping gives $10 - 2 = 8$ triangles, as predicted.
- **Many small holes.** $h$ tiny triangles placed along a line inside a long rectangle force the triangulation to connect the holes in their order along the line, which is why sorting is a lower bound.

## Known algorithms

| method | time | note |
|---|---|---|
| bridges plus [ear clipping](/ear-clipping/) | $O(n^2)$ | simplest; bridge holes in order of their rightmost vertex |
| plane sweep with monotone pieces | $O(n \log n)$ | the [monotone method](/monotone-polygon-triangulation/) without change |
| [trapezoidal map](/trapezoidal-map/) by randomized insertion | $O(n \log n)$ expected | Seidel's algorithm on all edges |
| Bar-Yehuda and Chazelle | $O(n + h \log^{1+\varepsilon} h)$ | linear time when $h$ is small |
| [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) | $O(n \log n)$ | best angles |

**Bridges.** Process the holes by decreasing $x$ of their rightmost vertex $m$. Shoot a ray from $m$ to the right, find the nearest edge it hits on the current outer boundary, and take the end point of that edge with the larger $x$, or, if a reflex vertex lies in the triangle between $m$, the hit point and that end point, the reflex vertex with the smallest angle to the ray. The segment from $m$ to the chosen vertex is a bridge. Splicing the hole into the outer cycle along it gives a weakly simple polygon with two more vertices.

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, by reduction from sorting through holes placed in a line (Asano, Asano and Pinter).
- **Upper bound.** $O(n \log n)$ by the sweep, optimal in the worst case. In terms of $h$, $O(n + h \log^{1+\varepsilon} h)$ for every $\varepsilon > 0$.
- **Simple polygons.** With $h = 0$, $\Theta(n)$ by [Chazelle's algorithm](/chazelle-polygon-triangulation/).

## Reductions

- **From sorting.** Given numbers $x_1, \ldots, x_h$, put a small triangle hole at each $(x_i, 0)$ in a large rectangle. In any triangulation, the triangles that the horizontal line through the holes crosses link the holes in sorted order, so the order can be read off in linear time.
- **To simple polygon triangulation.** Bridges turn the region into one weakly simple polygon, but finding the bridges itself takes $\Omega(n \log n)$ time in the worst case.
- **To planar subdivision triangulation.** A polygon with holes is one bounded face of a planar subdivision; see [planar subdivision](/planar-subdivision/).

## Applications

- **Rendering.** Fonts, map regions and vector graphics fill shapes with holes by triangulating them.
- **Art galleries with pillars.** A gallery with $h$ holes and $n$ vertices can always be guarded by $\lfloor (n + h)/3 \rfloor$ guards (Bjorling-Sachs and Souvaine; Hoffmann, Kaufmann and Kriegel); see the [art gallery theorem](/art-gallery-theorem/).
- **Mesh generation and path planning.** The free space around obstacles is a polygon with holes, and its triangulation is the base for shortest paths and meshes.

## References
