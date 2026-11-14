---
tag: WEFY9F
kind: problem
slug: feedrate-scheduling
name: Feedrate scheduling
aliases:
- feedrate optimization
- feedrate planning
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Choose the feed along a toolpath to keep cutting force, chip load and machine acceleration and jerk within limits while minimising machining time.
prereqs: [toolpath-planning, time-scaling]
see_also: [time-optimal-path-parameterization, convex-time-optimal-path-parameterization, bobrow-time-optimal-algorithm, maximum-velocity-curve, trapezoidal-velocity-profile, double-s-velocity-profile, parametric-cnc-interpolator, constant-engagement-toolpath]
sources:
  - paper: doi:10.1016/S0890-6955(01)00002-5
    title: Kaan Erkorkmaz and Yusuf Altintas, High speed CNC system design. Part I, jerk limited trajectory generation and quintic spline interpolation, International Journal of Machine Tools and Manufacture 41(9), 1323-1345, 2001
    locator: the jerk-limited feed profile along a toolpath and its use with spline interpolation
  - paper: "J. E. Bobrow, S. Dubowsky and J. S. Gibson, Time-optimal control of robotic manipulators along specified paths, The International Journal of Robotics Research 4(3), 3-17, 1985"
    locator: the phase plane of path position and path speed, and the time-optimal profile by switching between the largest acceleration and the largest deceleration
  - paper: doi:10.1109/TAC.1985.1104009
    title: Kang G. Shin and Neil D. McKay, Minimum-time control of robotic manipulators with geometric path constraints, IEEE Transactions on Automatic Control 30(6), 531-541, 1985
    locator: the minimum-time motion along a fixed path by phase plane methods
  - paper: doi:10.1109/TAC.2009.2028959
    title: Diederik Verscheure, Bram Demeulenaere, Jan Swevers, Joris De Schutter and Moritz Diehl, Time-optimal path tracking for robots, a convex optimization approach, IEEE Transactions on Automatic Control 54(10), 2318-2327, 2009
    locator: the change of variables to the squared path speed that makes the problem convex, and its solution as a second-order cone program
---

Feedrate scheduling is the problem of choosing the speed of the tool along a fixed toolpath. The path comes from the CAM system as a sequence of lines, arcs or splines. The machine must follow it in as little time as possible, but the speed is limited by the programmed feed, by the accuracy of the interpolator, by the acceleration and jerk that the drives can give, and by the load on the cutter. It is the same problem as [time-optimal path parameterization](/time-optimal-path-parameterization/) in robotics, applied to a machine tool. In the language of robotics, a feed schedule is a [time scaling](/time-scaling/) of the path: a function that says where on the path the tool is at each time. The problem is an optimization, and what "optimal" means depends on the model of the limits. For speed and acceleration limits the best schedule has a simple form, with a short proof. With jerk limits or with a model of the cutting force, the problem is harder, and the published gains are measurements on test parts, not theorems.

## In plain words

A machine follows a path drawn by the CAM program, and it has to decide how fast to go at each point. Faster is better, but there are limits. The motors can only speed up or slow down so fast. On a tight bend the machine must slow down, or it overshoots. Some machines also limit how suddenly the acceleration can change, because sudden changes shake the machine. The cutter must not take too big a bite.

The schedule must start slowing down before each bend, early enough to reach the safe speed there. So the planner looks ahead along the path. A simple rule works when only speed and acceleration are limited: speed up as hard as you can, but always stay slow enough that you can still stop in time for every bend ahead.

## Definition

**Input.** A path $C(s)$, $s \in [0, L]$, given by its arc length, with curvature $\kappa(s)$. Limits of these kinds:

- a speed limit $v \le V(s)$ at each point. It includes the programmed feed, the centripetal limit $v^2\kappa \le A_n$, the chord error limit of the interpolator, and a feed limit from the cutting load;
- a tangential acceleration limit $|\dot v| \le A$;
- limits on the acceleration $|\ddot x_i| \le A_i$ of each machine axis $i$;
- a jerk limit $|\dddot s| \le J$, or a jerk limit for each axis;
- the path starts and ends at rest.

**Goal.** Find the speed $v(s) \ge 0$ that satisfies all the limits and minimizes the time $T = \int_0^L ds / v(s)$.

**The squared speed.** Put $b(s) = v(s)^2$. Along the path, $\dot v = v\, dv/ds = b'/2$. The axis acceleration is $\ddot x = C''(s) b + C'(s) b'/2$. So the speed limits, the tangential acceleration limit and the axis acceleration limits are all linear in $b$ and $b'$:
$$
0 \le b \le V(s)^2, \qquad |b'| \le 2A, \qquad |C_i'' b + C_i' b'/2| \le A_i .
$$
The tangential jerk is $\dddot s = \sqrt{b}\, b''/2$, which is not linear.

**The chord error limit.** An interpolator with the period $\tau$ moves the tool along chords of length $v\tau$. On an arc of radius $\rho$ the chord is $\rho - \sqrt{\rho^2 - (v\tau/2)^2}$ away from the arc. To keep this within $\delta$, the speed must satisfy $v \le (2/\tau)\sqrt{2\rho\delta - \delta^2}$. With $\tau = 1$ ms, $\delta = 1\ \mu$m and $\rho = 1$ mm, the limit is 89.4 mm/s, about 5.4 m/min.

## Variants

- **Speed and tangential acceleration only.** The basic CNC look-ahead problem. It has an exact, linear-time solution, given below.
- **Axis limits.** Each machine axis has its own acceleration limit. This is the time-optimal path parameterization problem with linear constraints in $(b, b')$.
- **Jerk limits.** The acceleration must change at a bounded rate. The profiles are smoother, and the problem is no longer convex.
- **Physics-based feed.** The speed limit comes from a model of the cutting force or of the chip thickness, computed from the engagement of the tool in a model of the stock. The limit depends on the model, so the schedule is only as good as the model.
- **Five-axis paths.** The tool tip and the tool axis move together. The rotary axes add their own speed and acceleration limits, and near a pole a small change of the axis needs a large rotary move.

## Examples

**A straight line.** A move of length $L = 100$ mm with the feed limit $V = 50$ mm/s and the acceleration limit $A = 500$ mm/s². The best schedule accelerates at $A$ over $V^2/(2A) = 2.5$ mm, cruises, and brakes over 2.5 mm. This is the [trapezoidal velocity profile](/trapezoidal-velocity-profile/), and its time is
$$
T = \frac{L}{V} + \frac{V}{A} = 2 + 0.1 = 2.1 \text{ s}.
$$
With a jerk limit $J = 10000$ mm/s³ as well, the acceleration ramps up and down in $A/J = 0.05$ s, which gives the [double S profile](/double-s-velocity-profile/), and the time is $L/V + V/A + A/J = 2.15$ s. The formula holds because the move is long enough to reach both $A$ and $V$, which needs $V \ge A^2/J = 25$.

**A tight bend.** The same move, now with a bend of radius 1 mm between $s = 50$ and $s = 52$, and the centripetal limit $A_n = 500$ mm/s². On the bend the speed must be at most $\sqrt{A_n \rho} = 22.36$ mm/s. The best schedule brakes from 50 to 22.36 over the 2 mm before the bend, crosses it, and accelerates back over 2 mm. The total time is $2.18$ s, both by the formula and by a forward and backward scan on a grid of 200000 steps. A constant feed of 22.36 mm/s, safe everywhere, takes $4.52$ s. A planner without look-ahead, which slows down only when it reaches the bend, would need to brake from 50 to 22.36 at once, which the drives cannot do.

## Known algorithms

**The forward and backward scan.** For speed and tangential acceleration limits only, start from $b(s) = V(s)^2$ with $b(0) = b(L) = 0$. Scan forward and cap $b$ by what can be reached by accelerating from the left, $b(s) \le b(s - h) + 2Ah$. Then scan backward and cap $b$ by what still allows braking to the right. On $n$ grid points this takes $O(n)$ time. It is the look-ahead of CNC controllers. On a path of lines and arcs, each block gets its largest entry and exit speed by the same two scans over the blocks.

**Theorem.** Under the model $0 \le b \le V(s)^2$, $|b'| \le 2A$, $b(0) = b(L) = 0$, the scans give the profile
$$
b^*(s) = \min_{\sigma \in [0, L]} \big( \bar V(\sigma)^2 + 2A|s - \sigma| \big),
$$
where $\bar V$ is $V$ with the value 0 at both ends. Every feasible profile satisfies $b \le b^*$, and $b^*$ is feasible, so it is the fastest at every point and has the least time.

*Proof.* A feasible $b$ has $|b(s) - b(\sigma)| \le 2A|s - \sigma|$ and $b(\sigma) \le \bar V(\sigma)^2$, so $b(s) \le \bar V(\sigma)^2 + 2A|s - \sigma|$ for every $\sigma$, that is $b \le b^*$. The function $b^*$ is a minimum of functions with slope $\pm 2A$, so $|{b^*}'| \le 2A$ wherever it is differentiable, and it is Lipschitz with the constant $2A$. Taking $\sigma = s$ gives $b^* \le \bar V(s)^2$. So $b^*$ is feasible. Since $T = \int ds/\sqrt{b}$ falls as $b$ grows, $b^*$ has the least time. On a grid, the forward scan computes the minimum over $\sigma \le s$ and the backward scan the minimum over $\sigma \ge s$. $\square$

The proof rests on one property of the model: the maximum of two feasible profiles is feasible. A pointwise speed limit of any kind keeps the proof valid. The same property holds for any limit on $b$ and $b'$ at each point, because the maximum of two profiles equals one of them on each side of a crossing, and it is the reason why the phase plane methods below only use the largest acceleration and deceleration. Jerk limits break it: where two profiles cross, their maximum has a kink, so $b''$ is infinite there.

**Phase plane methods.** [Bobrow, Dubowsky and Gibson](/bobrow-time-optimal-algorithm/), and Shin and McKay, worked in the plane of path position and path speed. The speed limits form the [maximum velocity curve](/maximum-velocity-curve/), and the time-optimal profile switches between the largest acceleration and the largest deceleration allowed at each point. This handles axis and torque limits as well, with care at the points where the curve is touched.

**Convex optimization.** Verscheure and coauthors noted that in terms of $b$ the objective $\int b^{-1/2} ds$ is convex, because $t \mapsto t^{-1/2}$ is convex for $t > 0$, and that all the limits above except jerk are linear. So the problem is convex, every local optimum is global, and after discretization it is a [second-order cone program](/second-order-cone-programming/). See [convex time-optimal path parameterization](/convex-time-optimal-path-parameterization/).

**Jerk-limited profiles.** The [double S profile](/double-s-velocity-profile/) is the jerk-limited move between two speeds. Erkorkmaz and Altintas schedule jerk-limited feeds along spline toolpaths. Since the jerk constraint is not convex, general methods linearize it around a reference profile and solve a sequence of linear or convex programs, or they smooth a profile from the scan. A [minimum-jerk trajectory](/minimum-jerk-trajectory/) minimizes the integral of the squared jerk instead of the time.

**Physics-based scheduling.** The planner simulates the cut on a [z-map](/z-map-model/) or other stock model, predicts the force or chip thickness at each point, and lowers the feed where the load would exceed a limit and raises it where the tool cuts little or nothing. The result is then a speed limit $V(s)$ for the scan.

## Bounds

- The time is at least $L/\max_s V(s)$, and at least $2\sqrt{L/A}$ for a move from rest to rest with the acceleration limit $A$. The trapezoidal time $L/V + V/A$ is exact when $L \ge V^2/A$.
- Under the speed and acceleration model, the scan is optimal at every point, as the theorem says, and it takes $O(n)$ time on $n$ grid points or blocks.
- **The jerk constraint is not convex.** At one point, the allowed set in the plane of $b$ and $b''$ is $\sqrt{b}\,|b''| \le 2J$, the region under the convex curve $2J/\sqrt{b}$. The points $(1, 2J)$ and $(4, J)$ are in it, but their midpoint $(2.5, 1.5J)$ is not, since $1.5 > 2/\sqrt{2.5} = 1.265$. So the convex methods do not apply directly, and the methods for jerk limits give good profiles without a proof of global optimality.
- **What is measured.** The time savings reported for physics-based scheduling, and for jerk-limited planners against simpler ones, are measured on test parts with given machines and force models. They are not bounds. They depend on how well the force model matches the cut, and on how closely the controller follows the schedule.

## Reductions

- **To time-optimal path parameterization.** Treat the machine as a robot whose joints are its axes and whose end effector is the tool. The feed schedule is then a time scaling of the path, and the axis limits are the joint limits.
- **To a convex program.** With $b = v^2$ and no jerk limit, discretize the path and the problem becomes a second-order cone program, which is solved in polynomial time.
- **To a linear program.** If the objective is replaced by the sum of the speeds, or by $\sum_i b_i$ as a proxy, the problem with linear limits becomes a [linear program](/linear-programming-problem/). This is common in jerk-limited planners after linearization.

## Applications

- **CNC look-ahead.** Every modern controller scans ahead over a window of blocks and plans the speed at each block junction, so that the machine can brake in time.
- **Interpolation.** A [parametric interpolator](/parametric-cnc-interpolator/) turns the scheduled feed into steps of the curve parameter in each period.
- **Roughing.** Feed schedules from the cutting load complement path methods such as [constant engagement](/constant-engagement-toolpath/) and [trochoidal milling](/trochoidal-milling/): one changes the path, the other changes the speed.
- **Robots and 3D printers.** The same scans plan the speed of robot paths and of printer heads, where the corner speed is set by a junction deviation rule.

## References
