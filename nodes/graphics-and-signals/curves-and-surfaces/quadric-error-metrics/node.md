---
tag: HHFZ8A
kind: algorithm
slug: quadric-error-metrics
name: Quadric error metrics
aliases:
- Garland-Heckbert simplification
- QEM
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Simplifies a triangle mesh by greedy edge collapses; the cost of a collapse is the sum of squared distances to the planes of the old triangles, kept as a 4 by 4 matrix per vertex.
solves: [mesh-simplification]
model: real-ram
complexity:
  vars: {n: the number of triangles, d: the largest number of triangles at a vertex}
  time: {worst: O(n d^2 (d + log n))}
  space: {extra: O(n d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1997
  people: [Michael Garland, Paul Heckbert]
  note: Garland and Heckbert, at Carnegie Mellon University, kept the error of each vertex as a quadric, a sum of plane matrices, and contracted vertex pairs in the order of a heap, at SIGGRAPH 1997.
prereqs: [mesh-simplification, polygon-mesh, binary-heap]
see_also: [lazy-deletion, priority-queue, least-squares-problem, euler-formula, doubly-connected-edge-list, marching-cubes, poisson-surface-reconstruction, ball-pivoting-algorithm]
sources:
  - paper: doi:10.1145/258734.258849
    title: Michael Garland and Paul S. Heckbert, Surface simplification using quadric error metrics, Proceedings of SIGGRAPH 97, 209 to 216, 1997
    locator: the whole paper (the plane quadrics, the optimal position and its fallback, pair contraction with a heap, the normal flip test, the boundary planes)
  - paper: "Tamal K. Dey, Herbert Edelsbrunner, Sumanta Guha and Dmitry V. Nekhayev, Topology preserving edge contraction, Publications de l'Institut Mathématique (Beograd) 66(80), 23 to 45, 1999"
    locator: the link condition for edge contraction in 2-manifolds, with and without boundary
---

Quadric error metrics is a greedy algorithm for [mesh simplification](/mesh-simplification/). It collapses one edge of a triangle mesh at a time, and merges its two end points into one new vertex. Each vertex keeps a symmetric 4 by 4 matrix $Q$, the sum of the matrices of the planes of the original triangles that it stands for, and the error of a position $v$ is $\bar v^{\mathsf T} Q \bar v$ with $\bar v = (v, 1)$: the sum of the squared distances from $v$ to those planes. The edge with the least error goes first, taken from a [binary heap](/binary-heap/), so a mesh of $n$ triangles of bounded degree is reduced in $O(n \log n)$ time.

## In plain words

A mesh is made of flat triangles. To make it smaller, take one edge and pull its two end points together into one point. The two triangles on that edge disappear, and the triangles around them stretch to the new point.

Each original triangle lies on a flat plane. Every point of the mesh remembers the planes of the triangles that it has swallowed so far. When two points merge, the new point should stay close to all these planes. The algorithm places it where the total squared distance to them is least, and that total is the price of the merge.

Merge the cheapest edge first, then the next cheapest, until the mesh is small enough. A flat area costs nothing to merge, so it loses its points first, and sharp corners and edges stay to the end.

## The problem

The input is a [polygon mesh](/polygon-mesh/) with triangles only: points $p_1, \ldots, p_V$ and $n$ oriented triangles, and a target $m$. In the plain version the mesh is a 2-manifold, closed or with a border. The output is a mesh with at most $m$ triangles if the algorithm can get there, of the same topological type, whose vertices are near the original surface. For a triangle with unit normal $u$ and a point $p_0$ on it, let $\pi = (u, -u \cdot p_0)$, and let $K = \pi \pi^{\mathsf T}$; then $\bar v^{\mathsf T} K \bar v = (u \cdot v - u \cdot p_0)^2$ is the squared distance from $v$ to the plane of the triangle. Write a quadric as $Q = \begin{pmatrix} A & b \\ b^{\mathsf T} & c \end{pmatrix}$ with $A$ a 3 by 3 matrix.

## The algorithm

Each heap entry is an edge $(i, j)$ with $i < j$, its cost, its new position $\bar v$, and the version numbers of $i$ and $j$ when it was made. A vertex gets a new version when it moves, so older entries are stale; this is [lazy deletion](/lazy-deletion/) from a [priority queue](/priority-queue/).

```pseudo id=main
QEM-SIMPLIFY(p, T, m)
L1  for each triangle t do K_t ← π π^T for the unit plane π of t
L2  for each vertex i do Q_i ← the sum of K_t over the triangles t at i
L3  for each edge (i, j) do push (cost of (i, j), i, j, v̄) into the heap H
L4  while |T| > m and H is not empty do
L5      pop the entry (c, i, j, v̄) with the least (c, i, j); skip it if it is stale
L6      if the collapse breaks the link condition, or turns or flattens a triangle, then set it aside and continue
L7      p_i ← v̄; Q_i ← Q_i + Q_j
L8      remove the triangles at both i and j; put i for j in the other triangles; remove j
L9      for each neighbor k of i do push (cost of (i, k), i, k, v̄); put back the edges set aside at i and its neighbors
L10 return the points and the triangles that remain
OPTIMAL-POSITION(Q, p_i, p_j)
L11 if A is invertible then return -A^{-1} b, else return the best of p_i, p_j and (p_i + p_j) / 2
```

The cost of $(i, j)$ is $\bar v^{\mathsf T} (Q_i + Q_j) \bar v$ at $\bar v$ = OPTIMAL-POSITION$(Q_i + Q_j, p_i, p_j)$. The gradient of $\bar v^{\mathsf T} Q \bar v$ in $v$ is $2 (A v + b)$, so when $A$ is invertible, line L11 gives the unique minimizer; this is a 3 by 3 [least squares problem](/least-squares-problem/). $A$ is singular when all the planes are parallel to one line, for example on a flat region or along a straight crease. The paper then searches the segment from $p_i$ to $p_j$, and if that also fails it takes the best of the end points and the midpoint; the code here only does the last step.

The test of line L6 has two parts. The link condition of Dey, Edelsbrunner, Guha and Nekhayev: the vertices next to both $i$ and $j$ must be exactly the third vertices of the two triangles on the edge; no triangle $(i, u, w)$ may have a twin $(j, u, w)$; and on a mesh with a border, the border counts as one more vertex next to every border vertex, so an inner edge between two border vertices is not collapsed, and neither is an edge whose end points share a border neighbor. The normal test: each triangle that survives must keep a normal in the same half space, $N_{\text{old}} \cdot N_{\text{new}} > 0$. An entry that fails is set aside. It is put back into the heap only when the triangles at one of its end points change, in line L9, because the test depends on nothing else.

## Example

Take the cube $[0, 2]^3$ and split each face into 4 triangles around a center vertex. Then lift the center of the top face from $(1, 1, 2)$ to $(1, 1, 5/2)$, to make a low roof. The corners are $0$ to $7$, where corner $(x, y, z)$ has the number $x/2 + y + 2z$; the face centers are $8$ ($x = 0$), $9$ ($x = 2$), $10$ ($y = 0$), $11$ ($y = 2$), $12$ ($z = 0$) and the roof top $13$. That is 14 vertices and 24 triangles, and the target is $m = 12$. All values are exact rationals.

| step | edge | cost | new position | triangles after |
| --- | --- | --- | --- | --- |
| 1 | $(0, 8)$ | $0$ | $(0, 0, 0)$ | 22 |
| 2 | $(0, 10)$ | $0$ | $(0, 0, 0)$ | 20 |
| 3 | $(0, 12)$ | $0$ | $(0, 0, 0)$ | 18 |
| 4 | $(1, 9)$ | $0$ | $(2, 0, 0)$ | 16 |
| 5 | $(2, 11)$ | $0$ | $(0, 2, 0)$ | 14 |
| 6 | $(4, 13)$ | $16/19$ | $(4/19, 4/19, 45/19)$ | 12 |

A flat face center has a quadric of 4 copies of one plane. A corner has the planes of its three faces, so the sum $A$ is invertible, its minimizer is the corner, and the cost is 0. Many edges cost 0; the heap takes them in the order of $(i, j)$. The 5 flat centers go first. The roof top is next. Its 4 edges to the top corners all cost $16/19$ by symmetry, and $(4, 13)$ is the first of them. The new point minimizes
$$2x^2 + 2y^2 + \tfrac15 \left(2 (2z - y - 4)^2 + 2 (2z - x - 4)^2 + (2z + y - 6)^2 + (2z + x - 6)^2\right),$$
the sum over the quadrics of corner 4 and the roof top. The planes $x = 0$ and $y = 0$ count twice each, because two triangles of each face are at corner 4. The two roof planes at corner 4 count twice, once from the corner and once from the top, and the two other roof planes count once. At $(4/19, 4/19, 45/19)$ the terms are $2 \cdot \tfrac{16}{361} \cdot 2 = \tfrac{64}{361}$ and $\tfrac15 (2 \cdot 100 \cdot 2 + 400 \cdot 2) / 361 = \tfrac{240}{361}$, a total of $\tfrac{304}{361} = \tfrac{16}{19}$. The result is a closed mesh with 8 vertices and 12 triangles, $V - E + F = 8 - 18 + 12 = 2$; the corner $(0, 0, 2)$ moved up and in, toward the lost roof.

## Correctness

**Claim.** (1) For every vertex $i$, $\bar v^{\mathsf T} Q_i \bar v$ is the sum of the squared distances from $v$ to the planes of a multiset of original triangles, the ones that have been merged into $i$. (2) Line L11 returns the minimizer of this error when $A$ is invertible. (3) Each collapse of line L7 is a cheapest edge, in the order of $(c, i, j)$, among the edges that pass the test of line L6. (4) On a closed 2-manifold, or one with a border, every collapse keeps the topological type, so the Euler characteristic and the number of border loops do not change, and no surviving triangle turns over. (5) The loop stops.

Part (1) follows from line L2 and the sum in line L7, because a sum of plane quadrics gives a sum of squared distances. Part (2) is the gradient argument above, with $A$ positive semidefinite as a sum of $u u^{\mathsf T}$. Part (3) holds because, after each collapse, every current edge has a fresh heap entry with its current cost, or it is set aside and still fails the test. Part (4) is the theorem of Dey et al. on the link condition. Part (5): each collapse removes a vertex. The full proof is in [the correctness proof](proofs/correctness.md). These are all the guarantees. There is no bound on the distance from the output to the input in terms of the best mesh with $m$ triangles; the greedy order is a heuristic, and the error measure is only a bound for the planes near each vertex, not the Hausdorff distance.

## Complexity

The model is the [real RAM](/real-ram/).

- **Time.** Lines L1 to L3 take $O(n)$ steps and $O(n \log n)$ for the heap. A collapse at a vertex of degree at most $d$ does the test in $O(d)$ set operations, pushes $O(d)$ new entries, and puts back at most $O(d^2)$ edges set aside near it, each tested again in $O(d)$. Each pop costs $O(\log n)$, since the heap has $O(n d)$ entries. Stale entries are popped once each. There are at most $V$ collapses, so the total is $O(n d^2 (d + \log n))$. On meshes from scans and modeling tools the degree is bounded, and the time is $O(n \log n)$, as in the paper.
- **Space.** One quadric of 10 numbers per vertex, and $O(n d)$ heap entries.

## Properties

- **Cheap and local.** A quadric has 10 numbers, and merging two of them is one addition; no part of the old mesh is kept.
- **Greedy.** Each step is the best step only by the measure of that moment. The error of the final mesh has no worst case bound.
- **Underestimate.** The quadric counts the distance to whole planes, not to the triangles, and it counts a plane once for each vertex that held it. It is not the true distance to the input surface.
- **Topology.** With the link condition, the genus and the borders stay. Without it, and with pairs that are not edges, the paper joins separate parts on purpose.
- **Sharp features.** Corners and creases have quadrics of several planes with a large cost to move, so they stay longer than flat or smooth areas.

## Variants and improvements

- **Pair contraction.** The paper also contracts pairs of vertices closer than a threshold $t$ that are not joined by an edge. This joins nearby parts and changes the topology.
- **Borders.** For each border edge, the paper adds the quadric of a plane through the edge and perpendicular to its triangle, with a large weight, so that borders do not shrink.
- **Weights.** Multiply each $K_t$ by the area of $t$, so that small triangles count less. The code here weights all planes the same.
- **Attributes.** Garland and Heckbert extended the quadrics to colors and texture coordinates in 1998, and Hoppe gave another quadric for such attributes in 1999.
- **Memoryless.** Lindstrom and Turk, in 1998, compute the cost from the current mesh only, with no quadrics carried from the input.
- **Other placements.** Keep $v$ at $p_i$ or $p_j$ only (half edge collapse), which keeps the input points and makes progressive meshes easier to store.

## When to use it

Use quadric error metrics to reduce meshes from [marching cubes](/marching-cubes/), [Poisson surface reconstruction](/poisson-surface-reconstruction/), [ball pivoting](/ball-pivoting-algorithm/) or scanning when you need a good result fast, for example to make levels of detail. Many mesh libraries and tools use it. When you need a bound on the distance to the input, check the output against the input, or use a slower method that tracks the true error. To change the topology on purpose, use pair contraction or vertex clustering.

## Pitfalls

- **Planes without unit normals.** Building $K_t$ in line L1 from an unnormalized normal $N$ weights each plane by $|N|^2$, a power of the triangle area, and the costs then depend on the scale of the model. Divide by $|N|^2$ as in the code, or use the unit normal.
- **Stale entries.** Using a popped entry in line L5 without its version check collapses an edge with an old cost and an old position. Store the versions in the entry and skip it if a vertex has moved.
- **No link test.** Leaving out line L6 lets a collapse merge two triangles into one, fold a tetrahedron flat, or pinch the surface into a non-manifold vertex. Test the link condition, including the border vertex, and the normal flips.
- **Near singular systems.** Solving $A v = -b$ in line L11 when $A$ is nearly singular, as on a flat area in floating point, puts the vertex very far away. Test the determinant against a tolerance, and use the fallback.
- **Blocked edges forever.** Dropping an edge that fails line L6 for good loses collapses that become valid later. Put the edge back when its neighborhood changes, as in line L9.

## Implementations

## History

Michael Garland and Paul Heckbert presented the method at SIGGRAPH 1997, and Garland's thesis of 1999 at Carnegie Mellon University gives the full treatment. The edge collapse came from the mesh optimization of Hoppe, DeRose, Duchamp, McDonald and Stuetzle in 1993 and the progressive meshes of Hoppe in 1996, which used slower energy measures. Ronfard and Rossignac, in 1996, kept a set of planes at each vertex and used the largest distance; Garland and Heckbert replaced the set with the sum of squares, which fits in one matrix. The link condition for safe edge contraction was proved by Dey, Edelsbrunner, Guha and Nekhayev in 1999.

## References
