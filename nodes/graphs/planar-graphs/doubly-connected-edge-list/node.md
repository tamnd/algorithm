---
tag: 69ZYTE
kind: data-structure
slug: doubly-connected-edge-list
name: Doubly connected edge list
aliases:
- DCEL
- half-edge data structure
area: graphs/planar-graphs
level: core
summary: Half-edge representation of a planar subdivision, supporting face and edge traversal.
model: word-ram
complexity:
  vars:
    n: the number of vertices
    m: the number of edges
  time:
    worst: O(n + m)
  space:
    extra: Θ(n + m)
prereqs: [rotation-system, planar-embedding, planar-face, doubly-linked-list]
see_also: [planar-subdivision, polygon-mesh, triangulation, delaunay-triangulation, planar-dual-graph, euler-formula, adjacency-list, boyer-myrvold-planarity-test]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, Line Segment Intersection, Section 2.2, The doubly-connected edge list
  - paper: "David E. Muller and Franco P. Preparata, Finding the intersection of two convex polyhedra, Theoretical Computer Science 7(2), 217 to 236 (1978)"
    locator: the doubly connected edge list as the representation of a polyhedron
  - paper: "Leonidas Guibas and Jorge Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 74 to 123 (1985)"
    locator: the quad-edge structure and its two operations MakeEdge and Splice
  - paper: "Bruce G. Baumgart, A polyhedron representation for computer vision, AFIPS National Computer Conference, 1975"
    locator: the winged-edge representation of a polyhedron
  - book: "Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001"
    locator: Chapter 3, Embeddings of graphs in surfaces (rotation systems and the face tracing of a combinatorial embedding)
---

A doubly connected edge list (DCEL) stores a connected [plane graph](/planar-embedding/) as a set of half-edges: each edge becomes two directed half-edges, one for each side, and each half-edge points to its twin, to the next and previous half-edges around its [face](/planar-face/), to its origin vertex and to its face. With these pointers one can walk around a face, walk around a vertex, and add or remove an edge inside a face, each in time proportional to the part of the graph that changes or is reported. It is the standard representation of [planar subdivisions](/planar-subdivision/) in computational geometry and of [polygon meshes](/polygon-mesh/) in graphics. On this page the embedding is given combinatorially, as a [rotation system](/rotation-system/) (the counterclockwise order of the neighbours of each vertex); coordinates, if any, are only extra data on the vertices.

## In plain words

Think of each road on a map as two lanes, one in each direction, and drive so that the region you are passing is always on your left. Each lane knows the lane that comes after it on the way around its region, the lane that came before, the lane going the other way on the same road, the crossing where it starts, and the region on its left.

With this, you can drive all the way around a region by following "next". You can list the roads at a crossing in order by switching between "previous" and "the other way". To build a new road across a region, you connect four lanes, and the region splits in two. To remove a road between two regions, you connect the lanes around it again, and the two regions join.

## The abstract type

The structure represents a connected plane graph $G = (V, E)$ up to the topology of its drawing, that is, its combinatorial embedding. Loops and parallel edges are excluded on this page. The operations are:

- $\mathrm{BUILD}(rot)$: make the structure from a rotation system $rot$, where $rot[u]$ lists the neighbours of $u$ in counterclockwise order. The faces of the structure are the face orbits of $rot$.
- $\mathrm{NEIGHBOURS}(v)$: the neighbours of $v$ in counterclockwise order.
- $\mathrm{FACE\text{-}BOUNDARY}(f)$: the half-edges of face $f$ in order, with $f$ on their left.
- $\mathrm{SPLIT\text{-}FACE}(a, b)$: for two half-edges $a \ne b$ on the same face, with $origin[a] \ne origin[b]$ not adjacent, add the edge from $origin[a]$ to $origin[b]$ through that face. The face splits into two.
- $\mathrm{ADD\text{-}LEAF}(a)$: add a new vertex in the face of $a$ and join it to $origin[a]$.
- $\mathrm{JOIN\text{-}FACES}(h)$: if the two sides of the edge of $h$ are different faces, delete the edge. The two faces merge into one.

Each operation keeps the graph connected and plane, so [Euler's formula](/euler-formula/) $n - m + f = 2$ holds after every operation.

## Representation

Half-edges are the integers $0, 1, \ldots, 2m - 1$. The two half-edges of an edge are $2i$ and $2i + 1$, so $twin(h) = h \oplus 1$ needs no storage. For each half-edge $h$ from $u$ to $v$:

| field | meaning |
|---|---|
| $origin[h]$ | the vertex $u$ |
| $next[h]$ | the half-edge after $h$ on the face to the left of $h$; it starts at $v$ |
| $prev[h]$ | the half-edge before $h$ on that face; it ends at $u$ |
| $face[h]$ | the face to the left of $h$ |

For each vertex $v$, $vertex\_edge[v]$ is one half-edge out of $v$, or nil if $v$ has no edge. For each face $f$, $face\_edge[f]$ is one half-edge of $f$. The target of $h$ is $origin[twin(h)]$. The arrays $next$ and $prev$ are inverse permutations of the half-edges, and their cycles are the faces. This is the half-edge form of de Berg and others (Section 2.2), without coordinates and without the hole lists that a disconnected subdivision needs.

The rotation system is stored implicitly. The half-edge after $h$ around $origin[h]$ in counterclockwise order is $twin(prev[h])$: the face to the left of $h$ lies between $h$ and the next half-edge counterclockwise, and $prev[h]$ enters $origin[h]$ along that next edge.

## Operations

```pseudo id=main
BUILD(rot)                                ▷ rot[u]: the neighbours of u, counterclockwise
L1  for each vertex u, each v in rot[u] such that (u, v) has no half-edge yet do
L2      create half-edge h from u to v and twin(h) from v to u
L3  for each half-edge h from u to v do
L4      w ← the neighbour just before u in rot[v]; next[h] ← (v, w); prev[(v, w)] ← h
L5  for each half-edge h with face[h] = nil do
L6      f ← new face; face_edge[f] ← h; for g ← h, next[h], ... until back at h do face[g] ← f

NEIGHBOURS(v)
L7  h ← vertex_edge[v]
L8  repeat output origin[twin(h)]; h ← twin(prev[h]) until h = vertex_edge[v]

FACE-BOUNDARY(f)
L9  h ← face_edge[f]; repeat output h; h ← next[h] until h = face_edge[f]

SPLIT-FACE(a, b)                          ▷ link(x, y) means next[x] ← y; prev[y] ← x
L10 f ← face[a]; create h from origin[a] to origin[b], and t = twin(h)
L11 link(prev[a], h); link(h, b); link(prev[b], t); link(t, a)
L12 g ← new face; face[x] ← g for each x on the cycle of h; face[t] ← f; face_edge[g] ← h; face_edge[f] ← t

ADD-LEAF(a)
L13 create vertex w; h from origin[a] to w; t = twin(h); link(prev[a], h); link(h, t); link(t, a)

JOIN-FACES(h)                             ▷ requires face[h] ≠ face[twin(h)]
L14 t ← twin(h); face[x] ← face[t] for each x on the cycle of h
L15 link(prev[h], next[t]); link(prev[t], next[h]); repair vertex_edge and face_edge; free h, t and face of h
```

**Build.** Line L4 is the face tracing rule of the [rotation system](/rotation-system/): a walk that keeps the face on its left arrives at $v$ from $u$ and leaves along the neighbour that comes just before $u$ in counterclockwise order, which is the first edge clockwise from $u$. Lines L5 and L6 give a number to each cycle of $next$.

**Walks.** Line L8 turns around $v$ counterclockwise, and line L9 goes once around a face. Both stop when they return to the start, after $\deg(v)$ or $|f|$ steps.

**Split.** Before the split, the cycle of face $f$ reads $a, \ldots, prev[b], b, \ldots, prev[a]$. Line L11 cuts it into two cycles, $h, b, \ldots, prev[a]$ and $t, a, \ldots, prev[b]$. In the drawing, the new edge is an arc through the face from $origin[a]$ to $origin[b]$. Line L12 relabels the half-edges of the new face.

**Add a leaf.** The new edge goes into the face of $a$ at $origin[a]$, just before $a$, and the face cycle becomes $\ldots, prev[a], h, t, a, \ldots$. The number of faces does not change.

**Join.** The two cycles $h, next[h], \ldots, prev[h]$ and $t, next[t], \ldots, prev[t]$ become the one cycle $next[h], \ldots, prev[h], next[t], \ldots, prev[t]$. If $vertex\_edge$ of an end pointed to $h$ or $t$, it moves to the next half-edge around that end.

## Example

Take $K_4$ drawn with vertex 0 at $(0, 0)$, 1 at $(4, 0)$, 2 at $(2, 3)$ and 3 at $(2, 1)$, inside the triangle. Sorting the neighbours of each vertex by angle gives the rotation system $rot = [[1, 3, 2], [2, 3, 0], [0, 3, 1], [0, 1, 2]]$. BUILD numbers the half-edges in the order of line L1:

| $h$ | from, to | $next[h]$ | $prev[h]$ | $face[h]$ |
|---|---|---|---|---|
| 0 | 0, 1 | 8 | 3 | 0 |
| 1 | 1, 0 | 4 | 7 | 1 |
| 2 | 0, 3 | 11 | 5 | 2 |
| 3 | 3, 0 | 0 | 8 | 0 |
| 4 | 0, 2 | 7 | 1 | 1 |
| 5 | 2, 0 | 2 | 11 | 2 |
| 6 | 1, 2 | 10 | 9 | 3 |
| 7 | 2, 1 | 1 | 4 | 1 |
| 8 | 1, 3 | 3 | 0 | 0 |
| 9 | 3, 1 | 6 | 10 | 3 |
| 10 | 2, 3 | 9 | 6 | 3 |
| 11 | 3, 2 | 5 | 2 | 2 |

For half-edge 0, from 0 to 1, line L4 looks at $rot[1] = [2, 3, 0]$: the neighbour before 0 is 3, so $next[0]$ is the half-edge from 1 to 3, which is 8. The four faces are the vertex cycles $0, 1, 3$ and $0, 3, 2$ and $1, 2, 3$, the three inner triangles in counterclockwise order, and $1, 0, 2$, the outer face, which the walk goes around clockwise. So $n - m + f = 4 - 6 + 4 = 2$.

NEIGHBOURS(0) starts at $vertex\_edge[0] = 4$ (to vertex 2), then goes to $twin(prev[4]) = twin(1) = 0$ (to vertex 1), then to $twin(prev[0]) = twin(3) = 2$ (to vertex 3), and stops. The output $2, 1, 3$ is $rot[0]$ up to rotation.

JOIN-FACES(11) deletes the edge from 3 to 2. Faces 2 and 3 merge into the quadrilateral $3, 1, 2, 0$, and the graph has 3 faces: $4 - 5 + 3 = 2$.

## Correctness

The structure keeps five invariants: $next$ and $prev$ are inverse permutations of the live half-edges; $origin[next[h]] = origin[twin(h)]$; $face$ is constant exactly on the cycles of $next$, and $face\_edge[f]$ lies on face $f$; $vertex\_edge[v]$ starts at $v$; and the rotation read by line L8 is the rotation of a drawing of a connected plane graph whose faces are the cycles of $next$. BUILD sets them up by the face tracing rule, and each update rewires four pointers so that one face cycle splits in two, or two merge into one, which is exactly what drawing or erasing an arc inside a face does. JOIN-FACES keeps the graph connected because an edge with two different faces on its sides lies on a cycle, which follows from [Euler's formula](/euler-formula/) for several components. Every loop walks a cycle of a permutation and stops when it returns to its start. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst-case time |
|---|---|
| twin, next, prev, origin, face | $O(1)$ |
| BUILD | $O(n + m)$, given for each entry of $rot[u]$ the position of $u$ in the list of the neighbour |
| NEIGHBOURS($v$) | $O(\deg(v))$ |
| FACE-BOUNDARY($f$) | $O(|f|)$, the number of half-edges of $f$ |
| ADD-LEAF | $O(1)$ |
| SPLIT-FACE($a$, $b$) | $O(|g|)$ for the new face $g$, to relabel it |
| JOIN-FACES($h$) | $O(|face(h)|)$, to relabel it |

Space is $\Theta(n + m)$ words: four fields for each of the $2m$ half-edges, one for each vertex and one for each face, with $f \le 2n$ faces by Euler's formula when $n \ge 3$. If the rotation system is given only as neighbour lists, BUILD needs a dictionary from pairs $(u, v)$ to half-edges, and the time is $O(n + m)$ expected with a [hash table](/hash-table/) or $O((n + m) \log n)$ with sorting. The Python code uses a dictionary.

Face labels are the only reason that SPLIT-FACE and JOIN-FACES are not $O(1)$. Without the $face$ field, both take constant time, and the face of a half-edge is found by a walk.

## Variants

- **Faces with holes.** For a disconnected subdivision, each face stores one half-edge of its outer boundary and a list of one half-edge for each inner boundary (hole). This is the full form in de Berg and others, Section 2.2, used for map overlay.
- **Relabel the smaller face.** SPLIT-FACE can walk the two new cycles in parallel and relabel the shorter one, so the cost is $O(\min(|g|, |f|))$.
- **Original DCEL.** Muller and Preparata stored one record per edge, with its two vertices, its two faces and the next edge around each end. The half-edge form splits this record in two.
- **Quad-edge.** Guibas and Stolfi store each edge with its dual edge, so the same structure is also the [planar dual](/planar-dual-graph/), and two operations (MakeEdge and Splice) build every subdivision of an orientable surface.
- **Winged-edge.** Baumgart's structure stores, for each edge, its two ends, its two faces and four neighbouring edges; it is the older form used in solid modeling.
- **Combinatorial maps.** Dropping the planarity check gives a map on any orientable surface: the same arrays represent an embedding of genus $g$ with $n - m + f = 2 - 2g$ (see [graph genus](/graph-genus/)).

## When to use it

Use a DCEL when an algorithm walks along faces or around vertices of a plane graph, or edits the embedding: [triangulation](/triangulation/) and [Delaunay](/delaunay-triangulation/) codes, map overlay, mesh processing, the output of a planarity test such as the [Boyer-Myrvold test](/boyer-myrvold-planarity-test/), and the construction of the [planar dual](/planar-dual-graph/). If the algorithm only needs the neighbours of each vertex and not the faces, an [adjacency list](/adjacency-list/) is smaller.

## Pitfalls

- **Turning the wrong way.** If line L4 takes the neighbour after $u$ instead of before, the walk keeps the face on its right. Both conventions work, but the face walk and the vertex walk of line L8 must agree, or the faces come out wrong.
- **No embedding check.** BUILD accepts any rotation system, also one of $K_5$. Then the cycles of $next$ are faces of an embedding on a surface of higher genus. The test $n - m + f = 2$ tells whether the rotation system is plane.
- **Disconnected input.** Face tracing on a graph with $c$ components gives $c$ separate outer cycles. A plane drawing has only one outer face, so a disconnected subdivision needs hole lists.
- **Bridges.** Both sides of a bridge (and of every edge of a tree) lie on the same face, so JOIN-FACES does not apply. Deleting a bridge disconnects the graph.
- **Stale pointers after deletion.** After JOIN-FACES, $vertex\_edge$ and $face\_edge$ must not point to the deleted half-edges.
- **Isolated vertex.** A single vertex has no half-edge. Its only face has an empty boundary.

## Implementations

The Python class numbers half-edges so that the twin of $h$ is $h \oplus 1$ and keeps the fields in lists. BUILD uses a dictionary from pairs to half-edges. A method checks all invariants and Euler's formula. The tests build $K_4$, the cube, a tree and a single vertex, show that rotation systems of $K_5$ and $K_{3,3}$ fail the Euler check, build random straight-line drawings and compare the faces with an independent face tracer, and run random sequences of ADD-LEAF, SPLIT-FACE and JOIN-FACES.

## History

Baumgart introduced the winged-edge structure for polyhedra in 1975. Muller and Preparata named the doubly connected edge list in 1978, in an algorithm that intersects two convex polyhedra. Guibas and Stolfi introduced the quad-edge structure in 1985, which handles a subdivision and its dual together. The half-edge form with faces and hole lists is the one in the textbook of de Berg, Cheong, van Kreveld and Overmars.

## References
