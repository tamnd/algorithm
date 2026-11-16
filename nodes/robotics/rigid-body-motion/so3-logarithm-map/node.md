---
tag: 7X28ZK
kind: algorithm
slug: so3-logarithm-map
name: "Logarithm map of SO(3)"
aliases:
- matrix logarithm of a rotation
area: robotics/rigid-body-motion
level: core
summary: "Recovers the angle and axis of a 3D rotation matrix: theta by atan2 of the trace and the skew part, a series near 0, and the axis from the symmetric part near pi."
model: floating-point-model
complexity:
  vars: {n: "the size of the matrix, fixed at n = 3"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [special-orthogonal-group, rodrigues-rotation-formula]
see_also: [axis-angle-representation, rodrigues-rotation-formula, se3-exponential-map, shepperd-method, unit-quaternion-rotation, euler-rotation-theorem, spherical-linear-interpolation, uncertainty-on-lie-groups]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.3 (exponential coordinates of rotation and the matrix logarithm of a rotation, with the cases theta = 0 and theta = pi)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2.2 (exponential coordinates for rotation)
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the exponential and logarithm maps of SO(3) in the examples of the paper
---

The logarithm map of SO(3) takes a 3 by 3 rotation matrix $R$ and returns its exponential coordinates: a vector $w = \theta\hat\omega$ whose direction $\hat\omega$ is the rotation axis and whose length $\theta \in [0, \pi]$ is the rotation angle, so that $e^{[w]} = R$.
It inverts [Rodrigues' rotation formula](/rodrigues-rotation-formula/), which goes from axis and angle to the matrix.
The [axis-angle representation](/axis-angle-representation/) is the pair that both maps work with.
The formulas are short, but the textbook form loses accuracy near $\theta = 0$ and fails near $\theta = \pi$.
This page gives a version that is accurate in [floating point](/floating-point-model/) at every angle, and proves it.

## In plain words

Every turn of a solid object in space is a turn about one fixed line by some angle.
A rotation matrix holds this turn in nine numbers.
The logarithm finds the line and the angle again.
The angle comes from the sum of the three diagonal numbers.
The line comes from the differences of the numbers on the two sides of the diagonal.
When the angle is very small, the line hardly matters, and a short series avoids a division by zero.
When the angle is close to a half turn, the differences are almost zero and full of rounding noise.
Then the line comes from the sums of the numbers on the two sides of the diagonal, which are large there.
A half turn about a line is the same as a half turn about the reversed line, so at exactly a half turn there are two correct answers.

## The problem

The input is a matrix $R$ in the [special orthogonal group](/special-orthogonal-group/) SO(3), so $R^{\mathsf T} R = I$ and $\det R = 1$.
The output is a vector $w \in \mathbb{R}^3$ with $|w| \le \pi$ and $e^{[w]} = R$.
Here $[w]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $w$, so $[w] x = w \times x$, and $e^{[w]}$ is the [matrix exponential](/matrix-exponential/).
We write $w = \theta\hat\omega$ with a unit axis $\hat\omega$ and the angle $\theta = |w|$.
For $\theta < \pi$ the answer is unique.
At $\theta = \pi$ both $\pm\pi\hat\omega$ are answers.
At $\theta = 0$ the answer is $w = 0$, and the axis is undefined.

## The algorithm

The algorithm uses three facts that follow from Rodrigues' formula $R = I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2$:

$$\operatorname{tr} R = 1 + 2\cos\theta, \qquad \tfrac12 (R - R^{\mathsf T}) = \sin\theta\,[\hat\omega], \qquad \tfrac12 (R + R^{\mathsf T}) - \cos\theta\, I = (1 - \cos\theta)\,\hat\omega\hat\omega^{\mathsf T}.$$

The map $\operatorname{vee}$ is the inverse of $[\cdot]$: it reads the vector $(m_{32}, m_{13}, m_{21})$ from a skew-symmetric matrix $m$.
The two thresholds are $\delta_0 = 10^{-3}$ and $\delta_\pi = 10^{-2}$.

```pseudo id=main
SO3-LOG(R)                                  ▷ R in SO(3); returns w = θ ω̂ with θ in [0, π]
L1  c ← (tr R - 1) / 2, clamped to [-1, 1]   ▷ c = cos θ
L2  s ← vee(R - Rᵀ) / 2                       ▷ s = sin θ · ω̂
L3  θ ← atan2(|s|, c)
L4  if θ < δ₀ then                            ▷ R is close to I
L5      return (1 + θ²/6 + 7θ⁴/360) · s        ▷ the series of θ / sin θ
L6  if θ ≤ π - δ_π then
L7      return (θ / |s|) · s
L8  B ← (R + Rᵀ) / 2 - c I                    ▷ B = (1 - c) ω̂ ω̂ᵀ
L9  k ← the index of the largest diagonal entry B_kk
L10 ω̂ ← column k of B, divided by its length
L11 if ω̂ · s < 0 then ω̂ ← -ω̂                 ▷ at θ = π both signs are valid
L12 return θ ω̂
```

Lines L1 and L2 read $\cos\theta$ and $\sin\theta\,\hat\omega$ from $R$.
Line L3 takes the angle from both of them with atan2, and not from the cosine alone with arccos.
Line L5 handles small angles, where the exact factor $\theta / \sin\theta$ would be $0/0$ at $\theta = 0$.
Line L7 is the general case.
Lines L8 to L12 handle angles near $\pi$, where $s$ is short and its direction is not reliable.
The matrix $B$ is a multiple of $\hat\omega\hat\omega^{\mathsf T}$, so each of its columns is a multiple of $\hat\omega$.
Line L9 picks the column with the largest diagonal entry, which has $\omega_k^2 \ge 1/3$, so it is far from zero.
Line L11 takes the sign from $s$, which still points the right way when $\theta < \pi$.

## Example

Take the rotation by $2\pi/3$ about the axis $(1, 1, 1)/\sqrt3$, which moves $x$ to $y$, $y$ to $z$ and $z$ to $x$:

$$R = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}.$$

- Line L1: $\operatorname{tr} R = 0$, so $c = -1/2$.
- Line L2: $s = \tfrac12 (r_{32} - r_{23},\ r_{13} - r_{31},\ r_{21} - r_{12}) = (1/2, 1/2, 1/2)$, and $|s| = \sqrt3/2 = 0.8660254$.
- Line L3: $\theta = \operatorname{atan2}(0.8660254, -0.5) = 2\pi/3 = 2.0943951$.
- Line L7: $w = (2.0943951 / 0.8660254) \cdot (1/2, 1/2, 1/2) = (1.2091996, 1.2091996, 1.2091996)$.

So the axis is $(1, 1, 1)/\sqrt3$ and the angle is $2.0943951$ rad, or 120 degrees.

A second example takes the half turn about the $x$ axis, $R = \operatorname{diag}(1, -1, -1)$.
Line L1 gives $c = -1$ and line L2 gives $s = 0$, so line L3 gives $\theta = \operatorname{atan2}(0, -1) = \pi$.
The textbook formula $[\hat\omega] = (R - R^{\mathsf T}) / (2\sin\theta)$ is $0/0$ here.
Line L8 gives $B = \operatorname{diag}(2, 0, 0)$, line L9 picks $k = 1$, and line L10 gives $\hat\omega = (1, 0, 0)$.
Line L11 makes no change because $\hat\omega \cdot s = 0$, and the output is $w = (\pi, 0, 0)$.
The vector $(-\pi, 0, 0)$ is also correct.

The table shows a measurement on IEEE double precision with the implementation of this page.
The axis is $(2, 3, 6)/7$, and $R$ is computed from $w = \theta\hat\omega$ by Rodrigues' formula.
The textbook method is the three-case method: $R = I$ gives $w = 0$, $\operatorname{tr} R = -1$ gives $\theta = \pi$, and else $\theta = \arccos c$ and $[\hat\omega] = (R - R^{\mathsf T})/(2\sin\theta)$.
The columns give the largest absolute error.

| $\theta$ | $\theta$ by arccos | $\theta$ by atan2 | $w$ by the textbook method | $w$ by SO3-LOG |
|---|---|---|---|---|
| $10^{-9}$ | 1.0e-9 | 0 | 8.6e-10 | 0 |
| $10^{-6}$ | 4.4e-11 | 0 | 1.1e-22 | 1.1e-22 |
| $10^{-3}$ | 7.8e-15 | 0 | 1.1e-19 | 1.1e-19 |
| $1$ | 1.1e-16 | 1.1e-16 | 0 | 0 |
| $\pi - 10^{-3}$ | 6.6e-13 | 0 | 1.8e-9 | 0 |
| $\pi - 10^{-6}$ | 4.4e-11 | 4.4e-16 | 1.2e-4 | 1.1e-16 |
| $\pi - 10^{-9}$ | 1.0e-9 | 0 | 1.1e-9 | 2.2e-16 |

At $\theta = 10^{-9}$ the trace rounds to exactly 3, so the textbook method returns $w = 0$.
At $\theta = 10^{-6}$ its angle is wrong in the fifth digit, but the error cancels in $w$, because $\theta / \sin\theta$ is flat near 0.
Near $\pi$ the division by $\sin\theta$ makes the textbook error grow, and at $\pi - 10^{-9}$ the trace rounds to exactly $-1$, so the method returns the half turn.

## Correctness

Every rotation is $e^{[\hat\omega]\theta}$ for a unit $\hat\omega$ and some $\theta \in [0, \pi]$; this is [Euler's rotation theorem](/euler-rotation-theorem/) together with Rodrigues' formula.
The three identities above then give $c = \cos\theta$ and $s = \sin\theta\,\hat\omega$, and since $\sin\theta \ge 0$ on $[0, \pi]$, line L3 returns $\theta$ exactly.
Line L7 returns $(\theta/\sin\theta)\sin\theta\,\hat\omega = \theta\hat\omega$.
Line L5 differs from the exact factor by a relative amount of about $31\theta^6/15120$, which is below $3 \cdot 10^{-21}$ for $\theta < \delta_0$.
In lines L8 to L12, column $k$ of $B$ is $(1 - c)\,\omega_k\,\hat\omega$, so line L10 gives $\pm\hat\omega$, and line L11 fixes the sign when $\theta < \pi$.
At $\theta = \pi$ both signs give the same $R$.
The proof below also shows that the answer is unique when $\theta < \pi$, and gives first-order error estimates in floating point.

## Complexity

The input has a fixed size, so the time and the space are $\Theta(1)$.
The general case uses about 25 floating-point operations, one square root and one atan2.
The branch near $\pi$ adds about 35 operations and a second square root.
There is no loop and no iteration.

A general routine for the logarithm of an $n \times n$ matrix uses $O(n^3)$ operations per step, with several square roots of matrices.
The closed form above needs none of that, because it uses the structure of SO(3).

## Properties

- **Inverse of the exponential.** On the open ball $|w| < \pi$, the logarithm is the inverse of $w \mapsto e^{[w]}$, and it is smooth there.
- **A jump at $\pi$.** On the set of rotations by $\pi$, the output can jump between $\pi\hat\omega$ and $-\pi\hat\omega$. No continuous logarithm exists on all of SO(3).
- **Range.** A rotation by an angle $\alpha \in (\pi, 2\pi)$ about $\hat\omega$ comes back as the rotation by $2\pi - \alpha$ about $-\hat\omega$.
- **Accuracy.** The angle has an absolute error of the order of the unit roundoff at every angle, because both arguments of atan2 have such an error and the gradient of atan2 has length about 1 here.
- **Exact zero.** $R = I$ gives $w = 0$ exactly, with no division.

## Variants and improvements

- **The textbook three-case method.** Lynch and Park give the method with arccos and two exact tests, $R = I$ and $\operatorname{tr} R = -1$. In the case $\operatorname{tr} R = -1$ they give the axis from a nonzero column of $R + I$, which is $2\hat\omega\hat\omega^{\mathsf T}$ at $\theta = \pi$. Lines L8 to L10 extend this idea to angles near $\pi$, and the table shows why that matters.
- **Through a unit quaternion.** Convert $R$ to a unit quaternion $q = (q_w, q_v)$ with [Shepperd's method](/shepperd-method/), then use $\theta = 2\operatorname{atan2}(|q_v|, q_w)$ and $\hat\omega = q_v / |q_v|$. Shepperd's method picks the largest of four candidates in the same way as line L9. See [unit quaternion rotation](/unit-quaternion-rotation/).
- **The plane.** In SO(2), the logarithm is $\theta = \operatorname{atan2}(r_{21}, r_{11})$, with no special cases.
- **SE(3).** The logarithm of a rigid motion uses this map for the rotation part, then solves for the translation part. See the [exponential map of SE(3)](/se3-exponential-map/).

## When to use it

Use the logarithm to measure the difference of two rotations as an angle and an axis: $\log(R_1^{\mathsf T} R_2)$ is the rotation that takes $R_1$ to $R_2$, in the body frame of $R_1$.
Attitude controllers use it as the error signal.
The residuals of [pose graph optimization](/pose-graph-optimization/) and the error states of the [error-state Kalman filter](/error-state-kalman-filter/) use it to map rotations to vectors.
It is the base of [uncertainty on Lie groups](/uncertainty-on-lie-groups/), [rotation averaging](/rotation-averaging/) and [spherical linear interpolation](/spherical-linear-interpolation/), where $R_1 e^{t \log(R_1^{\mathsf T} R_2)}$ moves from $R_1$ to $R_2$ at constant angular speed.

## Pitfalls

- **arccos near 0 and $\pi$.** The slope of arccos is infinite at $\pm 1$, so an error $\delta$ in $c$ gives an angle error up to $\sqrt{2\delta}$. Use atan2 of both the sine and the cosine.
- **Exact equality tests.** A computed rotation is almost never exactly $I$ and almost never has a trace of exactly $-1$. Use a threshold, and choose it so that both branches are accurate where they meet.
- **Arguments out of range.** Rounding can make $c$ slightly larger than 1 or smaller than $-1$. Then arccos raises an error or returns NaN. Clamp $c$.
- **The sign at $\pi$.** Code that compares two logarithms near $\pi$ must accept both signs. A trajectory of rotations that passes through angle $\pi$ gets a jump in $w$; unwrap it by continuity if you need a smooth curve.
- **A matrix that is not a rotation.** After many products, $R$ drifts away from SO(3). The formulas then give a wrong answer without a warning. Orthonormalize $R$ first, for example with the [Gram-Schmidt process](/gram-schmidt-process/) or the [singular value decomposition](/singular-value-decomposition/).
- **The order of the vee map.** The vector of $[w]$ is $(m_{32}, m_{13}, m_{21})$. A swap of two indices gives the axis with a wrong sign.

## Implementations

## History

Rodrigues published the formula for a rotation in terms of its axis and angle in 1840, and the trace and skew relations that the logarithm uses follow from it.
Murray, Li and Sastry (1994) gave the arccos and skew formulas in their treatment of exponential coordinates for rotation, and Lynch and Park (2017) gave the three-case algorithm with the special cases $\theta = 0$ and $\theta = \pi$ in Section 3.2.3.
The use of atan2 and of the symmetric part near $\pi$ is common practice in numerical libraries for Lie groups; Sola, Deray and Atchuthan (2018) survey these maps for state estimation.

## References
