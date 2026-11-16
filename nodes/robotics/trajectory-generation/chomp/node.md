---
tag: ZMPYZV
kind: algorithm
slug: chomp
name: CHOMP
aliases:
- covariant Hamiltonian optimization for motion planning
area: robotics/trajectory-generation
level: advanced
summary: "Optimizes a discretized trajectory by covariant gradient steps on a smoothness cost plus an obstacle cost from a distance field."
solves: [trajectory-optimization]
model: real-ram
complexity:
  vars: {n: "the number of waypoints", d: "the dimension of the configuration space", m: "the number of obstacle terms per waypoint", I: "the number of iterations"}
  time: {worst: O(I n (d + m))}
  space: {extra: O(n d)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [trajectory-optimization, gradient-descent, signed-distance-function]
see_also: [stomp, sequential-convex-trajectory-optimization, gaussian-process-motion-planning, elastic-bands, potential-field-method, tridiagonal-system-solving, distance-transform, natural-gradient-descent]
sources:
  - paper: doi:10.1109/ROBOT.2009.5152817
    title: "Nathan Ratliff, Matt Zucker, J. Andrew Bagnell and Siddhartha Srinivasa, CHOMP: Gradient optimization techniques for efficient motion planning, IEEE International Conference on Robotics and Automation (ICRA), 2009, 489-494"
    locator: "the whole paper (the original method)"
  - paper: doi:10.1177/0278364913488805
    title: "Matt Zucker, Nathan Ratliff, Anca D. Dragan, Mihail Pivtoraiko, Matthew Klingensmith, Christopher M. Dellin, J. Andrew Bagnell and Siddhartha S. Srinivasa, CHOMP: Covariant Hamiltonian optimization for motion planning, The International Journal of Robotics Research 32(9-10), 2013, 1164-1193"
    locator: "Section 3.1, equations (1) to (3) (objective); Section 3.4, equations (16) and (17) (waypoints); Section 3.5, equations (18) and (19) (covariant update and termination); Section 3.6 (weight scheduling); Section 4.2, equation (21) (obstacle cost); Section 7.1 (experiments)"
---

CHOMP improves a robot trajectory by gradient descent, with two ideas that make plain gradient descent work well on trajectories. The trajectory is a list of waypoints between a fixed start and goal. The objective adds a smoothness term, the sum of squared velocities, and an obstacle term that charges every point of the robot for being close to or inside an obstacle, read from a [signed distance field](/signed-distance-function/). The first idea is the step: instead of moving each waypoint along its own gradient, CHOMP multiplies the gradient by the inverse of the smoothness matrix, which spreads a push on one waypoint smoothly over the whole trajectory. The second idea is that the obstacle term has useful gradients even inside obstacles, so CHOMP can start from a straight line that passes through them. Like all methods for [trajectory optimization](/trajectory-optimization/), CHOMP is local: it finds a stationary point near its start, which can be a poor one or can still be in collision.

## In plain words

Lay a chain of beads from start to goal, straight through the furniture. Each bead inside or near a piece of furniture feels a push outward. If each bead moved alone, the chain would get kinks. CHOMP instead lets each push bend the whole chain smoothly, as if the chain were a stiff spring, so the chain slides around the obstacle in one piece. It repeats this until the pushes and the stiffness balance. The method is fast and makes smooth motions. It can get stuck: if the chain hits an obstacle exactly in the middle, the pushes from both sides cancel and it does not know which way to go. It also does not promise that the result is free of collisions, so the caller must check.

## The problem

Input: a start $q_0$ and a goal $q_{n+1}$ in a configuration space $\mathbb R^d$, a number $n$ of free waypoints, a signed distance $D(x)$ to the obstacles for points $x$ of the workspace, the body points of the robot, and weights $\lambda > 0$ and $\varepsilon > 0$. The trajectory is $\xi = (q_1, \dots, q_n)$ with time step $\Delta t$. Zucker et al. (Section 3.1) minimize

$$U(\xi) = F_{\text{obs}}(\xi) + \lambda F_{\text{smooth}}(\xi), \qquad F_{\text{smooth}} = \frac12 \sum_{t=0}^{n} \left\|\frac{q_{t+1} - q_t}{\Delta t}\right\|^2 = \frac12 \xi^{\mathsf T} A \xi + \xi^{\mathsf T} b + c,$$

where $A$ is the tridiagonal finite-difference matrix (Section 3.4). The obstacle term charges each body point by the cost (Section 4.2, equation (21))

$$c(x) = \begin{cases} -D(x) + \tfrac12\varepsilon & D(x) < 0, \\ \tfrac{1}{2\varepsilon}(D(x) - \varepsilon)^2 & 0 \le D(x) \le \varepsilon, \\ 0 & \text{otherwise,}\end{cases}$$

and the paper integrates it along the path of each body point, weighted by the speed of the point (equation (3)). Output: a trajectory $\xi$ with a small gradient of $U$, which is a stationary point, usually free of collision when the start was close enough to a free one.

This page uses a point robot in the plane ($d = 2$, the robot is its single body point) with disc obstacles, and the plain sum $F_{\text{obs}} = \sum_t \sum_j c(D_j(q_t))$ over waypoints and discs. This keeps the gradient exact and allows the proof below.

## The algorithm

```pseudo id=main
CHOMP(q_0, q_{n+1}, n, λ, η, I, tol)
L1  ξ ← n evenly spaced points on the segment from q_0 to q_{n+1}
L2  for i ← 1 to I do
L3      for t ← 1 to n do g_t ← Σ_j c′(D_j(q_t)) ∇D_j(q_t)     ▷ obstacle gradient
L4      g ← g + λ (A ξ + b)                                  ▷ add smoothness gradient
L5      if ‖g‖ ≤ tol then return ξ
L6      solve A δ = g                                        ▷ tridiagonal, per coordinate
L7      ξ ← ξ - δ / η
L8  return ξ
```

Line L1 is the usual start: the straight line, even if it passes through obstacles. Line L3 is the gradient of the obstacle cost at each waypoint. With a distance field on a grid, $\nabla D$ comes from finite differences. The paper's speed-weighted version projects this gradient across the direction of motion and adds a curvature term (equation (12)); the plain sum used here does not need that. Line L4 adds the gradient of the smoothness term.

Lines L6 and L7 are the covariant step $\xi \leftarrow \xi - \frac1\eta A^{-1}\nabla U$ (equation (19)). It is the minimizer of the first-order model of $U$ plus $\frac\eta2 \|\xi - \xi_i\|_A^2$, a penalty on the change measured in the norm of the smoothness matrix instead of the Euclidean norm (equation (18)). Multiplying by $A^{-1}$ turns a gradient that is large at one waypoint into a smooth bump over the whole trajectory, and keeps the ends fixed. $A$ is tridiagonal, so line L6 costs $O(n)$ per coordinate with the [Thomas algorithm](/tridiagonal-system-solving/). Line L5 is the stopping test of the paper (Section 3.5): the gradient is small.

## Example

A point moves from $(-1, 0)$ to $(1, 0)$ with $n = 19$ waypoints ($\Delta t = 0.05$). One disc of radius $0.5$ has its center at $(0, -0.15)$, so the straight line cuts it $0.35$ deep. The weights are $\lambda = 0.02$ and $\varepsilon = 0.2$, and $\eta = 0.5276$ is the safe value from the proof.

| iteration | $U$ | smallest clearance | length | height of the middle waypoint |
|---|---|---|---|---|
| 0 | 3.85586 | $-0.350$ | 2.0000 | 0.0000 |
| 1 | 2.96117 | $-0.235$ | 2.0154 | 0.1147 |
| 2 | 2.06933 | $-0.109$ | 2.0697 | 0.2415 |
| 5 | 1.08020 | 0.137 | 2.2692 | 0.4871 |
| 10 | 1.06948 | 0.160 | 2.2865 | 0.5097 |
| 50 | 1.06187 | 0.169 | 2.2878 | 0.5193 |
| 349 | 1.06162 | 0.170 | 2.2883 | 0.5195 |

The trajectory leaves the disc within five steps, over the side away from the center, and stops after 349 iterations with $\|g\| \le 10^{-6}$. It keeps a clearance of $0.17$, just inside the band $\varepsilon = 0.2$ where the obstacle cost starts, because the smoothness term pulls it back toward the disc. The shortest path around the disc is about $2.134$ long; CHOMP's path is longer because it trades length for clearance.

If the disc is centered on the line, at $(0, 0)$, the problem is symmetric. Every gradient has a zero component across the line, the waypoints never leave the axis, and CHOMP stops in collision. Moving the start line up by $0.001$ is enough: the run then ends above the disc with a clearance of $0.16$.

## Correctness

CHOMP is a local descent method. The result proved in the [proof](proofs/correctness.md) is about the decrease of $U$, not about collisions. If $\eta \ge L = \lambda + m/(\varepsilon\mu)$, where $m$ is the number of discs and $\mu = 4\sin^2(\pi/(2(n+1)))/\Delta t^2$ is the smallest eigenvalue of $A$, then every step decreases $U$ by at least $\frac1{2\eta} g^{\mathsf T} A^{-1} g$. So $U$ never increases, and the smallest covariant gradient norm in the first $K$ steps is at most $2\eta U(\xi_0)/K$. The key fact is that each obstacle term is a function with a $1/\varepsilon$-Lipschitz gradient plus a concave function, so the usual descent bound holds even through the center of the disc, where the distance has no gradient. The limit is a stationary point. It need not be a minimum and need not be free of collision, as the symmetric example shows. Zucker et al. (Section 3.5) say the same: CHOMP can stop with a trajectory in collision, and cannot report that no free path exists.

## Complexity

One iteration evaluates the distance and its gradient at every body point of every waypoint, $O(nm)$ work for $m$ obstacle terms per waypoint, and solves a tridiagonal system for each of the $d$ coordinates, $O(nd)$. So one iteration costs $O(n(d + m))$, and the memory is $O(nd)$. With a precomputed distance field each distance query is $O(1)$; computing the field is a separate cost, done once per scene by a [distance transform](/distance-transform/).

The convergence result above bounds the gradient after $K$ iterations by $O(1/\sqrt K)$ in the covariant norm, which says nothing about how many iterations it takes to leave all obstacles. The 349 iterations of the example are a measurement.

## Properties

- **Local.** It finds a stationary point near the start. The result depends on the start line and on the weights.
- **Monotone with a safe step.** With $\eta \ge L$, the objective never increases (theorem, for the plain obstacle sum).
- **Smooth updates.** Each update is $A^{-1}$ applied to a vector, so it is smooth and keeps the ends fixed.
- **Starts from infeasible trajectories.** The obstacle cost grows linearly inside obstacles, so it pushes waypoints out even when they start inside.
- **Invariant to timing.** The paper's speed-weighted obstacle term does not change when the path is followed at a different speed (Section 3.1). The plain sum used here is not invariant in this way.
- **No feasibility guarantee.** It can stop in collision, and it cannot detect that no path exists.

## Variants and improvements

- **Weight scheduling.** Give most of the weight to the obstacle term first, and increase the smoothness weight once the trajectory is out of collision (Section 3.6). The paper reports that this helps convergence.
- **Hamiltonian Monte Carlo.** Add random momentum to the iterates so that the method can leave a poor local minimum. Zucker et al. use this to make CHOMP probabilistically complete in the limit.
- **Constraints and goal sets.** Project each step onto linearized equality constraints in the metric $A$, which also lets the goal be any point of a goal set (Section 6).
- **Other metrics.** Use accelerations or jerks in $F_{\text{smooth}}$; $A$ becomes pentadiagonal or wider.
- **Related methods.** [STOMP](/stomp/) uses the same smoothness metric to shape random samples and needs no gradient. [TrajOpt](/sequential-convex-trajectory-optimization/) treats collision as a constraint and uses a trust region. [GPMP2](/gaussian-process-motion-planning/) uses a Gaussian process prior in place of $A$.

## When to use it

Use CHOMP for arms in structured scenes such as tables and shelves, when a distance field is available and a smooth motion is wanted fast, or to smooth and improve the output of a sampling planner. Do not use it alone for maze-like problems with narrow passages, where a local method fails; use a [sampling planner](/rapidly-exploring-random-tree/) there and CHOMP after it.

## Pitfalls

- **Symmetric starts.** If the straight line of line L1 passes through the middle of an obstacle, the gradients of line L3 can cancel across the line and the trajectory never leaves the obstacle. Perturb the start or start from several lines.
- **The stopping test is not a feasibility test.** Line L5 stops on a small gradient, also in collision. Check the clearance of the result before using it.
- **A step that is too large.** If $\eta$ in line L7 is too small, the step overshoots and $U$ can grow or oscillate. The bound $L$ is safe but conservative; a line search on $U$ is an alternative.
- **Gradients from a coarse field.** Line L3 with finite differences on a coarse distance grid gives noisy gradients near obstacle surfaces and zero gradients far from them, so thin obstacles can be missed between grid cells and between waypoints.
- **Weights.** The balance of $\lambda$ and $\varepsilon$ decides the clearance and the length. The paper tunes its parameters on a set of training problems (Section 7.1.1). There is no rule that works for every scene.

## Implementations

## History

Nathan Ratliff, Matt Zucker, Andrew Bagnell and Siddhartha Srinivasa presented CHOMP at ICRA 2009. The journal version names the elastic band of [Quinlan and Khatib](/elastic-bands/) as a forerunner; CHOMP differs in measuring the obstacle cost in the workspace and in taking its steps in the smoothness metric. The journal version by Zucker et al. (2013) added Hamiltonian Monte Carlo, constraints, goal sets and experiments on the HERB robot, where CHOMP solved about 80% of a set of grasping problems in clutter (a measurement, Section 7.1.2). CHOMP was one of the first trajectory optimizers used as a general motion planner, and was followed by [STOMP](/stomp/) (2011), [TrajOpt](/sequential-convex-trajectory-optimization/) (2013) and [GPMP2](/gaussian-process-motion-planning/).

## References
