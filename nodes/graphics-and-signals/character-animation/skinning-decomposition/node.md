---
tag: H700TR
kind: algorithm
slug: skinning-decomposition
name: Smooth skinning decomposition with rigid bones
aliases:
- SSDR
area: graphics-and-signals/character-animation
level: research
summary: Fit bone transforms and sparse convex skinning weights to a sequence of example meshes by alternating least squares, to compress mesh animation.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", F: "the number of frames", B: "the number of bones", K: "the largest number of bones per vertex"}
  time: {iteration: "O(n 2^B (B^3 + B^2 F) + B F n K)"}
  space: {extra: "O(n B + B F)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [linear-blend-skinning, kabsch-algorithm, k-means]
see_also: [pose-space-deformation, automatic-rigging, bounded-biharmonic-weights, singular-value-decomposition, least-squares-problem, delta-mush, dual-quaternion-skinning, principal-component-analysis]
sources:
  - paper: doi:10.1145/2366145.2366218
    title: "Binh Huy Le and Zhigang Deng, Smooth skinning decomposition with rigid bones, ACM Transactions on Graphics 31(6), SIGGRAPH Asia 2012, article 199"
    locator: the formulation of the fit as linear blend skinning with rigid bones and nonnegative, affine and sparse weights, the k-means initialization, the weight update and the bone update by weighted Procrustes (general locator)
---

Smooth skinning decomposition with rigid bones (SSDR) takes an animation given as a sequence of meshes and finds a skeleton-free [linear blend skinning](/linear-blend-skinning/) model that reproduces it.
The output is a set of bones, one rigid transform per bone and frame, and skinning weights per vertex.
The weights are nonnegative, sum to 1 and have only a few nonzero entries per vertex, so the model plays in any engine that supports linear blend skinning.
Le and Deng (2012) fit the model by alternating least squares: fix the bones and solve for the weights, then fix the weights and solve for each bone.
Uses are the compression of mesh animations, such as a cloth or a muscle simulation, and the conversion of such data to a rig that a game engine can play.

## In plain words

You have a simulation that moves thousands of vertices in each frame, and you want to replay it cheaply.
Linear blend skinning moves each vertex as a weighted average of a few rigid motions.
If you can find a few rigid motions and a few weights per vertex that explain the data well, you store much less: one transform per bone and frame, and a few weights per vertex.
SSDR finds them.
It starts by grouping the vertices that move together, with [k-means](/k-means/), and fits one rigid motion to each group.
Then it repeats two steps.
With the motions fixed, each vertex gets the best few weights.
With the weights fixed, each bone gets the best rigid motion in each frame, which is a classic problem with a closed form solution.
Each step can only lower the error.

## The problem

The input is a rest mesh with vertices $v_i$, $i = 1, \ldots, n$, and $F$ example meshes with the vertices $q_{f,i}$.
The unknowns are the rigid transforms $(R_{f,b}, T_{f,b})$ for the bones $b = 1, \ldots, B$ and the frames $f$, and the weights $w_{i,b}$.
The problem is

$$\min \; E = \sum_{f} \sum_{i} \Big\lVert q_{f,i} - \sum_{b} w_{i,b} (R_{f,b} v_i + T_{f,b}) \Big\rVert^2$$

subject to $w_{i,b} \ge 0$, $\sum_b w_{i,b} = 1$, at most $K$ nonzero $w_{i,b}$ per vertex, and $R_{f,b}$ a rotation.
The number of bones $B$ and the sparsity $K$ are inputs.
The problem is not convex, and the sparsity constraint is combinatorial, so the method finds a local minimum.

## The algorithm

```pseudo id=main
SSDR(rest v, frames q, bones B, sparsity K)
L1  cluster the vertex trajectories with k-means into B groups; fit one rigid transform per group and frame; give each vertex weight 1 for its group
L2  repeat
L3      for each vertex i: w_i ← the least squares weights over the simplex, using all bones
L4          keep the K largest entries of w_i and solve again on them only
L5          if the old weights of i give a smaller error, keep the old weights
L6      for each bone b and frame f: r_(f,i) ← q_(f,i) minus the part of the other bones, for every vertex i
L7          (R_(f,b), T_(f,b)) ← the weighted Procrustes fit of w_(i,b) v_i to r_(f,i)
L8  until the error decreases by less than a tolerance
L9  return the weights and the transforms
```

Line L3 is a small least squares problem per vertex: stack the positions $R_{f,b} v_i + T_{f,b}$ of vertex $i$ over all frames as one column per bone, and find the convex combination of the columns closest to the stacked targets.
The paper solves it with an active set method for least squares with nonnegative weights that sum to 1.
The code in `impl/python` is for a few bones, so it tries every support: on each support it solves the equality-constrained system of the KKT conditions and keeps the solution if it is nonnegative.
This gives the exact minimizer over the simplex.

Line L4 makes the weights sparse.
Line L5 is a safeguard that this code adds, not a step of the paper: the sparse solution is the best on its support but can be worse than the old weights, and the safeguard keeps the error monotone.

Lines L6 and L7 update one bone with all other bones and all weights fixed.
With $\tilde v_i = w_{i,b} v_i$, the problem is $\min \sum_i \lVert r_{f,i} - w_{i,b} T - R \tilde v_i \rVert^2$, a [Kabsch](/kabsch-algorithm/) problem with weights.
The centers are $\bar p = \sum_i w_{i,b}^2 v_i / \sum_i w_{i,b}^2$ and $\bar q = \sum_i w_{i,b} r_{f,i} / \sum_i w_{i,b}^2$, the rotation comes from the [singular value decomposition](/singular-value-decomposition/) of the cross covariance of $w_{i,b} (v_i - \bar p)$ and $r_{f,i} - w_{i,b} \bar q$, and $T = \bar q - R \bar p$.
In 2D the rotation angle is $\operatorname{atan2}$ of the sums of the cross and dot products, so the code needs no SVD.

The code works in 2D with rigid transforms $(\theta, t)$.
The paper also re-initializes bones that end up with too few vertices; the code does not need this for its test data.

## Example

The weight step for one vertex with two bones and one 2D frame: let the two candidate positions be $(1, 0)$ for bone 1 and $(0, 1)$ for bone 2.

| target | weights | error |
|---|---|---|
| $(0.5, 0.5)$ | $(0.5, 0.5)$ | 0 |
| $(1, 1)$ | $(0.5, 0.5)$ | 0.5 |
| $(2, 0)$ | $(1, 0)$ | 1 |

The target $(0.5, 0.5)$ is on the segment between the two positions, so the error is zero.
The target $(1, 1)$ projects onto the middle of the segment, and the distance is $\sqrt{0.5}$.
The target $(2, 0)$ projects onto the line beyond $(1, 0)$, at the weights $(1.5, -0.5)$, which are not allowed, so the best convex weights are $(1, 0)$ with the error $1$.

In the tests, a strip of 39 vertices is skinned to a chain of three bones in six poses, with blended weights near the two joints.
From the k-means start, the error goes from 0.0798 to $4.3 \times 10^{-8}$ in 40 iterations with $K = 2$, and it never increases.
With $K = 1$, every vertex follows one bone, and the error stops at 0.0753.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **The weight step is exact.** The minimizer over the simplex is the solution of the KKT system on its support, so trying every support and keeping the best nonnegative solution gives the minimizer.
- **The bone step is exact.** The weighted Procrustes formula gives the global minimizer over rotations and translations of the error of one bone in one frame, with the rest fixed.
- **The error does not increase.** Line L5 makes the weight step at least as good as the old weights, and each bone step is exact, so it is at least as good as the old transform.
- **The ground truth is a fixed point.** If the data come from linear blend skinning with weights and bones of the allowed form, the true weights and bones give the error zero, and no step can leave the zero error.

A monotone error that is bounded below converges, but the limit can be a poor local minimum, and nothing bounds its distance to the global one.
Le and Deng show convergence in their experiments, not in a proof.

## Complexity

The costs are in the real RAM model, for one iteration.
The weight step of the code solves up to $2^B$ systems of size at most $B + 1$ per vertex, each built from dot products of length $2F$, so it costs $O(n 2^B (B^3 + B^2 F))$.
The active set method of the paper replaces the factor $2^B$ by the number of its iterations, which is small in practice.
Each bone step costs $O(F n K)$, because each vertex has at most $K$ nonzero weights, so all bones cost $O(B F n K)$.
The extra space is $O(n B)$ for the weights and $O(B F)$ for the transforms.

## Properties

- Output fits standard pipelines: the result is plain linear blend skinning with rigid bones and convex, sparse weights.
- Monotone in this code: the error does not increase over the iterations.
- Local: the result depends on the k-means start and can be a local minimum.
- No hierarchy: the bones are free rigid transforms, not a skeleton with joints.
- Lossy: with few bones, the error of a nonrigid motion, such as cloth, does not go to zero.

## Variants and improvements

- **Skinning mesh animations.** James and Twigg (2005) also fit a skinning model to mesh animations, starting from groups of triangles that rotate together.
- **Skeleton extraction.** Later work fits a hierarchy of bones with joints, so that the result is a skeleton an animator can use.
- **Better weights.** Instead of the per vertex simplex fit, one can add smoothness of the weights over the mesh, which helps when the examples do not cover all motions.
- **Corrections.** Residual errors can be stored as per pose corrections, as in [pose space deformation](/pose-space-deformation/).
- **Other skinning models.** The same alternating fit works with [dual quaternion skinning](/dual-quaternion-skinning/), with a harder bone step.
- **Linear compression.** [Principal component analysis](/principal-component-analysis/) of the frames is the main alternative for the compression of mesh animations, but its output is not a rig.

## When to use it

Use SSDR when you have an animation as a sequence of meshes, for example from a simulation or a capture, and you want to play it in a real-time engine that supports only linear blend skinning.
It is also useful to compress such data, and to start a rig from examples.
If the deformation is far from rigid pieces, such as a wave on water, a skinning model with few bones fits poorly.
If you already have a skeleton and want weights for it, use [automatic rigging](/automatic-rigging/) or [bounded biharmonic weights](/bounded-biharmonic-weights/) instead.

## Pitfalls

- **The number of bones.** It is an input. Too few bones give a large error, and too many give bones with few vertices that fit noise.
- **The start.** k-means can split a rigid part into two clusters or join two parts. Run with several seeds and keep the best fit.
- **Sparse weights can be worse.** Keeping the $K$ largest weights of the full solution does not give the best weights with $K$ entries. Without a safeguard such as line L5, the error can increase.
- **Rounding of the weights.** On a support of one bone, the weight is exactly 1 in theory, but a linear solve can give $1 \pm 10^{-16}$. The code sets it to 1, so the tests that compare the weights exactly pass.
- **Bones with too few vertices.** A bone with fewer than three vertices of weight is not determined in 3D. The paper re-initializes such bones.
- **Few frames.** With few example frames, the weights are not determined, and the result does not generalize to new poses.

## Implementations

## History

Fitting a skinning model to examples was studied before SSDR, for example by James and Twigg (2005).
Bones that are general affine maps can fit more motions, but many engines expect rigid bones, and weights without constraints are hard to edit.
Le and Deng (2012) kept the bones rigid and the weights convex and sparse, and showed that alternating least squares with these constraints fits many mesh animations with a small number of bones.
The method is now a common way to convert simulations to rigs for games.

## References
