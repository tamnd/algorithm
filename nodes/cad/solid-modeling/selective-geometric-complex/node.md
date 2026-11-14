---
tag: TH7Q2X
kind: data-structure
slug: selective-geometric-complex
name: Selective geometric complex
aliases:
- SGC
- Rossignac-O'Connor complex
area: cad/solid-modeling
level: advanced
summary: Rossignac and O'Connor's model of non-manifold and mixed-dimensional objects as a cell complex whose cells are each marked in or out, closed under Booleans.
model: real-ram
complexity:
  vars:
    n: the number of segments and points that cut the plane, over both operands
    k: the number of crossing points between the segments
  time:
    worst: "O((n + k)^2)"
  space:
    extra: "O(n + k)"
prereqs: [r-set, regularized-set-operations, doubly-connected-edge-list]
see_also: [nef-polyhedron, radial-edge-data-structure, solid-boolean-operations, set-membership-classification, constructive-solid-geometry, red-blue-intersection, all-segment-intersections, boundary-representation]
sources:
  - paper: "Jarek R. Rossignac and Michael A. O'Connor, SGC: a dimension-independent model for pointsets with internal structures and incomplete boundaries, in M. J. Wozny, J. U. Turner and K. Preiss (eds.), Geometric Modeling for Product Engineering, North-Holland, 1990, pages 145 to 180 (also an IBM research report, 1989)"
    locator: the definition of the selective geometric complex as a set of disjoint, relatively open, connected cells with in-or-out marks, and the Boolean operations by subdivision, selection and simplification
  - paper: "Jarek R. Rossignac and Aristides A. G. Requicha, Constructive non-regularized geometry, Computer-Aided Design 23(1), 21 to 32, 1991"
    locator: Boolean and topological operations on non-regularized sets, and their use in solid modeling
  - paper: doi:10.1016/j.comgeo.2006.11.009
    title: Peter Hachenberger, Lutz Kettner and Kurt Mehlhorn, Boolean operations on 3D selective Nef complexes, data structure, algorithms, optimized implementation and experiments, Computational Geometry 38(1-2), 64 to 99, 2007
    locator: the selective Nef complex, a selective complex for linear sets in three dimensions with the same overlay, selection and simplification steps
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: chapter 2, the doubly connected edge list, its boundary cycles and holes, and the overlay of two subdivisions
---

A selective geometric complex (SGC) stores a geometric object as a cell complex in which every cell is marked in or out. The cells are disjoint, connected and relatively open: points, open curve pieces, open surface pieces and open volumes, of any dimension and on curved supports. The object is the union of the marked cells. So one structure holds solids, solids with cracks or missing boundary, dangling faces and wires, and isolated points: every non-manifold and mixed-dimensional case that the [r-sets](/r-set/) of classical solid modeling exclude. Jarek Rossignac and Michael O'Connor introduced the SGC in 1989, with Boolean operations in three steps: *subdivide* both complexes until they are compatible, *select* the cells of the result by the Boolean rule, and *simplify* by merging cells whose marks agree. The set of objects that an SGC represents is closed under the Boolean operations and under interior, closure and boundary, with no regularization. This page builds the planar case from straight segments and points, with exact rational arithmetic, and proves that the operations are exact.

## In plain words

Draw some straight strokes and dots on paper. They cut the paper into pieces: the dots and stroke ends, the bits of stroke between them, and the open regions between the strokes. Colour some pieces. The coloured pieces are the object. A coloured region with uncoloured edges is an open area; one coloured stroke is a wire; one coloured dot is a point.

To combine two objects, draw both sets of strokes on one sheet, so every new piece lies inside one piece of each object. Colour a new piece if the rule says so: in both, in either, in the first only. Then rub out every stroke and dot that has the same colour as everything around it. What is left is a small drawing of the answer. The inside of an object keeps a piece only if everything touching it is coloured too.

## The abstract type

An SGC value is a point set $S$ in the plane, given with a complex that cuts the plane into cells. The operations are:

- **Build** a simple polygon, open or closed, a segment, open or closed, or a point.
- **Booleans:** union, intersection, difference, symmetric difference and complement, with no regularization.
- **Topology:** interior, closure, boundary, and regularization $\operatorname{cl}\operatorname{int} S$.
- **Queries:** does $S$ contain a point $p$; is $S$ empty; how many marked vertices, edges and faces it has.
- **Simplify:** merge the cells that need not be separate.

Two descriptions of the same set give equal values: after simplification they have the same marked cells, and emptiness of the symmetric difference tests equality in any case.

## Representation

A *complex* is given by a finite set of segments and points. The code splits every segment at its endpoints, at its crossings with other segments, and at the given points that lie on it. The pieces are the *edges*, each an open segment, and their endpoints and the given points are the *vertices*. The *faces* are the connected components of the plane minus all edges and vertices. Faces may have holes, and a face may contain isolated vertices and dangling edges.

The face structure is that of a [doubly connected edge list](/doubly-connected-edge-list/). Each edge gives two half-edges. At each vertex, the outgoing half-edges are sorted counterclockwise by an exact angle key. The next half-edge after $(a, b)$ is the one that leaves $b$ just clockwise of $(b, a)$, so each traced cycle has its face on the left. A cycle of positive signed area is the outer boundary of a bounded face, and every bounded face has exactly one. Each other cycle, and each isolated vertex, is a hole and is placed in the face whose outer cycle is the innermost one around it, by winding numbers. Face 0 is the unbounded face. For each edge, the code records the faces on its two sides.

The *star* of a cell $c$ is the set of other cells whose closure contains $c$. The star of an edge is the faces on its two sides. The star of a vertex is the edges that end at it with their faces, or, for an isolated vertex, the face around it. A face has an empty star. An SGC is a complex together with its set of marked cells.

## Operations

```pseudo id=main
COMBINE(A, B, op)                                        ▷ op is or, and, minus or xor
L1  segs ← the edges of A and of B; pts ← the vertices of A and of B
L2  C ← the complex cut out by segs and pts               ▷ every cell of C lies in one cell of A and one of B
L3  for each cell c of C do
L4      p ← a point inside c
L5      mark c if op(A contains p, B contains p)
L6  return SIMPLIFY(C, marks)

SIMPLIFY(S)
L7  keep each edge whose mark differs from one of its two faces
L8  keep each vertex unless its kept edges are two collinear edges marked like it,
    or it has no kept edge and is marked like its whole star
L9  C' ← the complex cut out by the kept edges, merged along lines, and the kept vertices
L10 mark each cell c' of C' if S contains a point inside c'
```

**Points inside cells.** A vertex is its own point, and an edge gives its midpoint. For the unbounded face, the code takes a point to the right of every vertex. For a bounded face, it takes the first edge $ab$ of the outer cycle, so the face is on the left of $ab$. It starts at the midpoint $m$ of $ab$ and moves along the left normal. It finds the first edge or vertex that the ray meets, at parameter $t^\ast$, and takes the point at $t^\ast / 2$.

**Containment** locates the cell of $p$, checking vertices, then edges, then the innermost outer cycle that winds around $p$. Then it looks up the mark.

**Complement** flips every mark on the same complex. **Interior** keeps the marked cells whose whole star is marked. **Closure** marks every cell that is marked or has a marked cell in its star. Both are simplified afterwards. **Boundary** is the closure minus the interior, and **regularization** is the closure of the interior.

**Primitives.** A polygon is the complex of its sides, with each cell marked by a direct test of its sample point: inside by winding number, or on a side if the polygon is closed. Segments and points are built the same way.

## Example

Take the closed square $[0, 4]^2$ and remove the open segment from $(1, 2)$ to $(3, 2)$, a crack inside it. The result $S$ keeps the two crack ends, which are not in the open segment. Its complex has 6 vertices, 5 edges and 2 faces. The faces are the outside and the square minus the crack. The crack is a hole in the square's face, a cycle of zero area. The marks are 6 vertices, 4 edges and 1 face.

| set | vertices, edges, faces in the complex | marked vertices, edges, faces |
|---|---|---|
| $S$ | 6, 5, 2 | 6, 4, 1 |
| $\operatorname{int} S$ | 6, 5, 2 | 0, 0, 1 |
| $\operatorname{cl} S$ | 4, 4, 2 | 4, 4, 1 |
| $\partial S$ | 6, 5, 2 | 6, 5, 0 |
| $\operatorname{cl}\operatorname{int} S$ | 4, 4, 2 | 4, 4, 1 |
| complement of $S$ | 6, 5, 2 | 0, 1, 1 |

The interior drops the crack ends, whose stars contain the unmarked crack. The closure fills the crack back in, and simplification removes it, since it is now marked like the face on both sides. The boundary is the square's outline, the crack and its two ends.

Unlike a [Nef polygon](/nef-polyhedron/), the SGC does not extend the crack to a full line. A Nef polygon for $S$ needs the lines $x = 1$, $x = 3$ and $y = 2$ across the whole plane, besides the four lines of the square. That is 7 lines, which cut the plane into 20 cells, against 2 faces here.

A second example shows the three steps. Take the closed squares $A = [0, 2] \times [0, 2]$ and $B = [2, 4] \times [0, 2]$, which share the edge $x = 2$. The overlay at L2 has 6 vertices, 7 edges and 3 faces. For $A \cup B$, all cells but the outside are marked. L7 drops the shared edge, whose mark equals both faces. L8 drops $(2, 0)$ and $(2, 2)$, each between two collinear kept edges marked like it. The result is one rectangle: 4 vertices, 4 edges, 2 faces. For $A \cap B$, the marked cells are the shared edge and its two ends, a segment, and its regularization is empty, as a regularized modeler would return.

## Correctness

The proof file proves the following for the planar code.

1. **The complex is a cell decomposition.** The vertices, open edges and faces are disjoint, connected and cover the plane. The traced cycles, with outer cycles and holes, give every face exactly once. Every point of a cell $c$ has a disc around it that meets only $c$ and the cells of its star.
2. **The overlay refines both inputs.** The skeleton of $A$, its edges and vertices, is contained in the skeleton of $C$. So every cell of $C$ lies inside exactly one cell of $A$ and one of $B$, and it is entirely in or entirely out of each. Lines L4 and L5 test one point, which decides the whole cell, so COMBINE returns exactly $\operatorname{op}(A, B)$.
3. **Simplification keeps the set and is minimal.** Every cell of the new complex $C'$ is a union of old cells. All of those old cells have the same mark: they are joined through removed edges and vertices, and L7 and L8 remove only cells marked like their neighbours. So L10 reproduces the set. After one pass, every edge separates differently marked cells, and every vertex is a bend, an end, a junction, or marked unlike its star. So a second pass changes nothing.
4. **Interior and closure follow the star.** This is the local structure of point 1, as for [Nef polyhedra](/nef-polyhedron/). So the sets that SGCs represent are closed under complement, the Booleans, interior, closure and boundary. The [r-sets](/r-set/) are not closed under these operations and need [regularized operations](/regularized-set-operations/).

The tests compare the code with the defining formula. They build a random formula of depth up to 3 over triangles, segments and points with integer corners in $[0, 4]^2$, each open or closed, combined by union, intersection, difference, symmetric difference and complement. They evaluate the formula directly at every point of a grid with step $\tfrac12$ around the box, and at every vertex of the complex. Interior, closure and boundary are checked against an oracle that evaluates the formula at $p$ and at $p + \varepsilon d$, for a fixed set of directions $d$ with one direction in every possible wedge. The tests also check that every simplified complex meets the minimality conditions, and that simplifying twice changes nothing.

## Complexity

For the planar code, with $n$ input segments and points and $k$ crossings, the complex has $O(n + k)$ cells. The bounds below are proved by counting the loops of the code:

- Building the complex takes $O(n^2)$ time to find the cuts on each segment, and $O((n + k) \log (n + k))$ time to sort the half-edges around the vertices and the cuts along the segments. Placing holes and isolated vertices in faces, and finding a point in each face, take $O(n + k)$ time per cycle, so $O((n + k)^2)$ in all.
- Containment takes $O(n + k)$ time.
- COMBINE takes $O((n + k)^2)$ time: one containment query per cell, with $n$ and $k$ counted over both operands. SIMPLIFY has the same bound.
- Complement takes linear time. Interior and closure take time linear in the total star size, which is $O(n + k)$, plus a simplification.

A production kernel avoids the quadratic terms. It overlays two subdivisions by a [plane sweep](/bentley-ottmann-algorithm/) in $O((N + k) \log N)$ time, for inputs of total size $N$ with $k$ crossings, and carries the face of each cell through the sweep instead of testing a point. The general SGC of Rossignac and O'Connor works in any dimension with curved cells, and its cost is set by the subdivision step, that is, by surface intersection. The original papers give no general bound, and this page does not state one.

## Variants

- **Any dimension, curved cells.** In the original SGC, each cell lies on an *extent*, a curve, surface or volume carrying the geometry, and the boundary of every cell is a union of cells. Subdivision intersects extents. Selection marks cells by classifying them against the operands, by [set membership classification](/set-membership-classification/). Simplification merges a cell into a neighbour of higher dimension when both have the same mark and the same extent.
- **Selective Nef complex.** Hachenberger, Kettner and Mehlhorn store linear sets in three dimensions as a complex of vertices, edges, facets and volumes with marks, with a sphere map at each vertex for the local picture. This is the [Nef polyhedron](/nef-polyhedron/) structure. Both store sets bounded by straight pieces with marks on all cells. The Nef sets are generated from half-spaces, so they include unbounded sets such as half-planes, which the segment-based code on this page cannot build.
- **Non-manifold boundary structures.** The [radial edge data structure](/radial-edge-data-structure/) of Weiler and later non-manifold B-reps store the same mixed-dimensional objects by their boundaries, with the faces around each edge in radial order. They usually store only the marked cells and their boundaries, not a complete cell decomposition of space.
- **Regularized use.** A modeler that needs only solids can regularize after each operation and keep only the boundary, which gives a classical [B-rep](/boundary-representation/).

## When to use it

Use an SGC when the lower-dimensional and non-manifold parts are part of the model. Examples are mid-surface and wire-frame models, meshes with internal faces between materials, cracks and cuts, analysis models that mix shells, beams and solids, and intermediate results that the next operation must not lose. Use it also when exact closure under Booleans matters more than size: an SGC operation never needs a special case for touching faces or coincident edges. For plain solids, a B-rep with [regularized Booleans](/solid-boolean-operations/) is smaller and faster. For linear objects with exact arithmetic, the Nef structure is the tested implementation of the same idea.

## Pitfalls

- **Overlapping collinear segments.** Two collinear segments that overlap must be split at each other's endpoints, so that both give the same edges. A crossing routine that ignores parallel segments misses this. The code adds every endpoint that lies on a segment as a cut, and stores edges with sorted endpoints, so duplicates merge.
- **Holes and isolated points.** A face can have several boundary cycles, and an isolated point has no cycle. The face around them must be found by containment, not from the half-edge structure alone, or the hole joins the wrong face.
- **Sampling a face.** The centroid of an outer cycle need not lie in the face: the face may be non-convex or have holes. Move off a boundary edge along its normal, and stop before the first crossing, as the code does.
- **Over-simplification.** Removing a vertex between two collinear edges is safe only if the edges carry the same mark as the vertex. Removing a vertex where edges bend changes the geometry, even if all marks agree.
- **Inexact arithmetic.** The marks depend on exact containment of sample points in cells. With floating point, a sample may land on the wrong side of a nearby edge. Use rational coordinates, or exact predicates as in [exact geometric computation](/exact-geometric-computation/).
- **Growth without simplification.** Each overlay adds all edges of both operands. Without simplification, the complex grows with the length of the modeling history, not with the complexity of the object.

## Implementations

## History

Rossignac and O'Connor, at IBM Research, circulated the selective geometric complex as a research report in 1989. It was published in the proceedings of an IFIP working conference, *Geometric Modeling for Product Engineering*, edited by Wozny, Turner and Preiss (North-Holland, 1990). The aim was a single dimension-independent model for objects with internal structure and incomplete boundaries. These are the cases of mixed-dimensional models, non-manifold models and models in mid-construction, which the r-sets of Requicha's theory exclude. The SGC came at the same time as other non-manifold representations, such as the radial edge structure of Weiler's 1986 thesis. Rossignac and Requicha then argued, in 1991, for constructive non-regularized geometry built on such sets. The linear case was later made exact and fully implemented as the selective Nef complex of Hachenberger, Kettner and Mehlhorn (2007), building on Walter Nef's 1978 theory of polyhedra.

## References
