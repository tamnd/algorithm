---
tag: HBHW2D
kind: algorithm
slug: topp-reachability-analysis
name: Time-optimal path parameterization by reachability analysis
aliases:
- TOPP-RA
area: robotics/trajectory-generation
level: research
summary: "Discretizes the path and solves small two-variable LPs, backward for the controllable sets and forward for the greedy profile; no switch points to find."
solves: [time-optimal-path-parameterization]
model: real-ram
complexity:
  vars: {N: "the number of grid intervals", m: "the number of constraint rows at a grid point"}
  time: {worst: O(N m^2)}
  space: {extra: Θ(N)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [time-optimal-path-parameterization, maximum-velocity-curve, linear-programming-problem]
see_also: [bobrow-time-optimal-algorithm, convex-time-optimal-path-parameterization, fourier-motzkin-elimination, seidel-linear-programming, trapezoidal-velocity-profile, time-scaling, kinodynamic-planning, model-predictive-control]
sources:
  - paper: doi:10.1109/TRO.2018.2819195
    title: "Hung Pham and Quang-Cuong Pham, A new approach to time-optimal path parameterization based on reachability analysis, IEEE Transactions on Robotics 34(3), 2018, 645-659 (arXiv 1707.07239)"
    locator: "Algorithm 1 (TOPP-RA); Section IV-B, Theorem 1 (correctness); Section IV-C, Theorems 2 and 3 (optimality); Section IV-D (complexity); Section V (experiments)"
  - paper: doi:10.1109/TRO.2014.2351113
    title: "Quang-Cuong Pham, A general, fast, and robust implementation of the time-optimal path parameterization algorithm, IEEE Transactions on Robotics 30(6), 2014, 1533-1540"
    locator: "the whole paper (the integration method, its failure modes at singular points, and the velocity limits)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 9.4 (time-optimal time scaling, the phase plane and the limits on s'')"
---

TOPP-RA computes the fastest way to move a robot along a fixed path when the motors have torque, velocity or acceleration limits. It cuts the path into $N$ short pieces and works with the squared path speed $x = \dot s^2$ at the grid points. A backward pass finds, at each grid point, the interval $K_i$ of speeds from which the robot can still reach the end of the path without breaking a limit; each interval is the projection of a polygon and costs one small [linear program](/linear-programming-problem/) in two variables. A forward pass then starts at rest and, at each grid point, takes the largest acceleration that keeps the next speed inside the next interval. The result is an admissible profile whenever one exists (a theorem), and it is time-optimal for the discretized problem when the grid is fine enough and the path has no zero-inertia points (a theorem with these conditions). Unlike the [integration method of Bobrow](/bobrow-time-optimal-algorithm/), it never has to find switch points or follow singular arcs, which is where integration codes fail. It is the method of Pham and Pham (2018). The path itself is an input and is not changed.

## In plain words

A robot must drive along a fixed road as fast as it can. Its engine and brakes are limited, and the limits change along the road. Work backward from the finish: at each mile marker, find the range of speeds from which the robot can still slow down in time for every later marker. Near the finish this range is small; further back it is larger. Then drive forward from the start. At each marker, press the pedal as hard as you can, but not so hard that you land outside the safe range at the next marker. Because each range was built to guarantee a safe future, the robot never gets stuck, and the greedy choice gives a fast profile. Each range comes from a tiny geometry problem with two unknowns, so the method is fast and does not depend on delicate root finding.

## The problem

Input: a path $q(s)$ in joint space with $s \in [0, 1]$, a grid $0 = s_0 < s_1 < \dots < s_N = 1$ with steps $\Delta_i = s_{i+1} - s_i$, the squared speeds $x_{\text{start}}$ and $x_{\text{end}}$ at the ends (zero for rest to rest), and at each grid point a set of constraint rows

$$\ell \le a\, u + b\, x + c \le h,$$

where $u = \ddot s$ is the path acceleration and $x = \dot s^2$. The admissible set $\Omega_i$ is the polygon of pairs $(u, x)$ that meet every row at $s_i$ and have $x \ge 0$. Joint torque limits have this form: along the path the [manipulator equation](/manipulator-equation/) gives $\tau = M q_s u + (M q_{ss} + C(q, q_s) q_s) x + g(q)$, with $q_s = dq/ds$. A joint velocity limit is the row $q_{s,j}^2 x \le v_j^2$, and a joint acceleration limit is $|q_{s,j} u + q_{ss,j} x| \le a_j$.

The control is constant on each interval, so $x_{i+1} = x_i + 2\Delta_i u_i$, which is the exact relation $d(\dot s^2)/ds = 2\ddot s$. Output: an admissible profile $(u_i, x_i)$ with $(u_i, x_i) \in \Omega_i$ and the given end speeds, with a traversal time $T = \sum_i 2\Delta_i / (\sqrt{x_i} + \sqrt{x_{i+1}})$ that is as small as the method can make it, or "infeasible". Checking the limits only at the grid points is the collocation discretization of the paper; between grid points the limits hold only up to an error of $O(\Delta)$.

## The algorithm

```pseudo id=main
TOPP-RA(s_0..s_N, Ω_0..Ω_N, x_start, x_end)
L1  K_N ← [x_end, x_end]
L2  for i ← N-1 down to 0 do
L3      K_i ← { x : some u has (u, x) ∈ Ω_i and x + 2Δ_i u ∈ K_{i+1} }   ▷ two LPs
L4      if K_i = ∅ then return INFEASIBLE
L5  if x_start ∉ K_0 then return INFEASIBLE
L6  x_0 ← x_start
L7  for i ← 0 to N-1 do
L8      u_i ← max { u : (u, x_i) ∈ Ω_i and x_i + 2Δ_i u ∈ K_{i+1} }
L9      x_{i+1} ← x_i + 2Δ_i u_i
L10 return (u, x)
```

$K_i$ is the controllable set at $s_i$: the squared speeds from which some admissible sequence of controls reaches $x_{\text{end}}$ at $s_N$. Line L1 starts with the single end speed. Line L3 computes $K_i$ from $K_{i+1}$. The set of $(u, x)$ in $\Omega_i$ that land in $K_{i+1}$ is a convex polygon, and $K_i$ is its shadow on the $x$ axis, so $K_i$ is an interval whose ends are the solutions of two linear programs in $(u, x)$: minimize $x$ and maximize $x$. The code finds both ends at once by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) of $u$: every pair of a lower and an upper bound on $u$ gives one linear inequality in $x$. Line L4 stops if a set is empty, line L5 if the start speed cannot be controlled to the end. The upper end of $K_i$ is never above the [maximum velocity curve](/maximum-velocity-curve/), and it is lower wherever the robot must already brake for a later part of the path.

The forward pass, lines L6 to L9, is greedy. Line L8 picks the largest $u$ that is admissible at the current state and keeps the next state controllable. This is a linear program in one variable: an intersection of intervals of $u$. Because $x_i \in K_i$, the set is never empty, so the forward pass cannot get stuck.

## Example

**One axis, trapezoid.** The path $q(s) = s$ with $|\dot q| \le 1$ and $|\ddot q| \le 2$ gives the rows $|u| \le 2$ and $x \le 1$. On the grid $s_i = i/4$, rest to rest:

| $i$ | $s_i$ | $K_i$ (backward) | $x_i$ (forward) | $u_i$ |
|---|---|---|---|---|
| 0 | 0 | $[0, 1]$ | 0 | 2 |
| 1 | 0.25 | $[0, 1]$ | 1 | 0 |
| 2 | 0.5 | $[0, 1]$ | 1 | 0 |
| 3 | 0.75 | $[0, 1]$ | 1 | $-2$ |
| 4 | 1 | $[0, 0]$ | 0 | |

At $i = 3$ the next set is $\{0\}$, so line L3 needs $x + 0.5u = 0$ with $|u| \le 2$, which allows $x \le 1$. Going forward, line L8 at $i = 0$ takes $u = 2$ and reaches the speed limit $x = 1$; at $i = 1$ and $i = 2$ any $u > 0$ would leave $K_{i+1}$, so $u = 0$; at $i = 3$ the only choice is $u = -2$. The time is $0.5 + 0.25 + 0.25 + 0.5 = 1.5$, which is exactly the minimum time of the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) with $D = 1$, $V = 1$, $A = 2$. Without the velocity limit the result is the triangle with $T = \sqrt 2 \approx 1.41421$ on any even grid.

**A 2R arm.** The planar arm with unit links, unit point masses at the link ends and no gravity has $M = [[3 + 2\cos q_2, 1 + \cos q_2], [1 + \cos q_2, 1]]$. It moves on the straight joint path from $(0, 0)$ to $(2, -3)$ with $|\tau_1| \le 10$ and $|\tau_2| \le 4$. The times on uniform grids are:

| $N$ | 10 | 20 | 50 | 100 | 200 | 1000 | 2000 |
|---|---|---|---|---|---|---|---|
| $T$ | 1.47772 | 1.49564 | 1.50580 | 1.50846 | 1.50961 | 1.51046 | 1.51056 |

The time grows toward about 1.5106 because a coarse grid checks the limits at fewer points and is therefore optimistic. On the grid with $N = 200$ the profile accelerates until $s \approx 0.24$, brakes to touch the maximum velocity curve at $s = 0.35$ (where $x = 1.1556$, a corner of the curve), moves with a small acceleration until $s \approx 0.73$, and then brakes to rest. The largest violation of a torque limit at a grid point is about $4 \cdot 10^{-15}$, and multiplying the profile by 1.01 breaks a limit.

## Correctness

Theorem (Pham and Pham 2018, Theorem 1): the algorithm returns an admissible profile of the discretized problem if one exists, and "infeasible" otherwise. The proof shows by backward induction that $K_i$ is exactly the set of speeds with an admissible future, and that line L3 computes it exactly because the shadow of a polygon is given by Fourier-Motzkin elimination. The forward pass keeps $x_i \in K_i$, so line L8 always has a choice, and the last state is $x_{\text{end}}$. See the [proof](proofs/correctness.md).

Optimality is a separate result. Pham and Pham prove (Theorem 2) that if the path has no zero-inertia points, which are points where the coefficient $a$ of $u$ in a torque row is zero, then there is a step threshold below which the greedy profile is time-optimal for the discretized problem; with zero-inertia points the excess time is $O(\Delta)$ (Theorem 3). The greedy pass is not optimal for every grid. On the 2R example with $N = 10$, the [convex formulation](/convex-time-optimal-path-parameterization/) of the same discretized problem reaches $T = 1.46762$, which is 0.7% faster than the greedy $1.47772$; with $N = 50$ the gap is 0.02%, and with $N = 200$ it is about $10^{-5}$ (measurements). The tests compare it with a brute force over a lattice of states with a margin of a few percent and check exact values only on the single axis.

## Complexity

The backward pass solves $N$ problems of the form "shadow of a polygon with $m + 3$ edges". Fourier-Motzkin elimination of one variable forms $O(m^2)$ rows, so the code takes $O(m^2)$ per grid point. A two-variable linear program can be solved in $O(m)$ time ([Seidel's algorithm](/seidel-linear-programming/) in expected time, or Megiddo's deterministic algorithm), which gives $O(mN)$ in total; Pham and Pham state $O(mN)$ for this reason and use a [simplex](/simplex-method/) solver in practice. The forward pass is $O(m)$ per point. Memory is $\Theta(N)$ for the sets and the profile, plus the rows. For comparison, the paper gives $O(m^2 N)$ for the integration method and a higher cost for the convex formulation solved as one large program.

## Properties

- **Complete for the discretized problem.** A theorem: it finds an admissible profile if one exists.
- **Optimal under conditions.** A theorem with hypotheses: for a fine enough grid and no zero-inertia points; otherwise within $O(\Delta)$.
- **No switch points.** The method never searches for switch points or tangent points, and it treats velocity limits, singular arcs and zero-inertia points in the same way as any other constraint.
- **Controllable sets come for free.** The sets $K_i$ tell, for any state on the path, whether the robot can still stop in time. This is useful for replanning and for feedback.
- **Discretization error.** Limits hold at the grid points only. A finer grid or the first-order interpolation scheme of the paper (Appendix D, error $O(\Delta^2)$) reduces the error.
- **Measured performance.** The paper reports a 100% success rate on its test paths. This is a measurement on their benchmarks, not a bound.

## Variants and improvements

- **Interpolation discretization.** Requiring the constraints also at the next grid point with the same control tightens each step and reduces the error from $O(\Delta)$ to $O(\Delta^2)$ (Pham and Pham, Appendix D).
- **Admissible velocity propagation.** The same sets, propagated forward instead of backward, give the range of final speeds that a path can reach. Planners that build paths piece by piece use this to prune, as in [kinodynamic planning](/kinodynamic-planning/).
- **Second-order cone constraints.** Limits on the norm of a vector of torques or forces, such as friction cones, make $\Omega_i$ convex but not polygonal; each step is then a small [second-order cone program](/second-order-cone-programming/).
- **Other methods for the same problem.** The [Bobrow integration method](/bobrow-time-optimal-algorithm/) integrates the phase plane; the [convex formulation of Verscheure et al.](/convex-time-optimal-path-parameterization/) solves one large convex program for the whole grid.

## When to use it

Use TOPP-RA when you need a reliable time-optimal parameterization of a given path in a robot controller or a planner: industrial arms with torque and velocity limits, paths with friction or contact constraints, and real-time retiming in the loop. Use the integration method when you want the switch points explicitly and the path has no singular arcs. Use the convex formulation when you want a different objective, such as time plus a penalty on torque, which TOPP-RA cannot handle because the greedy pass only maximizes speed.

## Pitfalls

- **A coarse grid is optimistic.** Line L3 checks the limits only at the grid points, so the true limits are broken between them. In the 2R example the time on 10 intervals is about 2% too small. Use a fine grid or the interpolation scheme, and check the final profile on a finer grid.
- **Rounding at the set bounds.** In floating point, line L9 can land slightly above the upper end of $K_{i+1}$ or slightly below zero. Then line L8 at the next point finds an empty set. The code accepts a small relative tolerance and clamps $x$ at zero.
- **End speeds that are not admissible.** $x_{\text{end}}$ must satisfy the rows at $s_N$, and a nonzero $x_{\text{start}}$ must be in $K_0$. Line L5 returns "infeasible" for a start that is too fast to stop, which is the correct answer but can surprise a caller that expects a slower profile.
- **Taking any admissible $u$ in line L8.** Every $u$ in the set keeps the profile admissible, but only the largest makes it fast. Picking the middle of the interval, for robustness, gives a valid but slow profile.
- **Expecting exact optimality.** The greedy profile is optimal only under the conditions of Theorem 2. Near zero-inertia points it can be slower by $O(\Delta)$.

## Implementations

## History

The phase-plane method of Bobrow, Dubowsky and Gibson and of Shin and McKay (1985) solved the problem by integrating curves and finding switch points. Pfeiffer and Johanni (1987) and later Pham (2014) showed that the integration method needs special care at singular and zero-inertia points, where implementations often failed. Earlier, the convex formulation of Verscheure et al. (2009) removed the switch points at the cost of one large optimization. Hung Pham and Quang-Cuong Pham (2018) borrowed the idea of reachable and controllable sets from control theory and turned the problem into a sequence of tiny linear programs, which made it both robust and fast. Their open-source library is widely used to retime robot paths.

## References
