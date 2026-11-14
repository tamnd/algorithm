---
tag: QG8W8W
kind: algorithm
slug: as-rigid-as-possible-deformation
name: As-rigid-as-possible surface deformation
aliases:
- ARAP deformation
- ARAP surface modeling
area: cad/mesh-processing
level: advanced
summary: Sorkine and Alexa's deformation that alternates fitting a rotation to each vertex cell and solving a Laplacian system, so detail stays locally rigid.
model: real-ram
complexity:
  vars: {n: the number of vertices, s: the number of rounds}
  time: {worst: O(n^3 + s n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2007
  people: [Olga Sorkine, Marc Alexa]
  note: They gave each vertex cell its own rotation, wrote one energy for the whole surface, and minimized it by alternating a best fit of the rotations with one sparse linear solve whose matrix never changes.
prereqs: [laplacian-surface-editing, cotangent-laplacian, kabsch-algorithm]
see_also: [arap-parameterization, singular-value-decomposition, cholesky-decomposition, optimal-superposition, implicit-fairing, laplacian-smoothing, coordinate-descent, finite-element-method]
sources:
  - paper: doi:10.2312/SGP/SGP07/109-116
    title: Olga Sorkine and Marc Alexa, As-rigid-as-possible surface modeling, Proceedings of the Eurographics Symposium on Geometry Processing, 2007, 109 to 116
    locator: the energy of the vertex cells, the best rotation of a cell by a 3 by 3 singular value decomposition, the linear system with the averaged rotations, the cotangent weights, and the alternation of the two steps
  - paper: doi:10.1145/344779.344859
    title: Marc Alexa, Daniel Cohen-Or and David Levin, As-rigid-as-possible shape interpolation, Proceedings of SIGGRAPH 2000, 157 to 164
    locator: the name as-rigid-as-possible, and the interpolation of two shapes through the rotations of their simplices
  - paper: doi:10.1145/1073204.1073323
    title: Takeo Igarashi, Tomer Moscovich and John F. Hughes, As-rigid-as-possible shape manipulation, ACM Transactions on Graphics 24(3), 2005, 1134 to 1141
    locator: the interactive deformation of a 2D shape by handles, with an error that tries to keep each triangle rigid
---

As-rigid-as-possible (ARAP) surface deformation lets a user move a few handle vertices of a mesh and finds new positions for all the other vertices, so that the neighbourhood of each vertex, its cell, moves as nearly as possible by a rotation and a translation. Olga Sorkine and Marc Alexa introduced it in 2007. The cell of vertex $i$ is the set of its edges, and each cell gets its own rotation $R_i$. The energy measures how far the edges of each cell are from a rotated copy of their rest shape. The method alternates two steps. The local step keeps the positions and finds the best rotation of each cell with a $3 \times 3$ [singular value decomposition](/singular-value-decomposition/), as in the [Kabsch algorithm](/kabsch-algorithm/). The global step keeps the rotations and solves one linear system with the [cotangent Laplacian](/cotangent-laplacian/), whose matrix never changes, so it is factored once. Neither step increases the energy, and a rigid motion of the whole mesh has energy 0.

## In plain words

Think of a mesh as many small hinged stars, one star around each corner, made of the edges at that corner. You hold a few corners in your hands and pull them. Each star may turn and move, but it does not want to stretch or bend.

The method repeats two moves. First, keep every corner where it is, and for each star find the turn that matches its old shape best. Second, keep those turns, and move all the free corners at once so that every edge points as nearly as possible the way its turned star wants. This second move is one large but simple linear solve, and the solver is set up only once.

Each move makes the total mismatch smaller or keeps it the same. After some rounds, the parts bend, and small details on the surface turn with them instead of being sheared.

## The problem

The input is a mesh with rest positions $p_1, \ldots, p_n$, a weight $w_{ij} = w_{ji} \ge 0$ on each edge, and a nonempty set $H$ of handle vertices with targets $h_k$. Every connected component of the edges with positive weight holds a handle. With $N(i)$ the neighbours of vertex $i$ and $e_{ij} = p_i - p_j$, the output is the set of new positions $q$, with $q_k = h_k$ on the handles, of small energy

$$E(q, R) = \sum_{i=1}^{n}\sum_{j \in N(i)} w_{ij}\,\bigl|(q_i - q_j) - R_i e_{ij}\bigr|^2,$$

where each $R_i$ is a rotation, a matrix in $SO(3)$. The weights are usually the cotangent weights $w_{ij} = \tfrac12(\cot\alpha_{ij} + \cot\beta_{ij})$. The exact minimum of $E$ is not the target. The method returns positions from which no single step decreases $E$ much further.

## The algorithm

```pseudo id=main
ARAP(rest positions p, weights w, handles H with targets h, s)
L1  A ← the matrix on the free vertices with A_ii = Σ_j w_ij and A_ij = −w_ij;  factor A = L Lᵀ
L2  R_i ← I for each vertex i;  q ← the solution of lines L5 and L6 with these rotations
L3  repeat s times
L4      for each vertex i do S_i ← Σ_j w_ij e_ij (q_i − q_j)ᵀ = U Σ Vᵀ;  R_i ← V diag(1, 1, d) Uᵀ with d = det(V Uᵀ)
L5      for each free vertex i do b_i ← Σ_j (w_ij / 2)(R_i + R_j) e_ij + Σ over handle neighbours j of w_ij h_j
L6      q ← the solution of L Lᵀ q = b, one coordinate at a time;  q_k ← h_k for each k in H
L7  return q
```

Line L4 is the local step. For fixed positions the energy of cell $i$ is a constant minus $2\operatorname{tr}(R_i S_i)$, so the best rotation maximizes the trace, and the singular value decomposition gives it. The factor $d$ keeps the determinant at $+1$, so the cell is not mirrored. Lines L5 and L6 are the global step. For fixed rotations the energy is a quadratic function of the positions, and its minimum solves, at each free vertex,

$$\sum_{j \in N(i)} w_{ij}(q_i - q_j) = \sum_{j \in N(i)} \frac{w_{ij}}{2}(R_i + R_j)\, e_{ij}.$$

The left side is the Laplacian of $q$ and does not depend on the rotations. The right side is the Laplacian of $p$ with each edge turned by the average of the rotations at its two ends. The handle values move to the right side. So the matrix $A$ of line L1 depends only on the rest mesh and on which vertices are handles, and each global step costs only the two triangular solves of line L6. Line L2 is the first guess: with all rotations equal to $I$, line L6 is the simplest form of [Laplacian surface editing](/laplacian-surface-editing/), which keeps the differential coordinates as they are.

## Example

**Bending a bar.** The bar is the box $1 \times 1 \times 4$ with its axis on the $z$ axis from $z = -2$ to $z = 2$. Each square end is cut into a $2 \times 2$ grid of squares and each long side into a $2 \times 8$ grid, and each square into two triangles: 144 triangles and 74 vertices, with cotangent weights. The 9 vertices of the bottom end are handles that stay in place. The 9 vertices of the top end are handles that are turned by $90°$ about the $x$ axis and moved to the end of a quarter circle of length 4, of radius $\rho = 8/\pi \approx 2.546$, which bends the bar toward $-y$. The table gives the energy after the first solve of line L2 and then after each local step and each global step.

| step | L2 | local 1 | global 1 | local 2 | global 2 | local 3 | global 30 |
|---|---|---|---|---|---|---|---|
| energy | $26.40$ | $7.31$ | $3.89$ | $2.67$ | $2.11$ | $1.82$ | $1.161$ |

The first solve, with no rotations, puts the middle of the bar at $(0, -1.273, -0.727)$, the midpoint of the straight line between the centres of the two ends, so the bar is sheared and cuts the corner, and one edge changes its length by $90\%$. After 30 rounds the centre of the middle ring is at $(0, -0.755, -0.209)$, close to the midpoint $(0, -0.746, -0.199)$ of the quarter circle. The largest change in the length of an edge is $19.5\%$ and the mean is $6.9\%$. That is near $1/(2\rho) \approx 19.6\%$, the strain of the inner and outer sides of a bar of width 1 bent to the radius $\rho$. On a finer bar, with a $3 \times 3 \times 12$ grid and 164 vertices, the energy after 30 rounds is $0.947$ and the largest change in length is $19.2\%$, against $91.9\%$ for the first solve.

**A rigid motion.** Turn the bar by $0.8$ rad about the axis $(1, 2, 3)$ and move it by $(0.3, -1, 2)$. On these positions, the local step returns the same rotation in every cell and the energy is below $10^{-20}$, and the global step with that rotation returns the same positions. Starting from the rest shape, with both ends as handles at their moved positions, the energy after the first solve and after round $1$, $5$, $10$, $20$, $40$ and $60$ is $16.1$, $1.26$, $0.334$, $0.141$, $0.0256$, $8.2 \times 10^{-4}$ and $2.6 \times 10^{-5}$, and after 60 rounds no vertex is more than $0.0028$ from its place in the rigid motion. With only the bottom end as a handle, the energy after the same rounds is $4.59$, $0.807$, $0.420$, $0.297$, $0.191$, $0.0869$ and $0.0397$, and after 60 rounds a vertex is still $0.596$ away.

## Correctness

The proof file shows these facts.

- **The local step is optimal.** For fixed positions, the energy of cell $i$ is a constant minus $2\operatorname{tr}(R_i S_i)$, because a rotation keeps lengths. The rotation $V \operatorname{diag}(1, 1, d)\, U^{\mathsf T}$ maximizes the trace over all rotations, by the lemma behind the Kabsch algorithm.
- **The global step is a least squares solve.** Each edge appears twice in $E$, and the two terms add to $2|q_i - q_j - c_{ij}|^2$ plus a part that does not depend on $q$, where $c_{ij} = \tfrac12(R_i + R_j)e_{ij}$. With nonnegative weights and a handle in every component, the matrix $A$ is symmetric positive definite, so the system of line L6 has exactly one solution, and it is the minimum of $E$ over the positions.
- **The energy never increases.** Each local step and each global step replaces one group of variables by its best value with the other group fixed. So $E(q^{(0)}, I) \ge E(q^{(0)}, R^{(1)}) \ge E(q^{(1)}, R^{(1)}) \ge \cdots \ge 0$, and the algorithm stops after $s$ rounds.
- **A rigid motion has energy 0.** If $q_i = Q p_i + t$ for a rotation $Q$, then every term of $E$ is 0 with $R_i = Q$. When the edges of each cell with positive weight span a plane, $Q$ is the only best rotation of each cell, and the global step with $R_i = Q$ returns the rigid motion, so it is a fixed point.

The energies converge, because they decrease and are at least 0. That the positions converge, or that they reach the global minimum of $E$, is not proved. The energy is not convex, because the set of rotations is not convex.

## Complexity

Let $n$ be the number of vertices. A mesh has $\Theta(n)$ edges, so lines L4 and L5 cost $\Theta(n)$ for each round. Each $3 \times 3$ singular value decomposition costs a constant. The code stores $A$ as a dense matrix, so the factorization of line L1 costs $\Theta(n^3)$ once, and each solve of line L6 costs $\Theta(n^2)$. The time is $O(n^3 + s n^2)$ on the [real RAM](/real-ram/), and the extra space is $\Theta(n^2)$ for the factor. In practice $A$ is sparse and a sparse [Cholesky decomposition](/cholesky-decomposition/) with a fill-reducing order is used. Then the factor of a surface mesh has far fewer entries, and each round costs about as much as a few sweeps over the mesh. On the bar of the example, 30 rounds take $0.63$ s with 74 vertices and $2.0$ s with 164 vertices in plain Python with dense matrices.

## Properties

- **Monotone.** The energy never increases from one step to the next.
- **Rigid motions are kept.** A rigid motion of all the handles is a fixed point with energy 0.
- **Invariant under rigid motions.** Moving the rest mesh and the targets by the same rigid motion moves the result in the same way, because the energy compares each cell with a rotated copy of itself.
- **One factorization.** The matrix depends only on the rest mesh and the set of handles. Moving the handles changes only the right side.
- **Local optimum.** The result depends on the first guess and on the number of rounds.
- **Positions only.** The handles fix positions, not rotations, so a handle of one vertex does not tell its neighbourhood how to turn.

## Variants and improvements

- **Uniform weights.** All $w_{ij} = 1$ always gives a positive definite matrix, at the cost of a result that depends on how the mesh is cut into triangles.
- **Other cells.** A cell can also include the edges between the neighbours of a vertex, or be a triangle or a tetrahedron. On a mesh of tetrahedra the same two steps give a deformation of a solid.
- **Shape interpolation and 2D shapes.** Alexa, Cohen-Or and Levin blended the rotations of the simplices of two shapes to interpolate between them, and Igarashi, Moscovich and Hughes deformed 2D shapes with handles at interactive rates. These are the ancestors of the surface method.
- **Parameterization.** The same local and global steps flatten a surface into the plane with triangles that are as close to rigid copies as possible, as in [ARAP parameterization](/arap-parameterization/).
- **Smooth rotations.** A term that penalizes the difference of the rotations of neighbouring cells makes the result smoother when the handles are few.
- **Faster convergence.** Starting each frame of an interactive session from the result of the previous frame, solving on a coarse mesh first, or extrapolating from the last few rounds, cuts the number of rounds.

## When to use it

Use ARAP deformation for interactive editing of a detailed surface with handles, where parts must bend or twist by large angles and the details must turn with them. [Laplacian surface editing](/laplacian-surface-editing/) needs one linear solve and is good for small changes. In its simplest form its differential coordinates do not turn, so large rotations shear the details, as the first solve of the example shows, and its linearized rotations hold only for small angles. For a character with a skeleton, skinning by the bones is cheaper. For physical behaviour, such as volume, mass or a material law, use a [finite element method](/finite-element-method/).

## Pitfalls

- **Negative cotangent weights.** A triangle with an angle above $90°$ gives a negative weight opposite that angle. The matrix need not be positive definite and the global step need not be a minimum. The code refuses such weights and offers uniform weights. Clamping the weights to 0 or remeshing also works.
- **Slow convergence.** The energy decreases roughly linearly. In the example, with only one end held, 60 rounds still leave a vertex $0.6$ away from the rigid motion that the energy prefers. Use more handles, a good first guess, or acceleration.
- **A component without a handle.** Its positions are not fixed, the matrix is singular, and the factorization fails.
- **Mirrored cells.** Without the factor $d$ the local step can return a reflection, and the cell turns inside out.
- **Lost twists.** The targets are positions only. A twist of the top end by a full turn gives the same targets as no twist, so the method cannot tell the two apart. Add handles along the bar, or turn the targets in small steps from frame to frame.
- **Changing the handles.** Adding or removing a handle changes the matrix, so it must be factored again. Moving a handle only changes the right side.
- **Too few rounds.** After one round the result is far better than the first solve, but it is not near the minimum. Stop on the change of the energy, not on a fixed small count.

## Implementations

## History

In 2000 Alexa, Cohen-Or and Levin used the phrase as-rigid-as-possible for the interpolation between two shapes that turns their simplices instead of moving their vertices along straight lines. In 2004 Sorkine and coauthors edited surfaces through their Laplacian coordinates, which keeps local detail but does not turn it. In 2005 Igarashi, Moscovich and Hughes deformed 2D shapes with handles, keeping each triangle as rigid as possible. In 2007 Sorkine and Alexa gave each vertex cell of a surface its own rotation, wrote a single energy for the whole surface, and minimized it by the alternation of a local fit of the rotations and a global linear solve with a fixed matrix. The same local and global steps were later used for parameterization, for meshes of tetrahedra, and for the simulation of elastic objects.

## References
