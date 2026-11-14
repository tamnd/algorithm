---
tag: 44KQTR
kind: algorithm
slug: laplacian-surface-editing
name: Laplacian surface editing
aliases:
- differential coordinates editing
area: cad/mesh-processing
level: advanced
summary: Sorkine and coauthors' editing that keeps the Laplacian coordinates of a mesh in least squares while handle vertices are moved, preserving local detail.
model: real-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2004
  people: [Olga Sorkine, Daniel Cohen-Or, Yaron Lipman, Marc Alexa, Christian Rössl, Hans-Peter Seidel]
  note: They encoded a surface by the Laplacian coordinates of its vertices and edited it by one sparse least squares solve, with a linearized similarity at each vertex so that the detail can turn and scale.
prereqs: [laplacian-matrix, normal-equations, polygon-mesh]
see_also: [as-rigid-as-possible-deformation, cotangent-laplacian, poisson-image-editing, laplacian-smoothing, implicit-fairing, manifold-harmonics, cholesky-decomposition, qr-decomposition]
sources:
  - paper: doi:10.1145/1057432.1057456
    title: Olga Sorkine, Daniel Cohen-Or, Yaron Lipman, Marc Alexa, Christian Rössl and Hans-Peter Seidel, Laplacian surface editing, Proceedings of the Eurographics/ACM SIGGRAPH Symposium on Geometry Processing, 2004, 175 to 184
    locator: the Laplacian coordinates with uniform weights, the least squares energy with soft handle constraints, and the implicit transformation of each vertex as a linearized similarity fit to its ring
  - paper: doi:10.1109/smi.2004.1314505
    title: Yaron Lipman, Olga Sorkine, Daniel Cohen-Or, David Levin, Christian Rössl and Hans-Peter Seidel, Differential coordinates for interactive mesh editing, Proceedings of Shape Modeling International, 2004, 181 to 190
    locator: editing with differential coordinates and the estimate of local rotations from the edited surface
  - paper: doi:10.1109/TVCG.2007.1054
    title: Mario Botsch and Olga Sorkine, On linear variational surface deformation methods, IEEE Transactions on Visualization and Computer Graphics 14(1), 2008, 213 to 230
    locator: the comparison of the linear deformation methods, and their trouble with large rotations
---

Laplacian surface editing changes the shape of a triangle mesh by moving a few handle vertices, and it keeps the small detail of the surface. It does not store the positions of the vertices but their Laplacian coordinates: for each vertex, the difference between the vertex and the mean of its neighbours. This vector is near the normal and its length follows the local curvature, so it encodes the detail. Olga Sorkine and coauthors (2004) moved the handles and then found the positions whose Laplacian coordinates are as close as possible, in least squares, to the old ones. That is one sparse linear solve. Because the Laplacian coordinates do not turn with the surface, they also fitted to each vertex a linearized similarity, a scale and a small rotation that depend linearly on the new positions, and turned each Laplacian coordinate by it. The energy stays a quadratic, and the solve stays linear. With the handles left at their rest positions the solve returns the input mesh.

## In plain words

Describe each corner of a mesh not by where it is, but by how it sits relative to its neighbours: a little above them, a little to the side. These small offsets hold the bumps and wrinkles of the surface.

Now pull a few corners to new places. Find new places for all the other corners so that each corner sits relative to its neighbours almost as it did before, and so that the pulled corners land near where they were pulled. This is one large least squares problem, and one solve answers it.

The offsets are fixed arrows, so if part of the surface turns, the old arrows point the wrong way. The method therefore lets each corner also turn and scale its own arrow a little, by the amount its neighbours suggest. This works well for small turns.

## The problem

The input is a connected triangle mesh with rest positions $p_1, \ldots, p_n$, a nonempty set $H$ of handle vertices with targets $h_k$, and a weight $\lambda > 0$. With $N(i)$ the $d_i$ neighbours of vertex $i$, the uniform Laplacian is $L(q)_i = q_i - \frac{1}{d_i}\sum_{j \in N(i)} q_j$, and the Laplacian coordinates are $\delta_i = L(p)_i$. The output is the positions $q$ that minimize

$$E(q) = \sum_{i=1}^{n}\bigl|L(q)_i - T_i(q)\,\delta_i\bigr|^2 + \lambda^2\sum_{k \in H}|q_k - h_k|^2.$$

In the plain form $T_i(q) = I$. With rotations, $T_i(q) = s_i I + [h_i]_\times$, where $h \times x = [h]_\times x$, and $(s_i, h_i, t_i)$ is the least squares fit of $s\,p_j + h \times p_j + t \approx q_j$ over the ring $\{i\} \cup N(i)$. The handles are soft constraints: a larger $\lambda$ pulls them closer to their targets.

## The algorithm

```pseudo id=main
LAPLACIAN-EDIT(rest positions p, handles H with targets h, weight λ, rotations)
L1  δ_i ← p_i − (1/d_i) Σ_j p_j for each vertex i
L2  if rotations: for each vertex i, write (s_i, h_i) of the fit of its rest ring as a linear function of q
L3  a row L(q)_i − T_i(q) δ_i for each vertex i, with T_i = I without rotations
L4  a row λ (q_k − h_k) for each handle k
L5  N ← Mᵀ M and b ← Mᵀ r, for the rows M x − r of lines L3 and L4
L6  solve N x = b by Cholesky
L7  return the positions q in x
```

Line L1 computes the Laplacian coordinates. In the plain form, lines L3 to L6 separate into three problems, one for each coordinate, with the same matrix $N = L^{\mathsf T}L + \lambda^2\sum_{k \in H} e_k e_k^{\mathsf T}$. With rotations, line L2 solves, for each vertex, the $7 \times 7$ normal equations of the fit of its rest ring. Their solution is $G^{-1}A^{\mathsf T}b$, where $b$ holds the new positions of the ring, so $s_i$ and $h_i$ are fixed linear combinations of the unknowns. Then $T_i(q)\delta_i = s_i\delta_i + h_i \times \delta_i$ is linear in $q$ too, line L3 couples the three coordinates, and the system has $3n$ unknowns. The translation $t_i$ of the fit is not applied, because $\delta_i$ is a difference of points. The matrix depends only on the rest mesh and on which vertices are handles, so an interactive editor factors it once and, as the user drags the handles, only changes $b$.

## Example

**The input comes back.** Take the grid of $5 \times 5$ points on the square $[-1, 1]^2$ with the bump $z = \frac12(1 - x^2)(1 - y^2)$, cut into 32 triangles, and three corners as handles at their rest positions. Solved exactly with rational numbers, the plain form returns the input exactly. The form with rotations does the same on the $4 \times 4$ grid of the bump. On that grid, moving the three handles by $(0.3, -0.2, 1)$ moves every vertex by the same vector, exactly, in both forms.

**Turning the border.** Take the $9 \times 9$ grid of the same bump, with 81 vertices and 128 triangles, and the 32 border vertices as handles with $\lambda = 1$. Turn the targets of the border by an angle $\theta$ about the $x$ axis. A perfect edit would turn the whole patch rigidly. The table gives the largest distance of an inner vertex from that rigid turn, and the height of the centre of the bump along the turned normal, which is $0.5$ at rest.

| $\theta$ | $0.1$ | $0.5$ | $1.0$ | $\pi/2$ |
|---|---|---|---|---|
| plain: error | $0.050$ | $0.247$ | $0.479$ | $0.707$ |
| plain: height | $0.498$ | $0.439$ | $0.270$ | $0.000$ |
| rotations: error | $0.0013$ | $0.031$ | $0.116$ | $0.252$ |
| rotations: height | $0.501$ | $0.527$ | $0.562$ | $0.500$ |

In the plain form the Laplacian coordinates keep pointing up, so the bump leans as the border turns, and at $\pi/2$ it is flat: its height along the new normal is 0. The linearized similarities fix most of this for small angles, but the error grows with the angle, because $sI + [h]_\times$ is a rotation only to first order. With $\lambda = 10$ the border vertices are at most $0.0021$ from their targets instead of $0.078$, and the inner errors do not change in the first three digits.

## Correctness

The proof file shows these facts.

- **The solve is the least squares minimum.** $E = |Mx - r|^2$ is a convex quadratic, its minima solve the normal equations of line L5, and the minimum is unique when the matrix is positive definite.
- **The plain matrix is positive definite.** On a connected mesh $L(u) = 0$ only for a constant $u$, because each value is then the mean of its neighbours and the largest value spreads. A handle makes that constant 0.
- **The unconstrained solve returns the input.** With the handles at their rest positions, $E(p) = 0$: the Laplacian coordinates of $p$ are $\delta$, and the fit of a rest ring to itself is $s = 1$, $h = 0$. By uniqueness the solve returns $p$, exactly in rational arithmetic.
- **No handle, no unique answer.** Without handles the plain minima are exactly $p$ plus a constant vector. With rotations, all linearized similarities of $p$ have energy 0, and three handles not on a line remove them.
- **A translation is kept.** If all handles move by the same vector, the whole mesh moves by it.

With rotations, that the matrix is positive definite once three handles are not on a line is not proved. The code reports a singular matrix, and the tests check the matrix on their meshes. How much detail survives large turns is measured, not proved.

## Complexity

Let $n$ be the number of vertices. The rows of lines L1 to L4 have $O(1)$ entries each on a mesh of bounded degree, with $O(n)$ rows in all, and each fit of line L2 is a $7 \times 7$ solve, so building $N$ costs $\Theta(n)$. The code stores $N$ as a dense matrix of size $n$ or $3n$, so the factorization costs $\Theta(n^3)$ and the extra space is $\Theta(n^2)$, on the [real RAM](/real-ram/). $N$ is sparse, and a sparse [Cholesky decomposition](/cholesky-decomposition/) with a fill-reducing order factors it much faster in practice. After the factorization, each new position of the handles costs one pair of triangular solves.

## Properties

- **One linear solve.** No iteration and no starting guess.
- **Exact.** On rational input the solve is exact, and the input comes back exactly.
- **Invariant under translation.** Moving all handles by a vector moves the result by it.
- **Not invariant under rotation.** The plain Laplacian coordinates do not turn. The linearized similarities turn them correctly only for small angles.
- **Soft handles.** The handles reach their targets only approximately, more closely as $\lambda$ grows.
- **One factorization.** The matrix depends on the rest mesh and on the set of handles, not on the targets.

## Variants and improvements

- **Cotangent weights.** The [cotangent Laplacian](/cotangent-laplacian/) makes the Laplacian coordinates depend on the shape and not on how the mesh is cut, at the cost of weights that can be negative on obtuse triangles.
- **Hard handles.** Remove the handle vertices from the unknowns and move their known values to the right side. The handles then hit their targets exactly.
- **Explicit rotations.** Estimate the rotation of each vertex from a first solve, turn the Laplacian coordinates by it, and solve again, as Lipman and coauthors did. [As-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) iterates this with exact rotations and handles large angles.
- **Gradient-domain editing.** Edit the gradients of the coordinate functions instead and solve a Poisson equation, as [Poisson image editing](/poisson-image-editing/) does for images.
- **Higher order.** Minimizing the bending, the squared Laplacian of the displacement, gives smooth deformations without detail, and detail can then be added back on top.

## When to use it

Use Laplacian surface editing for interactive edits of a detailed mesh with handles where the parts move or turn by small amounts, and for transferring detail from one surface to another, because the whole edit is one precomputed linear solve. For large rotations, such as bending a limb, use [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/), which costs a few more solves for each frame. To smooth a mesh instead of keeping its detail, use [Laplacian smoothing](/laplacian-smoothing/) or [implicit fairing](/implicit-fairing/).

## Pitfalls

- **No handle.** The plain system is singular, because a translation does not change Laplacian coordinates. With rotations, use at least three handles that are not on a line.
- **Large rotations.** In the example, at a turn of $\pi/2$ the plain form flattens the bump completely, and the linearized form still leaves an error of $0.25$ on a patch of width 2.
- **Weak handles.** With soft constraints and a small $\lambda$, the handles do not reach their targets. Raise $\lambda$ or eliminate the handles from the unknowns.
- **Normal equations.** $M^{\mathsf T}M$ squares the condition number of $M$. For fine meshes or large $\lambda$, a [QR decomposition](/qr-decomposition/) of $M$ is more accurate.
- **Degenerate rings.** The fit of line L2 needs a ring that is not in a line. A vertex whose triangles are all degenerate breaks it.
- **Uniform weights on irregular meshes.** The uniform Laplacian coordinates have tangential parts on an irregular mesh, so the result depends on how the mesh is cut into triangles.

## Implementations

## History

Differential coordinates for meshes go back to Taubin's work on mesh smoothing in the 1990s, where the Laplacian of the positions acted as a filter. In 2004 Lipman, Sorkine, Cohen-Or, Levin, Rössl and Seidel edited meshes through these coordinates and estimated local rotations from the result, and in the same year Sorkine, Cohen-Or, Lipman, Alexa, Rössl and Seidel gave Laplacian surface editing, with the linearized similarity at each vertex built into one least squares solve. Botsch and Sorkine compared the linear deformation methods in 2008 and showed that none of them handles large rotations well, which led to nonlinear methods such as as-rigid-as-possible deformation.

## References
