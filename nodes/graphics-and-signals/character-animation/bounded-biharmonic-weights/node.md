---
tag: W8RNMB
kind: algorithm
slug: bounded-biharmonic-weights
name: Bounded biharmonic weights
aliases:
- BBW
area: graphics-and-signals/character-animation
level: advanced
summary: Compute smooth, local and positive skinning weights for points, bones and cages by minimizing the Laplacian energy under bound constraints.
solves: [character-skinning, shape-deformation]
model: real-ram
complexity:
  vars: {n: "the number of mesh vertices", m: "the number of handles", I: "the number of active set iterations per handle"}
  time: {total: "O(n^3 + m I n^3)"}
  space: {extra: "O(n^2 + m n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [cotangent-laplacian, quadratic-programming, linear-blend-skinning]
see_also: [automatic-rigging, harmonic-coordinates, generalized-barycentric-coordinates, kkt-conditions, finite-element-method, cage-based-deformation, skinning-decomposition, as-rigid-as-possible-deformation]
sources:
  - paper: doi:10.1145/2010324.1964973
    title: "Alec Jacobson, Ilya Baran, Jovan Popović and Olga Sorkine, Bounded biharmonic weights for real-time deformation, ACM Transactions on Graphics 30(4), SIGGRAPH 2011, article 78"
    locator: "the energy with the constraints (3) to (6), where (5) is the partition of unity; the discrete energy with L M^(-1) L in equation (8); and the faster variant that drops (5), solves each weight on its own and normalizes (Fig. 6)"
---

Bounded biharmonic weights (BBW) are skinning weights that an artist can use with any mix of handles: points, bones and cages.
For each handle, the weight is the function on the shape that is 1 at the handle, 0 at the other handles, stays between 0 and 1, and is as smooth as possible in the sense of the Laplacian energy $\int (\Delta w)^2$.
Jacobson, Baran, Popović and Sorkine (2011) showed that the bounds are the key: without them, the smoothest weights go negative or above 1, which moves parts of the shape in the wrong direction.
After discretization on a triangle or tetrahedral mesh, each weight is the solution of a convex quadratic program.
The weights then drive [linear blend skinning](/linear-blend-skinning/) in real time.

## In plain words

A skinning weight says how much a point of the shape follows a handle.
It should be 1 on the handle, fade smoothly, and be 0 on the other handles.
The smoothest such function has no corners and no sharp peaks, but it can overshoot: past a handle, it can keep going down below 0, and then the point moves against its handle.
BBW keeps the smoothest function, but forbids values below 0 or above 1.
The result is smooth where it is free, and exactly 0 in the regions that the handle should not touch.
Computing it means solving one small optimization problem per handle on a mesh of the shape.
The fast version solves the handles one at a time, then divides the weights at each point by their sum.

## The problem

The input is a mesh of the shape (triangles in 2D, tetrahedra in 3D) with vertices $v_i$, $i = 1, \ldots, n$, and $m$ handles.
The output is a weight $w_k(v_i)$ for each handle $k$ and vertex $i$.
In the continuous form, the weights minimize $\sum_k \frac12 \int_\Omega (\Delta w_k)^2 \, dV$ subject to:
- $w_k = \delta_{jk}$ on handle $j$, which is the interpolation of the handles;
- $w_k$ is linear on each face of a cage, if there are cages;
- $\sum_k w_k = 1$ everywhere, which is the partition of unity;
- $0 \le w_k \le 1$ everywhere, which are the bounds.

The discrete energy of one weight is $\frac12 w^\top Q w$ with $Q = L M^{-1} L$, where $L$ is the [cotangent Laplacian](/cotangent-laplacian/) of the mesh as a stiffness matrix and $M$ is the lumped mass matrix.
In the faster variant, the partition of unity is dropped, each handle is solved on its own, and the weights are divided by their sum at the end.
The code in `impl/python` implements the faster variant for point handles on a 2D triangle mesh.

## The algorithm

```pseudo id=main
BBW(mesh, handles)
L1  build the cotangent stiffness matrix L and the lumped mass matrix M
L2  Q ← L M⁻¹ L
L3  for each handle k:
L4      w_k ← argmin ½ wᵀ Q w  subject to  w = δ_jk at handle j for every j,  and 0 ≤ w ≤ 1
L5  for each vertex i: divide every w_k(v_i) by Σ_k w_k(v_i)
L6  return the weights
```

Line L4 is a convex [quadratic program](/quadratic-programming/) with bound constraints.
The paper solves it with a general solver (MOSEK).
The code uses a primal active set method: it keeps a working set of variables held at a bound, solves the equality problem in the other variables, steps to the first bound that blocks the step, and releases the bound with the most negative multiplier when the step is zero.
It stops when every multiplier is nonnegative, which is the [KKT condition](/kkt-conditions/) of the problem.

Line L5 enforces the partition of unity.
The division changes the weights a little, so the result is not exactly the solution of the full problem with the constraint $\sum_k w_k = 1$, but it keeps the bounds, the interpolation and the smoothness in practice.

## Example

Take a strip of width 4 and height 1, meshed as a grid with five vertices along the bottom at $x = 0, 1, 2, 3, 4$, five along the top, and two triangles per square.
Put handle 1 at the bottom vertex $x = 0$ and handle 2 at the bottom vertex $x = 2$.
The weights of handle 1 along the bottom row are:

| $x$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| unbounded biharmonic | 1 | 0.5914 | 0 | $-0.3326$ | $-0.4325$ |
| bounded biharmonic | 1 | 0.5428 | 0 | 0 | 0 |

Without the bounds, the smooth weight keeps its slope past handle 2 and reaches $-0.43$ at the end of the strip.
With that weight, the end of the strip moves away from handle 1 when handle 1 moves.
The bounded weight is exactly 0 past handle 2, so the end of the strip follows only handle 2.
With two handles, the two weights already sum to 1 at every vertex, so line L5 changes nothing here.
The tests check these numbers to four decimals.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **Each problem has one solution.** $Q$ is positive semidefinite, and its null space is the constant vectors. A weight that is fixed at a handle vertex rules out the constants, so $Q$ is positive definite on the free variables, and the problem is strictly convex.
- **The active set method returns it.** When the method stops, the point is feasible and satisfies the KKT conditions, which are sufficient for a convex problem. The energy never increases, and if no step has length zero, no working set repeats, so the method stops after a finite number of steps.
- **The weights interpolate the handles and are bounded.** These are constraints of line L4, and line L5 keeps them, because it divides by a positive sum.
- **The weights sum to 1.** This is the effect of line L5.

The paper reports that the weights are local, with small supports, in its experiments; this is not proved.

## Complexity

The costs are in the real RAM model.
The code builds $Q$ as a dense matrix in $O(n^3)$ and solves a dense system of size up to $n$ in each active set iteration, so the total is $O(n^3 + m I n^3)$.
$L$ and $M$ are sparse, and $Q$ is sparse with the pattern of the two-ring neighborhoods, so a sparse solver is much faster on real meshes.
The weights are computed once, before the animation; at run time, skinning costs $O(n m)$ per frame, or $O(n K)$ if only the $K$ largest weights of each vertex are kept.

## Properties

- Smooth: the weights are smooth where the bounds are not active, also at point handles.
- Bounded: $0 \le w_k \le 1$.
- Interpolating: each weight is 1 on its handle and 0 on the others.
- Shape aware: the weights follow the mesh, so they do not cross a gap of the shape.
- Local in practice: the bounds make a weight exactly 0 in the regions behind other handles.
- Precomputed: the cost is all before the animation.

## Variants and improvements

- **Full problem.** Solve all handles together with the partition of unity as a constraint. The problem is larger, but it gives the exact minimizer with $\sum_k w_k = 1$.
- **Harmonic weights.** Minimize $\int \lVert \nabla w \rVert^2$ instead. The maximum principle gives the bounds for free, but at a point handle the weight has a sharp peak, which is a reason to use the biharmonic energy. [Harmonic coordinates](/harmonic-coordinates/) use this energy for cages.
- **Heat weights.** [Automatic rigging](/automatic-rigging/) computes weights by heat diffusion on the surface, which is a single linear solve for all bones with nonnegative weights, but it works on the surface and needs a visibility test.
- **Other deformation models.** The same weights can blend affine transforms of the handles in other schemes, for example with [as-rigid-as-possible deformation](/as-rigid-as-possible-deformation/) on a reduced space.

## When to use it

Use bounded biharmonic weights when an artist wants to deform a shape with a few handles of mixed types and needs smooth weights that are positive and local.
It works for 2D images and drawings with a triangle mesh, and for 3D characters with a tetrahedral mesh of the volume.
If you only have bones and a closed surface, the heat weights of [automatic rigging](/automatic-rigging/) are faster to compute.
If you have examples of the deformed shape, fit the weights to them with [skinning decomposition](/skinning-decomposition/).

## Pitfalls

- **Forgetting the bounds.** The unbounded minimizer is a single linear solve, but it overshoots, as in the example. The bounds are the main idea of the method.
- **Normalizing is not free.** Line L5 changes the weights. If the sums are far from 1, the result can lose smoothness, and the full problem is the better choice.
- **The mesh.** The weights live on the mesh, so the mesh must cover the shape and its handles must be mesh vertices. In 3D, the method needs a volume mesh, not only the surface.
- **Obtuse triangles.** Cotangent weights can be negative on meshes with obtuse angles. $Q$ stays positive semidefinite, but the weights can lose quality. Use a mesh with good triangles.
- **Solver time.** A general QP solver on a large mesh takes seconds to minutes. The weights are a precomputation, so this is often acceptable, but it limits interactive editing of the handles.

## Implementations

## History

Linear blend skinning with painted weights was the standard for years, and automatic weights came from heat diffusion, as in [automatic rigging](/automatic-rigging/) (Baran and Popović 2007), or from [harmonic coordinates](/harmonic-coordinates/) for cages.
Jacobson, Baran, Popović and Sorkine (2011) wrote weights for any mix of handles as the minimizers of the Laplacian energy with bounds, which made the weights smooth at point handles and kept them positive.
Later work by the same group and others added faster solvers, weights with fewer overshoots of other kinds, and weights for other skinning models.

## References
