---
tag: 7SBDXS
kind: algorithm
slug: arap-parameterization
name: As-rigid-as-possible parameterization
aliases:
- ARAP parameterization
- local-global parameterization
area: cad/mesh-processing
level: advanced
summary: Liu and coauthors' flattening that alternates fitting a rotation to each triangle and a global Poisson solve, which gives low stretch with a free boundary.
solves: [mesh-parameterization]
model: real-ram
complexity:
  vars: {n: the number of vertices, k: the number of iterations}
  time: {worst: O(n^3 + k n^2), nested_dissection: O(n^(3/2) + k n log n)}
  space: {extra: O(n^2), nested_dissection: O(n log n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Ligang Liu, Lei Zhang, Yin Xu, Craig Gotsman, Steven J. Gortler]
  note: Liu and coauthors gave the local and global steps for parameterization at the Symposium on Geometry Processing 2008, one year after Sorkine and Alexa used the same scheme to deform surfaces.
prereqs: [mesh-parameterization, cotangent-laplacian, least-squares-problem, singular-value-decomposition]
see_also: [least-squares-conformal-maps, tutte-embedding, angle-based-flattening, boundary-first-flattening, as-rigid-as-possible-deformation, kabsch-algorithm, cholesky-decomposition, texture-mapping]
sources:
  - paper: doi:10.1111/j.1467-8659.2008.01290.x
    title: Ligang Liu, Lei Zhang, Yin Xu, Craig Gotsman and Steven J. Gortler, A local/global approach to mesh parameterization, Computer Graphics Forum 27(5), 2008, 1495 to 1504
    locator: the energy with one linear map per triangle, the local step by a 2 x 2 SVD, the global step with the cotangent Laplacian, and the ARAP, ASAP and hybrid models
  - paper: doi:10.2312/SGP/SGP07/109-116
    title: Olga Sorkine and Marc Alexa, As-rigid-as-possible surface modeling, Symposium on Geometry Processing 2007, 109 to 116
    locator: the alternation of a rotation fit by SVD and a Poisson solve with a fixed matrix, and the proof that the energy does not increase
  - book: isbn:9781568814261
    title: Mario Botsch, Leif Kobbelt, Mark Pauly, Pierre Alliez and Bruno Lévy, Polygon Mesh Processing, AK Peters, 2010
    locator: Chapter 5, Parametrization (distortion of a map and the most isometric parametrizations)
---

As-rigid-as-possible parameterization, ARAP, flattens a triangle mesh with the topology of a disk into the plane so that each triangle keeps its shape and its size as well as possible. For each triangle it measures how far the linear map of that triangle is from a rotation, and it minimizes the sum of these errors, weighted by the area. It alternates two exact steps: a *local step* that fits the best rotation to each triangle, and a *global step* that solves one linear system for all the vertices with the rotations fixed. Each step can only lower the energy, and the matrix of the global step never changes, so it is factored once. It solves the [mesh parameterization](/mesh-parameterization/) problem with much less area distortion than a conformal map, and the boundary is free.

## In plain words

Cut the surface into its triangles and lay each one flat on the table. Each flat triangle has the right shape and size, but they no longer fit together. Now push and pull the corners so that the triangles join again, while each one stays as close as possible to its own flat copy.

After the push, the triangles have turned a little. So look again at each triangle and find how its flat copy must turn to match it best. Then push and pull the corners again toward the turned copies. Repeat these two steps.

Each round can only make the total error smaller, never larger. On a gently curved patch the result is a flat map in which most triangles are close to their true size, and the edge of the map takes whatever shape fits best.

## The problem

The input is a triangle mesh $M$ with $n$ vertices whose triangles all have positive area, whose dual graph (triangles, joined when they share an edge) is connected, and whose faces are oriented so that the outward normal follows the right-hand rule. The input also has a start map: a point $u_v \in \mathbb{R}^2$ for each vertex. The output is a new map $u$ of lower distortion. Each triangle $t$ has a *frame*: a counterclockwise triangle in the plane congruent to $t$, with area $A_t$. The map $u$ sends the frame of $t$ to the image triangle by a linear map plus a translation, and $J_t(u)$ is the $2 \times 2$ Jacobian of that linear map. The *ARAP energy* is

$$E(u, R) = \sum_t A_t \lVert J_t(u) - R_t \rVert_F^2, \qquad \hat E(u) = \min_{R} E(u, R),$$

where each $R_t$ is a rotation of the plane and $\lVert \cdot \rVert_F$ is the Frobenius norm. $\hat E(u) = 0$ exactly when each triangle is mapped by a rotation and a translation, that is, when the map keeps all lengths. The goal is a map with small $\hat E$. The energy is not convex, and the algorithm finds a local minimum, not the global one.

## The algorithm

The energy of one triangle has a second form, with the edges. Write $e_{ij} = q_i - q_j$ for the edge from corner $j$ to corner $i$ of the frame, and $\theta_{ij}$ for the angle of the frame opposite that edge. Then

$$A_t \lVert J_t - R_t \rVert_F^2 = \frac12 \sum_{(i,j) \in t} \cot \theta_{ij}\, \big\lVert (u_i - u_j) - R_t e_{ij} \big\rVert^2,$$

see the proof. So for fixed rotations, $E$ is a quadratic function of $u$, and its normal equations have the [cotangent Laplacian](/cotangent-laplacian/) $L$ of the mesh as their matrix: $L u = b(R)$, one system for the $x$ coordinates and one for the $y$ coordinates. $E$ does not change when $u$ moves by a translation, so one vertex $p$ is pinned.

```pseudo id=main
ARAP-PARAMETERIZATION(M, u, iterations)
L1  for each triangle t do compute its frame, A_t and the cotangents of its angles
L2  L ← the cotangent Laplacian without the row and column of the pinned vertex p
L3  factor L once (Cholesky)
L4  repeat iterations times
L5      for each triangle t do                               ▷ local step
L6          J ← J_t(u);  R_t ← the rotation by the angle atan2(J₂₁ − J₁₂, J₁₁ + J₂₂)
L7      b ← Σ over the edges (i, j) of each t of ½ cot θ_ij · R_t e_ij, added to row i and subtracted from row j
L8      solve L u = b for x and for y, with u_p fixed            ▷ global step
L9  return u
```

Line L6 is the closest rotation to $J$ in the Frobenius norm. For $R$ the rotation by $\theta$, $\operatorname{tr}(R^\top J) = \cos\theta\,(J_{11} + J_{22}) + \sin\theta\,(J_{21} - J_{12})$, and $\lVert J - R \rVert_F^2 = \lVert J \rVert_F^2 + 2 - 2 \operatorname{tr}(R^\top J)$, so the best $\theta$ is the angle of the vector $(J_{11} + J_{22}, J_{21} - J_{12})$. This is the same rotation as the usual $U V^\top$ from the [singular value decomposition](/singular-value-decomposition/) $J = U \Sigma V^\top$, with the sign of the last column of $U$ changed when $\det(U V^\top) < 0$, as in the [Kabsch algorithm](/kabsch-algorithm/). If both entries of the vector are 0, every rotation is optimal, and the code takes the identity.

Line L7 builds the right side. For each edge, the target of $u_i - u_j$ is the turned frame edge $R_t e_{ij}$. Line L8 then gives the map in which all the image edges are as close to their targets as possible, in the weighted least squares sense. The pinned vertex moves its terms to the right side.

**Start map.** The code of this page starts from a [Tutte embedding](/tutte-embedding/) with uniform weights and the boundary on a circle, which has no flipped triangle. A map from [least squares conformal maps](/least-squares-conformal-maps/) is also a common start.

**Degenerate cases.** A triangle with zero area has no frame and is rejected. An obtuse angle gives a negative cotangent, which is correct and must be kept, see the pitfalls. A mesh whose dual graph is not connected needs one pinned vertex on each part, or $L$ is singular.

## Example

Take the pyramid of the LSCM page: base corners $x_0 = (-1, -1, 0)$, $x_1 = (1, -1, 0)$, $x_2 = (1, 1, 0)$, $x_3 = (-1, 1, 0)$, apex $x_4 = (0, 0, 1)$, and the four side triangles $(0, 1, 4)$, $(1, 2, 4)$, $(2, 3, 4)$, $(3, 0, 4)$. The base edges have length 2 and the side edges have length $\sqrt3 \approx 1.732$. The angles at the apex add up to $282.1°$, so no flat map keeps all lengths. Vertex 0 is pinned.

| step | value |
|---|---|
| L1 | each frame is $(0, 0), (2, 0), (1, \sqrt2)$ with $A_t = \sqrt2$; the cotangents are $0.7071$ at the base corners and $0.3536$ at the apex |
| start | Tutte: $u_0 = (1, 0)$, $u_1 = (0, 1)$, $u_2 = (-1, 0)$, $u_3 = (0, -1)$, $u_4 = (0, 0)$; $\hat E = 1.899495$ |
| L6, triangle $(0, 1, 4)$ | $J = \begin{pmatrix} -0.5 & -0.3536 \\ 0.5 & -0.3536 \end{pmatrix}$, the vector $(-0.8536, 0.8536)$, so $R_t$ turns by $135°$ |
| L6, the other three | $-135°$, $-45°$ and $45°$ |
| L8 | $u_4 = (-0.6095, 0)$, $u_1 = (-0.6095, 1.6095)$, $u_2 = (-2.2190, 0)$, $u_3 = (-0.6095, -1.6095)$; $\hat E = 0.323521$ |
| second round | no change: the map is a fixed point |

The result is a square of side $2.2761$ with the apex at its centre. Each base edge is $13.8\%$ too long and each side edge $1.6095$ is $7.1\%$ too short. A conformal map keeps the angles instead and lets the size change; on the LSCM page the same pyramid has an image with only $2/3$ of the surface area.

The pyramid is symmetric, so one round reaches the fixed point. Move the apex to $(0.5, 0.25, 1)$ and the energies after 0, 1, 2, 3 and 4 rounds are $2.088639$, $0.453943$, $0.427259$, $0.420178$ and $0.418315$. After 11 rounds the energy is $0.417651$ and does not change in the sixth digit. The energy never increases, as the proof says.

**Floating point and flips.** The frames need square roots, so the computation is in floating point. Whether a triangle of the result is flipped is the sign of ORIENT2D, the [orientation test](/orientation-test/), on the computed points. For tiny triangles a float evaluation of that sign is not reliable, because of [catastrophic cancellation](/catastrophic-cancellation/). The tests of this page convert the float coordinates to rationals and evaluate ORIENT2D exactly; [exact predicates](/shewchuk-expansion-sum/) do the same faster. This is the [robustness problem](/geometric-robustness-problem/) of geometry. On 8 random disks of 37 vertices and 54 triangles (a hexagonal grid with jitter, lifted to a random quadratic surface, seeds 0 to 7, 25 rounds), the tests found no flipped triangle. This is a measurement, not a theorem.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four facts.

1. The local step is exact: line L6 gives a rotation that minimizes $A_t \lVert J_t - R \rVert_F^2$ over all rotations $R$.
2. The global step is exact: with the rotations fixed, $E$ is a convex quadratic function of $u$ with the pinned value fixed, its matrix is the cotangent Laplacian without one row and column, and that matrix is positive definite. So line L8 gives the unique minimizer.
3. **Key invariant.** The energies never increase: $\hat E(u_{k+1}) \le E(u_{k+1}, R_{k+1}) \le E(u_k, R_{k+1}) = \hat E(u_k)$, where $R_{k+1}$ are the rotations of round $k + 1$.
4. The energies form a sequence that does not increase and is bounded below by 0, so they converge. A stop rule "stop when the decrease is below $\varepsilon$" stops after at most $\lceil \hat E(u_0) / \varepsilon \rceil + 1$ rounds.

The proof does not show that the maps $u_k$ converge to a global minimum, or that the result has no flipped triangle.

## Complexity

For $n$ vertices and $k$ rounds, the local step takes $O(n)$ time per round, with a constant amount of work per triangle. The matrix $L$ does not depend on the rotations, so it is factored once and each round needs only two triangular solves. With dense Cholesky, as in the code of this page, the factorization takes $O(n^3)$ time and $O(n^2)$ space, and each round $O(n^2)$ time. The sparsity graph of $L$ is the mesh graph, which is planar for a disk, so a sparse Cholesky factorization with [nested dissection](/nested-dissection/) takes $O(n^{3/2})$ time and $O(n \log n)$ space, and each round $O(n \log n)$ time. In practice a few tens of rounds are used; the number needed for a given accuracy is not bounded by the proof.

## Properties

- **Proved.** The local step is optimal for each triangle, the global step is optimal for the given rotations, the energy does not increase, and the energy values converge.
- **Proved.** If the mesh is planar, its own coordinates are a map with $\hat E = 0$, the global minimum, and a start at that map stays there.
- **Measured.** On 3 planar disks of 37 vertices (seeds 0 to 2), the code started from Tutte reaches $\hat E < 10^{-20}$ within 100 rounds, and all edge lengths agree with the input to $10^{-9}$. On 8 curved disks (seeds 0 to 7), no triangle flipped.
- **Not guaranteed.** The result can have flipped triangles or a boundary that overlaps itself, and it can stop in a local minimum.
- **Free boundary.** Only one vertex is pinned, and it only fixes the translation.
- **Invariant.** A rigid motion of the 3D mesh does not change the result, because the frames do not change.

## Variants and improvements

- **As-similar-as-possible (ASAP).** Liu and coauthors also replace the rotations by similarities, a rotation times a scale. Then the energy is quadratic in $u$ and in the similarities together, and its minimum is a conformal map like [LSCM](/least-squares-conformal-maps/).
- **Hybrid model.** The same paper mixes the two with a parameter that weights angle keeping against area keeping, with a local step that solves a cubic equation.
- **ARAP deformation.** [As-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) uses the same two steps in 3D, with $3 \times 3$ rotations from an SVD and handles moved by the user.
- **Other energies.** Later methods use the same scheme of local fits and one fixed sparse matrix for energies that go to infinity when a triangle collapses, such as the symmetric Dirichlet energy, and so keep every triangle unflipped. This is the usual fix when injectivity is required.
- **Boundary control.** [Boundary first flattening](/boundary-first-flattening/) fixes the boundary lengths or angles first and gives a conformal map with that boundary.

## When to use it

Use it for texture charts where the size of each triangle matters, for example to keep the texel density even, or to cut cloth or sheet material from a flat pattern. It needs a good start map and a mesh cut into a disk, and the rounds cost more than one linear solve of LSCM. Check every triangle of the result with an exact orientation test. If a flip-free result is required, use a method with a barrier against flips, or a [Tutte embedding](/tutte-embedding/) with its fixed boundary. If only angles matter, a conformal map is cheaper.

## Pitfalls

- **Clamping the cotangents.** A common change sets negative cotangents to 0 at line L2 to make the matrix an M-matrix. That changes the energy: the edge form above is only equal to $A_t \lVert J_t - R_t \rVert_F^2$ with the true signed cotangents. With clamped weights the global step no longer minimizes $E$, and the proof that the energy does not increase fails.
- **A reflection instead of a rotation.** Taking $R_t = U V^\top$ from the SVD at line L6 without the sign fix gives a reflection when $\det J < 0$. The energy then rewards a flipped triangle, and flips stay in the map.
- **No pinned vertex.** Without the pin at line L2, $L$ is singular, because a translation of $u$ does not change the energy. A dense or Cholesky solver then fails, and an iterative solver can drift.
- **Rebuilding the matrix each round.** $L$ depends only on the 3D mesh. Factoring it inside the loop, at line L8, makes each round cost a full factorization.
- **A start map with flips.** The local step only picks rotations, and nothing in the energy forbids a flipped triangle. A start with folds, for example a conformal map of a strongly curved chart, can keep them to the end.
- **Float signs.** Reading flips from a float evaluation of ORIENT2D can report a tiny triangle with the wrong orientation. Use exact predicates.

## Implementations

## History

Olga Sorkine and Marc Alexa presented the alternation of rotation fits and one fixed sparse solve for surface deformation at the Symposium on Geometry Processing 2007. Ligang Liu, Lei Zhang, Yin Xu, Craig Gotsman and Steven J. Gortler applied the same idea to parameterization at the 2008 symposium, with $2 \times 2$ rotations, similarities, and a mixed model, and showed that the result is close to isometric on surfaces that are close to developable. The local and global scheme became a standard tool, and many later methods for low distortion and locally injective maps use it with other energies.

## References
