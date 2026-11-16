---
tag: 81FG3K
kind: theorem
slug: gauss-principle-of-least-constraint
name: Gauss principle of least constraint
aliases:
- Gauss principle
area: robotics/robot-dynamics
level: advanced
summary: For ideal constraints, the true acceleration minimizes (x - a)^T M (x - a) over the accelerations the constraints allow, where a is the acceleration without constraints.
prereqs: [manipulator-equation, quadratic-programming, lagrange-multiplier]
see_also: [kanes-method, pfaffian-constraint, kkt-conditions, rigid-contact-complementarity, forward-dynamics, pseudoinverse, nonholonomic-constraint, euler-lagrange-manipulator-dynamics]
sources:
  - paper: doi:10.1515/crll.1829.4.232
    title: Carl Friedrich Gauss, Über ein neues allgemeines Grundgesetz der Mechanik, Journal für die reine und angewandte Mathematik 4, 232-235, 1829
    locator: the whole paper (the principle stated for a system of particles)
  - paper: doi:10.1098/rspa.1992.0158
    title: Firdaus E. Udwadia and Robert E. Kalaba, A new perspective on constrained motion, Proceedings of the Royal Society of London A 439(1906), 407-410, 1992
    locator: the whole paper (the explicit equation of constrained motion with the Moore-Penrose inverse)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8, Section 8.7 (constrained dynamics)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: "Chapter 6, Section 6.1.2 (holonomic constraints and virtual work) and Section 6.1.3 (D'Alembert's principle)"
---

The Gauss principle of least constraint says that a mechanical system with ideal constraints accelerates in the way that differs least from its free motion, where the difference is measured with the mass matrix. If $a$ is the acceleration the system would have without the constraints, the true acceleration minimizes $(x - a)^T M (x - a)$ over all accelerations $x$ that the constraints allow. So constrained dynamics is a [quadratic program](/quadratic-programming/) at each instant. Udwadia and Kalaba (1992) solved this program in closed form.

## Statement

Let a system have generalized coordinates $q \in \mathbb{R}^n$ and the equation of motion $M(q)\ddot q = Q(q, \dot q, t) + Q_c$, where $M(q)$ is symmetric positive definite, $Q$ collects all applied, Coriolis, centripetal and gravity forces (for a robot, $Q = \tau - C(q, \dot q)\dot q - g(q)$), and $Q_c$ is the generalized force of the constraints. Let the constraints, holonomic or nonholonomic, be written at the level of accelerations as

$$A(q, \dot q, t)\,\ddot q = b(q, \dot q, t),$$

with $A \in \mathbb{R}^{m \times n}$, and assume that this linear system has at least one solution. (A holonomic constraint $\phi(q, t) = 0$ is differentiated twice and a Pfaffian constraint $A(q)\dot q = 0$ once.) Assume the constraints are ideal: $w^TQ_c = 0$ for every $w$ with $Aw = 0$.

Let $a = M^{-1}Q$ be the unconstrained acceleration. Then the true acceleration $\ddot q$ is the unique minimizer of

$$G(x) = (x - a)^T M\,(x - a)\quad\text{subject to}\quad Ax = b.$$

For every feasible $x$, $G(x) = G(\ddot q) + (x - \ddot q)^TM(x - \ddot q)$. If $A$ has full row rank, the minimizer is

$$\ddot q = a + M^{-1}A^T\big(AM^{-1}A^T\big)^{-1}(b - Aa),$$

and in general it is $\ddot q = a + M^{-1/2}\big(AM^{-1/2}\big)^{+}(b - Aa)$, where $^{+}$ is the [Moore-Penrose pseudoinverse](/pseudoinverse/) (Udwadia and Kalaba 1992).

For $N$ particles with masses $m_i$, applied forces $F_i$ and accelerations $\ddot r_i$, Gauss's original form says that the quantity $\sum_i m_i\,\|\ddot r_i - F_i/m_i\|^2$ is smallest for the true motion among all accelerations that the constraints allow.

## In plain words

Imagine the system with its constraints removed. Each part would accelerate in its own way, pushed only by the applied forces. The constraints stop that. The principle says that nature corrects the free motion as little as possible, and it counts a correction to a heavy part as more costly than the same correction to a light part. So the real motion is the allowed motion that is closest to the free motion, with mass as the measure of distance.

## Proof

Ideal constraints give $Q_c \in \mathrm{range}(A^T)$. The condition $w^TQ_c = 0$ for all $w \in \ker A$ says that $Q_c$ lies in $(\ker A)^\perp$, and $(\ker A)^\perp = \mathrm{range}(A^T)$. So $Q_c = A^T\lambda$ for some $\lambda \in \mathbb{R}^m$, the [Lagrange multipliers](/lagrange-multiplier/) of the constraints.

The true acceleration is feasible and minimal. From the equation of motion, $M(\ddot q - a) = Q_c = A^T\lambda$, and $A\ddot q = b$. Let $x$ be any feasible acceleration, so $A(x - \ddot q) = 0$. Write $x - a = (x - \ddot q) + (\ddot q - a)$ and expand:

$$G(x) = (x - \ddot q)^TM(x - \ddot q) + 2(x - \ddot q)^TM(\ddot q - a) + G(\ddot q).$$

The middle term is $2(x - \ddot q)^TA^T\lambda = 2\big(A(x - \ddot q)\big)^T\lambda = 0$. So $G(x) = G(\ddot q) + (x - \ddot q)^TM(x - \ddot q) \ge G(\ddot q)$, with equality only when $x = \ddot q$ because $M$ is positive definite.

The closed form. The problem is a strictly convex quadratic program with linear equality constraints, so its [KKT conditions](/kkt-conditions/) are necessary and sufficient: $M(x - a) = A^T\lambda$ and $Ax = b$. The first gives $x = a + M^{-1}A^T\lambda$. Put this in the second: $AM^{-1}A^T\lambda = b - Aa$. If $A$ has full row rank, $AM^{-1}A^T$ is positive definite, so $\lambda = (AM^{-1}A^T)^{-1}(b - Aa)$, which gives the formula. In general, substitute $y = M^{1/2}(x - a)$: the problem becomes the minimum-norm solution of $AM^{-1/2}y = b - Aa$, which is $y = (AM^{-1/2})^{+}(b - Aa)$, and $x = a + M^{-1/2}y$. $\square$

## Consequences

A worked example: the Atwood machine. Two masses $m_1 = 1$ kg and $m_2 = 3$ kg hang on the two ends of a string over a massless pulley without friction. Their heights are $x_1$ and $x_2$, measured upward. Without the string, both fall: $a = (-9.81, -9.81)$ m/s$^2$. The string keeps $x_1 + x_2$ constant, so $A = [1, 1]$ and $b = 0$. With $M = \mathrm{diag}(1, 3)$:

$$AM^{-1}A^T = 1 + \tfrac13 = \tfrac43,\qquad b - Aa = 19.62,\qquad \lambda = \tfrac34 \cdot 19.62 = 14.715,$$

$$\ddot q = a + M^{-1}A^T\lambda = (-9.81 + 14.715,\ -9.81 + 4.905) = (4.905, -4.905)\ \text{m/s}^2.$$

The light mass rises at $g/2$ and the heavy mass falls at $g/2$. The multiplier $\lambda = 14.715$ N is the tension in the string, which matches the textbook value $2m_1m_2g/(m_1 + m_2)$. The minimum is $G(\ddot q) = 1 \cdot 14.715^2 + 3 \cdot 4.905^2 = 288.7$ (that is, $3g^2$). The feasible acceleration $x = (0, 0)$ gives $G = 1 \cdot 9.81^2 + 3 \cdot 9.81^2 = 4g^2$, and the difference $g^2$ equals $(x - \ddot q)^TM(x - \ddot q) = 1 \cdot 4.905^2 + 3 \cdot 4.905^2$, as the statement says.

Constrained robots. For a robot with closed loops or contacts that do not slide, the equation $M\ddot q + C\dot q + g = \tau + A^T\lambda$ with $A\ddot q = b$ (Lynch and Park, Section 8.7) is the KKT system of the Gauss program. [Forward dynamics](/forward-dynamics/) of a constrained robot can therefore be computed by one solve of $AM^{-1}A^T$, or by a quadratic program solver.

Unilateral contact. If a contact can separate, the constraint is an inequality $Ax \ge b$ on the normal accelerations of the active contacts. Minimizing $G$ over this set gives the frictionless contact problem at the acceleration level, and its KKT conditions are a linear complementarity problem; see [rigid contact complementarity](/rigid-contact-complementarity/). Some physics engines, MuJoCo among them, build their contact solvers on the Gauss objective.

A free system. With no applied forces, $a = 0$, and the principle reduces to Hertz's principle of least curvature: the system moves along the straightest path that the constraints allow.

## Tightness

Friction breaks the principle. A block rests on a slope of angle $30$ degrees with a friction coefficient $\mu = 1$. Coulomb friction holds it, because $\tan 30^\circ < 1$, so its true acceleration is $0$. The constraint that it stays on the slope allows any acceleration along the slope, and the Gauss program picks the frictionless one, $9.81\sin 30^\circ = 4.905$ m/s$^2$ down the slope. The friction force does work on allowed motions, so it is not ideal, and the proof fails at its first step.

Rank. If $A$ does not have full row rank (redundant constraints, as in a table with four legs), the acceleration is still unique, because $M$ is positive definite and the feasible set is an affine set. The total constraint force $Q_c = M(\ddot q - a)$ is also unique, but the multipliers $\lambda$ are not. So the share of each redundant constraint, such as the load on each leg, is not fixed by the rigid model. Any rule that picks one $\lambda$ is a modeling choice, not a law of physics.

Consistency. If $Ax = b$ has no solution, for example two constraints that ask for different accelerations of the same point, the program is infeasible and the model is wrong.

Positive definiteness. If $M$ is only positive semidefinite (a link with no mass and no inertia), $G$ is not strictly convex and the minimizer can fail to be unique.

## History

Gauss published the principle in 1829 in a four-page paper in Crelle's journal, for a system of particles, and presented it as a new general law of mechanics equivalent to d'Alembert's principle. Hertz later stated the principle of least curvature for systems without forces. The Gibbs-Appell equations, from the late nineteenth century, are an equivalent form. Udwadia and Kalaba (1992) wrote the minimizer in closed form with the Moore-Penrose inverse, which gives the constraint forces without first choosing which coordinates to eliminate. In robotics, the constrained equation $M\ddot q + h = \tau + A^T\lambda$ is standard (Lynch and Park, Section 8.7), and the Gauss form is used in contact simulation.

## References
