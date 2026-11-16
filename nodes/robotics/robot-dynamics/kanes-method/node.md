---
tag: 3TCPJZ
kind: technique
slug: kanes-method
name: "Kane's method"
aliases:
- "Kane's equations"
area: robotics/robot-dynamics
level: advanced
summary: Derives equations of motion by projecting the forces and inertia forces of each body on its partial velocities, F_r + F_r* = 0. Ideal constraint forces drop out, with no multipliers.
prereqs: [newton-euler-equations, euler-lagrange-manipulator-dynamics]
see_also: [gauss-principle-of-least-constraint, nonholonomic-constraint, pfaffian-constraint, unicycle-model, recursive-newton-euler-algorithm, manipulator-equation, inverse-dynamics, euler-lagrange-equation]
sources:
  - book: isbn:9780070378469
    title: Thomas R. Kane and David A. Levinson, Dynamics, Theory and Applications, McGraw-Hill, 1985
    locator: the generalized speeds, partial velocities, generalized active and inertia forces, and the dynamical equations (general locator)
  - paper: doi:10.1177/027836498300200301
    title: Thomas R. Kane and David A. Levinson, The use of Kane's dynamical equations in robotics, International Journal of Robotics Research 2(3), 3-21, 1983
    locator: the whole paper (the method applied to the Stanford arm, and its operation count compared with other formulations)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: "Chapter 6, Section 6.1.2 (holonomic constraints and virtual work) and Section 6.1.3 (D'Alembert's principle)"
---

Kane's method derives the equations of motion of a system of rigid bodies by projecting forces onto special directions, the partial velocities. For each generalized speed $u_r$ it forms one scalar equation, $F_r + F_r^* = 0$, where $F_r$ collects the applied forces and $F_r^*$ the inertia forces $-m a$ and $-(\mathcal{I}\alpha + \omega \times \mathcal{I}\omega)$. Forces of ideal joints and of rolling without slipping do no work along the partial velocities, so they never appear. It sits between the [Newton-Euler equations](/newton-euler-equations/), which keep every joint force, and [Euler-Lagrange dynamics](/euler-lagrange-manipulator-dynamics/), which needs derivatives of an energy.

## In plain words

Each way that a system can move is a direction. If you push the system along one of these directions, some forces help, some resist, and some, such as the forces inside a hinge, do nothing at all. Kane's method writes one balance per direction: the forces that help, minus the resistance of the masses to speeding up, must add to zero. The hinge forces drop out by themselves. The method also lets you pick the directions freely, so a wheel that rolls without slipping simply gets fewer directions, and no extra unknown forces are needed.

## When it applies

- A system of rigid bodies (and particles) in an inertial frame, with $n$ generalized coordinates $q$.
- The velocities are linear in a set of $p$ generalized speeds $u \in \mathbb{R}^p$: $v_{ci} = \sum_r v^{ci}_r(q, t)\,u_r + v^{ci}_t(q, t)$ and $\omega_i = \sum_r \omega^{i}_r(q, t)\,u_r + \omega^i_t(q, t)$. For a holonomic system, $p = n$ and often $u = \dot q$. For a system with $n - p$ nonholonomic constraints, such as the rolling constraint of a wheel, one picks $p < n$ independent speeds.
- The constraints are ideal: the constraint forces do no work along any motion that the constraints allow. Frictionless joints and rolling without slipping are ideal. Sliding friction is not, and must be added as an applied force.
- It is useful for symbolic derivations of mechanisms, for vehicles with rolling constraints, and for spacecraft and multibody codes. Kane and Levinson (1983) used it to derive compact equations for a six-joint arm.

## The template

1. Choose the generalized coordinates $q$ and the generalized speeds $u$, and write the kinematic equations $\dot q = W(q)u$ that link them.
2. For each body $i$, write the velocity $v_{ci}$ of its center of mass and its angular velocity $\omega_i$ as linear functions of $u$.
3. Read off the partial velocities $v^{ci}_r = \partial v_{ci}/\partial u_r$ and the partial angular velocities $\omega^i_r = \partial\omega_i/\partial u_r$.
4. Differentiate to get the accelerations $a_{ci}$ and the angular accelerations $\alpha_i$, both in an inertial frame.
5. Form the generalized active forces. If body $i$ carries the resultant force $R_i$ through its center of mass and the couple $T_i$, then
$$F_r = \sum_i \big(v^{ci}_r \cdot R_i + \omega^i_r \cdot T_i\big).$$
A motor torque $\tau$ about the axis $z$ between body $j$ and body $k$ acts with $+\tau z$ on $k$ and $-\tau z$ on $j$, and contributes $\tau\,(\omega^k_r - \omega^j_r)\cdot z$.
6. Form the generalized inertia forces
$$F_r^* = \sum_i \Big(v^{ci}_r \cdot (-m_ia_{ci}) + \omega^i_r \cdot \big(-\mathcal{I}_i\alpha_i - \omega_i \times \mathcal{I}_i\omega_i\big)\Big).$$
7. Write Kane's equations $F_r + F_r^* = 0$ for $r = 1, \dots, p$. Together with $\dot q = W(q)u$ they are the equations of motion.

Why ideal constraint forces drop out. A constraint force $R^c$ that does no work on any allowed motion satisfies $\sum_i (v_{ci} \cdot R^c_i + \omega_i \cdot T^c_i) = 0$ for every $u$. Since the velocities are linear in $u$, the coefficient of each $u_r$ is zero, and that coefficient is exactly the contribution of the constraint forces to $F_r$. Kane's equations are then the [Newton-Euler equations](/newton-euler-equations/) of all bodies, projected on the partial velocities, which is d'Alembert's principle in the coordinates $u$.

Link to the manipulator equation. For a fixed-base arm with $u = \dot q$, the partial velocities are the columns of the Jacobians, $v^{ci}_r = J_{vi}e_r$ and $\omega^i_r = J_{\omega i}e_r$. Then $F^* = -\sum_i\big(J_{vi}^Tm_ia_{ci} + J_{\omega i}^T(\mathcal{I}_i\alpha_i + \omega_i \times \mathcal{I}_i\omega_i)\big) = -(M\ddot q + C\dot q)$ and $F = \tau - g(q)$, so Kane's equations are the [manipulator equation](/manipulator-equation/).

## Classic examples

The planar 2R arm. Take $L_1 = L_2 = 1$ m, point masses of 1 kg at the link ends, $u = \dot q$, a vertical plane with heights measured upward, and $q_1$ from the horizontal. With $s_1 = \sin q_1$, $c_1 = \cos q_1$, $s_{12} = \sin(q_1 + q_2)$ and $c_{12} = \cos(q_1 + q_2)$, the partial velocities are

$$v^{(1)}_1 = (-s_1, c_1),\quad v^{(1)}_2 = (0, 0),\quad v^{(2)}_1 = (-s_1 - s_{12},\ c_1 + c_{12}),\quad v^{(2)}_2 = (-s_{12}, c_{12}).$$

Link 1 turns at $u_1$ and link 2 at $u_1 + u_2$, so motor 1 contributes $\tau_1$ to $F_1$, and motor 2 contributes $\tau_2(1 - 1) = 0$ to $F_1$ and $\tau_2$ to $F_2$. The weights $(0, -9.81)$ N give $F_1 = \tau_1 - 9.81(2c_1 + c_{12})$ and $F_2 = \tau_2 - 9.81c_{12}$.

Now take $q = (0, \pi/2)$, $u = (1, 1)$ rad/s and $\dot u = 0$. The masses are at $(1, 0)$ and $(1, 1)$. Their accelerations are centripetal: $a_1 = (-1, 0)$ m/s$^2$ and $a_2 = a_1 - (u_1 + u_2)^2(c_{12}, s_{12}) = (-1, -4)$ m/s$^2$. The partial velocities there are $v^{(1)}_1 = (0, 1)$, $v^{(2)}_1 = (-1, 1)$ and $v^{(2)}_2 = (-1, 0)$. So

$$F_1^* = -\big((-1, 0)\cdot(0, 1) + (-1, -4)\cdot(-1, 1)\big) = 3,\qquad F_2^* = -(-1, -4)\cdot(-1, 0) = -1.$$

Without gravity, $F_r + F_r^* = 0$ gives $\tau = (-3, 1)$ N m, the same torques as the Euler-Lagrange equations. No joint reaction force was computed.

A knife edge on a plane (the [unicycle model](/unicycle-model/) with mass). A body of mass $m$ and inertia $I$ about its center of mass moves on a horizontal plane with pose $(x, y, \theta)$. A knife edge at the center of mass forbids sideways motion, $-\dot x\sin\theta + \dot y\cos\theta = 0$, which is a [nonholonomic constraint](/nonholonomic-constraint/). Choose $p = 2$ speeds: $u_1$, the forward speed, and $u_2 = \dot\theta$. Then $v_c = u_1(\cos\theta, \sin\theta)$ and $\omega = u_2$, so $v_1 = (\cos\theta, \sin\theta)$, $v_2 = 0$, $\omega_1 = 0$ and $\omega_2 = 1$. The acceleration is $a_c = \dot u_1(\cos\theta, \sin\theta) + u_1u_2(-\sin\theta, \cos\theta)$, and the second term is orthogonal to $v_1$. With a forward force $f$ and a turning moment $T$, Kane's equations are $m\dot u_1 = f$ and $I\dot u_2 = T$, with $\dot x = u_1\cos\theta$, $\dot y = u_1\sin\theta$, $\dot\theta = u_2$. The sideways force of the knife edge never enters. A Lagrangian treatment of the same system needs three equations and one multiplier.

A pendulum. A point mass $m$ on a massless rod of length $L$, with $u = \dot q$ and $q$ from the horizontal: $v_1 = L(-\sin q, \cos q)$, $F_1 = \tau - mgL\cos q$ and $F_1^* = -mL^2\dot u$, so $\tau = mL^2\ddot q + mgL\cos q$.

## Variations

- Choice of speeds. Body-frame components of the angular velocity, or the forward speed of a vehicle, often give shorter expressions than $u = \dot q$. The kinematic equations $\dot q = W(q)u$ then carry the extra work.
- Computer algebra. Packages for symbolic multibody dynamics implement the method, for example the mechanics module of SymPy, which has a class for Kane's method.
- Related principles. The Gibbs-Appell equations and Jourdain's principle lead to the same equations by other routes. The [Gauss principle of least constraint](/gauss-principle-of-least-constraint/) states the same physics as a minimum over accelerations.
- Recursive forms. Organized link by link along a chain, the projections of Kane's method become a recursive algorithm much like the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/).

## Pitfalls

- Partial velocities are derivatives with respect to the speeds $u$, not the coordinates $q$. If $u \ne \dot q$, do not differentiate with respect to $\dot q$.
- Accelerations must be taken in an inertial frame. When $v_c$ is written in a moving frame, add the transport term $\omega \times v$.
- Nonideal constraints. Joint friction and sliding contact do work, so their forces must be added to $F_r$ as applied forces. Leaving them out gives wrong equations without any warning.
- Internal forces that do work, such as a spring between two links, must appear in $F_r$; only workless constraint forces drop out.
- The constraint forces are not computed. If you need the joint reaction forces, for example to size a bearing, add a speed that violates the constraint (Kane and Levinson call such speeds auxiliary), or use the Newton-Euler equations.

## Exercises

1. Derive the equation of the pendulum with a rod of mass $m$ and length $L$ (center of mass at $L/2$, $I = mL^2/12$ about it). Answer: $\tau = \tfrac13mL^2\ddot q + \tfrac12mgL\cos q$.
2. For the 2R arm at $q = (0, 0)$, $u = (1, 0)$ rad/s and $\dot u = 0$, without gravity, show that $F^* = 0$, so no torque is needed. Explain the result with the direction of the centripetal accelerations.
3. Show that for $u = \dot q$, $F_r^* = -\big(\tfrac{d}{dt}\tfrac{\partial K}{\partial\dot q_r} - \tfrac{\partial K}{\partial q_r}\big)$, so Kane's equations and the Euler-Lagrange equations agree.
4. Add a viscous force $-b\,u_1$ along the heading of the knife edge and solve for $u_1(t)$ with $f = 0$. Answer: $u_1(t) = u_1(0)e^{-bt/m}$.

## References
