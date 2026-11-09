---
tag: 77AC3G
kind: data-structure
slug: quad-edge-data-structure
name: Quad-edge data structure
aliases:
- Guibas-Stolfi quad-edge
- quad-edge structure
- quad edge
area: geometry/triangulations
level: advanced
summary: Edge-based representation of planar subdivisions, used for triangulations and Voronoi diagrams.
model: real-ram
complexity:
  vars: {n: the number of edges}
  time: {worst: O(1)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [planar-subdivision, planar-dual-graph, triangulation, euler-formula]
see_also: [guibas-stolfi-algorithm, delaunay-triangulation, edge-flip, lawson-flip-algorithm, bowyer-watson-algorithm, triangulation-dual-tree, linked-list, kirkpatrick-point-location]
sources:
  - paper: doi:10.1145/282918.282923
    title: Leonidas Guibas and Jorge Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 74 to 123 (1985)
    locator: Sections 2 to 4 (the edge algebra, the quad-edge representation, MakeEdge and Splice) and Section 9 (Connect, DeleteEdge and Swap in the Delaunay algorithm)
  - paper: "Dani Lischinski, Incremental Delaunay triangulation, in Graphics Gems IV, Academic Press, 47 to 59 (1994)"
    locator: a compact implementation of quad-edges with Connect, DeleteEdge and Swap
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Section 2.2 (the doubly-connected edge list, the closest relative) and the notes of Chapter 2
  - url: https://www.cs.cmu.edu/afs/andrew/scs/cs/15-463/2001/pub/src/a2/quadedge.html
    title: Paul Heckbert, Quad-edge data structure notes, Carnegie Mellon University
    locator: the description of Rot, Onext and Splice with figures (to be checked)
---

The quad-edge data structure, introduced by Leonidas Guibas and Jorge Stolfi in 1985, represents a [planar subdivision](/planar-subdivision/) and its [dual](/planar-dual-graph/) at the same time. Each edge is stored as a group of four directed edges: the two directions of the edge itself and the two directions of the dual edge, which crosses it and joins the faces on its two sides. Every directed edge keeps one pointer, Onext, to the next edge counterclockwise around its origin. Everything else, the faces, the destination, the dual, is reached by a fixed algebra of rotations, and the whole structure is changed by only two primitives, MakeEdge and Splice. It is the usual structure for divide and conquer [Delaunay triangulation](/guibas-stolfi-algorithm/) and for flip-based algorithms.

## In plain words

Think of each edge of a map as a small cross: the edge itself, and a second short edge that crosses it and joins the two regions on its sides. Each of the four arms of the cross points to the next arm around its corner or its region. From any arm you can walk around a corner, around a region, or across to the other side of the map by following these pointers.

Only two changes are ever needed: make a new free edge, and splice two edges together at a corner, which either joins two corners into one or splits one into two. Adding an edge across a region, deleting an edge and flipping a diagonal are all built from these.

## The abstract type

A subdivision of an orientable surface, here the plane, given by its edges. Each edge $e$ has an origin $\mathrm{Org}(e)$, a destination $\mathrm{Dest}(e)$, a left face and a right face, and the operations:

- **Rot, Sym, Rot$^{-1}$.** Rotate a directed edge by a quarter turn to the dual edge pointing from its right face to its left face; Sym reverses the edge.
- **Onext, Oprev.** The next edge counterclockwise, or clockwise, around the origin.
- **Lnext, Rnext, Dnext and so on.** The next edge around the left face, the right face, the destination; all derived.
- **MakeEdge.** A new edge, alone, forming a subdivision of the sphere with one vertex at each end and one face.
- **Splice(a, b).** Merge or split the rings around the origins of $a$ and $b$, and at the same time the rings around their left faces.
- **Connect(a, b), DeleteEdge(e), Flip(e).** Derived operations: add an edge from $\mathrm{Dest}(a)$ to $\mathrm{Org}(b)$ inside their common left face, remove an edge, and swap a diagonal.

## Representation

Directed edges are numbered $e = 4q + r$ with $r \in \{0, 1, 2, 3\}$: $q$ names the undirected edge, $r = 0, 2$ are its two directions and $r = 1, 3$ are the two directions of the dual edge. Then

$$\mathrm{Rot}(4q + r) = 4q + ((r + 1) \bmod 4), \qquad \mathrm{Sym}(e) = \mathrm{Rot}^2(e),$$

so Rot and Sym cost one bit operation and are never stored. One array holds $\mathrm{Onext}(e)$ for every directed edge, and another holds the origin of each primal directed edge (the dual ones could hold face labels). All other maps come from these by the rules

$$\mathrm{Oprev}(e) = \mathrm{Rot}(\mathrm{Onext}(\mathrm{Rot}(e))), \qquad \mathrm{Lnext}(e) = \mathrm{Rot}(\mathrm{Onext}(\mathrm{Rot}^{-1}(e))),$$

which are valid because the dual Onext pointers mirror the primal ones. The face to the left of $e$ is the cycle $e, \mathrm{Lnext}(e), \mathrm{Lnext}^2(e), \ldots$. Space is four pointers and two vertex fields per edge.

## Operations

```pseudo id=main
L1  Rot(e) = 4·⌊e/4⌋ + ((e+1) mod 4);  Sym(e) = Rot(Rot(e));  Rot⁻¹(e) = Rot(Sym(e))
L2  Oprev(e) = Rot(Onext(Rot(e)));  Lnext(e) = Rot(Onext(Rot⁻¹(e)))
L3  MakeEdge(a, b): q ← number of edges so far; e ← 4q
L4    Onext(e) ← e; Onext(e+1) ← e+3; Onext(e+2) ← e+2; Onext(e+3) ← e+1; Org(e) ← a; Org(e+2) ← b
L5    return e
L6  Splice(a, b): α ← Rot(Onext(a)); β ← Rot(Onext(b))
L7    swap Onext(a) and Onext(b)
L8    swap Onext(α) and Onext(β)
L9  Connect(a, b): e ← MakeEdge(Dest(a), Org(b))
L10   Splice(e, Lnext(a))
L11   Splice(Sym(e), b); return e
L12 DeleteEdge(e): Splice(e, Oprev(e))
L13   Splice(Sym(e), Oprev(Sym(e)))
L14 Flip(e): a ← Oprev(e); b ← Oprev(Sym(e))
L15   Splice(e, a); Splice(Sym(e), b)
L16   Splice(e, Lnext(a)); Splice(Sym(e), Lnext(b))
L17   Org(e) ← Dest(a); Dest(e) ← Dest(b)
L18 Faces: for each unvisited directed edge e, follow Lnext from e until it returns
```

**MakeEdge** (L3 to L5) creates the four directed edges of one undirected edge. The primal directions are alone in their rings, and the two dual directions point to each other, because the new edge has a single face on both sides.

**Splice** (L6 to L8) is the only primitive that changes the topology. If $a$ and $b$ have different origins, it merges the two rings into one, putting $b$'s old successor after $a$ and $a$'s old successor after $b$. If they have the same origin, it splits the ring in two. Line L8 makes the matching change to the dual rings, so the faces are split or merged consistently. Splice is its own inverse.

**Connect** (L9 to L11) adds an edge from $\mathrm{Dest}(a)$ to $\mathrm{Org}(b)$, where $a$ and $b$ border the same face; the face is split in two. **DeleteEdge** (L12, L13) undoes it, and **Flip** (L14 to L17) deletes a diagonal of two triangles and connects the other two corners of the quadrilateral.

## Example

Build the convex hexagon $p_0 = (0,0)$, $p_1 = (4,0)$, $p_2 = (6,2)$, $p_3 = (5,5)$, $p_4 = (2,6)$, $p_5 = (-1,3)$ and triangulate it by a fan from $p_0$.

| step | operation | edges | faces |
|---|---|---|---|
| 1 | MakeEdge for $p_0 p_1, \ldots, p_4 p_5$, splicing each at its shared vertex | 5 | 1 |
| 2 | Connect($p_4 p_5$, $p_0 p_1$) closes the cycle with $p_5 p_0$ | 6 | 2 |
| 3 | Connect($p_1 p_2$, $p_0 p_1$) adds $p_2 p_0$ | 7 | 3 |
| 4 | Connect($p_2 p_3$, $p_0 p_2$) adds $p_3 p_0$ | 8 | 4 |
| 5 | Connect($p_3 p_4$, $p_0 p_3$) adds $p_4 p_0$ | 9 | 5 |

At the end, $V - E + F = 6 - 9 + 5 = 2$. Tracing Lnext from the four triangle faces gives $p_0 p_1 p_2$, $p_0 p_2 p_3$, $p_0 p_3 p_4$, $p_0 p_4 p_5$, with doubled areas $8$, $20$, $20$, $12$, which add up to $60$, the doubled area of the hexagon by the [shoelace formula](/shoelace-formula/). The outer face is the cycle of the six reversed boundary edges. Flipping $p_0 p_3$ then replaces it by $p_2 p_4$ in two Splice pairs, and the counts stay the same.

## Correctness

The structure stores only Onext; the correctness argument is that every primitive keeps the dual Onext pointers equal to what the primal ones require, $\mathrm{Onext}(f) = \mathrm{Rot}^{-1}(\mathrm{Onext}^{-1}(\mathrm{Rot}^{-1}(f)))$ for every dual edge $f$. MakeEdge satisfies it directly. For Splice, swapping $\mathrm{Onext}(a)$ and $\mathrm{Onext}(b)$ changes the required dual pointers exactly at $\alpha = \mathrm{Rot}(\mathrm{Onext}(a))$ and $\beta = \mathrm{Rot}(\mathrm{Onext}(b))$, and the required new values are their old values swapped, which is line L8. From the invariant, Lnext is $\mathrm{Onext}^{-1} \circ \mathrm{Sym}$, so faces are the cycles of a permutation, and Connect splits the common face of $a$ and $b$ into exactly two faces. The full proof, with Connect, DeleteEdge and Flip, is in the proof file.

## Complexity

| operation | time |
|---|---|
| Rot, Sym, Onext, Oprev, Lnext, Org, Dest | $O(1)$ |
| MakeEdge, Splice, Connect, DeleteEdge, Flip | $O(1)$ |
| walk around a vertex or a face of size $k$ | $O(k)$ |
| list all faces | $O(n)$ |

Space is $\Theta(n)$ for $n$ edges: four Onext pointers and the vertex data. Deleted edges leave holes in the arrays unless they are recycled through a free list.

## Variants

- **Doubly-connected edge list (DCEL).** Stores half-edges with twin, next and previous pointers and explicit face records. It handles only the primal subdivision, but it is simpler and more common in textbooks.
- **Winged edge.** Baumgart's 1975 structure for polyhedra, one record per edge with the four neighboring edges; the quad-edge structure is its cleaned-up algebraic version.
- **Half-edge with implicit twins.** Store half-edges in pairs at indices $2k$ and $2k+1$, as in many mesh libraries; it is the quad-edge without the dual half.
- **Triangle-based structures.** For pure triangulations, storing three vertices and three neighbors per triangle, as Shewchuk's Triangle does, uses less memory and is faster.
- **The Flip bit.** Guibas and Stolfi also include a Flip operator for non-orientable surfaces; it is omitted here.

## When to use it

Use it when the algorithm changes the topology a lot and needs both the subdivision and its dual, such as divide and conquer Delaunay triangulation, Voronoi diagrams, and flip algorithms, or when the subdivision may have faces of any size and isolated edges. For a fixed triangle mesh, a triangle-based structure is smaller; for read-only maps a DCEL is enough.

## Pitfalls

- **Onext is not stored for Lnext.** Computing Lnext by walking around a face needs the Rot formula; forgetting the dual pointers in Splice (line L8) breaks every face traversal.
- **Splice on the wrong pair.** Splice of two edges in the same ring splits it; calling Splice where a merge was meant silently disconnects a vertex.
- **Connect needs a common face.** If $a$ and $b$ do not border the same face, Connect produces a structure that is consistent but not planar.
- **Geometry is separate.** The structure stores no coordinates in its topology; it is the caller's job to make sure a new edge does not cross others and that a flipped quadrilateral is convex.
- **Orientation conventions.** Counterclockwise Onext and left faces must match the coordinate system; a mirrored input gives inside-out faces.

## Implementations

The Python version keeps two flat lists, the Onext pointers and the vertex of each directed edge, plus a flag for deleted edges; Rot and Sym are bit operations on indices. It provides MakeEdge, Splice, Connect, DeleteEdge and Flip, the face traversal, and three helpers: building a polygon, triangulating a convex face by a fan, and inserting a point into a face. The tests check the Guibas and Stolfi axioms on every directed edge after every change, Euler's formula, counterclockwise order of the edges around each vertex, the absence of crossings, and that the doubled areas of the faces add up exactly to the doubled area of the outer boundary. On random point sets inside a big triangle they count $2n - 5$ triangles and $3n - 6$ edges, and after Lawson flips they check the empty circle property by brute force. Coordinates are integers or `Fraction`.

## History

Baumgart's winged-edge structure (1975) introduced edge-based representations of polyhedra. Guibas and Stolfi presented the quad-edge structure and its algebra at STOC 1983 and in ACM Transactions on Graphics in 1985, together with the divide and conquer Delaunay algorithm built on it. Lischinski's 1994 Graphics Gems article made it widely used in graphics.

## References
