---
tag: JXW2FC
kind: algorithm
slug: cyclic-coordinate-descent-inverse-kinematics
name: Cyclic coordinate descent inverse kinematics
aliases:
- CCD inverse kinematics
area: robotics/robot-kinematics
level: core
summary: Turns one joint at a time, from the tip to the base, to point the end effector at the target, repeating until close.
model: real-ram
complexity:
  vars: {n: the number of joints, k: the number of sweeps}
  time: {worst: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1991
  people: [L.-C. T. Wang, C. C. Chen]
  note: Wang and Chen used cyclic coordinate descent for the inverse kinematics of manipulators, with a closed form update for each joint, combined with a second nonlinear programming method.
prereqs: [inverse-kinematics, forward-kinematics, coordinate-descent]
see_also: [coordinate-descent, fabrik, jacobian-transpose-method, damped-least-squares-inverse-kinematics, paden-kahan-subproblems, rodrigues-rotation-formula, kinematic-chain, newton-raphson-inverse-kinematics]
sources:
  - paper: doi:10.1109/70.86079
    title: "L.-C. T. Wang and C. C. Chen, A combined optimization method for solving the inverse kinematics problem of mechanical manipulators, IEEE Transactions on Robotics and Automation 7(4), 489-499, 1991"
    locator: the cyclic coordinate descent part of the method
---

Cyclic coordinate descent (CCD) solves the inverse kinematics of a chain of revolute joints by turning one joint at a time.
Each joint, from the tip to the base, turns by the angle that brings the end effector as close to the target as possible, and that angle has a closed form.
One sweep over the joints is cheap, needs no Jacobian and no linear solve, and never makes the error larger.
CCD is popular in computer animation for long chains, but it has no general guarantee that it reaches a target in reach, and it tends to bend the joints near the tip the most.

## In plain words

Think of a chain of rods with hinges, and a point the free end must touch.
Start at the hinge next to the free end.
Turn only that hinge, as far as needed to swing the free end as close to the point as it can go.
Then do the same with the next hinge toward the base, and so on, up to the base.
That is one sweep.
Repeat sweeps until the end touches the point or stops moving closer.
Each turn is easy to find, because one hinge can only move the end on a circle.

## The problem

**Input.**

- A serial chain of $n$ revolute joints, given by [forward kinematics](/forward-kinematics/): for a joint vector $\theta$, the world position $p_i$ and unit axis $w_i$ of each joint and the end effector position $e(\theta)$.
- A target point $t$, an initial guess $\theta^0$, a tolerance $\varepsilon$ and a sweep limit $k_{\max}$.

**Output.** A $\theta$ with $|e(\theta) - t| \le \varepsilon$, or the last iterate with the report that the tolerance was not met.

The version here matches positions only.
Orientation targets need a combined cost per joint, as in the method of Wang and Chen.

## The algorithm

```pseudo id=main
CCD-IK(chain, t, θ0, ε, k_max)
L1  θ ← θ0
L2  for k ← 1 to k_max
L3      (p_1..p_n, w_1..w_n, e) ← FORWARD-KINEMATICS(θ)
L4      if |e - t| ≤ ε then return θ
L5      for i ← n downto 1                          ▷ from the tip to the base
L6          u ← (e - p_i) minus its part along w_i; v ← (t - p_i) minus its part along w_i
L7          φ ← atan2(w_i · (u × v), u · v)          ▷ φ ← 0 if u · v = 0 and w_i · (u × v) = 0
L8          θ_i ← θ_i + φ; e ← p_i + R(w_i, φ)(e - p_i)
L9  return θ with the report that the tolerance was not met
```

Line L7 is the least squares form of the first [Paden-Kahan subproblem](/paden-kahan-subproblems/): the end effector moves on a circle about the axis of joint $i$, and L7 picks the point of that circle nearest to the target.
Line L8 moves the end effector with the [Rodrigues formula](/rodrigues-rotation-formula/) instead of a new forward kinematics.
This is valid because turning joint $i$ moves only the links after it, so $p_j$ and $w_j$ for $j < i$, which the sweep uses next, do not change.

Joint limits are easy to add: clamp $\theta_i + \varphi$ to the allowed range at L8.

## Example

The planar 2R arm has $L_1 = L_2 = 1$ m, both axes along $z$, the target $t = (1, 1)$ m and the start $\theta^0 = (0.3, 1.2)$ rad.
At the start the hand is at $(1.026074, 1.293015)$ m, and the error is 0.294173 m.

Sweep 1:

- Joint 2 turns by $\varphi = 0.007482$ rad, and the error becomes 0.294106 m.
- Joint 1 turns by $\varphi = -0.118343$ rad.
The hand moves to $(1.164205, 1.164205)$ m, on the line from the base through the target, and the error becomes 0.232222 m.

After the sweep, $\theta = (0.181657, 1.207482)$ rad.

| sweeps | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| error (m) | 0.294173 | 0.232222 | 0.135220 | 0.073280 | 0.038185 |

After that, each sweep halves the error, and after 33 sweeps the error is below $10^{-10}$ m at $\theta = (0, \pi/2)$ rad.
Near the solution, one sweep acts to first order like one Gauss-Seidel sweep on the normal equations with $J^{\mathsf T}J = \begin{pmatrix}2 & 1\\ 1 & 1\end{pmatrix}$, and the Gauss-Seidel ratio for this matrix is $1^2/(2 \cdot 1) = 0.5$.
This is an explanation of the observed ratio, not a proof.
For the same arm and start, the [Jacobian transpose method](/jacobian-transpose-method/) with its best fixed gain has the ratio 0.745.

For the target $(2.5, 0)$ m, out of reach, the error stops falling after 90 sweeps, with the arm stretched along the $x$ axis and the error at 0.5 m.

In the tests, 20 random chains of 6 joints in space, with targets that forward kinematics puts in reach, all reach the target to $10^{-9}$ m, in 7 to 181 sweeps.

## Correctness

The proof page proves four facts.

- **Best turn.** Line L7 gives the angle that minimizes the distance from the end effector to the target over all turns of joint $i$ alone.
- **Cheap update.** Line L8 gives the true end effector position, and the positions and axes from L3 stay valid for the joints that the sweep visits next.
- **Monotone error.** The error never increases, so the errors converge.
- **Fixed points.** If a sweep does not move any joint, the gradient of the squared error is zero.

**Convergence.** CCD has no general convergence result, and the sources of this page prove none.
The error converges to a limit, but the limit can be positive at a stationary point that is not a solution, and the joint vectors need not converge.
For a target out of reach, the stretched arm that points at the target is a stationary point.
The linear rate in the example is observed, not proved.

## Complexity

**Cost per sweep.** Line L3 costs $\Theta(n)$ for a serial chain, and each joint update at L6 to L8 costs $\Theta(1)$, in the [real RAM](/real-ram/).
So one sweep costs $\Theta(n)$, and $k$ sweeps cost $\Theta(kn)$.
A version that calls forward kinematics again for each joint costs $\Theta(n^2)$ per sweep.
The extra space is $\Theta(n)$ for the joint positions and axes.

**Number of sweeps.** It is not bounded in general, and it depends a lot on the start and the target, as the tests show.

## Properties

- **No Jacobian.** CCD needs no Jacobian, no matrix inverse and no tuning gain.
- **Always defined.** Each update exists for every configuration, including singular ones and targets out of reach.
- **Monotone.** The error after each joint update is never larger than before.
- **Order.** The order from the tip to the base is the usual one; other orders give other iterates and other end poses.
- **Uneven motion.** The joints near the tip often turn much more than the joints near the base, which gives curled poses in long chains.

## Variants and improvements

- **Orientation.** Wang and Chen minimize a weighted sum of a position and an orientation error for each joint, still in closed form.
- **Joint limits.** Clamp each angle at L8; the error still never increases, since the clamped angle lies between the old angle and the best one, where the error falls steadily.
- **Damping.** Scale each $\varphi$ by a factor below 1, or limit its size, to spread the motion over the chain.
- **Prismatic joints.** The best slide along the axis is the projection of $t - e$ onto the axis.
- **Other methods.** [FABRIK](/fabrik/) also works joint by joint, but on positions instead of angles; [damped least squares](/damped-least-squares-inverse-kinematics/) moves all joints together.

## When to use it

Use CCD for long chains, for interactive animation where each step must be cheap, and where joint limits must be applied joint by joint.
For a robot arm that must reach a full pose accurately, use [Newton-Raphson inverse kinematics](/newton-raphson-inverse-kinematics/) or [damped least squares](/damped-least-squares-inverse-kinematics/), or a closed form solution when the arm has one.

## Pitfalls

- **No guarantee.** CCD can stop at a stationary point that is not a solution, and nothing tells you this except the error at the end.
- **Exact degenerate starts.** For the 2R arm above, the straight start $(0, 0)$ rad and the target $(-1, 0)$ m fold the arm to the base in one sweep, where joint 1 has no best angle.
In exact arithmetic CCD stops there with an error of 1 m; in floating point, rounding moves it off that point.
- **Curled poses.** Since the tip joints turn first, the result can look unnatural; damping or a different order helps.
- **Slow convergence.** For targets near the boundary of the workspace, the error can fall slowly over many sweeps.
- **Angle wrap.** The angles grow by multiples of $2\pi$ over many sweeps; wrap them before you compare them with joint limits.

## Implementations

## History

Coordinate descent is an old optimization method.
Wang and Chen (1991) applied it to the inverse kinematics of manipulators, with a closed form solution for the best turn of each joint, and combined it with a second nonlinear programming method.
The method became a standard tool for inverse kinematics in computer animation and games, where its cheap steps and simple handling of joint limits matter more than its weak guarantees.

## References
