---
tag: EWJYN8
kind: algorithm
slug: stewart-trinkle-time-stepping
name: Stewart-Trinkle time stepping
aliases:
- Anitescu-Potra time stepping
- velocity-impulse time stepping
area: robotics/robot-dynamics
level: research
summary: A time-stepping method for rigid bodies with contact and Coulomb friction that solves one linear complementarity problem in impulses and velocities per step.
model: real-ram
complexity:
  vars: {n: "the number of generalized velocities", m: "the number of LCP unknowns, c (k + 2) for c active contacts with k friction edges each"}
  time: {worst: "O(n^3 + n^2 m + n m^2 + m^3 2^m)", per_pivot: Θ(m^2)}
  space: {extra: Θ(n^2 + m^2)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 1996
  people: [David E. Stewart, Jeffrey C. Trinkle]
  note: Stewart and Trinkle wrote the equations of motion with contact and Coulomb friction in impulses over a time step, so that each step is a complementarity problem that has a solution in cases where the acceleration form has none.
prereqs: [manipulator-equation, polyhedral-friction-cone, rigid-contact-complementarity]
see_also: [painleve-paradox, contact-implicit-trajectory-optimization, symplectic-euler-method, kkt-conditions, linear-programming-problem, quadratic-programming, gauss-principle-of-least-constraint, friction-cone]
sources:
  - paper: doi:10.1002/(SICI)1097-0207(19960815)39:15<2673::AID-NME972>3.0.CO;2-I
    title: "David E. Stewart and Jeffrey C. Trinkle, An implicit time-stepping scheme for rigid body dynamics with inelastic collisions and Coulomb friction, International Journal for Numerical Methods in Engineering 39(15), 1996"
    locator: pages 2673 to 2691
  - paper: doi:10.1023/A:1008292328909
    title: "Mihai Anitescu and Florian A. Potra, Formulating dynamic multi-rigid-body contact problems with friction as solvable linear complementarity problems, Nonlinear Dynamics 14(3), 1997"
    locator: pages 231 to 247
  - paper: doi:10.1137/S0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 2000"
    locator: pages 3 to 39
  - paper: doi:10.1109/ROBOT.2000.844054
    title: "David E. Stewart and Jeffrey C. Trinkle, An implicit time-stepping scheme for rigid body dynamics with Coulomb friction, IEEE International Conference on Robotics and Automation, 2000"
    locator: pages 162 to 169
  - paper: doi:10.1287/mnsc.11.7.681
    title: Carlton E. Lemke, Bimatrix equilibrium points and mathematical programming, Management Science 11(7), 1965
    locator: pages 681 to 689
  - book: isbn:9780898716863
    title: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, SIAM Classics in Applied Mathematics 60, 2009"
    locator: Chapter 4 (pivoting methods, Lemke's method and the lexicographic rule)
  - paper: doi:10.1007/s002050050129
    title: "David E. Stewart, Convergence of a time-stepping scheme for rigid-body dynamics and resolution of Painlevé's problem, Archive for Rational Mechanics and Analysis 145(3), 1998"
    locator: pages 215 to 260
  - paper: doi:10.1109/ISATP.2005.1511469
    title: "Jeffrey C. Trinkle, Stephen Berard and Jong-Shi Pang, A time-stepping scheme for quasistatic multibody systems, IEEE International Symposium on Assembly and Task Planning, 2005"
    locator: "pages 174 to 181; Section 1.1 on the solvability of the Stewart-Trinkle and Anitescu-Potra LCPs"
  - paper: doi:10.1007/BFb0120782
    title: "Katta G. Murty, Computational complexity of complementary pivot methods, Mathematical Programming Study 7, 1978"
    locator: pages 61 to 73
  - paper: doi:10.1007/s10107-005-0590-7
    title: Mihai Anitescu, Optimization-based simulation of nonsmooth rigid multibody dynamics, Mathematical Programming 105(1), 2006
    locator: pages 113 to 143
---

Stewart-Trinkle time stepping simulates rigid bodies that touch each other or the ground with Coulomb friction. It does not compute contact forces and accelerations. Over each time step $h$ it computes contact impulses and the new velocity together, as the solution of one linear complementarity problem (LCP), and then it moves the bodies with the new velocity. Because impulses can be as large as needed, a step has a solution even in the cases of the [Painlevé paradox](/painleve-paradox/), where the force and acceleration form of the [rigid contact model](/rigid-contact-complementarity/) has none.

## In plain words

Think of a film of a box that slides on a floor, taken at a fixed number of frames per second. Between two frames, the program does not ask how hard the floor pushes at each instant. It asks a simpler question: how much total push did the floor give during this short time? The answer must obey three rules. The floor can only push, never pull. The floor pushes only where the box touches it, and only enough to stop the box from going into it. The sideways push from friction can be at most a fixed part of the upward push, and it acts against the sliding. The program finds the pushes that obey all three rules at once, updates the speed of the box, and moves it to the next frame. A short hard push is always allowed, so the program never gets stuck.

## The problem

The system has the generalized coordinates $q$, the generalized velocities $v$, the mass matrix $M(q)$ and the [manipulator equation](/manipulator-equation/) $M \dot v + C v + g = \tau + J^T F_{\mathrm{ext}}$. All forces except the contact forces, that is the actuator forces, gravity and the velocity product terms, are collected in $f = \tau - C v - g$. Contact $i$ has a gap function $\phi_i(q)$, the distance between the two bodies along the contact normal, with $\phi_i \ge 0$ when they do not overlap. The normal points into the body that receives the contact force.

The friction cone of contact $i$ is replaced by a [polyhedral cone](/polyhedral-friction-cone/) with $k$ edges. In generalized coordinates, $n_i$ is the row $\partial \phi_i / \partial q$ written as a column, and $d_{i1}, \ldots, d_{ik}$ map $v$ to the tangential velocity of the contact point along the $k$ edge directions. The edges come in opposite pairs, so $k$ is even; in the plane $k = 2$. The matrices $N$ and $D$ have the $n_i$ and the $d_{ij}$ as columns. $E$ is block diagonal with one column of ones of length $k$ per contact, and $U = \mathrm{diag}(\mu_i)$ holds the friction coefficients.

An LCP with a square matrix $A$ and a vector $b$ asks for a vector $z \ge 0$ with $w = A z + b \ge 0$ and $z_i w_i = 0$ for every $i$. In words: each pair $(z_i, w_i)$ is nonnegative, and at least one member of the pair is 0.

Input: $q$, $v$, the step $h$, the forces $f$ and the contact data. Output: $q^+$ and $v^+$ after one step, and the impulses $c_n$ (normal) and $\beta$ (friction, one per edge) that act in the step.

## The algorithm

```pseudo id=main
STEWART-TRINKLE-STEP(q, v, h)
L1  f ← τ - C(q, v) v - g(q)                          ▷ all forces but contact
L2  v* ← v + h M^-1 f                                 ▷ the velocity without contact
L3  for each contact i with φ_i(q) ≤ ε do collect φ_i, n_i and d_i1, ..., d_ik
L4  A_GG ← G^T M^-1 G with G = [N D]
L5  A ← [A_GG, (0; E); (U, -E^T), 0]
L6  b ← (N^T v* + φ / h, D^T v*, 0)
L7  z = (c_n, β, λ) ← LEMKE(A, b)
L8  v+ ← v* + M^-1 (N c_n + D β)
L9  q+ ← q + h v+
SIMULATE(q, v, h, steps)
L10 repeat STEWART-TRINKLE-STEP steps times
LEMKE(A, b)
L11 if b ≥ 0 then return z = 0
L12 tableau [I | -A | -e | b] with the w variables in the basis
L13 r ← row of the smallest b_r (the last such row on ties); z0 enters
L14 loop
L15     pivot on row r and the entering column
L16     if the leaving variable is z0 then exit the loop
L17     entering ← the complement of the leaving variable
L18     r ← lexicographic minimum ratio row of the entering column
L19     if there is no such row then return RAY
L20 return z read from the basis
```

The matrix of line L5 written out is
$$A = \begin{pmatrix} N^T M^{-1} N & N^T M^{-1} D & 0 \\ D^T M^{-1} N & D^T M^{-1} D & E \\ U & -E^T & 0 \end{pmatrix}, \qquad z = \begin{pmatrix} c_n \\ \beta \\ \lambda \end{pmatrix}.$$
The three block rows of $w = A z + b$ are, by line L8, $N^T v^+ + \phi/h$, $D^T v^+ + E\lambda$ and $U c_n - E^T \beta$. So the three complementarity conditions say:

- $c_{n,i} \ge 0$, $\phi_i + h\, n_i^T v^+ \ge 0$, and one of them is 0: the contact can only push, the gap at the end of the step is not negative to first order, and a contact that separates has no impulse.
- $\beta_{ij} \ge 0$, $d_{ij}^T v^+ + \lambda_i \ge 0$, and one of them is 0: friction acts only along the edges against which the contact slides fastest, and $\lambda_i$ is the slip speed.
- $\lambda_i \ge 0$, $\mu_i c_{n,i} - \sum_j \beta_{ij} \ge 0$, and one of them is 0: friction stays in the linearized cone, and it is on the boundary of the cone when the contact slides.

The term $\phi/h$ in line L6 is the position part. It lets a contact with a small positive gap close without an impulse, and it pushes out a contact that already overlaps. Without it, the LCP is the velocity form of Anitescu and Potra (1997). Line L3 takes every contact that is closer than a distance $\varepsilon$, so that a contact can become active within the step.

Lines L11 to L20 are Lemke's method for the LCP: line L12 adds an artificial variable $z_0$ with the covering vector $e$ of ones, which gives a first basis that is not negative, and the pivots of lines L15 to L18 move from one almost complementary basis to the next until $z_0$ leaves the basis. This page does not depend on Lemke's method; any LCP solver can replace line L7.

## Example

A particle of mass 1 kg rests on the floor with $\mu = 0.5$, $g = 9.81$ m/s$^2$ and $h = 0.01$ s. A horizontal force of 7 N pushes it. With one contact and the two friction edges $\pm x$, the LCP has the four unknowns $(c_n, \beta_+, \beta_-, \lambda)$. Line L2 gives $v^* = (0.07, -0.0981)$ m/s, and
$$A = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & -1 & 1 \\ 0 & -1 & 1 & 1 \\ 0.5 & -1 & -1 & 0 \end{pmatrix}, \qquad b = \begin{pmatrix} -0.0981 \\ 0.07 \\ -0.07 \\ 0 \end{pmatrix}.$$

Lemke's method takes four pivots:

| Pivot | Enters | Leaves | Basic values after the pivot |
|---|---|---|---|
| 1 | $z_0$ | $w_{c_n}$ | $z_0 = 0.0981$, $w_{\beta+} = 0.1681$, $w_{\beta-} = 0.0281$, $w_\lambda = 0.0981$ |
| 2 | $c_n$ | $w_{\beta-}$ | $z_0 = 0.07$, $w_{\beta+} = 0.14$, $c_n = 0.0281$, $w_\lambda = 0.08405$ |
| 3 | $\beta_-$ | $w_\lambda$ | $z_0 = 0.013967$, $w_{\beta+} = 0.027933$, $c_n = 0.084133$, $\beta_- = 0.056033$ |
| 4 | $\lambda$ | $z_0$ | $\lambda = 0.02095$, $w_{\beta+} = 0.0419$, $c_n = 0.0981$, $\beta_- = 0.04905$ |

So $c_n = 0.0981$ N s, which is the weight times $h$, and $\beta_- = 0.04905$ N s $= \mu c_n$: friction acts in the $-x$ direction at its limit. Line L8 gives $v^+ = (0.07 - 0.04905, 0) = (0.02095, 0)$ m/s, so the particle slides with the acceleration $7 - 4.905 = 2.095$ m/s$^2$, and $\lambda = 0.02095$ m/s is its slip speed. With a push of 3 N in place of 7 N, the same LCP gives $\beta_- = 0.03$ N s and $v^+ = 0$: the particle sticks.

For a planar block of 2 kg, 0.4 m wide, sliding at 1 m/s on its two lower corners with $\mu = 0.4$ and $h = 0.01$ s, one step gives the normal impulses 0.07848 N s at the rear corner and 0.11772 N s at the front corner. Their sum is the weight times $h$. The friction impulse is $0.4 \times 0.1962 = 0.07848$ N s, and the speed falls to 0.96076 m/s.

## Correctness

Every solution of the LCP satisfies discrete forms of the contact laws: the gap at the end of the step is not negative to first order, the impulse lies in the linearized friction cone, and friction maximizes the dissipation over that cone (it is the solution of a small linear program whose KKT conditions are the second and third complementarity conditions). If all active gaps are at least 0 at the start of the step, the contact impulses do not add kinetic energy: $\tfrac12 (v^+)^T M v^+ \le \tfrac12 (v^*)^T M v^*$. Lemke's method with the lexicographic rule stops after a finite number of pivots, and when $z_0$ leaves the basis, the result solves the LCP. These are theorems; the proofs are in the correctness proof of this page.

Lemke's method can also stop on a ray, without a solution. For the velocity form without $\phi/h$, Anitescu and Potra (1997) proved that a solution always exists and that Lemke's method finds it. With the gap term, Trinkle, Berard and Pang (2005) call the LCP nearly always solvable. As $h \to 0$, the scheme converges, in the sense of measures, to a solution of the measure differential inclusion of rigid body motion with Coulomb friction (Stewart 1998); this is how the scheme resolves the Painlevé paradox.

## Complexity

In the [real RAM](/real-ram/), with $n$ velocities and $c$ active contacts with $k$ edges, the LCP has $m = c(k + 2)$ unknowns. Lines L2 to L6 cost $O(n^3 + n^2 m + n m^2)$ with a Cholesky factor of $M$, or $O(n + m^2)$ when the bodies are free so that $M$ is block diagonal. Each pivot of Lemke's method costs $\Theta(m^2)$. The number of pivots is at most $m\, 2^{m-1} + 1$, the number of almost complementary bases plus one, and it is exponential in $m$ for some LCPs (Murty 1978). In practice it is a small multiple of $m$ for the matrices of contact problems; this is an observation, not a bound. The extra space is $\Theta(n^2 + m^2)$.

## Properties

- **Impulses, not forces.** The unknowns are impulses over the step. A step can stop a sliding body at once, which the force form cannot do.
- **First order.** The velocity update is a semi-implicit Euler step, so the global error is $O(h)$ for smooth motion. Each impact is perfectly inelastic: the normal velocity after the impact is 0.
- **Not unique.** The LCP can have many solutions. For the block of the example at rest on two corners, the two friction impulses can push against each other by any amount that stays in the cones; the LCP for one step then has 17 basic solutions, but they all give the same $v^+$. Uniqueness of $v^+$ is not a general property of the scheme.
- **Linearized cone.** The cone with $k$ edges is inside or outside the true circular cone, depending on how the edges are placed; in the plane with $k = 2$ it is exact.
- **The gap term can add energy.** With an overlap $\phi_i < 0$, the term $\phi_i / h$ pushes the bodies apart with a velocity $-\phi_i / h$, and that adds kinetic energy.

## Variants and improvements

- **Anitescu and Potra (1997).** The velocity form without $\phi/h$ in $b$. Its LCP always has a solution and Lemke's method finds it. When the LCP with the gap term has no solution, a simulator can drop the gap term for that step and solve this one (Trinkle, Berard and Pang 2005).
- **Nonlinear cone.** A second-order cone in place of the polyhedral cone gives a nonlinear complementarity problem. Anitescu (2006) relaxed it to a convex cone program, which is solved by [second-order cone programming](/second-order-cone-programming/).
- **Iterative solvers.** Physics engines often solve the LCP of a step approximately by projected Gauss-Seidel: they sweep over the contacts and solve one contact at a time. This is fast and robust but gives an approximate answer.
- **Contact-implicit planning.** [Contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/) uses the same complementarity constraints over a whole trajectory, as constraints of a nonlinear program.

## When to use it

Use it to simulate robots, grasps and parts with many contacts and with friction, when the bodies may stick, slide, separate and collide, and when a fixed step is acceptable. It is a sound choice where the force and acceleration form has no solution or several, as in the Painlevé examples. If the contact set does not change, a smooth model with known constraint forces, for example the [manipulator equation](/manipulator-equation/) with fixed contacts, is cheaper and more accurate. For soft contacts, a penalty model with springs avoids the LCP, at the cost of stiff equations.

## Pitfalls

- **The sign of the edge directions.** The friction edges must come in opposite pairs, so that friction can act in every tangent direction. With only $+d$, the contact can only be pushed one way.
- **A large $\varepsilon$.** Contacts far from touching enter the LCP. With the term $\phi/h$, they stay free, but the LCP grows.
- **Penetration drift without the gap term.** The velocity form keeps $n_i^T v^+ \ge 0$ only, so small overlaps add up over many steps. The term $\phi/h$ removes them, but it can add energy; some codes use a fraction of $\phi/h$.
- **Rotations in space.** Line L9 is correct for coordinates such as $(x, y, \theta)$ in the plane. For a body in space, the orientation must be updated with the exponential map, not by adding $h \omega$ to angles.
- **Degenerate pivots.** Contact LCPs are often degenerate, for example a block with four corners on the floor. Lemke's method without the lexicographic rule can then cycle.

## Implementations

## History

Stewart and Trinkle (1996) formulated rigid body dynamics with inelastic collisions and Coulomb friction as a time-stepping scheme in which each step solves a complementarity problem in impulses and velocities, and they showed that it has a solution where the force form does not. Anitescu and Potra (1997) gave the velocity form, and proved that its LCP is always solvable and that Lemke's method solves it. Stewart (1998) proved convergence of the time-stepping scheme as the step goes to 0, which resolved Painlevé's problem in the measure sense, and Stewart (2000) surveyed the field in SIAM Review. Lemke's method (1965) comes from the computation of equilibria of bimatrix games.

## References
