---
tag: 4HZ1HE
kind: algorithm
slug: liepa-hole-filling
name: Liepa hole filling
aliases:
- minimum weight hole triangulation
area: cad/mesh-processing
level: advanced
summary: Liepa's method that triangulates a hole by dynamic programming over its boundary, minimising area and dihedral angles, then refines and fairs the patch.
solves: [hole-filling]
model: real-ram
complexity:
  vars: {n: the number of vertices of the border loop}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2003
  people: [Peter Liepa]
  note: Liepa gave the four steps (find the loop, triangulate by weight, refine, fair) at the first Symposium on Geometry Processing.
prereqs: [hole-filling, polygon-triangulation-dp]
see_also: [optimal-polygon-triangulation, min-weight-triangulation, catalan-triangulation-theorem, local-delaunay-criterion, laplacian-smoothing, implicit-fairing, volumetric-mesh-repair, mesh-repair-problem]
sources:
  - paper: doi:10.2312/SGP/SGP03/200-206
    title: Peter Liepa, Filling holes in meshes, Eurographics Symposium on Geometry Processing, 2003, 200 to 206
    locator: the weight of a triangulation (largest dihedral angle, then area), its dynamic program, and the refinement and fairing of the patch
  - paper: doi:10.1016/0167-8396(94)00011-G
    title: Gill Barequet and Micha Sharir, Filling gaps in the boundary of a polyhedron, Computer Aided Geometric Design 12(2), 1995, 207 to 229
    locator: the triangulation of a gap loop of least weight by dynamic programming in cubic time
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 8, Model Repair (the hole filling of Liepa as a surface-based repair method)
---

Liepa hole filling closes a hole of an oriented triangle mesh in three steps. First, a dynamic program over the border loop of $n$ vertices chooses the triangulation of the loop, with no new vertices, of least weight. The weight is a pair: the largest dihedral angle between neighbouring triangles, the mesh triangles at the loop included, and then the total area. Second, refinement splits large triangles at their centroids and flips edges, so that the patch gets the edge length of the mesh around it. Third, fairing moves the new vertices to a smooth position with the loop fixed. The program is the [polygon triangulation DP](/polygon-triangulation-dp/) of Klincsek and of Barequet and Sharir applied to a loop in space, and takes $\Theta(n^3)$ time and $\Theta(n^2)$ space. It solves the [mesh hole filling](/hole-filling/) problem for one loop, and the patch it gives is a guess at the missing surface, judged by how it looks and by measurement, not by a theorem.

## In plain words

A hole in a mesh has a ring of corners around it. Pick any way to cut the ring into triangles by joining its corners: that already closes the hole. There are very many ways, so we score each one. A cut is bad if two neighbouring triangles meet at a sharp fold, or if the triangles cover a lot of area.

Finding the best cut looks hard, but it is not. The side from the first corner to the last always belongs to one triangle, and that triangle splits the ring into two smaller rings. So solve all small rings first and build up.

The best cut has big, long triangles. So split each big one at its middle, flip edges that make thin triangles, and slide each new corner to the average of its neighbours. The patch is then smooth and as fine as the mesh around it.

## The problem

The input is an oriented manifold mesh with exact vertex positions and one border loop $v_0, \ldots, v_{n-1}$, listed in the direction in which the patch must use the loop edges, that is, against the direction of the mesh faces on them. For each loop edge $\{v_i, v_{i+1}\}$, let $o_i$ be the third vertex of the mesh triangle on it. The output is a set of triangles, with new vertices, whose border is the loop, so that the mesh with the patch has the loop edges as inner edges and a consistent orientation. The problem statement, its hardness, and other methods are on the [mesh hole filling](/hole-filling/) page.

## The algorithm

For a triangle $t = (v_i, v_m, v_k)$ with $i < m < k$, its weight is $\Omega(i, m, k) = (\theta, A)$, where $A$ is its area and $\theta$ is the largest dihedral angle between $t$ and its neighbours that are already known: the triangle chosen on the edge $\{i, m\}$ inside the part $P(i, m)$, or the mesh triangle with apex $o_i$ when $m = i + 1$; the same for the edge $\{m, k\}$; and the mesh triangle on $\{v_{n-1}, v_0\}$ when $(i, k) = (0, n - 1)$. The dihedral angle of two triangles is the angle between their normals by the right-hand rule, 0 when they are flat. Weights add by $(\theta, A) \oplus (\theta', A') = (\max(\theta, \theta'), A + A')$ and are compared in lexicographic order.

```pseudo id=main
LIEPA-FILL(M, v[0 .. n − 1])
L1  for i ← 0 to n − 2 do W[i][i + 1] ← (0, 0)
L2  for j ← 2 to n − 1 do                          ▷ by the length of the interval
L3      for i ← 0 to n − 1 − j do
L4          k ← i + j; W[i][k] ← ∞
L5          for m ← i + 1 to k − 1 do
L6              c ← W[i][m] ⊕ W[m][k] ⊕ Ω(i, m, k)
L7              if c < W[i][k] then W[i][k] ← c; O[i][k] ← m
L8  T ← the triangles (v_i, v_O[i][k], v_k), from (0, n − 1) down by the stored apexes
L9  repeat: split each triangle of T at its centroid x if α|x − v| > σ(v) and α|x − v| > σ(x) for its 3 vertices v
L10     flip each edge of T, not on the loop, whose two opposite angles sum to more than π
    until no triangle was split
L11 move each new vertex to the solution of the Laplace equation on T, with the loop fixed
    return T
```

Here $\sigma(v)$ is the mean length of the mesh edges at $v$ for a loop vertex, and $\sigma(x)$ is the mean of $\sigma$ at the three corners for a new centroid $x$. The factor $\alpha$ sets the density of the patch, and the code uses $\alpha = \sqrt{2}$.

**The predicate and its failure.** The angle term compares angles between normals, and each normal is a [cross product](/cross-product/) of edge vectors. For a nearly flat pair, the angle is near 0 and the normals are nearly parallel, so in floating point the cosine rounds to 1 and different near-flat choices tie. The choices of the program then depend on rounding. This does not break the result, since every triangulation closes the hole, but it makes the output depend on the order of the tests. A sliver triangle with a zero normal has no angle; the code gives it the worst angle $\pi$, so that the program avoids it when it can. With integer or rational coordinates and an exact weight such as the sum of the squared double areas, the program is exact.

## Example

**The area alone.** For the skew loop $v_0 = (0, 0, 0)$, $v_1 = (1, 0, 0)$, $v_2 = (1, 1, 0)$, $v_3 = (0, 1, 1)$, the [hole filling](/hole-filling/) page shows that the diagonal $\{0, 2\}$ gives area $1/2 + \sqrt{3}/2 \approx 1.366$, and the diagonal $\{1, 3\}$ gives $\sqrt{2} \approx 1.414$.

**The angle first.** Now let this loop be a hole in a folded sheet, with the mesh triangles $(v_1, v_0, o_0)$, $(v_2, v_1, o_1)$, $(v_3, v_2, o_2)$, $(v_0, v_3, o_3)$ and $o_0 = (0.5, -1, -6)$, $o_1 = (2, 0.5, -1)$, $o_2 = (0.5, 2, 0.5)$, $o_3 = (-1, 0.5, 0.5)$. The table follows lines L1 to L7.

| interval | apex | angles with the known neighbours | weight |
|---|---|---|---|
| $(0, 2)$ | 1 | with $o_0$: $80.54°$; with $o_1$: $45°$ | $(80.54°, 0.5)$ |
| $(1, 3)$ | 2 | with $o_1$: $0°$; with $o_2$: $0°$ | $(0°, 0.707)$ |
| $(0, 3)$ | $m = 1$ | with $o_0$: $35.54°$; with $(v_1, v_2, v_3)$: $60°$; with $o_3$: $0°$ | $(60°, 1.414)$ |
| $(0, 3)$ | $m = 2$ | with $(v_0, v_1, v_2)$: $54.74°$; with $o_2$: $35.26°$; with $o_3$: $35.26°$; and $80.54°$ from $W[0][2]$ | $(80.54°, 1.366)$ |

The angle with $o_0$ is $\arccos(1/\sqrt{37}) \approx 80.54°$, because the normal of $(v_1, v_0, o_0)$ is $(0, -6, 1)$ and the normal of $(v_0, v_1, v_2)$ is $(0, 0, 1)$. Line L7 keeps $m = 1$, since $60° < 80.54°$, and the patch is $(v_0, v_1, v_3)$, $(v_1, v_2, v_3)$. It has more area than the other choice, but it follows the two planes of the sheet, which meet at a crease of $60°$. On this small loop, the refinement of line L9 adds no vertex, because each centroid is closer to the corners than $\sigma / \alpha$.

## Correctness

Three facts are proved, and one is only measured.

- **The program is exact for a monotone weight.** If the weight of a triangle does not depend on its neighbours and the operation $\oplus$ is monotone, as sum and max are, the program returns a triangulation of least weight. Every triangulation of the part $v_i, \ldots, v_k$ has one triangle on the chord $\{v_i, v_k\}$, and its apex splits the rest into two smaller parts, so the induction of the [polygon triangulation DP](/polygon-triangulation-dp/) applies to the loop in space. The tests check this against all $C_{n-2}$ triangulations for loops up to 8 vertices, with the exact sum of squared double areas, with random integer tables, and with max.
- **Liepa's weight is not monotone, so the program is a heuristic for it.** The lexicographic pair fails monotonicity: $(1, 10) < (2, 0)$, but adding $(5, 0)$ gives $(5, 10) > (5, 0)$. A 5-vertex loop with such weights makes the program miss the optimum. The angle term also depends on the triangles chosen inside the parts. So the patch has the stated weight, but it need not be the best one. On random loops in the tests it was worse than the exhaustive optimum in 72 of 300 cases.
- **The patch closes the hole with a consistent orientation.** Each triangle $(v_i, v_m, v_k)$ uses its edges as $i \to m \to k \to i$. Each chord is used once in each direction, by the triangle below it and by its parent, and each loop edge once, against the mesh. Splits and flips keep these directed edges, and a flip that would make a third face on an edge is skipped.
- **The fairing has one solution.** With the loop fixed, the Laplace system on the new vertices is positive definite when each new vertex reaches the loop, so it has a unique solution, which is flat when the loop is flat.

The full proofs are below.

## Complexity

Lines L2 to L7 test each triple $i < m < k$ once, $\binom{n}{3}$ triples, each in $O(1)$ time on the [real RAM](/real-ram/) with one dihedral angle per known neighbour. So the program takes $\Theta(n^3)$ time, and the tables $W$ and $O$ take $\Theta(n^2)$ space. Line L8 takes $O(n)$ time. The refinement and the fairing depend on the size $p$ of the final patch, which depends on $\sigma$ and $\alpha$, not on $n$ alone. Each round of lines L9 and L10 takes about $O(p)$ time plus the flips. The fairing is a sparse linear system with $p$ unknowns. The code uses Gauss-Seidel sweeps, and a sparse direct or conjugate gradient solver is faster for large patches.

## Properties

- **No new vertices in the first step.** The program uses only loop vertices, so it cannot make a patch with a better shape than a triangulation of the loop allows. The refinement adds the inner vertices.
- **Not always embedded.** Nothing stops the patch from crossing itself or the mesh. Deciding whether a loop in space has a triangulation with its own vertices that does not cross itself is NP-complete, so a cubic program cannot promise it.
- **Deterministic.** Ties go to the smallest apex $m$.
- **Exact core.** With a monotone exact weight on rational coordinates, the triangulation step is exact. With Liepa's weight, angles are floating point values.

## Variants and improvements

- **Other weights.** The total area alone, the sum of the squared areas, the largest angle alone, or the sum of the dihedral angles. Sum and max weights per triangle keep the program exact. Barequet and Sharir weigh the triangles for long and thin gaps in CAD meshes.
- **Smoother fairing.** Liepa fairs with umbrella operators of the mesh. A Laplace equation gives a membrane that meets the mesh with a crease. A bi-Laplace equation also matches the normals at the loop and gives a thin plate. The [cotangent Laplacian](/cotangent-laplacian/) and [implicit fairing](/implicit-fairing/) give weights that depend less on the triangle shapes.
- **Remeshing in place of the splits.** Run [isotropic remeshing](/isotropic-remeshing/) on the patch with a target edge length taken from the mesh.
- **Islands and multiple loops.** The program fills one loop. Holes with islands need a bridge between the loops first, or a method of another type.
- **Search for embedded patches.** Some later methods add the test for crossing triangles into the search, at a higher cost.

## When to use it

Use it for holes of small and medium size in a scanned or edited mesh, where the patch should follow the surface around the hole and where the rest of the mesh should not change. It is the standard surface-based method, and it keeps every triangle of the input. For very large or very complex holes, for holes with islands, and for a model with many defects at once, a [volumetric mesh repair](/volumetric-mesh-repair/) or a reconstruction gives a closed result more reliably, at the cost of a new surface everywhere.

## Pitfalls

- **Holes that are not holes.** Each border loop of the mesh is a candidate, including the rim of a cup and the outline of an open sheet. Select the loops to fill, for example by their length.
- **Loops that touch themselves.** If a vertex appears twice in a loop, as when two holes meet at one vertex, a patch triangle can join the two copies, which gives a degenerate triangle or a non-manifold vertex. Split such loops first.
- **Chords that already exist.** A diagonal of the loop can already be an edge of the mesh, for example across a narrow neck. A patch triangle on it gives that edge three faces. Test the chords against the edges of the mesh and give such triangles an infinite weight.
- **Crossing patches.** For a loop with a strong twist, the best triangulation can cross itself. Test the result with a [mesh self-intersection](/mesh-self-intersection/) check.
- **Cubic time.** A loop of 2000 vertices takes about $1.3 \times 10^9$ steps. Cut very long loops into pieces first.
- **Wrong orientation.** The loop must be listed against the mesh faces. A loop in the wrong direction gives a patch that faces inward.

## Implementations

## History

Klincsek in 1980 and Gilbert in 1979 found the cubic dynamic program for the triangulation of least weight of a polygon. In 1995 Barequet and Sharir used it in space, to close the gaps between the faces of CAD models. In 2003 Liepa combined it with a weight that puts the dihedral angle first, and with refinement and fairing, so that the patch blends into the mesh around it. His method became the usual surface-based hole filler of mesh processing.

## References
