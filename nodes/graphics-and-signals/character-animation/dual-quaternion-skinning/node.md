---
tag: SVNNAZ
kind: algorithm
slug: dual-quaternion-skinning
name: Dual quaternion skinning
aliases:
- DQS
- dual quaternion linear blending
area: graphics-and-signals/character-animation
level: core
summary: Blends the joint transforms as unit dual quaternions with aligned signs, then normalizes. The result is rigid unless the blended real part is zero, and twisted joints do not collapse.
solves: [character-skinning]
model: real-ram
complexity:
  vars: {n: "the number of vertices", j: "the number of joints", k: "the largest number of joints per vertex"}
  time: {frame: "O(j + n k)"}
  space: {extra: "O(j)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [linear-blend-skinning, dual-quaternion, unit-quaternion-rotation]
see_also: [candy-wrapper-artifact, spherical-blend-skinning, optimized-centers-of-rotation-skinning, implicit-skinning, squad, spherical-linear-interpolation, character-skinning]
sources:
  - paper: doi:10.1145/1230100.1230107
    title: Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Skinning with dual quaternions, Proceedings of the 2007 Symposium on Interactive 3D Graphics and Games (I3D), 39-46, 2007
    locator: the whole paper (dual quaternion skinning)
  - paper: doi:10.1145/1409625.1409627
    title: Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Geometric skinning with approximate dual quaternion blending, ACM Transactions on Graphics 27(4), article 105, 2008
    locator: "Section 3.3 (equation 11 and Lemma 2, coordinate invariance), Section 3.4 (comparison with ScLERP), Section 4 (Algorithm 1), Section 4.1 (antipodality, Algorithm 2 and Lemma 5) and Section 4.2 (scale and shear)"
  - url: https://skinning.org/direct-methods.pdf
    title: Ladislav Kavan, Part I, Direct skinning methods and deformation primitives, in Alec Jacobson, Zhigang Deng, Ladislav Kavan and J. P. Lewis, Skinning, Real-time Shape Deformation, SIGGRAPH 2014 course
    locator: "Section 4 (dual quaternion blending, the double cover, non-rigid transforms and the bulging artifact)"
---

Dual quaternion skinning (DQS) deforms a mesh by a skeleton, like [linear blend skinning](/linear-blend-skinning/), but it blends the joint transforms as unit [dual quaternions](/dual-quaternion/) instead of as matrices.
A rigid transform with the rotation quaternion $r$ and the translation $t$ is $\sigma = r + \varepsilon d$ with $d = \tfrac12 t r$.
For a vertex with the weights $w_j$, DQS computes

$$b = \sum_j w_j s_j \sigma_j, \qquad c = \frac{b}{\lVert b \rVert},$$

where $s_j = \pm 1$ aligns the signs of the quaternions and $\lVert b \rVert$ is the dual quaternion norm.
If the real part $b_0$ of $b$ is not zero, $c$ is a unit dual quaternion, so the vertex moves by a rigid transform.
A twisted joint therefore does not collapse: the skin turns about the bone and keeps its distance from it.
Kavan, Collins, Žára and O'Sullivan gave the method in 2007, and it is in most animation tools and game engines as an option next to LBS.

## In plain words

Linear blend skinning averages the places where each bone would carry a point of the skin.
That average cuts across the circle, so the skin shrinks at a twist.
DQS averages the motions themselves, in a form where a turn and a shift are one object.
After the average, it scales the result so that it is again an exact turn and shift.
The point then moves on the circle, not across it, so a twist of half a turn between two bones gives a quarter turn in the middle, with no loss of thickness.
The price is that the skin can bulge out a little at a bent joint, and the method cannot blend a bone that is scaled.

## The problem

The input is the same as for [linear blend skinning](/linear-blend-skinning/): rest vertices and normals in the [bind pose](/bind-pose/), weights $w_{ij} \ge 0$ with $\sum_j w_{ij} = 1$, and the skinning matrices $P_j = M_j B_j^{-1}$ of $j$ joints.
Here each $P_j$ must be rigid, a rotation and a translation.
The output is the deformed position and unit normal of each vertex, for the [character skinning](/character-skinning/) problem.

Quaternions use the Hamilton convention with the scalar first.
A dual quaternion is $\sigma = r + \varepsilon d$ with $\varepsilon^2 = 0$.
It is a unit dual quaternion if $|r| = 1$ and $r \cdot d = 0$ (the dot product in $\mathbb R^4$).
The translation is recovered by $t = 2 d r^*$.

## The algorithm

```pseudo id=main
DQS(v, n, W, P)                                      ▷ rest mesh, weights, rigid skinning matrices
L1  for each joint j: (rⱼ, dⱼ) ← DQ(Pⱼ)              ▷ dⱼ = ½ (0, tⱼ) rⱼ
L2  for each vertex i do
L3      p ← r of the joint of largest weight in Wᵢ   ▷ the pivot
L4      b₀ ← 0; b_ε ← 0
L5      for each (j, w) in Wᵢ do
L6          s ← -1 if p · rⱼ < 0, else 1             ▷ rⱼ and -rⱼ are the same rotation
L7          b₀ ← b₀ + s w rⱼ; b_ε ← b_ε + s w dⱼ
L8      if b₀ = 0 then fail                           ▷ no rigid transform
L9      c₀ ← b₀ / |b₀|; c_ε ← b_ε / |b₀| - (c₀ · b_ε / |b₀|) c₀
L10     t ← 2 c_ε c₀*                                 ▷ its vector part
L11     v′ᵢ ← c₀ vᵢ c₀* + t; n′ᵢ ← c₀ nᵢ c₀*
L12 return v′, n′
```

Line L1 converts each skinning matrix once per frame.
Lines L3 to L7 blend the dual quaternions of the vertex after the sign alignment of [Kavan et al. (2008)](https://doi.org/10.1145/1409625.1409627), Algorithm 2, with the joint of largest weight as the pivot.
Line L9 is the division by the dual norm $\lVert b \rVert = |b_0| + \varepsilon\,\frac{b_0 \cdot b_\varepsilon}{|b_0|}$.
The term $-(c_0 \cdot b_\varepsilon / |b_0|)\, c_0$ makes $c_0 \cdot c_\varepsilon = 0$; it changes only the scalar part of $c_\varepsilon c_0^*$, so a shader may drop it and still get the same $t$.
Line L11 rotates the normal by the rotation of the blend, so it stays unit length.

## Example

Take $P_1 = I$ and $P_2 = R_x(\pi)$, with the weights $\tfrac12$ and $\tfrac12$ on the vertex $(0, 1, 0)$.
The quaternions are $r_1 = (1, 0, 0, 0)$ and $r_2 = (0, 1, 0, 0)$, and $r_1 \cdot r_2 = 0$, so no sign changes.
The blend is $b_0 = (0.5, 0.5, 0, 0)$ with $|b_0| = 0.70711$, so $c_0 = (0.70711, 0.70711, 0, 0)$, the rotation by $\pi/2$ about $x$.
The vertex goes to $(0, 0, 1)$, at the distance 1 from the axis.
[LBS](/linear-blend-skinning/) puts it at $(0, 0, 0)$.

A bent joint: let $P_2$ be the rotation by $\pi/2$ about the $z$ axis through the joint $c = (1, 0, 0)$, so $P_2 v = R_z(\pi/2) v + (1, -1, 0)$.
Then $r_2 = (0.70711, 0, 0, 0.70711)$ and $d_2 = (0, 0, -0.70711, 0)$.
For the vertex $(1.5, 0, 0)$ with the weights $\tfrac12$ and $\tfrac12$, the blend gives $c_0 = (0.92388, 0, 0, 0.38268)$, the rotation by $\pi/4$, and the vertex goes to $(1.35355, 0.35355, 0)$.
That is the distance 0.5 from the joint, as in the rest pose.
LBS gives $(1.25, 0.25, 0)$, at the distance 0.35355.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
They are proved properties of the blend in exact arithmetic.
- **Rigidity.** If $b_0 \ne 0$, line L9 gives $|c_0| = 1$ and $c_0 \cdot c_\varepsilon = 0$, so $c$ is a unit dual quaternion and line L11 applies a rotation and a translation.
- **The exception.** If $b_0 = 0$, there is no normalization and no rigid transform. Without the sign alignment this happens even for two joints with the same rotation, for example the weights $\tfrac12$ and $\tfrac12$ on $r$ and $-r$.
- **The pivot bound.** With the pivot alignment of line L6, $|b_0| \ge b_0 \cdot p \ge w_p > 0$, where $w_p$ is the weight of the pivot joint. So line L8 never fails after this alignment.
- **Single joints.** A vertex with one weight of 1 gets $c = \pm\sigma_j$, the transform $P_j$, which is also the LBS result.
- **Bind pose.** If every $P_j = I$, then every $\sigma_j = 1$ and the mesh is the rest mesh.
- **Coordinate invariance.** Changing the world frame by a rigid $G$ changes the result by $G$ (Kavan et al. 2008, Lemma 2).
- **Pure translations.** If all $r_j = 1$, the translation of the blend is $\sum_j w_j t_j$, the same as LBS.

The pivot bound does not mean that the signs are right.
For three or more joints the signs may have no choice where every pair has a nonnegative dot product (Kavan et al. 2008, Section 4.1), and the blend then depends on the pivot.

## Complexity

Line L1 costs $O(j)$ per frame.
Each vertex costs $O(k)$ for the blend and $O(1)$ for the normalization and the transform, so $O(n k)$ in total, and the time per frame is $O(j + n k)$.
The extra space is $O(j)$ dual quaternions, 8 numbers each instead of 12 for a $3 \times 4$ matrix.

## Properties

- Rigid when $b_0 \ne 0$: no loss of volume at a twist.
- For two joints, DQS and the screw linear interpolation ScLERP use the same screw axis; Kavan et al. (2008, Section 3.4) bound the difference of the rotation angles by 8.15 degrees and of the translations by 15.1%.
- Bulges at bent joints: near a bend the method acts like a spherical blend about the joint, and the skin can bulge out (the course of Jacobson et al. 2014, Section 4).
- Cannot represent scale or shear. Kavan et al. (2008, Section 4.2) handle them by a two phase method: blend the scale and shear part as matrices first, then the rigid part as dual quaternions.
- Kavan et al. (2008, Section 5) measured DQS at more than twice the speed of the log-matrix and spherical blending methods; this is a measurement on their GPU setup.

## Variants and improvements

- **Sign alignment.** Instead of one pivot per vertex, each joint can take its sign relative to its parent, once per frame for the whole skeleton (Kavan et al. 2008, Section 4.1).
- **Spherical blend skinning.** [Spherical blend skinning](/spherical-blend-skinning/), by the same group, blends the rotations about a center of rotation found by least squares.
- **Optimized centers of rotation.** [CoR skinning](/optimized-centers-of-rotation-skinning/) removes the bulge with a precomputed center per vertex.
- **Contact.** [Implicit skinning](/implicit-skinning/) uses DQS or LBS as its first step.
- **Rotation interpolation.** For two keys, the rotation part of DQS is normalized linear interpolation of quaternions, not [slerp](/spherical-linear-interpolation/); for curves through many keys, see [squad](/squad/).

## When to use it

Use DQS where joints twist, for example forearms, wrists, necks and shoulders, and where the joints have no scale.
Its cost is close to LBS, so it is a common default in games when the bulge at bent joints is acceptable.
If the joints scale, use LBS or the two phase method.

## Pitfalls

- **No sign alignment.** Without lines L3 to L6, two joints with nearly the same rotation can cancel, and the skin of the vertex jumps or the blend fails.
- **Sign flips over time.** When the pivot changes, or when $p \cdot r_j$ crosses zero, the sign of a term flips, and the vertex can jump. Kavan et al. (2008, Section 4.1) discuss these cases.
- **Wrong translation formula.** $d = \tfrac12 t r$ is for $\sigma$ applied as a rotation then a translation. The order $\tfrac12 r t$ is a different convention.
- **Scaled joints.** A joint matrix with a scale has no unit dual quaternion. Converting it with a rotation extraction silently drops the scale.
- **Normals.** The normal is rotated by $c_0$. Using the inverse transpose of the LBS matrix instead gives normals that do not match the DQS surface.

## Implementations

## History

Dual quaternions were used in kinematics and robotics for screw motions long before skinning.
Kavan and Žára (2005) first replaced the matrix blend of LBS by a quaternion blend about a center of rotation, in [spherical blend skinning](/spherical-blend-skinning/).
Kavan, Collins, Žára and O'Sullivan (2007) gave dual quaternion skinning at I3D, and the 2008 journal version proved the coordinate invariance of the blend, compared it with ScLERP, and treated the signs and the non-rigid joints.

## References
