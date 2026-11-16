---
tag: MTVMY0
kind: theorem
slug: jacobian-statics-duality
name: Jacobian statics duality
aliases:
- force-velocity duality
- joint torques from end effector wrench
area: robotics/robot-kinematics
level: core
summary: By virtual work, the joint torques that balance an end effector wrench F are J^T F, the transpose of the velocity map.
prereqs: [space-and-body-jacobian, wrench]
see_also: [geometric-jacobian, kinematic-singularity, manipulability-ellipsoid, jacobian-transpose-method, manipulator-equation, small-displacement-torsor, rigidity-matrix, grasp-matrix]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.2 (statics of open chains, tau = J^T F by power balance, in the space and in the body frame)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.8 (statics, the principle of virtual work and the kineto-statics duality of the range and null spaces)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 3 (end effector forces and the transpose of the manipulator Jacobian)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, 2nd edition, Wiley, 2020
    locator: Chapter 4 (the manipulator Jacobian and the relation between end effector forces and joint torques)
---

For a robot arm at rest, the joint torques $\tau$ that hold a [wrench](/wrench/) $\mathcal F$ (a force and a moment) at the end effector are $\tau = J(q)^{\mathsf T}\mathcal F$, where $J(q)$ is the Jacobian that maps joint velocities to the end effector twist.
The same matrix that maps joint motion to tip motion, transposed, maps tip load to joint load; the proof is one line of the principle of virtual work.
The result needs $J$ and $\mathcal F$ in the same frame, ideal joints, and no gravity, or gravity added as a separate term.
In computer aided design, the same pairing of small motions and loads appears as the [small displacement torsor](/small-displacement-torsor/), and in rigidity theory the [rigidity matrix](/rigidity-matrix/) and its transpose play the two roles.

## Statement

**Setting.** A serial chain has rigid links and $n$ joints, each revolute or prismatic, with the joint values $q \in \mathbb{R}^n$.
The joints are ideal: the joint mechanism does no work, so the only generalized force along joint $i$ is the actuator force or torque $\tau_i$.
The arm is at rest, $\dot q = 0$ and $\ddot q = 0$, and gravity is not acting (or is treated below).
Twists are $\mathcal V = (\omega, v)$ and wrenches are $\mathcal F = (m, f)$, moment first, in the same frame, so that the power of $\mathcal F$ on $\mathcal V$ is $\mathcal V^{\mathsf T}\mathcal F$.
Let $J_s(q)$ and $J_b(q)$ be the [space and body Jacobians](/space-and-body-jacobian/), with $\mathcal V_s = J_s \dot q$ and $\mathcal V_b = J_b \dot q$.
The end effector applies the wrench $\mathcal F$ to the environment, written $\mathcal F_s$ in the fixed frame {s} and $\mathcal F_b$ in the end effector frame {b}; the environment applies $-\mathcal F$ to the arm.

**Theorem.** The arm is in static equilibrium if and only if

$$\tau = J_s(q)^{\mathsf T}\mathcal F_s = J_b(q)^{\mathsf T}\mathcal F_b.$$

With gravity acting, the condition is $\tau = g(q) + J(q)^{\mathsf T}\mathcal F$, where $g(q)$ is the vector of joint torques that hold the arm against gravity.
With the [geometric Jacobian](/geometric-jacobian/) $J = (J_P, J_O)$, linear part first, the same statement holds with the wrench written as $(f, \mu)$, where $\mu$ is the moment about the end effector origin in base coordinates.

## In plain words

Push on the tip of a robot arm, and ask how hard each motor must push back to keep the arm still.
The answer comes from the motion of the arm, not from a new calculation.
If turning a joint a little moves the tip a lot in the direction of your push, then that joint must work hard.
If turning a joint does not move the tip along your push at all, that joint feels nothing.
The table of numbers that says how joint motion moves the tip, read the other way, says how tip load reaches the joints.
At a fully stretched pose, a pull along the arm reaches no motor, because no joint motion moves the tip along the arm.

## Proof

**By virtual work.** Fix $q$ and take any joint velocity $\dot q \in \mathbb{R}^n$ as a virtual velocity.
The links are rigid and the joints are ideal, so the only forces on the arm that do work in this motion are the actuator torques, with power $\tau^{\mathsf T}\dot q$, and the wrench $-\mathcal F_s$ of the environment, with power $-\mathcal V_s^{\mathsf T}\mathcal F_s$.
The principle of virtual work says that a system with ideal constraints is in equilibrium if and only if the total virtual power of the applied forces is zero for every virtual velocity that the constraints allow.
An open chain has no constraint on $\dot q$, so every $\dot q$ is allowed, and $\mathcal V_s = J_s \dot q$.
The condition is

$$\tau^{\mathsf T}\dot q - (J_s\dot q)^{\mathsf T}\mathcal F_s = (\tau - J_s^{\mathsf T}\mathcal F_s)^{\mathsf T}\dot q = 0 \quad \text{for all } \dot q \in \mathbb{R}^n,$$

which holds if and only if $\tau = J_s^{\mathsf T}\mathcal F_s$.

**By cutting the chain.** The same result follows from the equilibrium of rigid bodies, without the principle.
Cut the arm just before link $i$, and look at the subchain of links $i$ to $n$.
It is at rest, so the wrenches on it sum to zero.
The only external wrenches are $-\mathcal F_s$ at the end effector and the wrench $W_i$ that link $i - 1$ applies through joint $i$; the joint wrenches inside the subchain cancel in pairs.
So $W_i = \mathcal F_s$.
Joint $i$ allows the motion along its current screw axis, which is column $i$ of $J_s$.
An ideal joint transmits through its structure only wrenches with zero power along this axis, so the power of $W_i$ along the axis comes from the actuator alone: $J_{si}^{\mathsf T} W_i = \tau_i$.
Hence $\tau_i = J_{si}^{\mathsf T}\mathcal F_s$ for each $i$.

**The frame does not matter.** The body Jacobian is $J_b = \mathrm{Ad}_{T_{bs}} J_s$, and wrenches change frame with the transpose of the adjoint, $\mathcal F_b = \mathrm{Ad}_{T_{sb}}^{\mathsf T}\mathcal F_s$ (see the [adjoint map](/adjoint-map-se3/)).
So $J_b^{\mathsf T}\mathcal F_b = J_s^{\mathsf T}\mathrm{Ad}_{T_{bs}}^{\mathsf T}\mathrm{Ad}_{T_{sb}}^{\mathsf T}\mathcal F_s = J_s^{\mathsf T}(\mathrm{Ad}_{T_{sb}}\mathrm{Ad}_{T_{bs}})^{\mathsf T}\mathcal F_s = J_s^{\mathsf T}\mathcal F_s$, because $\mathrm{Ad}_{T_{sb}}\mathrm{Ad}_{T_{bs}} = \mathrm{Ad}_{I} = I$.
In the geometric form, $\dot p_e^{\mathsf T} f + \omega^{\mathsf T}\mu$ is the same power as $\mathcal V_s^{\mathsf T}\mathcal F_s$, so the same argument gives $\tau = J^{\mathsf T}(f, \mu)$.

**Gravity.** Gravity adds the potential energy $P(q)$, with virtual power $-\nabla P(q)^{\mathsf T}\dot q$ on the arm, so the condition becomes $\tau = g(q) + J^{\mathsf T}\mathcal F$ with $g = \nabla P$.
This is the [manipulator equation](/manipulator-equation/) $M\ddot q + C\dot q + g = \tau + J^{\mathsf T}\mathcal F_{ext}$ at $\dot q = \ddot q = 0$, with $\mathcal F_{ext} = -\mathcal F$.

## Consequences

**The 2R arm.** Take the planar 2R arm with $L_1 = L_2 = 1$ m at $q = (0, \pi/2)$, with the tip at $(1, 1)$ m and the linear Jacobian $J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}$.
A tip force $f = (1, 2)$ N needs $\tau = J^{\mathsf T} f = (-1 + 2, -1) = (1, -1)$ N m.
The moments check this: joint 1 at the origin feels $1 \cdot 2 - 1 \cdot 1 = 1$ N m, and joint 2 at $(1, 0)$, with the lever $(0, 1)$, feels $0 \cdot 2 - 1 \cdot 1 = -1$ N m.
In general, $\tau = (-f_x + f_y, -f_x)$ at this configuration.

**Range and null spaces.** For any matrix, the null space of $J^{\mathsf T}$ is the orthogonal complement of the range of $J$.
So the wrenches that need no joint torque are exactly the wrenches with zero power on every twist the arm can make.
At a [kinematic singularity](/kinematic-singularity/) both spaces are nonzero.
In the stretched 2R arm, $q_2 = 0$, the linear Jacobian is $\begin{pmatrix} 0 & 0 \\ 2 & 1 \end{pmatrix}$; the tip cannot move along the arm, and a pull $f = (1, 0)$ N along the arm needs $\tau = 0$: the structure holds it.

**Redundant arms.** If $n$ is larger than the task dimension, $J$ has a null space of joint motions that leave the tip still.
A torque that is not in the range of $J^{\mathsf T}$ cannot be balanced by any tip wrench; at rest it would move the arm in this null space.

**From torques to wrenches.** If $J$ is square and invertible, $\mathcal F = J^{-\mathsf T}\tau$ is the wrench that given motor torques produce.
If $J^{\mathsf T}$ is not injective, the wrench is fixed only up to its null space.

**Uses.** The [force ellipsoid](/manipulability-ellipsoid/) is the image of the unit ball of torques under this map, dual to the velocity ellipsoid.
The [Jacobian transpose method](/jacobian-transpose-method/) for inverse kinematics, and Jacobian transpose control, treat the task error as a virtual spring wrench and apply $J^{\mathsf T}$ to it.
In grasping, the [grasp matrix](/grasp-matrix/) is related in the same way to the map from object twists to contact velocities.

## Tightness

Each hypothesis is needed.

- **Gravity.** In a vertical plane, the 2R arm at $q = (0, \pi/2)$ with point masses of 1 kg at the link ends, gravity of 9.81 m/s^2 along $-y$ and no tip load needs $\tau = g(q) = (19.62, 0)$ N m, while $J^{\mathsf T}\mathcal F = 0$.
- **Ideal joints.** With Coulomb friction at the joints, equilibrium holds for a set of torques, $|\tau_i - (J^{\mathsf T}\mathcal F)_i| \le \tau_{f,i}$, and $\tau$ is no longer unique.
- **Rest.** When the arm moves, the inertial terms $M\ddot q + C\dot q$ of the manipulator equation add to the torques.
- **The same frame.** $J_s^{\mathsf T}\mathcal F_b$ is not the torque vector. In the 2R example, a tip force of 1 N along the $x$ axis of {s} is $\mathcal F_s = (0, 0, -1, 1, 0, 0)$ (the moment about the origin of {s} is $(1, 1, 0) \times (1, 0, 0)$), and the correct torques are $J_s^{\mathsf T}\mathcal F_s = (-1, -1)$ N m. In {b} the same force is $\mathcal F_b = (0, 0, 0, 0, -1, 0)$, and $J_b^{\mathsf T}\mathcal F_b = (-1, -1)$ N m as well, but the mixed product $J_s^{\mathsf T}\mathcal F_b = (0, 1)$ N m is wrong.
- **Open chains.** For a closed chain, such as a [parallel manipulator](/parallel-manipulator/), the joint velocities are not free; the loop constraints enter the virtual work argument with multipliers, and the actuated torques are not $J^{\mathsf T}\mathcal F$ for the open chain Jacobian of one leg.

## History

The principle of virtual work goes back to a letter of Johann Bernoulli to Varignon in 1717, and Lagrange made it the basis of statics in the Mécanique analytique of 1788.
The relation $\tau = J^{\mathsf T}\mathcal F$ is its form for a serial arm, and it is in all the standard robotics texts.
Lynch and Park derive it from power balance in both frames, and Siciliano et al. state the duality of the range and null spaces of $J$ and $J^{\mathsf T}$ under the name kineto-statics duality.

## References
