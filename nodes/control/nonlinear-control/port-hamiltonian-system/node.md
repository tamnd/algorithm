---
tag: XPB19M
kind: model
slug: port-hamiltonian-system
name: Port-Hamiltonian system
aliases:
- port-Hamiltonian model
area: control/nonlinear-control
level: advanced
summary: "A model x' = (J - R) grad H + g u, y = g^T grad H, built from an energy H, a skew interconnection J, a damping R >= 0 and ports. It is passive with storage H."
prereqs: [passivity, hamiltonian-systems, control-affine-system]
see_also: [ida-pbc, passivity-based-control, dissipativity, passivity-theorem, kalman-yakubovich-popov-lemma, euler-lagrange-equation, symplectic-integrators, lasalle-invariance-principle]
sources:
  - paper: "B. M. Maschke and A. J. van der Schaft, Port-controlled Hamiltonian systems: modelling origins and system-theoretic properties, Proceedings of the 2nd IFAC Symposium on Nonlinear Control Systems (NOLCOS), Bordeaux, 1992"
    title: "Port-controlled Hamiltonian systems: modelling origins and system-theoretic properties"
    locator: the definition of port-controlled Hamiltonian systems and their passivity
  - paper: doi:10.1561/2600000002
    title: "Arjan van der Schaft and Dimitri Jeltsema, Port-Hamiltonian Systems Theory: An Introductory Overview, Foundations and Trends in Systems and Control 1(2-3), 173-378, 2014"
    locator: the input-state-output port-Hamiltonian systems with dissipation, the power balance, interconnection and Casimirs
  - paper: doi:10.1016/S0005-1098(01)00278-3
    title: "Romeo Ortega, Arjan van der Schaft, Bernhard Maschke and Gerardo Escobar, Interconnection and damping assignment passivity-based control of port-controlled Hamiltonian systems, Automatica 38(4), 585-596, 2002"
    locator: Section 2 (the model (1), the energy balance (3) and (4), and the passivity of the map from u to y)
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Chapter 6 (passivity) and Section 4.2 (the invariance principle)
---

A port-Hamiltonian system is a model of a physical system written in terms of its energy. A function $H(x)$ gives the stored energy, a skew-symmetric matrix $J(x)$ says how energy moves between the parts without loss, a symmetric positive semidefinite matrix $R(x)$ says where energy is lost, and a matrix $g(x)$ says where energy enters through the input $u$. The output $y = g^T \nabla H$ is chosen so that $y^T u$ is the power that flows in. Masses and springs, electric circuits, motors and many coupled systems fit this form. The rate of change of the energy is the supplied power minus the dissipated power, so the model is passive with the energy as storage function (see [passivity](/passivity/)). Classical [Hamiltonian systems](/hamiltonian-systems/) are the special case with no damping and no ports. Control methods such as [passivity-based control](/passivity-based-control/) and [IDA-PBC](/ida-pbc/) use the form because they can change the energy and the damping and keep the structure.

## The machine

**Equations.** The state is $x \in \mathbb{R}^n$, the input is $u \in \mathbb{R}^m$, the output is $y \in \mathbb{R}^m$, and time is continuous, $t \ge 0$:

$$\dot x = \bigl(J(x) - R(x)\bigr) \nabla H(x) + g(x)\, u, \qquad y = g(x)^T \nabla H(x).$$

**Standing assumptions.**

- $H : \mathbb{R}^n \to \mathbb{R}$ is the Hamiltonian, the total stored energy. It is $C^1$ with a locally Lipschitz gradient, and bounded below. $\nabla H$ is the gradient as a column vector.
- $J(x) = -J(x)^T$ for every $x$. This is the interconnection matrix.
- $R(x) = R(x)^T \ge 0$ for every $x$. This is the dissipation matrix.
- $g(x) \in \mathbb{R}^{n \times m}$ is the input matrix. $J$, $R$ and $g$ are locally Lipschitz.

Under these assumptions the right side is locally Lipschitz in $x$ and continuous in $t$ for a continuous input, so solutions exist and are unique while they stay bounded (see the [Lipschitz condition](/lipschitz-condition/) and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/)). The model is a [control-affine system](/control-affine-system/) $\dot x = f(x) + g(x) u$ with the special drift $f = (J - R) \nabla H$ and a matching output. The input $u$ and the output $y$ are conjugate variables: force and velocity, voltage and current, torque and angular velocity. Their product is a power.

**Example: mass, spring and damper.** Let $q$ be the position and $p = m \dot q$ the momentum, so $x = (q, p)$. The energy is $H = \frac12 k q^2 + \frac{1}{2m} p^2$, and

$$J = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}, \qquad R = \begin{bmatrix} 0 & 0 \\ 0 & b \end{bmatrix}, \qquad g = \begin{bmatrix} 0 \\ 1 \end{bmatrix}.$$

With $\nabla H = (k q,\ p / m)$ the equations are $\dot q = p / m$ and $\dot p = -k q - b p / m + u$, where $u$ is an external force. The output $y = p / m$ is the velocity, and $y u$ is the power of the force.

**Example: fully actuated mechanical systems.** With configuration $q \in \mathbb{R}^k$, momentum $p = M(q) \dot q$, mass matrix $M(q) > 0$ and potential energy $V(q)$, take $H = \frac12 p^T M(q)^{-1} p + V(q)$,

$$J = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}, \qquad R = \begin{bmatrix} 0 & 0 \\ 0 & D(q) \end{bmatrix}, \qquad g = \begin{bmatrix} 0 \\ I \end{bmatrix},$$

with friction $D(q) \ge 0$. The output is the velocity $\dot q$. This is the same system as the Euler-Lagrange model of the [Euler-Lagrange equation](/euler-lagrange-equation/), written with momenta instead of velocities.

**Example: magnetic levitation.** A ball of mass $m$ hangs under an electromagnet. The state is the flux linkage $\lambda$, the position $\theta$ of the ball and its momentum $p$. With $H = \frac{(1 - \theta) \lambda^2}{2k} + \frac{p^2}{2m} + m g_0 \theta$, the coil current is $\partial H / \partial \lambda$, the magnetic force is $-\partial H / \partial \theta$, and the coil resistance is the only dissipation. The [IDA-PBC](/ida-pbc/) page uses this model. Here the electric and the mechanical energy are in one function, and the interconnection matrix couples them.

## What it counts

The model counts energy. Along every solution,

$$\frac{d}{dt} H(x(t)) = \nabla H^T (J - R) \nabla H + \nabla H^T g\, u = -\nabla H^T R\, \nabla H + y^T u,$$

because $\nabla H^T J \nabla H = 0$ for a skew-symmetric $J$. This is the power balance: the stored energy changes by the supplied power $y^T u$ minus the dissipated power $\nabla H^T R \nabla H \ge 0$. Integrated from $0$ to $t$,

$$H(x(t)) - H(x(0)) = \int_0^t y^T u\, ds - \int_0^t \nabla H^T R\, \nabla H\, ds \le \int_0^t y^T u\, ds.$$

So the system is passive with storage function $H$ (shifted to be nonnegative), in the sense of [dissipativity](/dissipativity/) with the supply rate $y^T u$. The model predicts the energy budget: how much energy a controller must supply, and how much the friction and the resistors take out.

For the mass, spring and damper with $m = 1$, $k = 2$, $b = 0.5$ and $x(0) = (1, 0)$, the energy starts at $H = 1$. With $u = 0$, a classical RK4 simulation with step $0.01$ gives $H = 0.68257$ at $t = 1$ and $H = 0.09856$ at $t = 5$. With the feedback $u = -y$, which adds the damping $1$ to $b$, it gives $H = 0.46920$ at $t = 1$ and $H = 0.00040$ at $t = 5$.

## Relation to other models

- **Hamiltonian systems.** With $R = 0$, $g = 0$ and the constant canonical $J = \begin{bmatrix} 0 & I \\ -I & 0 \end{bmatrix}$, the model is a classical [Hamiltonian system](/hamiltonian-systems/), and $H$ is conserved. The port-Hamiltonian form allows a state dependent and singular $J$, adds dissipation, and opens ports to the outside.
- **Euler-Lagrange systems.** For mechanical systems, the Legendre transform $p = \partial L / \partial \dot q$ maps the Euler-Lagrange model to the port-Hamiltonian model above. The port-Hamiltonian form is wider: it also covers electrical and electromechanical systems in which the energy is not kinetic plus potential (Ortega et al. 2002, Section 1).
- **Control-affine systems.** Every port-Hamiltonian system is a [control-affine system](/control-affine-system/). The converse needs a storage function $H$ and a factorization of the drift as $(J - R)\nabla H$, which is a strong structural property.
- **Passive linear systems.** Take $H = \frac12 x^T Q x$ with $Q > 0$. Then $\dot x = (J - R) Q x + g u$ and $y = g^T Q x$ is linear. Conversely, let $\dot x = A x + B u$, $y = C x$ be passive with a storage $\frac12 x^T P x$, $P > 0$, which by the [Kalman-Yakubovich-Popov lemma](/kalman-yakubovich-popov-lemma/) means $A^T P + P A \le 0$ and $P B = C^T$. Put $J = \frac12 (A P^{-1} - P^{-1} A^T)$ and $R = -\frac12 P^{-1} (A^T P + P A) P^{-1}$. Then $J$ is skew, $R \ge 0$, $A = (J - R) P$ and $C = B^T P$. So every linear system with a positive definite quadratic storage function for the supply $y^T u$ is a port-Hamiltonian system with $H = \frac12 x^T P x$.
- **Dissipative systems.** Port-Hamiltonian systems are dissipative with the supply rate $y^T u$. A general dissipative system has no such geometric structure, and its storage function need not be the physical energy.

## Known results in the model

- **Passivity and the power balance.** Shown above. It holds for every $H$, every skew $J$ and every $R \ge 0$, so it does not depend on the numerical values of the parameters. This is the main reason the model is used for robust control design.
- **Lyapunov stability of strict minima.** If $x^\star$ is a strict local minimum of $H$ and $u = 0$, then $V = H - H(x^\star)$ is a [Lyapunov function](/lyapunov-function/) with $\dot V = -\nabla H^T R \nabla H \le 0$, so $x^\star$ is a Lyapunov stable equilibrium (Khalil 2002, Chapter 4). Asymptotic stability needs more. By the [LaSalle invariance principle](/lasalle-invariance-principle/) on a compact sublevel set of $H$ around $x^\star$, it holds if no solution other than $x^\star$ stays in the set where $\nabla H^T R \nabla H = 0$.
- **Damping injection.** The feedback $u = -K_v y$ with $K_v = K_v^T > 0$ gives the closed loop $\dot x = (J - R - g K_v g^T) \nabla H$, which is port-Hamiltonian again with the larger dissipation $R + g K_v g^T$. It cannot move the minimum of $H$. To stabilize another point the energy must be changed, which is what [passivity-based control](/passivity-based-control/) and [IDA-PBC](/ida-pbc/) do.
- **Power-preserving interconnection.** Connect two port-Hamiltonian systems by $u_1 = -y_2 + e_1$ and $u_2 = y_1 + e_2$. The result is port-Hamiltonian with energy $H_1(x_1) + H_2(x_2)$, dissipation $\operatorname{diag}(R_1, R_2)$, inputs $(e_1, e_2)$ and the interconnection matrix $\begin{bmatrix} J_1 & -g_1 g_2^T \\ g_2 g_1^T & J_2 \end{bmatrix}$, which is skew-symmetric. This is the energy view of the [passivity theorem](/passivity-theorem/): the feedback connection of two passive systems is passive.
- **Casimir functions and the dissipation obstacle.** A function $C(x)$ with $\nabla C^T (J - R) = 0$ does not change along the system with $u = 0$, for every $H$. Such a function is a Casimir. Multiply the condition on the right by $\nabla C$: since $\nabla C^T J \nabla C = 0$, this gives $\nabla C^T R \nabla C = 0$, so $R \nabla C = 0$ (because $R \ge 0$) and then $J^T \nabla C = 0$ as well. So Casimirs cannot depend on the states where dissipation acts. This limits the energy-Casimir method of control, and it is one reason why IDA-PBC changes $J$ and $R$ instead of looking for Casimirs.
- **Structure-preserving simulation.** For $R = 0$ and $u = 0$, $H$ is constant along exact solutions, but a general method such as RK4 lets it drift slowly. [Symplectic integrators](/symplectic-integrators/) keep a modified energy close to $H$ over long times for canonical $J$. With dissipation, discrete gradient methods give a discrete power balance. These are properties of the numerical method, not of the model.

## References
