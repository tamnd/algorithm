---
tag: V9JGZW
kind: concept
slug: floating-base-dynamics
name: Floating-base dynamics
aliases:
- floating base robot model
area: robotics/robot-dynamics
level: core
summary: The dynamics of a robot whose base is not fixed to the world, such as a humanoid or a quadruped; the six coordinates of the base have no actuator, so only contact forces can move the whole robot.
prereqs: [newton-euler-equations, manipulator-equation]
see_also: [centroidal-dynamics, centroidal-momentum-matrix, articulated-body-algorithm, recursive-newton-euler-algorithm, whole-body-control, contact-wrench-cone, zero-moment-point, special-euclidean-group]
sources:
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 9, Hybrid Dynamics and Other Topics: Section 9.3 (floating bases), Section 9.4 (floating-base forward dynamics) and Section 9.5 (floating-base inverse dynamics)"
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
  - paper: doi:10.1007/s10514-013-9341-4
    title: David E. Orin, Ambarish Goswami and Sung-Hee Lee, Centroidal dynamics of a humanoid robot, Autonomous Robots 35(2-3), 2013
    locator: the sections on the centroidal momentum matrix and its relation to the floating-base equations
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 8 (dynamics of open chains) for the fixed-base equations and the conventions used here
---

Floating-base dynamics is the dynamics of a robot whose base is free to move in space: a humanoid, a quadruped, a free-flying space robot or a drone with an arm. The configuration has the pose of the base, six coordinates, in addition to the joint angles. No actuator acts on these six coordinates, so the joint motors alone cannot move the center of mass in a chosen way; only the forces from the contacts with the world, and gravity, can.

## In plain words

A robot arm bolted to a table can push on the table, so its motors can move the hand anywhere they like. A walking robot is bolted to nothing. When it swings a leg, the rest of the body moves the other way, because the motors push the parts of the robot against each other and not against the world. If the robot jumps, its center falls along the same curve as a thrown stone, whatever the motors do in the air. To walk, run or stand, the robot must use its feet: it pushes on the ground, and the ground pushes back. The ground can push but not pull, and friction limits the sideways push. So the motion that a legged robot can make at a given moment depends on where its feet are and how hard they can push.

## The idea

Take a robot with $n$ joints and one free base body. The configuration is $q = (T_b, \theta)$ with the base pose $T_b \in$ [SE(3)](/special-euclidean-group/) and the joint angles $\theta \in \mathbb{R}^n$. The velocity is $v = (\mathcal{V}_b, \dot\theta) \in \mathbb{R}^{6+n}$, where $\mathcal{V}_b$ is the [twist](/rigid-body-twist/) of the base, angular part first. The velocity is not the time derivative of a set of coordinates of $q$: the orientation needs at least three coordinates with singular points, or four with a constraint, while its velocity has three components.

The equations of motion have the form of the [manipulator equation](/manipulator-equation/),
$$M(q)\dot v + C(q, v) v + g(q) = S^T \tau + \sum_c J_c(q)^T F_c ,$$
where $M$ is the $(6+n) \times (6+n)$ mass matrix, $\tau \in \mathbb{R}^n$ the joint torques, $S = [\,0_{n \times 6}\ \ I_n\,]$ the selection matrix of the actuated coordinates, and $F_c$ the [wrench](/wrench/) of contact $c$ on the robot, moment first, with its contact Jacobian $J_c$.

Split the equation into the first six rows, of the base, and the last $n$ rows, of the joints:
$$M_{bb}\dot{\mathcal{V}}_b + M_{bj}\ddot\theta + h_b = \sum_c J_{c,b}^T F_c , \qquad M_{jb}\dot{\mathcal{V}}_b + M_{jj}\ddot\theta + h_j = \tau + \sum_c J_{c,j}^T F_c .$$
The base rows have no $\tau$. They are the Newton-Euler equations of the whole robot: written at the center of mass, they say that the rate of change of the total momentum is the gravity wrench plus the contact wrenches. This is [centroidal dynamics](/centroidal-dynamics/), and the matrix that maps $v$ to the total momentum is the [centroidal momentum matrix](/centroidal-momentum-matrix/).

Three consequences follow.

- **Underactuation.** A desired acceleration $\dot v$ is possible only if the base rows can be met with contact wrenches that the contacts can apply, that is wrenches in the [contact wrench cone](/contact-wrench-cone/). Without contact, the center of mass follows a parabola and, with no gravity, the total momentum is constant.
- **Inverse dynamics needs the contact forces.** For a fixed base, the torques follow from $\dot v$ alone. With a floating base, the base rows first fix the sum of the contact wrenches, and when several contacts share the load, the split between them is a choice. [Whole-body control](/whole-body-control/) makes that choice with a quadratic program.
- **Forward dynamics is the same problem with a heavier base.** The [articulated-body algorithm](/articulated-body-algorithm/) treats the base as a body with a joint of six degrees of freedom to the world, and the [composite rigid body algorithm](/composite-rigid-body-algorithm/) forms the full $M(q)$ (Featherstone 2008, Sections 9.3 to 9.5).

## Examples

**A base and one sliding mass.** A base of 3 kg moves without friction on a horizontal line, and a prismatic joint moves a mass of 1 kg along the same line. With the base position $x_b$ and the joint position $d$, the mass is at $x_b + d$, and
$$M = \begin{pmatrix} 4 & 1 \\ 1 & 1 \end{pmatrix}, \qquad M \begin{pmatrix} \ddot x_b \\ \ddot d \end{pmatrix} = \begin{pmatrix} 0 \\ \tau \end{pmatrix}.$$
The solution is $\ddot x_b = -\tau/3$ and $\ddot d = 4\tau/3$. The acceleration of the mass is $\ddot x_b + \ddot d = \tau$ (in m/s$^2$ for $\tau$ in N), and the acceleration of the center of mass is $(3 \ddot x_b + 1 \cdot \tau)/4 = 0$. The motor moves the parts against each other but cannot move the center of mass.

**A free-flying space robot.** A satellite with an arm, with no gravity and no contact, keeps its total linear and angular momentum. When the arm swings, the satellite turns the other way. Because the angular momentum constraint cannot be integrated to a constraint on the configuration, a sequence of arm motions can turn the satellite to any orientation and bring the arm back, as a falling cat does.

**A humanoid standing still.** With $\dot v = 0$ and $v = 0$, the base rows say that the contact wrenches of the two feet sum to minus the gravity wrench: the vertical forces sum to $m g$, and their moment about the center of mass is zero. This is two equations of six components for two feet, so many force distributions are possible, and the [zero moment point](/zero-moment-point/) of the sum must lie in the support polygon.

## Where it is used

- Control of humanoids and quadrupeds: whole-body control and [convex MPC for legged locomotion](/convex-mpc-legged-locomotion/) work with the base rows and contact wrenches as unknowns.
- Simulation of legged robots and of robots that grasp and push, with contact models such as [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/).
- Space robotics, where the base reacts to every motion of the arm.
- [Dynamic parameter identification](/dynamic-parameter-identification/) of legged robots: the base rows do not contain the joint torques, so they give equations in the inertial parameters that need only the contact force measurements.

## References
