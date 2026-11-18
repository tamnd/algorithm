---
tag: 1WQ6KE
kind: algorithm
slug: linear-blend-skinning
name: Linear blend skinning
aliases:
- LBS
- skeletal subspace deformation
- smooth skinning
area: graphics-and-signals/character-animation
level: intro
summary: Deforms a mesh by a skeleton. Each vertex goes to the weighted sum of its positions under the skinning matrices of its joints. Fast and simple, but twisted joints collapse.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex"}
  time: {frame: "O(j + n k)"}
  space: {extra: "O(j)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [character-skeleton, bind-pose]
see_also: [dual-quaternion-skinning, candy-wrapper-artifact, spherical-blend-skinning, optimized-centers-of-rotation-skinning, delta-mush, bounded-biharmonic-weights, skinning-decomposition, pose-space-deformation]
sources:
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: "Section 2 (linear blend skinning, its other names, its history and the candy wrapper artifact)"
  - paper: doi:10.1145/1409625.1409627
    title: Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Geometric skinning with approximate dual quaternion blending, ACM Transactions on Graphics 27(4), article 105, 2008
    locator: "Section 2.2 (linear blend skinning, equation 2, and the candy wrapper example)"
---

Linear blend skinning (LBS) moves the vertices of a character mesh with the joints of its [skeleton](/character-skeleton/).
Each vertex $v$ in the [bind pose](/bind-pose/) has weights $w_j \ge 0$ with $\sum_j w_j = 1$, and it goes to

$$v' = \Bigl(\sum_j w_j\, M_j B_j^{-1}\Bigr) v,$$

where $B_j$ is the world transform of joint $j$ in the bind pose and $M_j$ is its world transform in the current pose.
The matrix $M_j B_j^{-1}$ moves a point that is attached rigidly to joint $j$ from the bind pose to the current pose.
LBS is the standard skinning method of games and of most animation tools, because it costs a few multiply-adds per weight and runs well on a GPU.
Its known defect is that a weighted sum of rotation matrices is not a rotation, so a twisted joint loses volume (the [candy wrapper artifact](/candy-wrapper-artifact/)).

## In plain words

Think of each bone as a hand that holds a part of the skin.
If a point of the skin is held by one hand, it moves with that hand as if it were glued to it.
Near a joint, two or more hands hold the same point.
LBS asks each hand where it would carry the point, and then takes the average of these places, with the weights as the shares.
This gives smooth skin across the joint, and it is very cheap.
But the average of two places on a circle lies inside the circle.
So when one hand turns far relative to the other, the skin between them shrinks toward the bone.

## The problem

The input is a rest mesh with vertices $v_i$ and normals $n_i$ in the bind pose, the bind transforms $B_j$, the current world transforms $M_j$ of $j$ joints (from [forward kinematics](/forward-kinematics/) over the [skeleton](/character-skeleton/)), and for each vertex a sparse list of at most $k$ pairs $(j, w_{ij})$ with $w_{ij} \ge 0$ and $\sum_j w_{ij} = 1$.
The output is the deformed position $v'_i$ and the deformed unit normal $n'_i$ of each vertex.
This is one method for the [character skinning](/character-skinning/) problem.
Transforms are $4 \times 4$ homogeneous matrices that act on column vectors.

## The algorithm

```pseudo id=main
LBS(v, n, W, M, B⁻¹)                                 ▷ rest mesh, weights, pose and bind transforms
L1  for each joint j: Pⱼ ← Mⱼ Bⱼ⁻¹                    ▷ the skinning matrix palette
L2  for each vertex i do
L3      A ← 0                                         ▷ a 4 × 4 matrix
L4      for each (j, w) in Wᵢ: A ← A + w Pⱼ
L5      v′ᵢ ← A vᵢ                                    ▷ vᵢ as the point (x, y, z, 1)
L6      n′ᵢ ← normalize(A₃⁻ᵀ nᵢ)                       ▷ A₃ is the upper left 3 × 3 block
L7  return v′, n′
```

Line L1 runs once per frame for the whole skeleton.
Lines L3 and L4 blend the matrices first, which costs one matrix per vertex; transforming the point by each $P_j$ and blending the points gives the same result, because the map is linear.
Line L6 uses the inverse transpose, because normals must stay orthogonal to the tangents, and the tangents move by $A_3$.
The code uses the cofactor matrix $\operatorname{cof}(A_3) = \det(A_3)\, A_3^{-T}$ with the sign of the determinant, which gives the same unit normal and does not divide by a small determinant.

## Example

Take two joints at the origin with $B_1 = B_2 = I$.
Joint 1 stays still, and joint 2 twists by the angle $\theta$ about the $x$ axis.
The vertex $v = (0, 1, 0)$ has the weights $\tfrac12$ and $\tfrac12$.

| twist $\theta$ | $P_1 v$ | $P_2 v$ | $v'$ | distance from the axis |
|---|---|---|---|---|
| $0$ | $(0, 1, 0)$ | $(0, 1, 0)$ | $(0, 1, 0)$ | $1$ |
| $\pi/2$ | $(0, 1, 0)$ | $(0, 0, 1)$ | $(0, 0.5, 0.5)$ | $0.70711$ |
| $\pi$ | $(0, 1, 0)$ | $(0, -1, 0)$ | $(0, 0, 0)$ | $0$ |

In general the distance is $\bigl|\cos(\theta/2)\bigr|$.
At the half turn the vertex falls onto the axis, which is the candy wrapper collapse.
A method that blends rotations instead of matrices, such as [dual quaternion skinning](/dual-quaternion-skinning/), keeps the distance 1 and turns the vertex by $\theta/2$.

## Correctness

LBS has no target shape to match, so correctness here means that it computes the stated blend and has the properties that skinning needs.
These are proved properties of the formula, in exact arithmetic; the proofs are in [proofs/correctness.md](proofs/correctness.md).
- Line L5 equals $\sum_j w_j P_j v$, the blend of the rigidly moved points, because matrix products are linear.
- Because $\sum_j w_j = 1$, the bottom row of $A$ is $(0, 0, 0, 1)$, so $A$ is an affine map.
- In the bind pose, $M_j = B_j$, so every $P_j = I$, $A = I$, and the mesh is the rest mesh.
- A vertex with one weight of 1 moves rigidly with its joint.
- If every joint moves by the same rigid motion $G$, the whole mesh moves by $G$.
- The normal of line L6 is orthogonal to every deformed tangent $A_3 t$ with $t \cdot n = 0$.

LBS does not keep lengths or volume in general: $A_3$ is a rotation only when all the rotations of the joints of the vertex agree.

## Complexity

Line L1 costs $O(j)$ matrix products per frame.
Lines L2 to L6 cost $O(k)$ per vertex, so $O(n k)$ in total, and the time per frame is $O(j + n k)$.
The extra space is the palette, $O(j)$.
The vertices are independent, so a vertex shader or a compute kernel runs them in parallel.

## Properties

- Linear in the vertex and in the weights; affine invariant when $\sum_j w_j = 1$.
- Deterministic, with a fixed cost per weight.
- Handles any affine joint transform, including scale and shear, because it blends matrices.
- Not volume preserving. The blended matrix can be close to singular at a twisted joint, and shrinks the skin at a bent joint (the collapsing elbow).
- The result depends only on the weights and the palette. It has no state between frames.

## Variants and improvements

- **Dual quaternion skinning.** [Dual quaternion skinning](/dual-quaternion-skinning/) blends unit dual quaternions and normalizes them, so the result is always rigid when the blended real part is not zero.
- **Spherical blend skinning.** [Spherical blend skinning](/spherical-blend-skinning/) blends the rotations as quaternions about a center found by least squares.
- **Optimized centers of rotation.** [CoR skinning](/optimized-centers-of-rotation-skinning/) precomputes a center per vertex, then blends the rotation as a quaternion and the center as LBS.
- **Corrective layers.** [Pose space deformation](/pose-space-deformation/) adds sculpted corrections as a function of the pose, and [delta mush](/delta-mush/) smooths the LBS result and puts back the rest detail.
- **Contact.** [Implicit skinning](/implicit-skinning/) projects the LBS or DQS vertices onto an implicit surface to model skin contact.
- **Weights.** The weights come from a painter, from [automatic rigging](/automatic-rigging/), from [bounded biharmonic weights](/bounded-biharmonic-weights/), or from [skinning decomposition](/skinning-decomposition/) of example meshes.

## When to use it

Use LBS as the default for real-time characters, crowds and mobile targets.
It is the method that file formats and engines expect, and it supports scale.
Use dual quaternion skinning or a corrective method where joints twist far, for example forearms, wrists and shoulders.

## Pitfalls

- **Weights that do not sum to 1.** Then $A$ is not affine, and the mesh drifts or scales. Normalize the weights after you clamp or prune them.
- **Wrong matrix order.** The palette is $M_j B_j^{-1}$, not $B_j^{-1} M_j$. With row vectors the order is reversed; keep one convention.
- **Normals by $A_3$.** Multiplying the normal by $A_3$ is correct only for a rotation. Use the inverse transpose and normalize, or use the rotation of a rigid method.
- **Singular blends.** At a twist of $\pi$ between two joints with equal weights, $A_3$ has rank 1 and the normal is not defined. The cofactor of a rank 1 matrix is zero, so the code raises an error there.
- **Too many influences.** Hardware paths often limit $k$ to 4. Pruning the small weights changes the shape; renormalize after it.

## Implementations

## History

The roots of LBS are hard to trace, as Kavan notes in the 2014 skinning course.
Magnenat-Thalmann, Laperrière and Thalmann (1988) used joint-dependent local deformations of a hand mesh, and the method spread in games and tools under many names: vertex blending, enveloping, smooth skinning and matrix palette skinning.
Lewis, Cordner and Fong (2000) gave an exact description of it under the name skeleton subspace deformation, also written skeletal subspace deformation, as the base layer of pose space deformation.
Kavan, Collins, Žára and O'Sullivan (2008) gave the candy wrapper example with a twist of 180 degrees and replaced the matrix blend with a dual quaternion blend.

## References
