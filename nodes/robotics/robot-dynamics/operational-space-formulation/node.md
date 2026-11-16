---
tag: ZWJ4FR
kind: technique
slug: operational-space-formulation
name: Operational space formulation
aliases:
- task-space dynamics
- Khatib operational space
area: robotics/robot-dynamics
level: advanced
summary: "Write the robot dynamics in task coordinates, Lambda x'' + eta = F with Lambda = (J M^-1 J^T)^-1, control the task with a force F, and apply tau = J^T F plus null-space torques."
prereqs: [manipulator-equation, geometric-jacobian, computed-torque-control]
see_also: [dynamically-consistent-generalized-inverse, null-space-projection, whole-body-control, impedance-control, hybrid-position-force-control, task-priority-inverse-kinematics, kinematic-singularity, manipulability-ellipsoid]
sources:
  - paper: doi:10.1109/JRA.1987.1087068
    title: "Oussama Khatib, A unified approach for motion and force control of robot manipulators: the operational space formulation, IEEE Journal of Robotics and Automation 3(1), 1987"
    locator: pages 43 to 53
  - paper: doi:10.1177/027836499501400103
    title: "Oussama Khatib, Inertial properties in robotic manipulation: an object-level framework, The International Journal of Robotics Research 14(1), 1995"
    locator: pages 19 to 36
  - paper: doi:10.1177/027836499701600203
    title: Roy Featherstone and Oussama Khatib, Load independence of the dynamically consistent inverse of the Jacobian matrix, The International Journal of Robotics Research 16(2), 1997
    locator: pages 168 to 170
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8, Section 8.6 (dynamics in the task space)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7, Section 7.8 (operational space dynamic model) and Section 7.9 (dynamic manipulability ellipsoid)
---

The operational space formulation writes the dynamics of a robot in the coordinates of the task, such as the position of the hand, instead of the joint angles. The result is a mass-spring-like equation $\Lambda \ddot x + \eta = F$, in which $\Lambda$ is the inertia that the hand seems to have and $F$ is a force at the hand. A controller chooses $F$ to give the hand the desired motion or contact force, and the joint torques are $\tau = J^T F$, plus torques that act only in the null space of the task when the robot is redundant (Khatib 1987).

## In plain words

When you push the hand of a robot arm, it feels heavier in some directions than in others, because the push must move different amounts of the arm. The method works out this felt weight for the current pose, and also the forces that come from gravity and from the motion of the arm. With these, the hand behaves like a single object that you can push. The controller decides how hard to push the hand to follow a path or to press on a surface, and then turns that push into motor efforts. If the arm has more joints than the task needs, the extra joints can do a second job, such as keeping the elbow away from an obstacle. The method gives a way to do that second job without disturbing the motion of the hand.

## When it applies

- The joint dynamics $M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau$ are known well enough, and the joints are torque controlled.
- The task is a set of $m$ coordinates $x = f(q)$ with the Jacobian $J(q) = \partial f / \partial q$ of size $m \times n$, $m \le n$, and $J$ has full row rank $m$ in the region of use, away from [singularities](/kinematic-singularity/).
- The task is a motion, a force on the environment, or a mix of the two in different directions.

## The template

1. **Task inertia.** Compute $\Lambda(q) = (J M^{-1} J^T)^{-1}$, an $m \times m$ symmetric positive definite matrix.
2. **Task dynamics.** With $\ddot x = J \ddot q + \dot J \dot q$ and $h = C\dot q + g$, the joint dynamics give, for every torque of the form $\tau = J^T F + N^T \tau_0$,
$$\Lambda \ddot x + \eta = F, \qquad \eta = \Lambda \big(J M^{-1} h - \dot J \dot q\big).$$
3. **Task control.** Choose $F = \Lambda a + \eta$, where $a$ is the desired task acceleration, for example $a = \ddot x_d + K_D(\dot x_d - \dot x) + K_P(x_d - x)$. Then $\ddot x = a$: each task coordinate behaves as a unit mass with a PD law. For a force task, put the desired force into $F$ directly in the constrained directions.
4. **Null space.** With the [dynamically consistent generalized inverse](/dynamically-consistent-generalized-inverse/) $\bar J = M^{-1} J^T \Lambda$, define $N = I - \bar J J$. Any $\tau_0$ enters as $N^T \tau_0$.
5. **Torques.** Apply $\tau = J^T F + N^T \tau_0$.

Step 2 holds because $J M^{-1} N^T = J M^{-1} - J M^{-1} J^T \bar J^T = J M^{-1} - \Lambda^{-1}\Lambda J M^{-1} = 0$. So the null-space torque has no effect on $\ddot x$, and $\ddot x = J M^{-1}(J^T F - h) + \dot J \dot q$, which rearranges to the task equation. This is a theorem for exact models; with model errors it holds only approximately.

For a robot with $n = m$ and an invertible $J$, $N = 0$, $\Lambda = J^{-T} M J^{-1}$, and the template is [computed-torque control](/computed-torque-control/) written in task coordinates.

## Classic examples

**The planar arm with two joints.** Take links of 1 m with point masses of 1 kg at their ends, and the pose $q = (0, \pi/2)$, where the hand is at $(1, 1)$ m. Then
$$M = \begin{pmatrix} 3 & 1 \\ 1 & 1 \end{pmatrix}, \quad J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}, \quad J M^{-1} J^T = \begin{pmatrix} 1 & 0 \\ 0 & 0.5 \end{pmatrix}, \quad \Lambda = \begin{pmatrix} 1 & 0 \\ 0 & 2 \end{pmatrix} \text{ kg}.$$
The hand feels a mass of 1 kg along $x$ and 2 kg along $y$. Along $y$, the push points along link 2 and must move the elbow mass with the hand; along $x$, only the hand mass moves, as joint 2 turns. The [manipulability ellipsoid](/manipulability-ellipsoid/) of the dynamics has these directions as its axes.

**The same arm with a task of one coordinate.** Let the task be only the $x$ coordinate of the hand, so $J = (-1, -1)$ and the arm has one redundant degree of freedom. Then $\Lambda = 1$ kg, $\bar J = M^{-1} J^T \Lambda = (0, -1)^T$, and
$$N = I - \bar J J = \begin{pmatrix} 1 & 0 \\ -1 & 0 \end{pmatrix}, \qquad N^T \tau_0 = (\tau_{0,1} - \tau_{0,2},\ 0).$$
A null-space torque $\tau_0 = (1, 0)$ N m gives $N^T\tau_0 = (1, 0)$ and the task acceleration $J M^{-1} N^T \tau_0 = 0$: joint 1 turns and joint 2 turns back so that the hand does not move in $x$. With the projector of the Moore-Penrose [pseudoinverse](/pseudoinverse/) in place of $N$, the torque becomes $(0.5, -0.5)$ and the hand accelerates at $0.5$ m/s$^2$: that projector is not consistent with the dynamics.

**Force control on a surface.** For a hand that presses on a plane with the normal $z$, choose $F_z$ as the desired contact force plus a force feedback term, and $F_x$, $F_y$ by the motion law of step 3. This is the unified motion and force control of Khatib (1987), and it is the dynamic form of [hybrid position/force control](/hybrid-position-force-control/).

## Variations

- **Several tasks with priorities.** A second task acts through $N^T$ of the first, and its own inertia is computed in the null space of the first; this gives a hierarchy of tasks, as in [task-priority inverse kinematics](/task-priority-inverse-kinematics/) at the level of torques.
- **Impedance in task space.** Choose $F$ to make the hand behave like a chosen mass, spring and damper; see [impedance control](/impedance-control/).
- **Whole-body control.** For a robot with a floating base, the task dynamics include the contact constraints, and [whole-body control](/whole-body-control/) solves the same problem with a quadratic program that also enforces torque limits and friction cones.
- **Object-level control.** Khatib (1995) combined the task inertias of several arms and of a held object into one model of the object, so that a controller can command the object directly.

## Pitfalls

- **Singularities.** As $J$ loses rank, $J M^{-1} J^T$ becomes singular and $\Lambda$ grows without bound in the lost direction, so the commanded torques become very large. Damp the inverse or remove the direction from the task near singular poses.
- **Model errors.** The cancellation of $\eta$ and the null-space property both use $M$, $C$ and $g$. Errors couple the null-space motion into the task.
- **Unstable null-space motion.** If $\tau_0$ has no damping term, the redundant joints can drift, because the task controller does not see them. Add a joint damping term to $\tau_0$.
- **The wrong inverse.** The null space must be built with $\bar J$, not with the pseudoinverse of $J$, unless $M$ is a multiple of the identity.
- **Mixed units.** For a task with a position and an orientation, $\Lambda$ mixes kilograms and kilogram square meters; gains must be chosen per block, and the orientation error must be a proper error on SO(3).

## Exercises

1. Show that $J M^{-1} N^T = 0$ for $N = I - \bar J J$, and that $N$ is a projector: $N^2 = N$.
2. For the planar arm of the example, compute $M$, $J$ and $\Lambda$ at $q = (0, \pi/2)$ and confirm $\Lambda = \mathrm{diag}(1, 2)$ kg.
3. Show that $\dot q = \bar J \dot x$ minimizes the kinetic energy $\tfrac12 \dot q^T M \dot q$ among all $\dot q$ with $J \dot q = \dot x$. In the second example, compare the kinetic energy for $\dot x = 1$ m/s: 0.5 joule with $\bar J$ and 0.75 joule with the pseudoinverse.
4. For $n = m$ and invertible $J$, show that $\Lambda = J^{-T} M J^{-1}$ and that the template with $\tau_0 = 0$ gives the computed-torque law in task coordinates.

## References
