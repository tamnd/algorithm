---
tag: TVY2W5
kind: algorithm
slug: impedance-control
name: Impedance control
aliases:
- Hogan impedance control
area: robotics/grasping-and-manipulation
level: core
summary: "Makes the end effector behave as a chosen mass, spring and damper around a goal motion, so contact forces stay moderate and predictable."
model: real-ram
complexity:
  vars: {n: "the number of joints, equal to the task dimension (a nonredundant arm); the bounds are for one control step"}
  time: {per_step: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1985
  people: [Neville Hogan]
  note: Hogan argued that a manipulator in contact should control the dynamic relation between motion and force, its impedance, instead of motion or force alone.
prereqs: [manipulator-equation, wrench, jacobian-statics-duality]
see_also: [admittance-control, hybrid-position-force-control, computed-torque-control, pd-control-with-gravity-compensation, operational-space-formulation, passivity, peg-in-hole, geometric-jacobian]
sources:
  - paper: doi:10.1115/1.3140702
    title: "Neville Hogan, Impedance control: an approach to manipulation: Part I, Theory, Journal of Dynamic Systems, Measurement, and Control 107(1), 1985"
    locator: "pages 1 to 7; Parts II (implementation) and III (applications) follow in the same issue"
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 11, Section 11.7 (impedance control) and Section 11.7.1 (impedance-control algorithm)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 9 (force control, compliance and impedance control)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 9 (Force Control, by Luigi Villani and Joris De Schutter)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 10 (force control)
---

Impedance control is a way to control a robot that touches its environment. It does not command a position or a force. It commands a relation between the two: the end effector should move as if it were a chosen mass on a chosen spring and damper, attached to a goal motion $x_0(t)$. In free space the end effector then follows $x_0$; against an obstacle it pushes with a force that the spring sets, and the force stays bounded even when the position of the obstacle is not known exactly. Hogan introduced the idea in 1985. The dual scheme, which measures the force and commands a motion, is [admittance control](/admittance-control/).

## In plain words

A position-controlled robot that meets a wall it did not expect pushes as hard as its motors allow, because it tries to reach a point inside the wall. A person in the same case gives way. Impedance control makes the robot give way in a chosen manner.

The designer picks three numbers per direction: a mass, a stiffness and a damping. The robot then reacts to a push as a weight on a spring and a shock absorber would. A soft spring gives gentle contact but poor accuracy in free space, and a stiff spring gives the reverse. If the goal point is a little inside a surface, the robot presses on the surface with a force equal to the spring stiffness times that depth, or less if the surface is soft.

## The problem

The arm has $n$ joints and its end effector has a task position $x = f(q) \in \mathbb{R}^n$ with Jacobian $J(q)$, square and nonsingular in the region of interest. The environment applies a force $F_{\text{ext}}$ to the end effector, so the arm obeys

$$M(q)\ddot q + C(q, \dot q)\dot q + g(q) = \tau + J(q)^T F_{\text{ext}},$$

by the [duality of the Jacobian and statics](/jacobian-statics-duality/). A goal motion $x_0(t)$ and target matrices $M_d$, $D_d$, $K_d$ (symmetric positive definite) are given. With $\tilde x = x - x_0$, the task is to choose $\tau$ so that

$$M_d\ddot{\tilde x} + D_d\dot{\tilde x} + K_d\tilde x = F_{\text{ext}}.$$

## The algorithm

This is the form with a force sensor at the wrist and a full dynamic model. Diagonal target matrices are the usual choice.

```pseudo id=main
IMPEDANCE(q, q', x_0, x_0', x_0'', F_ext, M_d, D_d, K_d)
L1  x ← f(q);  x' ← J(q) q'
L2  x̃ ← x - x_0;  x̃' ← x' - x_0'
L3  a_x ← x_0'' + M_d⁻¹ (F_ext - D_d x̃' - K_d x̃)      ▷ wanted task acceleration
L4  a_q ← J(q)⁻¹ (a_x - J'(q, q') q')
L5  τ ← M(q) a_q + C(q, q') q' + g(q) - J(q)ᵀ F_ext
L6  return τ
```

Lines L4 and L5 are [computed-torque control](/computed-torque-control/) toward the acceleration $a_x$. The term $-J^T F_{\text{ext}}$ in line L5 cancels the measured contact force, and line L3 puts it back, scaled by $M_d^{-1}$. If the target mass is not changed ($M_d$ equal to the task-space inertia of the arm), the force sensor is not needed, and the law reduces to

$$\tau = J(q)^T\big(K_d(x_0 - x) - D_d\dot x\big) + g(q)$$

for a fixed goal. This simple form is the one most often used on torque-controlled arms. It is [PD control with gravity compensation](/pd-control-with-gravity-compensation/) with the spring and damper placed in task space.

## Example

Take the planar 2R arm with $L_1 = L_2 = 1$ m and point masses of 1 kg at the link ends, in a vertical plane with gravity along $-y$. A frictionless wall fills $x \ge 1$ m and acts as a stiff spring, $F_{\text{ext}} = (-k_e(x - 1), 0)$ for $x > 1$ with $k_e = 10^4$ N/m. The targets are $M_d = I$ kg, $K_d = 400 I$ N/m and $D_d = 40 I$ N s/m, which is critical damping. The arm starts at rest with its end point at $(0.9, 0.5)$ m, and the goal is fixed at $x_0 = (1.05, 0.5)$, 5 cm inside the wall.

At the start, $\tilde x = (-0.15, 0)$, so line L3 gives $a_x = (60, 0)$ m/s$^2$ and lines L4 and L5 give $\tau = (-10.38, -59.64)$ N m. The table shows a simulation with RK4 and a step of 1 ms.

| time (s) | end point $x$ (m) | wall force (N) |
|---|---|---|
| 0.100 | 0.98910 | 0 |
| 0.115 | first contact | 0 |
| 0.131 | peak | 67.5 |
| 0.200 | 1.00321 | 32.1 |
| 0.500 | 1.00192 | 19.24 |
| 1.500 | 1.0019231 | 19.231 |

At rest the target equation gives $K_d\tilde x = F_{\text{ext}}$. Together with the wall law this gives the rest position $x = (K_d x_0 + k_e x_w)/(K_d + k_e) = 1.0019231$ m and the contact force

$$\frac{k_e K_d}{k_e + K_d}(x_0 - x_w) = \frac{10^4 \cdot 400}{10400} \cdot 0.05 = 19.231 \text{ N}.$$

The force is that of the target spring and the wall spring in series. The impact peak of 67.5 N is set by the target mass and the speed at contact, not by the spring alone. The $y$ coordinate stays at 0.5 m within $10^{-9}$ m during the whole motion, because the target matrices are diagonal and the law cancels the arm's own inertia. The simple law without a force sensor reaches the same rest force, but its $y$ coordinate moves by up to 1.8 mm during the impact, because the arm's inertia couples the two directions.

## Correctness

The claim is: with an exact model, a nonsingular $J(q)$ and an exact force measurement, the closed loop satisfies $M_d\ddot{\tilde x} + D_d\dot{\tilde x} + K_d\tilde x = F_{\text{ext}}$ for every force $F_{\text{ext}}$. Putting line L5 into the arm equation, the $C$, $g$ and $J^T F_{\text{ext}}$ terms cancel, so $\ddot q = a_q$. Then $\ddot x = J\ddot q + \dot J\dot q = a_x$ by line L4, and line L3 rearranges to the target equation. For a passive environment and a fixed goal, the energy $\tfrac12\dot{\tilde x}^T M_d\dot{\tilde x} + \tfrac12\tilde x^T K_d\tilde x$ plus the energy stored in the environment does not grow, which bounds the motion and the contact force. The full proof, including the rest force against a spring wall, is in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, with $n$ joints and a task of dimension $n$:

- Lines L1 and L2 need the forward kinematics and the [geometric Jacobian](/geometric-jacobian/). For a serial chain, the joint frames take $O(n)$ operations and the $n \times n$ Jacobian then takes $O(n^2)$.
- Line L4 solves a linear system with $J$, which takes $O(n^3)$ operations by Gaussian elimination.
- Line L5 is one inverse dynamics call, $O(n)$ with the recursive Newton-Euler algorithm, plus $J^T F_{\text{ext}}$ in $O(n^2)$.

So one step costs $O(n^3)$ time and $O(n^2)$ memory. For a 6-joint arm this is a fixed small number of operations. The law without a force sensor needs only $J^T$ times a vector and the gravity torque, which is $O(n^2)$.

## Properties

- **Bounded contact force.** At rest against a spring-like surface, the force is $k_e K_d/(k_e + K_d)$ times the depth of the goal inside the surface, so it is at most $K_d$ times that depth, whatever the stiffness of the surface.
- **One law for free motion and contact.** No switching is needed when contact starts or ends. This is the main practical advantage over [hybrid position/force control](/hybrid-position-force-control/).
- **Passivity.** The simple law makes the arm a passive system seen from the contact point. Coupled to any passive environment, the system stays stable, which is not true for most position or force controllers.
- **No force tracking.** The force is not controlled directly. It follows from the depth of the goal and the stiffness of the environment, and it changes if the surface is not where the model says.

## Variants and improvements

- **Without inertia shaping.** If $M_d$ is the natural task-space inertia $\Lambda(q) = (J M^{-1} J^T)^{-1}$, no force sensor is needed. This is the simple law above, also called compliance control or Cartesian stiffness control when the target mass is ignored.
- **Admittance control.** On an arm with stiff position servos and no torque control, measure the force, integrate the target dynamics to get a reference motion, and send it to the position loop. See [admittance control](/admittance-control/).
- **Orientation.** For rotations the spring needs care: a spring on Euler angles depends on the chosen angles. Springs on the axis-angle error, or on the rotation matrix, give a stiffness that does not depend on the coordinates.
- **Redundant arms.** With more joints than task directions, the [operational space formulation](/operational-space-formulation/) gives the task impedance and leaves a null space for a second task.
- **Variable impedance.** The stiffness and damping can change with time or with the task phase, but a changing stiffness can inject energy and needs its own stability check.

## When to use it

Use it whenever the robot touches its environment and the position of the contact surface is uncertain: assembly such as [peg-in-hole](/peg-in-hole/) insertion, polishing, opening doors, and physical work with people. It needs a torque-controlled arm or at least a joint torque interface. For an arm with only position control, use admittance control. When a precise contact force must be held, combine it with an explicit force loop or use [hybrid position/force control](/hybrid-position-force-control/).

## Pitfalls

- **Stiff environments and impact.** The impact force depends on the target mass and the approach speed. A small target mass needs a fast inner loop and accurate force measurement; with a slow loop or noisy sensors, a small $M_d$ against a stiff wall can make the contact unstable.
- **Model errors.** The full law cancels the inertia of the arm. Errors in the model or in the force measurement leave the target equation only approximately true, and friction in the joints hides small forces.
- **Singularities.** Line L4 needs $J^{-1}$, which does not exist at a [kinematic singularity](/kinematic-singularity/). Near one, the joint torques grow large for a small task force.
- **Coordinates of the spring.** A diagonal stiffness in one frame is not diagonal in another. Choose the frame in which the task has natural directions, such as the normal of the surface.
- **Goal inside the obstacle.** The contact force is set by how far the goal lies inside the surface. A goal far inside a stiff surface gives a large force; plan the goal with the surface position in mind.

## Implementations

## History

Robot force control had several schemes by the early 1980s, such as stiffness control, damping control and the hybrid scheme of Raibert and Craig, and Mason described compliant motion with natural and artificial constraints in 1981. Neville Hogan published "Impedance control: an approach to manipulation" in three parts in the Journal of Dynamic Systems, Measurement, and Control in March 1985. He argued that a manipulator interacts with its environment as a physical system, so the controller should set its impedance, and that the robot should look like an impedance because the environment usually looks like an admittance. The idea became the base of most later interaction control, including the control of collaborative robots.

## References
