---
tag: QS04RA
kind: problem
slug: solid-boolean-operations
name: Boolean operations on solids
aliases:
- solid Booleans
- solid set operations
area: cad/solid-modeling
level: core
summary: Given two solids as boundary representations, compute the B-rep of their regularized union, intersection or difference.
prereqs: [boundary-representation, regularized-set-operations, r-set]
see_also: [boundary-evaluation, vertex-neighborhood-classification, constructive-solid-geometry, mesh-boolean-operations, polygon-clipping, geometric-robustness-problem, surface-surface-intersection, radial-edge-data-structure]
sources:
  - paper: doi:10.1109/PROC.1985.13108
    title: Aristides A. G. Requicha and Herbert B. Voelcker, Boolean operations in solid modeling, boundary evaluation and merging algorithms, Proceedings of the IEEE 73(1), 30 to 44, 1985
    locator: the whole paper (the statement of the problem for B-reps and CSG trees, and the generate, classify and merge scheme)
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the definition of solids as r-sets, the regularized operations, and the conversion between representations
  - paper: doi:10.1145/7529.7530
    title: Martti Mäntylä, Boolean operations of 2-manifolds through vertex neighborhood classification, ACM Transactions on Graphics 5(1), 1 to 29, 1986
    locator: the whole paper (Booleans on B-reps of manifold solids, with the degenerate cases of coincident faces, edges and vertices)
  - paper: doi:10.1109/38.41469
    title: Christoph M. Hoffmann, John E. Hopcroft and Michael S. Karasick, Robust set operations on polyhedral solids, IEEE Computer Graphics and Applications 9(6), 50 to 59, 1989
    locator: the whole paper (Booleans on polyhedra in floating point with consistent decisions)
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: Chapter 3, Boolean operations on boundary representations
  - paper: doi:10.1137/0221041
    title: Bernard Chazelle, An optimal algorithm for intersecting three-dimensional convex polyhedra, SIAM Journal on Computing 21(4), 671 to 696, 1992
    locator: the whole paper (the intersection of two convex polyhedra in linear time)
---

The Boolean operation problem on solids asks for the boundary of the union, intersection or difference of two solids, given by their boundaries. The operations are the regularized ones of [regularized set operations](/regularized-set-operations/), so the result is again a solid, with no dangling faces or edges. It is the core operation of a B-rep modeler: drilling a hole is a difference, and adding a boss is a union. The output can have size proportional to the product of the input sizes, and arbitrarily small changes of the input can change the topology of the output, which is why the problem is hard to solve robustly in floating point.

## In plain words

You have two solid objects stored by their skins: the faces, edges and corners on the outside. You want the skin of a new object: everything in either one, the part they share, or the first one with the second one cut out.

The new skin is made of pieces of the old skins. The task is to find where the two skins cross, cut them there, keep the right pieces, and join the pieces into a closed skin.

Two things make this harder than it sounds. When two objects touch along a face or an edge, the rules must say exactly what happens to the shared part. And a computer that rounds its numbers can decide that a corner is on both sides of a face at once.

## Definition

**Input.** Two solids $A$ and $B$ in $E^3$, each an [r-set](/r-set/) (a bounded, closed, regular and semianalytic set), given as a valid [boundary representation](/boundary-representation/): faces with an outward orientation, their bounding loops of edges, and the vertices, with the adjacency between them. An operation $\mathrm{op} \in \{\cup^*, \cap^*, -^*\}$.

**Output.** A valid B-rep of the solid $C = A \mathrm{\ op\ } B$, where $X \cup^* Y = \operatorname{cl} \operatorname{int}(X \cup Y)$, $X \cap^* Y = \operatorname{cl} \operatorname{int}(X \cap Y)$ and $X -^* Y = \operatorname{cl} \operatorname{int}(X - Y)$. Valid means that the faces cover $\partial C$, that they meet only along edges and vertices, that each face is oriented with $C$ on its inner side, and that the face, edge and vertex records agree with each other. $C$ can be empty.

**Constraints.** The output describes the exact set $C$. Two coplanar neighboring faces may be merged into one face or left as two faces; both are valid, but the merged form is the canonical one. The input can be degenerate: faces can be coplanar, solids can touch along faces, edges or vertices, and a vertex of one solid can lie on a face of the other. These cases are part of the problem, not an exception to it.

**Size.** Let $n$ and $m$ be the total number of vertices, edges and faces of $A$ and $B$. The output size is measured in the same way.

**Model.** The [real RAM](/real-ram/) with exact signs for the upper bounds. The polyhedral case is the base case. For curved faces the input also includes the surfaces, and the edges of $C$ include the intersection curves of [surface surface intersection](/surface-surface-intersection/).

## Variants

- **CSG input.** The input is a [CSG](/constructive-solid-geometry/) tree of primitives, and the output is the B-rep of the whole tree. This is the conversion problem solved by [boundary evaluation](/boundary-evaluation/). A Boolean of two B-reps is the case of a tree with one inner node and two leaves.
- **Plain set operations.** Without regularization, the intersection of two cubes that share a face is that face, and the result is not a solid. Some systems keep these lower-dimensional parts on purpose, which needs a non-manifold data structure such as the [radial edge structure](/radial-edge-data-structure/).
- **Manifold output.** The regularized union of two manifold solids can be non-manifold, for example two cubes that share one edge. A system that stores only [manifold solids](/manifold-solid/) must reject such a result or split it.
- **Convex polyhedra.** The intersection of two convex polyhedra is a convex polyhedron of size $O(n + m)$. The union and the difference of convex polyhedra are not convex.
- **Many operands.** The union of $k$ solids at once, which avoids building the intermediate results.
- **Meshes.** The input is a triangle mesh that can be open or self-intersecting, and the inside is defined by a winding number. See [mesh Boolean operations](/mesh-boolean-operations/).
- **The plane.** Booleans on polygons, the problem of [polygon clipping](/polygon-clipping/).

## Examples

All results below are regularized and can be checked by hand. For each B-rep the counts $V$, $E$, $F$ of vertices, edges and faces obey the [Euler-Poincaré formula](/euler-poincare-formula/), here $V - E + F = 2s$ for $s$ shells without holes or handles.

**Two overlapping cubes.** $A = [0, 2]^3$ and $B = [1, 3]^3$, each with volume $8$.

| result | volume | $V$ | $E$ | $F$ | faces |
|---|---|---|---|---|---|
| $A \cup^* B$ | $15$ | $20$ | $30$ | $12$ | 6 squares and 6 L-shaped hexagons |
| $A \cap^* B$ | $1$ | $8$ | $12$ | $6$ | the cube $[1, 2]^3$ |
| $A -^* B$ | $7$ | $14$ | $21$ | $9$ | 3 squares of side 2, 3 L-shaped hexagons, 3 unit squares |

The union has the 7 corners of $A$ outside $B$, the 7 corners of $B$ outside $A$, and 6 new vertices where an edge of one cube passes through a face of the other, such as $(1, 2, 2)$. The difference has the 7 corners of $A$, the same 6 new vertices, and the corner $(1, 1, 1)$ of $B$, which is the inner corner of the notch.

**Two touching cubes.** $D = [0, 1]^3$ and $D' = [1, 2] \times [0, 1]^2$ share the face $x = 1$. The union is the box $[0, 2] \times [0, 1]^2$ with volume $2$ and, after merging, $6$ faces; the shared face is not on its boundary. The intersection is empty, although the plain intersection is the square $\{1\} \times [0, 1]^2$. The difference $D -^* D'$ is $D$.

**Two cubes that share an edge.** $[0, 1]^3$ and $[1, 2] \times [1, 2] \times [0, 1]$ meet along the segment $x = y = 1$. The union is a solid with volume $2$ whose boundary is not a 2-manifold along that segment, where four faces meet.

**A cavity.** $A = [0, 3]^3$ and $B = [1, 2]^3$. Then $A -^* B$ has volume $26$ and two shells, the outer cube and the inner cube with its faces turned inward. $V = 16$, $E = 24$, $F = 12$, and $V - E + F = 4 = 2 \cdot 2$.

## Known algorithms

- **[Boundary evaluation](/boundary-evaluation/)** (Requicha and Voelcker). Cut each face of each solid by the other solid, classify each piece as on the boundary of the result or not, and keep the boundary pieces with the right orientation. It handles CSG trees and the degenerate cases by its side rules. The page proves it correct and gives $O(m^4)$ time for convex primitives with $m$ face planes in all, which is far from tight for real models.
- **[Vertex neighborhood classification](/vertex-neighborhood-classification/)** (Mäntylä). Generate the crossing points of the two boundaries, classify the neighborhood of each vertex of the crossing, and connect the kept edges into faces. It works on two B-reps and makes each in, out or on decision from one vertex neighborhood, which handles coincident faces and edges locally. The page gives $O(n^2 \log n)$ time for the planar version with $n$ edges.
- **[Set membership classification](/set-membership-classification/)** (Tilove). The classification of a point, segment or face against a solid as in, out or on. It is the classify step of both methods above, and its correctness gives their correctness.
- **Convex polyhedra.** Chazelle computes $A \cap B$ for two convex polyhedra in $O(n + m)$ time, which is optimal.
- **Mesh methods.** [Mesh arrangements](/mesh-arrangements/) build the full arrangement of the two triangle meshes, label each cell with winding numbers, and extract the boundary of the cells that the operation selects.
- **Robust floating point.** Hoffmann, Hopcroft and Karasick give a polyhedral Boolean in floating point that derives each uncertain decision from the decisions it has already made, so that the result is consistent. Exact arithmetic is the other route; see [exact geometric computation](/exact-geometric-computation/).

## Bounds

**Output size.** The output can have $\Theta(nm)$ size, and no more. *Upper bound.* Each vertex of $C$ is a vertex of $A$ or $B$, or the meeting point of an edge of one solid with a face of the other, or, in degenerate input, the meeting point of two edges. A segment that is not in a plane meets the plane in at most one point, so there are $O(nm)$ vertices. Each face of $C$ lies in one face of $A$ or $B$, and the pieces of each input face form a planar graph, so the edges and faces are also $O(nm)$. *Lower bound.* Let $A$ be a comb: the base $[0, 2k] \times [0, 2k] \times [0, 1]$ with $k$ teeth $[2i, 2i + 1] \times [0, 2k] \times [1, 2]$. It has $4k + 4$ faces. Let $B$ be the same comb turned by a right angle and hung from above: the base $[0, 2k]^2 \times [2, 3]$ with teeth $[0, 2k] \times [2j, 2j + 1] \times [1, 2]$. Then $A \cap^* B$ is the $k^2$ disjoint unit cubes $[2i, 2i + 1] \times [2j, 2j + 1] \times [1, 2]$, with $6k^2$ faces, since the contacts at $z = 1$ and $z = 2$ have no volume. So every algorithm that writes the output takes $\Omega(nm)$ time in the worst case.

**Convex case.** The intersection of two convex polyhedra has $O(n + m)$ size, and the bound of Chazelle is optimal.

**Discontinuity.** The output is not a continuous function of the input. Move $D'$ in the touching example by $\delta$ along $x$. For every $\delta > 0$ the union has two shells, and for $\delta \le 0$ it is one box. For every $\delta < 0$ the intersection is a thin box with $6$ faces, and for $\delta \ge 0$ it is empty. Any arbitrarily small rounding error at such an input can change the combinatorial answer, and CAD models contain such inputs on purpose. This is the [geometric robustness problem](/geometric-robustness-problem/) in its sharpest form.

The bounds above are proved. The running times of practical Boolean codes, which use bounding boxes and spatial indexes to skip most pairs of faces, are measured, not proved.

## Reductions

- **From polygon Booleans.** For polygons $P$ and $Q$, $(P \times [0, 1]) \mathrm{\ op\ } (Q \times [0, 1]) = (P \mathrm{\ op\ } Q) \times [0, 1]$, with the regularized operations on both sides. So a solid Boolean solves [polygon clipping](/polygon-clipping/) with a constant factor more work.
- **To CSG boundary evaluation and back.** A CSG tree is evaluated by one Boolean for each inner node, from the leaves up. A Boolean of two B-reps is the evaluation of a tree with one inner node.
- **Interference detection.** Two parts of an assembly collide exactly when $A \cap^* B \ne \emptyset$. This decision problem reduces to the Boolean, but it is easier, since it needs only one witness point.
- **Mass properties of a combination.** The volume of $A \cap^* B$ is a [mass property](/mass-properties-of-solids/) of the Boolean result.

## Applications

- **Feature modeling.** Holes, pockets, slots and fillets of a mechanical part are differences and unions with simple tool solids.
- **Machining simulation.** The stock after a cut is the stock minus the volume swept by the tool.
- **Assembly checks.** The interference of two parts is their intersection.
- **3D printing and meshes.** The union of the parts of a model gives one printable surface.
- **Conversion.** Boundary evaluation turns CSG models into B-reps for display, meshing and analysis.

## References
