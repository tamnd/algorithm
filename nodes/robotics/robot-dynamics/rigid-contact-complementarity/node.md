---
tag: 4KBV2X
kind: model
slug: rigid-contact-complementarity
name: Rigid contact complementarity model
aliases:
- linear complementarity contact model
- LCP contact model
area: robotics/robot-dynamics
level: advanced
summary: Rigid bodies in contact with Coulomb friction, written as complementarity conditions; at each contact either the gap or the normal force is zero, and with a linearized cone the forces solve an LCP.
prereqs: [friction-cone, manipulator-equation, polyhedral-friction-cone]
see_also: [stewart-trinkle-time-stepping, painleve-paradox, gauss-principle-of-least-constraint, grasp-contact-models, quadratic-programming, kkt-conditions, np-complete, hybrid-automata]
sources:
  - paper: doi:10.1137/0142022
    title: Per Lötstedt, Mechanical systems of rigid bodies subject to unilateral constraints, SIAM Journal on Applied Mathematics 42(2), 1982
    locator: pages 281 to 296
  - paper: doi:10.1145/122718.122722
    title: "David Baraff, Coping with friction for non-penetrating rigid body simulation, Computer Graphics (SIGGRAPH '91 Proceedings) 25(4), 1991"
    locator: the sections on the consistency of contact forces with friction and its NP-completeness
  - paper: doi:10.1137/S0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 2000"
    locator: pages 3 to 39
  - paper: doi:10.1109/ISATP.2005.1511469
    title: "Jeffrey C. Trinkle, Stephen Berard and Jong-Shi Pang, A time-stepping scheme for quasistatic multibody systems, IEEE International Symposium on Assembly and Task Planning, 2005"
    locator: "pages 174 to 181; Section 1.1 on existence and uniqueness for the instantaneous model"
  - paper: doi:10.1007/BF00940344
    title: Sung-Jin Chung, NP-completeness of the linear complementarity problem, Journal of Optimization Theory and Applications 60(3), 1989
    locator: pages 393 to 399
  - paper: doi:10.1023/A:1008292328909
    title: "Mihai Anitescu and Florian A. Potra, Formulating dynamic multi-rigid-body contact problems with friction as solvable linear complementarity problems, Nonlinear Dynamics 14(3), 1997"
    locator: pages 231 to 247
  - book: isbn:9780898716863
    title: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, SIAM Classics in Applied Mathematics 60, 2009"
    locator: Chapter 1 (the problem and its sources) and Chapter 4 (pivoting methods)
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 11, Contact and Impact
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 37, Contact Modeling and Manipulation, by Imin Kao, Kevin M. Lynch and Joel W. Burdick, pages 931 to 954"
---

The rigid contact complementarity model describes rigid bodies that touch each other or the ground, with Coulomb friction, without any spring in the contact. Its central condition is a complementarity: at each contact, either the bodies are apart and the contact force is zero, or they touch and the force can be positive, but never both a gap and a force. With the friction cone replaced by a polyhedral cone, the unknown contact forces solve a linear complementarity problem (LCP) at each instant.

## The machine

**State.** The generalized coordinates $q$ and velocities $v$ of the bodies, with the mass matrix $M(q)$ and the other terms $h(q, v) = C v + g$ of the [manipulator equation](/manipulator-equation/). The input is the actuator torque $\tau$.

**Contacts.** Contact $i$ has a gap function $\phi_i(q)$, the signed distance along the contact normal, with $\phi_i \ge 0$ when the bodies do not overlap. The row $n_i^T = \partial \phi_i / \partial q$ maps $v$ to the normal velocity, and $D_i$ maps $v$ to the tangential velocity of the contact point. The normal points into the body that receives the force, so a positive normal force pushes the bodies apart.

**Forces.** The normal force $f_{n,i} \ge 0$ and the friction force $f_{t,i}$, with the generalized force $n_i f_{n,i} + D_i f_{t,i}$. The equation of motion is
$$M \dot v + h = \tau + \sum_i \big(n_i f_{n,i} + D_i f_{t,i}\big).$$

**Contact law.** Normal direction, in positions: $0 \le \phi_i \perp f_{n,i} \ge 0$, where $a \perp b$ means $a^T b = 0$. For a closed contact with $\phi_i = 0$ and $\dot\phi_i = 0$, the same condition holds one level down: $0 \le \ddot\phi_i \perp f_{n,i} \ge 0$. Friction, with the coefficient $\mu_i$ (Coulomb's law): $\| f_{t,i} \| \le \mu_i f_{n,i}$; if the contact slides, $f_{t,i} = -\mu_i f_{n,i}\, s_i / \| s_i \|$ for the slip velocity $s_i$; if it sticks, any force in the cone is allowed, and the tangential acceleration is zero.

**Standing assumptions.** Rigid bodies, a finite number of point contacts, Coulomb friction with a known $\mu$, no adhesion, and a rule for impacts (here, perfectly inelastic: the normal velocity becomes zero).

**The LCP.** Given a square matrix $A$ and a vector $b$, the linear complementarity problem asks for $z \ge 0$ with $w = A z + b \ge 0$ and $z_i w_i = 0$ for all $i$. For closed frictionless contacts, put $N = [n_1 \ldots n_c]$. Then $\ddot\phi = N^T \dot v + \dot N^T v$ and $\dot v = M^{-1}(\tau - h + N f_n)$ give
$$w = \ddot\phi = (N^T M^{-1} N)\, f_n + N^T M^{-1}(\tau - h) + \dot N^T v, \qquad z = f_n .$$
With friction and a [polyhedral cone](/polyhedral-friction-cone/) of $k$ edges per contact, the friction force is $D_i \beta_i$ with $\beta_i \ge 0$, and a slack $\lambda_i$ joins the unknowns. The LCP then has the same block form as one step of [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/), with forces and accelerations in place of impulses and velocities.

## What it counts

For a given state and input, the model gives the contact forces, the accelerations and the contact mode of each contact: separate, stick or slide.

**A block on a floor.** A block of 1 kg on a floor with $\mu = 0.5$ and $g = 9.81$ m/s$^2$ is pushed by a horizontal force $F$. The normal force is 9.81 N. If $|F| \le 4.905$ N, the block sticks and the friction force is $-F$. If $F = 7$ N, the block slides with the acceleration $7 - 4.905 = 2.095$ m/s$^2$. The model gives one answer for every $F$.

**Forces that are not unique.** A rigid bar of 1 kg rests without friction on three supports at $x = -1$, $0$ and $1$ m, with its center of mass at $x = 0$. The supports carry $(s,\ 9.81 - 2s,\ s)$ N for every $s$ in $[0, 4.905]$: all satisfy the model, and all give the same acceleration, zero. A rigid model cannot say how the weight is shared; a compliant model can.

**Forces that do not exist.** With friction, there are states with no solution and states with several, the [Painlevé paradox](/painleve-paradox/). For the sliding rod on that page with $\mu > 4/3$, some states have no consistent contact force and others have two.

## Relation to other models

- **Compliant contact.** A penalty model puts a stiff spring and a damper at each contact. It always gives unique forces, which depend on the chosen stiffness, and it needs small time steps because the springs are stiff.
- **Impulse form.** Writing the model in impulses over a time step gives [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/), which has a solution in the cases where the force form fails.
- **Gauss's principle.** For frictionless contacts, the LCP is the KKT system of a convex [quadratic program](/quadratic-programming/): minimize the [Gauss constraint](/gauss-principle-of-least-constraint/) $\tfrac12 (\dot v - \dot v_{\mathrm{free}})^T M (\dot v - \dot v_{\mathrm{free}})$ subject to $\ddot\phi \ge 0$; the normal forces are its multipliers.
- **Quasi-static grasp models.** [Grasp contact models](/grasp-contact-models/) use the same unilateral and friction conditions without the inertia terms.
- **Hybrid systems.** Each contact mode is a smooth system, and the switches between modes make the model a [hybrid automaton](/hybrid-automata/); the complementarity form avoids listing the modes.

## Known results in the model

- **Frictionless existence and uniqueness (theorem).** Without friction, $N^T M^{-1} N$ is positive semidefinite and the LCP is the KKT system of a convex quadratic program. When that program is feasible, for example when the contact normals $n_i$ are linearly independent, the LCP has a solution. The accelerations are unique, but the forces need not be (Lötstedt 1982).
- **With friction (theorem).** Solutions may not exist or may not be unique. Existence is guaranteed only when the friction coefficients are below a threshold that depends on the contact geometry (Trinkle, Berard and Pang 2005, Section 1.1).
- **Complexity (theorem).** Deciding whether a configuration with friction has consistent contact forces is NP-complete (Baraff 1991). The general LCP is [NP-complete](/np-complete/) too (Chung 1989), while LCPs with a positive semidefinite matrix can be solved in polynomial time as convex quadratic programs.
- **Contact modes.** With $c$ contacts in the plane, each contact can separate, stick, slide left or slide right, so a brute force search tries up to $4^c$ modes and solves a linear system for each. Pivoting methods such as Lemke's method, and the iterative method of projected Gauss-Seidel, avoid the full search in practice.
- **Impulsive form (theorem).** The velocity form of the time-stepping LCP always has a solution, and Lemke's method finds it (Anitescu and Potra 1997); see [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/).

## References
