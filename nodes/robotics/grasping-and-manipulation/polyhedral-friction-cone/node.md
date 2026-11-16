---
tag: MHHJV1
kind: technique
slug: polyhedral-friction-cone
name: Polyhedral friction cone approximation
aliases:
- linearized friction cone
area: robotics/grasping-and-manipulation
level: core
summary: Replaces the circular Coulomb friction cone by a pyramid with k edges, so that contact force constraints become linear and fit in linear programs and LCPs.
prereqs: [friction-cone, conic-hull]
see_also: [friction-cone, force-closure-test, grasp-wrench-space, contact-wrench-cone, stewart-trinkle-time-stepping, second-order-cone-programming, convex-mpc-legged-locomotion, whole-body-control]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12, Section 12.2.1 (Friction), the friction cone approximated by a polyhedral cone, and Section 12.2.3 (force closure with the edges of the cones)
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.2 (Force Closure), the linearized friction cone of equation (38.59), inscribed, and the circumscribed cone with mu / cos(pi / n_g); the chapter is pages 955 to 988"
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (friction cones and contact models)
  - paper: doi:10.1002/(SICI)1097-0207(19960815)39:15<2673::AID-NME972>3.0.CO;2-I
    title: "David E. Stewart and Jeffrey C. Trinkle, An implicit time-stepping scheme for rigid body dynamics with inelastic collisions and Coulomb friction, International Journal for Numerical Methods in Engineering 39(15), 2673-2691, 1996"
    locator: the linear complementarity formulation, which uses a polyhedral approximation of the friction cone
---

The circular [friction cone](/friction-cone/) $\lVert f_t \rVert \le \mu f_n$ is convex but not polyhedral, so a contact force constraint with it is not linear. The polyhedral approximation replaces the cone by a pyramid: the set of nonnegative combinations of $k$ edge vectors. Each contact force then becomes $f = \sum_j a_j e_j$ with $a_j \ge 0$, a linear constraint, and grasp analysis, force optimization and contact simulation can use linear programs and linear complementarity problems. The price is an error that depends on $k$ and on the choice between an inner and an outer pyramid.

## In plain words

A friction cone is like an ice cream cone standing on the contact point. Any push that stays inside the cone is safe; the finger does not slip. Round shapes are awkward for some solvers, which want flat sides. So we cut the round cone into a pyramid with a few flat sides. If the corners of the pyramid touch the round cone, the pyramid fits inside it, and anything the pyramid allows is safe, but a few safe pushes are lost. If the flat sides touch the round cone instead, the pyramid is larger, and it allows a few pushes that really slip. More sides make the error smaller and the problem bigger.

## When it applies

- The contact model is a point contact with Coulomb friction, or a soft finger whose torsion limit is also linearized ([grasp contact models](/grasp-contact-models/)).
- The problem around the contacts is linear: a feasibility test, a linear program, or a linear complementarity problem. A solver that handles second-order cones directly does not need the approximation.
- The error of the pyramid is acceptable, or its direction is the safe one for the question: an inner pyramid for a test that must not accept a bad grasp, an outer pyramid for a bound that must not reject a feasible motion.
- In the plane the method is exact: a planar cone has exactly the two edges $n \pm \mu t$.

## The template

The input is the inward unit normal $n$ at the contact, the coefficient $\mu$, and the number of edges $k \ge 3$. The output is the list of edges; the pyramid is their [conic hull](/conic-hull/).

```pseudo id=main
LINEARIZE-CONE(n, μ, k, outer)
L1  choose unit tangents t1, t2 with (t1, t2, n) orthonormal
L2  if outer then ν ← μ / cos(π/k) else ν ← μ
L3  for j = 0 to k - 1 do
L4      θ ← 2πj / k
L5      e_j ← n + ν (cos θ · t1 + sin θ · t2)
L6  return (e_0, ..., e_{k-1})          ▷ FC_k = { Σ a_j e_j : a_j ≥ 0 }
```

Then replace each constraint "$f$ is in the friction cone" by "$f = \sum_j a_j e_j$ with $a_j \ge 0$". The normal force is $f_n = \sum_j a_j$, because each edge has normal component 1. A wrench constraint follows by linearity: the contact can apply exactly the wrenches $\sum_j a_j (p \times e_j, e_j)$.

**Why the error is $\cos(\pi/k)$.** Cut the cone at $f_n = 1$. The section of the true cone is a disc of radius $\mu$ in the tangent plane. With $\nu = \mu$ (L2), the edges hit the circle at the vertices of a regular $k$-gon inscribed in the disc. The inradius of that $k$-gon is $\mu \cos(\pi/k)$, so in the worst tangential direction, halfway between two edges, the pyramid allows only $\mu \cos(\pi/k)$ where the true cone allows $\mu$. With $\nu = \mu / \cos(\pi/k)$ the $k$-gon is circumscribed about the disc: its inradius is $\mu$, and its vertices reach $\mu / \cos(\pi/k)$ in the directions of the edges.

| $k$ | inner: worst tangential reach $\cos(\pi/k)$ | outer: worst overreach $1/\cos(\pi/k)$ | inner: area of the section |
|---|---|---|---|
| 3 | 0.5000 | 2.0000 | 0.4135 |
| 4 | 0.7071 | 1.4142 | 0.6366 |
| 6 | 0.8660 | 1.1547 | 0.8270 |
| 8 | 0.9239 | 1.0824 | 0.9003 |
| 16 | 0.9808 | 1.0196 | 0.9745 |

The area column is the area of the inscribed $k$-gon divided by the area of the disc, $k \sin(2\pi/k) / (2\pi)$. An inner pyramid within 5 percent of the true cone in every direction needs $k \ge 10$; within 1 percent it needs $k \ge 23$.

## Classic examples

**Force-closure test.** The [force-closure test](/force-closure-test/) turns each edge into a primitive wrench and asks for a strictly positive combination that sums to zero. With an inner pyramid, a CLOSED answer is also true for the circular cones. Two hard fingers in space with $k = 4$ show the usual size: 8 primitive wrenches in $\mathbb{R}^6$.

**The friction box of legged robots.** Controllers for walking robots often write the friction constraint as $\lvert f_x \rvert \le \mu f_z$ and $\lvert f_y \rvert \le \mu f_z$. This is a 4-edge pyramid with $\nu = \mu \sqrt{2}$ along the diagonals, that is the outer pyramid of the template rotated by 45 degrees. Its corners reach $\sqrt{2} \mu \approx 1.414 \mu$, so a force in a diagonal direction can pass the constraint and still slip. Replacing $\mu$ by $\mu / \sqrt{2}$ gives the inner pyramid. The [contact wrench cone](/contact-wrench-cone/) of a flat foot and the quadratic programs of [whole-body control](/whole-body-control/) and [convex MPC](/convex-mpc-legged-locomotion/) use such pyramids.

**Time-stepping simulation.** Stewart and Trinkle (1996) write each step of a rigid body simulation with Coulomb friction as a linear complementarity problem. The tangential force is a nonnegative combination of $k$ directions in the tangent plane, so the friction cone is a pyramid; see [Stewart-Trinkle time-stepping](/stewart-trinkle-time-stepping/). The direction of the sliding friction force is then one of the $k$ directions, which makes a sliding body turn slightly toward an edge of the pyramid.

**Grasp force optimization.** To hold an object with the least squeeze, minimize the sum of the normal forces $\sum_i \sum_j a_{ij}$ subject to the balance of wrenches and $a_{ij} \ge 0$. With pyramids this is a linear program.

## Variations

- **Inner, outer, or in between.** The inner pyramid ($\nu = \mu$) gives sufficient conditions for the true cone; the outer pyramid ($\nu = \mu / \cos(\pi/k)$) gives necessary conditions. Some codes use a pyramid of equal area, which has no guarantee in either direction.
- **Edges aligned with the load.** A pyramid with one edge in the direction of the expected tangential load has no error in that direction. Only the directions between edges lose capacity.
- **Soft fingers.** The soft finger contact adds a torsional moment about the normal with $\lvert m_n \rvert \le \gamma f_n$. Each edge $e_j$ is then used twice, with the moments $+\gamma n$ and $-\gamma n$. The Handbook also describes models that couple the twist limit and the friction limit (Howe and Cutkosky 1996); they are not polyhedral.
- **Exact cones.** A [second-order cone program](/second-order-cone-programming/) keeps the circular cone and avoids the error, at the price of an interior point solver.
- **Refinement.** The pyramid with $2k$ edges contains the one with $k$ edges when the edges of the first are among those of the second. A test that answers CLOSED with $k$ edges then also answers CLOSED with $2k$.

## Pitfalls

- **Calling an outer pyramid conservative.** The friction box $\lvert f_x \rvert, \lvert f_y \rvert \le \mu f_z$ is larger than the cone. A force that passes it can slip.
- **A wrong tangent basis.** The tangents $t_1, t_2$ must be orthogonal to $n$ and to each other, with unit length. A tangent that is not orthogonal to $n$ tilts the whole pyramid.
- **Unnormalized normals.** If $n$ is not a unit vector, $\mu$ is scaled by the wrong amount and the cone has the wrong angle.
- **Too many edges.** The number of variables is $ck$ for $c$ contacts. A large $k$ makes the program bigger and more degenerate, while the error falls only like $\pi^2 / (2k^2)$.
- **Anisotropic sliding.** In a simulation, a pyramid with few edges makes a sliding body prefer the directions of the edges. This is an artifact of the approximation, not of Coulomb's law.
- **The plane needs no approximation.** A planar contact has exactly two edges. Using more edges in the plane only adds redundant columns.

## Exercises

1. Show that a regular $k$-gon inscribed in a circle of radius $\mu$ has inradius $\mu \cos(\pi/k)$, and conclude the inner column of the table.
2. Find the least $k$ for which the inner pyramid loses at most 1 percent of the tangential capacity in every direction. (Answer: $k = 23$, since $\cos(\pi/22) \approx 0.98982$ and $\cos(\pi/23) \approx 0.99068$.)
3. Show that the friction box $\lvert f_x \rvert \le \mu f_z$, $\lvert f_y \rvert \le \mu f_z$ contains the circular cone, and that a force at 45 degrees can exceed the true limit by the factor $\sqrt{2}$.
4. Show that a pyramid whose edges lie on the cone is contained in the cone, using the convexity of the cone.

## References
