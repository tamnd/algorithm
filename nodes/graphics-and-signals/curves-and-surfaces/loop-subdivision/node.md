---
tag: 4625V7
kind: algorithm
slug: loop-subdivision
name: Loop subdivision
aliases:
- Loop scheme
- Loop subdivision surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Splits each triangle of a closed triangle mesh into four and moves the points by fixed weights. The limit is the quartic box spline surface, C2 on the regular part and C1 at other vertices.
solves: [surface-from-control-mesh]
model: real-ram
complexity:
  vars: {V: the number of vertices, E: the number of edges, F: the number of faces}
  time: {worst: Θ(V + E + F)}
  space: {extra: Θ(V + E + F)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Charles Loop]
  note: Charles Loop gave the scheme in his master's thesis at the University of Utah in 1987, as a generalization of the quartic three direction box spline to triangle meshes of any topology.
prereqs: [polygon-mesh, b-spline, subdivision-surface]
see_also: [subdivision-surface, surface-from-control-mesh, catmull-clark-subdivision, butterfly-subdivision, sqrt3-subdivision, knot-refinement, euler-formula, eigenvalue]
sources:
  - paper: "Charles Loop, Smooth subdivision surfaces based on triangles, M.S. thesis, Department of Mathematics, University of Utah, 1987"
    locator: the edge and vertex rules, the weight beta_n with the cosine, and the analysis of the extraordinary vertices
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: the chapters on box splines and on triangle meshes, for the mask of the three direction quartic box spline and the simpler weight 3/(8n)
  - book: isbn:9783540764052
    title: Jörg Peters and Ulrich Reif, Subdivision Surfaces, Springer, 2008
    locator: the analysis of the subdivision matrix and the characteristic map, which gives the C1 property of Loop's scheme at extraordinary vertices (check)
---

Loop subdivision refines a closed triangle [polygon mesh](/polygon-mesh/) by splitting each triangle into four. It adds a point on each edge and moves each old vertex toward its neighbors, with weights that depend only on the valence. On the regular part of the mesh, where six triangles meet at each vertex, a step is exactly the refinement of the quartic three direction box spline, so the limit there is that surface and it is $C^2$. At the isolated extraordinary vertices the limit is $C^1$, and the scheme is the standard smooth scheme for triangle meshes.

## In plain words

Start with a coarse cage of flat triangles, such as a tetrahedron. Put a new point on each edge, mostly from the two ends of the edge and a little from the two corners across it. Then pull each old corner toward the corners around it. Join the new points so that each old triangle becomes four smaller triangles: one at each corner and one in the middle.

The new cage is finer and rounder. Do it again, and again, and the cage settles on a smooth surface. Where six triangles meet at every corner, the surface is a standard smooth spline surface. At the few corners where more or fewer than six meet, it is still smooth, but less smooth.

## The problem

The input is a triangle mesh $M = (V, E, F)$ with $V$ vertices, $E$ edges and $F$ triangles. The mesh is a closed oriented 2-manifold: each edge is in exactly two triangles, with opposite directions, and the triangles around each vertex form one cycle. Then $3F = 2E$. The output is the mesh after one step, also a closed oriented 2-manifold, with $V + E$ vertices and $4F$ triangles. The limit of repeated steps is the [subdivision surface](/subdivision-surface/) of $M$.

The model is the [real RAM](/real-ram/), and the unit of work is one addition or scaling of a point. With rational coordinates the new points are rational for the valences 3, 4 and 6, and with the simpler weight of Warren for all valences.

## The algorithm

For a vertex $v$ of valence $n$, the weight of each neighbor is
$$\beta_n = \frac{1}{n} \left( \frac{5}{8} - \left( \frac{3}{8} + \frac{1}{4} \cos \frac{2\pi}{n} \right)^2 \right).$$

```pseudo id=main
LOOP(M = (V, E, F))
L1  for each edge ab with the triangles (a, b, c) and (b, a, d): edge point e_ab ← 3/8 (a + b) + 1/8 (c + d)
L2  for each vertex v with the neighbors u_1, ..., u_n: vertex point v' ← (1 − n β_n) v + β_n (u_1 + ... + u_n)
L3  for each triangle (a, b, c): add (a', e_ab, e_ca), (b', e_bc, e_ab), (c', e_ca, e_bc) and (e_ab, e_bc, e_ca)
L4  return the new points and the new triangles
```

Lines L1 and L2 use only the old points, so they can run in any order, and in parallel. Line L3 keeps the orientation of each triangle, so the new mesh has the same orientation. The weights give $\beta_3 = \frac{3}{16}$, $\beta_4 = \frac{31}{256}$ and $\beta_6 = \frac{1}{16}$, so a regular vertex keeps $\frac{10}{16}$ of itself and takes $\frac{1}{16}$ of each of its six neighbors.

## Example

Take the regular tetrahedron with the vertices $p_0 = (1, 1, 1)$, $p_1 = (1, -1, -1)$, $p_2 = (-1, 1, -1)$ and $p_3 = (-1, -1, 1)$, and the triangles $(0,1,2)$, $(0,3,1)$, $(0,2,3)$ and $(1,3,2)$. It has $V = 4$, $E = 6$ and $F = 4$, it is a closed 2-manifold with $\chi = 4 - 6 + 4 = 2$, and every vertex has valence $n = 3$.

| Step | Point | Rule | Value |
|---|---|---|---|
| L1 | edge $p_0 p_1$, with $c = p_2$ and $d = p_3$ | $\frac38 (p_0 + p_1) + \frac18 (p_2 + p_3)$ | $\frac38 (2, 0, 0) + \frac18 (-2, 0, 0) = (\frac12, 0, 0)$ |
| L2 | vertex $p_0$ | $\beta_3 = \frac{3}{16}$, so $\frac{7}{16} p_0 + \frac{3}{16}(p_1 + p_2 + p_3)$ | $\frac{7}{16}(1,1,1) - \frac{3}{16}(1,1,1) = (\frac14, \frac14, \frac14)$ |
| L3 | triangle $(0, 1, 2)$ | four new triangles | $(p_0', e_{01}, e_{20})$, $(p_1', e_{12}, e_{01})$, $(p_2', e_{20}, e_{12})$, $(e_{01}, e_{12}, e_{20})$ |

The new mesh has $V' = 4 + 6 = 10$ vertices, $E' = 2 \cdot 6 + 3 \cdot 4 = 24$ edges and $F' = 16$ triangles, so $\chi = 10 - 24 + 16 = 2$. The 4 old vertices still have valence 3, and the 6 edge points have valence 6. A second step gives $V = 34$, $E = 96$ and $F = 64$. The corner moves from distance $\sqrt{3} \approx 1.73$ to $\sqrt{3}/4 \approx 0.43$ from the center, and its limit point is $(\frac15, \frac15, \frac15)$, at distance $\approx 0.35$. The scheme shrinks a coarse mesh a lot, because it does not pass through the control points.

## Correctness

The proof file shows five facts. First, the triangles of line L3 form a closed oriented 2-manifold: each new directed edge is in one triangle, and its reverse is in one other triangle. Second, $V' = V + E$, $E' = 2E + 3F$ and $F' = 4F$, so $V' - E' + F' = V - E + F$, and the [Euler characteristic](/euler-formula/) is kept. Third, the weights sum to 1, and the cosine formula gives $\frac{3}{16}$, $\frac{31}{256}$ and $\frac{1}{16}$ for the valences 3, 4 and 6. Fourth, on a regular mesh on a torus, the new points are $q_\alpha = \sum_\beta a_{\alpha - 2\beta} p_\beta$ with the mask $\frac{1}{16}(1 + x)^2 (1 + y)^2 (1 + xy)^2$ of the quartic box spline with the directions $(1,0)$, $(0,1)$ and $(1,1)$, each twice. So a step is refinement of that box spline surface, like [knot refinement](/knot-refinement/) for a [B-spline](/b-spline/), and the limit on the regular part is the box spline surface, which is $C^2$. Fifth, the value $\frac{\omega v + \sum_j u_j}{\omega + n}$ with $\omega = \frac{3}{8 \beta_n}$ does not change in a step, so it is the limit point of $v$.

At an extraordinary vertex the limit is $C^1$. Loop chose $\beta_n$ so that the subdivision matrix has the eigenvalues that this needs. The full proof uses the characteristic map, and the proof file does not repeat it (check).

## Complexity

- **One step, $\Theta(V + E + F)$ time.** Each edge point costs 4 additions, and each vertex point costs $n_v + 1$. The sums are $E$ and $\sum_v n_v = 2E$. The lookup of the triangles at an edge uses a hash map from directed edges to triangles, which is expected $O(1)$ per edge.
- **Space, $\Theta(V + E + F)$.** The output has $V + E$ points and $4F$ triangles.
- **$k$ steps.** Each step multiplies the number of triangles by 4, so $k$ steps make $4^k F$ triangles, and the time and memory grow by a factor of 4 per step.

## Properties

- **Approximating.** The old vertices move, so the limit does not pass through the control points.
- **Primal.** The old vertices stay as vertices, and the topology of a step is the split of each triangle into four. The [butterfly scheme](/butterfly-subdivision/) uses the same split.
- **Extraordinary vertices are kept.** All new vertices have valence 6, and the old vertices keep their valence. So the number of extraordinary vertices does not change, and they move apart in the mesh with each step.
- **Smoothness.** $C^2$ on the regular part and $C^1$ at extraordinary vertices (check). At an extraordinary vertex the limit is in general not $C^2$, and the curvature there is not well behaved (check), so the reflections can show a small flat spot or a bump.
- **Local and affine.** Each new point depends on its 1-ring only, and the weights sum to 1, so the step commutes with affine maps.
- **Convex hull.** All weights are positive for $n \ge 3$, so each new point is in the convex hull of its stencil.
- **Limit points.** The limit point of a vertex is $\frac{\omega v + \sum_j u_j}{\omega + n}$ with $\omega = \frac{3}{8 \beta_n}$, without more steps. For $n = 6$ it is $\frac12 v + \frac{1}{12} \sum_j u_j$.

## Variants and improvements

- **Warren's weight.** $\beta_n = \frac{3}{8n}$ for $n > 3$ and $\beta_3 = \frac{3}{16}$. It is rational, it is the same as Loop's weight for $n = 3$ and $n = 6$, and it also gives a smooth limit (check). The implementation has it as `rule="warren"`.
- **Boundaries and creases.** On a boundary edge, the edge point is the midpoint, and a boundary vertex uses the cubic B-spline curve rule $\frac{1}{8}(u_1 + 6 v + u_2)$ with its two boundary neighbors. Tagged edges use the same curve rules for sharp features.
- **Exact evaluation.** As for [Catmull-Clark](/catmull-clark-subdivision/), the eigen decomposition of the subdivision matrix gives the limit surface near an extraordinary vertex without repeated steps. Away from them, each triangle of the limit is a quartic box spline patch.
- **Other triangle schemes.** The [$\sqrt{3}$ scheme](/sqrt3-subdivision/) adds one point per face and grows the mesh more slowly. The [butterfly scheme](/butterfly-subdivision/) keeps the old points, so it interpolates them.
- **Quad schemes.** [Catmull-Clark](/catmull-clark-subdivision/) and [Doo-Sabin](/doo-sabin-subdivision/) work on quads and on faces of any size.

## When to use it

Use it to make smooth surfaces from triangle meshes, for example from scans or from meshes that a [surface tessellation](/surface-tessellation/) made. It gives $C^2$ almost everywhere with a 1-ring stencil, which is small. For quad meshes, Catmull-Clark gives better shapes. When the surface must pass through the control points, use the butterfly scheme. To go the other way, from a fine mesh to a coarse one, see [mesh simplification](/mesh-simplification/).

## Pitfalls

- **Non-triangle faces.** The rules are for triangles. Triangulate the mesh first, or use Catmull-Clark.
- **Old points in place of new ones.** Lines L1 and L2 use the old points only. Writing the vertex points into the old array before the edge points are computed gives wrong edge points.
- **Open meshes.** An edge with only one triangle has no point $d$. Without boundary rules the step is not defined, and the implementation rejects such meshes.
- **Inconsistent orientation.** If two triangles list a shared edge in the same direction, the twin of the edge is missing, and the new triangles have opposite normals. The implementation checks that each directed edge is in one triangle only.
- **Shrinkage.** A coarse mesh shrinks a lot. The tetrahedron with corners at distance $\sqrt{3}$ gives a limit with corners at distance $\sqrt{3}/5$. To fit given points, move the control points first, or use an interpolating scheme.
- **Floating point weights.** For valences other than 3, 4 and 6, Loop's $\beta_n$ is irrational, so the result is not exact. Use Warren's weight when exact rational output is needed.
- **Memory.** Each step multiplies the number of triangles by 4. Five steps of a mesh with 1000 triangles give about one million triangles.

## Implementations

The Python file in this folder has `loop_subdivision(vertices, faces, rule)`, which follows the pseudocode, `loop_beta(n, rule)`, which gives Loop's weight or Warren's weight, `half_edges(faces)`, which builds the map from directed edges to the third vertex and checks that the mesh is a closed oriented 2-manifold, and `euler_characteristic(faces)`. The new points are the vertex points and then the edge points in the order of the sorted edges. The sort is only for a fixed output order, and an insertion order would keep the time linear. The tests check the tetrahedron example, the counts $V', E', F'$ and the Euler characteristic on a tetrahedron, an octahedron, two bipyramids and two tori, the stencil weights against the hand computation, Warren's weights, the limit point formula, and on random regular tori the full result against the box spline mask $\frac{1}{16}(1 + x)^2 (1 + y)^2 (1 + xy)^2$.

## History

Charles Loop gave the scheme in his 1987 master's thesis at the University of Utah. He started from the quartic box spline with three directions, each twice, whose refinement gives the rules on a regular triangle mesh, and he chose the vertex weight $\beta_n$ for the other valences so that the limit is smooth there. In the 1990s the scheme became the standard smooth scheme for triangle meshes, and Warren and others gave the simpler weight $3/(8n)$.

## References
