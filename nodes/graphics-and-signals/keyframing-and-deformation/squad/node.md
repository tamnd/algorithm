---
tag: 5MKSXN
kind: algorithm
slug: squad
name: Spherical quadrangle interpolation
aliases:
- squad
- Shoemake quaternion spline
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Interpolates a sequence of unit quaternions with a C1 curve made of three nested slerps per segment, the spherical form of a cubic curve built by the quadrangle construction.
model: real-ram
complexity:
  vars: {n: "the number of keys"}
  time: {build: "Θ(n)", query: "Θ(1)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [keyframe-interpolation, spherical-linear-interpolation, unit-quaternion-rotation]
see_also: [cumulative-b-spline-quaternion-curve, so3-logarithm-map, catmull-rom-spline, bezier-curve, de-casteljau-algorithm, angular-velocity, dual-quaternion-skinning, euler-angles]
sources:
  - paper: doi:10.1145/325165.325242
    title: Ken Shoemake, Animating rotation with quaternion curves, Computer Graphics (Proceedings of SIGGRAPH 1985) 19(3), 245-254, 1985
    locator: the whole paper (slerp, and spherical Bezier curves through quaternion keys built from slerp)
  - url: http://web.mit.edu/2.998/www/QuaternionReport1.pdf
    title: Erik B. Dam, Martin Koch and Martin Lillholm, Quaternions, interpolation and animation, Technical Report DIKU-TR-98/5, University of Copenhagen, 1998
    locator: "Section 6.2.1 (Squad, Definition 17, equations 6.14 and 6.15) and Proposition 30 (Squad is C1)"
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: "Chapter 3, Section 3.3 (interpolation of orientations)"
---

Spherical quadrangle interpolation, or squad, makes a smooth curve of unit quaternions through a sequence of key orientations $q_0, \dots, q_{n-1}$.
On the segment from $q_i$ to $q_{i+1}$ it nests three [slerps](/spherical-linear-interpolation/):

$$\operatorname{squad}(q_i, q_{i+1}, s_i, s_{i+1}, t) = \operatorname{slerp}\bigl(\operatorname{slerp}(q_i, q_{i+1}, t),\ \operatorname{slerp}(s_i, s_{i+1}, t),\ 2t(1 - t)\bigr),$$

with the inner control points $s_i = q_i \exp\bigl(-\tfrac14(\log(q_i^{-1} q_{i+1}) + \log(q_i^{-1} q_{i-1}))\bigr)$.
The curve passes through the keys, and with these control points its first derivative is continuous at each key.
Shoemake gave the method in his 1987 course notes, and it is a common way to interpolate orientation keys in animation systems.

## In plain words

Slerp turns a body from one key orientation to the next at a steady rate about one fixed axis.
If you chain slerps through many keys, the body changes its spin with a jerk at each key.
Squad smooths these jerks.
For each key it makes one extra helper orientation, which looks at the key before and the key after.
Inside a segment it blends two slerps: one between the keys, and one between the helpers.
At the two ends of the segment the blend uses only the keys, so the curve still goes through them.
In the middle the helpers bend the path, so that the spin at each key is the same when you arrive and when you leave.

## The problem

The input is a sequence of unit quaternions $q_0, \dots, q_{n-1}$, $n \ge 2$, in the Hamilton convention with the scalar first, at the times $0, 1, \dots, n - 1$.
They stand for the key orientations of a body, as in [keyframe interpolation](/keyframe-interpolation/).
The output is a curve $q(u)$ of unit quaternions, $u \in [0, n - 1]$, with $q(i) = q_i$ for each key, and with a continuous first derivative $q'(u)$, so that the [angular velocity](/angular-velocity/) of the body is continuous.

The quaternion logarithm of a unit quaternion $(\cos\varphi, \sin\varphi\,\hat u)$, $\varphi \in [0, \pi]$, is the pure quaternion $(0, \varphi\,\hat u)$, and $\exp$ is its inverse.
For unit quaternions $q^{-1} = q^*$.
On a unit quaternion the logarithm is the half of the rotation vector, so it is the [SO(3) logarithm](/so3-logarithm-map/) divided by 2.
Write $\operatorname{arc}(p, q, t) = p \exp(t \log(p^* q))$.
This is slerp from $p$ to $q$ without the sign test, and it is equal to slerp when $p \cdot q \ge 0$.

## The algorithm

The build step makes the key signs consistent and computes the control points.
The query step evaluates one segment at a local time $t \in [0, 1]$; for the global time $u$, use $i = \lfloor u \rfloor$ and $t = u - i$.

```pseudo id=main
SQUAD(q₀, ..., qₙ₋₁; i, t)                          ▷ unit quaternions; returns the point at time i + t
L1  for k ← 1 to n - 1: if qₖ₋₁ · qₖ < 0 then
L2      qₖ ← -qₖ                                     ▷ the same rotation, near the previous key
L3  s₀ ← q₀; sₙ₋₁ ← qₙ₋₁                             ▷ the end keys are their own control points
L4  for k ← 1 to n - 2 do
L5      a ← log(qₖ* qₖ₊₁)                            ▷ half the rotation vector to the next key
L6      b ← log(qₖ* qₖ₋₁)                            ▷ half the rotation vector to the previous key
L7      sₖ ← qₖ exp(-(a + b) / 4)
L8  A ← arc(qᵢ, qᵢ₊₁, t)                              ▷ the slerp of the keys
L9  B ← arc(sᵢ, sᵢ₊₁, t)                              ▷ the slerp of the control points
L10 return arc(A, B, 2t(1 - t))
```

Lines L1 and L2 replace a key by its negative when it is far from the previous one on the unit sphere, so each step between keys is the short way.
Lines L3 to L7 compute the control points; they run once for the whole sequence.
Lines L8 to L10 are the query.
The weight $2t(1 - t)$ is 0 at both ends of the segment, so $q(i) = q_i$, and it is at most $\frac12$ in the middle, so the curve never reaches the control points.

## Example

Take three keys: $q_0 = (1, 0, 0, 0)$, the identity; $q_1 = (0.70711, 0, 0, 0.70711)$, the rotation by 90 degrees about $z$; and $q_2 = q_1 \cdot (0.70711, 0.70711, 0, 0) = (0.5, 0.5, 0.5, 0.5)$, a further turn by 90 degrees about the $x$ axis of the body.

- Lines L1 and L2: $q_0 \cdot q_1 = 0.70711$ and $q_1 \cdot q_2 = 0.70711$, so no key changes sign.
- Line L3: $s_0 = q_0$ and $s_2 = q_2$.
- Lines L5 and L6 at $k = 1$: $a = (0, 0.7854, 0, 0)$, half of the turn about $x$, and $b = (0, 0, 0, -0.7854)$, half of the turn back about $z$.
- Line L7: $-(a + b)/4 = (0, -0.19635, 0, 0.19635)$, so $s_1 = (0.54296, -0.13706, -0.13706, 0.81708)$.
- Lines L8 to L10 at $i = 0$, $t = 0.5$: $q(0.5) = (0.90349, -0.03911, -0.03911, 0.42503)$, a rotation by 0.88591 radians. Plain slerp gives $(0.92388, 0, 0, 0.38268)$, a rotation by $\pi/4$ about $z$.
- At $i = 1$, $t = 0.5$: $q(1.5) = (0.62514, 0.23923, 0.23923, 0.70337)$, a rotation by 1.79096 radians. Plain slerp gives $(0.65328, 0.27060, 0.27060, 0.65328)$.

The body angular velocity at the key $q_1$ shows the difference.
With slerp per segment it jumps from $(0, 0, 1.5708)$ before the key to $(1.5708, 0, 0)$ after it.
With squad it is $(0.7854, 0, 0.7854)$ from both sides, which is the vector part of $a - b$.

## Correctness

The weight $2t(1 - t)$ vanishes at $t = 0$ and $t = 1$, and $\operatorname{arc}(A, B, 0) = A$, so the segment starts at $q_i$ and ends at $q_{i+1}$.
Each arc is a product of unit quaternions, so the result has length 1.

For the first derivative, use $\frac{\partial}{\partial w}\operatorname{arc}(A, B, w) = A\log(A^* B)$ at $w = 0$, where the derivative with respect to $B$ vanishes.
At $t = 0$ the weight has derivative 2 and $A^* B = q_i^* s_i = \exp(-(a + b)/4)$, so

$$q'(i^+) = q_i a + 2 q_i \cdot \left(-\tfrac{a + b}{4}\right) = q_i\,\frac{a - b}{2}.$$

At $t = 1$ of the segment before, the inner slerp arrives with the derivative $q_i \log(q_{i-1}^* q_i) = -q_i b$, the weight has derivative $-2$, and again $A^* B = q_i^* s_i$, so $q'(i^-) = -q_i b + q_i\frac{a + b}{2} = q_i\frac{a - b}{2}$.
The two sides agree, so the curve is $C^1$ at every inner key.
In flat space the same construction gives the tangent $\frac12(q_{i+1} - q_{i-1})$, which is the tangent of the [Catmull-Rom spline](/catmull-rom-spline/).
The [proof](proofs/correctness.md) gives the details.

## Complexity

The build step, lines L1 to L7, takes $\Theta(n)$ time: two logarithms, one exponential and three quaternion products per inner key.
It stores the $n$ control points, $\Theta(n)$ extra space.
One query takes $\Theta(1)$ time: three arcs, each with one logarithm, one exponential and two products.
If the keys are at uneven times, finding the segment of a time $u$ takes $O(\log n)$ by [binary search](/binary-search/).

## Properties

- **Interpolation.** The curve passes through every key, $q(i) = q_i$, up to the sign that line L2 chooses.
- **First derivative continuous.** With keys at equal time steps, the curve is $C^1$ and the body angular velocity at key $i$ is the vector part of $a - b$ from both sides.
- **Not $C^2$.** The second derivative jumps at the keys in general. In the example the one-sided second differences at $q_1$ differ in each component.
- **Two keys give slerp.** For $n = 2$, $s_0 = q_0$ and $s_1 = q_1$, so lines L8 and L9 give the same point and the curve is the slerp.
- **Keys about one axis.** If all keys are rotations about one fixed axis with equal angle steps, then $a + b = 0$, $s_k = q_k$, and the curve is slerp at constant speed.
- **Independence of frames.** For unit quaternions $c$ and $d$, the keys $c\,q_k\,d$ give the curve $c\,q(u)\,d$. So the curve does not depend on the world frame or the body frame.
- **Local control.** The control point $s_k$ depends on the keys $k - 1$, $k$ and $k + 1$, so moving one key changes at most four segments.
- **Not the shortest path.** Between keys the curve bends away from the great arc, as the example shows. It does not minimize any energy, and the angular speed is not constant.

## Variants and improvements

- **Spherical Bezier curves.** Shoemake (1985) built cubic Bezier curves on the sphere with the [de Casteljau algorithm](/de-casteljau-algorithm/), with slerp in place of linear interpolation. It needs six slerps per point. Squad uses three, and in flat space its quadrangle form is the cubic [Bezier curve](/bezier-curve/) with the control points $q_i$, $\frac13(2s_i + q_{i+1})$, $\frac13(2s_{i+1} + q_i)$ and $q_{i+1}$.
- **Uneven key times.** If segment $i$ has the duration $h_i$, the time derivative of the curve is $q_i\frac{a - b}{2h_i}$ on the right of key $i$ and $q_i\frac{a - b}{2h_{i-1}}$ on the left. The axis of the angular velocity stays continuous, but its size jumps. To remove the jump, use $e = -(h_{i-1} a + h_i b) / (2(h_{i-1} + h_i))$ in line L7. Then both sides have the derivative $q_i (a - b)/(h_{i-1} + h_i)$, by the computation of the Correctness section.
- **Tension, continuity and bias.** The control point can use the [Kochanek-Bartels](/kochanek-bartels-spline/) weights on $a$ and $b$, as in the scalar case.
- **Cumulative B-spline curves.** The [cumulative B-spline quaternion curve](/cumulative-b-spline-quaternion-curve/) of Kim, Kim and Shin is $C^2$ and has simple closed forms for its derivatives, but it does not pass through the keys.
- **Rigid motions.** For a rotation with a translation, interpolate the translation with a scalar spline, or use [dual quaternions](/dual-quaternion/), as in [dual quaternion skinning](/dual-quaternion-skinning/) for blends of joint transforms.

## When to use it

Use squad for camera and joint orientations in keyframe animation when the keys must be hit exactly and the turning must have no jerk at the keys.
It is cheap to evaluate, so it suits games and real-time playback.
If the keys are only guides and a smoother angular acceleration matters more, use the cumulative B-spline curve.
For two keys only, use [slerp](/spherical-linear-interpolation/).

## Pitfalls

- **Inconsistent signs.** Without lines L1 and L2, the logarithms in lines L5 and L6 measure the long way between two keys, and the body turns by nearly a full turn.
- **Sign tests inside the query.** Lines L8 to L10 must not flip the sign of $B$ when $A \cdot B < 0$. A flip changes the result, and the curve then jumps at the time where $A \cdot B$ crosses 0.
- **Euler angles.** Splines on [Euler angles](/euler-angles/) per channel depend on the angle order and fail near [gimbal lock](/gimbal-lock/). Squad works on the rotations themselves.
- **Speed.** The parameter is not the angle. The angular speed varies inside a segment, so a constant speed needs a reparametrization.
- **Logarithm near the angle $\pi$.** If two adjacent keys differ by a half turn, their logarithm has no unique axis, and a small change of a key switches the path.

## Implementations

## History

Shoemake (1985) brought quaternions and slerp to computer animation and built spherical Bezier curves through keys.
He gave squad in the course notes "Quaternion calculus and fast animation" of SIGGRAPH 1987, as a cheaper form of the same idea.
Dam, Koch and Lillholm (1998) wrote out the construction, proved that squad is $C^1$, and noted that the first published proof was flawed.
Parent (2012) describes squad and other orientation curves in his textbook on computer animation.

## References
