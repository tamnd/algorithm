---
tag: 4Q9BTY
kind: data-structure
slug: winged-edge-data-structure
name: Winged-edge data structure
aliases:
- winged edge
- Baumgart winged edge
area: cad/solid-modeling
level: core
summary: Baumgart's B-rep in which each edge stores its two vertices, two faces and four neighbour edges, so edge queries take O(1) time and walks around a face or vertex O(1) per step.
model: word-ram
complexity:
  vars:
    n: the number of edges
  time:
    expected: O(n)
  space:
    extra: Θ(n)
prereqs: [boundary-representation]
see_also: [doubly-connected-edge-list, quad-edge-data-structure, radial-edge-data-structure, euler-operators, polygon-mesh, rotation-system, corner-table, euler-poincare-formula]
sources:
  - paper: doi:10.1145/1499949.1500071
    title: Bruce G. Baumgart, A polyhedron representation for computer vision, Proceedings of the AFIPS National Computer Conference 44, 589 to 596, 1975
    locator: the winged-edge polyhedron, its edge, face and vertex nodes, and the traversals around a face and around a vertex
  - paper: doi:10.1109/MCG.1985.276271
    title: Kevin Weiler, Edge-based data structures for solid modeling in curved-surface environments, IEEE Computer Graphics and Applications 5(1), 21 to 40, 1985
    locator: the winged-edge structure, its sufficiency for the adjacency relations, and the variants with loops and with edge uses
  - book: isbn:9780881751086
    title: Martti Mäntylä, An Introduction to Solid Modeling, Computer Science Press, 1988
    locator: Chapter 6, Boundary models, Section 6.2, Boundary data structures (p. 102), the winged-edge structure and its comparison with the half-edge structure
  - paper: doi:10.1145/282918.282923
    title: Leonidas Guibas and Jorge Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 74 to 123, 1985
    locator: the edge algebra and the quad-edge structure, which store one edge record with its two orientations and its dual
---

The winged-edge data structure stores the boundary of a polyhedral solid with one record per edge. Each edge record holds the two vertices of the edge, the two faces on its two sides and four more edges, the *wings*: the edges before and after it on each of its two faces. Each vertex and each face stores one edge. Bruce Baumgart made it for computer vision in the early 1970s, and it was the first edge-based [boundary representation](/boundary-representation/). From one edge, the program can reach every adjacent vertex, face and edge in $O(1)$ time, and it can walk around a face or around a vertex in $O(1)$ time per step. The price is that an edge does not know in which direction a face uses it, so every step of a walk must test which side of the edge it is on.

## In plain words

Think of each fold of a cardboard box as a small card. The card names the two corners at the ends of the fold and the two sides of the box that meet at it. It also names four more folds. On each of the two sides, it names the fold just before it and the fold just after it, when you go around that side.

To go around one side of the box, start at any fold of that side, look on its card for the fold after it on this side, and move to that fold. To go around a corner, look on the card for the fold just before it on the side that leaves the corner. The four wings around each card give the structure its name.

## The abstract type

The structure stores a closed oriented polyhedral surface whose faces are disks, and it answers adjacency queries about it.

- $\mathrm{BUILD}(n, \mathcal{F})$: make the structure for the vertices $0, \ldots, n - 1$ and the faces $\mathcal{F}$, each a cyclic list of vertices, counterclockwise seen from outside.
- $\mathrm{EDGE\text{-}VERTICES}(e)$ and $\mathrm{EDGE\text{-}FACES}(e)$: the two ends and the two faces of $e$.
- $\mathrm{FACE\text{-}EDGES}(f)$: the edges of $f$ in counterclockwise order, so also its vertices.
- $\mathrm{VERTEX\text{-}EDGES}(v)$: the edges at $v$ in counterclockwise order, so also the neighbours and the faces of $v$.
- $\mathrm{SPLIT\text{-}EDGE}(e)$: put a new vertex inside $e$.
- $\mathrm{SPLIT\text{-}FACE}(f, u, w)$ and $\mathrm{JOIN\text{-}FACES}(e)$: cut $f$ into two faces by a new edge from $u$ to $w$, and remove an edge that has two different faces.

The updates are three of the [Euler operators](/euler-operators/), in the forms that keep one loop per face: SPLIT-EDGE is MEV, SPLIT-FACE is MEF and JOIN-FACES is KEF. Each one keeps $V - E + F$, so the shell keeps its genus.

## Representation

Each edge $e$ has a direction, from $v_{start}[e]$ to $v_{end}[e]$. Seen from outside and walking from $v_{start}$ to $v_{end}$, the face $f_{left}[e]$ is on the left and $f_{right}[e]$ on the right. The faces run counterclockwise seen from outside, so $f_{left}[e]$ uses $e$ from start to end, and $f_{right}[e]$ uses it from end to start.

| record | fields |
|---|---|
| edge $e$ | $v_{start}[e]$, $v_{end}[e]$, $f_{left}[e]$, $f_{right}[e]$ and the four wings $left_{prev}[e]$, $left_{next}[e]$, $right_{prev}[e]$, $right_{next}[e]$ |
| vertex $v$ | its point and one edge $vertex\_edge[v]$ at $v$ |
| face $f$ | one edge $face\_edge[f]$ of $f$; in a curved B-rep also the surface |

The wings $left_{prev}[e]$ and $left_{next}[e]$ are the edges before and after $e$ in the counterclockwise loop of $f_{left}[e]$, and $right_{prev}[e]$ and $right_{next}[e]$ are the same for $f_{right}[e]$. So the topology takes 8 references per edge and one per vertex and per face, $8E + V + F$ in total. The [half-edge](/boundary-representation/) form of the same surface stores 4 or 5 references per half-edge, 8 or 10 per edge, and it adds a loop record when faces have rings.

Baumgart's own edge nodes also hold list links and more fields than these eight; the table gives only the eight that carry the topology, as Weiler and Mäntylä describe them. Some texts call the four wings the clockwise and counterclockwise successors and predecessors, with different conventions for which is which, so read the convention of a source before you copy its code.

The edge record does not say in which direction a face uses the edge. To step to the next edge of face $f$ from edge $e$, the program must test whether $f$ is $f_{left}[e]$ or $f_{right}[e]$. This test needs the two faces of each edge to be different. In the same way, to step around vertex $v$, it must test whether $v$ is $v_{start}[e]$ or $v_{end}[e]$.

## Operations

```pseudo id=main
FACE-EDGES(f)                          ▷ the edges of f, counterclockwise from outside
L1  e₀ ← face_edge[f]; e ← e₀
L2  repeat output e
L3      if f_left[e] = f then e ← left_next[e] else e ← right_next[e]
L4  until e = e₀

VERTEX-EDGES(v)                        ▷ the edges at v, counterclockwise from outside
L5  e₀ ← vertex_edge[v]; e ← e₀
L6  repeat output e
L7      if v_start[e] = v then e ← left_prev[e] else e ← right_prev[e]
L8  until e = e₀

SPLIT-FACE(f, u, w)                    ▷ u, w on f and not joined by an edge
L9  walk f; find the edges a_in, a_out before and after u, and b_in, b_out before and after w
L10 make a face g and an edge n from u to w with f_left[n] ← f, f_right[n] ← g
L11 left_prev[n] ← a_in; left_next[n] ← b_out; right_prev[n] ← b_in; right_next[n] ← a_out
L12 for each edge of f from a_out to b_in: replace f by g on the side of f
L13 set the next wing of a_in on f, the prev wing of b_out on f, the next wing of b_in on g and the prev wing of a_out on g to n
L14 face_edge[f] ← n; face_edge[g] ← n
```

**Around a face.** Line L3 is the orientation test. If $f$ is the left face of $e$, then $f$ uses $e$ from start to end, and the next edge of $f$ is $left_{next}[e]$. If not, $f$ uses $e$ from end to start, and the next edge is $right_{next}[e]$. The vertex at the start of $e$ on $f$ is $v_{start}[e]$ in the first case and $v_{end}[e]$ in the second.

**Around a vertex.** Let $e$ be an edge at $v$, and let $f$ be the face that uses $e$ as it leaves $v$: this is $f_{left}[e]$ if $v = v_{start}[e]$ and $f_{right}[e]$ if not. The edge before $e$ in $f$ comes into $v$. Seen from outside, $f$ lies counterclockwise from $e$ at $v$, so this edge is the next edge counterclockwise around $v$. Line L7 takes it from the wing on the side of $f$.

**Updates.** In SPLIT-FACE, the new edge $n$ has $f$ on its left, so $f$ keeps the part of its loop from $w$ around to $u$, and the new face $g$ gets the part from $u$ to $w$. Line L12 moves the edges of that part to $g$, one side field each. Line L13 sets the four wings that pointed across the cut. JOIN-FACES does the opposite steps: it moves the edges of the right face of $n$ to the left face and joins the wings around the two ends of $n$. SPLIT-EDGE puts a new vertex $m$ inside $e$: it makes a new edge from $m$ to $v_{end}[e]$, changes $v_{end}[e]$ to $m$, and sets six wings. It needs no walk, so it takes $O(1)$ time.

**Build.** BUILD makes one edge for each unordered pair $\{u, v\}$ that is a side of a face, with a hash map on the pair. The first face that uses the pair is the left face, and the direction of the edge is the direction in which that face uses it. The second face must use it in the other direction, and it becomes the right face. Then BUILD walks each face list once and sets the prev and next wings on the side of that face. It fails if a pair is used by one face only, by more than two faces, twice in one direction, or twice by one face, and if the walk around a vertex misses an edge at that vertex.

## Example

Take the cube with the vertices $0 = (0, 0, 0)$, $1 = (1, 0, 0)$, $2 = (1, 1, 0)$, $3 = (0, 1, 0)$ and $4$ to $7$ the same points with $z = 1$, and the faces $0 = (0, 3, 2, 1)$ at the bottom, $1 = (4, 5, 6, 7)$ at the top, $2 = (0, 1, 5, 4)$, $3 = (1, 2, 6, 5)$, $4 = (2, 3, 7, 6)$ and $5 = (3, 0, 4, 7)$. BUILD gives these 12 edges:

| $e$ | $v_{start}$ | $v_{end}$ | $f_{left}$ | $f_{right}$ | $left_{prev}$ | $left_{next}$ | $right_{prev}$ | $right_{next}$ |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 3 | 0 | 5 | 3 | 1 | 11 | 9 |
| 1 | 3 | 2 | 0 | 4 | 0 | 2 | 10 | 11 |
| 2 | 2 | 1 | 0 | 3 | 1 | 3 | 8 | 10 |
| 3 | 1 | 0 | 0 | 2 | 2 | 0 | 9 | 8 |
| 4 | 4 | 5 | 1 | 2 | 7 | 5 | 8 | 9 |
| 5 | 5 | 6 | 1 | 3 | 4 | 6 | 10 | 8 |
| 6 | 6 | 7 | 1 | 4 | 5 | 7 | 11 | 10 |
| 7 | 7 | 4 | 1 | 5 | 6 | 4 | 9 | 11 |
| 8 | 1 | 5 | 2 | 3 | 3 | 4 | 5 | 2 |
| 9 | 4 | 0 | 2 | 5 | 4 | 3 | 0 | 7 |
| 10 | 2 | 6 | 3 | 4 | 2 | 5 | 6 | 1 |
| 11 | 3 | 7 | 4 | 5 | 1 | 6 | 7 | 0 |

The face edges are $face\_edge = (0, 4, 3, 2, 1, 0)$, and the vertex edges are $vertex\_edge = (0, 2, 1, 0, 4, 4, 5, 6)$.

FACE-EDGES(2) starts at edge 3. Face 2 is on the right of edge 3, so the next edge is $right_{next}[3] = 8$. Face 2 is on the left of edge 8, so the next edge is $left_{next}[8] = 4$. Then $right_{next}[4] = 9$ and $left_{next}[9] = 3$, the start. The walk uses the edges in both directions: the left and right sides alternate. The start vertices on face 2 are $v_{end}[3] = 0$, $v_{start}[8] = 1$, $v_{end}[4] = 5$ and $v_{start}[9] = 4$, which is the face list $(0, 1, 5, 4)$.

VERTEX-EDGES(0) starts at edge 0, which leaves 0, so the next edge is $left_{prev}[0] = 3$. Edge 3 ends at 0, so the next is $right_{prev}[3] = 9$, and edge 9 also ends at 0, so the next is $right_{prev}[9] = 0$, the start. The neighbours of 0 are $3, 1, 4$ and the faces on the left of the edges out of 0 are $0, 2, 5$, counterclockwise seen from outside the corner.

SPLIT-FACE(1, 4, 6) cuts the top face along its diagonal. It makes edge 12 from 4 to 6 with $f_{left} = 1$, $f_{right} = 6$ and the wings $left_{prev} = 7$, $left_{next} = 6$, $right_{prev} = 5$, $right_{next} = 4$. Face 1 becomes $(4, 6, 7)$ and the new face 6 is $(6, 4, 5)$. Now $V - E + F = 8 - 13 + 7 = 2$, as before.

## Correctness

Assume BUILD returns. Then every edge has two different faces that use it in opposite directions, and on the side of each face, its two wings are its neighbours in the face list of that face. So line L3 moves from each edge of $f$ to the next edge of $f$, and FACE-EDGES lists the face list of $f$ once and stops. The vertex step of line L7 is a permutation of the edges at $v$, because its inverse is the next wing on the face that comes into $v$, and each of its steps crosses one face at $v$. A cycle of this permutation is one fan of faces at $v$. BUILD checks that the cycle of $vertex\_edge[v]$ has every edge at $v$, so VERTEX-EDGES lists them all. Each update changes only the fields of the edges on the cut and keeps these two facts, so the queries stay correct after any sequence of updates. The full proof is in the proof file.

The orientation test of line L3 is correct only if $f_{left}[e] \ne f_{right}[e]$. If both sides of $e$ are the same face, for example for a bridge edge that joins a hole to the outer boundary of a face, the test always takes the left wing, and the walk can go around the face in a loop that does not contain all its edges. BUILD rejects such input.

## Complexity

Let $n$ be the number of edges.

- BUILD takes $O(n)$ expected time with a hash map on the vertex pairs, and $\Theta(n)$ space: $8n$ edge fields, one field per vertex and one per face.
- EDGE-VERTICES, EDGE-FACES and each wing take $O(1)$ time. The test of line L3 or line L7 is one comparison.
- FACE-EDGES($f$) takes $O(k)$ time for a face with $k$ edges, and VERTEX-EDGES($v$) takes $O(d)$ time for a vertex of degree $d$. So the neighbours, the faces at a vertex and the vertices of a face take time linear in the size of the answer.
- SPLIT-EDGE takes $O(1)$ time. SPLIT-FACE walks $f$ to find $u$ and $w$ and to change the face of the moved edges, so it takes $O(k)$ time, plus $O(d)$ for the test that $u$ and $w$ are not neighbours. JOIN-FACES takes time linear in the sizes of the two faces.

The constant time of the summary is the time of one step. No structure of this kind lists the $k$ edges of a face in less than $k$ steps, because it must output them.

## Variants

- **Half-edge.** Split each edge record into two half-edges, one for each face. Each half-edge knows its own face and its own next edge, so the orientation test of line L3 goes away, and a face can have rings through a loop record. This is the [doubly connected edge list](/doubly-connected-edge-list/) of planar subdivisions, and the [B-rep](/boundary-representation/) page builds a solid modeler form of it.
- **Quad-edge.** The [quad-edge data structure](/quad-edge-data-structure/) of Guibas and Stolfi stores one record per edge with four directed versions of it, two for the edge and two for its dual. It stores the surface and its dual together, and it allows non-orientable surfaces.
- **Signed edge references.** Store each wing, each $face\_edge$ and each $vertex\_edge$ as an edge with a direction bit. Then the walks need no test, and the structure is close to a half-edge structure that shares one record per edge.
- **Faces with rings.** Weiler's modified winged edge puts a loop record between the edges and the faces, so that a face can have several boundaries. Without it, a face with a hole needs a bridge edge with the same face on both sides, and the orientation test fails on it.
- **Non-manifold.** The [radial edge data structure](/radial-edge-data-structure/) stores any number of faces around an edge, which the two face fields of a winged edge cannot do.

## When to use it

Use the winged edge when the faces are disks, the surface is a closed 2-manifold, and memory per edge matters more than the cost of one comparison per step. It suits polyhedral modelers and mesh editors that make many local changes by [Euler operators](/euler-operators/), because each edge has only one record to update. When faces can have holes, or when code must walk loops fast and without branches, use a half-edge form. For a triangle mesh that does not change its connectivity, a [corner table](/corner-table/) or the face-vertex lists of a [polygon mesh](/polygon-mesh/) use less memory.

## Pitfalls

- **The orientation test.** Every step around a face must test whether the face is the left or the right face of the edge. Code that always takes $left_{next}$ walks on the wrong face as soon as an edge is used backwards, as edges 3 and 4 of face 2 are in the example.
- **Same face on both sides.** The test is ambiguous if $f_{left}[e] = f_{right}[e]$. This happens with bridge edges in faces with holes and with dangling edges inside a face. Reject them, or store directions with the references.
- **Wing conventions.** Sources disagree on the names of the four wings and on the direction of the face loops. Mixing two conventions gives walks that go backwards or jump between faces.
- **Double edges.** SPLIT-FACE between two vertices that are already joined by an edge makes two edges with the same ends. A face list then no longer gives the surface, and many algorithms that look up an edge by its ends break. Test $w \notin$ VERTEX-EDGES($u$) first, as the implementation does.
- **One fan per vertex.** Two solids that touch at one vertex pass the edge tests of BUILD, but the walk around that vertex sees only one of them. Count the edges at each vertex and compare with the walk.
- **Wings after an update.** An update must set the wings of the neighbouring edges on the correct side. Use helper functions that choose the side by the face, as the implementation does, and check all wings after each update in the tests.

## Implementations

## History

Baumgart described the winged-edge polyhedron in a Stanford report of 1972 and at the AFIPS National Computer Conference in 1975, as the representation of his geometric modeling system for computer vision. It was the first boundary structure built on edges, and his Euler primitives made and changed polyhedra one edge and one face at a time. In 1985 Weiler studied which edge-based structures can answer all adjacency queries, and he gave variants with loops for faces with holes and with edge uses. In the same year Guibas and Stolfi published the quad-edge structure, which removes the orientation test with an algebra of directed edges. Mäntylä's book of 1988 compares the winged edge with the half-edge structure that later solid modelers used.

## References
