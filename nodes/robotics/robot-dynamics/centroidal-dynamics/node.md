---
tag: EWBD4X
kind: model
slug: centroidal-dynamics
name: Centroidal dynamics
aliases:
- centroidal momentum dynamics
area: robotics/robot-dynamics
level: advanced
summary: The rate of the total momentum about the center of mass equals the sum of contact wrenches and gravity, a model of the whole robot.
prereqs: [centroidal-momentum-matrix, newton-euler-equations, wrench]
see_also: [convex-mpc-legged-locomotion, whole-body-control, linear-inverted-pendulum-model, zero-moment-point, contact-wrench-cone, spring-loaded-inverted-pendulum, floating-base-dynamics, footstep-planning]
sources:
  - paper: doi:10.1007/s10514-013-9341-4
    title: David E. Orin, Ambarish Goswami and Sung-Hee Lee, Centroidal dynamics of a humanoid robot, Autonomous Robots 35(2-3), 2013
    locator: pages 161 to 176
  - paper: doi:10.1109/IROS.2008.4650772
    title: "David E. Orin and Ambarish Goswami, Centroidal momentum matrix of a humanoid robot: structure and properties, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2008"
    locator: pages 653 to 659
  - paper: doi:10.1109/HUMANOIDS.2014.7041375
    title: Hongkai Dai, Andrés Valenzuela and Russ Tedrake, Whole-body motion planning with centroidal dynamics and full kinematics, IEEE-RAS International Conference on Humanoid Robots, 2014
    locator: pages 295 to 302
---

Centroidal dynamics is the model of a robot, or of any system of rigid bodies, that keeps only its total momentum about its center of mass. The rate of change of this momentum equals the sum of the external wrenches about the center of mass: the contact forces and gravity. The joints can move momentum between the bodies, but they cannot change the total. So the model is exact for the whole robot, and it has only 6 equations, however many joints the robot has. Legged robots use it to plan and control balance, walking and jumping, with the [centroidal momentum matrix](/centroidal-momentum-matrix/) to connect it to the joints.

## The machine

**State.** The position of the center of mass (CoM) $c$ in meters, the linear momentum $l = m \dot c$ in kg m/s, and the angular momentum $k$ about the CoM in kg m$^2$/s, all in a fixed frame with $z$ up. Together, $h_G = (k, l)$ is the centroidal momentum. When the model is coupled to the joints, the state also holds the configuration $q$ of the robot, with $h_G = A_G(q) \dot q$.

**Inputs.** The contact forces $f_j$ in N at the contact points $p_j$ in m, $j = 1, \dots, N_c$, and for surface contacts also contact torques $\tau_j$ in N m. Together they are the contact [wrenches](/wrench/).

**Parameters.** The total mass $m$ in kg and the gravity vector $g = (0, 0, -9.81)$ m/s$^2$.

**Equations.** By the [Newton-Euler equations](/newton-euler-equations/) for the whole system of bodies,
$$\dot c = \frac{l}{m}, \qquad \dot l = \sum_j f_j + m g, \qquad \dot k = \sum_j \big( (p_j - c) \times f_j + \tau_j \big).$$
Gravity acts at the CoM, so it has no moment about it. With the centroidal momentum matrix, the same equations read $A_G(q) \ddot q + \dot A_G(q, \dot q) \dot q = \sum_j \mathrm{Ad}(T_{jG})^T w_j + (0, m g)$, where $w_j$ is contact wrench $j$ in a frame at the contact.

**Assumptions.** The bodies are rigid, and the only external forces are gravity and the contact forces. The equations themselves need nothing more. When the model is used alone as a reduced model, it also assumes that the joints can produce any motion of the bodies that the momentum allows, so it ignores the joint limits, the torque limits and the kinematics. The contact forces must respect the contact model: a unilateral normal force $f_{j,z} \ge 0$ on flat ground and a friction cone, which together give the [contact wrench cone](/contact-wrench-cone/).

## What it counts

The model counts the momentum that the contacts can give the robot and nothing else. A motion of the robot is possible only if its centroidal momentum rate lies in the set of rates that the allowed contact wrenches produce; for the friction-cone constraints this set is a convex cone shifted by gravity. The joint torques, the internal forces and the motion of each body are not in the model. The joints decide how the momentum is shared among the bodies, but the total follows the equations above whatever the joints do. In particular, without contacts, nothing the robot does with its joints can change $l$ other than by gravity, or change $k$ at all.

## Relation to other models

- **Floating-base dynamics.** In the [floating-base dynamics](/floating-base-dynamics/) of a robot, the six rows of the unactuated base are equivalent to the centroidal dynamics, written in the base frame. The remaining rows add the joint torques. Whole-body control and motion planning often keep the centroidal dynamics and the full kinematics but drop the joint torques; Dai, Valenzuela and Tedrake (2014) planned whole-body motions of humanoid robots this way.
- **Single rigid body.** If the angular momentum is approximated by $k = I_G \omega$ with a constant inertia $I_G$ and the base angular velocity $\omega$, the model becomes one rigid body pushed by the contacts. The [convex MPC for legged locomotion](/convex-mpc-legged-locomotion/) uses this model, with further linearization.
- **Linear inverted pendulum.** Take $\dot k = 0$, a constant height $c_z = z_0$ and flat ground at $z = 0$, and let $p$ be the [center of pressure](/center-of-pressure/) of the contact forces, with the total force $F$. Then $F_z = m g$ from the vertical row, and the $y$ row of $\dot k = 0$ gives $-z_0 F_x - (p_x - c_x) F_z = 0$. So $m \ddot c_x = F_x = m g (c_x - p_x) / z_0$, which is the [linear inverted pendulum model](/linear-inverted-pendulum-model/), with $p$ as the [zero moment point](/zero-moment-point/).
- **Spring-loaded inverted pendulum.** The [spring-loaded inverted pendulum](/spring-loaded-inverted-pendulum/) also keeps $k = 0$ and adds a spring leg that sets the contact force, a model of running.
- **Contact planning.** [Footstep planning](/footstep-planning/) chooses the contact points $p_j$, and the centroidal dynamics then decides whether the CoM motion between the footsteps is possible.

## Known results in the model

**Standing still.** A robot of $m = 50$ kg with its CoM at $(0, 0, 0.9)$ m stands on two feet at $(0, \pm 0.1, 0)$ m. It is in equilibrium when $\sum_j f_j = -m g$ and $\sum_j (p_j - c) \times f_j = 0$. Each foot pushing $(0, 0, 245.25)$ N up satisfies both: the vertical forces sum to $490.5$ N $= 50 \cdot 9.81$ N, and the moments $(\pm 24.525, 0, 0)$ N m cancel. With $300$ N under the foot at $y = +0.1$ and $190.5$ N under the other, the total force is the same, but $\dot k_x = 0.1 \cdot 300 - 0.1 \cdot 190.5 = 10.95$ N m, so the robot starts to tip about the $x$ axis.

**Pushing forward.** If each foot of the same robot pushes $(10, 0, 245.25)$ N, then $\dot l = (20, 0, 0)$ N and the CoM accelerates at $\ddot c_x = 0.4$ m/s$^2$. But the moments are $(24.525, -9, -1)$ and $(-24.525, -9, 1)$ N m, so $\dot k = (0, -18, 0)$ N m and the robot pitches backward. To accelerate without pitching, the center of pressure must move back to $p_x = -0.4 \cdot 0.9 / 9.81 = -0.0367$ m, so that the vertical force gives the moment $0.0367 \cdot 490.5 = 18$ N m back. This is the linear inverted pendulum result.

**Flight.** Without contacts, $\dot l = m g$ and $\dot k = 0$. The CoM follows a parabola and the angular momentum about it is constant. A CoM that leaves the ground with $\dot c = (1, 0, 2)$ m/s reaches its highest point after $2 / 9.81 = 0.204$ s, $0.204$ m higher. The joints cannot change this path.

**Turning with zero angular momentum.** $k = 0$ does not mean that the orientation of the robot is fixed, because the angular rows of $A_G$ are not the derivative of any function of the configuration. By a cycle of joint motions, a robot in flight can change its orientation with $k = 0$ all the time, as a falling cat lands on its feet.

**Convex constraints, bilinear dynamics.** For fixed contact points and a fixed CoM, the equations are linear in the contact forces, and the friction cones are convex, so a whole-body controller can find the forces by [quadratic programming](/quadratic-programming/). When the CoM path and the forces are both unknown, the term $(p_j - c) \times f_j$ is bilinear, and trajectory optimization with the full centroidal model is nonconvex.

## References
