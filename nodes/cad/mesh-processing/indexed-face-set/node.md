---
tag: A865QN
kind: data-structure
slug: indexed-face-set
name: Indexed face set
aliases:
- face-vertex mesh
- shared vertex representation
area: cad/mesh-processing
level: intro
summary: A mesh stored as an array of vertex positions and a list of faces, each given by the indices of its vertices, the form of most mesh files.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of faces, c: "the number of corners, the sum of the face sizes", k: the size of the answer}
  time: {build: O(n + c) expected, edge-faces: O(1 + k) expected, boundary-edges: O(c)}
  space: {extra: Θ(n + c)}
prereqs: [polygon-mesh, hash-table]
see_also: [doubly-connected-edge-list, corner-table, manifold-mesh, vertex-welding, mesh-repair-problem, winged-edge-data-structure, euler-poincare-formula, adjacency-list]
sources:
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 2, Mesh Data Structures, Section 2.1, Face-Based Data Structures
  - url: https://www.web3d.org/documents/specifications/14772/V2.0/part1/nodesRef.html
    title: The Virtual Reality Modeling Language, ISO/IEC 14772-1:1997, Chapter 6, Node Reference
    locator: Section 6.23, IndexedFaceSet (the coord and coordIndex fields, and the ccw field for the vertex order)
---

An indexed face set stores a [polygon mesh](/polygon-mesh/) as two lists: an array of vertex positions, and a list of faces, where each face is the list of the indices of its vertices in order. Each vertex is stored once and the faces share it by index. This is the form of most mesh files, such as OFF, OBJ and PLY, and the name comes from the IndexedFaceSet node of VRML. The two lists alone answer "which vertices does this face have" in constant time, but not "which faces are next to this face". This page adds an edge table, a [hash table](/hash-table/) from each undirected edge to the faces that use it, which answers the adjacency queries in expected time proportional to the answer and finds the boundary and non-manifold edges.

## In plain words

Think of a model made of flat tiles. You write a numbered list of the corner points of all tiles, with each point written one time. Then, for each tile, you write the numbers of its corners in the order you meet them when you go around the tile. Two tiles that touch use the same numbers for their shared corners.

This is all a mesh file needs. To move a point, you change one line, and every tile that uses it moves with it. To find the tiles next to a given tile, you make a second list: for each side of a tile, which tiles use that side. A side that only one tile uses is on the edge of a hole. A side that three or more tiles use is a place where the surface branches.

## The abstract type

The structure holds a mesh with $n$ vertices and $m$ faces. A face is a sequence of $k \ge 3$ distinct vertex indices. The order gives the orientation: by the convention of most formats, the vertices go counterclockwise when the face is seen from outside, so the outward normal follows the right-hand rule. The operations are:

- $\mathrm{BUILD}(V, F)$: make the structure from the positions $V$ and the faces $F$.
- $\mathrm{EDGE\text{-}FACES}(u, v)$: the faces that have $\{u, v\}$ as an edge.
- $\mathrm{FACE\text{-}NEIGHBORS}(f)$: the faces other than $f$ that share an edge with $f$.
- $\mathrm{VERTEX\text{-}FACES}(v)$: the faces that have $v$ as a vertex.
- $\mathrm{BOUNDARY\text{-}EDGES}$: the edges that one face uses. $\mathrm{NON\text{-}MANIFOLD\text{-}EDGES}$: the edges that three or more faces use.
- $\mathrm{EULER}$: the Euler characteristic $\chi = V - E + F$ of the mesh.

## Representation

| field | meaning |
|---|---|
| $V[0 \ldots n-1]$ | the position of each vertex |
| $F[0 \ldots m-1]$ | each face as a tuple of vertex indices, in order |
| $E$ | a hash map from the key $(\min(u, v), \max(u, v))$ of each edge to the list of its uses $(f, i)$: edge $i$ of face $f$ |
| $VF[0 \ldots n-1]$ | for each vertex, the faces that use it |

The first two rows are the file. The last two rows are derived from them, and a program builds them after it reads the file. The key of an edge has no direction, so both faces of an edge use the same entry. The index $i$ in a use tells the direction: face $f$ goes along the edge from $F[f][i]$ to $F[f][i+1]$.

## Operations

```pseudo id=main
BUILD(V, F)
L1  E ← empty hash map; VF[v] ← empty list for each vertex v
L2  for each face f, each corner i = 0 .. |F[f]| − 1 do
L3      u ← F[f][i]; v ← F[f][(i + 1) mod |F[f]|]
L4      append (f, i) to E[{u, v}]
L5      append f to VF[u]

EDGE-FACES(u, v)
L6  return the faces of the uses in E[{u, v}], or nothing if there is no entry

FACE-NEIGHBORS(f)
L7  for each edge e of f, each use (g, j) in E[e] with g ≠ f and g not yet output do output g

BOUNDARY-EDGES
L8  return the keys e of E with |E[e]| = 1

EULER
L9  return n − |E| + m
```

Line L4 puts both directions of an edge in one entry, because the key is the sorted pair. A closed [manifold mesh](/manifold-mesh/) has exactly two uses in each entry. Line L8 lists the edges of the holes, and the same scan with $|E[e]| \ge 3$ lists the non-manifold edges. Line L9 counts each distinct edge once, because each one is one key of $E$.

The edge table can also test the orientation. Two faces that share an edge are oriented the same way exactly when they go along it in opposite directions. Two uses of an edge in the same direction show a flipped face, which [consistent mesh orientation](/consistent-mesh-orientation/) repairs.

## Example

A unit square made of two triangles, in the OFF format:

```text
OFF
4 2 0
0 0 0
1 0 0
1 1 0
0 1 0
3 0 1 2
3 0 2 3
```

The header gives 4 vertices and 2 faces. Each face line starts with the number of its vertices. BUILD makes this edge table:

| edge | uses | count |
|---|---|---|
| $\{0, 1\}$ | $(0, 0)$ | 1 |
| $\{1, 2\}$ | $(0, 1)$ | 1 |
| $\{0, 2\}$ | $(0, 2)$, $(1, 0)$ | 2 |
| $\{2, 3\}$ | $(1, 1)$ | 1 |
| $\{0, 3\}$ | $(1, 2)$ | 1 |

The diagonal $\{0, 2\}$ has two uses. Face 0 goes along it from 2 to 0 (edge 2 of $(0, 1, 2)$), and face 1 goes from 0 to 2 (edge 0 of $(0, 2, 3)$). The directions are opposite, so the two faces have the same orientation. FACE-NEIGHBORS(0) is $[1]$. The four other edges are boundary edges, and $\chi = 4 - 5 + 2 = 1$, the value for a disk.

The same square as a triangle soup, the form of an STL file, has 6 vertices, with $(0,0,0)$ and $(1,1,0)$ written twice, and the faces $(0, 1, 2)$ and $(3, 4, 5)$. Now no edge has two uses, the faces have no neighbours, and $\chi = 6 - 6 + 2 = 2$: two separate triangles. [Vertex welding](/vertex-welding/) merges the duplicate points and gives back the first form.

## Correctness

The loop of line L2 keeps this invariant: for each edge $e$, the entry $E[e]$ lists, in order, the uses of $e$ by the corners scanned so far, and $E$ has no empty entry. Line L4 adds each corner to the entry of exactly its own edge. So at the end, each entry lists all uses of its edge, and the keys are exactly the distinct edges. EDGE-FACES, FACE-NEIGHBORS and BOUNDARY-EDGES read these lists, and EULER counts the keys. The full proof is below.

## Complexity

Let $c = \sum_f |F[f]|$ be the number of corners. For a triangle mesh $c = 3m$.

- BUILD does $c$ hash table insertions, so it takes $O(n + c)$ expected time.
- EDGE-FACES takes $O(1 + k)$ expected time for $k$ faces on the edge.
- FACE-NEIGHBORS takes expected time proportional to the number of uses of the edges of $f$, which is $O(|f|)$ on a manifold mesh.
- VERTEX-FACES takes time proportional to its answer.
- BOUNDARY-EDGES and EULER take $O(c)$ time, or $O(1)$ for EULER if the sizes are kept.
- The space is $\Theta(n + c)$: the positions, the faces, at most $c$ edge keys and $c$ uses.

The bare file form, without $E$ and $VF$, uses $3n$ numbers for the positions and $c$ indices for the faces. It is one of the smallest forms with shared vertices. Each adjacency query on it scans all faces, in $\Theta(c)$ time.

## Variants

- **Triangle soup.** Each face stores its own coordinates, with no shared indices. STL files use this form. It has no adjacency, and [vertex welding](/vertex-welding/) is needed to make it an indexed face set.
- **Fixed-size faces.** For a triangle mesh, the faces are one array of $3m$ indices. This is the index buffer of a graphics card.
- **Corner attributes.** OBJ and VRML give each corner its own index into separate normal and texture coordinate arrays, so a vertex can have different normals on the two sides of a crease.
- **Edge-based structures.** The [corner table](/corner-table/) adds one array of opposite corners to a triangle index array. The [doubly connected edge list](/doubly-connected-edge-list/), the half-edge form, and the [winged-edge structure](/winged-edge-data-structure/) store the adjacency explicitly and allow local edits in constant time.

## When to use it

Use it to store and exchange meshes, and to draw them. It is the input of almost every mesh algorithm, and it can hold any mesh, also a mesh with non-manifold edges, holes and flipped faces. Use the edge table when you need adjacency once, for example to find holes, to check that a mesh is closed, or to build a better structure. If a program walks over the mesh many times, or edits it, change to a [corner table](/corner-table/) or a half-edge structure.

## Pitfalls

- **Indices from 0 or 1.** OFF counts vertices from 0, and OBJ counts them from 1 and allows negative indices from the end. A wrong base moves every face by one vertex.
- **Duplicate vertices.** A file can have two vertices at the same position. The faces then do not share an edge, and the mesh looks closed but has holes in its topology. Weld first.
- **Degenerate faces.** A face can repeat an index, or have collinear vertices. The structure on this page rejects a repeated index. Collinear vertices give a zero normal and break later geometric tests.
- **The edge count of the OFF header.** Many writers put 0 there. Do not trust it. Count the keys of $E$.
- **Directed edge keys.** A key $(u, v)$ with a direction puts the two faces of an edge in different entries, and every edge looks like a boundary edge.

## Implementations

## History

The format of a vertex list and a face list of indices is as old as computer graphics. The name comes from the IndexedFaceSet node of Silicon Graphics' Open Inventor, which VRML took over in its 1.0 version in 1995. The VRML97 standard, ISO/IEC 14772-1:1997, defines the node with the fields coord and coordIndex, where the index $-1$ ends a face. Botsch and others describe it as the face-based data structure, the simplest of the mesh data structures.

## References
