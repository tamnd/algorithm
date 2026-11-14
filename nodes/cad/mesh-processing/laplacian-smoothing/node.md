---
tag: 8BS9ES
kind: algorithm
slug: laplacian-smoothing
name: Laplacian smoothing
aliases:
- umbrella smoothing
area: cad/mesh-processing
level: intro
summary: Moves each vertex toward the average of its neighbours, step by step. It removes noise but also shrinks the mesh.
model: real-ram
complexity:
  vars: {n: the number of vertices, K: the number of steps}
  time: {worst: Θ(K n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1988
  people: [David A. Field, Gabriel Taubin]
  note: Moving a node to the centroid of its neighbours was in use for finite element meshes before Field's 1988 paper; Taubin in 1995 explained it as a low-pass filter and showed why it shrinks.
prereqs: [laplacian-matrix, polygon-mesh, manifold-mesh]
see_also: [taubin-smoothing, implicit-fairing, cotangent-laplacian, isotropic-remeshing, tutte-embedding, image-smoothing, jacobi-method, liepa-hole-filling]
sources:
  - paper: doi:10.1002/cnm.1630040603
    title: David A. Field, Laplacian smoothing and Delaunay triangulations, Communications in Applied Numerical Methods 4(6), 1988, 709 to 712
    locator: the smoothing step that moves each node to the centroid of its neighbours, and its effect on the angles of a planar triangulation
  - paper: doi:10.1145/218380.218473
    title: Gabriel Taubin, A signal processing approach to fair surface design, Proceedings of SIGGRAPH 95, 1995, 351 to 358
    locator: the Laplacian smoothing step as a filter on the eigenvectors of the Laplacian, its transfer function 1 - lambda k, and the shrinkage it causes
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 4, Smoothing (Laplacian smoothing as diffusion with an explicit step, uniform and cotangent weights, shrinkage)
---

Laplacian smoothing moves every vertex of a mesh a fraction $\lambda$ of the way toward the average of its neighbours, and repeats this step $K$ times. The average minus the vertex is the *umbrella vector* $U(x)_i$, the uniform [graph Laplacian](/laplacian-matrix/) of the positions, so one step is $x \leftarrow x + \lambda U(x)$, an explicit step of the diffusion $\dot x = U(x)$. Noise is the part of the shape that changes fast from vertex to vertex, and the step damps it most. But every step also pulls a closed mesh inward, and after many steps the mesh collapses to a point. On an open mesh, the border is held fixed, and the vertices tend to the solution of a discrete Laplace equation. It costs $\Theta(n)$ time per step on a mesh with $n$ vertices.

## In plain words

Each corner of the mesh looks at the corners joined to it, finds their middle, and steps part of the way there. A corner that sticks out of a smooth surface, because of noise, is far from the middle of its neighbours, so it moves a lot. A corner on a smooth part moves little.

All corners move at once, using the old positions, and the whole thing is repeated a few times. The surface gets smoother after each round.

The catch is that on a round surface the middle of the neighbours is always a bit inside, so every corner moves a bit inward, even where there is no noise. A ball smoothed many times gets smaller and smaller and ends as a point. Corners on the edge of an open sheet are kept still, so that the sheet does not pull in from its edges.

## The problem

The input is a triangle mesh with vertex positions $x_1, \ldots, x_n \in \mathbb{R}^3$, its faces, a factor $0 < \lambda < 1$, a number of steps $K$, and a set $F$ of fixed vertices, by default the border vertices of the mesh. The output is new positions with the same connectivity, smoother in the sense that the high-frequency part of the shape is damped. There is no single target shape: the result depends on $\lambda$ and $K$, and the user stops when the noise is gone. The [Taubin smoothing](/taubin-smoothing/) and [implicit fairing](/implicit-fairing/) pages solve the same task with less shrinkage and with larger steps.

## The algorithm

Let $N(i)$ be the set of neighbours of vertex $i$ and $d_i = |N(i)|$ its valence. The centroid of the neighbours is $c_i = \frac{1}{d_i}\sum_{j \in N(i)} x_j$, and the umbrella vector is $U(x)_i = c_i - x_i$.

```pseudo id=main
LAPLACIAN-SMOOTH(x[1 .. n], faces, λ, K, F)
L1  N ← the neighbour lists of the mesh; F ← the border vertices if not given
L2  for k ← 1 to K do
L3      for each vertex i ∉ F do
L4          c_i ← (1 / d_i) Σ_{j ∈ N(i)} x_j
L5          y_i ← x_i + λ (c_i − x_i)
L6      y_i ← x_i for each i ∈ F
L7      x ← y                                   ▷ all vertices move at once
    return x
```

All new positions are computed from the old ones, which is a [Jacobi](/jacobi-method/) step. In matrix form, one step on the free vertices is $x \leftarrow S x$ with

$$S = (1 - \lambda) I + \lambda D^{-1} A,$$

where $A$ is the adjacency matrix of the edge graph and $D = \operatorname{diag}(d_i)$, and $S$ is the identity on the rows of $F$. The positions are treated one coordinate at a time, and the step uses no geometric predicate, only sums and one division per vertex. With rational coordinates and a rational $\lambda$, it is exact, and the code follows it with `Fraction`.

## Example

**One noisy vertex in a flat grid.** Take the $4 \times 4$ grid of points $(i, j, 0)$, $0 \le i, j \le 3$, with each square cut by the diagonal from $(i, j)$ to $(i + 1, j + 1)$. The four inner vertices $a = (1, 1)$, $b = (2, 1)$, $c = (1, 2)$, $e = (2, 2)$ have valence 6, and the twelve border vertices are fixed. Lift $a$ to height $z = 1$ and smooth with $\lambda = \frac{1}{2}$. The $x$ and $y$ coordinates do not move, because each inner vertex of this grid is the centroid of its six neighbours. Only the heights change.

| step | $z_a$ | $z_b$ | $z_c$ | $z_e$ |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 1 | $1/2$ | $1/12$ | $1/12$ | $1/12$ |
| 2 | $13/48$ | $13/144$ | $13/144$ | $7/72$ |
| 3 | $137/864$ | $131/1728$ | $131/1728$ | $149/1728$ |

In step 1, the neighbours of $a$ all have height 0, so $z_a = 1 + \frac{1}{2}(0 - 1) = \frac{1}{2}$. Each of $b, c, e$ has $a$ as one of its six neighbours, so its centroid has height $\frac{1}{6}$ and it moves to $\frac{1}{12}$. In step 2, $a$ has three neighbours at $\frac{1}{12}$ and three on the border, so $c_a$ has height $\frac{1}{24}$ and $z_a = \frac{1}{2} + \frac{1}{2}(\frac{1}{24} - \frac{1}{2}) = \frac{13}{48}$. The bump spreads and sinks, and the heights tend to 0, the flat grid held by its border.

**A closed mesh.** On the octahedron with vertices $(\pm 1, 0, 0)$, $(0, \pm 1, 0)$, $(0, 0, \pm 1)$, the four neighbours of each vertex sum to 0, so $c_i = 0$ and each step with $\lambda = \frac{1}{2}$ halves every position. After three steps the octahedron is $\frac{1}{8}$ of its size, with the same shape. On the icosphere with 162 vertices on the unit sphere, the measured volume after 1, 10 and 50 steps with $\lambda = \frac{1}{2}$ is $0.934$, $0.507$ and $0.034$ times the start. The mesh has no noise at all, and smoothing still shrinks it.

## Correctness

Smoothing has no single right output, so the claims are about what each step does and where the steps lead. These are proved:

- **The step is the matrix $S$.** Line L5 is $y_i = (1 - \lambda)x_i + \frac{\lambda}{d_i}\sum_j x_j$, row $i$ of $S$. So $K$ steps give $S^K x$, and the tests compare the code with this product exactly.
- **Affine invariance.** Each new position is an affine combination of old ones, with weights summing to 1, so smoothing commutes with rotations, translations and scalings, and a mesh in a plane stays in the plane.
- **Fixed points.** A vertex whose position is the centroid of its neighbours does not move. Every inner vertex of the regular grid above is such a vertex, by point symmetry of its six neighbours.
- **A closed mesh tends to one point.** With no fixed vertex, $\sum_i d_i x_i$ is the same after every step. If the mesh is connected and $0 < \lambda < 1$, all positions converge to the weighted centroid $\sum_i d_i x_i / \sum_i d_i$. This is the shrinkage, in its limit.
- **An open mesh tends to a membrane.** If every connected part of the mesh has a fixed vertex and $0 < \lambda < 1$, the free positions converge to the unique solution of $x_i = c_i$ for all $i \notin F$, the discrete harmonic map with the uniform weights, as in a [Tutte embedding](/tutte-embedding/).

The rate of shrinking on a given mesh is only measured, as in the example. The proofs are in the correctness file.

## Complexity

A manifold triangle mesh with $n$ vertices has at most $3n$ edges, so $\sum_i d_i \le 6n$. Line L1 builds the neighbour lists in $O(n)$ time from the faces. Each step does $d_i$ additions and one division per free vertex, $\Theta(n)$ in total on the [real RAM](/real-ram/), so $K$ steps take $\Theta(Kn)$ time. The extra space is the array $y$ and the lists, $\Theta(n)$. With exact `Fraction` coordinates the numbers grow in size with $K$, and the time per step grows too, which is why exact runs are only for tests.

The number of steps for a given effect depends on the mesh. A feature that spans $m$ edges needs about $m^2$ steps to be smoothed away, as for any diffusion, which is why large features take many steps and why [implicit fairing](/implicit-fairing/) uses one large stable step instead.

## Properties

- **A low-pass filter.** For a closed mesh, write $x$ in the eigenvectors of $G = I - D^{-1}A$, with eigenvalues $0 = k_1 < k_2 \le \cdots \le k_n \le 2$, which play the role of frequencies. One step multiplies the part of frequency $k$ by $1 - \lambda k$. High frequencies, the noise, are damped most, but every frequency except $k = 0$ is damped a little. This is Taubin's view, and the cause of the shrinkage.
- **Stable only for small steps.** The factor $1 - \lambda k$ lies in $(-1, 1]$ for all $k \le 2$ exactly when $0 < \lambda < 1$. With $\lambda > 1$, frequencies near $k = 2$ flip sign and grow.
- **Depends on the connectivity.** The uniform weights ignore edge lengths and angles. On a flat but irregular mesh, $c_i \ne x_i$, so vertices slide inside the plane: at the origin with the neighbours $(1, 0)$, $(1, 1)$, $(0, 1)$, $(-1, 0)$, $(0, -1)$, one step with $\lambda = \frac{1}{2}$ moves the vertex to $(\frac{1}{10}, \frac{1}{10})$. This tangential motion makes the triangles more regular, which is useful in [remeshing](/isotropic-remeshing/), but it also distorts textures and parameterizations.
- **Exact.** With rational input and rational $\lambda$, all values are exact.

## Variants and improvements

- **Cotangent weights.** Replace the average by $\sum_j w_{ij} x_j / \sum_j w_{ij}$ with the [cotangent weights](/cotangent-laplacian/). The step then follows the mean curvature normal, has no tangential drift on flat regions, and needs the weights to be recomputed after each step. Weights can be negative on obtuse triangles.
- **Taubin smoothing.** Alternate a step with $\lambda > 0$ and a step with a negative factor $\mu < -\lambda$, so that low frequencies keep their size. See [Taubin smoothing](/taubin-smoothing/).
- **Implicit steps.** Solve $(I - \lambda L) x' = x$ instead, which is stable for any $\lambda$. See [implicit fairing](/implicit-fairing/).
- **Volume correction.** Scale the mesh after each step so that its volume stays the same. This stops the collapse, but does not stop the change of shape that shrinkage causes.
- **Gauss-Seidel order.** Update $x_i$ in place, so that later vertices see the new positions. This converges faster but depends on the order of the vertices and is not symmetric.
- **Tangential smoothing.** Keep only the part of $U(x)_i$ in the tangent plane of the vertex. The shape stays, and the vertices spread more evenly, which is the relaxation step of [isotropic remeshing](/isotropic-remeshing/).
- **Feature-aware weights.** Lower the weight of an edge across a sharp crease, so that the crease is not rounded.

## When to use it

Use it for a quick cleanup of small noise, for the relaxation of vertex positions inside a remesher, for fairing a small patch inside a fixed border, as after [Liepa hole filling](/liepa-hole-filling/), and as a baseline. Do not use it for many steps on a closed shape, because the shape shrinks and loses its features. For that, use [Taubin smoothing](/taubin-smoothing/) or [implicit fairing](/implicit-fairing/). For images, the same idea is [image smoothing](/image-smoothing/) with a box or Gaussian kernel.

## Pitfalls

- **Shrinkage.** A closed mesh shrinks after every step, even without noise, and converges to a point. Count steps, and correct the volume or use a non-shrinking method.
- **A free border.** If the border vertices are not fixed, they move to the average of their neighbours, which lie on one side, and the border pulls inward.
- **In-place updates by mistake.** Writing $y_i$ into $x$ during the loop gives a Gauss-Seidel sweep whose result depends on the vertex order.
- **Too large a factor.** $\lambda \ge 1$ makes the highest frequencies grow or oscillate.
- **Non-manifold input.** A vertex where two fans meet averages over both, and can be pulled between two separate sheets.
- **Sliding in flat regions.** On an irregular mesh, vertices move inside the surface. If the texture coordinates or the triangle shapes must stay, use cotangent weights.

## Implementations

## History

Moving each node of a finite element mesh to the centroid of its neighbours was in use in mesh generation before 1988, and Field's paper of that year, which studies how it changes the angles of a Delaunay triangulation in the plane, is the usual reference. In 1995 Taubin applied the same step to the vertices of a surface mesh, showed that it is a filter on the eigenvectors of the Laplacian with transfer function $1 - \lambda k$, explained the shrinkage, and fixed it with a second step of negative factor. In 1999 Desbrun, Meyer, Schröder and Barr replaced the uniform weights by cotangent weights and the explicit step by an implicit one, the basis of most later smoothing methods.

## References
