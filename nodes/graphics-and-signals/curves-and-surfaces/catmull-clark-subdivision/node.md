---
tag: 8H54E8
kind: algorithm
slug: catmull-clark-subdivision
name: Catmull-Clark subdivision
aliases:
- Catmull-Clark scheme
- Catmull-Clark surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Refines any closed polygon mesh into quads with face, edge and vertex points. The limit is the bicubic B-spline surface on the regular part, C2 there and C1 at extraordinary vertices.
solves: [surface-from-control-mesh]
model: real-ram
complexity:
  vars: {V: the number of vertices, E: the number of edges, F: the number of faces}
  time: {worst: Θ(V + E + F)}
  space: {extra: Θ(V + E + F)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1978
  people: [Edwin Catmull, Jim Clark]
  note: Catmull and Clark published the scheme in Computer-Aided Design in 1978, in the same issue as the scheme of Doo and Sabin.
prereqs: [polygon-mesh, b-spline, subdivision-surface]
see_also: [subdivision-surface, surface-from-control-mesh, doo-sabin-subdivision, loop-subdivision, lane-riesenfeld-algorithm, tensor-product-surface, knot-refinement, euler-formula]
sources:
  - paper: doi:10.1016/0010-4485(78)90110-0
    title: E. Catmull and J. Clark, Recursively generated B-spline surfaces on arbitrary topological meshes, Computer-Aided Design 10(6), 350-355 (1978)
    locator: the face, edge and vertex point rules, the vertex rule (Q + 2R + (n - 3)v)/n, and the reduction to bicubic B-spline refinement on a regular grid
  - paper: doi:10.1016/0010-4485(78)90111-2
    title: D. Doo and M. Sabin, Behaviour of recursive division surfaces near extraordinary points, Computer-Aided Design 10(6), 356-360 (1978)
    locator: the eigenvalue analysis of the subdivision matrix near an extraordinary point, applied to the Catmull-Clark rules
  - paper: doi:10.1145/280814.280945
    title: Jos Stam, Exact evaluation of Catmull-Clark subdivision surfaces at arbitrary parameter values, Proceedings of SIGGRAPH 98 (1998)
    locator: the eigen decomposition of the subdivision matrix that evaluates the limit surface near an extraordinary vertex without repeated subdivision
  - paper: "Jörg Peters and Ulrich Reif, Analysis of algorithms generalizing B-spline subdivision, SIAM Journal on Numerical Analysis 35(2), 728-748 (1998)"
    locator: the proof that the Catmull-Clark and Doo-Sabin limit surfaces are C1 at extraordinary points (check)
  - book: isbn:9781558604469
    title: Joe Warren and Henrik Weimer, Subdivision Methods for Geometric Design, A Constructive Approach, Morgan Kaufmann, 2002
    locator: Chapter 2 for the subdivision of uniform B-splines, and the chapters on polyhedral meshes for the quad schemes
---

Catmull-Clark subdivision refines a [polygon mesh](/polygon-mesh/) with faces of any size into a finer mesh of quads. Each step adds a point at the center of each face and on each edge, moves each old vertex to a weighted average of its neighbors, and splits each face of $k$ sides into $k$ quads. On a regular part of the mesh, where all faces are quads and all vertices have valence 4, the step is exactly the refinement of a bicubic uniform [B-spline](/b-spline/) surface, so the limit there is that surface and it is $C^2$. At the isolated extraordinary vertices the limit is $C^1$, and it is the standard scheme for smooth surfaces in film animation.

## In plain words

Start with a coarse cage of flat faces, such as a cube. Put a new point in the middle of each face. Put a new point on each edge, at the average of the two ends and the two face middles next to it. Then pull each old corner toward its neighbors. Join the points so that each old face becomes a ring of four-sided faces around its middle point.

The new cage is finer and a little rounder. Do it again, and again. The corners get rounder each time, and the cage settles on a smooth surface. Where the cage looks like a checkerboard, the surface is a standard smooth spline surface. At the few corners where more or fewer than four faces meet, it is still smooth, but less smooth.

## The problem

The input is a mesh $M = (V, E, F)$ with $V$ vertices, $E$ edges and $F$ faces, where the faces are polygons of any number of sides. The mesh is a closed oriented 2-manifold: each edge is in exactly two faces, with opposite directions, and the faces around each vertex form one cycle. The output is the mesh after one step, also a closed 2-manifold, with $V + E + F$ vertices and only quads. The limit of repeated steps is the [subdivision surface](/subdivision-surface/) of $M$.

The model is the [real RAM](/real-ram/), and the unit of work is one addition or scaling of a point. With integer or rational coordinates all new points are rational, and the implementation is exact.

## The algorithm

For a vertex $v$ of valence $n$, $Q$ is the average of the face points of the $n$ faces around $v$, and $R$ is the average of the midpoints $(v + u)/2$ of the $n$ edges $vu$.

```pseudo id=main
CATMULL-CLARK(M = (V, E, F))
L1  for each face f: face point q_f ← the average of the vertices of f
L2  for each edge ab in the faces f and g: edge point r_ab ← (a + b + q_f + q_g) / 4
L3  for each vertex v of valence n: Q ← the average of q_f over the faces f around v; R ← the average of (v + u)/2 over the edges vu
L4      vertex point v' ← (Q + 2R + (n − 3) v) / n
L5  for each face f = (v_0, ..., v_(k−1)) and each i: add the quad (v_i', r_(v_i v_(i+1)), q_f, r_(v_(i−1) v_i))
L6  return the new points and the new quads
```

Line L5 keeps the orientation of each face, so the new mesh has the same orientation. Lines L1 to L4 depend only on the old points, so they can run in any order, and in parallel.

On a mesh of quads, line L4 is the stencil

$$v' = \left(1 - \frac{7}{4n}\right) v + \frac{3}{2n^2} \sum_j e_j + \frac{1}{4n^2} \sum_j d_j,$$

where $e_j$ are the $n$ edge neighbors and $d_j$ the $n$ diagonal vertices of the faces around $v$. For $n = 4$ the weights are $9/16$, $3/32$ and $1/64$. Line L2 is $\frac{3}{8}(a + b) + \frac{1}{16}(c + d + e + f)$, where $c, d, e, f$ are the other vertices of the two quads.

## Example

Take the cube $[-1, 1]^3$ as a quad mesh with $V = 8$, $E = 12$ and $F = 6$. It is a closed 2-manifold with $\chi = 8 - 12 + 6 = 2$, and every vertex has valence $n = 3$, so all 8 are extraordinary.

| Step | Point | Rule | Value |
|---|---|---|---|
| L1 | face $x = 1$ | average of 4 corners | $(1, 0, 0)$ |
| L2 | edge from $(1, 1, 1)$ to $(1, 1, -1)$ | $(a + b + q_{x=1} + q_{y=1})/4$ | $\frac{1}{4}((2, 2, 0) + (1, 0, 0) + (0, 1, 0)) = (3/4, 3/4, 0)$ |
| L3 | vertex $(1, 1, 1)$ | $Q$ = average of $(1, 0, 0), (0, 1, 0), (0, 0, 1)$ | $(1/3, 1/3, 1/3)$ |
| L3 | vertex $(1, 1, 1)$ | $R$ = average of $(1, 1, 0), (1, 0, 1), (0, 1, 1)$ | $(2/3, 2/3, 2/3)$ |
| L4 | vertex $(1, 1, 1)$ | $(Q + 2R + 0 \cdot v)/3$ | $(5/9, 5/9, 5/9)$ |

The stencil gives the same point: $\frac{5}{12}$ of the corner, $\frac{1}{6}$ of each of the 3 edge neighbors and $\frac{1}{36}$ of each of the 3 diagonal vertices, which is $\frac{5}{12} + \frac{1}{6} - \frac{1}{36} = \frac{5}{9}$ in each coordinate.

The new mesh has $V' = 8 + 12 + 6 = 26$ vertices, $F' = 6 \cdot 4 = 24$ quads and $E' = 48$ edges, so $\chi = 26 - 48 + 24 = 2$. The 8 old corners still have valence 3, and the 18 new points have valence 4. A second step gives $V = 98$, $E = 192$ and $F = 96$. The corner moves from distance $\sqrt{3} \approx 1.73$ to $5\sqrt{3}/9 \approx 0.96$ from the center, while the face points stay at distance 1, so the cage becomes round.

## Correctness

The proof file shows four facts. First, the quads of line L5 form a closed oriented 2-manifold: each new directed edge is in one quad, and its reverse is in one other quad. Second, $V' = V + E + F$, $E' = 4E$ and $F' = 2E$, so $V' - E' + F' = V - E + F$, and the [Euler characteristic](/euler-formula/) is kept. Third, the stencils above follow from lines L1 to L4. Fourth, on a regular quad grid the weights are the tensor product of the cubic B-spline rules $\frac{1}{8}(1, 6, 1)$ and $\frac{1}{2}(1, 1)$, so a step is [knot refinement](/knot-refinement/) of a bicubic uniform B-spline surface. The surface does not change under this refinement, so the limit on the regular part is that surface, and it is $C^2$.

At an extraordinary vertex the limit is $C^1$. The proof uses the eigenvalues of the subdivision matrix and the characteristic map. Doo and Sabin began this analysis in 1978, and Peters and Reif gave a complete proof in 1998 (check). The proof file does not repeat it.

## Complexity

- **One step, $\Theta(V + E + F)$ time.** Each face point costs $\deg f$ additions, each edge point 4, and each vertex point $O(n)$. The sums are $\sum_f \deg f = 2E$ and $\sum_v n_v = 2E$. The edge lookup uses a hash map from directed edges to faces, which is expected $O(1)$ per edge.
- **Space, $\Theta(V + E + F)$.** The output has $V + E + F$ points and $2E$ quads.
- **$k$ steps.** After the first step all faces are quads, and each later step multiplies the number of faces by 4. So $k$ steps make $2E \cdot 4^{k-1}$ faces, and the time and memory grow by a factor of about 4 per step.

## Properties

- **Approximating.** The old vertices move, so the limit does not pass through the control points.
- **Quads after one step.** A face with $k$ sides becomes $k$ quads, and its face point becomes a vertex of valence $k$. So a mesh of triangles gives extraordinary vertices of valence 3 at the face points.
- **Extraordinary vertices are kept.** After the first step, the number of vertices with valence other than 4 does not change, and they move apart in the mesh with each step.
- **Smoothness.** $C^2$ on the regular part and $C^1$ at extraordinary vertices. At an extraordinary vertex the limit is in general not $C^2$, so the curvature there is not well behaved, and this can show as a small dent or flat spot in reflections.
- **Local and affine.** Each new point depends on the faces next to it, and the weights sum to 1, so the step commutes with affine maps.
- **Convex hull.** All weights are positive for $n \ge 3$, so each new point is in the convex hull of its stencil, and the limit is in the convex hull of the control mesh.
- **Exact on regular parts.** Over the inner cell of each $3 \times 3$ block of regular quads, the limit is the bicubic B-spline patch of its 16 control points, which can be evaluated directly.

## Variants and improvements

- **An equal form of the vertex rule.** $v' = \frac{n - 2}{n} v + \frac{1}{n^2} \sum_j u_j + \frac{1}{n^2} \sum_f q_f$, with the edge neighbors $u_j$ and the face points $q_f$. It gives the same weights.
- **Boundaries.** On a boundary edge, the edge point is the midpoint, and a boundary vertex uses the cubic B-spline curve rule $\frac{1}{8}(u_1 + 6 v + u_2)$ with its two boundary neighbors. The boundary curve is then a cubic B-spline.
- **Creases and corners.** Tagged edges use the curve rules on both sides, which gives sharp features. Semi-sharp creases use the curve rules for a few steps and the smooth rules after.
- **Exact evaluation (Stam 1998).** Near an extraordinary vertex, the eigen decomposition of the subdivision matrix gives the limit surface at any parameter without repeated steps. Away from them, the limit is a bicubic patch.
- **Limit positions and tangents.** Each vertex has a closed formula for its limit point and two tangent vectors, from the left eigenvectors of the subdivision matrix. On a regular vertex the limit point has the weights $\frac{1}{36}(1, 4, 1) \otimes (1, 4, 1)$.
- **Adaptive and GPU evaluation.** Refine only near extraordinary vertices and use bicubic patches elsewhere.
- **Other schemes.** [Doo-Sabin](/doo-sabin-subdivision/) is the dual biquadratic scheme, and [Loop](/loop-subdivision/) and [$\sqrt{3}$](/sqrt3-subdivision/) are the schemes for triangles.

## When to use it

Use it to make smooth surfaces from quad-dominant control meshes, as in character modeling and animation. It gives $C^2$ almost everywhere, simple rules, and exact bicubic patches on the regular part, so it fits with B-spline tools. For triangle meshes, the Loop scheme gives better shapes. When the surface must pass through the control points, use an interpolating scheme such as the [butterfly scheme](/butterfly-subdivision/).

## Pitfalls

- **Edge points in place of midpoints.** The vertex rule uses the average $R$ of the edge midpoints, not of the new edge points. With the new edge points, the weights change and the limit is not the B-spline surface.
- **Open meshes.** An edge with only one face has no second face point. Without boundary rules the step is not defined, and the implementation rejects such meshes.
- **Inconsistent orientation.** If two faces list a shared edge in the same direction, line L5 gives quads with opposite orientations, and the normals flip. Check that each directed edge is in one face only.
- **Memory.** Each step multiplies the number of faces by 4. Five steps of a mesh with 1000 quads give about one million quads.
- **Triangle input.** One step of a triangle mesh gives a vertex of valence 3 at the center of each triangle. The surface is smooth, but it often has bumps. Use a triangle scheme for triangle meshes.
- **Order of updates.** The vertex points use the old positions. Writing the vertex points into the old array before the edge points are computed gives wrong edge points.

## Implementations

The Python file in this folder has `catmull_clark(vertices, faces)`, which follows the pseudocode, `half_edges(faces)`, which builds the map from directed edges to faces and checks that the mesh is a closed oriented 2-manifold, and `euler_characteristic(faces)`. Points are tuples of any dimension, and with integers or fractions the result is exact. The tests check the cube example, the counts $V', E', F'$ and the Euler characteristic on a tetrahedron, a cube, a prism, two bipyramids and two tori, the stencil weights against the hand computation for valences 3 to 6, and on random regular tori the full result against the tensor product of the cubic B-spline rules, with the new quads against the cells of the fine grid.

## History

Edwin Catmull and Jim Clark published the scheme in 1978 in Computer-Aided Design, as a generalization of bicubic B-spline refinement to meshes of any topology. In the same issue Daniel Doo and Malcolm Sabin gave their dual scheme and the first analysis near extraordinary points with the eigenvalues of the subdivision matrix. Later work proved the $C^1$ continuity at extraordinary vertices, and Jos Stam showed in 1998 how to evaluate the limit surface exactly. In the late 1990s the scheme became a standard in film production, with added rules for creases.

## References
