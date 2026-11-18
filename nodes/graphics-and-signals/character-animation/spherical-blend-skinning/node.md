---
tag: E1S4SH
kind: algorithm
slug: spherical-blend-skinning
name: Spherical blend skinning
aliases:
- spherical skinning
area: graphics-and-signals/character-animation
level: advanced
summary: Blends the joint rotations as quaternions about a center of rotation that least squares finds for each set of joints. Each vertex moves rigidly, so twisted joints keep their volume.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex"}
  time: {frame: "O(j + n k^2)"}
  space: {extra: "O(j + n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [linear-blend-skinning, unit-quaternion-rotation, least-squares-problem]
see_also: [dual-quaternion-skinning, candy-wrapper-artifact, optimized-centers-of-rotation-skinning, singular-value-decomposition, spherical-linear-interpolation, rotation-averaging, character-skinning]
sources:
  - paper: doi:10.1145/1053427.1053429
    title: "Ladislav Kavan and Jiří Žára, Spherical blend skinning, a real-time deformation of articulated models, Proceedings of the 2005 Symposium on Interactive 3D Graphics and Games (I3D), 9-16, 2005"
    locator: "Section 4 (the center of rotation by least squares, equation 9), Section 4.1 (QLERP) and Section 4.2 (the sign of the quaternions)"
---

Spherical blend skinning (SBS) deforms a mesh by a skeleton, like [linear blend skinning](/linear-blend-skinning/), but it blends the rotations of the joints as quaternions instead of blending matrices.
A rotation needs a center, and the joints that move a vertex do not share one in general.
SBS finds the center $r_c$ by least squares, as the point that the rigid skinning transforms $C_j$ of the vertex's joints move the least apart, and then computes

$$v' = Q\,(v - r_c) + \sum_j w_j\, C_j r_c,$$

where $Q$ is the normalized weighted sum of the joint quaternions.
The center depends only on the set of joints, so one center serves every vertex with the same set.
Each vertex moves by a rigid transform, so a twisted joint keeps its radius and the [candy wrapper artifact](/candy-wrapper-artifact/) does not occur.
SBS came two years before [dual quaternion skinning](/dual-quaternion-skinning/), which removed the need for a center.

## In plain words

Plain skinning averages the positions that each bone would give a point.
When two bones turn in opposite directions, the average falls inside the limb, and the skin collapses.
Spherical blend skinning averages the turns instead.
It first finds a pivot point that the bones of a region agree on as well as possible.
Then it turns the point about that pivot by the average turn of the bones.
Because the point is only turned and moved, never squeezed, the limb keeps its thickness.
Points that use the same bones share one pivot, so the extra cost is small.

## The problem

The input is the rest mesh with the vertices $v_i$ and the normals $n_i$, the weights $w_{ij} \ge 0$ with $\sum_j w_{ij} = 1$, and the rigid skinning transforms $C_j = M_j B_j^{-1}$ of the current pose, where $M_j$ comes from [forward kinematics](/character-skeleton/) and $B_j$ is the [bind pose](/bind-pose/) transform.
Write $C_j x = R_j x + t_j$, with the rotation $R_j$ and its unit quaternion $q_j$.
The output is the deformed mesh.
This is the [character skinning](/character-skinning/) problem with rigid joint transforms; SBS does not handle scale.

## The algorithm

For a set $J$ of joints, the center $r_c$ minimizes

$$f(r) = \sum_{a < b \in J} \lvert C_a r - C_b r \rvert^2 = \sum_{a < b \in J} \lvert (R_a - R_b)\, r - (t_b - t_a) \rvert^2.$$

If the minimizer is not unique, SBS takes the one of minimal norm.

```pseudo id=main
SPHERICAL-BLEND-SKINNING(V, N, W, C)                  ▷ rest mesh, weights, joint transforms
L1  for each vertex i
L2      J ← the set of joints with w_ij > 0
L3      if J is not in the cache of this frame
L4          r ← minimal norm minimizer of Σ_{a<b ∈ J} |(R_a - R_b) r - (t_b - t_a)|²
L5          cache[J] ← r
L6      r_c ← cache[J]
L7      Q ← normalize(Σ_j s_j w_ij q_j)              ▷ s_j = ±1, so that q_p · s_j q_j ≥ 0 for the pivot p
L8      v'_i ← Q (v_i - r_c) + Σ_j w_ij C_j r_c
L9      n'_i ← Q n_i
L10 return V', N'
```

Line L4 is a linear least squares problem with 3 unknowns.
Its normal equations are $N r = g$ with $N = \sum (R_a - R_b)^\top (R_a - R_b)$ and $g = \sum (R_a - R_b)^\top (t_b - t_a)$.
The code takes the pseudo-inverse of the symmetric $3 \times 3$ matrix $N$ from its eigenvalues; an [SVD](/singular-value-decomposition/) of the stacked matrix is more accurate.
Line L7 is QLERP, the normalized linear blend of quaternions, with the pivot $p$ taken as the joint of the largest weight; it is a cheap stand-in for a true spherical average of the rotations.
Line L8 rotates the vertex about $r_c$ and then moves $r_c$ to the blend of its images; for one joint it gives $C_j v$.

## Example

Take two joints with the weights $0.5$ and $0.5$, $C_0 = I$, and $C_1$ a turn by $\pi$ about the $x$ axis, the twist of the candy wrapper.
The center minimizes $|(I - R_x(\pi))\, r|^2$, which is zero on the whole $x$ axis, and the point of minimal norm is the origin.
QLERP blends $q_0 = (1, 0, 0, 0)$ and $q_1 = (0, 1, 0, 0)$ into $(1, 1, 0, 0)/\sqrt2$, the turn by $\pi/2$ about $x$.

| vertex | LBS | SBS |
|---|---|---|
| $(0, 1, 0)$ | $(0, 0, 0)$ | $(0, 0, 1)$ |
| $(0.3, 1, 0)$ | $(0.3, 0, 0)$ | $(0.3, 0, 1)$ |

LBS collapses the vertex onto the axis; SBS turns it by half the twist and keeps the radius 1.
For a twist $\theta \le \pi$ the SBS vertex turns by exactly $\theta/2$.

For a bend, let $C_1$ turn by $\pi/2$ about the $z$ axis through $c = (1, 0, 0)$, the elbow.
The least squares problem is zero on the line through $c$ parallel to $z$, so $r_c = (1, 0, 0)$.
The vertex $(1.5, 0, 0)$ goes to $(1.35355, 0.35355, 0)$, at the distance $0.5$ from the elbow, while LBS gives $(1.25, 0.25, 0)$ at the distance $0.35355$.
In this example the result equals that of dual quaternion skinning.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they are proved properties in exact arithmetic.
- In the bind pose every vertex and normal stays where it is, and a vertex with one joint moves by $C_j$.
- If the joints of a set turn about a common point $c$ and the minimizer is unique, then $r_c = c$.
- The result does not depend on which minimizer line L4 picks, so the minimal norm choice is only a way to make the choice unique.
- With the pivot alignment, the sum in line L7 has a norm of at least the pivot weight, so $Q$ always exists.
- For a fixed joint set and fixed weights, the map $v \mapsto v'$ is a rotation followed by a translation: the vertices keep their distances and the normals stay unit vectors.
- If the whole pose and mesh are moved by a rigid change of coordinates, the result moves with them.
- If $Q$ is replaced by the matrix $\sum_j w_j R_j$, line L8 gives linear blend skinning for any center, so the difference between the methods is only the blend of the rotations.

## Complexity

The quaternions of the palette cost $O(j)$ per frame.
A center costs $O(k^2)$ for the $k(k-1)/2$ pairs and $O(1)$ for the $3 \times 3$ solve, and a vertex costs $O(k)$ after that.
In the worst case each vertex has its own joint set, which gives $O(j + n k^2)$ time per frame; in a real mesh most vertices share a few joint sets, and the centers add little.
The cache holds at most one center per vertex, so the extra space is $O(j + n)$.

## Properties

- Rigid per vertex: no volume loss under twist, unlike LBS (a proved property).
- QLERP is not the exact spherical average of the rotations; for the turn angles of real joints it is close, and the paper analyzes its error (Section 4.1). This is a heuristic choice for speed.
- The center of a set of joints is the same for all its vertices, so vertices that use the same joints with different weights turn about the same point.
- The center can jump when the least squares problem is close to rank deficient, for example when the relative turns of the joints have nearly parallel axes.
- It needs rigid joint transforms; scale and shear in $C_j$ are outside the method.

## Variants and improvements

- **Dual quaternion skinning.** [DQS](/dual-quaternion-skinning/) blends rotation and translation together as dual quaternions, with no center and no least squares, and it is coordinate invariant in the same way.
- **Optimized centers of rotation.** [CoR skinning](/optimized-centers-of-rotation-skinning/) computes a center per vertex from the weights in a precomputation, instead of per joint set in each frame, which removes the bulge of DQS in bends.
- **Better rotation averages.** QLERP can be replaced by a true spherical average or by [rotation averaging](/rotation-averaging/), at a higher cost.
- **Linear rotation blend.** With $\sum_j w_j R_j$ in place of $Q$ the method becomes LBS again, which shows that the center has no effect on LBS.

## When to use it

Use it where twist collapse is a problem and the joint transforms are rigid, and where a per-joint-set solve per frame is acceptable.
Today DQS is the usual choice for the same job, because it needs no center and runs in the same way on the GPU; SBS is mainly of interest as the step between LBS and DQS, and as the source of the idea of a center of rotation.

## Pitfalls

- **Cache per frame.** The center depends on the pose, so the cache must be cleared every frame; it is keyed by the joint set, not by the weights.
- **Sign of the quaternions.** $q$ and $-q$ give the same rotation; without the pivot alignment of line L7 the blend can turn the long way or reach zero.
- **Rank deficiency.** A set of two joints always has a line of solutions, because the relative turn of the two joints has an axis $u$ with $R_a u = R_b u$, and a move along $u$ does not change $f$. Without the minimal norm rule the solver fails or picks an arbitrary point.
- **Large weight sets.** The center of many joints is a compromise for all of them and can lie far from every joint; limit the joints per vertex to a few.
- **Normals.** Rotate normals by $Q$ only; they are not moved by the translation.

## Implementations

## History

Ladislav Kavan and Jiří Žára presented spherical blend skinning at I3D 2005 as a fix for the volume loss of linear blend skinning in twists.
Two years later Kavan, Collins, Žára and O'Sullivan introduced dual quaternion skinning, which gives a rigid blend without the center of rotation.
The idea of a center of rotation per vertex came back in 2016 with the optimized centers of Le and Hodgins.

## References
