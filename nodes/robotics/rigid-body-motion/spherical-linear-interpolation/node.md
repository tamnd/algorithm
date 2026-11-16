---
tag: BJ0DKQ
kind: algorithm
slug: spherical-linear-interpolation
name: Spherical linear interpolation
aliases:
- slerp
- quaternion slerp
area: robotics/rigid-body-motion
level: core
summary: Interpolates two unit quaternions along the shorter great arc between them, which turns a body about one fixed axis at constant angular speed from the first orientation to the second.
model: real-ram
complexity:
  vars: {n: "the number of quaternion components, fixed at n = 4"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [unit-quaternion-rotation, axis-angle-representation]
see_also: [shepperd-method, so3-logarithm-map, quaternion-kinematic-equation, dual-quaternion, bezier-curve, time-scaling, rotation-averaging, euler-angles]
sources:
  - paper: doi:10.1145/325165.325242
    title: Ken Shoemake, Animating rotation with quaternion curves, Computer Graphics (Proceedings of SIGGRAPH 1985) 19(3), 245-254, 1985
    locator: the whole paper (the slerp formula, the comparison with Euler angle interpolation, and quaternion Bezier curves built from slerp)
  - paper: arxiv:1711.02508
    title: Joan Sola, Quaternion kinematics for the error-state Kalman filter, 2017
    locator: "Section 2.7 (spherical linear interpolation, equation 127: q(t) = q0 (q0* q1)^t, and the form on the 4D arc)"
---

Spherical linear interpolation, or slerp, takes two [unit quaternions](/unit-quaternion-rotation/) $q_0$ and $q_1$ and a number $t \in [0, 1]$, and returns the point at the fraction $t$ of the great arc from $q_0$ to $q_1$ on the unit sphere of $\mathbb{R}^4$:

$$\operatorname{slerp}(q_0, q_1, t) = \frac{\sin((1 - t)\Omega)}{\sin\Omega}\, q_0 + \frac{\sin(t\Omega)}{\sin\Omega}\, q_1 = q_0\,(q_0^* q_1)^t,$$

where $\Omega$ is the angle between $q_0$ and $q_1$ as vectors of $\mathbb{R}^4$.
As rotations, the result turns the body from the first orientation to the second about one fixed axis at a constant angular speed.
Shoemake brought the method to computer animation in 1985, and it is the standard way to interpolate orientations in graphics and robotics.

## In plain words

You have two orientations of a body and you want the ones in between.
A unit quaternion is a point on a sphere in four dimensions, and each orientation is such a point.
Slerp walks along the shortest circle on that sphere from the first point to the second, at a steady pace.
For the body, this means one steady turn about one fixed line.
Each orientation has two points on the sphere, opposite to each other.
If you pick the wrong one, the body turns the long way round, so slerp first picks the point that is nearer.
When the two points are almost equal, a plain straight line between them, pushed back onto the sphere, is as good and avoids a division by zero.

## The problem

The input is two unit quaternions $q_0$ and $q_1$, in the Hamilton convention with the scalar first, and a number $t$, usually in $[0, 1]$.
They stand for the rotations $R_0$ and $R_1$, with $R(q)\,v$ equal to the vector part of $q\,(0, v)\,q^*$.
The output is a unit quaternion $q(t)$ such that $q(0) = q_0$, $q(1) = \pm q_1$, and

$$R(q(t)) = R_0\, e^{t\,[w]}, \qquad w = \log(R_0^{\mathsf T} R_1),$$

where $\log$ is the [logarithm map of SO(3)](/so3-logarithm-map/) with $|w| \le \pi$.
So $q(t)$ is the rotation $R_0$ followed by the fraction $t$ of the relative rotation $R_0^{\mathsf T} R_1$, about the axis $w/|w|$ in the frame of $R_0$.

## The algorithm

The algorithm takes the angle $\Omega$ from atan2, $\Omega = 2\operatorname{atan2}(|q_1 - q_0|, |q_1 + q_0|)$, which is accurate at every angle.
This is the angle of the isosceles triangle with sides $q_0$ and $q_1$: the chord $|q_1 - q_0| = 2\sin\frac\Omega2$ and the sum $|q_1 + q_0| = 2\cos\frac\Omega2$.
The threshold is $\delta = 10^{-6}$.

```pseudo id=main
SLERP(q₀, q₁, t)                               ▷ unit quaternions; returns the point at t on the short arc
L1  d ← q₀ · q₁                                  ▷ the dot product in R⁴, d = cos Ω
L2  if d < 0 then
L3      q₁ ← -q₁                                 ▷ the same rotation, on the near side of the sphere
L4  Ω ← 2 atan2(|q₁ - q₀|, |q₁ + q₀|)            ▷ the angle between q₀ and q₁, in [0, π/2]
L5  if Ω < δ then                                ▷ the two points almost agree
L6      q ← (1 - t) q₀ + t q₁
L7      return q / |q|
L8  a ← sin((1 - t) Ω) / sin Ω
L9  b ← sin(t Ω) / sin Ω
L10 return a q₀ + b q₁
```

Lines L1 to L3 choose the sign of $q_1$ that makes the arc short.
Line L4 computes the angle of the arc.
Lines L6 and L7 are the normalized linear interpolation, used only for tiny arcs.
Lines L8 to L10 are the slerp formula.

## Example

Interpolate from the identity $q_0 = (1, 0, 0, 0)$ to the rotation by 90 degrees about $z$, $q_1 = (0.70711, 0, 0, 0.70711)$, at $t = 0.25$.

- Line L1: $d = 0.70711 \ge 0$, so line L3 is not used.
- Line L4: $|q_1 - q_0| = 0.76537$ and $|q_1 + q_0| = 1.84776$, so $\Omega = 2\operatorname{atan2}(0.76537, 1.84776) = 0.78540 = \pi/4$.
- Lines L8 and L9: $a = \sin(3\pi/16)/\sin(\pi/4) = 0.78569$ and $b = \sin(\pi/16)/\sin(\pi/4) = 0.27590$.
- Line L10: $q = 0.78569\,(1, 0, 0, 0) + 0.27590\,(0.70711, 0, 0, 0.70711) = (0.98079, 0, 0, 0.19509)$.

This is $(\cos 11.25°, 0, 0, \sin 11.25°)$, the rotation by 22.5 degrees about $z$, which is one quarter of 90 degrees, as it must be.
The normalized linear interpolation of lines L6 and L7 at the same $t$ gives $(0.98229, 0, 0, 0.18737)$, the rotation by 21.598 degrees, so it does not move at a constant speed.

The sign test matters for rotations that are near each other but have quaternions far apart.
Take the rotations by 170 degrees and by $-170$ degrees about $z$, with $q_0 = (0.08716, 0, 0, 0.99619)$ and $q_1 = (0.08716, 0, 0, -0.99619)$.
The two rotations differ by only 20 degrees, but $d = \cos 170° = -0.98481$.
Without line L3, the midpoint would be proportional to $q_0 + q_1 = (0.17431, 0, 0, 0)$, which is the identity: the body would turn back through 0 degrees, the long way of 340 degrees.
With line L3, $q_1$ becomes $(-0.08716, 0, 0, 0.99619)$, $\Omega = 10$ degrees, and the midpoint is $(0, 0, 0, 1)$, the rotation by 180 degrees, halfway along the short way.

As a check with the matrix form, the midpoint between the identity and $q_1 = (0.5, 0.5, 0.5, 0.5)$, the rotation by $2\pi/3$ about $(1, 1, 1)/\sqrt3$, is $(0.86603, 0.28868, 0.28868, 0.28868)$.
Its logarithm is $(0.60460, 0.60460, 0.60460)$, the rotation by $\pi/3$ about the same axis.

## Correctness

After lines L1 to L3, $q_0 \cdot q_1 \ge 0$, so $\Omega \in [0, \pi/2]$, and the relative rotation $q_0^* q_1 = (\cos\Omega, \sin\Omega\,\hat u)$ turns by the angle $2\Omega \le \pi$ about the unit axis $\hat u$.
Write $q_1 = \cos\Omega\, q_0 + \sin\Omega\, p$, where $p$ is a unit vector of $\mathbb{R}^4$ orthogonal to $q_0$.
Then the great arc is $\cos(t\Omega)\, q_0 + \sin(t\Omega)\, p$, and substituting $p$ gives the formula of lines L8 to L10.
Left multiplication by $q_0$ is an isometry of $\mathbb{R}^4$ that maps $1$ to $q_0$ and $q_0^* q_1$ to $q_1$, so the arc is also $q_0 (\cos(t\Omega) + \sin(t\Omega)\,\hat u) = q_0 (q_0^* q_1)^t$.
The factor $(q_0^* q_1)^t$ is the rotation by $2t\Omega$ about $\hat u$, which is $e^{t[w]}$ with $w = 2\Omega\hat u = \log(R_0^{\mathsf T} R_1)$.
For $\Omega < \delta$, the normalized linear interpolation lies on the same arc, and its angle differs from $t\Omega$ by at most about $0.016\,\Omega^3$, which is below $2 \cdot 10^{-20}$.
The [proof](proofs/correctness.md) gives the details.

## Complexity

One call takes $\Theta(1)$ time and space in the real RAM: one dot product, two norms of 4-vectors, one atan2, three sines and about 30 additions and multiplications.
To evaluate many values of $t$ for the same pair, compute lines L1 to L4 and $\sin\Omega$ once; each further point then costs two sines and 8 multiplications.

## Properties

- **Constant angular speed.** The arc angle grows linearly in $t$, so the body turns at the constant rate $2\Omega$ per unit of $t$ about a fixed axis. Since $R(t) = R_0 e^{t[w]}$ and $e^{t[w]} w = w$, both the body and the space [angular velocity](/angular-velocity/) are constant, equal to $w$ and $R_0 w$.
- **Shortest path.** The curve is a geodesic of SO(3) with its usual metric, the one that measures the angle of $R_a^{\mathsf T} R_b$. After the sign test, it is the shortest such path between the two rotations, of length $2\Omega \le \pi$.
- **Symmetry.** $\operatorname{slerp}(q_0, q_1, t) = \operatorname{slerp}(q_1, q_0, 1 - t)$, up to the sign that line L3 chooses.
- **Independence of frames.** For unit quaternions $a$ and $b$, $\operatorname{slerp}(a q_0 b, a q_1 b, t) = a\, \operatorname{slerp}(q_0, q_1, t)\, b$. So the path does not depend on the choice of the world frame or of the body frame.
- **Unit length.** The output has length 1 in exact arithmetic. In floating point its length is within a few units of the roundoff of 1.
- **Only two points.** Slerp of a sequence of keyframes, one segment at a time, has a jump in the angular velocity at each key. The curve is continuous, but not smooth.

## Variants and improvements

- **Normalized linear interpolation (nlerp).** Lines L6 and L7 alone. The path is the same arc, but the speed is not constant; the angle error at $t = 0.2113$ is about $0.016\,\Omega^3$. Nlerp is cheaper and is commutative when blending several rotations with weights.
- **The matrix form.** $R_0\, e^{t \log(R_0^{\mathsf T} R_1)}$ with Rodrigues' formula and the [logarithm map](/so3-logarithm-map/) gives the same rotations without quaternions. It costs more, and it needs care near the angle $\pi$.
- **Curves through many keys.** Shoemake built Bezier curves on the sphere by the de Casteljau construction of a [Bezier curve](/bezier-curve/), with slerp in place of the linear interpolation. Spline schemes of this kind give a smooth angular velocity at the keys.
- **Rigid motions.** Screw linear interpolation does the same for a rotation and a translation together with a [dual quaternion](/dual-quaternion/), and moves along a screw axis.
- **Time scaling.** To start and stop with zero angular speed, replace $t$ by a [time scaling](/time-scaling/) $s(t)$, such as the cubic $3t^2 - 2t^3$. The axis stays fixed and only the speed along the arc changes.

## When to use it

Use slerp to move a body or a camera between two orientations: keyframe animation, the orientation part of a straight-line motion of an end effector, and the interpolation of a measured attitude between two time stamps of a sensor.
It also gives the midpoint of two rotations, which is the simplest case of [rotation averaging](/rotation-averaging/).
Convert the end orientations from matrices with [Shepperd's method](/shepperd-method/).
To follow a measured angular velocity instead of a fixed end point, integrate the [quaternion kinematic equation](/quaternion-kinematic-equation/).

## Pitfalls

- **The long way round.** Without the sign test of line L2, two close rotations can have quaternions with a negative dot product, and the body then turns by up to 360 degrees minus the right angle.
- **arccos of the dot product.** $\Omega = \arccos d$ loses about half of the digits when $d$ is close to 1, so a tiny arc gets an angle error of about $10^{-8}$. The atan2 form of line L4 avoids this.
- **Division by $\sin\Omega$.** At $\Omega = 0$ the formula is $0/0$. Use the linear branch below a small threshold.
- **Interpolating Euler angles.** Linear interpolation of [Euler angles](/euler-angles/) or [roll-pitch-yaw angles](/roll-pitch-yaw-angles/) gives a path that changes its axis, depends on the angle convention, and can swing wildly near [gimbal lock](/gimbal-lock/).
- **Mixed conventions.** Lines L8 to L10 use only sums and dot products in $\mathbb{R}^4$, so they work in the JPL convention (scalar last, $ij = -k$) as well. The power form $q_0 (q_0^* q_1)^t$ and the conversion to a matrix use the quaternion product, which differs between the conventions. Do not mix the two in one computation.
- **Angles of half a turn.** If the two rotations differ by exactly $\pi$, the two short paths in opposite directions have the same length, and a small change of the input switches between them.

## Implementations

## History

Shoemake (1985) introduced slerp to computer animation in his SIGGRAPH paper on quaternion curves.
He compared it with the interpolation of Euler angles, and built smooth curves through many keyframes with slerp in a Bezier construction.
The formula for a point on a great arc is older and comes from spherical geometry.
Sola (2017) gives the equivalent forms $q_0 (q_0^* q_1)^t$ and the form on the arc in $\mathbb{R}^4$ in the Hamilton convention.

## References
