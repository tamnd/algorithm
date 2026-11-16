---
tag: 88VVBT
kind: technique
slug: whole-body-control
name: Whole-body control
aliases:
- WBC
- whole-body operational space control
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Computes joint torques of a floating-base robot that serve several tasks and contact constraints at once, often by a quadratic program."
prereqs: [floating-base-dynamics, operational-space-formulation, quadratic-programming]
see_also: [hierarchical-quadratic-programming, null-space-projection, task-priority-inverse-kinematics, centroidal-dynamics, contact-wrench-cone, zero-moment-point, convex-mpc-legged-locomotion, polyhedral-friction-cone]
sources:
  - paper: doi:10.1142/S0219843605000594
    title: "Luis Sentis and Oussama Khatib, Synthesis of whole-body behaviors through hierarchical control of behavioral primitives"
    locator: "International Journal of Humanoid Robotics 2(4), pp. 505-518, the whole paper (task, posture and contact constraints for a humanoid robot, with lower priority tasks in the dynamically consistent null space of higher ones)"
  - paper: doi:10.1177/0278364914521306
    title: "Adrien Escande, Nicolas Mansard and Pierre-Brice Wieber, Hierarchical quadratic programming, fast online humanoid-robot motion generation"
    locator: "The International Journal of Robotics Research 33(7), pp. 1006-1028 (strict task priorities with inequality tasks, solved fast enough for the control loop of a humanoid robot)"
  - paper: doi:10.1109/TRO.2011.2142450
    title: "Oussama Kanoun, Florent Lamiraux and Pierre-Brice Wieber, Kinematic control of redundant manipulators, generalizing the task-priority framework to inequality task"
    locator: "IEEE Transactions on Robotics 27(4), pp. 785-792 (a cascade of QPs, one per priority level, with inequality tasks)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Chapter 8 (the dynamics of open chains, M(q), the Coriolis and gravity terms) and Chapter 11 (task space motion control)"
---

Whole-body control is a way to command every joint of a robot with many joints, such as a humanoid, a quadruped or a mobile manipulator, so that it does several things at once. It keeps its balance, holds its feet or hands on contacts without slipping, reaches with a hand, and keeps a good posture. Each goal is written as a task: a desired acceleration of some point or quantity, such as the center of mass, a foot or a hand. At each control cycle, a solver finds the joint accelerations, the contact forces and the joint torques that meet the equations of motion and the contact constraints and that serve the tasks as well as possible, either by weights or in a strict order of priority. Sentis and Khatib built it for humanoid robots on the operational space formulation; today it is usually a [quadratic program](/quadratic-programming/), solved a thousand times per second. The same template works for a fixed arm, where it is the operational space control of the arm with a posture task in the null space.

## In plain words

A humanoid robot that opens a door must do many things at the same moment. It must not fall. Its feet must not slide. Its hand must follow the handle. Its other arm and its head should stay in a natural pose. Every joint affects all of these at once, so you cannot give one joint to each job.

Whole-body control writes each job as a wish for how some part of the body should speed up. Then it asks a solver: which joint efforts give the motion closest to all the wishes, without breaking the laws of physics, without slipping, and without asking the motors for too much? If not all wishes can come true, the important ones win, for example "do not fall" before "look nice".

## When it applies

- The robot has more joints than any one task needs, so tasks can share the joints.
- The robot has torque control, or at least a fast joint loop that can follow accelerations, and a model of its masses and inertias.
- Contacts with the ground or with objects are known: where they are and which ones are active. The contact schedule comes from a higher level, such as a footstep planner or [convex MPC](/convex-mpc-legged-locomotion/).
- The state, including the pose and velocity of the floating base, is estimated at the control rate.

For a fixed arm, the base is not floating, and there may be no contacts; the template still applies, with fewer constraints.

## The template

**Model.** A floating-base robot has the generalized velocity $\nu = (\nu_b, \dot q) \in \mathbb{R}^{6 + n}$, with the twist $\nu_b$ of the base and the $n$ joint rates. Its [floating-base dynamics](/floating-base-dynamics/) with $k$ contacts are

$$M(q)\dot\nu + h(q, \nu) = S^T\tau + J_c^T\lambda, \qquad S = \begin{pmatrix} 0_{n \times 6} & I_n \end{pmatrix},$$

where $M$ is the mass matrix, $h$ holds the Coriolis, centrifugal and gravity terms, $\tau$ the joint torques, $J_c$ the stacked contact Jacobians and $\lambda$ the contact forces.

**Steps at each control cycle.**

1. Read the state $(q, \nu)$ and compute $M$, $h$, $J_c$, $\dot J_c\nu$ and the task Jacobians $J_i$ and $\dot J_i\nu$, with the recursive algorithms of rigid body dynamics.
2. For each task $i$ with coordinates $x_i$, set the wanted acceleration $\ddot x_i^\ast = \ddot x_{i,d} + K_{d,i}(\dot x_{i,d} - \dot x_i) + K_{p,i}(x_{i,d} - x_i)$.
3. Solve for $(\dot\nu, \lambda, \tau)$:
$$\min \sum_i w_i\,\bigl|J_i\dot\nu + \dot J_i\nu - \ddot x_i^\ast\bigr|^2 + \varepsilon\,\bigl(|\lambda|^2 + |\tau|^2\bigr)$$
subject to the dynamics, the contact condition $J_c\dot\nu + \dot J_c\nu = 0$ (feet do not move), each contact force in a linearized [friction cone](/polyhedral-friction-cone/) with a positive normal part, and the torque, joint limit and other inequality limits.
4. Send $\tau$ to the joints, and repeat at the next cycle.

**The unactuated rows.** The first six rows of the dynamics have no torque:

$$M_b\dot\nu + h_b = J_{c,b}^T\lambda.$$

They say that the contact forces alone must produce the change of the total momentum of the robot, which is the Newton-Euler equation of the whole body about its center of mass, the [centroidal dynamics](/centroidal-dynamics/). Many solvers keep only these rows as constraints, with variables $(\dot\nu, \lambda)$, and compute $\tau$ afterwards from the other $n$ rows, which is cheaper.

**Weights or priorities.** With weights $w_i$, the tasks trade off against one another, and a small task can still disturb a large one a little. With strict priorities, each task is optimized only among the solutions that keep all higher ones at their best value: this is [hierarchical quadratic programming](/hierarchical-quadratic-programming/). Without inequalities, the strict version has a closed form with [null space projections](/null-space-projection/): Sentis and Khatib used the dynamically consistent null space of the [operational space formulation](/operational-space-formulation/), in which a lower task cannot produce any acceleration of a higher task.

## Classic examples

**Accelerating the center of mass on two feet.** A planar robot of mass $m = 50$ kg has its center of mass at height $0.9$ m above the point between its feet, which are at $x = -0.1$ and $x = 0.1$ m. The task asks for a forward acceleration of the center of mass of $0.5$ m/s² with no change of the angular momentum. The unactuated rows give three equations for the two contact forces $(f_{x,1}, f_{z,1})$ and $(f_{x,2}, f_{z,2})$:

- forward: $f_{x,1} + f_{x,2} = 50 \cdot 0.5 = 25$ N;
- up: $f_{z,1} + f_{z,2} = 50 \cdot 9.81 = 490.5$ N;
- moment about the center of mass: $-0.1 f_{z,1} + 0.1 f_{z,2} + 0.9(f_{x,1} + f_{x,2}) = 0$, so $f_{z,1} - f_{z,2} = 225$ N.

So $f_{z,1} = 357.75$ N on the rear foot and $f_{z,2} = 132.75$ N on the front foot. The center of pressure is at $(-0.1 \cdot 357.75 + 0.1 \cdot 132.75)/490.5 = -0.0459$ m, which is the [zero-moment point](/zero-moment-point/) $-0.9 \cdot 0.5/9.81$. The split of the 25 N between the feet is free, an internal force; the regularization term picks $12.5$ N each, inside a friction cone with $\mu = 0.5$ ($12.5 \le 0.5 \cdot 132.75$). If the task asks for $2$ m/s² instead, the center of pressure would have to be at $-0.18$ m, behind the rear foot, so no positive normal forces exist. With the task as a weighted cost, the solver gives the largest acceleration that the feet allow, $0.1 \cdot 9.81/0.9 = 1.09$ m/s².

**Humanoid reaching.** Tasks in priority order: the contact constraints, the center of mass over the support polygon, the hand position, and a posture task that keeps the joints near a rest pose. When the hand target is too far, the hand task fails gracefully while the balance holds.

**Quadruped trotting.** [Convex MPC](/convex-mpc-legged-locomotion/) plans the ground forces of the stance feet over a horizon on a simple model; whole-body control tracks those forces and the swing foot paths with the full model at a higher rate.

**A fixed arm.** With no floating base and no contacts, $S = I$, and the template with an end effector task and a posture task is operational space control, with the posture in the null space of the end effector task.

## Variations

- **Velocity-level and kinematic versions.** Solve for joint velocities with [task-priority inverse kinematics](/task-priority-inverse-kinematics/) and send them to stiff position-controlled joints. This is simpler and often enough for slow tasks.
- **Projected dynamics.** Remove the contact forces by projecting the dynamics onto the null space of $J_c$, so the solver needs only $\dot\nu$ and $\tau$.
- **Momentum-based control.** Make the rate of change of centroidal momentum the main task, and distribute the contact forces in the [contact wrench cone](/contact-wrench-cone/).
- **With prediction.** Model predictive control on the full or centroidal model over a short horizon, with whole-body control as the fast tracking layer.

## Pitfalls

- **Wrong contact state.** If a foot is declared in contact but is in the air, the constraint $J_c\dot\nu + \dot J_c\nu = 0$ is false and the solution is wrong. Use contact detection and switch constraints smoothly.
- **Infeasible hard tasks.** A task written as an equality constraint can make the QP infeasible, as in the example with $2$ m/s². Keep tasks as costs or as priority levels, and keep only the physics as hard constraints.
- **Gains in conflict.** With weights, a stiff low-importance task can pull a high-importance task off its target. Scale the weights by the task units, or use strict priorities.
- **Model errors.** The torques rely on $M$ and $h$; errors in masses show up as tracking errors. Add integral action on the slow tasks, or estimate the parameters.
- **Time budget.** The QP must finish in about 1 ms on the robot computer. Warm start from the last solution, and keep the number of variables small with the unactuated-rows form.

## Exercises

1. In the example with two feet, find the largest forward acceleration of the center of mass when the friction coefficient is $\mu = 0.05$ and the forces are split equally between the feet.
2. Show that for a fixed arm with an end effector task of full rank and no inequality limits, the weighted problem with a tiny posture weight tends to the solution with the posture in the null space of the end effector task.
3. Write the unactuated rows for a robot that stands on one point foot, and show that the horizontal acceleration of its center of mass is fixed by the position of the foot and the height of the center of mass if the angular momentum must not change.
4. Explain why the internal force between two feet does not change the motion of the robot, and give one reason to choose it on purpose rather than by the smallest norm.

## References
