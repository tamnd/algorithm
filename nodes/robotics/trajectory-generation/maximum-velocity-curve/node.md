---
tag: 8W39EQ
kind: definition
slug: maximum-velocity-curve
name: Maximum velocity curve
aliases:
- MVC
- velocity limit curve
area: robotics/trajectory-generation
level: advanced
summary: "The largest path speed at each path point for which some admissible acceleration exists, the ceiling of the phase plane."
prereqs: [time-scaling, manipulator-equation]
see_also: [time-optimal-path-parameterization, bobrow-time-optimal-algorithm, topp-reachability-analysis, convex-time-optimal-path-parameterization, fourier-motzkin-elimination, seidel-linear-programming, singular-arc]
sources:
  - paper: doi:10.1177/027836498500400301
    title: "James E. Bobrow, Steven Dubowsky and John S. Gibson, Time-optimal control of robotic manipulators along specified paths, The International Journal of Robotics Research 4(3), 1985, 3-17"
    locator: "the whole paper (the velocity limit in the phase plane)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 9.4 (the phase plane and the limits on the path acceleration)"
  - paper: doi:10.1109/JRA.1987.1087090
    title: "Friedrich Pfeiffer and Rainer Johanni, A concept for manipulator trajectory planning, IEEE Journal of Robotics and Automation 3(2), 1987, 115-123"
    locator: "the whole paper (switch points on the curve and singular points)"
  - paper: doi:10.1109/TRO.2014.2351113
    title: "Quang-Cuong Pham, A general, fast, and robust implementation of the time-optimal path parameterization algorithm, IEEE Transactions on Robotics 30(6), 2014, 1533-1540"
    locator: "the whole paper (the curve from torque limits and from velocity limits, and its singular points)"
---

The maximum velocity curve tells how fast a machine may move at each point of a fixed path and still obey its force limits. When a robot follows a given path, its state is the position $s$ on the path and the speed $\dot s$. The motor limits allow, at each pair $(s, \dot s)$, only some values of the path acceleration $\ddot s$. At low speed there is a range of admissible accelerations; as the speed grows, the forces needed just to stay on the path at that speed grow too, and the range shrinks. The maximum velocity curve, or MVC, is the speed at which the range shrinks to nothing. Above it, no choice of acceleration keeps all motors within their limits, so every admissible motion along the path stays below the curve. The curve is the ceiling of the phase plane of $(s, \dot s)$ in [time-optimal path parameterization](/time-optimal-path-parameterization/), and the place where the optimal profile switches from braking to acceleration. Some sources call it the velocity limit curve.

## Definition

Let $q(s)$, $s \in [0, 1]$, be a path for a robot, and write $x = \dot s^2$ and $u = \ddot s$. Along the path, each limit of the robot is a row

$$\ell_j \le a_j(s)\, u + b_j(s)\, x + c_j(s) \le h_j, \qquad j = 1, \dots, m.$$

Torque limits have this form by the [manipulator equation](/manipulator-equation/); joint velocity and acceleration limits too (see the problem page). For fixed $(s, x)$, each row with $a_j \ne 0$ gives a lower and an upper bound on $u$, and a row with $a_j = 0$ gives a condition on $x$ alone. Let $L(s, x)$ be the largest lower bound and $U(s, x)$ the smallest upper bound. The pair $(s, x)$ is **admissible** if $x \ge 0$, $L(s, x) \le U(s, x)$, and every row with $a_j = 0$ holds.

The **maximum velocity curve** is

$$\mathrm{MVC}(s) = \sup\{x \ge 0 : (s, x) \text{ is admissible}\},$$

with the value $+\infty$ if the set is not bounded. This is the squared form, which the pages of this group use; the curve in the plane of $(s, \dot s)$ is $\sqrt{\mathrm{MVC}(s)}$.

**Why it is a ceiling.** $L$ is a maximum of functions that are affine in $x$, so it is convex in $x$; $U$ is a minimum of affine functions, so it is concave; so $U - L$ is concave, and the set of $x$ with $L \le U$ is an interval. If $x = 0$ is admissible at $s$, which holds whenever the robot can stand still there, the admissible $x$ form the interval $[0, \mathrm{MVC}(s)]$. So every admissible profile $x(s)$ lies on or below the curve.

**How to compute it.** $\mathrm{MVC}(s)$ is the value of the linear program "maximize $x$ over $(u, x)$ subject to the rows at $s$", a linear program in two variables. Eliminating $u$ by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) gives it directly: each pair of a lower bound from row $i$ and an upper bound from row $j$ gives one linear inequality in $x$, so $O(m^2)$ work per point. A two-variable LP solver such as [Seidel's algorithm](/seidel-linear-programming/) takes $O(m)$ expected time per point.

**Two parts of the curve.** A velocity limit $|q_{s,j}\dot s| \le v_j$ bounds $x$ alone, at $v_j^2/q_{s,j}^2$, whatever $u$ is. Torque and acceleration limits bound $x$ only through the condition $L \le U$. Pham (2014) treats the two parts separately, because the optimal profile can run along a velocity-limit part for a whole stretch.

## Examples and non-examples

- **One axis, acceleration limit only.** For $q(s) = s$ with $|\ddot q| \le A$, the rows are $-A \le u \le A$, which do not involve $x$, so $\mathrm{MVC}(s) = +\infty$ everywhere. The profile is limited only by the need to start and stop.
- **One axis with a velocity limit.** Adding $|\dot q| \le V$ gives the row $x \le V^2$, so $\mathrm{MVC}(s) = V^2$, a flat ceiling. The optimal profile runs along it in the middle of a long move, which is the cruise phase of the [trapezoidal velocity profile](/trapezoidal-velocity-profile/).
- **A 2R arm.** A planar arm with unit links, unit point masses at the link ends and no gravity follows the straight joint path from $(0, 0)$ to $(2, -3)$ with $|\tau_1| \le 10$ and $|\tau_2| \le 4$. The curve is infinite at $s = 0$, where the arm is stretched out and the speed terms of the torques vanish. It falls to a sharp minimum of $1.156$ at $s = 0.35$, where the active pair of torque limits changes, then rises to $15.79$ at $s = 1$. Values at other points are in the table on the [problem page](/time-optimal-path-parameterization/). The minimum is a kink, so the curve is continuous but not smooth there.
- **Non-example: the optimal profile.** The optimal profile touches the MVC only at a few points or along short stretches. In general the profile cannot follow the curve, because the slope $d\,\mathrm{MVC}/ds$ can require a $u$ outside $[L, U]$. On the 2R arm, the optimal profile touches the curve once, near $s = 0.349$.
- **Non-example: a jerk limit.** A limit on $\dddot q$ involves $du/ds$, so it is not a row in $(u, x)$ at one point, and the definition above does not apply to it.

## Related definitions

- **Phase plane.** The plane of $(s, \dot s)$, or of $(s, x)$, in which time-optimal profiles are drawn. Lynch and Park (Section 9.4) work in the plane of $(s, \dot s)$.
- **Admissible set.** At each $s$, the polygon $\Omega(s)$ of pairs $(u, x)$ that meet every row. The MVC is the highest point of its projection on the $x$ axis. The [reachability method](/topp-reachability-analysis/) works with these polygons directly.
- **Switch points.** Points on the MVC where the optimal profile changes from braking to acceleration. They are tangent points, where the curve of full acceleration is tangent to the MVC; discontinuity points, where the MVC jumps; and singular points. Pfeiffer and Johanni (1987) studied how to find them, and the [Bobrow algorithm](/bobrow-time-optimal-algorithm/) searches for them.
- **Zero-inertia and singular points.** Points where the coefficient $a_j(s)$ of an active row is zero. There $L$ or $U$ jumps, the MVC can have a corner, and the optimal profile can run along the curve on a [singular arc](/singular-arc/).
- **Controllable and reachable sets.** The set of $x$ at $s$ from which the end can still be reached, and the set of $x$ that can be reached from the start. Both lie below the MVC and are usually much lower; on the 2R arm the bound $\int ds/\sqrt{\mathrm{MVC}}$ is about $0.623$, while the minimum time is about $1.511$.

## References
