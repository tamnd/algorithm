---
tag: 7KE72T
kind: algorithm
slug: sequential-convex-trajectory-optimization
name: Sequential convex trajectory optimization
aliases:
- TrajOpt
area: robotics/trajectory-generation
level: advanced
summary: "Schulman's method that convexifies collision constraints with signed distance at each step and solves trust region convex programs."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {n: "the number of waypoints", m: "the number of obstacles", I: "the number of convex subproblems solved", N: "the number of Newton steps per subproblem"}
  time: {worst: O(I N n m)}
  space: {extra: O(n m)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [trajectory-optimization, quadratic-programming, penalty-method]
see_also: [chomp, stomp, gaussian-process-motion-planning, barrier-method, signed-distance-function, gjk-algorithm, convex-optimization-problem, interior-point-method]
sources:
  - paper: doi:10.15607/RSS.2013.IX.031
    title: "John Schulman, Jonathan Ho, Alex Lee, Ibrahim Awwal, Henry Bradlow and Pieter Abbeel, Finding locally optimal, collision-free trajectories with sequential convex optimization, Robotics: Science and Systems IX, 2013"
    locator: "the whole paper (the original method)"
  - paper: doi:10.1177/0278364914528132
    title: "John Schulman, Yan Duan, Jonathan Ho, Alex Lee, Ibrahim Awwal, Henry Bradlow, Jia Pan, Sachin Patil, Ken Goldberg and Pieter Abbeel, Motion planning with sequential convex optimization and convex collision checking, The International Journal of Robotics Research 33(9), 2014, 1251-1270"
    locator: "the sequential convex optimization with l1 penalties and a trust region, and the linearized signed distance constraints"
  - book: isbn:9780521833783
    title: "Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004"
    locator: "Chapter 11 (the barrier method used for the subproblem)"
---

Sequential convex trajectory optimization, known by the name of its software, TrajOpt, treats collision avoidance as a constraint: the signed distance between the robot and each obstacle must stay above a safety margin. The constraint is not convex, so the method replaces it, at the current trajectory, by its linearization, and solves the resulting convex problem only inside a trust region, a box around the current trajectory where the linearization is trusted. It moves to the new trajectory only if the true merit improves enough compared with the improvement the convex model predicted, and it adjusts the box from that comparison. Violated constraints are charged by an $\ell_1$ penalty whose weight grows until they hold. Like all methods for [trajectory optimization](/trajectory-optimization/), it is local: it finds a stationary point near its start.

## In plain words

Bend a wire from start to goal so that it is short and keeps a safe distance from every obstacle. Near the current wire, the rule "stay away from this obstacle" is replaced by a simpler rule, "stay on this side of a straight fence", which is easy to obey exactly. Solve the easy version, but only allow the wire to move a little. Then check the real obstacles. If the move helped as much as the easy version promised, keep it and allow bigger moves next time; if not, undo it and allow smaller moves. When nothing helps, check whether the wire is safe; if not, make safety more important and continue. The result is a good wire near the start, not always the best one.

## The problem

Input: a start $q_0$ and a goal $q_{n+1}$, $n$ free waypoints $x = (x_1, \dots, x_n)$, signed distance functions $\mathrm{sd}_j$ for the obstacles, and a margin $d_{\text{safe}}$. Minimize

$$f(x) = \sum_{t=0}^n \|x_{t+1} - x_t\|^2 \quad \text{subject to} \quad \mathrm{sd}_j(x_t) \ge d_{\text{safe}} \text{ for all } t, j,$$

with $x_0 = q_0$ and $x_{n+1} = q_{n+1}$. The papers handle robot arms, where $x_t$ is a vector of joint angles and the signed distance is computed between convex parts of the robot and of the scene; they also add joint limits, other costs and constraints, and a continuous-time version of the collision constraint. This page uses a point robot in the plane with signed distances given as functions, which keeps the code short.

For a penalty weight $\mu$, the merit function is

$$\varphi(x) = f(x) + \mu \sum_{t, j} \max\bigl(0,\ d_{\text{safe}} - \mathrm{sd}_j(x_t)\bigr).$$

## The algorithm

```pseudo id=main
SCP(x, μ_0, Δ_0)
L1  μ ← μ_0; Δ ← Δ_0
L2  for j ← 1 to J do                                  ▷ penalty loop
L3      repeat                                         ▷ trust region loop
L4          v_k ← sd_k(x_{t_k}); g_k ← ∇sd_k(x_{t_k}) for every constraint k
L5          δ ← argmin φ̂(δ) subject to ‖δ‖∞ ≤ Δ          ▷ convex subproblem
L6          pred ← φ(x) - φ̂(δ); if pred ≤ xtol then leave the loop
L7          ρ ← (φ(x) - φ(x + δ)) / pred
L8          if ρ ≥ c then x ← x + δ; Δ ← τ₊Δ else Δ ← τ₋Δ
L9      until Δ < Δ_min
L10     if every constraint holds within ctol then return x
L11     μ ← k_μ μ
L12 return x                                           ▷ constraints not met
```

Line L4 linearizes every constraint at the current trajectory: $\mathrm{sd}_k(x_{t_k} + \delta_{t_k}) \approx v_k + g_k^{\mathsf T}\delta_{t_k}$. For a disc obstacle $g_k$ is the unit vector from the center to the waypoint. For a robot arm, $g_k$ is the normal at the closest points between two convex shapes, found for example with [GJK](/gjk-algorithm/), mapped to joint space by the Jacobian.

Line L5 minimizes the convex model

$$\hat\varphi(\delta) = f(x + \delta) + \mu \sum_k \max\bigl(0,\ d_{\text{safe}} - v_k - g_k^{\mathsf T}\delta_{t_k}\bigr)$$

over the box $\|\delta\|_\infty \le \Delta$. With one slack variable per hinge it is a [quadratic program](/quadratic-programming/). The code solves it with a [barrier method](/barrier-method/): Newton steps on the objective plus logarithms of all constraint values, with the weight of the objective raised by a factor 20 until the gap bound is $10^{-8}$. The slacks enter each Newton system in a diagonal block, so they can be eliminated, which leaves a block tridiagonal system with $2 \times 2$ blocks, solved in $O(n)$.

Lines L6 to L9 are the trust region logic. The predicted decrease is what the model promises; the true decrease is measured on $\varphi$. A step is accepted when the ratio is at least $c = 0.1$, and then the box grows by $\tau_+ = 1.5$; otherwise it shrinks by $\tau_- = 0.5$. Lines L10 and L11 raise the penalty by $k_\mu = 10$ when the trajectory still violates a constraint.

## Example

A point moves from $(-1, 0)$ to $(1, 0)$ with $n = 9$ waypoints. One disc of radius $0.5$ has its center at $(0, -0.15)$, so the straight start line cuts it $0.35$ deep. The margin is $d_{\text{safe}} = 0.1$, $\mu = 10$ and $\Delta_0 = 0.1$.

| step | $\Delta$ | predicted decrease | true decrease | merit $\varphi$ | smallest clearance | height of the middle waypoint |
|---|---|---|---|---|---|---|
| 0 | | | | 15.3560 | $-0.350$ | 0.000 |
| 1 | 0.1 | 6.3416 | 6.4133 | 8.9427 | $-0.250$ | 0.100 |
| 2 | 0.15 | 6.3581 | 6.3581 | 2.5846 | $-0.100$ | 0.250 |
| 3 | 0.225 | 2.0728 | 2.0728 | 0.5118 | 0.100 | 0.450 |
| 4 | 0.3375 | 0.0236 | 0.0236 | 0.4882 | 0.100 | 0.450 |
| 5 | 0.5063 | 0.0004 | 0.0004 | 0.4878 | 0.100 | 0.450 |

In the first two steps the trust region limits the move: the middle waypoint rises by exactly $\Delta$. After step 3 the trajectory is feasible and the remaining steps only spread the waypoints. The next predicted decrease is $3.4 \cdot 10^{-6}$, below $\mathrm{xtol} = 10^{-4}$; all constraints hold, so the method returns with $\mu = 10$, five accepted steps and none rejected. The result has $f = 0.48781$, ten equal segments, and length $2.2086$.

The true decrease is never below the predicted one here. That is no accident: the distance to a disc is a convex function, so its linearization is below it, and the model is an upper bound on the merit (proof, Theorem 2). The shortest continuous path that keeps a distance of $0.6$ from the center is $2.2115$ long, longer than the result. The difference is the pitfall of discrete constraints: the segments between waypoints cut the corner, and the smallest clearance along the segments is $0.0895$, below the margin.

## Correctness

The [proof](proofs/correctness.md) shows three things. First, for a fixed penalty weight, every accepted step lowers the merit by more than $c \cdot \mathrm{xtol}$, so there are finitely many of them, and the number of rejected steps is bounded too, because each one halves $\Delta$ and the loop ends below $\Delta_{\min}$. So the method always ends, and the merit never increases while $\mu$ is fixed. Second, if every signed distance is convex in the variables, as for a point robot among convex obstacles, the convex model is an upper bound on the merit, so every step is accepted. Third, if the subproblem is solved exactly and predicts no decrease, then no direction decreases the merit to first order: the point is a stationary point of the penalized problem. With robot arms the signed distance is not convex in the joint angles, steps can be rejected, and the first and third results still hold. None of this says that the result is a global minimum or that it satisfies the constraints; line L10 checks that, and the method is local.

## Complexity

Each Newton step of the subproblem assembles the system in $O(nm)$ and solves it in $O(n)$ after eliminating the slacks; with $d$ joints instead of 2, the blocks are $d \times d$ and the cost is $O(n(d^3 + md))$. So one subproblem costs $O(Nnm)$ for $N$ Newton steps, and the whole run costs $O(INnm)$ for $I$ subproblems, plus the evaluation of the signed distances at every pass. The memory is $O(nm)$. The theory of the barrier method bounds $N$ by a quantity that grows with the logarithm of the accuracy (see the barrier method page). There is no useful bound on $I$; the six subproblems of the example are a measurement.

## Properties

- **Local.** It converges to a stationary point of the penalized merit near the start.
- **Monotone for a fixed penalty.** Accepted steps decrease the merit; rejected steps leave the trajectory unchanged.
- **Infeasible starts are allowed.** The $\ell_1$ penalty and the slacks make every subproblem feasible, even when the start is deep in collision.
- **Deterministic.** The same input gives the same output.
- **Hard constraints in the end.** Unlike [CHOMP](/chomp/), which charges closeness to obstacles in the cost, the penalty weight grows until the constraints hold or the outer limit is reached.

## Variants and improvements

- **Continuous-time collision.** Constrain the convex hull of the robot at two consecutive waypoints, not only the waypoints, so that thin obstacles cannot slip between waypoints. The IJRR paper does this.
- **Only nearby obstacles.** Linearize only the pairs closer than a threshold; pairs far away have zero penalty and zero effect on the model.
- **Equality constraints.** Penalize $|h(x)|$ with the same $\ell_1$ approach, for example for an end effector pose at the goal.
- **Other subproblem solvers.** Any solver for convex quadratic programs works for line L5; an [interior point method](/interior-point-method/) or an active set method is common. The software uses an external solver.
- **Related methods.** [CHOMP](/chomp/) and [GPMP2](/gaussian-process-motion-planning/) use costs instead of constraints, and [STOMP](/stomp/) needs no gradients.

## When to use it

Use it for robot arms when the motion must keep a guaranteed margin from obstacles and other constraints, such as joint limits and pose constraints, must hold exactly. It works from infeasible starts such as the straight line in joint space, and it is often fast enough for interactive planning. For problems where a local method fails, use a [sampling planner](/rapidly-exploring-random-tree/) first and this method to improve the result.

## Pitfalls

- **Constraints at waypoints only.** Line L4 constrains the waypoints, and the segments between them can cut into an obstacle, as in the example. Use the continuous-time version or check the segments.
- **A wrong trust region update.** If line L8 accepts steps with a negative ratio, the merit can grow and the loop can cycle. Keep $c > 0$.
- **The penalty is not the constraint.** A stop in line L6 means a stationary point of the merit, not a feasible trajectory. Always check line L10 and report failure when line L12 is reached.
- **Gradients at singular points.** At the center of a disc, or where two closest-point pairs switch, the gradient in line L4 is not defined or jumps. Then the subproblem sees a flat or wrong model and the method can stall.
- **Penalty growth.** A large $\mu$ in line L11 makes the subproblem badly scaled. If no feasible trajectory is near the start, $\mu$ grows to the outer limit and the result still violates the constraints.

## Implementations

## History

John Schulman, Jonathan Ho, Alex Lee, Ibrahim Awwal, Henry Bradlow and Pieter Abbeel presented the method at Robotics: Science and Systems in 2013, with the TrajOpt software. The journal version of 2014 added the continuous-time collision constraint and more experiments. It followed [CHOMP](/chomp/) and [STOMP](/stomp/), and differs from them in treating collision as a constraint with a signed distance computed between convex shapes. The trust region and $\ell_1$ penalty framework is older and comes from nonlinear programming.

## References
