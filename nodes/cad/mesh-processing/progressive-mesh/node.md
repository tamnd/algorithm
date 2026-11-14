---
tag: WJ1E5T
kind: data-structure
slug: progressive-mesh
name: Progressive mesh
aliases:
- Hoppe progressive mesh
area: cad/mesh-processing
level: advanced
summary: Hoppe's representation of a mesh as a coarse base mesh and a sequence of vertex splits that undo edge collapses, for smooth level of detail and streaming.
model: word-ram
complexity:
  vars: {n: the number of vertices, d: the largest number of faces at the two vertices of an edge, k: the number of splits applied}
  time: {ecol: O(d) expected, vsplit: O(d), refine: O(k d), build_code: O(n^2 d), build_heap: O(n d log n)}
  space: {extra: Θ(n)}
prereqs: [manifold-mesh, mesh-simplification, euler-formula]
see_also: [quadric-error-metrics, corner-table, edgebreaker, priority-queue, indexed-face-set, doubly-connected-edge-list, edge-flip, euler-poincare-formula]
sources:
  - paper: doi:10.1145/237170.237216
    title: Hugues Hoppe, Progressive meshes, Proceedings of SIGGRAPH 96, pages 99-108, 1996
    locator: the edge collapse and vertex split, the representation as a base mesh with a sequence of vertex splits, geomorphs, progressive transmission, and the construction by energy minimization
  - paper: "Tamal K. Dey, Herbert Edelsbrunner, Sumanta Guha and Dmitry V. Nekhayev, Topology preserving edge contraction, Publications de l'Institut Mathématique (Beograd) (N.S.) 66(80), pages 23-45, 1999"
    locator: the link condition for an edge contraction that keeps the topological type of a 2-manifold
---

A progressive mesh stores a triangle mesh $M^n$ as a coarse base mesh $M^0$ and a list of vertex splits. Each vertex split adds one vertex and, inside the surface, two triangles, and the splits in order rebuild the meshes $M^1, M^2, \dots, M^n$ exactly. It comes from [mesh simplification](/mesh-simplification/) run backwards: simplification removes vertices by edge collapses, each collapse is recorded as the vertex split that undoes it, and the records are kept in reverse order. Hugues Hoppe introduced the structure in 1996. Any prefix of the list gives a valid mesh, so a program can stream the mesh coarse to fine, stop at any level of detail, and move between levels one vertex at a time.

## In plain words

Start with a detailed surface made of triangles. Shrink one short edge to a single point: the two triangles on that edge disappear, and the surface has one point fewer. Repeat until the surface is very coarse.

Each time, write down a small note that says exactly how to pull the point apart again: which point, where its two halves go, and which of its neighbours mark the two triangles that come back.

Keep the coarse surface and the notes in reverse order. Reading the notes one by one grows the surface back, step by step, to the original. You can stop after any note and still have a proper surface, so a viewer can show a rough shape at once and refine it while the rest arrives.

## The abstract type

The structure holds an oriented [manifold mesh](/manifold-mesh/) of triangles, with faces oriented by the right-hand rule. The operations are:

- $\mathrm{ECOL}(M, v_s, v_t, p)$: collapse the edge $v_s v_t$ into the vertex $v_s$ at the position $p$, and return the vertex split that undoes it. It fails if the collapse would make the mesh stop being a manifold.
- $\mathrm{VSPLIT}(M, s)$: apply the vertex split $s$, the inverse of the collapse that made it.
- $\mathrm{LINK}(M, v_s, v_t)$: whether the collapse of $v_s v_t$ is legal.
- $\mathrm{BUILD}(M^n, n_0)$: collapse edges until $n_0$ vertices remain, and return the base mesh $M^0$ and the splits $s_0, s_1, \dots$ in the order of refinement.
- $\mathrm{REFINE}(M^0, k)$: the mesh $M^k$ after the first $k$ splits.

The main law is $\mathrm{VSPLIT}(\mathrm{ECOL}(M, v_s, v_t, p)) = M$ for every legal collapse: the same vertices with the same positions, and the same faces with the same corners in the same order.

## Representation

Let $f_l = (v_s, v_t, v_l)$ be the face with the directed edge $v_s \to v_t$ and $f_r = (v_t, v_s, v_r)$ the face with $v_t \to v_s$. On a boundary edge one of them is missing. A vertex split is a record

| field | meaning |
|---|---|
| $v_s$, $v_t$ | the vertex that stays and the vertex that comes back |
| $v_l$, $v_r$ | the third vertices of $f_l$ and $f_r$, or none |
| $p_s$, $p_t$ | the positions of $v_s$ and $v_t$ before the collapse |
| $f_l$, $f_r$ | the ids and the corners of the two removed faces |

The record does not list the faces that go back from $v_s$ to $v_t$. They are found from $v_l$ and $v_r$ alone: they are the faces around $v_s$ counterclockwise from the edge to $v_r$ up to the edge to $v_l$. So a record has a fixed size, whatever the degree of the vertex.

The mesh of the code keeps stable ids: a map from vertex ids to positions, a map from face ids to oriented triangles, and for each vertex the set of its faces, its *star*. In Hoppe's stream the ids are implicit: the vertices of $M^0$ are numbered $0$ to $n_0 - 1$, the split $s_i$ creates the vertex $n_0 + i$, and the new faces are appended. Then $v_t$ and the face ids need no storage, $v_s$ needs about $\log_2 n$ bits, and $v_l$ and $v_r$ can be named by their place among the neighbours of $v_s$.

## Operations

```pseudo id=main
ECOL(M, v_s, v_t, p)
L1  f_l ← the face with v_s → v_t, v_l its third vertex;  f_r ← the face with v_t → v_s, v_r its third vertex
L2  if v_l = v_r or not LINK(M, v_s, v_t) then fail
L3  s ← (v_s, v_t, v_l, v_r, p(v_s), p(v_t), f_l with its corners, f_r with its corners)
L4  remove f_l and f_r
L5  in every other face of v_t, replace v_t by v_s
L6  p(v_s) ← p;  remove v_t
L7  return s

VSPLIT(M, s)
L8  F ← the faces around v_s counterclockwise from the edge to v_r up to the edge to v_l
L9  in every face of F, replace v_s by v_t
L10 p(v_s) ← s.p_s;  p(v_t) ← s.p_t
L11 put back f_l and f_r with their ids and corners

LINK(M, v_s, v_t)
L12 close the boundary with one extra vertex ω;  Lk(v) ← the vertices and edges opposite v
L13 return Lk(v_s) ∩ Lk(v_t) = Lk(v_s v_t)          ▷ Lk of the edge: v_l, v_r, and ω on a boundary edge

BUILD(M, n_0)
L14 while M has more than n_0 vertices and some edge passes LINK: v_s v_t ← the cheapest such edge; push ECOL(M, v_s, v_t, p)
L15 return M as M^0, and the pushed records in reverse order
```

**Line L8 in detail.** Around $v_t$ counterclockwise, $f_l$ turns from $v_l$ to $v_s$ and $f_r$ from $v_s$ to $v_r$, so the other faces of $v_t$ run from $v_r$ to $v_l$. Around $v_s$, $f_r$ turns from $v_r$ to $v_t$ and $f_l$ from $v_t$ to $v_l$, so the other faces of $v_s$ run from $v_l$ to $v_r$. After the collapse both runs are around $v_s$, and the run from $v_r$ to $v_l$ is exactly the old faces of $v_t$. When $v_t$ is on the boundary, its run has a gap: the walk goes from $v_r$ to the end of the fan of $v_s$, then from the start of the fan to $v_l$. When $v_r$ is missing, the walk starts at the start of the fan, and when $v_l$ is missing it ends at the end of the fan.

**The link condition.** The *link* of a vertex is the cycle (or path) of vertices and edges opposite it in its faces. Closing the boundary with one extra vertex $\omega$, joined to every boundary edge by a triangle, turns a mesh with boundary into a closed one. Line L13 is the condition of Dey, Edelsbrunner, Guha and Nekhayev. It forbids, for example, collapsing an edge of a tetrahedron (the two links share an edge), collapsing an inner edge whose two ends are both on the boundary (they share $\omega$, which would pinch the surface), and collapsing an edge whose ends have a third common neighbour (two edges would merge into one).

**Placement and cost.** The position $p$ and the order of the collapses are not part of the structure. The code of this page takes the shortest legal edge and its midpoint, with exact rational arithmetic. [Quadric error metrics](/quadric-error-metrics/) give a much better cost and position. Hoppe's construction minimized an energy of the distance to the original surface.

## Example

Take the octahedron with the vertices $0 = (1, 0, 0)$, $1 = (-1, 0, 0)$, $2 = (0, 1, 0)$, $3 = (0, -1, 0)$, $4 = (0, 0, 1)$, $5 = (0, 0, -1)$, and the faces $0{:}\,(0, 2, 4)$, $1{:}\,(2, 1, 4)$, $2{:}\,(1, 3, 4)$, $3{:}\,(3, 0, 4)$, $4{:}\,(2, 0, 5)$, $5{:}\,(1, 2, 5)$, $6{:}\,(3, 1, 5)$, $7{:}\,(0, 3, 5)$. Collapse $v_t = 4$ into $v_s = 0$ at $p = (\tfrac12, 0, \tfrac12)$.

- Line L1: face 3 is $(3, 0, 4)$, which contains $0 \to 4$, so $f_l$ is face 3 and $v_l = 3$. Face 0 is $(0, 2, 4)$, which contains $4 \to 0$, so $f_r$ is face 0 and $v_r = 2$.
- Line L2: the neighbours of 0 are $\{2, 3, 4, 5\}$ and those of 4 are $\{0, 1, 2, 3\}$. They share only $\{2, 3\} = \{v_r, v_l\}$, and the links share no edge, so the collapse is legal.
- Lines L3 to L6: the record is $(0, 4, 3, 2, (1, 0, 0), (0, 0, 1), \text{face } 3 = (3, 0, 4), \text{face } 0 = (0, 2, 4))$. Faces 1 and 2 become $(2, 1, 0)$ and $(1, 3, 0)$. The result has 5 vertices, 9 edges and 6 faces, so $V - E + F = 2$ is unchanged.

Now the split. Around vertex 0 the faces turn $2 \to 1$ (face 1), $1 \to 3$ (face 2), $3 \to 5$ (face 7) and $5 \to 2$ (face 4). Line L8 walks from $v_r = 2$: face 1 to 1, face 2 to 3, and stops at $v_l = 3$. So faces 1 and 2 get vertex 4 back, lines L10 and L11 restore the positions and faces 0 and 3, and the mesh is the octahedron again, equal in every entry.

**Measured.** The tests ran BUILD with the shortest edge first down to 4 vertices, and then all the splits, on these meshes (the coordinates jittered by rationals with seeds 1, 2 and 3):

| mesh | $V$, $F$ | legal edges at the start | base mesh $M^0$ | splits | splits with one face |
|---|---|---|---|---|---|
| octahedron | 6, 8 | 12 of 12 | 4 vertices, 4 faces | 2 | 0 |
| octahedron subdivided twice | 66, 128 | 192 of 192 | 4 vertices, 4 faces | 62 | 0 |
| torus grid $5 \times 6$ | 30, 60 | 90 of 90 | 7 vertices, 14 faces | 23 | 0 |
| grid disk $4 \times 5$ | 30, 40 | 67 of 69 | 4 vertices, 2 faces | 26 | 14 |

Every level $M^k$ rebuilt by REFINE was equal to the mesh after the matching collapse, and $M^n$ was equal to the input. The spheres end as a tetrahedron and the torus at 7 vertices; in both, every edge fails the link condition, so no further collapse is possible. The torus result agrees with the known fact that a triangulated torus needs at least 7 vertices; that fact is cited, not tested. These are measurements on these meshes, not bounds.

## Correctness

**Invariant.** After any sequence of legal collapses, the stack of records holds, for each collapse, everything it removed or changed except the faces that it moved from $v_t$ to $v_s$, and those faces are exactly the run of line L8 at the moment the split is applied.

The proof in [proofs/correctness.md](proofs/correctness.md) shows:

1. A legal collapse keeps $V - E + F$: it removes one vertex, three edges and two faces inside the surface, or one vertex, two edges and one face on a boundary edge, and it creates no repeated or degenerate face.
2. The run of line L8 is exactly the set of faces of $v_t$ other than $f_l$ and $f_r$, in all four cases (both faces present, $v_t$ on the boundary, $v_l$ missing, $v_r$ missing).
3. So $\mathrm{VSPLIT}(\mathrm{ECOL}(M)) = M$ exactly, and by induction on the stack, applying the first $k$ splits to $M^0$ gives $M^k$, for every $k$.

That a legal collapse keeps the mesh a manifold of the same topological type is the theorem of Dey, Edelsbrunner, Guha and Nekhayev; it is cited, not proved. The tests check it on every legal collapse of the meshes above.

## Complexity

With a hash set for each star, ECOL and VSPLIT look only at the faces of $v_s$ and $v_t$, and LINK builds two links of the same size, so each takes $O(d)$ time, expected for the hash sets, where $d$ is the number of faces at $v_s$ and $v_t$. REFINE to level $k$ costs the sum of these over the $k$ splits, which is $O(k)$ for meshes of bounded degree. The structure uses $\Theta(n)$ space: the base mesh and one record of fixed size per split.

BUILD as in the code scans all edges for each collapse, which is $O(n^2 d)$ in total. With a [priority queue](/priority-queue/) of edge costs that is updated after each collapse, as in quadric simplification, it takes $O(n d \log n)$ for bounded degree $d$.

## Variants

- **Geomorphs.** Instead of jumping from $M^k$ to $M^{k+1}$, move $v_t$ from $p_s$ to $p_t$ over a few frames, so that changes of level are not visible. Hoppe's paper describes this.
- **View-dependent refinement.** Hoppe in 1997 arranged the splits in a forest, so that each region of the mesh can be refined on its own, depending on the view. A split then needs its neighbours to be present, which adds dependency rules.
- **Half-edge collapse.** With $p$ always equal to the old position of $v_s$, no new positions are needed, and $v_s$ stays at a vertex of the input. This suits progressive transmission, because the coarse meshes use only input vertices.
- **Vertex removal and other operators.** Removing a vertex and filling the hole, or merging vertices that are not joined by an edge (vertex pair contraction, as in quadric simplification), give other progressive formats. Vertex pair contraction can change the topology, which a progressive mesh with the link condition never does.
- **Compression.** Progressive mesh compression codes the splits in batches with few bits each. Single-rate coders such as [Edgebreaker](/edgebreaker/) use fewer bits in total but cannot show coarse levels.

## When to use it

Use a progressive mesh when a mesh must be shown or sent at many levels of detail: streaming over a network, level of detail in games and viewers, or a coarse proxy for simulation. Every level is a valid manifold mesh, and moving between neighbouring levels costs $O(d)$ per vertex. If only one coarse level is needed, plain [mesh simplification](/mesh-simplification/) is simpler. If the mesh is only stored or sent once at full detail, a single-rate coder is smaller.

## Pitfalls

- **Skipping the link condition.** A collapse that fails it can glue two sheets, pinch the surface at a vertex, or make two faces with the same three vertices, as on a tetrahedron. The mesh then stops being a manifold, and later splits may not find their faces.
- **Fold-overs.** The link condition is about connectivity only. Moving $v_s$ to $p$ can still turn a face over, so that its normal points inward. Test the normals before and after, or in a flat parameter domain the sign of ORIENT2D, the [orientation test](/orientation-test/). In floating point that sign can be wrong for thin faces because of [catastrophic cancellation](/catastrophic-cancellation/); [exact arithmetic](/shewchuk-expansion-sum/) avoids it. This is the [robustness problem](/geometric-robustness-problem/) of geometry.
- **Storing the moved faces.** Recording the list of faces moved from $v_t$ to $v_s$ makes the record size depend on the degree. Deriving them from $v_l$ and $v_r$ keeps it fixed, but the walk must then handle the boundary gap of line L8, which a first version of the code of this page did not do: it failed on a corner vertex of a grid with only two faces.
- **Order of the splits.** A split is valid only on the mesh made by the earlier splits. Applying the splits out of order, or after an edit of the mesh, gives wrong faces without an error.
- **Attributes.** Normals, colours and texture coordinates on the corners also need to be restored. A record that stores only positions loses the seams of a texture atlas.

## Implementations

## History

Hugues Hoppe introduced progressive meshes at SIGGRAPH 1996, with the edge collapse as the only simplification step, the vertex split as its inverse, geomorphs between levels, and progressive transmission. He built the sequence by an energy that measured the distance to the original surface, from his earlier work on mesh optimization. In 1997 he extended it to view-dependent refinement. Michael Garland and Paul Heckbert's [quadric error metrics](/quadric-error-metrics/) of 1997 gave a fast cost for choosing the collapses. Dey, Edelsbrunner, Guha and Nekhayev stated the link condition in 1999 as the local test that an edge contraction keeps the topology of a manifold.

## References
