---
tag: C2728X
kind: algorithm
slug: conservative-advancement
name: Conservative advancement
aliases:
- conservative advancement CCD
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Advance time by the distance between two bodies divided by a bound on their approaching speed, repeating until they touch or the step ends.
solves: [continuous-collision-detection]
model: floating-point-model
complexity:
  vars: {s: the number of steps, D: the cost of one distance query, T: the length of the time interval, L: a bound on the relative speed of all points, e: the distance tolerance}
  time: {call: O(s D), step: O(D), steps_worst: O(T L / e)}
  space: {extra: O(1)}
properties: {deterministic: true, online: false, recursive: false, exact: false}
history:
  year: 1996
  people: [Brian Mirtich]
  note: Mirtich used conservative advancement in his impulse-based rigid body simulator to find the time of the next collision, with distances from his closest-feature code and a bound on the speed of the closest points.
prereqs: [continuous-collision-detection, convex-collision-detection, floating-point-model]
see_also: [elementary-ccd-tests, gjk-algorithm, lin-canny-closest-features, v-clip, expanding-polytope-algorithm, sweep-and-prune, bisection-method, collision-impulse]
sources:
  - paper: doi:10.1109/ROBOT.2009.5152234
    title: Min Tang, Young J. Kim and Dinesh Manocha, C2A, controlled conservative advancement for continuous collision detection of polygonal models, Proceedings of the 2009 IEEE International Conference on Robotics and Automation
    locator: the description of conservative advancement for rigid motion, the bound on the motion of the closest points, and the controlled variant
  - paper: doi:10.1145/285857.285860
    title: Brian Mirtich, V-Clip, fast and robust polyhedral collision detection, ACM Transactions on Graphics 17(3), 1998, 177 to 208
    locator: the closest features and distances that a time of impact loop of this kind uses
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 5, Basic Primitive Tests (the dynamic intersection tests of moving objects)
---

Conservative advancement is a method for [continuous collision detection](/continuous-collision-detection/) of two convex bodies that move during a time step. It computes the distance $d$ between the bodies at the current time, and a bound $\mu$ on the speed at which any point of one body can approach the other. The bodies cannot touch before $d / \mu$ has passed, so the method moves the time forward by that amount and repeats. It stops when the distance is below a tolerance, which gives a time of impact from below, or when the time passes the end of the step. The method never steps past the first contact. It needs only a distance query, so it works for any convex shapes with a [GJK](/gjk-algorithm/) or a [closest-feature](/v-clip/) distance, and for any motion with a known speed bound.

## In plain words

Two objects move during a short time. You want the first moment they touch.

Measure the gap between them now. You also know the fastest speed at which they can come together: the speed of the motion toward each other, plus the speed of the spin at the outer edge. In the time that it takes to close the gap at that top speed, they cannot touch. So you can jump that far ahead in time with no risk.

At the new time, measure the gap again and jump again. Each jump is safe. When the gap is tiny, report the time as the time of contact. If the time goes past the end of the step, they do not touch in this step.

## The problem

The input is two convex polygons $A$ and $B$ with their vertices in local coordinates around their centers of rotation, a start pose, a constant velocity $v$ and a constant angular velocity $\omega$ for each, an interval $[0, T]$ and a tolerance $\mathrm{tol} > 0$. A local point $p$ of $A$ is at $c_A + v_A t + R(\theta_A + \omega_A t)\, p$ at time $t$. The output is a time $t$ with $d(t) \le \mathrm{tol}$ that is not later than the first contact, or NO-CONTACT if the bodies do not touch in $[0, T]$. The 2D form on this page has the same structure as the 3D form, where $\omega$ is a vector and the rotation part of the bound is $|\omega| r$ in the same way.

## The algorithm

```pseudo id=main
CONSERVATIVE-ADVANCEMENT(A, B, T, tol)
L1  t ← 0
L2  loop
L3      (d, pA, pB) ← DISTANCE(A(t), B(t))
L4      if d ≤ tol then return t
L5      n ← (pA - pB) / d
L6      μ ← -n · (vA - vB) + |ωA| rA + |ωB| rB
L7      if μ ≤ 0 then return NO-CONTACT
L8      t ← t + d / μ
L9      if t > T then return NO-CONTACT
```

Here $r_A$ is the largest distance of a vertex of $A$ from its center of rotation. The first term of $\mu$ is the speed of the translation along the closest direction $n$, which is negative when the bodies move apart. The other terms bound the speed of any point that the rotation moves. The line through $p_B$ with normal $n$ separates the bodies at time $t$, and $\mu$ bounds how fast the gap along $n$ can close, so the gap stays positive until $t + d/\mu$. The implementation uses a brute force distance over all vertex-edge pairs. A real system uses GJK or a closest-feature walk, started from the result of the previous step.

## Example

$A$ is the square with corners $(\pm 1, \pm 1)$, at rest. $B$ is the same square, with its center at $(6, 0)$, the velocity $(-6, 0)$ and the angular velocity $\pi$ per unit of time. So $r_B = \sqrt{2}$, and the rotation adds $\pi \sqrt{2} \approx 4.443$ to the bound. Take $T = 1$ and $\mathrm{tol} = 10^{-3}$.

At $t = 0$ the gap is $d = 4$, between the right side of $A$ and the left side of $B$, and $n = (-1, 0)$. The bound is $\mu = 6 + 4.443 = 10.443$, so the first step is $4 / 10.443 \approx 0.3830$. The direction $n$ stays $(-1, 0)$ in all steps of this example, because the closest feature of $A$ stays its right side.

| step | t | d | d / μ |
|---|---|---|---|
| 0 | 0 | 4 | 0.383036 |
| 1 | 0.383036 | 1.409299 | 0.134953 |
| 2 | 0.517989 | 0.837178 | 0.080167 |
| 3 | 0.598156 | 0.154728 | 0.014817 |
| 4 | 0.612973 | 0.036975 | 0.003541 |
| 5 | 0.616514 | 0.009246 | 0.000885 |
| 6 | 0.617399 | 0.002337 | 0.000224 |
| 7 | 0.617623 | 0.000592 | |

At step 7 the gap is below the tolerance, and the method returns $t \approx 0.617623$. Dense sampling and bisection give the first contact $t^* \approx 0.617699$, when a corner of $B$, turned by about $111$ degrees, hits the right side of $A$. The answer is before $t^*$, as it must be. Near the contact the gap shrinks by a factor of about 4 per step, because the true speed of the corner is about three quarters of the bound. With $\mathrm{tol} = 10^{-2}$, $10^{-4}$, $10^{-6}$ and $10^{-8}$, the method took 5, 9, 12 and 16 steps.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). At time $t_0$ the line through the closest point of $B$ with normal $n$ separates the convex bodies with the gap $d_0$. A point of $A$ moves along $n$ by at least $h\, n \cdot v_A - h\,|\omega_A|\, r_A$ in the time $h$, because a rotation moves a point at the radius $|p|$ by a chord, which is at most the arc $|\omega| h |p|$. The same holds for $B$. So every pair of points is at least $d_0 - h \mu$ apart, and the bodies cannot touch before $h = d_0 / \mu$. By induction, no time of the loop passes the first contact $t^*$, and a NO-CONTACT answer is right. Each step that does not stop is longer than $\mathrm{tol} / L$, where $L$ bounds $\mu$, so the loop stops.

## Complexity

Each step costs one distance query, $O(D)$. With GJK on convex polytopes this is linear in the number of vertices, or close to $O(1)$ with a closest-feature walk under coherent motion. The number of steps $s$ has no bound that is independent of the input. The proof gives $s \le \lceil T L / \mathrm{tol} \rceil + 1$. For a head-on approach without rotation, $\mu$ is exact and one step reaches the contact. For a contact at a clear angle, the gap shrinks by a constant factor per step, as in the example, and $s$ grows like $\log(1/\mathrm{tol})$. This is observed, not proved. For a grazing motion, the gap stays small but positive and each step is short. In the tests of this page, a spinning square that passes another square with the smallest gap $g$ took 3, 9, 39 and 152 steps for $g = 1$, $0.1$, $0.01$ and $0.001$. The extra space is $O(1)$.

## Properties

- **Conservative.** In exact arithmetic the returned time is never after the first contact, and no contact is missed, also for fast rotation and thin objects. This is the property that discrete collision checks lack.
- **Any motion with a speed bound.** The method needs a distance and a bound on the speed of the closest points. It does not need the motion to be linear: a screw motion or a spline motion works with a matching bound.
- **Approximate.** It returns a time with a gap of at most $\mathrm{tol}$, not the exact time of contact.
- **Floating point.** The distance and $\mu$ have rounding errors. A step of $(d - \mathrm{tol}/2)/\mu$ keeps the result conservative when these errors are smaller than $\mathrm{tol}/2$.

## Variants and improvements

- **Controlled advancement (C2A).** Tang, Kim and Manocha (2009) apply the method to polygonal models with a bounding volume hierarchy, and control the size of the steps so that fewer of them are needed near the contact.
- **Nonconvex bodies.** Run the method on the pairs of convex pieces or bounding volumes, and take the smallest time. A hierarchy lets the method skip pairs whose bound already shows no contact in the step.
- **Articulated bodies.** For a chain of links, the speed bound of a link adds the bounds of its parents.
- **Exact tests for primitives.** For triangle meshes with linear vertex motion, the [elementary CCD tests](/elementary-ccd-tests/) solve a cubic for each vertex-face and edge-edge pair instead.

## When to use it

Use conservative advancement to find the time of impact of two convex rigid bodies that rotate during a step, or of objects with a good distance query and a simple speed bound. It is the usual choice when the motion has a rotation, which makes the exact contact equations nonlinear. For meshes with linear vertex motion, as in cloth, use the elementary tests. Pair it with a broad phase such as [sweep and prune](/sweep-and-prune/) over the swept bounding boxes, so that only near pairs reach the loop.

## Pitfalls

- **A bound that is too small.** If $r$ is measured from the center of mass but the body rotates about another point, or if $\omega$ is the wrong norm, $\mu$ is not a bound, and the method can step past the contact.
- **Tolerance zero.** With $\mathrm{tol} = 0$, the loop approaches the contact in ever smaller steps and does not stop. Use a positive tolerance and a limit on the steps.
- **Grazing motion.** A body that passes close to another with a spin makes many short steps. Limit the steps, and accept a conservative time if the limit is hit.
- **Penetration at the start.** If $d = 0$ at $t = 0$, the method returns 0. Separate the bodies first, for example with the [expanding polytope algorithm](/expanding-polytope-algorithm/).
- **The sign of $n$.** The normal must point from $B$ to $A$, so that the translation term is the approaching speed. With the wrong sign, the method steps too far when the bodies approach.

## Implementations

## History

Mirtich used conservative advancement in his 1996 Berkeley thesis on impulse-based simulation of rigid bodies, where it finds the time of the next collision with distances from his closest-feature code. Later work extended the method to articulated models and to nonconvex meshes, and Tang, Kim and Manocha (2009) made the controlled form C2A for general polygonal models.

## References
