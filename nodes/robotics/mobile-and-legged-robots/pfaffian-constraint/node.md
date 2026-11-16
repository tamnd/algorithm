---
tag: XZQQBC
kind: definition
slug: pfaffian-constraint
name: Pfaffian constraint
aliases:
- Pfaffian form
area: robotics/mobile-and-legged-robots
level: core
summary: "A velocity constraint A(q) q' = 0, linear in the velocities with coefficients that depend on the configuration. It is holonomic if it integrates to a constraint on q, else nonholonomic."
prereqs: [configuration-space]
see_also: [nonholonomic-constraint, lagrange-multiplier, unicycle-model, kinematic-bicycle-model, lie-bracket, control-affine-system, four-bar-linkage, euler-lagrange-manipulator-dynamics]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 2.4 (configuration and velocity constraints, Pfaffian constraints, holonomic and nonholonomic), Chapter 8 (dynamics with constraints) and Section 13.3.1 (the constraints of wheeled robots)"
  - book: isbn:9780849379819
    title: "Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994"
    locator: "Chapter 7 (Pfaffian constraints, their integrability and Frobenius' theorem)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 13.1 (velocity constraints in implicit form and the parametric form q' = G(q) u)"
---

A Pfaffian constraint is a set of $k$ equations $A(q)\,\dot q = 0$ on the velocity $\dot q$ of a system with configuration $q$, where the $k \times n$ matrix $A(q)$ depends on the configuration only. The constraint is linear in the velocities. Each row is a differential form $a_1(q)\,dq_1 + \dots + a_n(q)\,dq_n$, a Pfaffian form, named after Johann Friedrich Pfaff. Two sources give most constraints of this form in robotics. A constraint on positions $h(q) = 0$, such as the loop of a closed chain, gives one after differentiation in time. A contact that rolls without slipping, such as a wheel on the ground, gives one directly. A Pfaffian constraint is **holonomic** if it integrates back to a constraint on positions, and **nonholonomic** otherwise; the [nonholonomic constraint](/nonholonomic-constraint/) page is about that property and its test, and this page is about the form.

## Definition

**Setting.** The configuration space has dimension $n$ and local coordinates $q$. A Pfaffian constraint is

$$A(q)\,\dot q = 0, \qquad A(q) \in \mathbb{R}^{k \times n},$$

with $A$ smooth and of rank $k$ at every $q$ under study. The $j$-th row defines the one-form $\omega_j = \sum_i a_{ji}(q)\, dq_i$, and the constraint says $\omega_j(\dot q) = 0$ for each $j$.

**Allowed velocities.** At each $q$ the allowed velocities are the null space $\ker A(q)$, of dimension $m = n - k$. Choose smooth vector fields $g_1, \dots, g_m$ that span it, the columns of a matrix $G(q)$ with $A(q) G(q) = 0$. Then the constrained motions are exactly the solutions of

$$\dot q = G(q)\, u, \qquad u \in \mathbb{R}^m,$$

a driftless [control-affine system](/control-affine-system/). The constraint is the implicit form and $G$ the parametric form of the same set of motions. For a robot, $u$ is often a set of wheel or steering speeds.

**Holonomic and nonholonomic.** The constraint is holonomic if there are $k$ functions $h(q)$ with independent differentials such that the rows of $A(q)$ and of $\partial h / \partial q$ span the same subspace, so that $h(q(t))$ stays constant on every allowed motion. It is nonholonomic otherwise. Holonomic does not mean that $A$ itself is a gradient: a row can need an integrating factor $\mu(q) \ne 0$ such that $\mu\,\omega_j$ is the differential of a function.

**Tests (theorems).** For one constraint, $k = 1$, the form $\omega$ is integrable if and only if $\omega \wedge d\omega = 0$. In three variables, with $\omega = a \cdot dq$, this reads $a \cdot (\nabla \times a) = 0$. If moreover $\nabla \times a = 0$ on a simply connected set, $\omega$ is exact and $h$ is its potential, with no integrating factor. For any $k$, the Frobenius theorem gives the test in terms of the fields $g_i$: the constraint is holonomic if and only if every [Lie bracket](/lie-bracket/) $[g_i, g_j]$ stays in $\ker A$. The [nonholonomic constraint](/nonholonomic-constraint/) page states the test and its consequences.

**Forces of the constraint.** In the dynamics, the constraint acts through forces in the row space of $A$:

$$M(q)\,\ddot q + c(q, \dot q) = \tau + A(q)^T \lambda, \qquad A(q)\,\dot q = 0,$$

with $\lambda \in \mathbb{R}^k$ a vector of [Lagrange multipliers](/lagrange-multiplier/). These forces do no work on allowed motions, because $\dot q^T A^T \lambda = 0$. This is the Lagrange-d'Alembert principle; it holds for holonomic and nonholonomic Pfaffian constraints alike. Differentiate the constraint once, $A \ddot q + \dot A \dot q = 0$, to solve for $\lambda$.

**Close forms that are not Pfaffian.** A constraint $A(q)\,\dot q + b(q, t) = 0$, with a moving support, is affine in the velocities. A constraint such as $\dot x^2 + \dot y^2 \le v_{\max}^2$ is a bound, not an equality. A constraint that is nonlinear in $\dot q$ is rare in robotics.

## Examples and non-examples

**A pendulum (holonomic, from a position constraint).** A point at distance $l$ from a pivot satisfies $h(x, y) = x^2 + y^2 - l^2 = 0$. Differentiation gives $x\dot x + y\dot y = 0$, so $A = [x, y]$. At $(x, y) = (0.6, -0.8)$ with $l = 1$, the allowed velocities are the multiples of $(0.8, 0.6)$, tangent to the circle.

**A wheel on a line (holonomic, from rolling).** A wheel of radius $r$ that rolls on a straight line, with center $x$ and angle $\varphi$, obeys $\dot x - r\dot\varphi = 0$. This is the differential of $x - r\varphi$, so the constraint integrates to $x - r\varphi = c$.

**An integrating factor (holonomic, not exact).** In the variables $(x, y, z)$, the constraint $y\dot x - x\dot y = 0$ has $a = (y, -x, 0)$ and $\nabla \times a = (0, 0, -2)$, which is not zero, so the form is not exact. But $a \cdot (\nabla \times a) = 0$, so it is integrable. With $\mu = -1/(x^2 + y^2)$, $\mu\,\omega = d\phi$ where $\phi$ is the polar angle of $(x, y)$. Each motion keeps $\phi$ constant: the point moves along a ray from the $z$ axis, and $z$ is free.

**The rolling unicycle (nonholonomic).** For the [unicycle](/unicycle-model/) with $q = (x, y, \theta)$, no sideways slip is $\dot x\sin\theta - \dot y\cos\theta = 0$. Here $a = (\sin\theta, -\cos\theta, 0)$ and $\nabla \times a = (-\sin\theta, \cos\theta, 0)$, so $a \cdot (\nabla \times a) = -1$ at every $q$. No integrating factor exists, and the constraint is nonholonomic. The parametric form is $\dot q = (\cos\theta, \sin\theta, 0)\, v + (0, 0, 1)\, \omega$.

**The constraint force of the unicycle.** Take a body of mass $m$ with a forward force $F$ and the constraint above. The equations are $m\ddot x = F\cos\theta + \lambda\sin\theta$ and $m\ddot y = F\sin\theta - \lambda\cos\theta$. Differentiating the constraint gives $\ddot x\sin\theta - \ddot y\cos\theta = -v\omega$ with $v$ the forward speed, so $\lambda = -m v \omega$. This is the sideways force of the ground on the wheel, $m v^2 / R$ toward the center of the turn: for $m = 20$ kg, $v = 1$ m/s and $\omega = 0.5$ rad/s, it is 10 N. The kinematic model holds only while friction can supply this force.

**A car (two constraints).** The [kinematic bicycle model](/kinematic-bicycle-model/) with the steering angle in the state has one no-slip constraint for the rear wheel and one for the front wheel. Both are Pfaffian, and both are nonholonomic.

**A closed chain.** The loop closure of a [four-bar linkage](/four-bar-linkage/) is a set of equations on the joint angles. Its time derivative is a Pfaffian constraint, holonomic by construction.

## Related definitions

- [Nonholonomic constraint](/nonholonomic-constraint/): the Pfaffian constraints that do not integrate, with the Frobenius test.
- [Configuration space](/configuration-space/): a holonomic constraint defines a smaller configuration space; a nonholonomic one does not.
- [Control-affine system](/control-affine-system/): the parametric form $\dot q = G(q) u$ is a driftless one.
- [Lagrange multiplier](/lagrange-multiplier/): the constraint forces in the dynamics.
- [Lie bracket](/lie-bracket/): the operation in the integrability test for several constraints.
- [Euler-Lagrange manipulator dynamics](/euler-lagrange-manipulator-dynamics/): the unconstrained equations that the multipliers extend.

## References
