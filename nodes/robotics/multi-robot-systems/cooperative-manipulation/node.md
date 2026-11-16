---
tag: MVPA8B
kind: problem
slug: cooperative-manipulation
name: Cooperative manipulation
aliases:
- multi-arm manipulation
area: robotics/multi-robot-systems
level: advanced
summary: Several arms or robots hold and move one object together, sharing the load while internal forces stay bounded.
prereqs: [grasp-matrix, wrench, null-space-projection]
see_also: [impedance-control, hybrid-position-force-control, admittance-control, operational-space-formulation, force-closure, newton-euler-equations, geometric-jacobian, multi-robot-system]
sources:
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, 2nd edition, Springer, 2016
    locator: Chapter 39, Cooperative manipulation, by Fabrizio Caccavale and Masaru Uchiyama, pages 989 to 1006 (kinetostatics, load sharing, internal forces and control schemes)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, mechanics, planning, and control, Cambridge University Press, 2017
    locator: the chapter on grasping and manipulation (contact wrenches and the map from contact forces to the object wrench)
---

Cooperative manipulation is the problem of moving one object with several arms or mobile manipulators that hold it at the same time. The robots must share the weight and the motion so that the object follows the wanted path, while the forces that only squeeze the object, the *internal forces*, stay within safe limits. These internal forces are the contact forces in the null space of the [grasp matrix](/grasp-matrix/), so the problem is the control of both the object motion and that null space; it differs from a single-arm grasp, studied with [force closure](/force-closure/), because each arm has its own controller and errors between arms create internal forces at once.

## In plain words

Two people carry a table. Each one lifts part of the weight, and both walk the same way. If one of them pulls a bit too far, the table does not move: instead the two people pull against each other through it. These pulls do nothing useful, and if they get too big, the table breaks or slips out of their hands.

Robots that carry an object together have the same task. They must split the load, move together, and keep the pulling and pushing against each other small. Because the object is stiff, even a tiny mismatch in where the robots think it is turns into large forces, so the robots must control force as well as position.

## Definition

There are $r$ robots holding one rigid object. Robot $i$ applies a contact [wrench](/wrench/) $f_i$ at its grasp, 6 numbers for a rigid grasp in space, fewer for a point contact. Stack them into $f$. The grasp matrix $G$ maps the contact wrenches to the net wrench on the object at a reference point:

$$w = G f.$$

The object moves by the [Newton-Euler equations](/newton-euler-equations/): $w$ must equal the wrench needed for the wanted acceleration plus the weight, in newtons and newton meters.

- **Load sharing.** Given the needed $w$, choose $f$ with $G f = w$.
- **Internal forces.** Any $f$ in the null space of $G$ gives $w = 0$: it squeezes or twists the object without moving it. Every solution is $f = G^{+} w + (I - G^{+} G) \lambda$ for a free vector $\lambda$, where $G^{+}$ is the pseudoinverse, and the second term is the internal part.
- **Motion.** The robots' end effectors must keep the grasp: their velocities must match the rigid motion of the object, through each robot's [geometric Jacobian](/geometric-jacobian/).
- **Control problem.** Given a wanted object trajectory and wanted internal forces, find joint torques for all robots so that both are tracked, with contact and torque limits.

The robots run synchronous control loops, typically at hundreds to thousands of updates per second. A *centralized* scheme computes all commands on one computer from all sensor data. A *decentralized* scheme lets each robot compute its own command from its own sensors, and maybe from messages with the others.

## Variants

- **Rigid grasps** (each robot holds the object firmly) or **point contacts with friction** (robots push), where each contact force must also stay in its friction cone.
- **Fixed-base arms** in a work cell, or **mobile manipulators** whose bases also move.
- **Rigid or flexible objects**, such as sheets, cables or soft bags.
- **Known or unknown objects**: the mass, center of mass and grasp points may have to be estimated.
- **Humans in the team**: a robot shares a load with a person, who is not controlled.
- **Many simple robots** without arms that push an object together, related to [swarm robotics](/swarm-robotics/).

## Examples

**Two robots lift a bar, in the plane.** A bar of mass 2 kg is held at points $(-0.5, 0)$ m and $(0.5, 0)$ m from its center, with point contacts that transmit forces only. Robot $i$ applies $(f_{ix}, f_{iy})$. The net force and the moment about the center are

$$G = \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & -0.5 & 0 & 0.5 \end{pmatrix}, \quad f = (f_{1x}, f_{1y}, f_{2x}, f_{2y}).$$

To hold the bar still against gravity, $w = (0, 2 \cdot 9.81, 0) = (0, 19.62, 0)$ in newtons and newton meters. The pseudoinverse solution is $f = (0, 9.81, 0, 9.81)$ N: each robot lifts half. $G$ has rank 3 and 4 columns, so its null space has dimension 1, spanned by $(1, 0, -1, 0)$. Adding $\lambda (1, 0, -1, 0)$ gives forces that pull the bar apart ($\lambda < 0$) or squeeze it ($\lambda > 0$) by $\lambda$ newtons along its axis, and change nothing about its motion.

**A position error.** If both robots hold the bar rigidly under stiff position control with stiffness $k$ in newtons per meter, and robot 2's command is 1 mm too far out, the bar cannot stretch, so a pull of about $k \cdot 0.001 / 2$ N appears in the bar, if both arms have the same stiffness. With $k = 10^5$ N/m this is 50 N, more than twice the weight, from an error of 1 mm. This is why cooperative manipulation needs force or impedance control.

**Two arms with rigid grasps in space.** Each grasp transmits 6 wrench components, so $f$ has 12 entries and $w$ has 6. The null space has dimension 6: three internal forces and three internal moments.

## Known algorithms

- **Leader and follower.** One robot is position controlled and leads; the others are force controlled and follow, keeping their contact force at the wanted value. Simple, but slow to react when the leader moves fast.
- **[Hybrid position and force control](/hybrid-position-force-control/).** Control the object motion in the directions it can move and the internal forces in the null space directions.
- **Object [impedance control](/impedance-control/).** Make the object behave like a mass-spring-damper around the wanted path, and add an impedance on the internal forces, so that errors give bounded forces.
- **Augmented object model.** Khatib and coworkers (1996) combine the object and all arms into one dynamic model in the task space, in the style of the [operational space formulation](/operational-space-formulation/), and split the needed wrench among the robots.
- **Load distribution by optimization.** Choose $\lambda$ to minimize the largest torque, to keep each contact force inside its friction cone, or to keep internal forces at a set value, by a small linear or quadratic program.
- **Decentralized schemes.** Each robot uses its own force sensor, and a model of the object, to estimate the motion and its share; messages are used only to agree on the plan.

## Bounds

- **Dimension of internal forces (theorem).** For $r$ rigid grasps in space, $f$ has $6 r$ entries, $G$ has rank 6 when the grasps are not all at one point, and the internal forces form a space of dimension $6 r - 6$. For point contacts with friction in space, the dimension is $3 r - 6$ when $G$ has full rank.
- **Load sharing is linear (theorem).** For fixed contact points, all solutions of $G f = w$ are an affine space, so any convex limit on forces and torques gives a convex problem.
- **Sensitivity (heuristic, from the example).** With stiff grasps, internal forces grow with the stiffness times the position error, as the example shows; in practice compliance is added to keep forces safe.

## Reductions

- With $r = 1$ the problem reduces to the control of one arm in contact with the object.
- With frictional point contacts and no motion, holding the object is the [force closure](/force-closure/) question for the grasp of all robots together.
- Load sharing is a [null space projection](/null-space-projection/) problem: the needed object wrench is met first, and secondary goals act in the null space of $G$.

## Applications

Two arms in a factory carry a car door or a long beam, two arms of a humanoid hold a box, several mobile robots move furniture or large parts in a warehouse, space robots handle a satellite, and surgical robots use two arms on one tissue. In each case the key risk is internal force: a mismatch between the robots damages the object or the robots.

## References
