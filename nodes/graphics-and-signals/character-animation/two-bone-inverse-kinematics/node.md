---
tag: 9Q6NF0
kind: algorithm
slug: two-bone-inverse-kinematics
name: Analytic two-bone inverse kinematics
aliases:
- two-bone IK
- limb IK
area: graphics-and-signals/character-animation
level: core
summary: Solves an arm or leg with two bones in closed form. The law of cosines gives the angle at the root and the bend, and a pole vector selects the plane and the side of the middle joint.
solves: [inverse-kinematics]
model: real-ram
complexity:
  time: {solve: "O(1)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
prereqs: [inverse-kinematics, forward-kinematics, character-skeleton]
see_also: [fabrik, cyclic-coordinate-descent-inverse-kinematics, jacobian-transpose-method, robot-workspace, footskate-cleanup, motion-retargeting, skeletal-animation]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 6, Inverse Kinematics (the planar two-link arm and analytic inverse kinematics)
  - book: isbn:9780124158429
    title: Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012
    locator: the chapter on kinematic linkages (inverse kinematics)
---

Analytic two-bone inverse kinematics puts the end of a limb with two bones, such as an arm (shoulder, elbow, wrist) or a leg (hip, knee, ankle), on a target point.
The three joints form a triangle with the sides $l_1$ and $l_2$ (the bones) and $d$ (the distance from the root to the target).
The law of cosines gives its angles:

$$\cos\alpha = \frac{l_1^2 + d^2 - l_2^2}{2 l_1 d}, \qquad \cos\beta = \frac{l_1^2 + l_2^2 - d^2}{2 l_1 l_2},$$

where $\alpha$ is the angle at the root between the bone and the line to the target, and $\beta$ is the inner angle at the middle joint.
The triangle can turn about the line from the root to the target, so a pole vector, a point that the animator places in front of the knee or behind the elbow, selects the plane and the side.
The answer is a closed form with a fixed cost, so it is the standard limb solver of game engines and animation rigs, used for foot planting on uneven ground, hands on props, and [footskate cleanup](/footskate-cleanup/).

## In plain words

Your arm has two bones of fixed length.
To touch a point, the shoulder, the elbow and the hand make a triangle whose three sides you know: the upper arm, the forearm, and the distance from the shoulder to the point.
A triangle with known sides has known angles, so you get the bend of the elbow and the angle at the shoulder at once, with no search.
The same triangle can still swing around the line from the shoulder to the point, so you also say where the elbow should point.
If the point is too far, the arm is stretched straight toward it.
If it is too near, the arm is folded as far as it goes.

## The problem

The input is the root position $a$, the target $t$, the bone lengths $l_1, l_2 > 0$, and a pole point $p$.
The output is the middle joint $e$ and the end $f$ with $|e - a| = l_1$ and $|f - e| = l_2$, such that $f = t$ when the target is reachable, and $e$ lies in the plane of $a$, $t$ and $p$, on the side of $p$.
The target is reachable if and only if $|l_1 - l_2| \le d \le l_1 + l_2$ for $d = |t - a|$; this is the [workspace](/robot-workspace/) of the limb.
For other targets the end goes to the reachable point nearest to $t$ on the ray from $a$ through $t$.
It is the two-link case of the [inverse kinematics](/inverse-kinematics/) problem.
The robotics pages use a world with $z$ up, and this page uses $y$ up; the method does not depend on the up axis, because the pole gives the plane.

## The algorithm

```pseudo id=main
TWO-BONE-IK(a, t, l₁, l₂, p)                          ▷ root, target, bone lengths, pole
L1  v ← t - a; d ← |v|                                ▷ fail if d = 0
L2  d ← clamp(d, |l₁ - l₂|, l₁ + l₂)                  ▷ the reachable distances
L3  x ← v / |v|                                       ▷ the unit direction to the target
L4  y ← normalize((p - a) - ((p - a) · x) x)          ▷ the pole direction, orthogonal to x
L5  cos α ← (l₁² + d² - l₂²) / (2 l₁ d); sin α ← √(1 - cos² α)
L6  e ← a + l₁ (cos α x + sin α y)                    ▷ the middle joint
L7  f ← a + d x                                       ▷ the end, on the line to the target
L8  return e, f
```

Line L2 clamps the distance, so an unreachable target still gives a valid limb.
Line L4 removes the part of the pole along $x$, so $x$ and $y$ are orthonormal and span the bending plane.
Line L5 is the law of cosines; the code computes $\sin\alpha$ by the product form of Heron's formula, which is exactly 0 for a straight limb, where $\sqrt{1 - \cos^2\alpha}$ loses half the digits.
The bend of the middle joint relative to the straight limb is $\theta_2 = \pi - \beta$.
A rig then turns each bone from its current direction to $e - a$ and to $f - e$, with [forward kinematics](/forward-kinematics/) over the [skeleton](/character-skeleton/) for the joints below.

In the plane, with the root at the origin and the joint angles of the planar 2R arm, the same triangle gives the textbook form

$$\cos\theta_2 = \frac{x^2 + y^2 - l_1^2 - l_2^2}{2 l_1 l_2}, \qquad \theta_1 = \operatorname{atan2}(y, x) - \operatorname{atan2}(l_2 \sin\theta_2,\ l_1 + l_2\cos\theta_2),$$

with $\theta_2 \ge 0$ for one elbow solution and $\theta_2 \le 0$ for the other.

## Example

Take $l_1 = l_2 = 1$, the root at the origin and the target $(1, 1, 0)$.
Then $d = \sqrt2$, $\cos\alpha = (1 + 2 - 1)/(2\sqrt2) = 1/\sqrt2$, so $\alpha = \pi/4$, and $\cos\beta = (1 + 1 - 2)/2 = 0$, so the elbow angle is $\beta = \pi/2$.

| pole $p$ | $y$ | elbow $e$ | planar angles $(\theta_1, \theta_2)$ |
|---|---|---|---|
| $(2, -1, 0)$ | $(1, -1, 0)/\sqrt2$ | $(1, 0, 0)$ | $(0, \pi/2)$ |
| $(-1, 2, 0)$ | $(-1, 1, 0)/\sqrt2$ | $(0, 1, 0)$ | $(\pi/2, -\pi/2)$ |

These are the two solutions of the 2R arm on the [inverse kinematics](/inverse-kinematics/) page.
For the target $(3, 0, 0)$, $d = 3$ is clamped to 2, $\cos\alpha = 1$, and the limb is straight: $e = (1, 0, 0)$ and $f = (2, 0, 0)$, pointing at the target.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md); they are proved properties of the closed form in exact arithmetic.
- After line L2, $d$, $l_1$ and $l_2$ satisfy the triangle inequalities, so $|\cos\alpha| \le 1$ and the triangle exists.
- $|e - a| = l_1$, because $x$ and $y$ are orthonormal.
- $|f - e| = l_2$, by the law of cosines in the triangle $a, e, f$.
- If the target is reachable, the clamp does nothing and $f = t$.
- If $d > l_1 + l_2$, then $\cos\alpha = 1$, and $e$ and $f$ lie on the ray from $a$ to $t$: the straight limb points at the target.
- $e - a$ is a combination of $x$ and $y$ with $\sin\alpha \ge 0$, so $e$ is in the plane of $a$, $t$ and $p$, on the side of $p$.

## Complexity

The method uses a fixed number of arithmetic operations and two square roots, so it costs $O(1)$ time and $O(1)$ space per limb.
A character with four limbs needs four calls per frame.

## Properties

- Closed form, deterministic, with no iteration and no convergence test.
- For a reachable target in a fixed plane there are exactly two solutions when $|l_1 - l_2| < d < l_1 + l_2$, and the pole picks one; at the two limits they merge.
- The result is continuous in the target and the pole, except where the pole lies on the line from the root to the target.
- Near full extension, $\alpha$ changes fast: $d\alpha / dd$ tends to infinity as $d$ tends to $l_1 + l_2$, so the middle joint can snap when a target moves near the limit.

## Variants and improvements

- **Longer chains.** [FABRIK](/fabrik/), [cyclic coordinate descent](/cyclic-coordinate-descent-inverse-kinematics/) and the [Jacobian transpose method](/jacobian-transpose-method/) handle chains of any length by iteration. A common rig solves a three bone leg by a two-bone solve and a fixed foot angle.
- **Soft limits.** Many rigs ease $d$ toward $l_1 + l_2$ with a smooth function to hide the snap near full extension. This is a tuning, with no source on this page.
- **Stretch.** Some rigs scale the bones when the target is out of reach, instead of the clamp of line L2.
- **Joint limits and twist.** The pole sets the plane, but not the twist of the end bone; the end orientation is set separately, for example to match the ground normal under a foot.
- **Style.** [Style based IK](/style-based-inverse-kinematics/) learns the choice among solutions from motion data.

## When to use it

Use it for any arm or leg with a hinge in the middle when the end must reach a point exactly: foot contact, hand contact, aiming, and cleanup of foot sliding.
For spines, tails, tentacles and other long chains, use an iterative solver.

## Pitfalls

- **Target at the root.** If $d = 0$, there is no direction $x$; the code raises an error. With $l_1 = l_2$ every direction is a solution.
- **Pole on the line.** If $p - a$ is parallel to $x$, line L4 divides by zero. The code then picks a fixed direction orthogonal to $x$; a rig should keep the pole away from the line.
- **Clamping only $\cos\alpha$.** Clamping the cosine to $[-1, 1]$ without clamping $d$ keeps the joint angles valid, but the end no longer lies on the line to the target. Clamp $d$ first.
- **Mixed conventions.** The planar angles $\theta_1$ and $\theta_2$ are relative: $\theta_2$ is measured from the direction of the first bone. Joint angles of a rig may use the inner angle $\beta$ instead.
- **Bone lengths from the pose.** Take $l_1$ and $l_2$ from the bind pose, not from the current animated pose, or the limb drifts when the animation scales a bone.

## Implementations

## History

The closed form of the planar two-link arm comes from robotics, where it is the first example of analytic inverse kinematics, as in Lynch and Park (2017).
Computer animation took it over for limbs, and Parent (2012) treats it with the other inverse kinematics methods for linkages.
The pole vector is the control that animation tools added to choose the bending plane of a three dimensional limb.

## References
