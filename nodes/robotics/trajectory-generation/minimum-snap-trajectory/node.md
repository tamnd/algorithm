---
tag: GASDKD
kind: algorithm
slug: minimum-snap-trajectory
name: Minimum-snap trajectory
aliases:
- Mellinger-Kumar minimum snap
area: robotics/trajectory-generation
level: advanced
summary: "Piecewise polynomials through waypoints that minimize the integral of squared fourth derivative, found by a quadratic program."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {m: "the number of segments", d: "the number of coordinates"}
  time: {worst: Θ(d m³)}
  space: {extra: Θ(m²)}
properties: {deterministic: true, randomized: false, online: false, exact: true}
history:
  year: 2011
  people: [Daniel Mellinger, Vijay Kumar]
  note: "Mellinger and Kumar used the differential flatness of the quadrotor to plan its motion as piecewise polynomials of the flat outputs that minimize the integrated squared snap, found by a quadratic program, and flew the results on real vehicles."
prereqs: [minimum-jerk-trajectory, quadratic-programming]
see_also: [differential-flatness, quadrotor-differential-flatness, minimum-jerk-trajectory, kkt-conditions, b-spline, trajectory-optimization, rapidly-exploring-random-tree, quadrotor-dynamics]
sources:
  - paper: doi:10.1109/ICRA.2011.5980409
    title: "Daniel Mellinger and Vijay Kumar, Minimum snap trajectory generation and control for quadrotors, IEEE International Conference on Robotics and Automation, 2011, 2520-2525"
    locator: "the whole paper (the snap cost, the quadratic program over the polynomial coefficients, corridor constraints and the choice of segment times)"
  - paper: doi:10.1007/978-3-319-28872-7_37
    title: "Charles Richter, Adam Bry and Nicholas Roy, Polynomial trajectory planning for aggressive quadrotor flight in dense indoor environments, Robotics Research (ISRR 2013), Springer Tracts in Advanced Robotics, 2016, 649-666"
    locator: "the whole paper (the unconstrained form in the free derivatives at the waypoints, and waypoints from a sampling-based planner)"
---

A minimum-snap trajectory passes through a list of waypoints at given times and makes the integral of the squared fourth derivative of the position, the snap, as small as possible. Each segment between two waypoints is a polynomial of degree 7 in each coordinate. The waypoints fix the positions, the start and the end are at rest, and the first three derivatives are continuous at the inner waypoints. Everything else is chosen by the optimization. The cost is quadratic and the constraints are linear, so the coefficients come from a [quadratic program](/quadratic-programming/), and with only equality constraints they come from one linear system. Mellinger and Kumar (2011) introduced the method for quadrotors. A quadrotor is [differentially flat](/differential-flatness/): its motor inputs are functions of the position, the yaw and their derivatives, and the moments that the motors must produce depend on the fourth derivative of the position. So a trajectory with small snap is one the vehicle can fly smoothly. The method is the four-derivative relative of the [minimum-jerk trajectory](/minimum-jerk-trajectory/).

## In plain words

A drone must fly through a list of points, at given times, without stopping at each one. Its motors cannot change their speed instantly, so the flight path must be very smooth. Connect the points by curves, one curve per gap. Each curve is a polynomial with eight numbers per direction. Choose all those numbers at once so that the curves meet at the points without corners or kinks, and so that a measure of roughness, the snap, added up over the whole flight, is as small as possible. That choice is a standard optimization problem with a quadratic cost and straight-line rules, and a linear solver finds the exact answer.

## The problem

Input: waypoints $w_0, \dots, w_m$ of one coordinate and segment durations $T_1, \dots, T_m > 0$. Output: polynomials $p_1, \dots, p_m$ of degree at most 7, with $p_i$ defined on $[0, T_i]$ in local time, that minimize

$$f = \sum_{i=1}^m \int_0^{T_i} \big(p_i^{(4)}(t)\big)^2\, dt$$

subject to $p_i(0) = w_{i-1}$ and $p_i(T_i) = w_i$; zero first, second and third derivatives at the start of $p_1$ and the end of $p_m$; and $p_i^{(k)}(T_i) = p_{i+1}^{(k)}(0)$ for $k = 1, 2, 3$ at each inner waypoint. Several coordinates are independent problems with the same durations. Mellinger and Kumar also add inequality constraints, such as corridors around the straight segments; then the problem is a general quadratic program.

## The algorithm

Write $c_i \in \mathbb R^8$ for the coefficients of $p_i$ and $c = (c_1, \dots, c_m)$. Then $f = c^{\mathsf T} Q c$ with $Q$ block diagonal, and the constraints are $Ac = b$ with $5m + 3$ rows.

```pseudo id=main
MIN-SNAP(w0..wm, T1..Tm)
L1  for each segment i = 1..m
L2      put Qi into the diagonal block i of Q, with Qi[r][s] = r(r-1)(r-2)(r-3) s(s-1)(s-2)(s-3) Ti^(r+s-7) / (r+s-7) for r, s ≥ 4, else 0
L3  for each segment i: add the rows pi(0) = w(i-1) and pi(Ti) = wi
L4  for k = 1, 2, 3: add the rows p1^(k)(0) = 0 and pm^(k)(Tm) = 0
L5  for each inner waypoint i and k = 1, 2, 3: add the row pi^(k)(Ti) - p(i+1)^(k)(0) = 0
L6  solve [2Q Aᵀ; A 0] (c, λ) = (0, b)                ▷ the KKT system
L7  return c split into the m segments
```

Lines L1 and L2 build the cost: the integral of the product of the fourth derivatives of $t^r$ and $t^s$. Lines L3 to L5 build the constraints. Line L6 solves the [KKT conditions](/kkt-conditions/) of the equality-constrained problem, with one [Lagrange multiplier](/lagrange-multiplier/) per constraint, by [Gaussian elimination](/gaussian-elimination/). The code also has a second method, after Richter, Bry and Roy: write each segment through the values $(p, p', p'', p''')$ at its two ends, fix the known ones, and minimize over the free derivatives at the inner waypoints, an unconstrained quadratic. Both give the same exact answer.

## Example

**One segment.** From $0$ to $1$ in time $1$, the constraints fix all eight coefficients, and

$$p(t) = 35t^4 - 84t^5 + 70t^6 - 20t^7,$$

with cost $100800$ and peak velocity $p'(1/2) = 35/16 = 2.1875$. For a distance $D$ and a time $T$ the cost is $100800\, D^2/T^7$.

**Out and back.** Waypoints $0, 1, 0$ with $T_1 = T_2 = 1$ s. The solution is

$$p_1(t) = 14t^4 - \tfrac{126}{5}t^5 + \tfrac{77}{5}t^6 - \tfrac{16}{5}t^7, \qquad p_2(t) = 1 - \tfrac{21}{5}t^2 + 7t^4 - 7t^6 + \tfrac{16}{5}t^7.$$

At the inner waypoint the velocity is $0$ and the jerk is $0$, by symmetry, the acceleration is $-42/5$, and the snap is $168$ from both sides. The cost is $32256$. Stopping at the waypoint with two one-segment moves would cost $2 \cdot 100800 = 201600$, more than six times as much. These numbers are exact, computed by the code with fractions.

**Durations matter.** With $T_1 = 1$ and $T_2 = 2$ instead, the velocity at the inner waypoint is $7/4$, not $0$, and the cost drops to about $4306$. The durations are inputs, and the result depends on them strongly.

## Correctness

Theorem: the KKT matrix of line L6 is nonsingular, and its solution is the unique minimizer. The [proof](proofs/correctness.md) has three steps. A polynomial of degree 7 is fixed by its value and first three derivatives at both ends of its interval, a [Hermite interpolation](/hermite-interpolation/) fact; this shows that the constraint matrix has full row rank. If a feasible direction had zero cost, every segment would be a cubic, and the zero data at the start would force all of them to zero, so $Q$ is [positive definite](/positive-definite-matrix/) on the null space of $A$. The standard argument then gives the unique minimum. A further theorem: although only the first three derivatives are forced to be continuous, the optimum also has continuous derivatives of orders 4, 5 and 6 at the inner waypoints, and it is optimal among all piecewise smooth functions with square-integrable fourth derivative, not only among polynomials of degree 7.

## Complexity

The KKT system has $8m + 5m + 3 = 13m + 3$ unknowns. Dense Gaussian elimination, as in the code, costs $\Theta(m^3)$ time and $\Theta(m^2)$ space per coordinate, so $\Theta(dm^3)$ for $d$ coordinates; the matrix is the same for all coordinates, so one factorization can serve all of them. The matrix is banded when the unknowns are ordered by segment, and a banded solver takes $\Theta(m)$ time. With inequality constraints, a quadratic programming solver is needed, and its cost depends on the solver.

## Properties

- **Smooth.** The optimum is $C^6$ at the inner waypoints (a theorem), although only $C^3$ is imposed. The seventh derivative jumps.
- **Linear in the waypoints.** For fixed durations, the coefficients are a linear function of the waypoints, so the same matrix serves every coordinate and every set of waypoints.
- **No limits by default.** The equality-constrained problem ignores velocity, acceleration and obstacle limits between waypoints. The path can bulge out between waypoints.
- **Scaling in time.** Stretching all durations by a factor $k$ divides the cost by $k^7$ and keeps the shape of the path.
- **Durations are inputs.** The cost decreases without bound as the durations grow, so they cannot be chosen by the same cost alone; Mellinger and Kumar fix the total time and redistribute it among segments by gradient descent.

## Variants and improvements

- **Inequality constraints.** Corridor constraints at sample points keep the path near the straight segments (Mellinger and Kumar). This turns the linear system into a quadratic program.
- **Free derivatives.** Richter, Bry and Roy solve for the free derivatives at the waypoints in an unconstrained form, which is better conditioned for many segments, and they take the waypoints from a [rapidly-exploring random tree](/rapidly-exploring-random-tree/) run on a simpler model. They add segments where the polynomial path hits an obstacle.
- **Other orders.** Minimizing the third derivative gives the [minimum-jerk trajectory](/minimum-jerk-trajectory/) through waypoints, with quintic segments. Yaw is often planned with a lower order cost.
- **Other bases.** The same problem can be written with [B-splines](/b-spline/) or Bernstein polynomials, which give convex hull bounds useful for safety constraints.
- **General optimization.** With dynamics, limits and obstacles in one problem, use [trajectory optimization](/trajectory-optimization/).

## When to use it

Use minimum snap for quadrotors and other differentially flat vehicles, where smooth position trajectories become feasible inputs, and as a smoothing step after a geometric planner has found waypoints. Check the velocity, acceleration and thrust limits after solving, and lengthen the durations if they are violated. Use a time-optimal method if the vehicle must fly at its limits.

## Pitfalls

- **Ill-conditioning.** Coefficients in powers of $t$ give badly conditioned matrices for long segments or many segments. Scale time per segment, use the free-derivative form, or use exact arithmetic for small problems as the tests do.
- **Bad durations.** A short segment next to a long one makes the path overshoot. Estimate durations from distances and a nominal speed, then refine.
- **Collisions between waypoints.** Waypoints that are free do not make the polynomials free. Check the result and add waypoints or constraints.
- **Too few constraints at the ends.** If the end derivatives are left free, the problem changes; leaving out the zero-derivative rows at the ends gives a different, natural boundary optimum.
- **Mixing local and global time.** Each segment uses its own local time; the continuity rows of line L5 compare the end of one segment with the start of the next.

## Implementations

## History

Polynomial splines that minimize an integrated squared derivative are an old idea of approximation theory: the natural cubic spline minimizes the integrated squared second derivative among all interpolants. Mellinger and Kumar (2011) chose the fourth derivative for quadrotors because of their differential flatness, set the problem as a quadratic program with corridor constraints, optimized the segment times, and flew aggressive trajectories with real vehicles. Richter, Bry and Roy (ISRR 2013, published 2016) gave the unconstrained formulation in the free derivatives and combined it with a sampling-based planner for flight in cluttered indoor spaces.

## References
