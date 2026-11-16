---
tag: 7J4453
kind: model
slug: flexible-joint-model
name: Flexible joint model
aliases:
- Spong elastic joint model
area: robotics/robot-dynamics
level: advanced
summary: A robot model with a torsional spring between each motor and its link, so the state has link and motor positions; Spong's reduced form assumes the rotor energy comes from its own spin only.
prereqs: [euler-lagrange-manipulator-dynamics, manipulator-equation]
see_also: [feedback-linearization, singular-perturbation-method, pd-control-with-gravity-compensation, passivity-based-control, backstepping, input-output-linearization, impedance-control, computed-torque-control]
sources:
  - paper: doi:10.1115/1.3143860
    title: Mark W. Spong, Modeling and control of elastic joint robots, Journal of Dynamic Systems, Measurement, and Control 109(4), 1987
    locator: pages 310 to 318
  - paper: doi:10.1109/9.90238
    title: Patrizio Tomei, A simple PD controller for robots with elastic joints, IEEE Transactions on Automatic Control 36(10), 1991
    locator: pages 1208 to 1213
  - paper: doi:10.1109/JRA.1987.1087102
    title: Mark W. Spong, Khashayar Khorasani and Petar V. Kokotovic, An integral manifold approach to the feedback control of flexible joint robots, IEEE Journal of Robotics and Automation 3(4), 1987
    locator: pages 291 to 300
  - paper: doi:10.1109/ROBOT.1998.677024
    title: Alessandro De Luca and Pasquale Lucibello, A general algorithm for dynamic feedback linearization of robots with elastic joints, IEEE International Conference on Robotics and Automation, 1998
    locator: pages 504 to 510
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 11, Robots with Flexible Elements, by Alessandro De Luca and Wayne J. Book, pages 243 to 282"
---

The flexible joint model describes a robot whose joints are not rigid: between each motor and the link it drives there is a torsional spring, which stands for the elasticity of a harmonic drive, a belt or a torque sensor. The model has two positions per joint, one for the link and one for the motor, and so twice the state of a rigid robot. Spong (1987) gave the reduced form used in most control work, under the assumption that the kinetic energy of each rotor comes from its own spin only.

## The machine

**State.** The link positions $q_1 \in \mathbb{R}^n$ (rad), the motor positions $q_2 \in \mathbb{R}^n$ (rad, the motor angle divided by the gear ratio, so that $q_1 = q_2$ when the spring is at rest), and their velocities. The state has dimension $4n$.

**Input.** The motor torques $u \in \mathbb{R}^n$ (N m), referred to the link side of the gear.

**Parameters.** The link dynamics $M(q_1)$, $C(q_1, \dot q_1)$ and $g(q_1)$ of the rigid robot, the diagonal joint stiffness matrix $K$ (N m/rad), and the diagonal matrix $J$ of the rotor inertias reflected through the gears (kg m$^2$, the rotor inertia times the square of the gear ratio).

**Assumptions** (Spong 1987).
1. Each joint is a linear torsional spring between the motor and the link, with no damping and no backlash.
2. Each rotor is a uniform body with its center of mass on its axis, so the gravity and the inertia of the robot do not depend on the motor positions.
3. The kinetic energy of each rotor is due only to its own spin about its axis. The part that comes from the motion of the links that carry the rotor is neglected. This is a good approximation for large gear ratios.

**Equations.** With these assumptions, the Euler-Lagrange equations are
$$M(q_1)\ddot q_1 + C(q_1, \dot q_1)\dot q_1 + g(q_1) + K(q_1 - q_2) = 0,$$
$$J \ddot q_2 - K(q_1 - q_2) = u .$$
The links feel the motors only through the spring torque $K(q_2 - q_1)$, and the motors feel the links only through the same torque. Without assumption 3, the model has an inertia coupling term $S(q_1)\ddot q_2$ in the link equation and $S(q_1)^T \ddot q_1$ in the motor equation; this is the complete model.

## What it counts

**Motion.** Given $u(t)$ and the initial state, the model gives the link and motor trajectories, including the vibration of the links against the motors.

**Energy.** The total energy is
$$E = \tfrac12 \dot q_1^T M(q_1) \dot q_1 + \tfrac12 \dot q_2^T J \dot q_2 + \tfrac12 (q_1 - q_2)^T K (q_1 - q_2) + U_g(q_1),$$
with the potential $U_g$ of gravity, $g = \partial U_g / \partial q_1$. Along every motion $\dot E = \dot q_2^T u$: the motors are the only source of energy, and the map from $u$ to $\dot q_2$ is passive.

**Static deflection.** At rest, $K(q_1 - q_2) = -g(q_1)$. To hold the link at $q_1$, the motor must be at $q_2 = q_1 + K^{-1} g(q_1)$, and its torque is $u = g(q_1)$. A link of mass $m$ with its center of mass at the distance $l$, held horizontal with $m g l = 9.81$ N m on a joint with $K = 100$ N m/rad, deflects by $0.0981$ rad, about 5.6 degrees.

**Vibration.** For one joint with no gravity, a link inertia $I = 1$ kg m$^2$, $J = 0.5$ kg m$^2$ and $K = 100$ N m/rad: with the motor held still, the link oscillates at $\sqrt{K / I} = 10$ rad/s. With the motor free ($u = 0$), the link and the motor swing against each other at $\sqrt{K (1/I + 1/J)} = \sqrt{300} \approx 17.32$ rad/s, and their common rotation is a free motion with the inertia $I + J$.

## Relation to other models

- **The rigid robot.** As $K \to \infty$, $q_1 - q_2 \to 0$, and the model tends to the [manipulator equation](/manipulator-equation/) with the inertia $M(q) + J$ and the input $u$. The model is a singular perturbation of the rigid model, with the small parameter $1/\sqrt{k}$ for a common stiffness scale $k$; see the [singular perturbation method](/singular-perturbation-method/).
- **The complete model.** Without assumption 3, the coupling $S(q_1)$ is strictly upper triangular for a serial robot. It changes the control results below; with $S = 0$ it is the reduced model.
- **Series elastic actuators.** A spring placed on purpose between motor and load has the same equations. Variable stiffness actuators make $K$ a function of a second motor.
- **Flexible links.** Elastic links have distributed deformation and need many modes or a partial differential equation, not one spring per joint.
- **Joint friction and damping.** A damping term $D(\dot q_1 - \dot q_2)$ in parallel with the spring, and motor friction in the motor equation, are common extensions.

## Known results in the model

- **Feedback linearization (theorem).** The reduced model is linearizable by static state feedback, with the link positions as outputs. Each output has relative degree 4: $q_1^{(4)}$ is the first derivative of $q_1$ in which $u$ appears, through $\ddot q_2$, and the map from $u$ to $q_1^{(4)}$ has the invertible matrix $M(q_1)^{-1} K J^{-1}$ (Spong 1987). See [feedback linearization](/feedback-linearization/) and [input-output linearization](/input-output-linearization/).
- **The complete model.** With the coupling term, static feedback no longer linearizes the model in general. De Luca and Lucibello (1998) gave an algorithm that linearizes it by dynamic feedback.
- **PD regulation (theorem).** A PD law on the motor positions with constant gravity compensation, $u = K_P(\bar q_2 - q_2) - K_D \dot q_2 + g(\bar q_1)$ with $\bar q_2 = \bar q_1 + K^{-1} g(\bar q_1)$, makes the rest point $(\bar q_1, \bar q_2)$ globally asymptotically stable if the joint stiffness and the gain $K_P$ are large enough compared with a bound on the gradient of $g$ (Tomei 1991). It uses only motor measurements. Compare [PD control with gravity compensation](/pd-control-with-gravity-compensation/) for the rigid robot.
- **Singular perturbation.** For stiff joints, the motion splits into a slow rigid motion and fast spring oscillations; a control designed for the rigid model plus a corrective term computed on an integral manifold of the slow motion gives tracking for stiff enough joints (Spong, Khorasani and Kokotovic 1987).
- **Passivity and backstepping.** The passive map from $u$ to $\dot q_2$ is the basis of [passivity-based control](/passivity-based-control/) of elastic joint robots, and the cascade of the link and motor equations suits [backstepping](/backstepping/).

## References
