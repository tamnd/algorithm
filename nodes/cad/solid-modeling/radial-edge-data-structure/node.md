---
tag: X79HMJ
kind: data-structure
slug: radial-edge-data-structure
name: Radial edge data structure
aliases:
- Weiler radial edge
area: cad/solid-modeling
level: advanced
summary: Weiler's structure for non-manifold solids that orders the faces around each edge radially, so wire edges, sheets and solids sharing an edge can be stored.
model: word-ram
complexity:
  vars:
    n: the sum of the face sizes, so the number of edgeuses is 2n
    m: the largest number of faces at one edge
  time:
    expected: O(n m)
  space:
    extra: Θ(n)
prereqs: [boundary-representation, winged-edge-data-structure, manifold-solid]
see_also: [euler-operators, vertex-neighborhood-classification, solid-boolean-operations, orientation-test, manifold-mesh, mesh-arrangements, doubly-connected-edge-list, regularized-set-operations]
sources:
  - book: "Kevin J. Weiler, Topological Structures for Geometric Modeling, PhD thesis, Rensselaer Polytechnic Institute, Troy, New York, 1986 (also RPI Center for Interactive Computer Graphics, technical report TR-86032)"
    locator: the non-manifold topology, the faceuse, loopuse, edgeuse and vertexuse elements, and the radial edge structure
  - book: "Kevin Weiler, The radial edge structure, a topological representation for non-manifold geometric boundary modeling, in M. J. Wozny, H. W. McLaughlin and J. L. Encarnação (eds.), Geometric Modeling for CAD Applications, North-Holland, 1988, 3 to 36"
    locator: the elements of the structure, the mate and radial pointers, and the adjacency relations it gives
  - paper: doi:10.1109/MCG.1985.276271
    title: Kevin Weiler, Edge-based data structures for solid modeling in curved-surface environments, IEEE Computer Graphics and Applications 5(1), 21 to 40, 1985
    locator: the edge-based manifold structures that the radial edge structure extends, and the sufficiency of their adjacency relations
  - paper: doi:10.1145/376957.376976
    title: Sang Hun Lee and Kunwoo Lee, Partial entity structure, a compact non-manifold boundary representation based on partial topological entities, Proceedings of the Sixth ACM Symposium on Solid Modeling and Applications, 159 to 170, 2001
    locator: the storage of the radial edge structure and a compact variant with about half its size
---

The radial edge data structure stores the boundary of a *non-manifold* model: solids that share an edge or a vertex, sheets with free edges, and wire edges, all in one structure. Kevin Weiler gave it in his 1986 thesis. A [winged edge](/winged-edge-data-structure/) or a half-edge [B-rep](/boundary-representation/) stores exactly two faces at each edge, so it can store only a [manifold solid](/manifold-solid/). The radial edge structure stores the *uses* of each cell: each face has two faceuses, one for each side, and each edge has one edgeuse for each side of each face at it. Around each edge, the faces are kept in their angular order, and each edgeuse points to the edgeuse of the next face that faces the same wedge of space. This page builds the structure for planar faces with exact integer points, and inserts each new face into the angular order at each of its edges with a sign test.

## In plain words

Think of a book that lies open with its pages spread out around the spine. Each page has two sides, and the space between two pages next to each other is a wedge. A plain B-rep can store only a book with two pages, the front and the back of one closed box. The radial edge structure can store any number of pages at one spine.

For each side of each page, the structure keeps a record at the spine. That record knows the record on the other side of the same page, and the record on the side of the next page that looks into the same wedge. If you go from page to page through these records, you go once around the spine in order. The pages can belong to boxes that touch along the spine, to single sheets of paper, or to both.

## The abstract type

The structure stores a set of vertices with points, a set of planar faces, and wire edges, and it answers adjacency queries about them.

- $\mathrm{ADD\text{-}FACE}(f)$: add a planar face given as a list of vertices, counterclockwise about its normal. Fail if a side of $f$ lies on the same half-plane as a face that is already at that edge.
- $\mathrm{ADD\text{-}WIRE}(u, v)$: add an edge with no face.
- $\mathrm{RADIAL\text{-}FACES}(e)$: the faces at $e$ in counterclockwise order about the direction of $e$.
- $\mathrm{FACE\text{-}VERTICES}(f)$, $\mathrm{FACE\text{-}EDGES}(f)$, $\mathrm{VERTEX\text{-}EDGES}(v)$ and $\mathrm{VERTEX\text{-}FACES}(v)$: the cells around a face and around a vertex.
- $\mathrm{SHELLS}()$: the faceuses grouped into the parts of the boundary of a region that are connected across edges.

A faceuse is a face together with one of its two sides. The faceuse $f^+$ is on the side of the normal $N_f$ of $f$, and $f^-$ is on the other side. Each region of space near the boundary is bounded by faceuses, not by faces: a sheet between two regions is in the boundary of both, once with each side.

## Representation

The records are those of Weiler with the loops and the regions left out, because here each face has one loop and the regions are not computed:

| record | fields |
|---|---|
| vertex $v$ | its point and the list of edgeuses that start at $v$ (Weiler's vertexuses) |
| edge $e$ | its ends $v_0[e]$, $v_1[e]$, the number of faces at it, and one edgeuse $eu[e]$ that runs from $v_0$ to $v_1$ |
| face $f$ | its vertex list, its normal $N_f$ (Newell's sum, exact) and its faceuse $f^+$ |
| faceuse | its face, its side $\pm 1$, its $mate$ (the other side) and one edgeuse of its loop |
| edgeuse $x$ | its edge, its start vertex, its faceuse, $next[x]$ and $prev[x]$ on the loop, $mate[x]$ and $radial[x]$ |

The loop of $f^+$ follows the vertex list of $f$, and the loop of $f^-$ goes the other way. So each loop runs counterclockwise seen from the side of its faceuse, which is the orientation of a manifold B-rep seen from outside. For an edgeuse $x$ of face $f$ at edge $e$:

- $mate[x]$ is the edgeuse of $e$ on the other side of $f$. It runs the other way.
- $radial[x]$ is the edgeuse of the next face around $e$ on the side that faces the same wedge as $x$. It also runs the other way.

Both are involutions without fixed points. A wire edge has two edgeuses with no faceuse, and each is the mate and the radial of the other.

The angular order is defined by the *fin* of each face at each edge: the direction $w_f = N_f \times (q - p)$, where $f^+$ runs along the edge from $p$ to $q$. The fin is perpendicular to the edge and points from the edge into the face, because a loop that runs counterclockwise about $N_f$ has its face on its left. Let $d = v_1[e] - v_0[e]$. Then the fin $b$ is counterclockwise of the fin $a$ by less than a half turn about $d$ exactly when $\det[a, b, d] > 0$, the [orientation test](/orientation-test/) in three dimensions. With integer points, all fins and determinants are integers.

Which use faces which wedge? Let $s = +1$ if $f^+$ runs from $v_0$ to $v_1$, and $s = -1$ if not, so that $w_f = s \, N_f \times d$. A quarter turn of $w_f$ counterclockwise about $d$ gives the direction $d \times w_f = s \, |d|^2 N_f$, because $N_f$ is perpendicular to $d$. So the side of $N_f$ faces the counterclockwise wedge exactly when $s = +1$, that is, when $f^+$ runs from $v_0$ to $v_1$. The same holds for $f^-$ with $-N_f$. In both cases: *the edgeuse that runs from $v_0$ to $v_1$ faces the wedge counterclockwise of its face*, and its mate faces the wedge clockwise of it. This is the rule that the code uses.

## Operations

```pseudo id=main
RADIAL-FACES(e)                        ▷ the faces at e, counterclockwise about v₁ − v₀
L1  u₀ ← eu[e]; u ← u₀                 ▷ eu[e] runs from v₀ to v₁
L2  repeat output face(u)
L3      u ← mate[radial[u]]
L4  until u = u₀

ADD-FACE(f)                            ▷ f planar, counterclockwise about its normal N
L5  make f⁺ and f⁻: the edgeuses of f⁺ follow f, those of f⁻ go backwards; pair each with its mate
L6  for each side of f from p to q do
L7      e ← the edge {p, q}; make it with v₀ = p and v₁ = q if it is new
L8      x ← the edgeuse of f at e that runs from v₀ to v₁; y ← mate[x]; w ← N × (q − p)
L9      if e has no face then radial[x] ← y; radial[y] ← x; eu[e] ← x
L10     else u ← eu[e]
L11         while w is not inside the wedge from fin(u) counterclockwise to fin(radial[u]) do u ← mate[radial[u]]
L12         z ← radial[u]; radial[u] ← y; radial[y] ← u; radial[x] ← z; radial[z] ← x
```

**Around an edge.** Let the faces at $e$ be $F_0, F_1, \ldots, F_{k-1}$ in counterclockwise order of their fins about $d$, and let $x_i$ be the edgeuse of $F_i$ that runs from $v_0$ to $v_1$, and $y_i = mate[x_i]$. Then $x_i$ faces the wedge from $F_i$ to $F_{i+1}$, and so does $y_{i+1}$. The structure keeps $radial[x_i] = y_{i+1}$, indices mod $k$. So $mate[radial[x_i]] = x_{i+1}$, and lines L1 to L4 visit $x_0, x_1, \ldots$ once around. With one face, $radial[x_0] = y_0 = mate[x_0]$: the two sides of a free edge of a sheet face the same wedge, which is the whole turn around the edge.

**Insert a face.** Line L11 walks around the edge until it finds the wedge that contains the new fin $w$. The test is exact:

- if $\det[a, b, d] > 0$, the wedge from $a$ to $b$ is less than a half turn, and $w$ is inside it if $\det[a, w, d] > 0$ and $\det[w, b, d] > 0$;
- if $\det[a, b, d] < 0$, the wedge is more than a half turn, and $w$ is inside it if it is not inside the wedge from $b$ to $a$;
- if $a$ and $b$ are opposite, $w$ is inside if $\det[a, w, d] > 0$, and if $a$ and $b$ are the same fin (one face), the wedge is the whole turn.

Line L12 then puts the new face between $F_i$ and $F_{i+1}$: the wedge from $F_i$ to $F_{i+1}$ is cut into two, $x_i$ now pairs with $y$ and $x$ pairs with $y_{i+1}$. Before any change, ADD-FACE checks each edge: it fails if a fin of the new face has the same direction as a fin already there, because then two faces overlap near the edge, and if an edge is a wire edge.

**Shells.** Two faceuses that are joined by a radial pointer face the same wedge at an edge, so they bound the same region near that edge. SHELLS joins the faceuses of $x$ and $radial[x]$ for every edgeuse $x$ with a union-find structure. The sets are the parts of the boundary of each region that are connected across edges. Weiler's shells are also connected at vertices, for example for the outside of two cubes that touch at one corner. To join these, a modeler must sort the faceuses around the vertex, which is the job of [vertex neighbourhood classification](/vertex-neighborhood-classification/). This page does not do it.

## Example

Take two unit cubes, $[0, 1]^3$ and $[1, 2] \times [1, 2] \times [0, 1]$, that share the edge $e$ from $v_0 = (1, 1, 0)$ to $v_1 = (1, 1, 1)$, so $d = (0, 0, 1)$. Four faces meet at $e$:

| face | part of | fin direction | angle about $+z$ | use that runs up | it faces |
|---|---|---|---|---|---|
| $F_0$, the face $x = 1$ of the first cube | first cube | $-y$ | 270° | $F_0^+$ | the empty quarter $x > 1$, $y < 1$ |
| $F_1$, the face $y = 1$ of the second cube | second cube | $+x$ | 0° | $F_1^-$ | the second cube |
| $F_2$, the face $x = 1$ of the second cube | second cube | $+y$ | 90° | $F_2^+$ | the empty quarter $x < 1$, $y > 1$ |
| $F_3$, the face $y = 1$ of the first cube | first cube | $-x$ | 180° | $F_3^-$ | the first cube |

The normals of the faces point out of their cubes, so the side $F_0^+$ is outside the first cube and $F_1^-$ is inside the second cube. The radial pointers join $F_0^+$ with $F_1^+$ (both face the empty quarter $x > 1$, $y < 1$), $F_1^-$ with $F_2^-$ (both inside the second cube), $F_2^+$ with $F_3^+$ (the other empty quarter) and $F_3^-$ with $F_0^-$ (inside the first cube). RADIAL-FACES($e$) returns $F_0, F_1, F_2, F_3$.

SHELLS returns three sets: the 12 outer faceuses, which are joined through $e$, the 6 inner faceuses of the first cube and the 6 inner faceuses of the second cube. A half-edge B-rep cannot store this model at all, because $e$ has four faces. If the two cubes touch only at the vertex $(1, 1, 1)$, SHELLS returns four sets, because the two outer sets meet only at that vertex.

A book with three square pages on one spine is a model with sheets. Each page has free edges, where its two sides are radial to each other, so all six faceuses form one set. A wire edge added at a corner of a page is stored with no faceuse, and it does not change the shells.

## Correctness

The structure keeps this invariant at each edge $e$ with $k \ge 1$ faces: the edgeuses that run from $v_0$ to $v_1$ are $x_0, \ldots, x_{k-1}$, one per face, in strictly counterclockwise order of their fins, and $radial[x_i] = mate[x_{i+1}]$ and $radial[mate[x_{i+1}]] = x_i$. With it, lines L1 to L4 list each face at $e$ once in order and stop after $k$ steps.

ADD-FACE keeps the invariant. The fins at $e$ have $k$ different directions, and the new fin $w$ has none of them, so $w$ lies strictly inside exactly one of the $k$ open wedges between consecutive fins, and the walk of line L11 finds it within $k$ steps. The sign tests of the wedge test are exact, so the choice is never wrong. Line L12 changes four radial pointers so that the new face sits between $F_i$ and $F_{i+1}$, and the order stays counterclockwise. The loops and the mates of the new face are made once, in line L5, and no other loop changes. The full proof, with the wedge test and the claim about the side that each use faces, is in the proof file.

Proved here: the structure stores the topology and the radial order exactly for any set of planar faces that do not overlap near an edge. Not checked: that faces do not cross each other away from their edges, and that the model is the boundary of a set of regions. Those are geometric checks, as for any B-rep.

## Complexity

Let $n$ be the sum of the face sizes, $k$ the number of faces at an edge, and $m$ the largest $k$.

- ADD-FACE for a face with $s$ sides takes $O(s)$ expected time for the hash map of the edges, plus $O(k)$ time at each edge for the check of the fins and the walk of line L11. So building a model costs $O(n m)$ expected time, and $O(n)$ when every edge has at most a constant number of faces, as in a manifold.
- RADIAL-FACES($e$) takes $O(k)$ time, FACE-VERTICES and FACE-EDGES take time linear in the size of the face, and the vertex queries take time linear in the number of edgeuses at the vertex.
- SHELLS takes $O(n \, \alpha(n))$ time with union-find.
- Space: $2n$ edgeuses with 7 fields each, two faceuses per face, and the edges and vertices. For a manifold, this is about twice the size of a half-edge structure, because each side of each face has its own loop. Lee and Lee report that their partial entity structure stores the same information in about half the space.

## Variants

- **Full radial edge.** Weiler's structure also has loopuses for faces with holes, vertexuses as records, shells and regions as records, and the model at the top. A loop can be a single vertex, and a shell can be a single vertex or a wire.
- **Compact variants.** The partial entity structure of Lee and Lee keeps a use record only where the model is non-manifold, and so it is much smaller on models that are mostly manifold.
- **Non-manifold Euler operators.** Weiler's boundary graph operators and later work extend the [Euler operators](/euler-operators/) to wires, sheets and solids that touch, with the radial order kept by each operator.
- **Cell complexes.** Simplicial and cell complexes with incidence graphs store any dimension, and [mesh arrangements](/mesh-arrangements/) store the cells of many intersecting meshes. They give up the edge-centred walks of the radial edge structure.

## When to use it

Use the radial edge structure when a model must hold mixed dimensions or solids that touch: in non-manifold modelers, in finite element pre-processing where the regions of an assembly share faces, in the intermediate steps of [solid Boolean operations](/solid-boolean-operations/), and in models that store the result of a Boolean before [regularization](/regularized-set-operations/). For a manifold solid, a half-edge or winged-edge structure uses about half the memory and does not need the radial sort.

## Pitfalls

- **Sides, not faces.** A region is bounded by faceuses. Code that treats a face as one boundary element loses the information that a sheet separates two regions, or that both sides of a face bound the same region.
- **The radial order needs exact tests.** Two faces at a small angle can swap places with floating-point determinants, and then the radial pointers join faceuses that do not face the same wedge. Use integer or rational points, or an [exact predicate](/exact-geometric-computation/).
- **The direction of the edge.** The rule that the use from $v_0$ to $v_1$ faces the counterclockwise wedge depends on the direction of the edge record. If the code compares fins about $-d$ in one place and about $d$ in another, the order comes out reversed.
- **Overlapping faces.** Two faces whose fins have the same direction overlap near the edge. The radial order is then undefined, so reject them, or merge them first.
- **Shells through vertices.** Joining faceuses across edges does not join the parts of a region boundary that meet only at a vertex. Do not count regions from these sets without the vertex step.
- **Memory.** Each face has two loops and each edge has $2k$ edgeuses. On large manifold meshes, the structure uses about twice the memory of a half-edge mesh.

## Implementations

## History

Weiler compared the edge-based structures for manifold solids in 1985 and defined the radial edge structure for non-manifold models in his 1986 thesis at Rensselaer Polytechnic Institute. He presented it at the IFIP working conference on geometric modeling in 1986, published in 1988 together with his boundary graph operators. Non-manifold modelers of the late 1980s and the 1990s used it or variants of it, and Lee and Lee gave the compact partial entity structure in 2001.

## References
