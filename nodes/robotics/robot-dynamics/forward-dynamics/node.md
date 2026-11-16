---
tag: 9JRMMF
kind: problem
slug: forward-dynamics
name: Forward dynamics
aliases:
- direct dynamics
area: robotics/robot-dynamics
level: core
summary: "Given the state q, q' of a robot and its joint torques tau, find the joint accelerations q'' = M(q)^-1 (tau - C q' - g). Solved in O(n) by the articulated-body algorithm."
prereqs: [manipulator-equation, ode-initial-value-problem]
see_also: [articulated-body-algorithm, composite-rigid-body-algorithm, inverse-dynamics, recursive-newton-euler-algorithm, cholesky-decomposition, runge-kutta-methods, rigid-contact-complementarity, rigid-body-dynamics-derivatives]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8, Section 8.5 (forward dynamics of open chains)
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 6 (the composite-rigid-body algorithm and the factorization of the joint-space inertia matrix), Chapter 7 (forward dynamics, the articulated-body algorithm) and Chapter 10 (accuracy and efficiency)
  - paper: doi:10.1115/1.3139699
    title: M. W. Walker and D. E. Orin, Efficient dynamic computer simulation of robotic mechanisms, Journal of Dynamic Systems, Measurement, and Control 104(3), 205-211, 1982
    locator: the whole paper (forward dynamics by repeated inverse dynamics calls, and the composite-rigid-body method)
  - paper: doi:10.1177/027836498300200102
    title: Roy Featherstone, The calculation of robot dynamics using articulated-body inertias, International Journal of Robotics Research 2(1), 13-30, 1983
    locator: the whole paper (the articulated-body algorithm, linear in the number of joints)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7 (direct dynamics and inverse dynamics)
---

Forward dynamics is the problem of finding how a robot accelerates: given its joint positions $q$, joint velocities $\dot q$ and joint torques $\tau$, find the joint accelerations $\ddot q$. For a robot without contact the answer is unique, $\ddot q = M(q)^{-1}\big(\tau - C(q, \dot q)\dot q - g(q)\big)$. Simulation of a robot is forward dynamics inside an ODE integrator. This page states the problem and its bounds; the [articulated-body algorithm](/articulated-body-algorithm/) page gives the $O(n)$ method in detail, and [inverse dynamics](/inverse-dynamics/) is the opposite problem.

## In plain words

You know where every joint of a robot is, how fast it moves, and which torque each motor gives. What happens next? Forward dynamics answers with the acceleration of every joint. One motor torque moves the whole arm, because the links push on each other, so the answer is a coupled system of equations, one per joint. A simulator asks this question many times per second and steps the state forward with the answer.

## Definition

Input:
- A robot model: $n$ joints, each revolute or prismatic, joined into a serial chain or a tree with a fixed base; the joint axes and the link frames; and for each link its mass, center of mass and rotational inertia.
- The gravity vector, $(0, 0, -9.81)$ m/s$^2$ in the space frame $\{s\}$.
- The state $(q, \dot q) \in \mathbb{R}^n \times \mathbb{R}^n$, the joint torques $\tau \in \mathbb{R}^n$, and optionally external wrenches $F_{\text{ext}}$ on given links with their Jacobians $J(q)$.

Output: the vector $\ddot q \in \mathbb{R}^n$ that satisfies the [manipulator equation](/manipulator-equation/)

$$M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J(q)^T F_{\text{ext}}.$$

Because the [joint-space inertia matrix](/joint-space-inertia-matrix/) $M(q)$ is symmetric positive definite, the output exists and is unique:

$$\ddot q = M(q)^{-1}\big(\tau + J(q)^T F_{\text{ext}} - C(q, \dot q)\dot q - g(q)\big).$$

The simulation version adds an initial state $(q(0), \dot q(0))$ and a torque history $\tau(t)$ on $[0, T]$, and asks for $q(t)$. It is the [ODE initial value problem](/ode-initial-value-problem/) $\dot x = f(x, \tau(t))$ with $x = (q, \dot q)$, and each evaluation of $f$ is one forward dynamics problem.

## Variants

- Floating base. A legged robot, a humanoid or a space robot has six extra coordinates for its base, which no motor drives directly. The problem has the same form with $n + 6$ unknowns; see [floating-base dynamics](/floating-base-dynamics/).
- Closed loops. Parallel robots and four-bar linkages add loop-closure constraints $A(q)\ddot q = b(q, \dot q)$ with unknown multipliers $\lambda$. The problem becomes the linear system $\begin{bmatrix} M & A^T \\ A & 0\end{bmatrix}\begin{bmatrix}\ddot q \\ -\lambda\end{bmatrix} = \begin{bmatrix}\tau - C\dot q - g \\ b\end{bmatrix}$. The [Gauss principle of least constraint](/gauss-principle-of-least-constraint/) gives the same solution as the minimizer of a quadratic program.
- Contact with friction. Unilateral contacts and Coulomb friction turn the problem into a complementarity problem, which may have no solution or several (the [Painleve paradox](/painleve-paradox/)). Simulators usually solve it at the velocity level with a time step; see [rigid contact complementarity](/rigid-contact-complementarity/) and [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/).
- Hybrid dynamics. Some joints have a given acceleration and the rest a given torque. The unknowns are the accelerations of the second set and the torques of the first.
- Derivatives. Optimal control and estimation need $\partial\ddot q/\partial q$, $\partial\ddot q/\partial\dot q$ and $\partial\ddot q/\partial\tau = M^{-1}$; see [rigid-body dynamics derivatives](/rigid-body-dynamics-derivatives/).

## Examples

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane, with $q_1$ measured from the horizontal. Its terms are $M = [[3 + 2c_2, 1 + c_2], [1 + c_2, 1]]$, $C\dot q = (-s_2(2\dot q_1\dot q_2 + \dot q_2^2),\ s_2\dot q_1^2)$ and $g = 9.81(2c_1 + c_{12},\ c_{12})$, where $c_2 = \cos q_2$, $s_2 = \sin q_2$, $c_1 = \cos q_1$ and $c_{12} = \cos(q_1 + q_2)$.

Free fall. At $q = (0, 0)$, at rest, with $\tau = 0$: $M = [[5, 2], [2, 1]]$, $M^{-1} = [[1, -2], [-2, 5]]$ and $g = (29.43, 9.81)$ N m. So $\ddot q = -M^{-1}g = (-29.43 + 19.62,\ 58.86 - 49.05) = (-9.81, 9.81)$ rad/s$^2$. Both masses fall with $9.81$ m/s$^2$ at the first instant, and link 2 keeps its absolute angle because $\ddot q_1 + \ddot q_2 = 0$.

Motion without gravity. At $q = (0, \pi/2)$, $\dot q = (1, 1)$ rad/s and $\tau = 0$, in a horizontal plane: $M = [[3, 1], [1, 1]]$ with $\det M = 2$, and $C\dot q = (-3, 1)$ N m. So $\ddot q = -M^{-1}(-3, 1) = -\tfrac12(1 \cdot (-3) - 1 \cdot 1,\ -1 \cdot (-3) + 3 \cdot 1) = (2, -3)$ rad/s$^2$. The [inverse dynamics](/inverse-dynamics/) of this state and acceleration gives back $M(2, -3) + (-3, 1) = (3, -1) + (-3, 1) = (0, 0)$.

Conditioning. At $q_2 = 0$ the eigenvalues of $M$ are $3 \pm 2\sqrt2$, so its [condition number](/condition-number/) is $(3 + 2\sqrt2)^2 \approx 34$. Arms with heavy proximal links and light distal links have much larger condition numbers, which makes the solve for $\ddot q$ sensitive to errors in $\tau$ and in the model.

## Known algorithms

All counts are in the [real-RAM](/real-ram/) model for a serial chain or a tree of $n$ joints with one degree of freedom each.

1. Inverse dynamics plus a linear solve (Walker and Orin 1982, their first method). One call of the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/) with $\ddot q = 0$ gives the bias $h = C\dot q + g$. Calls with $\dot q = 0$, no gravity and $\ddot q = e_j$ give the columns of $M$. That is $n + 1$ calls of an $O(n)$ algorithm, so $O(n^2)$ to form the system, and then $O(n^3)$ to solve $M\ddot q = \tau - h$.
2. Composite-rigid-body method (Walker and Orin 1982, their third method; Featherstone 2008, Chapter 6). The bias comes from one RNEA call, and the [composite-rigid-body algorithm](/composite-rigid-body-algorithm/) forms $M$ in $O(n^2)$ for a serial chain. A [Cholesky decomposition](/cholesky-decomposition/) $M = LL^T$ costs $O(n^3)$, and the two triangular solves $O(n^2)$. For trees, the factorization can keep the branch-induced sparsity of $M$ and costs less.
3. Articulated-body algorithm (Featherstone 1983; Featherstone 2008, Chapter 7). It never forms $M$. A pass from the base outward computes the velocities, a pass inward computes the [articulated-body inertia](/articulated-body-inertia/) and bias force of each subtree, and a second pass outward computes the accelerations. Each pass does a constant amount of work per joint, so the total is $O(n)$.
4. Lynch and Park (Section 8.5) state the problem with $M$ and $h$ from their closed-form expressions and solve the linear system, which is the second method in matrix notation.

Which method is fastest in practice depends on $n$ and on the branching. For small $n$ the composite-rigid-body method is often faster than the articulated-body algorithm, because its constants are smaller; Featherstone (2008, Chapter 10) compares the operation counts. Do not use a hand count as a published one.

## Bounds

- Upper bound: $O(n)$ arithmetic operations for a serial chain or a tree, by the articulated-body algorithm.
- Upper bound with $M$: $O(n^2)$ to form $M$ plus $O(n^3)$ for the dense Cholesky factorization of a serial chain. The cubic term counts the factorization; without it, given a factor, the solve is $O(n^2)$.
- Lower bound: $\Omega(n)$, because the output has $n$ numbers and in general each depends on the input. So forward dynamics of a serial chain or a tree is $\Theta(n)$ in the real-RAM model.

## Reductions

- Forward dynamics to inverse dynamics. Because the manipulator equation is affine in $\ddot q$, $n + 1$ calls of an inverse dynamics routine give $M$ and $h$, and one solve gives $\ddot q$. This is method 1 above.
- Inverse dynamics to forward dynamics. The map $\tau \mapsto \ddot q$ is affine, $\ddot q = M^{-1}\tau + b$. With $n + 1$ calls of a forward dynamics routine you get $b$ (at $\tau = 0$) and the columns of $M^{-1}$ (at $\tau = e_j$), and then $\tau = M(\ddot q - b)$. So the two problems are equivalent up to $O(n)$ calls and an $O(n^3)$ solve, although direct algorithms solve each in $O(n)$.
- Simulation to forward dynamics. An explicit [Runge-Kutta method](/runge-kutta-methods/) of order 4 makes four forward dynamics calls per time step. For long runs without friction, [symplectic integrators](/symplectic-integrators/) are used because their energy error does not drift. Since $M$ depends on $q$, the Hamiltonian is not separable, and the usual symplectic methods for it are implicit.

## Applications

- Robot simulators and physics engines evaluate forward dynamics at every time step, often with contact.
- Shooting methods for [trajectory optimization](/trajectory-optimization/) roll out the dynamics from a guess of the torques.
- Model-based state estimators predict the next state with forward dynamics.
- Control design checks a controller in simulation, with a model that differs on purpose from the one inside the controller.

## References
