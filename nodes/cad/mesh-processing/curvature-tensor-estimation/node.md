---
tag: TJZ7S2
kind: algorithm
slug: curvature-tensor-estimation
name: Curvature tensor estimation
aliases:
- normal cycle curvature estimation
- Taubin curvature tensor
area: cad/mesh-processing
level: advanced
summary: Estimates principal curvatures and directions at mesh vertices, by Taubin's average of edge normal curvatures or by Cohen-Steiner and Morvan's tensor of dihedral angles.
model: real-ram
complexity:
  vars: {n: the number of vertices and faces of the mesh}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1995
  people: [Gabriel Taubin, David Cohen-Steiner, Jean-Marie Morvan]
  note: Taubin read the curvature tensor of a vertex from the normal curvatures along its edges. Cohen-Steiner and Morvan built a tensor from the dihedral angles of the edges and proved its convergence.
prereqs: [surface-curvature, discrete-mean-curvature, polygon-mesh]
see_also: [discrete-gaussian-curvature, cotangent-laplacian, isotropic-remeshing, anisotropic-mesh-adaptation, mesh-segmentation, taubin-smoothing, symmetric-eigenproblem]
sources:
  - paper: doi:10.1109/ICCV.1995.466840
    title: Gabriel Taubin, Estimating the tensor of curvature of a surface from a polyhedral approximation, Proceedings of the Fifth International Conference on Computer Vision (ICCV), 1995, 902 to 907
    locator: the normal curvature along an edge from the vertex normal, the weighted average of the edge tensors, and the principal curvatures from its eigenvalues
  - paper: doi:10.1145/777792.777839
    title: David Cohen-Steiner and Jean-Marie Morvan, Restricted Delaunay triangulations and normal cycle, Proceedings of the 19th Annual Symposium on Computational Geometry (SoCG), 2003, 312 to 321
    locator: the curvature measure from the dihedral angles of the edges in a region, and the error bound for restricted Delaunay triangulations of a smooth surface
  - paper: "Pierre Alliez, David Cohen-Steiner, Olivier Devillers, Bruno Lévy and Mathieu Desbrun, Anisotropic polygonal remeshing, ACM Transactions on Graphics 22(3), 2003, 485 to 493"
    title: Pierre Alliez, David Cohen-Steiner, Olivier Devillers, Bruno Lévy and Mathieu Desbrun, Anisotropic polygonal remeshing, ACM Transactions on Graphics 22(3), 2003, 485 to 493
    locator: the edge tensor averaged over a region around each vertex, and its principal directions used to trace lines of curvature for remeshing
---

Curvature tensor estimation finds, at each vertex of a triangle mesh, the two principal curvatures $k_1 \ge k_2$ and the two principal directions of the surface that the mesh approximates. The [mean curvature](/discrete-mean-curvature/) gives only $\frac{1}{2}(k_1 + k_2)$. The tensor also tells in which direction the surface bends most, which is what feature lines, curvature-aligned remeshing and shape analysis need. This page shows two methods. Taubin (1995) takes a normal curvature from each edge at the vertex, averages these samples as a tensor in the tangent plane, and corrects its eigenvalues by a fixed linear map. Cohen-Steiner and Morvan (2003) sum, over the edges in a region around the vertex, the dihedral angle times the length times the outer product of the edge direction, and divide by the area. Neither method is exact on a general mesh. Both are exact in known cases, which the correctness section states.

## In plain words

Stand on a curved surface and walk a short step in some direction. The ground drops away from your feet by some amount. If it drops a lot, the surface bends strongly in that direction. On a ball it drops the same amount in every direction. On a pipe it drops when you walk around the pipe, not when you walk along it.

On a mesh, each edge from a corner is a short step. The first method measures how much the ground drops along each edge, writes down that number with the direction of the edge, and finds the two directions in which the bending is largest and smallest. The second method looks at the folds between neighbouring triangles. A sharp fold across a direction means strong bending across it. Adding up the folds near a corner gives the same two directions and their bending.

## The problem

The input is a triangle [polygon mesh](/polygon-mesh/) with vertex positions $x_1, \ldots, x_n$ that sample a smooth surface, and optionally a unit normal $N_i$ at each vertex. The output, at each inner vertex $i$, is $k_1 \ge k_2$ and unit tangent vectors $d_1 \perp d_2$, estimates of the [principal curvatures](/surface-curvature/) and principal directions at $x_i$. The sign convention: a curvature is positive where the surface bends away from $N_i$, so a sphere with outward normals has $k_1 = k_2 = 1/r$. A vertex on the border, or whose region meets the border, gets no estimate.

## The algorithm

Taubin's method:

```pseudo id=main
TAUBIN-CURVATURE(x[1 .. n], faces)
L1  N_i ← unit(Σ over faces f at i of area(f) n_f) for each vertex i
L2  for each inner vertex i do
L3      for each neighbour j of i do
L4          T_ij ← unit((I − N_i N_iᵀ)(x_i − x_j));  κ_ij ← 2 N_i·(x_i − x_j) / |x_i − x_j|²
L5          w_ij ← total area of the faces that hold the edge ij
L6      M_i ← Σ_j w_ij κ_ij T_ij T_ijᵀ / Σ_j w_ij
L7      m1 ≥ m2 ← eigenvalues of M_i in the tangent plane, with unit eigenvectors d1, d2
L8      k1 ← 3m1 − m2;  k2 ← 3m2 − m1
    return (k1, k2, d1, d2) for each inner vertex
```

Line L4 is the curvature of the circle through $x_i$ and $x_j$ that is tangent to the plane normal to $N_i$ at $x_i$. Its direction $T_{ij}$ is the edge projected to that plane. Line L6 averages the samples as a $2 \times 2$ symmetric tensor in the tangent plane, and L7 finds its eigenvalues in closed form. Line L8 is the correction. If the samples were the exact normal curvatures $\kappa(\theta) = k_1\cos^2\theta + k_2\sin^2\theta$ spread evenly over all directions, the average would have the eigenvalues $\frac{3k_1 + k_2}{8}$ and $\frac{k_1 + 3k_2}{8}$, and L8 inverts this map. The code uses the sign convention of the problem statement.

The edge tensor of Cohen-Steiner and Morvan replaces lines L3 to L6. For a region $B$ around vertex $i$,

$$\bar T(B) = \frac{1}{|B|}\sum_{e} \beta(e)\,|e \cap B|\,\bar e\,\bar e^{\top},$$

where $\beta(e)$ is the signed angle between the normals of the two faces at the edge $e$, positive at a convex edge, $|e \cap B|$ is the length of the edge inside $B$, and $\bar e$ is the unit edge direction. The code takes for $B$ the mixed Voronoi cell of the vertex, which holds half of each edge at the vertex, or with `rings = r` the union of the cells of the vertices at most $r$ edges away. A fold along $\bar e$ bends the surface across $\bar e$, so the eigenvalue of the eigenvector $\bar e$ is the curvature in the tangent direction $N_i \times \bar e$. The two directions swap. The sign of $\beta$ comes from an exact orientation test on the four corners of the two faces, so it never flips by rounding.

## Example

**A sphere.** On icospheres of radius $r = 2$, where $k_1 = k_2 = 0.5$, the largest error of $k_1$ and $k_2$ over all vertices is, at 162, 642 and 2562 vertices:

| method | 162 | 642 | 2562 |
|---|---|---|---|
| Taubin | $0.052$ | $0.104$ | $0.121$ |
| edge tensor, the cell of the vertex | $0.036$ | $0.031$ | $0.030$ |
| edge tensor, the cells of the vertex and its neighbours | $0.031$ | $0.0115$ | $0.0061$ |

Taubin's error does not go down. Its mean $\frac{1}{2}(k_1 + k_2)$ is good, within $0.008$ with the normals of the mesh at 2562 vertices. With the true normals the mean is exact at every vertex, and both values are exact at the 12 vertices of valence 5. The error is in the split between $k_1$ and $k_2$ at the vertices of valence 6, whose six edge directions are not evenly spaced. The edge tensor on one cell does not converge either. On the larger region it does, at about first order in the edge length.

**A cylinder.** On a cylinder of radius 1 with $m$ columns of rectangles, each cut by the same diagonal into two right triangles, the edge tensor gives exactly $k_1 = \frac{\pi/m}{\sin(\pi/m)}$ around the axis and $k_2 = 0$ along it: $1.02617$, $1.00645$, $1.00161$, $1.00040$ for $m = 8, 16, 32, 64$. Taubin's method gives $1.221$ and $-0.221$ at $m = 8$, and $1.24500$ and $-0.24500$ at $m = 64$, near the limit $\frac{1}{2} \pm \frac{\sqrt 5}{3} \approx 1.2454, -0.2454$. The mean is right, and the split is wrong at every resolution, because the six edge directions of each vertex are 0°, 45° and 90° (each two times), not evenly spaced. On a twisted cylinder, where each ring of vertices is turned by half a column so that the six directions are nearly 60° apart, Taubin gives $k_1 = 1.00000$ and $k_2 = 0.00979$, $0.00242$, $0.00060$, $0.00015$ for $m = 8, 16, 32, 64$.

**A saddle.** On the grid of spacing $1/k$ on $z = \frac{1}{2}(x^2 - y^2)$, cut by the diagonal of direction $(1, 1)$, the true values at the origin are $\pm 1$. At $k = 4, 8, 16, 32$, Taubin gives $\pm 1.3128$, $\pm 1.3281$, $\pm 1.3320$, $\pm 1.3330$, which tends to $\pm\frac{4}{3}$, and the edge tensor on one cell gives $\pm 0.9574$, $\pm 0.9890$, $\pm 0.9972$, $\pm 0.9993$. Both put $k_1$ along the $y$ axis, where the surface bends down, away from the upward normal.

## Correctness

Neither method is exact on a general mesh. The proof file shows these facts:

- **The edge samples.** On a circle of radius $\rho$ through $x_i$ with center $x_i - \rho N_i$, line L4 gives exactly $1/\rho$. On a smooth surface with the true normal, it gives the normal curvature in the direction $T_{ij}$ up to $O(|x_i - x_j|)$.
- **Exact for balanced directions.** If the samples are exact normal curvatures and the weighted directions satisfy $\sum_j w_j e^{2\mathrm{i}\theta_j} = \sum_j w_j e^{4\mathrm{i}\theta_j} = 0$, then lines L6 to L8 return the exact $k_1$, $k_2$ and directions. Five or more evenly spaced directions with equal weights satisfy this. Four do not: for $k_1 = 1$, $k_2 = 0$ and directions on the principal axes, the output is $\frac{3}{2}$ and $-\frac{1}{2}$.
- **The mean is always the weighted mean of the samples.** $\frac{1}{2}(k_1 + k_2) = \sum_j w_j\kappa_{ij} / \sum_j w_j$, because each $T_{ij}T_{ij}^\top$ has trace 1. So on a sphere with the true normals the mean is exact on every mesh.
- **A bias that refinement keeps.** On the grid with one diagonal, the limits are $\pm\frac{4}{3}$ on the saddle and $\frac{1}{2} \pm \frac{\sqrt 5}{3}$ on the cylinder, as the example measures.
- **The edge tensor on a cylinder.** The closed form above holds for every region made of whole cells away from the border.
- **Exact signs and rigid motions.** The sign of each dihedral angle is exact. A rotation and a translation of the mesh do not change $k_1$ and $k_2$, and rotate the directions.

Cohen-Steiner and Morvan prove an error bound for the edge tensor on restricted Delaunay triangulations, when the region is large compared with the triangles. The page does not prove that bound. The convergence on the sphere is measured, not proved. The method stops: every loop is over a finite set, and the eigenvalues of a $2 \times 2$ symmetric matrix have a closed form.

## Complexity

Line L1 visits each face once. For each vertex, the loop of L3 to L5 walks the faces at the vertex and adds each face area to the two edges at the vertex that it holds, with a table indexed by the neighbour, so it costs time proportional to the degree. The degrees sum to twice the number of edges, and each edge is in one or two faces, so there are at most 3 edges per face. The total time is $\Theta(n)$ on the [real RAM](/real-ram/), with $n$ the number of vertices and faces, and the extra space is $\Theta(n)$ for the normals and the tables. The edge tensor costs $\Theta(n)$ for one cell per vertex, and $O(ns)$ when each region holds at most $s$ vertices.

## Properties

- **Not exact.** Both methods only approximate the curvature, and the error depends on the shape of the triangles, not only on their size.
- **Taubin's mean is robust.** The trace is a weighted mean of the samples, and only the split between $k_1$ and $k_2$ depends on the spacing of the edge directions.
- **Local.** Taubin's method and the one-cell edge tensor use only the first ring of each vertex. A larger region trades detail for stability.
- **Invariant under rigid motions.** The values do not change under rotations and translations. A uniform scale by $s$ divides them by $s$.
- **Signed.** At a concave vertex both curvatures are negative, and at a saddle they have opposite signs.

## Variants and improvements

- **Larger regions.** Alliez, Cohen-Steiner, Devillers, Lévy and Desbrun average the edge tensor over a disk of fixed geodesic radius, which smooths noise and makes the directions stable enough to trace lines of curvature.
- **Per-face tensors.** Rusinkiewicz (2004) fits a second fundamental form on each face from the differences of the vertex normals, then moves the face tensors to the vertex frames and averages them.
- **Fitting.** One can fit a quadric or a higher-order polynomial height function to the neighbours in a local frame, by least squares, and read the curvatures from its coefficients. Goldfeather and Interrante (2004) fit a cubic that also uses the normals.
- **From the mean and Gaussian curvatures.** $k_{1,2} = H \pm \sqrt{H^2 - K}$, with $H$ from the [discrete mean curvature](/discrete-mean-curvature/) and $K$ from the [angle defect](/discrete-gaussian-curvature/). This gives no directions.

## When to use it

Use the edge tensor over a region of a few rings when the directions matter, as for curvature-aligned [remeshing](/anisotropic-mesh-adaptation/), lines of curvature or [segmentation](/mesh-segmentation/), and when the mesh is dense compared with the features. Use Taubin's method when speed and simplicity count more than accuracy, and on meshes whose vertices have well-spread edge directions, such as the output of [isotropic remeshing](/isotropic-remeshing/). Use a fitting method on noisy scans or when higher derivatives are needed.

## Pitfalls

- **Grid meshes.** On a regular grid with one diagonal, Taubin's split between $k_1$ and $k_2$ is wrong by a fixed amount however fine the grid, as the cylinder and the saddle show.
- **The region is too small.** The edge tensor over one cell need not converge. Use a region that holds several rings.
- **The swap of the directions.** The edge tensor's eigenvector $\bar e$ is the direction of no bending for its eigenvalue. Reporting $\bar e$ as the direction of that curvature turns the result by 90°.
- **The sign of the normal.** If the faces are not consistently oriented, the normals and so the signs of the curvatures flip from vertex to vertex. Orient the mesh first.
- **Dihedral signs from floats.** Near-flat edges can get the wrong sign of $\beta$ from rounding. Decide the sign with an exact orientation test.
- **The border.** A vertex on the border has no full ring of edges, and the estimates there are biased. Skip it or use a fitting method.

## Implementations

## History

In 1995 Taubin observed that the curvature of the circle through a vertex and a neighbour, tangent to the vertex normal, is a sample of the normal curvature along the edge. He averaged these samples as a tensor and read the principal curvatures from its eigenvalues by a fixed linear map. In 2003 Cohen-Steiner and Morvan derived a curvature tensor of a polyhedral surface from the theory of normal cycles, as the sum of the dihedral angles of the edges in a region, and proved that it converges to the tensor of a smooth surface for restricted Delaunay triangulations. In the same year Alliez, Cohen-Steiner, Devillers, Lévy and Desbrun used this tensor to trace lines of curvature for anisotropic remeshing. Later methods, by Rusinkiewicz and by Goldfeather and Interrante in 2004, estimate the tensor per face or by fitting.

## References
