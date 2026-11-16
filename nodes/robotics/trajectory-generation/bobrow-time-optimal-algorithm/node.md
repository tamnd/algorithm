---
tag: BWJG6T
kind: algorithm
slug: bobrow-time-optimal-algorithm
name: Bobrow-Dubowsky-Gibson algorithm
aliases:
- Shin-McKay algorithm
- numerical integration method for TOPP
area: robotics/trajectory-generation
level: advanced
summary: "Finds the fastest timing along a fixed robot path by integrating maximum acceleration and deceleration curves in the phase plane and joining them at switch points."
solves: [time-optimal-path-parameterization]
model: real-ram
complexity:
  vars: {h: "the integration step in s", m: "the number of constraint rows", k: "the number of switch points", b: "the number of bisection steps per switch"}
  time: {worst: O(k b m^2 / h)}
  space: {extra: O(k / h)}
properties: {deterministic: true, randomized: false, online: false, exact: false}
prereqs: [time-optimal-path-parameterization, maximum-velocity-curve, time-scaling]
see_also: [topp-reachability-analysis, convex-time-optimal-path-parameterization, bang-bang-control, pontryagin-maximum-principle, trapezoidal-velocity-profile, runge-kutta-methods, manipulator-equation, feedrate-scheduling]
sources:
  - paper: doi:10.1177/027836498500400301
    title: "James E. Bobrow, Steven Dubowsky and John S. Gibson, Time-optimal control of robotic manipulators along specified paths, The International Journal of Robotics Research 4(3), 1985, 3-17"
    locator: "the whole paper (the phase plane, the velocity limit, and the construction from acceleration and deceleration curves)"
  - paper: doi:10.1109/TAC.1985.1104009
    title: "Kang G. Shin and Neil D. McKay, Minimum-time control of robotic manipulators with geometric path constraints, IEEE Transactions on Automatic Control 30(6), 1985, 531-541"
    locator: "the whole paper (the same construction, found independently)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 9.4 (time-optimal time scaling: the phase plane, the time-scaling algorithm, and its assumptions and caveats)"
  - paper: doi:10.1109/JRA.1987.1087090
    title: "Friedrich Pfeiffer and Rainer Johanni, A concept for manipulator trajectory planning, IEEE Journal of Robotics and Automation 3(2), 1987, 115-123"
    locator: "the whole paper (switch points where the maximum velocity curve is not smooth, and singular points)"
  - paper: doi:10.1109/TRO.2014.2351113
    title: "Quang-Cuong Pham, A general, fast, and robust implementation of the time-optimal path parameterization algorithm, IEEE Transactions on Robotics 30(6), 2014, 1533-1540"
    locator: "the whole paper (singular arcs, velocity limits, and a robust implementation)"
---

The Bobrow-Dubowsky-Gibson algorithm finds the fastest way to move along a fixed path when the forces that drive the motion are limited. A robot arm that must follow a given curve, a machine tool that must cut a given contour, or a vehicle that must stay on a given road all have this problem: the shape of the motion is decided, and only the timing is free. The algorithm describes the timing by one number at each point of the path, the speed along the path, and draws it as a curve in the "phase plane" of position against speed. The limits on the forces give, at each point and speed, a largest and a smallest allowed acceleration, and above a certain speed, the [maximum velocity curve](/maximum-velocity-curve/), no acceleration is allowed at all. The fastest timing always uses the largest or the smallest acceleration, and it changes from one to the other only at a few switch points. The algorithm integrates these extreme curves numerically and searches for the switch points where a braking curve just touches the maximum velocity curve. It was published in 1985 by Bobrow, Dubowsky and Gibson and, independently, by Shin and McKay. It is the classical solution of [time-optimal path parameterization](/time-optimal-path-parameterization/), and it is fast, but finding switch points numerically is fragile.

## In plain words

A driver must follow a winding mountain road as fast as possible. On each part of the road the car can speed up only so hard and brake only so hard, and in tight bends there is a top speed above which the car slides off. The fastest drive never cruises gently: at every moment the driver either floors it or brakes as hard as possible. The only question is where to switch. Start at the finish line and work out the last hard braking run that ends at a stop. Then start at the beginning and floor it. If you hit a bend's top speed first, find the braking run that just touches that top speed without going over, use it to slow down in time, and floor it again after the bend. Repeat until the speeding-up curve meets the last braking run.

## The problem

Input: a path $q(s)$ in joint space, $s \in [0, 1]$, and limits that are linear in $\ddot s$ and $\dot s^2$ at each $s$. For an arm with torque limits $\tau_{\min} \le \tau \le \tau_{\max}$ the [manipulator equation](/manipulator-equation/) gives along the path

$$\tau = M(q) q_s\, \ddot s + \left(M(q) q_{ss} + C(q, q_s) q_s\right) \dot s^2 + g(q),$$

with $q_s = dq/ds$. This page writes $x = \dot s^2$ and $u = \ddot s$, so that each limit is a row $\ell \le a u + b x + c \le h$, and $dx/ds = 2u$. At each $(s, x)$ the rows give an interval $[L(s, x), U(s, x)]$ of admissible $u$. The maximum velocity curve $\mathrm{MVC}(s)$ is the largest $x$ where $L \le U$. Output: a profile $x(s)$ from $(0, 0)$ to $(1, 0)$ that stays at or below the MVC, has $2L \le dx/ds \le 2U$, and has the least traversal time $T = \int_0^1 ds/\sqrt{x}$. Lynch and Park draw the same plane with the speed $\dot s$ on the vertical axis; using $x$ makes the curves easier to integrate, because $dx/ds$ does not blow up at $\dot s = 0$.

## The algorithm

```pseudo id=main
TOPP-INTEGRATE(path, limits)
L1  F ← integrate dx/ds = 2L backward from (1, 0) until it leaves the region below the MVC
L2  (s_i, x_i) ← (0, 0);  switches ← empty list
L3  repeat
L4      A ← integrate dx/ds = 2U forward from (s_i, x_i) until it crosses F or the MVC
L5      if A crosses F then add the crossing (U to L) to switches; return A then F, and switches
L6      (s_lim, x_lim) ← the point where A crosses the MVC
L7      binary search x in [0, x_lim] for the largest x whose forward L curve from (s_lim, x) stays below the MVC
L8      (s_tan, x_tan) ← the point where that L curve touches the MVC
L9      D ← integrate dx/ds = 2L backward from (s_tan, x_tan) until it crosses A
L10     add the crossing of D and A (U to L) and (s_tan, x_tan) (L to U) to switches
L11     (s_i, x_i) ← (s_tan, x_tan)
```

Line L1 builds the final braking curve: any admissible profile must be on or below it, because from a point above it even the hardest braking overshoots the end. Line L4 accelerates as hard as possible. If the acceleration curve meets the braking curve $F$, the switch from $U$ to $L$ at their crossing finishes the profile (line L5). Otherwise the curve hits the MVC at $s_{\text{lim}}$ (line L6), and somewhere past $s_{\text{lim}}$ the profile must have braked. Lines L7 and L8 find where: a braking curve that starts high at $s_{\text{lim}}$ crosses the MVC, one that starts at zero falls to zero, and the boundary between the two touches the MVC at a tangent point. Line L9 integrates the braking curve backward from the tangent point until it meets the acceleration curve, which gives a switch from $U$ to $L$. At the tangent point the profile switches back to $U$, and the loop repeats from there (line L11). The code uses RK4 with a fixed step $h$ in $s$, so each curve costs $O(1/h)$ evaluations of the limits.

## Example

**One axis.** For $q(s) = s$ with $|\ddot q| \le 2$, the limits are $-2 \le u \le 2$ and the MVC is infinite. Line L1 gives $F$: $x = 4(1 - s)$. Line L4 gives $A$: $x = 4s$. They cross at $s = 1/2$, $x = 2$, which is the triangle profile with $T = \sqrt 2 \approx 1.41421$, the minimum time of the [trapezoidal velocity profile](/trapezoidal-velocity-profile/) without a velocity limit. With different limits, $-3 \le u \le 1$, the curves cross at $s = 3/4$, where the time to accelerate over $3/4$ at rate 1 and to brake over $1/4$ at rate 3 balance.

**A 2R arm.** The planar arm with unit links, unit point masses at the link ends and no gravity has $M = [[3 + 2\cos q_2, 1 + \cos q_2], [1 + \cos q_2, 1]]$. It follows the straight joint path from $(0, 0)$ to $(2, -3)$ with $|\tau_1| \le 10$ and $|\tau_2| \le 4$. The MVC is infinite at $s = 0$, where $\sin q_2 = 0$, and has a sharp minimum of $1.1556$ at $s = 0.35$, where the active torque limit changes. With $h = 0.001$:

| piece | $s$ range | control | $x$ at the end |
|---|---|---|---|
| accelerate | 0 to 0.2386 | $U$ | 1.325 |
| brake | 0.2386 to 0.349 | $L$ | 1.151 (tangent point, near the MVC minimum) |
| accelerate | 0.349 to 0.7311 | $U$ (negative up to $s \approx 0.6$) | 1.059 |
| brake | 0.7311 to 1 | $L$ ($F$) | 0 |

The traversal time is $1.51065$ ($1.51044$ with $h = 0.01$ and $1.51074$ with $h = 0.004$). The [reachability method](/topp-reachability-analysis/) on a grid of 2000 intervals gives $1.51056$ for the same problem.

## Correctness

Theorem (Bobrow, Dubowsky and Gibson 1985; Shin and McKay 1985; Lynch and Park, Section 9.4): if the limits are continuous along the path and Lipschitz in the speed, and the algorithm finds each tangent point exactly, the profile is admissible and is at least as high as every admissible profile at every $s$, so it is time-optimal. The proof uses a comparison lemma for differential inequalities. Any admissible profile that starts at or below an acceleration curve stays below it going forward, and one that ends at or below a braking curve stays below it going backward. Every acceleration piece of the result starts at $(0, 0)$ or on the MVC, and every braking piece ends at $(1, 0)$ or on the MVC, where no admissible profile can be higher. See the [proof](proofs/correctness.md).

The conditions matter. The theorem is about the exact curves; the computed curves carry the error of the integrator, and the tangent point is found only to within one step $h$ (this is visible in the table, where the tangent point is at 0.349 or 0.348 rather than 0.35 for some $h$).

## Complexity

Each curve takes at most $1/h$ RK4 steps. Each step evaluates the limits four times, at $O(m)$ for $m$ rows, and checks the MVC at $O(m^2)$, because the MVC is the smallest crossing of a lower and an upper bound on $u$. Each switch costs a binary search of $b$ bisection steps, each one a full curve. The total is $O(k\, b\, m^2 / h)$ for $k$ switches, with $b = O(\log(x_{\text{lim}} / \varepsilon))$ for a tolerance $\varepsilon$. Memory is $O(k/h)$ for the profile. The number of switches $k$ depends on the path and is not bounded in advance. Pham and Pham (2018) report $O(m^2 N)$ for this method on a grid of $N$ points, with the MVC computed once per point.

## Properties

- **Time-optimal under its hypotheses.** A theorem for exact integration and isolated tangent points; see Correctness.
- **Bang-bang.** The control is always $L$ or $U$, which uses full torque on at least one joint at every point.
- **Profile, not grid.** The result is a set of curves with explicit switch points, and the limits are checked along the curves, not only at grid points.
- **Fragile at singularities.** Where the MVC is flat (velocity limits) or where the optimal profile must follow the MVC (singular arcs), the tangent search fails. This is a known weakness, studied by Pfeiffer and Johanni (1987) and by Pham (2014).

## Variants and improvements

- **Finding switch points directly.** Instead of a binary search from $s_{\text{lim}}$, compute the candidate switch points on the MVC first: points where the MVC is not smooth, points where its slope equals the slope of the extreme curve, and zero-inertia points. Then integrate from them. Pfeiffer and Johanni (1987) and Pham (2014) work in this way.
- **Velocity limits.** A joint velocity limit puts a flat part on the MVC. The optimal profile then follows the MVC with a control strictly between $L$ and $U$. Implementations treat these parts as their own arcs (Pham 2014).
- **Acceleration limits instead of torque limits.** For a kinematic robot with joint acceleration limits, the rows are $|q_{s,j} u + q_{ss,j} x| \le a_j$, and the same algorithm applies without a dynamic model.
- **Grid methods.** The [reachability method](/topp-reachability-analysis/) replaces the integration by small linear programs and avoids the switch-point search; the [convex formulation](/convex-time-optimal-path-parameterization/) solves one convex program.

## When to use it

Use the integration method for paths with torque or acceleration limits and a smooth or piecewise smooth MVC, when you want a profile with explicit switch points and limits that hold along the whole path, not only at grid points. For paths with velocity limits, many contact constraints or near-singular dynamics, use a grid method such as TOPP-RA, which handles these cases without special code.

## Pitfalls

- **Flat MVC.** With a velocity limit, line L7 cannot find a touching curve: every braking curve from just below the MVC crosses it or falls away along a flat ceiling, and the binary search shrinks to a point. The code in this page does not handle velocity limits for this reason.
- **Tangent point off by one step.** Line L8 picks a grid point of the integrated curve. If the true tangent point lies between grid points, the switch is off by up to $h$, and the profile may cross the MVC slightly. A smaller $h$ near the switch, or an explicit switch-point search, fixes this.
- **Integrating through corners.** The right side $2U(s, x)$ has corners where the active limit changes. RK4 loses its order there, so the error is $O(h)$ near corners, not $O(h^4)$.
- **Starting at zero speed.** At $(0, 0)$ the path may need a positive $U$ to start at all. If $U(0, 0) \le 0$, the robot cannot leave the start, and the algorithm must stop (the code returns nothing).
- **Line L9 never meets A.** If the braking curve from the tangent point falls to zero speed before it meets the acceleration curve, the path cannot be traversed with these limits. The code returns nothing; a general implementation must report this case.

## Implementations

## History

The problem arose in the early 1980s, when robot controllers began to follow planned paths. Bobrow, Dubowsky and Gibson (IJRR, 1985) and Shin and McKay (IEEE Transactions on Automatic Control, 1985) found the same solution at the same time: the optimal profile is bang-bang in the path acceleration, and its switch points lie on the velocity limit curve. Shin and McKay published a follow-up in 1986 (IEEE Transactions on Automatic Control 31, 491-500). Pfeiffer and Johanni (1987) studied the switch points and the singular cases. Many implementations followed, and many failed at singular points; Pham (2014) analyzed these failures and gave a robust implementation. Lynch and Park present the algorithm in their textbook in the form used on this page.

## References
