---
tag: FBTW3E
kind: data-structure
slug: corner-table
name: Corner table
aliases:
- Rossignac corner table
area: cad/mesh-processing
level: core
summary: Rossignac's compact triangle mesh structure with two integer arrays, the vertex and the opposite corner of each corner, which supports all adjacency queries.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of triangles, d: the degree of the vertex}
  time: {build: O(n + m) expected, next: O(1), opposite: O(1), swing: O(1), ring: O(d)}
  space: {extra: Θ(n + m)}
prereqs: [indexed-face-set, manifold-mesh]
see_also: [doubly-connected-edge-list, polygon-mesh, quad-edge-data-structure, winged-edge-data-structure, consistent-mesh-orientation, mesh-simplification, edge-flip, hash-table]
sources:
  - paper: "Jarek Rossignac, Alla Safonova and Andrzej Szymczak, 3D compression made simple: Edgebreaker on a corner-table, Shape Modeling International 2001, Genova, pages 278 to 283"
    locator: the description of the corner table (the arrays V and O and the operators next, previous, opposite, left, right and swing)
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 2, Mesh Data Structures, Section 2.4, Directed-Edge Data Structure (the same idea of implicit triangle indices)
---

A corner table stores a triangle mesh in two integer arrays. Each triangle $t$ has three *corners* $3t$, $3t + 1$ and $3t + 2$, one at each of its vertices. The array $V$ gives the vertex of each corner, and the array $O$ gives the *opposite* corner: the corner of the next triangle across the edge that faces the corner. All other relations come from the index arithmetic: the triangle of corner $c$ is $\lfloor c/3 \rfloor$, the next corner in the triangle is $3\lfloor c/3 \rfloor + (c+1) \bmod 3$, and one step around a vertex is $\mathrm{next}(O[\mathrm{next}(c)])$. Jarek Rossignac and his students described it in 2001 for the Edgebreaker compression scheme. It works for consistently oriented [manifold meshes](/manifold-mesh/) of triangles, and it uses about half the memory of a half-edge structure.

## In plain words

Each triangle has three corners. Give every corner a number: the corners of the first triangle are 0, 1 and 2, the corners of the second are 3, 4 and 5, and so on. Then the triangle of a corner, and the other two corners of that triangle, follow from the number alone.

For each corner you keep two numbers. The first is the point where the corner sits. The second is the corner across from it in the triangle next door, on the far side of the opposite side. With these two lists you can step from a triangle to its neighbours, and you can walk around a point from triangle to triangle until you come back. You store nothing else.

## The abstract type

The structure holds a triangle mesh with $n$ vertices and $m$ triangles. The mesh is a [manifold mesh](/manifold-mesh/) in the edge sense (each edge has one or two triangles) and consistently oriented (the two triangles of an inner edge use it in opposite directions). The operations are:

- $\mathrm{BUILD}(T)$: make the structure from a triangle list $T$, as in an [indexed face set](/indexed-face-set/), or fail if an edge is used twice in one direction.
- $\mathrm{NEXT}(c)$, $\mathrm{PREV}(c)$, $\mathrm{TRIANGLE}(c)$, $\mathrm{VERTEX}(c)$: the relations inside one triangle.
- $\mathrm{OPPOSITE}(c)$: the corner across the edge that faces $c$, or $-1$ on a border.
- $\mathrm{LEFT}(c) = O[\mathrm{next}(c)]$ and $\mathrm{RIGHT}(c) = O[\mathrm{prev}(c)]$: the corners of the two neighbouring triangles that share an edge at $c$.
- $\mathrm{SWING}(c)$: the corner of the same vertex in the next triangle counterclockwise around it, or $-1$.
- $\mathrm{RING}(c)$: all corners of the fan of the vertex of $c$, in order.

Counterclockwise here means the orientation of the mesh: with the right-hand rule for the vertex order, it is counterclockwise when seen from the side of the normal.

## Representation

| array | size | meaning |
|---|---|---|
| $V[c]$ | $3m$ | the vertex of corner $c$; $V[3t], V[3t+1], V[3t+2]$ is triangle $t$ in order |
| $O[c]$ | $3m$ | the opposite corner of $c$, or $-1$ if the edge that faces $c$ is a border edge |
| $C[v]$ | $n$ | one corner of vertex $v$, or $-1$ (optional) |
| positions | $n$ | the coordinates of each vertex |

The array $V$ is the index buffer of the triangle list, so the table adds only $O$, and $C$ if walks start from a vertex. The edge that faces corner $c$ runs from $V[\mathrm{next}(c)]$ to $V[\mathrm{prev}(c)]$. The opposite corner $d = O[c]$ is the corner whose edge runs the other way, from $V[c']$ to $V[c'']$ with $c' = \mathrm{prev}(c)$ and $c'' = \mathrm{next}(c)$. So $O[O[c]] = c$.

## Operations

```pseudo id=main
BUILD(T)                                   ▷ T: m triangles, consistently oriented
L1  for t = 0 .. m − 1, k = 0, 1, 2 do V[3t + k] ← T[t][k]; O[3t + k] ← −1
L2  H ← empty hash map from directed edges to corners
L3  for each corner c do
L4      key ← (V[NEXT(c)], V[PREV(c)])       ▷ the edge that faces c
L5      if key is in H then fail             ▷ an edge used twice in one direction
L6      H[key] ← c
L7  for each corner c do
L8      d ← H[(V[PREV(c)], V[NEXT(c)])], or −1 if the key is absent
L9      O[c] ← d

NEXT(c)
L10 return 3⌊c/3⌋ + (c + 1) mod 3
PREV(c)
L11 return NEXT(NEXT(c))

SWING(c)                                   ▷ the next corner of V[c], counterclockwise
L12 d ← O[NEXT(c)]; if d = −1 then return −1 else return NEXT(d)

RING(c)
L13 s ← c; while UNSWING(s) ∉ {−1, c} do s ← UNSWING(s); if UNSWING(s) = c then s ← c
L14 output s, SWING(s), SWING(SWING(s)), ... until −1 or back at s
```

Here UNSWING$(c) = \mathrm{PREV}(O[\mathrm{PREV}(c)])$ is the step the other way. Line L8 looks for the corner whose edge is the reverse of the edge of $c$, which is the corner across that edge. Line L5 catches two kinds of bad input: a face with the wrong orientation, and an edge with three or more triangles, since two of them must use it in the same direction.

SWING follows from the definitions. Let $c$ sit at $v$ in the triangle $(v, a, b)$. The corner $\mathrm{next}(c)$ sits at $a$ and faces the edge from $b$ to $v$. Its opposite corner $d$ is in the triangle on the other side of $\{v, b\}$, and it faces the edge from $v$ to $b$, so $\mathrm{next}(d)$ sits at $v$. Line L13 walks back to the first triangle of a border fan, so that line L14 lists the whole fan.

## Example

A tetrahedron with the vertices $0 = (0,0,0)$, $1 = (1,0,0)$, $2 = (0,1,0)$, $3 = (0,0,1)$ and the triangles $(0, 2, 1)$, $(0, 1, 3)$, $(1, 2, 3)$, $(0, 3, 2)$. By the right-hand rule each normal points out; for example, the normal of $(0, 2, 1)$ is $(0, 0, -1)$. BUILD gives:

| corner $c$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $V[c]$ | 0 | 2 | 1 | 0 | 1 | 3 | 1 | 2 | 3 | 0 | 3 | 2 |
| $O[c]$ | 8 | 5 | 10 | 7 | 11 | 1 | 9 | 3 | 0 | 6 | 2 | 4 |

Corner 0 sits at vertex 0 and faces the edge from 2 to 1. Corner 8 sits at vertex 3 in triangle 2, $(1, 2, 3)$, and faces the edge from 1 to 2, the same edge the other way. So $O[0] = 8$ and $O[8] = 0$.

Now walk around vertex 0 from corner 0. $\mathrm{next}(0) = 1$, $O[1] = 5$, and $\mathrm{next}(5) = 3$, so SWING$(0) = 3$, the corner of vertex 0 in triangle 1. Then $\mathrm{next}(3) = 4$, $O[4] = 11$, $\mathrm{next}(11) = 9$, so SWING$(3) = 9$, in triangle 3. Then $\mathrm{next}(9) = 10$, $O[10] = 2$, $\mathrm{next}(2) = 0$, and the walk is back at corner 0. RING$(0) = [0, 3, 9]$, and the neighbours $V[\mathrm{next}(c)]$ in order are $2, 1, 3$.

For the square of two triangles $(0, 1, 2)$ and $(0, 2, 3)$, only the diagonal is an inner edge: $O = [-1, 5, -1, -1, -1, 1]$. The fan of vertex 2 is a path. RING$(2)$ first steps back to corner 4 in triangle 1, since UNSWING$(4) = -1$, and returns $[4, 2]$, with the neighbours $3, 0, 1$.

## Correctness

BUILD stores each directed edge with the corner that faces it, and it fails if a directed edge appears twice. Then $O[c]$ is the corner that faces the reverse edge, which is the corner across the edge in the other triangle, and $O$ is its own inverse. SWING crosses the edge $\{v, b\}$ after $c$ and stays at the vertex $v$, and UNSWING is its inverse. So the corners of a vertex, joined by SWING, form one path or one cycle for each fan, and RING lists one of them from its start. The full proof is below.

## Complexity

- BUILD does $3m$ insertions and $3m$ lookups in a [hash table](/hash-table/), so it takes $O(n + m)$ expected time. Sorting the $3m$ directed edges instead gives $O(m \log m)$ worst-case time.
- NEXT, PREV, TRIANGLE, VERTEX, OPPOSITE, LEFT, RIGHT and SWING take $O(1)$ time.
- RING takes $O(d)$ time for a vertex in $d$ triangles.
- The space is $6m$ integers for $V$ and $O$, and $n$ more for $C$. For a closed mesh, $m \approx 2n$, so the table has about $12n$ integers, or $6n$ in addition to the index buffer. A half-edge structure with next, twin, vertex and face for each of $3m$ half-edges has about $24n$ integers.

## Variants

- **The directed-edge structure.** It numbers the half-edges as $3t + k$ in the same way and stores the twin of each half-edge, which is the same information as $O$ with another naming. Botsch and others describe it in Section 2.4 of their book.
- **Corner tables for quads and polygons.** For quad meshes, the corners are $4t + k$. For mixed polygons, an extra array of face offsets replaces the index arithmetic.
- **Non-manifold vertices.** A vertex with two fans, such as the tip of two cones that touch, has two separate rings. The table still works for each edge, but RING from one corner finds only its own fan. Some programs split such vertices into one copy for each fan.
- **Compression.** Edgebreaker walks the triangles with $O$ and writes one of five symbols for each triangle. This was the first use of the table.
- **Local edits.** An [edge flip](/edge-flip/) changes two triangles and six entries of $O$. An edge collapse, as in [mesh simplification](/mesh-simplification/), removes two triangles and needs the arrays to be compacted or the dead triangles to be marked.

## When to use it

Use a corner table for a triangle mesh that a program walks often but changes little: smoothing, curvature, geodesics, compression and parameterization. It is easy to build from an [indexed face set](/indexed-face-set/), it is two flat arrays that are fast to copy and to send to a graphics card, and it needs no pointers. For meshes with polygons of mixed sizes, or with many local edits, a [doubly connected edge list](/doubly-connected-edge-list/) is simpler. For non-manifold meshes, use a structure such as the [radial edge structure](/radial-edge-data-structure/).

## Pitfalls

- **A flipped triangle.** If one triangle has the wrong orientation, its edges have the same direction as those of its neighbours, and BUILD fails or leaves borders where there are none. Run [consistent mesh orientation](/consistent-mesh-orientation/) first.
- **Swing at a border.** SWING returns $-1$ at a border edge. A walk that starts in the middle of a border fan and only swings forward misses the triangles before it. Walk back first, as line L13 does.
- **Duplicate vertices.** Two vertices at the same position are different vertices for the table, and the edge between them is a border. Weld first, see [vertex welding](/vertex-welding/).
- **Degenerate triangles.** A triangle with a repeated vertex has an edge from a vertex to itself, which breaks the swing around that vertex. Remove such triangles before BUILD.
- **The sign convention.** Some texts define swing with $\mathrm{prev}$ in place of $\mathrm{next}$, which turns the other way. Check the convention of the code you use.

## Implementations

## History

Jarek Rossignac, Alla Safonova and Andrzej Szymczak described the corner table in 2001, at Shape Modeling International in Genova, to make the Edgebreaker compression of triangle mesh connectivity simple to program. Edgebreaker itself is from Rossignac's earlier work of 1999. The directed-edge structure of Campagna, Kobbelt and Seidel, from 1998, uses the same implicit numbering of half-edges in triangles.

## References
