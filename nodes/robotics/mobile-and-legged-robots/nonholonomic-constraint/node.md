---
tag: VMFRKS
kind: definition
slug: nonholonomic-constraint
name: Nonholonomic constraint
aliases:
- non-integrable velocity constraint
area: robotics/mobile-and-legged-robots
level: core
summary: A constraint on velocities that cannot be integrated to one on positions, such as a wheel that rolls without slipping sideways.
prereqs: [pfaffian-constraint, lie-bracket, configuration-space]
see_also: [lie-algebra-rank-condition, brockett-condition, unicycle-model, differential-drive-model, kinematic-bicycle-model, controllability, control-affine-system, differential-flatness]
sources:
  - book: isbn:9780849379819
    title: "Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994"
    locator: "Chapter 7 (nonholonomic behavior in robotic systems: Pfaffian constraints, controllability and Frobenius' theorem, examples of nonholonomic systems)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 2.4 (holonomic and nonholonomic constraints) and Section 13.3.2 (controllability of the wheeled robot)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 13.1 (velocity constraints on the configuration space) and Section 15.4 (nonholonomic system theory: distributions, Lie brackets and the Frobenius and Chow theorems)"
  - book: isbn:9783540762195
    title: "Jean-Paul Laumond (editor), Robot Motion Planning and Control, Lecture Notes in Control and Information Sciences 229, Springer, 1998"
    locator: "the chapters Guidelines in nonholonomic motion planning for mobile robots and Geometry of nonholonomic systems"
---

A nonholonomic constraint is a constraint on the velocities of a mechanical system that cannot be integrated into a constraint on its positions. The standard case is a wheel that rolls without slipping sideways: the wheel cannot move in the direction of its axle at any instant, but it can still reach every position and heading by a sequence of motions, as a driver does to park a car. In control terms, the allowed velocities at a configuration $q \in \mathbb{R}^n$ form a subspace of dimension $m < n$, and the system is a driftless [control-affine system](/control-affine-system/) $\dot q = g_1(q) u_1 + \dots + g_m(q) u_m$. The constraint is nonholonomic when the [Lie brackets](/lie-bracket/) of the $g_i$ give directions outside this subspace. Then the [Lie algebra rank condition](/lie-algebra-rank-condition/) and the Chow-Rashevskii theorem give controllability, but [Brockett's condition](/brockett-condition/) fails, so no continuous time-invariant state feedback makes a rest point asymptotically stable. A [Pfaffian constraint](/pfaffian-constraint/) is the common form of a velocity constraint, linear in the velocities; it can be holonomic or nonholonomic, and this page is about the property that tells the two apart.

## Definition

**Setting.** The configuration space is a connected smooth manifold $Q$ of dimension $n$, with local coordinates $q$. The system is subject to $k$ velocity constraints in Pfaffian form,

$$A(q)\,\dot q = 0, \qquad A(q) \in \mathbb{R}^{k \times n}, \quad \operatorname{rank} A(q) = k \text{ for all } q,$$

with $A$ smooth. The allowed velocities at $q$ are the null space $\Delta(q) = \ker A(q)$, of dimension $m = n - k$. Choose smooth vector fields $g_1, \dots, g_m$ that span $\Delta(q)$ at each $q$. Then the motions that respect the constraints are exactly the solutions of $\dot q = \sum_i g_i(q) u_i(t)$ for some inputs $u_i$.

**Holonomic.** The constraints are **holonomic**, or integrable, if there are $k$ smooth functions $h_1, \dots, h_k$ with independent differentials such that the rows of $A(q)$ and the rows $\partial h_j / \partial q$ span the same subspace at every $q$. Then every allowed motion keeps $h(q(t))$ constant, so the constraints are really constraints on the configuration: the system moves on a level set $h(q) = c$ of dimension $m$. This is a definition, and it can hold only locally.

**Nonholonomic.** The constraints are **nonholonomic** if they are not holonomic. They are **completely nonholonomic** if no nonzero combination of them is integrable, and **partially nonholonomic** if some combination is.

**The Frobenius test.** The distribution $\Delta$ is **involutive** if $[g_i, g_j](q) \in \Delta(q)$ for all $i, j$ and all $q$, with the bracket $[f, g] = (Dg) f - (Df) g$. The theorem of Frobenius states that the constraints are holonomic if and only if $\Delta$ is involutive. More generally, let $\bar\Delta$ be the involutive closure of $\Delta$, the span of the $g_i$ and of all their iterated brackets, and assume its dimension $n - p$ is constant. Then exactly $p$ independent combinations of the constraints are integrable, and the other $k - p$ are nonholonomic. The constraints are completely nonholonomic when $\bar\Delta(q) = \mathbb{R}^n$ at every $q$, that is, when the $g_i$ satisfy the [Lie algebra rank condition](/lie-algebra-rank-condition/) everywhere.

**Consequences (theorems).**

- Chow-Rashevskii: if the constraints are completely nonholonomic and $Q$ is connected, any two configurations are joined by a motion that respects the constraints. So the system is [controllable](/controllability/) with $m < n$ inputs, and the set of reachable configurations has dimension $n$, while the velocity at each instant is in a space of dimension $m$.
- If $p$ combinations are integrable, every motion stays on a level set of dimension $n - p$, and Chow-Rashevskii applies on that level set.
- Brockett: for a driftless system with $m < n$ and independent $g_i$ at the rest point $q^*$, the map $(q, u) \mapsto \sum_i g_i(q) u_i$ does not cover a neighborhood of $0$, so no continuous feedback $u = k(q)$ makes $q^*$ asymptotically stable. A nonholonomic robot needs time-varying or discontinuous feedback to park at a point. Tracking a moving reference with nonzero speed does not have this obstruction.

## Examples and non-examples

**The rolling wheel, the standard case.** A wheel, or a [unicycle](/unicycle-model/), on the plane has configuration $q = (x, y, \theta)$: the contact point and the heading. Rolling without sideways slip is the single constraint $\dot x \sin\theta - \dot y \cos\theta = 0$, so $A = [\sin\theta, -\cos\theta, 0]$. The allowed velocities are spanned by

$$g_1 = (\cos\theta, \sin\theta, 0), \qquad g_2 = (0, 0, 1),$$

driving forward and turning on the spot. Only $g_1$ depends on $q$, so $[g_1, g_2] = -(Dg_1)\, g_2 = -\partial g_1 / \partial\theta = (\sin\theta, -\cos\theta, 0)$. This is the sideways direction, which the constraint forbids. The determinant of the matrix with columns $g_1, g_2, [g_1, g_2]$ is $\cos^2\theta + \sin^2\theta = 1$, so the three fields span $\mathbb{R}^3$ at every $q$. The distribution is not involutive, so the constraint is nonholonomic; in fact it is completely nonholonomic, and by Chow-Rashevskii the wheel can reach every pose. The bracket also tells how: forward, turn, backward, turn back, each for a small time $\varepsilon$, gives a net motion of about $\varepsilon^2 [g_1, g_2]$, a small sideways step. This is the basis of parallel parking.

**A wheel on a line, a non-example.** A wheel of radius $r$ that rolls on a straight line has configuration $(x, \varphi)$, the position of the center and the angle of the wheel. Rolling without slip is $\dot x - r\dot\varphi = 0$. This integrates to $x - r\varphi = c$. The constraint is holonomic: rolling does not make a constraint nonholonomic by itself. A single Pfaffian constraint in two variables is always integrable near points where $A \ne 0$, because $\Delta$ then has dimension 1 and every bracket $[g_1, g_1] = 0$.

**The vertical rolling disk.** A disk of radius $r$ that rolls upright on the plane has $q = (x, y, \theta, \varphi)$, with $\varphi$ the rolling angle. The two constraints $\dot x = r\dot\varphi\cos\theta$ and $\dot y = r\dot\varphi\sin\theta$ leave $g_1 = (r\cos\theta, r\sin\theta, 0, 1)$ and $g_2 = (0, 0, 1, 0)$. The brackets are $g_3 = [g_1, g_2] = (r\sin\theta, -r\cos\theta, 0, 0)$ and $g_4 = [g_2, g_3] = (r\cos\theta, r\sin\theta, 0, 0)$. The determinant of $[g_1, g_2, g_3, g_4]$ is $-r^2$; for example $-0.0025$ for $r = 0.05$ m. It is not zero, so both constraints are nonholonomic, and the disk can reach any position, heading and wheel angle. A bracket of depth two is needed, one more than for the unicycle.

**A partially nonholonomic robot.** A [differential-drive robot](/differential-drive-model/) with the wheel angles in the state has three constraints in five variables. One combination of them integrates: the heading equals a fixed multiple of the difference of the wheel angles, plus a constant. So the reachable set has dimension 4, not 5, and the other two constraints are nonholonomic.

**Not a velocity constraint.** A joint limit $q_1 \le 1$ or an obstacle restricts positions with an inequality. Some authors also call such constraints nonholonomic, but they reduce the configuration space and do not restrict the directions of motion inside it. This page uses the word only for equality constraints on velocities.

## Related definitions

- [Pfaffian constraint](/pfaffian-constraint/): the form $A(q)\dot q = 0$, which can be holonomic or nonholonomic.
- [Lie bracket](/lie-bracket/): the vector field that the Frobenius test and the Chow-Rashevskii theorem use.
- [Lie algebra rank condition](/lie-algebra-rank-condition/): the brackets span the tangent space; for constraints, this is complete nonholonomy.
- [Brockett's condition](/brockett-condition/): the obstruction to continuous stabilizing feedback that nonholonomic systems fail.
- [Controllability](/controllability/): what Chow-Rashevskii gives for a completely nonholonomic system.
- [Unicycle model](/unicycle-model/), [kinematic bicycle model](/kinematic-bicycle-model/): the standard nonholonomic robots. An [omnidirectional robot](/omnidirectional-robot-kinematics/) has no nonholonomic constraint on its chassis.
- [Configuration space](/configuration-space/): holonomic constraints shrink it; nonholonomic constraints restrict the directions of motion in it.

## References
