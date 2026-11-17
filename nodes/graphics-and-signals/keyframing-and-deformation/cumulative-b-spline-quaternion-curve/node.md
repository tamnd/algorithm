---
tag: 7V1M8B
kind: algorithm
slug: cumulative-b-spline-quaternion-curve
name: Cumulative B-spline quaternion curve
aliases:
- Kim-Kim-Shin quaternion curve
area: graphics-and-signals/keyframing-and-deformation
level: advanced
summary: Build a C2 curve of unit quaternions by writing a B-spline in cumulative form and replacing each scaled difference of control points by a power of a relative rotation.
model: real-ram
complexity:
  vars: {n: "the number of control quaternions"}
  time: {build: "Θ(n)", query: "Θ(1)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [b-spline, spherical-linear-interpolation, unit-quaternion-rotation, squad]
see_also: [keyframe-interpolation, so3-logarithm-map, angular-velocity, quaternion-kinematic-equation, catmull-rom-spline, de-casteljau-algorithm, bezier-curve, euler-angles]
sources:
  - paper: doi:10.1145/218380.218486
    title: Myoung-Jun Kim, Myung-Soo Kim and Sung Yong Shin, A general construction scheme for unit quaternion curves with simple high order derivatives, Proceedings of SIGGRAPH 1995, 369-376, 1995
    locator: the whole paper (the cumulative form of a spline, the unit quaternion curve built from it, its derivatives, and the B-spline, Bezier and Hermite cases)
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: "Chapter 3, Section 3.3 (interpolation of orientations)"
---

The cumulative B-spline quaternion curve of Kim, Kim and Shin (1995) is a smooth curve of unit quaternions controlled by a sequence $q_0, \dots, q_{n-1}$ of orientations.
It starts from the [B-spline](/b-spline/) written in cumulative form, $p(t) = p_0 \tilde B_0(t) + \sum_{i \ge 1} (p_i - p_{i-1})\,\tilde B_i(t)$, where $\tilde B_i = \sum_{j \ge i} B_j$.
Each sum becomes a product and each scaled difference becomes a power of a relative rotation:

$$q(t) = q_0^{\tilde B_0(t)} \prod_{i = 1}^{n-1} \exp\bigl(\omega_i \tilde B_i(t)\bigr), \qquad \omega_i = \log(q_{i-1}^{-1} q_i).$$

For the uniform cubic B-spline the curve is $C^2$, its derivatives have short closed forms, and like a B-spline it does not pass through its control points.

## In plain words

A B-spline is a smooth curve that follows a row of control points without touching them.
You can build it step by step: start at the first point, then add a part of each step to the next point.
How much of each step you add depends on the time, through smooth weight functions.
For orientations, a step is a turn from one control orientation to the next.
This method does a part of each turn, in order, and the weights are the same as for the B-spline.
Because the weights change smoothly, the turning speed and the turning acceleration also change smoothly.
The price is that the curve passes near the control orientations, not through them.

## The problem

The input is a sequence of unit quaternions $q_0, \dots, q_{n-1}$, $n \ge 4$, in the Hamilton convention with the scalar first.
The output is a curve $q(t)$ of unit quaternions for $t \in [0, n - 3]$ that is $C^2$, so that the body [angular velocity](/angular-velocity/) and its derivative are continuous, and that depends only on the rotations, not on the coordinates.
A key interpolating curve such as [squad](/squad/) is only $C^1$.
The logarithm of a unit quaternion $(\cos\varphi, \sin\varphi\,\hat u)$ is $(0, \varphi\hat u)$, and $\exp$ is its inverse on pure quaternions.

## The algorithm

On segment $j \in \{0, \dots, n - 4\}$ with the local parameter $u \in [0, 1]$, only four basis functions are active.
The factors before them are $\exp(\omega_i) = q_{i-1}^{-1} q_i$, whose product telescopes to $q_j$, and the factors after them are 1.
So the segment is

$$q(u) = q_j \exp\bigl(\tilde B_1(u)\,\omega_{j+1}\bigr) \exp\bigl(\tilde B_2(u)\,\omega_{j+2}\bigr) \exp\bigl(\tilde B_3(u)\,\omega_{j+3}\bigr)$$

with the cumulative uniform cubic basis

$$\tilde B_1 = \tfrac16(5 + 3u - 3u^2 + u^3), \quad \tilde B_2 = \tfrac16(1 + 3u + 3u^2 - 2u^3), \quad \tilde B_3 = \tfrac16 u^3.$$

```pseudo id=main
KKS(q₀, ..., qₙ₋₁; j, u)                            ▷ control quaternions; the point of segment j at u
L1  for k ← 1 to n - 1: if qₖ₋₁ · qₖ < 0 then
L2      qₖ ← -qₖ                                     ▷ the same rotation, near the previous one
L3  for k ← 1 to n - 1: ωₖ ← log(qₖ₋₁* qₖ)           ▷ half the rotation vector of each step
L4  (B̃₁, B̃₂, B̃₃) ← the cumulative basis at u
L5  q ← qⱼ
L6  for k ← 1 to 3 do
L7      q ← q exp(B̃ₖ ωⱼ₊ₖ)                           ▷ a part of the k-th step
L8  return q
```

Lines L1 to L3 run once for the sequence.
Lines L4 to L8 are the query; for a global parameter $t$, use $j = \lfloor t \rfloor$ and $u = t - j$.
The factors of line L7 must be applied in this order, since quaternion products do not commute.

## Example

Take four control orientations: $q_0 = (1, 0, 0, 0)$; $q_1 = (0.70711, 0, 0, 0.70711)$, a turn by 90 degrees about $z$; $q_2 = (0.5, 0.5, 0.5, 0.5)$, a further turn by 90 degrees about the body $x$ axis; and $q_3 = (0, 0.70711, 0, 0.70711)$, a further turn by 90 degrees about the body $z$ axis.

- Lines L1 and L2: all adjacent dot products are $0.70711$, so no sign changes.
- Line L3: $\omega_1 = (0, 0, 0, 0.7854)$, $\omega_2 = (0, 0.7854, 0, 0)$ and $\omega_3 = (0, 0, 0, 0.7854)$.
- At $u = 0$ the basis is $(\frac56, \frac16, 0)$, and $q(0) = (0.78657, 0.10355, 0.07946, 0.60355)$, a rotation by 1.33114 radians. The key $q_1$ is a rotation by $\pi/2 = 1.5708$, so the curve does not pass through it.
- At $u = 0.5$ the basis is $(0.97917, 0.5, 0.02083)$, and $q(0.5) = (0.65328, 0.27931, 0.26160, 0.65328)$, close to the midpoint $(0.65328, 0.27060, 0.27060, 0.65328)$ of the slerp from $q_1$ to $q_2$.
- At $u = 1$ the basis is $(1, \frac56, \frac16)$, and $q(1) = (0.48296, 0.48296, 0.37059, 0.62941)$.

The body angular velocity at $u = 0.5$ is $(1.18201, 0.10022, 0.33519)$ radians per unit of $u$.

## Correctness

In the global form, each cumulative basis function $\tilde B_i = \sum_{j \ge i} B_j$ is a sum of $C^2$ cubic B-splines, so it is $C^2$.
The map $x \mapsto \exp(x\,\omega_i)$ is smooth, so each factor $\exp(\omega_i \tilde B_i(t))$ is a $C^2$ curve of unit quaternions.
A product of finitely many $C^2$ curves is $C^2$, so $q(t)$ is $C^2$.
Each factor has length 1, so $q(t)$ is a unit quaternion.

The segment form of line L7 is the global form: on segment $j$, $\tilde B_i = 1$ for $i \le j$ and $\tilde B_i = 0$ for $i > j + 3$, by the partition of unity and the supports of the B-splines.
Then $\prod_{i \le j}\exp(\omega_i) = \prod_{i \le j} q_{i-1}^{-1} q_i = q_0^{-1} q_j$.
If all control quaternions are rotations about one fixed axis, the factors commute, and the angle is the scalar B-spline of the key angles.
The [proof](proofs/correctness.md) gives the details.

## Complexity

The build step, lines L1 to L3, costs $\Theta(n)$ time: one quaternion product and one logarithm per step, and $\Theta(n)$ space for the $\omega_k$.
A query costs $\Theta(1)$: three exponentials and three quaternion products.
The body angular velocity costs about as much more, with the closed form of the Properties section.

## Properties

- **$C^2$ continuity.** The curve, its velocity and its acceleration are continuous on $[0, n - 3]$.
- **Simple derivatives.** With $A_k = \exp(\tilde B_k\omega_{j+k})$, $q' = q_j(A_1' A_2 A_3 + A_1 A_2' A_3 + A_1 A_2 A_3')$ and $A_k' = A_k\,\omega_{j+k}\tilde B_k'$. So the body angular velocity $2\,q^* q'$ is $2(A_3^* A_2^* \tilde B_1'\omega_{j+1} A_2 A_3 + A_3^* \tilde B_2'\omega_{j+2} A_3 + \tilde B_3'\omega_{j+3})$.
- **Approximation, not interpolation.** At the joint $u = 0$ of segment $j$, the curve is $q_j\exp(\frac56\omega_{j+1})\exp(\frac16\omega_{j+2})$, not $q_{j+1}$. For rotations about one axis the angle there is $\frac16(\theta_j + 4\theta_{j+1} + \theta_{j+2})$, as for the scalar B-spline.
- **Local control.** Segment $j$ depends on $q_j, \dots, q_{j+3}$ only, so moving one control quaternion changes four segments.
- **Independence of frames.** For unit quaternions $a$ and $b$, the control quaternions $a\,q_k\,b$ give the curve $a\,q(t)\,b$.
- **One axis.** For rotations about one fixed axis, the curve is the uniform cubic B-spline of the rotation angles.
- **No symmetry under reversal.** Reversing the order of the control quaternions does not give the same curve run backwards, because the products do not commute. In tests with random keys up to two radians apart, the difference is a few thousandths.

## Variants and improvements

- **Other bases.** The construction works for any basis in cumulative form. Kim, Kim and Shin also give quaternion Bezier and Hermite curves this way, with the Bernstein basis of the [Bezier curve](/bezier-curve/).
- **Interpolating curves.** To pass through given keys, solve for control quaternions whose curve meets the keys at the joints. Kim, Kim and Shin treated this problem in a second paper of 1995. The equations are nonlinear, because the products do not commute.
- **Nonuniform knots.** Use the cumulative basis of a nonuniform B-spline for keys at uneven times. The curve is still $C^2$.
- **Squad and spherical Bezier curves.** [Squad](/squad/) and the spherical Bezier curves of Shoemake interpolate the keys and are cheaper to set up, but they are only $C^1$, and their derivatives have no simple form.

## When to use it

Use the cumulative B-spline curve when a smooth angular acceleration matters more than hitting each key exactly: a camera that must not shake, a vehicle or a body in a physics-based animation, or a smooth target for a controller that uses the angular acceleration.
It is also a good model of a smooth rotation trajectory to fit to noisy orientation data, because the derivatives are cheap.
If the keys must be hit, use [squad](/squad/) or an interpolating variant.

## Pitfalls

- **Inconsistent signs.** Without lines L1 and L2, a step between two close rotations can have a quaternion angle above $\pi/2$, and the curve turns the long way.
- **Steps of a half turn.** If two adjacent control quaternions differ by a rotation of $\pi$, the logarithm in line L3 has no unique axis.
- **The order of the factors.** The factors of line L7 do not commute. Changing their order, or writing the product in the other order, gives a different curve that is no longer the cumulative form.
- **Treating it as an interpolant.** The control quaternions are not on the curve. An animator who sets keys and expects the curve to pass through them will see an offset at each key.
- **Euler angles.** A B-spline on [Euler angles](/euler-angles/) is also $C^2$, but it depends on the angle order and fails near gimbal lock.

## Implementations

## History

Shoemake (1985) brought quaternion curves to animation with slerp and spherical Bezier curves.
Kim, Kim and Shin (1995) observed that the cumulative form of a spline turns into a unit quaternion curve when each difference becomes a power of a relative rotation.
They gave the construction for the B-spline, Bezier and Hermite bases, and showed that the derivatives of the curves have simple forms.
The cumulative B-spline curve is now also used for continuous-time trajectories of cameras and inertial sensors.

## References
