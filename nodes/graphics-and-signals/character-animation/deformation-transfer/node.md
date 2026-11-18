---
tag: CM6PX4
kind: algorithm
slug: deformation-transfer
name: Deformation transfer
aliases:
- Sumner-Popovic deformation transfer
area: graphics-and-signals/character-animation
level: advanced
summary: Copy the deformation of a source mesh onto a different target mesh by transferring per-triangle deformation gradients and solving a least-squares system.
solves: [shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of target vertices", t: "the number of target triangles", p: "the number of triangle pairs in the correspondence"}
  time: {setup: "O(p + (n + t)^3)", frame: "O(p + (n + t)^2)"}
  space: {extra: "O((n + t)^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [least-squares-problem]
see_also: [blendshape-model, example-based-facial-rigging, laplacian-surface-editing, as-rigid-as-possible-deformation, motion-retargeting, cotangent-laplacian, cholesky-decomposition, poisson-equation]
sources:
  - paper: doi:10.1145/1015706.1015736
    title: "Robert W. Sumner and Jovan Popovic, Deformation transfer for triangle meshes, ACM Transactions on Graphics 23(3), SIGGRAPH 2004, 399-405"
    locator: "section 3, equation (1), for the fourth vertex and the per-triangle transformations; section 4 for the formulation in the vertex positions, the factorization that depends only on the target, and the solution up to a translation"
---

Deformation transfer copies a deformation from one mesh to another.
The input is a source mesh in its rest shape, the same source mesh deformed, for example into a smile or a bent knee, and a different target mesh in its rest shape.
The output is the target deformed in the same way.
Sumner and Popović (2004) gave the method.
It describes the change of each source triangle by a 3 by 3 matrix, the [deformation gradient](/deformation-gradient/) of that triangle, and then finds the target vertices whose triangles change by the same matrices, as closely as possible in the least squares sense.
Facial rigs use it to copy the targets of a generic [blendshape model](/blendshape-model/) onto a new face, and it is the first step of [example-based facial rigging](/example-based-facial-rigging/).

## In plain words

Take one small triangle of the source and look at how the deformation changed it: it may turn, stretch or shear.
Write that change as a matrix.
Do this for every triangle of the source.
Then go to the target and say which target triangles belong to which source triangles, for example the corner of the mouth to the corner of the mouth.
Now each target triangle should change by the matrix of its source triangle.
Each triangle alone could do that, but the triangles share vertices, so they cannot all do it exactly.
So we look for the vertex positions that make the changes of the target triangles as close as possible to the wanted matrices.
That is one linear least squares problem.
The target keeps its own shape and proportions, and only the change is copied.

## The problem

The source has rest vertices $v_i$ and deformed vertices $\tilde v_i$, on the same triangles.
The target has rest vertices $u_i$, $i = 1, \ldots, n$, and $t$ triangles.
A correspondence is a list of pairs $(T, S)$ of a target triangle $T$ and a source triangle $S$.
It can be many to many: a target triangle may appear in several pairs, and a source triangle too.
The output is the deformed target $\tilde u_1, \ldots, \tilde u_n$.

A triangle $(v_1, v_2, v_3)$ alone does not fix an affine map of space, because the direction normal to it is free.
The method adds a fourth vertex

$$v_4 = v_1 + \frac{(v_2 - v_1) \times (v_3 - v_1)}{\sqrt{\lVert (v_2 - v_1) \times (v_3 - v_1) \rVert}},$$

which is equation (1) of the paper.
The square root makes the length of $v_4 - v_1$ proportional to the size of the triangle, so the normal direction scales with the triangle.
The frame of the triangle is the matrix $V = [v_2 - v_1,\ v_3 - v_1,\ v_4 - v_1]$, with these three columns.
The deformation of a source triangle is $S = \tilde V V^{-1}$, the unique linear map that takes the rest frame to the deformed frame.

For the target, the deformed vertices and the deformed fourth vertices are the unknowns.
The deformed frame $\tilde U_T$ of a target triangle is linear in them, so the problem is

$$\min_{\tilde u,\ \tilde u_4} \sum_{(T, S)} \lVert \tilde U_T U_T^{-1} - S_S \rVert_F^2.$$

The energy does not change when all unknowns move by the same vector, so one vertex is fixed to remove the translation.

## The algorithm

```pseudo id=main
DEFORMATION-TRANSFER(source rest v, source deformed ṽ, target rest u, pairs, fixed vertex f at position x_f)
L1  for each source triangle S: S_S ← Ṽ_S V_S⁻¹                ▷ frames with the fourth vertex of equation (1)
L2  for each target triangle T: Q_T ← U_T⁻¹                      ▷ depends only on the target rest mesh
L3  for each pair (T, S) and each column k: add the row Σ_r Q_T[r][k] (x_r - x_a) = column k of S_S
L4  remove the unknown of vertex f, and move its terms with x_f to the right side
L5  solve AᵀA X = AᵀB                                            ▷ one matrix, three right sides for x, y and z
L6  read ũᵢ from X for every vertex, with ũ_f = x_f
L7  return ũ
```

In line L3, $a$ is the first vertex of $T$, and $x_r$ is the unknown of the second vertex, the third vertex or the fourth vertex, for $r = 0, 1, 2$.
The row is the same for the three coordinates, and the right side has one entry per coordinate, the column $k$ of $S_S$.
So the matrix $A$ has one row per pair and column, and one column per unknown point: the $n$ target vertices and the $t$ fourth vertices, less the fixed one.

Lines L2 to L5 build and solve the normal equations.
The matrix $A$ depends only on the target rest mesh and the correspondence, not on the source deformation.
The paper uses this: it factors $A^\top A$ once, and for each new source pose it only builds the right side and solves with the factors.
The code in `impl/python` uses the dense solver of the shared helper and factors again on each call, which is simple and fast enough for small meshes.

## Example

Take one source triangle $(0,0,0), (1,0,0), (0,1,0)$, deformed by a shear to $(0,0,0), (1,0,0), (0.5,1,0)$.
Its normal is $(0,0,1)$ with length 1, so $v_4 = (0,0,1)$, and $V$ is the identity.
The deformed frame has the columns $(1,0,0)$, $(0.5,1,0)$ and $(0,0,1)$, so

$$S = \begin{pmatrix} 1 & 0.5 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}.$$

The target is a longer triangle $(0,0,0), (2,0,0), (0,1,0)$.
Its cross product is $(0,0,2)$, so $v_4 = (0, 0, 2/\sqrt{2}) = (0, 0, 1.41421)$.
With one pair and the first vertex fixed at the origin, the energy is zero when $\tilde U = S U$.
The columns of $S U$ are $(2,0,0)$, $(0.5,1,0)$ and $(0,0,1.41421)$.
So the target becomes $(0,0,0), (2,0,0), (0.5,1,0)$, and the fourth vertex stays at $(0,0,1.41421)$.
The top vertex moved by the same shear as in the source, and the long side kept its length 2.
The tests check these numbers.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
They hold in exact arithmetic, for a connected target mesh without degenerate triangles, in which every target triangle is in at least one pair.
- **One solution.** With one vertex fixed, $A$ has full column rank, so $A^\top A$ is positive definite and line L5 has exactly one solution, the unique minimizer of the energy.
- **No deformation, no change.** If the source is not deformed, every $S_S$ is the identity, the target rest mesh has zero energy, and so it is the result.
- **A uniform similarity is exact.** If the source moves by $x \mapsto s R x + c$ with a rotation $R$ and $s > 0$, the fourth vertex moves by the same map, every $S_S = sR$, and the target moves by the same map. For a general affine map the fourth vertex does not follow the map, so the result is close to it but not exact.
- **Self transfer.** If the target is the source with the identity correspondence, the deformed source has zero energy, so the method gives it back.

The tests check all of these, and also that the solution has a zero gradient and beats random perturbations, and that a repeated correspondence gives the same result.

## Complexity

The costs are in the real RAM model.
Line L1 costs $O(1)$ per source triangle, and line L3 costs $O(1)$ per pair.
The system has $n + t - 1$ unknown points and $3p$ rows, each with at most four nonzero entries.
The dense solve of the code costs $O((n + t)^3)$.
With a sparse Cholesky or LU factorization, as in the paper, the cost of the factorization depends on the fill, and for meshes it is close to linear in practice.
For each new source pose, only the right side changes, so the cost per frame is the cost of lines L1 and L3 plus two triangular solves with the kept factors.

## Properties

- Linear: for a fixed target and correspondence, the result depends linearly on the source matrices $S_S$.
- Translation is lost: the energy sees only differences of vertices, so the position comes from the fixed vertex or another constraint.
- The target keeps its own proportions, because only the change of each triangle is copied, not its shape.
- The correspondence can be many to many and does not need the two meshes to have the same vertex count or connectivity.
- Each coordinate $x$, $y$ and $z$ is a separate solve with the same matrix.

## Variants and improvements

- **The correspondence step.** The paper also finds the triangle correspondence, from a few marker points given by the user, by deforming the source onto the target with an energy of smoothness, identity and closest points, and then pairing triangles whose centroids are close. The code in `impl/python` takes the correspondence as input.
- **Gradient domain editing.** The same idea, prescribing the per-triangle change and solving for vertices, is the base of [Poisson-type](/poisson-equation/) mesh editing and of [Laplacian surface editing](/laplacian-surface-editing/).
- **Rotations only.** A related family of energies fits only a rotation per element, as in [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/). That is a different method: it keeps the target rigid where it can, and does not copy stretch or shear.
- **Facial rigs.** Copying every target of a generic blendshape rig onto a new face gives a first rig for that face. [Example-based facial rigging](/example-based-facial-rigging/) starts from that rig and then corrects it with scans of the actor.
- **Motion.** Applying the method to every frame of an animation copies the animation, frame by frame. It copies shape changes, not the motion of a skeleton, which is the job of [motion retargeting](/motion-retargeting/).

## When to use it

Use deformation transfer when the source and the target are different meshes of a similar kind, such as two faces or two animals, and the deformation of the source is given as meshes.
It is the right tool for copying blendshape targets or simulated shape changes to a new character.
If the two meshes have the same connectivity, the correspondence is the identity and the method is a short linear solve.
If the deformation comes from a skeleton, it is often simpler to copy the skeleton motion and skin the target.

## Pitfalls

- **Degenerate triangles.** A triangle with zero area has no fourth vertex and no inverse frame. Remove such triangles first, or give them a small area.
- **Triangles without a pair.** A target triangle in no pair has no term in the energy, and if a vertex is only in such triangles, $A^\top A$ is singular. Give every triangle at least one pair.
- **No fixed vertex.** Without a fixed vertex or another constraint, $A^\top A$ is singular, because a translation of all unknowns costs nothing.
- **A poor correspondence.** Pairs between triangles of different regions copy the wrong change. Check the correspondence by eye on a few strong deformations.
- **Large rotations of the target.** The source matrices are given in the frame of the source. If the target is posed in a different orientation, align the two meshes first, or the copied changes turn the target the wrong way.

## Implementations

## History

Sumner and Popović presented deformation transfer at SIGGRAPH 2004.
They introduced the fourth vertex of equation (1) to make the change of a triangle an affine map of space, the many to many correspondence of triangles, and the formulation in the vertex positions with a factorization that depends only on the target.
The method came out of the same period as the gradient domain and Laplacian methods of mesh editing, which also prescribe local changes and solve a sparse linear system for the vertices.

## References
