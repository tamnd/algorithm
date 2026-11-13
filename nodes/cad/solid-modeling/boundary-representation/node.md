---
tag: MR3WHM
kind: data-structure
slug: boundary-representation
name: Boundary representation
aliases:
- B-rep
- BRep
area: cad/solid-modeling
level: intro
summary: Represent a solid by its boundary, a set of faces glued along edges and vertices, with the topology (which faces meet where) stored apart from the geometry (the surfaces and points).
model: word-ram
complexity:
  vars:
    n: the number of half-edges (twice the number of edges)
  time:
    expected: O(n)
  space:
    extra: Θ(n)
prereqs: [r-set, manifold-solid, doubly-connected-edge-list]
see_also: [winged-edge-data-structure, radial-edge-data-structure, euler-operators, euler-poincare-formula, polygon-mesh, solid-boolean-operations, mass-properties-of-solids, constructive-solid-geometry]
sources:
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Chapter 6, Boundary models (p. 101; Section 6.2, Boundary data structures, p. 102; Section 6.2.4, Faces with several boundaries, p. 108; Section 6.3, Validity of boundary models, p. 110), and Chapter 10, Half-edge data structure (p. 161)
  - paper: doi:10.1145/356827.356833
    title: Aristides A. G. Requicha, Representations for rigid solids, theory, methods, and systems, ACM Computing Surveys 12(4), 437 to 464, 1980
    locator: the section on boundary representations, their validity, and the properties of the scheme
  - book: isbn:9781558600676
    title: Christoph M. Hoffmann, Geometric and Solid Modeling, An Introduction, Morgan Kaufmann, 1989
    locator: Chapter 2, Basic Concepts (boundary representation and the face, edge and vertex adjacencies)
  - paper: doi:10.1109/MCG.1985.276271
    title: Kevin Weiler, Edge-based data structures for solid modeling in curved-surface environments, IEEE Computer Graphics and Applications 5(1), 21 to 40, 1985
    locator: the adjacency relations between vertices, edges and faces, and which of them each edge-based structure gives in constant time
  - paper: doi:10.1145/1499949.1500071
    title: Bruce G. Baumgart, A polyhedron representation for computer vision, Proceedings of the AFIPS National Computer Conference 44, 589 to 596, 1975
    locator: the winged-edge polyhedron, the first edge-based boundary structure
---

A boundary representation (B-rep) describes a solid by its skin: a set of faces, each a piece of a surface, glued along edges and at vertices. It stores two kinds of data apart. The *topology* says which vertices bound each edge, which edges bound each face and which faces are next to each other. The *geometry* gives the plane or curved surface of each face, the curve of each edge and the point of each vertex. Almost every commercial CAD kernel stores its solids as B-reps, because a B-rep gives the faces and edges directly for drawing, for machining and for the computation of [mass properties](/mass-properties-of-solids/). This page builds a half-edge B-rep of a polyhedral [manifold solid](/manifold-solid/), with faces that may have holes, and checks that it is valid.

## In plain words

Think of a cardboard box. You can describe the box by its six flat sides and by how the sides are taped together. The B-rep stores exactly this: a list of corners, a list of folds, and a list of sides, and for each side the folds around it.

Each fold is stored twice, once for each side that it touches, as two arrows that point in opposite directions. The arrows of one side go around it counterclockwise when you look at the side from outside the box. With these arrows you can go around a side, cross a fold to the next side, and turn around a corner. A side can also have a hole, for example the top of a block with a peg on it. The hole is one more ring of arrows on the same side.

## The abstract type

The structure stores the boundary of a polyhedral solid, and it answers adjacency queries about it. The cells are the solid, its shells, faces, loops, edges and vertices. A *shell* is a connected part of the boundary, a *face* is a planar polygon, possibly with holes, and a *loop* is one boundary cycle of a face. The first loop of a face is its outer loop, and the other loops are its *rings*. Orientation follows the right-hand rule: when the fingers follow a loop, the thumb points along the outward normal of the face. So the outer loop runs counterclockwise seen from outside, and each ring runs clockwise.

- $\mathrm{BUILD}(P, \mathcal{F})$: make the structure from the points $P$ and the faces $\mathcal{F}$, each face a list of loops of vertex indices.
- $\mathrm{FACE\text{-}BOUNDARY}(f)$: the loops of $f$ as vertex cycles, outer loop first.
- $\mathrm{EDGE\text{-}FACES}(u, v)$: the faces on the left and on the right of the edge from $u$ to $v$.
- $\mathrm{OUTGOING}(v)$: the edges at $v$ in cyclic order, so also the faces and the neighbours of $v$ in that order.
- $\mathrm{ADJACENT\text{-}FACES}(f)$ and $\mathrm{SHELLS}()$: the faces next to $f$, and the connected parts of the boundary.
- $\mathrm{VALIDATE}()$: check that the stored data is the boundary of a manifold solid, as far as the checks of the next sections go, and return the counts $V, E, F, L, R, S, H$ of the [Euler-Poincaré formula for solids](/euler-poincare-formula/).

A B-rep is *unambiguous* in the sense of Requicha: a valid B-rep describes one [r-set](/r-set/). It is not *unique*: a face can be cut into two coplanar faces, and the solid does not change.

## Representation

Each edge is stored as two half-edges, one for each face that uses it, with opposite directions. The records are:

| record | fields |
|---|---|
| half-edge $h$ | $origin[h]$, $twin[h]$ (the other half of the edge), $next[h]$ and $prev[h]$ (the neighbours on the loop), $loop[h]$ |
| loop $\ell$ | $face[\ell]$ and one half-edge $loop\_edge[\ell]$ |
| face $f$ | the list of its loops, outer loop first; in a curved B-rep also the surface |
| vertex $v$ | its point and one half-edge $out[v]$ that starts at $v$ |
| shell, solid | the list of faces of each shell, the list of shells |

The face to the left of $h$ is $face[loop[h]]$, and the target of $h$ is $origin[twin[h]]$. So the structure stores 10 references per edge: 5 for each of its two half-edges. The field $prev$ can be dropped, at the cost of a walk around the loop to find it, which gives 8. This is the half-edge structure of Mäntylä (Chapter 10), and it is the [doubly connected edge list](/doubly-connected-edge-list/) of planar subdivisions with a loop record added between half-edges and faces, so that a face can have more than one boundary.

These queries take $O(1)$ time: the two vertices of an edge, the two faces of an edge, the next and previous edge on a loop, the face of a loop, and the edge across from a half-edge. The edges, faces or neighbours around a vertex take $O(d)$ time for a vertex of degree $d$, and the boundary of a face takes time linear in its number of edges. A plain list of faces, as in an indexed face set, answers only the first of these queries without a search.

The geometry is stored apart. Here each vertex has an exact point with integer or rational coordinates, and the plane of a face is computed from its outer loop by Newell's sum $N_f = \sum_i p_i \times p_{i+1}$. For a planar polygon, $N_f$ is twice its vector area, so it points along the outward normal by the right-hand rule.

## Operations

```pseudo id=main
BUILD(P, faces)                         ▷ each face: loops of vertex indices, outer loop first
L1  for each face f, each loop ℓ of f do
L2      for each pair (u, v) of cyclically adjacent vertices of ℓ do
L3          fail if key[(u, v)] exists; create h; origin[h] ← u; loop[h] ← ℓ; key[(u, v)] ← h
L4      link the half-edges of ℓ in a cycle with next and prev
L5  for each half-edge h with key (u, v) do twin[h] ← key[(v, u)]; fail if there is none
L6  for each half-edge h do if out[origin[h]] = nil then out[origin[h]] ← h

OUTGOING(v)                             ▷ the half-edges out of v in cyclic order
L7  h ← out[v]; repeat output h; h ← twin[prev[h]] until h = out[v]

VALIDATE()
L8  check twin[twin[h]] = h and origin[twin[h]] = origin[next[h]] for each h
L9  for each vertex v: check that OUTGOING(v) has every half-edge that starts at v
L10 the shells ← the components of the faces, linked across twins
L11 for each shell: χ ← V − E + F − R of the shell; check χ ≤ 2 and χ even; H ← H + (2 − χ)/2
L12 for each face: N ← newell(outer loop); check N ≠ 0, all its vertices on the plane, N · newell(ring) < 0 for each ring
L13 check that the volume of each shell is not 0, and that the volume (1/6) Σ_f Σ_loops q_f · newell(loop) > 0
```

**Build.** Lines L1 to L4 make one half-edge for each pair of adjacent vertices of each loop. Line L3 fails if a directed edge comes twice: then a face is reversed, or more than two faces meet at the edge. Line L5 pairs each half-edge with the one that goes the other way, and fails if there is none: then an edge has only one face, and the surface has a gap.

**Around a vertex.** Line L7 is the rotation of the half-edge structure. The half-edge $prev[h]$ ends at $v$ on the face of $h$, and its twin starts at $v$ on the face across that edge. So each step moves to the next face around $v$, across the edge between them.

**Validity.** Line L9 is the vertex condition of a manifold: the faces at $v$ make one fan. Line L11 uses the [Euler-Poincaré formula for solids](/euler-poincare-formula/) in its per-shell form $V - E + F - R = 2 - 2g$: a B-rep does not store $H$, so the formula gives the genus $g$ of each shell, and the check is that this genus is a whole number $g \ge 0$. Line L12 checks, with exact integers, that each face is planar and that its rings turn the other way from its outer loop. Line L13 computes the volume by the divergence theorem: on a planar face $p \cdot n$ is constant, so $\iiint_S 1 \, dV = \frac{1}{3} \oint p \cdot n \, dA = \frac{1}{6} \sum_f q_f \cdot \sum_{\text{loops}} N_\ell$, where $q_f$ is any vertex of $f$. A cavity shell has negative volume, and a solid whose faces all point inward has a negative total.

## Example

Take the unit cube with the vertices $0 = (0, 0, 0)$, $1 = (1, 0, 0)$, $2 = (1, 1, 0)$, $3 = (0, 1, 0)$ and $4$ to $7$ the same points with $z = 1$. The faces, each with one loop counterclockwise from outside, are

| face | loop | outward normal |
|---|---|---|
| 0 | 0, 3, 2, 1 | $-z$ |
| 1 | 4, 5, 6, 7 | $+z$ |
| 2 | 0, 1, 5, 4 | $-y$ |
| 3 | 1, 2, 6, 5 | $+x$ |
| 4 | 2, 3, 7, 6 | $+y$ |
| 5 | 3, 0, 4, 7 | $-x$ |

BUILD makes the 24 half-edges $0, 1, \ldots, 23$ in this order, four per face. Half-edge 0 goes from 0 to 3 on face 0; its twin is half-edge 20, from 3 to 0 on face 5. Half-edge 8 goes from 0 to 1 on face 2, with twin 3 on face 0. So EDGE-FACES(0, 1) is (2, 0): the front face is on the left of the edge from 0 to 1, and the bottom face on its right.

OUTGOING(0) starts at $out[0] = 0$. Then $prev[0] = 3$ (from 1 to 0) and $twin[3] = 8$; then $prev[8] = 11$ (from 4 to 0) and $twin[11] = 21$; then $prev[21] = 20$ and $twin[20] = 0$, the start. The half-edges $0, 8, 21$ go to the neighbours $3, 1, 4$, on the faces $0, 2, 5$: the three faces at the corner, in one fan.

VALIDATE finds one shell with $V - E + F - R = 8 - 12 + 6 - 0 = 2$, so $H = 0$, and returns $V = 8$, $E = 12$, $F = 6$, $L = 6$, $R = 0$, $S = 1$, $H = 0$. The volume is 1. The tests run the same check on three more solids:

| solid | $V$ | $E$ | $F$ | $L$ | $R$ | $S$ | $H$ | volume |
|---|---|---|---|---|---|---|---|---|
| unit cube | 8 | 12 | 6 | 6 | 0 | 1 | 0 | 1 |
| square frame $[0,3]^2 \times [0,1]$ minus the hole $(1,2)^2 \times [0,1]$ | 16 | 24 | 10 | 12 | 2 | 1 | 1 | 8 |
| plate $[0,4]^2 \times [0,1]$ with the block $[1,3]^2 \times [1,2]$ on top | 16 | 24 | 11 | 12 | 1 | 1 | 0 | 20 |
| cube $[0,3]^3$ with the cavity $(1,2)^3$ | 16 | 24 | 12 | 12 | 0 | 2 | 0 | 26 |

In the frame, the top and the bottom faces are square rings, each with an outer loop and one ring, so $R = 2$, and $16 - 24 + 10 - 2 = 0 = 2(1 - 1)$. In the plate with the block, the top face of the plate has the outline of the block as a ring, and the four sides of the block are attached to that ring. In the cube with a cavity, the inner shell has its normals pointing into the cavity, so its volume is $-1$ and the total is $27 - 1 = 26$.

## Correctness

Assume that VALIDATE returns. Then line L8 says that the half-edges pair up into edges with opposite directions, and lines L3 and L5 say that each edge has exactly two faces. Line L9 says that the faces at each vertex form one cycle, so the surface is a closed 2-manifold, and it is oriented because the two faces of each edge use it in opposite directions. If each face is a planar polygon whose rings lie inside its outer loop, then each face is a disk with $k$ holes, and joining each ring to the outer loop by a cut edge gives a decomposition into disks with $R$ more edges; so each shell has Euler characteristic $V - E + F - R$, and the classification of closed orientable surfaces gives $2 - 2g$ with $g$ its genus. So the counts that VALIDATE returns satisfy $V - E + F - (L - F) - 2(S - H) = 0$ with the true $H$. The volume of line L13 is exact by the divergence theorem, and a positive total rules out a solid whose faces all point inward. The queries walk cycles of the permutations $next$ and $h \mapsto twin[prev[h]]$, so they stop and list each item once. The full proof is in the proof file.

VALIDATE does not check that faces of the surface do not cross each other, nor that a ring lies inside its outer loop. A surface with the face lists of the square frame passes all checks even if its points are moved so that two faces cross, as long as each face stays planar and the volume stays positive. A full geometric check needs a test of each pair of faces, and the [solid Boolean operations](/solid-boolean-operations/) and [exact geometric computation](/exact-geometric-computation/) pages discuss those tests.

## Complexity

Let $n$ be the number of half-edges, so $n = 2E$.

- BUILD makes $n$ half-edges and does $2n$ hash-map operations: $O(n)$ expected time and $\Theta(n)$ space.
- Each pointer query takes $O(1)$ time. OUTGOING($v$) takes $O(d)$ time, and FACE-BOUNDARY($f$) takes time linear in the size of $f$.
- VALIDATE takes $O(n)$ time: lines L8 and L9 touch each half-edge a constant number of times, the shell search of line L10 visits each face and each half-edge once, and lines L12 and L13 do a constant number of exact products per half-edge. With integer coordinates of $b$ bits, each product has $O(b)$ bits, so the arithmetic is exact and its cost is polynomial in $b$.

## Variants

- **Winged edge.** The [winged-edge data structure](/winged-edge-data-structure/) stores one record per edge, with its two vertices, its two faces and four neighbouring edges. It uses 8 references per edge, but it must test the orientation of an edge in each step around a face.
- **Radial edge.** The [radial edge data structure](/radial-edge-data-structure/) stores any number of faces around an edge, in angular order, and so it can store non-manifold solids such as two cubes that share an edge.
- **Quad-edge.** The [quad-edge data structure](/quad-edge-data-structure/) stores a subdivision of a surface and its dual at the same time.
- **Faces without rings.** Many mesh structures allow only one loop per face, so a face with a hole must be cut into simpler faces by extra edges. The [polygon mesh](/polygon-mesh/) page gives the face-vertex and half-edge forms of meshes, and the [corner table](/corner-table/) is a compact form for triangle meshes.
- **Curved B-reps.** Faces carry trimmed NURBS or analytic surfaces, edges carry curves, and the topology is the same. The faces of a curved solid are often [trimmed surfaces](/trimmed-surface/).
- **Construction by Euler operators.** Instead of BUILD from a face list, a modeler can make and change a B-rep only by [Euler operators](/euler-operators/), which keep the Euler-Poincaré formula for solids true after each step.

## When to use it

Use a B-rep when the application needs faces, edges and vertices as objects: for drawing with sharp edges, for picking a face in a user interface, for tool paths, for attaching features and dimensions to faces, and for exact mass properties. It is the main representation of mechanical CAD. Use a [CSG tree](/constructive-solid-geometry/) when the solid is built from primitives and the history must be kept, and a [voxel set](/spatial-occupancy-enumeration/) when exact faces do not matter and the shape is noisy, as in medical data. Booleans on B-reps are hard to make robust, and that is the main cost of the representation.

## Pitfalls

- **The formula is not a validity test.** A B-rep can satisfy $V - E + F - (L - F) - 2(S - H) = 0$ and still not be a solid: the formula does not see faces that cross, and it does not see a face that is reversed when the counts are kept. Line L11 is only one check among several.
- **Rings must be counted.** If a face with a hole is stored as one loop that joins the hole to the outer boundary by a doubled edge, the counts change: the doubled edge adds an edge and the ring disappears. Count rings as $R = L - F$, and use faces that are disks with holes.
- **Orientation of the rings.** The outer loop and the rings of a face must turn in opposite directions. If a ring has the direction of the outer loop, the edges of that ring are used twice in one direction, and line L3 fails.
- **A reversed inner shell.** If the shell of a cavity has its normals pointing away from the cavity, the cavity adds volume instead of taking it away, and the total volume is still positive. The sign of the total does not find this error. A check must test a point of each inner shell against the shells around it.
- **Floating point.** The planarity test of line L12 and the volume sign of line L13 are sign tests. With floating-point coordinates, a face that is planar in exact arithmetic can fail the test, and a nearly flat shell can get the wrong sign. Use integer or rational coordinates, or a tolerance that the whole system agrees on.
- **Non-manifold input.** Two cubes that share an edge have an edge with four faces, and two cubes that share a vertex have a vertex with two fans. A half-edge B-rep cannot store either, so the build or the check must reject them, as lines L3 and L9 do.

## Implementations

## History

Baumgart's winged-edge polyhedron of 1972 and 1975 was the first edge-based boundary structure; he made it for computer vision. In the 1970s, the BUILD modeler of Braid's group in Cambridge and other early systems stored solids by their faces, edges and vertices. Requicha's 1980 survey put the boundary representation into his theory of representation schemes, with validity and unambiguity as formal properties. Weiler compared the edge-based structures in 1985 and showed which adjacency queries each one answers in constant time. Mäntylä's book of 1988 gives the half-edge structure with loops that this page uses, and builds a modeler on it with [Euler operators](/euler-operators/).

## References
