---
tag: N80C35
kind: problem
slug: time-optimal-path-parameterization
name: Time-optimal path parameterization
aliases:
- TOPP
- time-optimal path tracking
area: robotics/trajectory-generation
level: core
summary: "Find the fastest time scaling of a fixed path under joint torque, velocity and acceleration limits."
prereqs: [time-scaling, manipulator-equation]
see_also: [maximum-velocity-curve, bobrow-time-optimal-algorithm, topp-reachability-analysis, convex-time-optimal-path-parameterization, time-optimal-control, bang-bang-control, trajectory-generation-problem, feedrate-scheduling]
sources:
  - paper: doi:10.1177/027836498500400301
    title: "James E. Bobrow, Steven Dubowsky and John S. Gibson, Time-optimal control of robotic manipulators along specified paths, The International Journal of Robotics Research 4(3), 1985, 3-17"
    locator: "the whole paper (the reduction to the phase plane and the bang-bang structure)"
  - paper: doi:10.1109/TAC.1985.1104009
    title: "Kang G. Shin and Neil D. McKay, Minimum-time control of robotic manipulators with geometric path constraints, IEEE Transactions on Automatic Control 30(6), 1985, 531-541"
    locator: "the whole paper (the same reduction, found at the same time)"
  - paper: doi:10.1109/TAC.2009.2028959
    title: "Diederik Verscheure, Bram Demeulenaere, Jan Swevers, Joris De Schutter and Moritz Diehl, Time-optimal path tracking for robots: a convex optimization approach, IEEE Transactions on Automatic Control 54(10), 2009, 2318-2327"
    locator: "the whole paper (the convex reformulation in b = s'^2)"
  - paper: doi:10.1109/TRO.2018.2819195
    title: "Hung Pham and Quang-Cuong Pham, A new approach to time-optimal path parameterization based on reachability analysis, IEEE Transactions on Robotics 34(3), 2018, 645-659"
    locator: "Section IV-D (the costs of the three approaches) and Section V (experiments)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 9.4 (time-optimal time scaling)"
---

Time-optimal path parameterization asks how fast a machine can move along a curve that is already fixed. A machine with several motors, such as a robot arm, a machine tool or a vehicle, must follow a given geometric path, and each motor can give only a limited force or torque. The question is the timing: at each point of the path, how fast to go, so that the whole path takes the least time and no motor is ever asked for more than it can give. Because the path is fixed, the state of the whole machine collapses to two numbers, the position $s$ along the path and the speed $\dot s$, and every motor limit becomes a limit on the path acceleration $\ddot s$ that depends on $s$ and $\dot s$. The answer has a simple shape: the machine always speeds up or slows down as hard as it can, and switches between the two at a few points. Three families of methods compute it: integration of the extreme curves ([Bobrow](/bobrow-time-optimal-algorithm/)), a sequence of small linear programs ([reachability analysis](/topp-reachability-analysis/)), and one convex program ([convex formulation](/convex-time-optimal-path-parameterization/)). The problem is the time-optimal case of the [trajectory generation problem](/trajectory-generation-problem/), and the robotic counterpart of [feedrate scheduling](/feedrate-scheduling/) for machine tools.

## In plain words

Think of driving a car on a winding road that you must follow exactly. You want to reach the end as soon as possible. On a straight piece you push the pedal down. Before a sharp bend you must brake early enough to enter it at a safe speed. The best driver is always either at full throttle or at full brake, and the art is to know where to switch. A robot arm on a fixed path has the same choice, but its limits are more complex: how hard it can speed up depends on where it is on the path and on how fast it already goes, because the motors must also fight the swinging of the arm. The problem asks for the switch points and the speed at every point of the path.

## Definition

**Input.**

- A path $q : [0, 1] \to \mathbb R^n$ in the joint space of a robot with $n$ joints, twice differentiable, with $q_s = dq/ds$ and $q_{ss} = d^2 q/ds^2$.
- The dynamics in the form of the [manipulator equation](/manipulator-equation/) $\tau = M(q)\ddot q + C(q, \dot q)\dot q + g(q)$, and limits $\tau_{\min} \le \tau \le \tau_{\max}$. Joint velocity and acceleration limits can be added.
- The path speeds at the two ends, $\dot s(0)$ and $\dot s(1)$, usually zero (rest to rest).

Along the path, $\dot q = q_s \dot s$ and $\ddot q = q_s \ddot s + q_{ss} \dot s^2$. Write $x = \dot s^2$ and $u = \ddot s$. Then

$$\tau = M(q) q_s\, u + \left(M(q) q_{ss} + C(q, q_s) q_s\right) x + g(q),$$

so each torque limit is a row $\ell \le a(s) u + b(s) x + c(s) \le h$ that is linear in $(u, x)$. A joint velocity limit $|q_{s,j}\dot s| \le v_j$ is the row $q_{s,j}^2 x \le v_j^2$. A joint acceleration limit is $|q_{s,j} u + q_{ss,j} x| \le a_j$. The squared speed obeys $dx/ds = 2u$.

**Output.** A time scaling $s(t)$, given as a profile $x(s) \ge 0$ with the end values from the input, such that at almost every $s$ the pair $(u, x)$ with $u = \tfrac12\,dx/ds$ meets every row, and the traversal time

$$T = \int_0^1 \frac{ds}{\sqrt{x(s)}}$$

is as small as possible. If no admissible profile exists, report that.

At each point $s$, the rows give an interval $[L(s, x), U(s, x)]$ of admissible $u$. The largest $x$ where this interval is not empty is the [maximum velocity curve](/maximum-velocity-curve/) $\mathrm{MVC}(s)$. Every admissible profile stays at or below it.

**The bang-bang structure.** Bobrow, Dubowsky and Gibson (1985) and Shin and McKay (1985) showed that an optimal profile has, at almost every $s$, either $u = U(s, x)$ (full acceleration) or $u = L(s, x)$ (full braking), except where it runs along the MVC. The switches from braking to acceleration happen on the MVC. Lynch and Park (Section 9.4) present the same result. The proof on the [Bobrow page](/bobrow-time-optimal-algorithm/) compares any admissible profile with the extreme curves; it needs the rows to meet some regularity conditions, and it fails at singular points where a coefficient $a_j(s)$ of the active row is zero (see Variants).

## Variants

- **Discretized.** The limits are imposed only at the points of a grid $s_0 < \dots < s_N$, with $u$ constant on each interval. This is the form solved by the [reachability method](/topp-reachability-analysis/) and the [convex formulation](/convex-time-optimal-path-parameterization/). The limits then hold between grid points only up to an error that shrinks with the grid step.
- **With velocity limits.** Joint velocity limits add a second ceiling to the MVC that does not depend on $u$. The profile can then run along the ceiling for a whole stretch.
- **With singular points.** At points where the coefficient of $u$ in an active row is zero (zero-inertia points), the limits on $u$ jump, the optimal profile can follow the MVC on a singular arc, and the integration method often fails there. Pham (2014) analyzes these failures; see also [singular arcs](/singular-arc/) in optimal control.
- **Penalized.** Minimize $T$ plus a cost on torques or on the rate of torque change, so that the profile is smoother. The [convex formulation](/convex-time-optimal-path-parameterization/) allows convex penalties.
- **With jerk or torque-rate limits.** These limits involve $d u/ds$ and break the linear structure in $(u, x)$; the problem is then no longer convex in the same variables.
- **Admissible velocity propagation.** Instead of one optimal profile, compute the set of all reachable end speeds, for use inside a [kinodynamic planner](/kinodynamic-planning/). The reachability method does this as a by-product.

## Examples

**One axis.** For $q(s) = s$ with $|\dot q| \le 1$ and $|\ddot q| \le 2$, rest to rest, the rows are $-2 \le u \le 2$ and $x \le 1$. The optimal profile accelerates at $u = 2$ up to $x = 1$ at $s = 1/4$, runs at $x = 1$, and brakes at $u = -2$ from $s = 3/4$. This is the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) with $T = 1.5$. Without the velocity limit, the two extreme curves $x = 4s$ and $x = 4(1 - s)$ meet at $s = 1/2$, and $T = \sqrt 2 \approx 1.41421$.

**A 2R arm.** A planar arm with unit links, unit point masses at the link ends and no gravity follows the straight joint path from $(0, 0)$ to $(2, -3)$ with $|\tau_1| \le 10$ and $|\tau_2| \le 4$. Some values of the MVC (in $x = \dot s^2$):

| $s$ | 0 | 0.1 | 0.2 | 0.3 | 0.35 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---|---|---|---|---|---|---|---|---|
| $\mathrm{MVC}(s)$ | infinite | 6.444 | 2.893 | 1.570 | 1.156 | 1.218 | 1.703 | 3.037 | 15.79 |

At $s = 0$ the arm is stretched out, so the Coriolis and centrifugal terms vanish; the path is a straight line in joint space, so $q_{ss} = 0$; then $u = 0$ is admissible at every speed, and the MVC has no limit there. The optimal profile accelerates to $s \approx 0.239$, brakes to touch the MVC near its minimum at $s \approx 0.349$, accelerates again to $s \approx 0.731$, and brakes to rest. The minimum time is about $1.5106$. The three methods agree: $1.51065$ for the integration method with step $0.001$, $1.51056$ for the reachability method with 2000 grid intervals, and $1.50555$ for the convex formulation with 50 intervals, where the coarse grid checks the limits at fewer points.

## Known algorithms

- **Numerical integration** ([Bobrow-Dubowsky-Gibson algorithm](/bobrow-time-optimal-algorithm/), also by Shin and McKay). Integrate the curve of full braking back from the end and the curve of full acceleration forward from the start. Where the forward curve hits the MVC, search the MVC for the next switch point and integrate from there. Fast, and exact up to the integration error, but fragile at singular points.
- **Reachability analysis** ([TOPP-RA](/topp-reachability-analysis/)). On a grid of $N$ intervals, compute backward the sets of speeds from which the end can still be reached, each with a few small [linear programs](/linear-programming-problem/), then go forward greedily. Time $O(mN)$ for $m$ rows; it never fails when the discretized problem is feasible.
- **Convex optimization** ([convex formulation](/convex-time-optimal-path-parameterization/)). With $b = \dot s^2$ as the variable, the discretized problem is convex and can be written as a [second-order cone program](/second-order-cone-programming/). An [interior point method](/interior-point-method/) gives the optimum of the discretized problem up to a chosen tolerance, and convex penalties can be added.
- **Dynamic programming** on a grid of $(s, \dot s)$ values. Simple, but the cost grows with the product of the two grid sizes, and the answer is only as fine as the speed grid.

## Bounds

- **Lower bound from the MVC.** Every admissible profile has $x(s) \le \mathrm{MVC}(s)$, so $T \ge \int_0^1 ds/\sqrt{\mathrm{MVC}(s)}$. The bound is often weak: for the 2R arm above it is about $0.623$, while the optimum is about $1.511$, because the arm cannot reach the MVC from rest.
- **One axis.** For one axis with $|\dot q| \le V$ and $|\ddot q| \le A$ over a distance $D$, the optimum is $D/V + V/A$ if $D \ge V^2/A$, and $2\sqrt{D/A}$ otherwise.
- **Computation.** For a grid of $N$ intervals with $m$ rows per point, the reachability method takes $O(mN)$ time (Pham and Pham 2018, Section IV-D). The discretized problem is a second-order cone program, so interior point methods solve it in polynomial time; each Newton step of a direct implementation costs $O(N + M)$ for $M$ constraints, thanks to the tridiagonal structure of the problem. The integration method takes $O(m/h)$ time per curve with step $h$, times the number of curves.
- **Discretization error.** With limits checked only at grid points, the result can break a limit between grid points by an amount of order $\Delta$, the grid step. Pham and Pham give an $O(\Delta)$ bound for the collocation form and $O(\Delta^2)$ for a first-order interpolation form.

## Reductions

- **Path tracking to a one-dimensional system.** A fixed path reduces the $n$-joint dynamics to the double integrator $\ddot s = u$ with state-dependent bounds on $u$. TOPP is then [time-optimal control](/time-optimal-control/) of this system, and the [Pontryagin maximum principle](/pontryagin-maximum-principle/) predicts the [bang-bang](/bang-bang-control/) form.
- **To a convex program.** The change of variables $b = \dot s^2$, $a = \ddot s$ makes the limits linear and the time $\int ds/\sqrt b$ convex (Verscheure et al. 2009).
- **To linear programs in two variables.** Each step of the reachability method is a pair of linear programs over the admissible polygon at one grid point.
- **Straight line with box limits to a trapezoid.** For $q(s) = q_0 + s\Delta q$ with constant velocity and acceleration limits per joint, every row reduces to a constant bound on $\dot s$ or $\ddot s$, and the answer is a trapezoid in $s$.
- **Path-velocity decomposition.** A planner chooses a path that avoids obstacles; TOPP then gives the timing. With moving obstacles the timing must also avoid regions of the plane of $s$ and $t$; see [path-velocity decomposition](/path-velocity-decomposition/).

## Applications

Industrial robots use TOPP to shorten cycle times on pick-and-place and welding paths. Sampling-based planners call it to time the paths they find, and some planners use the reachable speed sets to test kinodynamic feasibility. Legged and humanoid robots apply the same reduction with contact force limits along a planned center of mass path. Vehicles and machine tools use the same idea for speed planning along a road or tool path with limits on lateral acceleration or feed force.

## References
