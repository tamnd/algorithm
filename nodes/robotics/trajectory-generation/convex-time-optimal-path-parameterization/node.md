---
tag: KKZDAS
kind: algorithm
slug: convex-time-optimal-path-parameterization
name: Convex time-optimal path parameterization
aliases:
- Verscheure's method
area: robotics/trajectory-generation
level: research
summary: "Uses the squared path speed as the variable, so that the fastest timing along a fixed path under torque limits becomes one convex program, solved globally."
solves: [time-optimal-path-parameterization]
model: real-ram
complexity:
  vars: {N: "the number of grid intervals", m: "the number of constraint rows at a grid point", K: "the number of Newton steps"}
  time: {worst: O(K N m)}
  space: {extra: Θ(N m)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [time-optimal-path-parameterization, convex-function, interior-point-method]
see_also: [topp-reachability-analysis, bobrow-time-optimal-algorithm, second-order-cone-programming, barrier-method, kkt-conditions, thomas-algorithm, maximum-velocity-curve, trajectory-optimization]
sources:
  - paper: doi:10.1109/TAC.2009.2028959
    title: "Diederik Verscheure, Bram Demeulenaere, Jan Swevers, Joris De Schutter and Moritz Diehl, Time-optimal path tracking for robots: a convex optimization approach, IEEE Transactions on Automatic Control 54(10), 2009, 2318-2327"
    locator: "the whole paper (the change of variables b = s'^2, the convexity of the problem, the discretization and the second-order cone form)"
  - book: isbn:9780521833783
    title: "Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004"
    locator: "Chapter 11 (interior-point methods, the barrier method and its duality gap) and Chapter 9 (Newton's method)"
  - paper: doi:10.1109/TRO.2018.2819195
    title: "Hung Pham and Quang-Cuong Pham, A new approach to time-optimal path parameterization based on reachability analysis, IEEE Transactions on Robotics 34(3), 2018, 645-659"
    locator: "Section IV-D (comparison of the cost of the convex approach with the reachability approach)"
---

Convex time-optimal path parameterization finds the fastest way to move along a fixed path when the forces that drive the motion are limited, by solving a single convex optimization problem. A robot arm that must follow a given curve can choose only its timing, and with the speed along the path as the unknown, the limits on the motor torques are nonlinear. Verscheure, Demeulenaere, Swevers, De Schutter and Diehl (2009) observed that with the square of the path speed as the unknown, $b = \dot s^2$, every torque limit becomes linear and the traversal time becomes a convex function. After the path is cut into $N$ pieces, the problem is a convex program with about $N$ variables, so a standard [interior point method](/interior-point-method/) finds the global optimum of the discretized problem to any accuracy. There are no switch points to find, unlike in the [integration method of Bobrow](/bobrow-time-optimal-algorithm/). Because the problem is a general convex program, the objective can also include other convex terms, such as a penalty on torque or a smoothness term, which neither the integration method nor the [reachability method](/topp-reachability-analysis/) allows.

## In plain words

Choosing how fast to drive along a fixed road is hard to write down well if you think in terms of speed: the limits on the engine and the brakes depend on the speed in a curved way. If you think in terms of the square of the speed, the same limits become straight lines, and the travel time becomes a bowl-shaped function. Finding the bottom of a bowl inside a region bounded by straight lines is a problem that computers solve reliably: there is only one bottom, and a standard method finds it. So the method cuts the road into many short pieces, writes one unknown per piece, and hands the whole problem to such a solver. The answer is the best timing for that set of pieces, not just a good one.

## The problem

Input: a path $q(s)$ with $s \in [0, 1]$, a grid $0 = s_0 < \dots < s_N = 1$ with steps $\Delta_k$, and at each grid point the constraint rows $\ell \le A a + B b + c \le h$ in the path acceleration $a = \ddot s$ and the squared path speed $b = \dot s^2$. Torque limits have this form: along the path the [manipulator equation](/manipulator-equation/) gives $\tau = M q_s a + (M q_{ss} + C(q, q_s) q_s) b + g(q)$. Rest to rest means $b_0 = b_N = 0$.

The acceleration is constant on each piece, so $b$ is affine in $s$ there and $a_k = (b_{k+1} - b_k)/(2\Delta_k)$. Substituting this removes the $a_k$, and the problem is:

$$\min_{b} \ T(b) = \sum_{k=0}^{N-1} \frac{2\Delta_k}{\sqrt{b_k} + \sqrt{b_{k+1}}} \quad \text{subject to}\quad \ell \le A_k \frac{b_{k+1} - b_k}{2\Delta_k} + B_k b_k + c_k \le h,\ \ b_k \ge 0.$$

$T(b)$ is the exact traversal time of the piecewise-constant acceleration profile. The constraints are linear and $T$ is convex, so this is a [convex](/convex-function/) program. Verscheure et al. rewrite it as a [second-order cone program](/second-order-cone-programming/) with auxiliary variables; this page solves the direct form with a [barrier method](/barrier-method/).

## The algorithm

```pseudo id=main
CONVEX-TOPP(grid, rows, ε)
L1  b ← (0, δ, ..., δ, 0) with δ halved until every limit holds strictly
L2  t ← t_0
L3  repeat
L4      repeat                                          ▷ Newton's method on t T(b) - Σ log(slack_j)
L5          form the gradient and the Hessian of t T(b) - Σ_j log(-g_j(b))   ▷ tridiagonal
L6          solve H d = -gradient by the Thomas algorithm
L7          λ² ← -gradient · d;  if λ²/2 ≤ η then leave the inner loop
L8          step ← 1, halved until b + step d is strictly feasible and the barrier value decreases enough
L9          b ← b + step d
L10     if M / t < ε then return b and a_k = (b_{k+1} - b_k)/(2Δ_k)
L11     t ← μ t
```

The barrier term $-\sum_j \log(-g_j(b))$ is finite only where every one of the $M$ limits holds strictly, so it keeps the iterates inside. Line L1 needs a strictly feasible start; a small constant speed works when every limit holds strictly at rest. Each term of $T$ and each limit involves only $b_k$ and $b_{k+1}$, so the Hessian of line L5 is tridiagonal and line L6 solves it in $O(N)$ time by the [Thomas algorithm](/thomas-algorithm/). Line L7 measures the Newton decrement, line L8 is a backtracking line search, and lines L10 and L11 raise the weight $t$ of the time against the barrier until the duality gap bound $M/t$ is below $\varepsilon$. The code uses $t_0 = 1$, $\mu = 20$ and $\varepsilon = 10^{-9}$.

## Example

**One axis.** $q(s) = s$ with $|\dot q| \le 1$ and $|\ddot q| \le 2$ on the grid $s_k = k/4$. The optimum is $b = (0, 1, 1, 1, 0)$ and $a = (2, 0, 0, -2)$, the [trapezoidal profile](/trapezoidal-velocity-profile/) with $T = 1.5$. The barrier method reaches it to within $2 \cdot 10^{-10}$ in 49 Newton steps. Without the velocity limit, on 8 intervals, it returns the triangle with $T = \sqrt 2$.

**A 2R arm.** The planar arm with unit links, unit point masses at the link ends and no gravity follows the straight joint path from $(0, 0)$ to $(2, -3)$ with $|\tau_1| \le 10$ and $|\tau_2| \le 4$. On 10 intervals the optimum and the greedy profile of TOPP-RA, for the same discretization, are:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $b_k$ (convex) | 0 | 0.500 | 1.028 | 1.165 | 0.877 | 1.408 | 1.031 | 1.029 | 0.829 | 0.324 | 0 |
| $x_k$ (TOPP-RA) | 0 | 0.500 | 1.028 | 1.260 | 1.218 | 0.826 | 0.990 | 1.010 | 0.829 | 0.324 | 0 |

The convex optimum takes $T = 1.46762$ and the greedy profile $1.47772$. The optimum gives up speed at $k = 3$ and $k = 4$ to be much faster at $k = 5$, which the greedy pass cannot see. On 50 intervals the optimum is $1.50555$ (115 Newton steps) and on 200 intervals $1.50960$ (235 Newton steps), where the two methods agree to about $10^{-5}$. The zigzag at $k = 4$ and $k = 5$ is an effect of the coarse grid, not of the robot.

## Correctness

Theorem (Verscheure et al. 2009): with $b = \dot s^2$ the discretized problem is convex. The proof shows that the sum $\sqrt{b_k} + \sqrt{b_{k+1}}$ is concave, so its reciprocal is convex, and that the limits are linear in $b$ once $a$ is eliminated. The barrier method then gives a point that meets every limit strictly and whose time is within $M/t$ of the optimum: at the minimizer of the barrier problem, the numbers $1/(t \cdot \text{slack}_j)$ are Lagrange multipliers that certify this bound by weak duality. See the [proof](proofs/correctness.md). The theorem assumes exact centering; the code stops when the Newton decrement is small, which adds an error of the same order.

The result is the global optimum of the discretized problem, not of the continuous one. Limits hold at the grid points, and the error between grid points is $O(\Delta)$.

## Complexity

One Newton step forms the tridiagonal system in $O(Nm)$ time for $m$ rows per point, solves it in $O(N)$, and each trial of the line search costs $O(Nm)$. For the second-order cone form, interior point theory bounds the number of Newton steps by $O(\sqrt{Nm}\, \log(Nm/\varepsilon))$, which gives $O((Nm)^{1.5} \log(Nm/\varepsilon))$ in total. The direct form used here has no such proven bound, because its barrier is not known to be self-concordant; the measured counts are 49 to 235 steps for $N$ from 4 to 200. Memory is $\Theta(Nm)$ for the rows. A general solver that does not use the band structure pays more per step; Pham and Pham (2018) compare the costs of the approaches.

## Properties

- **Globally optimal for the discretization.** A theorem: the program is convex, so any local optimum is global.
- **Strictly feasible output.** Every iterate meets every limit with a positive margin.
- **Flexible objective.** Any convex term can be added, for example $\sum \|\tau_k\|^2$ to save energy, or a bound on the rate of change of the torque written in $b$.
- **No switch points.** Velocity limits, singular arcs and zero-inertia points need no special treatment.
- **Slower than the reachability method.** For pure minimum time on a fine grid, TOPP-RA gives nearly the same answer with $O(N)$ tiny linear programs.

## Variants and improvements

- **Second-order cone form.** Verscheure et al. introduce auxiliary variables for the square roots and their reciprocals and obtain a second-order cone program, which off-the-shelf solvers accept.
- **Energy and smoothness.** Adding a convex penalty on the torques gives a family of trade-offs between time and effort. Adding a penalty on the change of $a_k$ smooths the jumps of the acceleration.
- **Third-order limits.** A limit on jerk or on the rate of change of torque is not convex in $b$. Adding it needs a nonconvex method, for example a sequence of convex problems built around the one on this page.
- **Other methods for the same problem.** The [Bobrow integration method](/bobrow-time-optimal-algorithm/) and the [reachability method](/topp-reachability-analysis/).

## When to use it

Use the convex formulation when you need the guaranteed optimum of the discretized problem, when the objective has more than the time, or when a general convex solver is already in the system. For pure minimum time in a fast loop, TOPP-RA is cheaper. Combined with a path optimizer, the convex problem also serves as an inner step of [trajectory optimization](/trajectory-optimization/) over both the path and the timing.

## Pitfalls

- **No strictly feasible start.** Line L1 needs a point where every limit holds with a margin. If some limit is active at rest, for example gravity that a motor can only just hold, the barrier is undefined there, and a phase-one problem must find the start.
- **Zigzag on a coarse grid.** As the example shows, the optimum can oscillate from one grid point to the next, because the limits are checked only at grid points. Use a finer grid or limit the change of $a_k$.
- **Hessian near zero speed.** The terms $b_k^{-1/2}$ next to the end points have second derivatives that grow like $b_k^{-5/2}$. Line L5 then has a large spread of values; the Thomas algorithm is stable here because the matrix is positive definite, but the line search of line L8 must still reject steps that make some $b_k$ negative.
- **Stopping on the gap alone.** Line L10 bounds the error only if each centering loop has converged. Stopping a centering loop early, after a fixed number of Newton steps, gives a point that may be farther from the optimum than $M/t$.

## Implementations

## History

Time-optimal path parameterization was solved in 1985 by integration in the phase plane (Bobrow, Dubowsky and Gibson; Shin and McKay). The use of $\dot s^2$ as the state was already standard in that work. Verscheure, Demeulenaere, Swevers, De Schutter and Diehl (2009) showed that in this variable the whole discretized problem is convex, which allowed a general convex solver, a global optimum and additional convex objectives. Pham and Pham (2018) showed that for the pure minimum-time problem a much cheaper sequence of linear programs suffices.

## References
