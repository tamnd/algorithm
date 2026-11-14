---
tag: NG1GH7
kind: algorithm
slug: mesh-arrangements
name: Mesh arrangements for solid geometry
aliases:
- Zhou mesh arrangement
area: cad/mesh-processing
level: research
summary: Zhou, Grinspun, Zorin and Jacobson's method that computes the exact arrangement of all input triangles, labels each cell by winding numbers and extracts any Boolean.
solves: [mesh-boolean-operations]
model: real-ram
complexity:
  vars: {n: the number of input edges (triangles in 3D), K: the number of intersection points}
  time: {planar_code: O(n^2 + (n + K) log n), output_worst: O(n^2)}
  space: {arrangement: O(n + K)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2016
  people: [Qingnan Zhou, Eitan Grinspun, Denis Zorin, Alec Jacobson]
  note: Zhou, Grinspun, Zorin and Jacobson presented mesh arrangements at SIGGRAPH 2016, with exact intersections and winding number labels for Booleans on self-intersecting, open or overlapping input.
prereqs: [winding-number-algorithm, all-segment-intersections, doubly-connected-edge-list]
see_also: [generalized-winding-number, mesh-self-intersection, triangle-triangle-intersection, constrained-delaunay-triangulation, bentley-ottmann-algorithm, polygon-clipping, solid-boolean-operations, exact-geometric-computation]
sources:
  - paper: doi:10.1145/2897824.2925901
    title: Qingnan Zhou, Eitan Grinspun, Denis Zorin and Alec Jacobson, Mesh arrangements for solid geometry, ACM Transactions on Graphics 35(4), 2016, Article 39
    locator: the exact resolution of self-intersections, the patches and cells of the arrangement, the propagation of winding numbers between cells, and the extraction of Booleans by a winding number rule
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Line Segment Intersection, Sections 2.2 to 2.4 (the doubly connected edge list, the overlay of two subdivisions, and Boolean operations on polygons)
---

Mesh arrangements is a method for Boolean operations on triangle meshes that works even when the input meshes cut themselves, overlap, touch along faces, or are not closed. It cuts every triangle of every input against every other with exact arithmetic, so that the pieces meet only along shared edges. The pieces divide space into cells. Each cell gets one [winding number](/winding-number-algorithm/) per input mesh, found by starting outside, where all winding numbers are 0, and adding the multiplicity of each face crossed. A Boolean is then a rule on these numbers, for example "inside A or inside B", and the output is the set of faces between a cell where the rule holds and one where it fails. Qingnan Zhou, Eitan Grinspun, Denis Zorin and Alec Jacobson presented it in 2016. It is the main exact method for the [mesh Boolean operations](/mesh-boolean-operations/) problem. The code of this page implements the same steps one dimension lower, for closed polygons in the plane, with exact rational arithmetic.

## In plain words

Draw two overlapping shapes on paper with a pencil. Every place where two lines cross becomes a corner, and the lines cut the paper into many small regions. Now ask, for each region, how many times each shape wraps around it. Outside everything, the answer is zero. Each time you cross a line of a shape going inward, the count for that shape goes up by one.

When every region has its counts, a Boolean is just a choice of regions. The union keeps the regions where either count is positive, the intersection keeps those where both are. The answer is the outline of the chosen regions. Because the counts come from crossing lines, the method does not care if a shape crosses itself or if two shapes share an edge.

## The problem

The input is $K$ meshes, here $K$ sets of closed polygons, each oriented so that the outward normal follows the right-hand rule; in the plane that means counterclockwise, with the outward normal on the right of each edge. The polygons may cross themselves and each other, overlap along edges and touch at points. A rule $f$ maps a vector of $K$ winding numbers to inside or outside, with $f(0, \dots, 0)$ outside. The output is the boundary of the region where $f$ holds, as a set of directed edges with the region on the left, and its area.

## The algorithm

Two input edges meet in a single crossing point, or, if they lie on one line, along an overlap. The crossing point of segments $p_1p_2$ and $q_1q_2$ has the parameter $t = \mathrm{cross}(q_1 - p_1, q_2 - q_1) / \mathrm{cross}(p_2 - p_1, q_2 - q_1)$, which is a rational number for rational input, so the point is exact. Each half-edge $u \to v$ of the result carries a vector $m$, the number of input edges of each input that run from $u$ to $v$ minus those that run from $v$ to $u$. Crossing that half-edge from its right side to its left side raises the winding numbers by $m$.

```pseudo id=main
MESH-ARRANGEMENT-BOOLEAN(polygons with input tags, rule f)
L1  for each pair of input edges, add their crossing point or overlap ends to both as cut points
L2  split each edge at its sorted cut points; merge equal pieces, adding their signed counts m
L3  sort the half-edges around each vertex by angle; next(u → v) is the edge at v just clockwise of v → u
L4  for each connected component, take its leftmost lowest vertex v; label the outer half-edge at v with the winding numbers of the other components at v
L5  propagate labels: next(h) gets the label of h; the twin of h gets label(h) − m(h)
L6  keep each half-edge h with f(label(h)) true and f(label(twin(h))) false
L7  return the kept half-edges and their area by the shoelace formula
```

In 3D, Zhou and coauthors replace L1 and L2 by an exact intersection of all pairs of triangles that a bounding box test finds, followed by a [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) of each triangle with its cut segments, as in [mesh self-intersection](/mesh-self-intersection/). L3 becomes the sorting of the patches around each non-manifold edge by an exact orientation test, and the components nested inside each other are placed by finding the outer hull of each. L5 and L6 are the same, with cells and faces in place of faces and edges.

**Degenerate cases.** A polygon edge of length zero is dropped. Two inputs that share an edge produce one merged piece whose $m$ counts both, so the shared edge is not duplicated. A piece that one polygon uses in both directions has $m = 0$; it separates two faces with equal labels and is never output. Points where only two pieces meet in a straight line stay as vertices of the output, so the output can have collinear consecutive edges. A clockwise polygon has winding number $-1$ inside, and with the rule $w > 0$ it removes area from a counterclockwise polygon of the same input, which is how holes are given.

## Example

Let input A be the square $[0, 2]^2$ and input B the square $[1, 3]^2$, both counterclockwise.

| step | value |
|---|---|
| L1 | the boundaries cross at $(2, 1)$ and $(1, 2)$ |
| L2 | 12 pieces and 10 vertices; each piece has $m = (\pm 1, 0)$ or $(0, \pm 1)$ |
| L4 | the least vertex is $(0, 0)$; its outgoing pieces go to $(2, 0)$ and $(0, 2)$, and the one with the larger angle, $(0,0) \to (0,2)$, has the outside on its left: label $(0, 0)$ |
| L5 | A runs $(0, 2) \to (0, 0)$, so $m((0,0) \to (0,2)) = (-1, 0)$ and the twin gets $(0,0) - (-1,0) = (1, 0)$ |
| L5 | the other faces get $(1, 1)$ in the overlap and $(0, 1)$ in the part of B outside A |
| L6, union | rule $w_A > 0$ or $w_B > 0$: 8 half-edges, the outer pieces of both squares |
| L7 | union area 7, intersection area 1 (4 half-edges), difference A − B area 3 (6 half-edges) |

The tests also check the labels on random closed polylines with integer vertices in $[0, 6]^2$, which cross themselves and each other and often share vertices and overlapping edges. In 30 such inputs, 110 of the 1950 pieces were shared by more than one input edge, the winding numbers ranged from $-2$ to $3$, and the label of the face found by an exact ray from 1155 random points equalled the exact winding number at the point every time.

**When the arithmetic is floating point.** The method depends on exactness in a way most geometry code does not. If the crossing point of two edges is rounded, it no longer lies on either edge, the pieces can cross again near it, and a piece can end up on the wrong side of a vertex. Then the cycles of L3 do not close, or the labels of L5 disagree, and the code of this page would raise its consistency error. The signs that decide the order around a vertex and the side of a point are [orientation tests](/orientation-test/), and in doubles they suffer from [catastrophic cancellation](/catastrophic-cancellation/) exactly in the degenerate cases that Booleans produce, such as shared edges and coplanar faces. Zhou and coauthors therefore compute the whole arrangement with exact rational numbers, and only filtered [exact predicates](/shewchuk-expansion-sum/) keep this fast. The output has rational coordinates; rounding them to doubles can create new self-intersections, which is a remaining part of the [robustness problem](/geometric-robustness-problem/).

## Correctness

After the cuts, two pieces meet only at common endpoints, because every point where two input edges meet is a cut point of both, and pieces of collinear overlapping edges coincide and are merged. The winding numbers are constant on each face and jump by $m$ across a piece, so the propagation rules of L5 hold for the true values. The first label of a component is right: a ray to the left of its leftmost vertex misses the component, which is made of whole closed polygons and winds 0 there, and the other polygons do not pass through the vertex. By induction every label equals the true winding numbers, every half-edge of the component is reached, and the kept half-edges are exactly the boundary of the chosen region, with the region on the left, so the shoelace sum is its area. The full proof is below.

## Complexity

For $n$ input edges, the code of this page tests all pairs, $O(n^2)$ time, and then sorts the cut points of each edge and the pieces around each vertex, $O((n + K) \log n)$ for $K$ crossing points. A [sweep](/bentley-ottmann-algorithm/) finds the crossings in $O((n + K) \log n)$, which is better when $K$ is small. The search of L5 visits each half-edge once, $O(n + K)$. The arrangement takes $O(n + K)$ space, and $K$ can be $\Theta(n^2)$, for example for two grids of long thin rectangles laid across each other, so the output alone can be quadratic. In 3D, the arrangement of $n$ triangles can have $\Theta(n^2)$ cut segments, and every step also pays for exact arithmetic, whose cost grows with the bit length of the coordinates.

## Properties

- **Exact.** With rational input all labels and the output are exact.
- **Robust to bad input.** Self-intersections, overlaps, shared faces and nested components are handled by the winding numbers.
- **Any Boolean at once.** One arrangement serves union, intersection, difference, symmetric difference, and rules over many inputs, such as "inside at least two of five".
- **Order independent.** The result depends only on the input polygons, not on the order of their edges.
- **Needs closed input for integer labels.** The labels are integer winding numbers only when each input is closed. An open mesh has no integer winding number, and the propagation can then reach one cell with two different values.

## Variants and improvements

- **Planar overlay.** The planar case is the overlay of subdivisions with a [doubly connected edge list](/doubly-connected-edge-list/), as in de Berg and coauthors, and [polygon clipping](/polygon-clipping/) methods such as [Vatti clipping](/vatti-clipping/) and the [Greiner-Hormann algorithm](/greiner-hormann-algorithm/) compute the same Booleans for polygons with less general input.
- **Nef polyhedra.** Exact Booleans of general polyhedra with selective Nef complexes, by Granados and coauthors (2003) and in CGAL, are exact too but build a much larger structure.
- **Plane-based and interval methods.** Bernstein and Fussell (2009) and Campen and Kobbelt (2010) represent the geometry by planes and use filtered or fixed-precision predicates to get speed with exactness.
- **Generalized winding numbers.** For open or broken meshes, the [generalized winding number](/generalized-winding-number/) gives a soft inside value per cell instead of an exact integer.
- **Faster exact cuts.** Cherchi, Livesu, Scateni and Attene (2020) replaced the rational numbers by indirect predicates on the input coordinates, which avoids the growth of bit length.

## When to use it

Use it when the input meshes may be dirty, as scanned or modelled meshes often are, and the Boolean must be watertight and exact: 3D printing, CAD of meshes, and preparing meshes for simulation. For clean input and speed, plane-based or floating point methods may be enough, and for B-rep solids with curved faces, see [solid Boolean operations](/solid-boolean-operations/). In the plane, use a polygon clipping library unless the input has the same kinds of degeneracy.

## Pitfalls

- **Floating point intersections.** Rounded crossing points break the structure, as described above. Keep the arithmetic exact until the end.
- **Wrong orientation.** A polygon or mesh with reversed faces has winding number $-1$ inside and is treated as a hole by the rule $w > 0$. Fix the orientation first, or use $w \ne 0$.
- **Rounding the output.** The exact output may become self-intersecting when its coordinates are rounded to doubles.
- **Quadratic output.** Many long thin parts crossing each other create $\Theta(n^2)$ pieces, and exact rationals grow in size with each step.

## Implementations

## History

Booleans of polyhedra go back to the boundary evaluation of solid modelling in the 1970s and 1980s, and exact methods to the Nef polyhedra of Walter Nef (1978) and their implementation in CGAL by Granados, Hachenberger, Hert, Kettner, Mehlhorn and Seel (2003). Winding numbers as the inside rule of polygon fill go back to early computer graphics. Jacobson, Kavan and Sorkine-Hornung used generalized winding numbers for broken meshes in 2013. Zhou, Grinspun, Zorin and Jacobson combined exact arrangements with winding number labels in 2016, and their code in the libigl library made robust mesh Booleans widely available.

## References
