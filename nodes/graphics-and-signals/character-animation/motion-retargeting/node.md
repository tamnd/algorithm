---
tag: 0KV7A9
kind: algorithm
slug: motion-retargeting
name: Motion retargeting
aliases:
- retargetting motion to new characters
area: graphics-and-signals/character-animation
level: core
summary: Adapt a motion recorded on one character to another with different proportions, keeping constraints such as foot contacts by spacetime optimization.
model: real-ram
complexity:
  vars: {m: "the number of constraint rows", s: "the number of control points of the displacement", I: "the number of iterations"}
  time: {total: "O(I (m^2 s + m^3))"}
  space: {extra: "O(m s + m^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [spacetime-constraints, b-spline, inverse-kinematics]
see_also: [footskate-cleanup, motion-warping, two-bone-inverse-kinematics, character-skeleton, jacobian-pseudoinverse-method, pseudoinverse, deformation-transfer, style-based-inverse-kinematics]
sources:
  - paper: doi:10.1145/280814.280820
    title: "Michael Gleicher, Retargetting motion to new characters, SIGGRAPH 98, 33-42"
    locator: the formulation of retargeting as a spacetime problem over the whole motion, with the change written as a displacement curve of B-splines, kinematic constraints of the new character and an objective that keeps the displacement small (general locator)
  - paper: doi:10.1145/378456.378507
    title: "Andrew Witkin and Michael Kass, Spacetime constraints, SIGGRAPH 88, Computer Graphics 22(4), 159-168"
    locator: the spacetime frame of an optimization over the whole trajectory under constraints (general locator)
---

Motion retargeting adapts a motion made for one character to a second character with other proportions.
If you copy the joint angles of a walk from a tall actor to a short character, the feet of the short character do not reach the floor, slide during the contacts, or go through the floor.
Gleicher (1998) wrote the fix as an optimization over the whole motion at once: add a smooth displacement to every degree of freedom, as small as possible, so that the new character meets the constraints of the motion, such as a planted foot.
The displacement is a [B-spline](/b-spline/) curve in time, so the change is smooth and keeps the details of the original motion.
It is a kinematic form of [spacetime constraints](/spacetime-constraints/): there are no forces and no dynamics, only constraints over time and a preference for a small change.

## In plain words

The source motion is good, and we want to keep as much of it as we can.
The new character has shorter or longer bones, so some important facts of the motion break: the foot no longer touches the floor where and when it should.
We write down these facts as constraints: at these frames, the foot is at this point.
Then we add a correction curve to every joint angle and to the root, over the whole motion.
The correction curve is smooth, so it cannot add jitter.
Among all smooth corrections that make the constraints true, we take the smallest one.
Frames far from all constraints keep their original values.
Frames near a constraint change a little, and the change fades in and out over a few frames.

## The problem

A character has the degrees of freedom $q = (q_1, \ldots, q_D)$: a root position and joint angles.
The source motion is $q(t)$ at the frames $t = 0, \ldots, F - 1$.
The new character has the same skeleton with other bone lengths, so the same $q$ gives other end positions through [forward kinematics](/forward-kinematics/).
The constraints are equations $g_f(q(t_f)) = p_f$ at chosen frames, for example the position of a foot during a contact, often taken from the source motion.
The output is a new motion $q(t) + d(t)$ that meets the constraints and stays close to the source.

The displacement is $d_k(t) = \sum_j c_{k j} B(t / \delta - j + 1)$ for each degree of freedom $k$, where $B$ is the uniform cubic B-spline basis and $\delta$ is the spacing of the control points in frames.
The problem is

$$\min_c \; c^\top W c \quad \text{subject to} \quad g_f(q(t_f) + d(t_f)) = p_f \text{ for every constraint } f,$$

with $W$ a diagonal matrix of weights per degree of freedom.
The weights are tuning: they say how much a change of the root position costs against a change of an angle.
The spacing $\delta$ is also tuning: a smaller spacing allows faster changes.

## The algorithm

```pseudo id=main
RETARGET(source q, new lengths, constraints (t_f, p_f), spacing δ, weights W)
L1  c ← 0                                          ▷ start from the source motion
L2  repeat
L3      for each constraint f: compute q(t_f) + d(t_f), the residual r_f = g_f - p_f and the Jacobian rows J_f in c
L4      b ← J c - r                                 ▷ the linearized constraints are J c = b
L5      solve (J W⁻¹ Jᵀ) μ = b
L6      c ← W⁻¹ Jᵀ μ                               ▷ the smallest c with J c = b
L7  until c does not change and r is small
L8  return q(t) + d(t) for every frame
```

Line L3 is forward kinematics and its Jacobian at each constrained frame, multiplied by the B-spline basis values: the derivative of $g_f$ in $c_{kj}$ is $\partial g_f / \partial q_k \cdot B(t_f / \delta - j + 1)$.
Lines L4 to L6 replace the constraints by their linearization and take the solution of smallest weighted norm, which is the [pseudoinverse](/pseudoinverse/) solution.
This is a step of sequential quadratic programming with the Hessian of the objective only.
At a fixed point, the constraints hold and $W c$ is in the row space of $J$, which is the first order condition of the constrained problem.

The code in `impl/python` uses a planar leg with a root $(r_x, r_y)$, a hip angle and a knee angle, so $D = 4$, and a foot position constraint at each frame of a contact.
Gleicher's paper works with full 3D skeletons and more kinds of constraints; the toy keeps only the part that defines the method.

## Example

Take a straight leg that hangs down, with all angles 0 and the root at height 2.
The source bones have the lengths 1 and 1, so the foot is on the floor at height 0.
The new character has the lengths 0.9 and 0.9, so its foot is at height 0.2.
Ask for the foot on the floor at frame 8 only, with the spacing $\delta = 2$, and make the angles very costly, so that only the root moves.

The root height needs the displacement $-0.2$ at frame 8, which is a knot.
At a knot, the three basis functions that are not zero have the values $1/6$, $4/6$ and $1/6$, and the sum of their squares is $1/2$.
The smallest control points with $\frac{1}{6} c_{j-1} + \frac{4}{6} c_j + \frac{1}{6} c_{j+1} = -0.2$ are proportional to the basis values: $c = 2 \cdot (-0.2) \cdot (1/6, 4/6, 1/6) = (-0.0667, -0.2667, -0.0667)$.

| frame | 2 | 4 | 6 | 8 | 10 | 12 | 14 |
|---|---|---|---|---|---|---|---|
| root height change | 0 | $-0.0111$ | $-0.0889$ | $-0.2$ | $-0.0889$ | $-0.0111$ | 0 |

At frame 10 the change is $\frac{1}{6}(-0.2667) + \frac{4}{6}(-0.0667) = -0.0889$, and at frame 12 it is $\frac{1}{6}(-0.0667) = -0.0111$.
So the root drops smoothly into the contact and comes back up, and frames 2 and 14 and beyond do not change.
The tests check these numbers.

For the walk in the tests, with 24 frames, 10 frames of contact and the bone lengths 0.8 and 0.9 instead of 1 and 1, the method converges in 22 iterations, and the root drops by about 0.22 to 0.30 during the contact.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).
- **Each step meets the linearized constraints with the smallest change.** If $J$ has full row rank, $J W^{-1} J^\top$ is positive definite, and line L6 gives the unique minimizer of $c^\top W c$ subject to $J c = b$.
- **A fixed point is a first order optimum.** If the iteration stops with $r = 0$, then the constraints hold, and $W c = J^\top \mu$, which is the Lagrange condition of the constrained problem.
- **The same character gives the source motion.** If the source already meets the constraints, $r = 0$ at $c = 0$, so the first step gives $c = 0$.
- **Frames far from all constraints do not change.** A control point whose basis does not reach any constrained frame has a zero column in $J$, so line L6 gives it the value 0. A frame where only such control points act keeps the source pose.

The method does not have a global guarantee: the constraints are nonlinear, the iteration can fail to converge, and the fixed point can be a local optimum.
The tests check the constraints, the first order condition, that feasible neighbors are not better, the far frames and the check value.

## Complexity

The costs are in the real RAM model.
With $m$ constraint rows and $s = D \cdot (\text{number of control points})$ unknowns, line L3 costs $O(m D)$ for the kinematics and the nonzero entries, because each constrained frame meets only four control points per degree of freedom.
The code builds $J W^{-1} J^\top$ densely in $O(m^2 s)$ and solves it in $O(m^3)$, so one iteration costs $O(m^2 s + m^3)$.
With the sparsity of $J$, the matrix $J W^{-1} J^\top$ is banded in time, and one iteration costs $O(m)$ for a fixed bandwidth.
The number of iterations depends on the problem; it is 22 in the test walk.

## Properties

- Smooth: the change is a cubic B-spline, so it is twice continuously differentiable in time, and its frequency content is bounded by the spacing.
- Local in time: frames far from all constraints keep the source values.
- Minimal: among the smooth changes that meet the linearized constraints, it takes the smallest one in the weighted norm.
- Kinematic: there are no forces and no dynamics, so physical effects of the new size, such as a different timing, are not modeled.
- Not exact in general: the constraints hold to the tolerance of the iteration, and only at the constrained frames.

## Variants and improvements

- **Per frame inverse kinematics.** Solve [inverse kinematics](/inverse-kinematics/) at each frame of a contact, then smooth the changes. This is faster but can add jitter, because nothing ties the frames together. The spacetime form with a smooth displacement avoids that.
- **Foot contact cleanup.** [Footskate cleanup](/footskate-cleanup/) fixes the foot positions during the contacts with analytic [two-bone inverse kinematics](/two-bone-inverse-kinematics/) per frame and small changes of the bone lengths.
- **Displacement maps.** The idea of adding a smooth curve to a motion is also the base of [motion warping](/motion-warping/), where the user gives the key changes by hand.
- **Other objectives.** The objective can measure the change in other quantities, such as end positions, instead of the degrees of freedom. The choice changes the result.
- **Shapes instead of skeletons.** To copy a deformation of a mesh to a different mesh, use [deformation transfer](/deformation-transfer/).

## When to use it

Use motion retargeting when a motion capture clip or an animation must play on a character with different proportions, and contacts or other spatial facts of the motion must still hold.
It is the right tool when the motion matters more than the exact pose at each frame.
If the only problem is the foot sliding during contacts, [footskate cleanup](/footskate-cleanup/) is simpler and faster.

## Pitfalls

- **Too many constraints for the spacing.** If many constrained frames fall in the support of few control points, $J$ is close to rank deficient and the iteration converges slowly or not at all. A smaller spacing, or fewer constrained frames, fixes it. In the toy, a spacing of 4 frames with 10 constrained frames converges much more slowly than a spacing of 2.
- **Constraints that cannot all hold.** A foot target out of the reach of the new leg has no solution. Choose the targets for the new character, for example by scaling the positions of the source with the size of the character.
- **Weights.** Without weights, a change of one radian costs as much as a change of one length unit. Set the weights for the units of the skeleton.
- **Constraints only at the frames.** The constraints hold at the constrained frames and not in between. Add constraints at all frames of a contact.
- **Local optima.** The method starts from the source motion and finds a nearby solution. For a very different character, the result can be a poor local optimum.

## Implementations

## History

Before Gleicher's paper, motions were adapted to new characters by hand, or by per frame inverse kinematics.
Witkin and Kass (1988) had introduced [spacetime constraints](/spacetime-constraints/), optimization over a whole motion under constraints, with dynamics.
Gleicher (1998) used the same frame without the dynamics, wrote the change as a displacement of B-splines that is as small as possible, and solved for the whole motion at once.
Later systems added faster solvers and per frame methods with filtering, and the problem remains a standard step in pipelines that use motion capture.

## References
