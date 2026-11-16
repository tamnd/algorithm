---
tag: EYWAYK
kind: definition
slug: dynamically-consistent-generalized-inverse
name: Dynamically consistent generalized inverse
aliases:
- inertia-weighted pseudoinverse
area: robotics/robot-dynamics
level: advanced
summary: "The right inverse J_bar = M^-1 J^T (J M^-1 J^T)^-1 of a task Jacobian, weighted by the mass matrix; torques in its null space cause no task acceleration."
prereqs: [pseudoinverse, joint-space-inertia-matrix, operational-space-formulation]
see_also: [null-space-projection, jacobian-pseudoinverse-method, task-priority-inverse-kinematics, weighted-least-squares, sherman-morrison-formula, lagrange-multiplier, whole-body-control, positive-definite-matrix]
sources:
  - paper: doi:10.1177/027836499501400103
    title: "Oussama Khatib, Inertial properties in robotic manipulation: an object-level framework, The International Journal of Robotics Research 14(1), 1995"
    locator: pages 19 to 36
  - paper: doi:10.1177/027836499701600203
    title: Roy Featherstone and Oussama Khatib, Load independence of the dynamically consistent inverse of the Jacobian matrix, The International Journal of Robotics Research 16(2), 1997
    locator: pages 168 to 170
  - paper: doi:10.1109/JRA.1987.1087068
    title: "Oussama Khatib, A unified approach for motion and force control of robot manipulators: the operational space formulation, IEEE Journal of Robotics and Automation 3(1), 1987"
    locator: pages 43 to 53
---

The dynamically consistent generalized inverse of a task Jacobian $J$ is the right inverse $\bar J = M^{-1} J^T (J M^{-1} J^T)^{-1}$, where $M$ is the [joint-space inertia matrix](/joint-space-inertia-matrix/) of the robot, so it is the [pseudoinverse](/pseudoinverse/) of $J$ in the metric of the kinetic energy. Its null-space projector separates the joint torques of a redundant robot into torques that act on the task and torques that do not change the task acceleration at all. Khatib introduced it in the [operational space formulation](/operational-space-formulation/) of redundant robots, and Featherstone and Khatib (1997) proved that it does not depend on a load carried by the end-effector.

## Definition

Let $M \in \mathbb{R}^{n \times n}$ be symmetric [positive definite](/positive-definite-matrix/) and let $J \in \mathbb{R}^{m \times n}$, $m \le n$, have full row rank. Let $\Lambda = (J M^{-1} J^T)^{-1}$, the task-space inertia. The **dynamically consistent generalized inverse** of $J$ is
$$\bar J = M^{-1} J^T \Lambda = M^{-1} J^T (J M^{-1} J^T)^{-1} \in \mathbb{R}^{n \times m}.$$
It satisfies $J \bar J = I_m$, and $N = I - \bar J J$ is a projector onto the null space of $J$.

It has three equivalent descriptions.

1. **Minimum kinetic energy.** For each $\dot x$, $\dot q = \bar J \dot x$ is the unique minimizer of $\tfrac12 \dot q^T M \dot q$ under $J \dot q = \dot x$. With a [Lagrange multiplier](/lagrange-multiplier/) $\nu$, the optimality condition is $M \dot q = J^T \nu$, so $\dot q = M^{-1} J^T \nu$, and $J \dot q = \dot x$ gives $\nu = \Lambda \dot x$.
2. **Weighted pseudoinverse.** $\bar J$ is the minimum norm right inverse of $J$ for the norm $\| \dot q \|_M = (\dot q^T M \dot q)^{1/2}$; see [weighted least squares](/weighted-least-squares/).
3. **Dynamic consistency.** A right inverse $G$ of $J$ is called dynamically consistent if every torque of the form $(I - G J)^T \tau_0$ produces no task acceleration from rest, that is $J M^{-1} (I - G J)^T = 0$. This condition reads $J M^{-1} = J M^{-1} J^T G^T$, so $G^T = \Lambda J M^{-1}$ and $G = \bar J$. So $\bar J$ is the only dynamically consistent right inverse. This is a theorem with the short proof just given.

**Load independence (theorem).** Let a rigid load be attached to the end-effector, with the full task of six coordinates, so that the mass matrix becomes $M_L = M + J^T \Lambda_L J$, where $\Lambda_L$ is the inertia of the load in task coordinates. Then $\bar J$ does not change, and the task inertia becomes $\Lambda + \Lambda_L$ (Featherstone and Khatib 1997). In short, the push-through identity gives $M_L^{-1} J^T = M^{-1} J^T (I + \Lambda_L \Lambda^{-1})^{-1}$, so $J M_L^{-1} J^T = \Lambda^{-1} (I + \Lambda_L \Lambda^{-1})^{-1}$, whose inverse is $\Lambda + \Lambda_L$, and $M_L^{-1} J^T (\Lambda + \Lambda_L) = M^{-1} J^T \Lambda$. The identity is a form of the Woodbury formula; see the [Sherman-Morrison formula](/sherman-morrison-formula/).

## Examples and non-examples

**A redundant planar arm.** Take the planar arm with two joints, links of 1 m and point masses of 1 kg at the link ends, at $q = (0, \pi/2)$, and the task of the $x$ coordinate of the hand. Then
$$M = \begin{pmatrix} 3 & 1 \\ 1 & 1 \end{pmatrix}, \quad J = (-1, -1), \quad \Lambda = 1 \text{ kg}, \quad \bar J = \begin{pmatrix} 0 \\ -1 \end{pmatrix}.$$
To move the hand in $x$ at 1 m/s with the least kinetic energy, turn only joint 2, at $-1$ rad/s; the kinetic energy is 0.5 joule. The null-space projector is $N = \begin{pmatrix} 1 & 0 \\ -1 & 0 \end{pmatrix}$.

**A square Jacobian.** If $m = n$ and $J$ is invertible, $\bar J = J^{-1}$ for every $M$.

**Non-example: the Moore-Penrose pseudoinverse.** For the same arm, $J^+ = J^T (J J^T)^{-1} = (-0.5, -0.5)^T$. It is a right inverse of $J$, but it is not dynamically consistent: the torque $(I - J^+ J)^T \tau_0 = (0.5, -0.5)$ N m for $\tau_0 = (1, 0)$ N m gives the hand the acceleration $0.5$ m/s$^2$. For $\dot x = 1$ m/s it also gives the kinetic energy 0.75 joule, more than the minimum. $J^+ = \bar J$ holds exactly when $M^{-1}$ maps the row space of $J$ into itself, for example when $M = c I$.

**Non-example: the transpose.** $J^T$ maps task forces to joint torques and appears in $\tau = J^T F$, but it is not an inverse of $J$: $J J^T \ne I$ in general.

## Related definitions

- [Operational space formulation](/operational-space-formulation/): the task dynamics $\Lambda \ddot x + \eta = F$ and the torque $\tau = J^T F + (I - \bar J J)^T \tau_0$.
- [Null-space projection](/null-space-projection/): the kinematic projector $I - J^+ J$, which is the special case $M = I$.
- [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/) and [task-priority inverse kinematics](/task-priority-inverse-kinematics/): the kinematic analogues, with $J^+$ in place of $\bar J$.
- [Whole-body control](/whole-body-control/): hierarchies of tasks that use dynamically consistent projectors, or a quadratic program in their place.

## References
