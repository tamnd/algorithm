---
tag: Y618J7
kind: problem
slug: forward-kinematics
name: Forward kinematics
aliases:
- direct kinematics
area: robotics/robot-kinematics
level: intro
summary: Given the joint values of a robot, compute the pose of its end effector. For an open chain this is a product of one transform per joint, O(n) operations by the product of exponentials.
prereqs: [kinematic-chain, homogeneous-transformation-matrix]
see_also: [product-of-exponentials-formula, denavit-hartenberg-convention, inverse-kinematics, robot-workspace, stewart-gough-forward-kinematics, space-and-body-jacobian, vector-loop-closure, real-ram]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 4, Forward Kinematics (Section 4.1, the product of exponentials in the space and the body form), and Appendix C, Denavit-Hartenberg parameters
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.8, Direct Kinematics (2.8.1 open chain, 2.8.2 Denavit-Hartenberg convention, 2.8.3 closed chain), and Section 2.9, kinematics of typical manipulator structures
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 3, Manipulator Kinematics, the section on forward kinematics with the product of exponentials
  - paper: doi:10.1007/BFb0031048
    title: R. W. Brockett, Robotic manipulators and the product of exponentials formula, in P. A. Fuhrmann (editor), Mathematical Theory of Networks and Systems, Lecture Notes in Control and Information Sciences 58, Springer, 1984
    locator: pages 120 to 129, the product of exponentials form of the forward kinematics
  - paper: doi:10.1115/1.4011045
    title: J. Denavit and R. S. Hartenberg, A kinematic notation for lower-pair mechanisms based on matrices, Journal of Applied Mechanics 22, 1955
    locator: pages 215 to 221, the four parameters per joint and the matrix product along the chain
---

Forward kinematics asks where the end of a robot is when its joint values are known. The input is the angle of each revolute joint and the travel of each prismatic joint. The output is the position and the orientation of the end effector, as a $4 \times 4$ [homogeneous transformation matrix](/homogeneous-transformation-matrix/). For an open [kinematic chain](/kinematic-chain/), such as a serial arm, the answer is a product of one transform per joint and takes $O(n)$ arithmetic operations for $n$ joints. For a closed chain, such as a parallel robot, the same question asks for the solution of loop equations and is much harder. The reverse question is [inverse kinematics](/inverse-kinematics/).

## In plain words

A robot arm is a row of rigid parts with a motor at each joint. Each motor reports how far it has turned. Forward kinematics turns these readings into the place and the direction of the gripper.

You can do it one joint at a time. Start at the base. The first joint turns everything after it. The second joint turns everything after it, and so on. Each step is a fixed move along a link followed by the move of one joint. After the last joint you know where the gripper is.

For an arm with one chain of joints there is always exactly one answer, and the work grows in proportion to the number of joints. For a robot whose gripper is held by several chains at once, the motor readings alone do not give the answer directly, and there can be many answers.

## Definition

**Robot model.** An open chain robot has $n$ one-freedom joints, revolute or prismatic, with joint values $q = (q_1, \dots, q_n) \in \mathbb{R}^n$. A fixed frame $\{s\}$ is on the base and a frame $\{b\}$ is on the end effector. The model is given in one of two standard forms:

- a list of screw axes $\mathcal{S}_1, \dots, \mathcal{S}_n$ in $\{s\}$ and the home pose $M \in SE(3)$ at $q = 0$, for the [product of exponentials](/product-of-exponentials-formula/), or
- a table of [Denavit-Hartenberg parameters](/denavit-hartenberg-convention/) $(\theta_i, d_i, a_i, \alpha_i)$ and a fixed tool transform.

**Input.** The model and a joint vector $q$.

**Output.** The pose $T_{sb}(q) \in SE(3)$ of $\{b\}$ in $\{s\}$:

$$T_{sb}(q) = e^{[\mathcal{S}_1] q_1} e^{[\mathcal{S}_2] q_2} \cdots e^{[\mathcal{S}_n] q_n} M .$$

The map $q \mapsto T_{sb}(q)$ is the **forward kinematics map**. Its derivative is the Jacobian, which maps joint velocities to the end effector twist (see [space and body Jacobian](/space-and-body-jacobian/)).

For an open chain the problem always has exactly one answer, because the right side is a function of $q$. For a closed chain, the input is only the values of the actuated joints, and the output is every pose of the end effector that is consistent with them and with the loop closure equations. That version can have several answers or none.

## Variants

| variant | input | output | status |
|---|---|---|---|
| serial open chain | all $n$ joint values | one pose | closed form, $O(n)$ |
| tree, such as a hand or a humanoid | all joint values | one pose per leaf | closed form, $O(n)$ for all leaves |
| position only | all joint values | the end effector point | closed form, $O(n)$ |
| velocity forward kinematics | $q$ and $\dot q$ | the twist $J(q)\dot q$ | closed form, $O(n)$ for the twist |
| closed chain or parallel robot | actuated joint values only | all consistent poses | polynomial system; up to 40 poses for the general [Stewart-Gough platform](/stewart-gough-forward-kinematics/) |
| planar four-bar | input crank angle | coupler and rocker angles | two solutions, from the [vector loop closure](/vector-loop-closure/) |

## Examples

**A planar 2R arm.** Two revolute joints with vertical axes, links of length $L_1 = L_2 = 1$ m. The end point is at

$$x = L_1\cos q_1 + L_2\cos(q_1 + q_2), \qquad y = L_1\sin q_1 + L_2\sin(q_1 + q_2),$$

and the gripper points in the direction $q_1 + q_2$. At $q = (0, \pi/2)$ the end point is at $(1, 0) + (0, 1) = (1, 1)$ m and the heading is $\pi/2$, so

$$T_{sb} = \begin{pmatrix} 0 & -1 & 0 & 1 \\ 1 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}.$$

In product of exponentials form, $\mathcal{S}_1 = (0, 0, 1, 0, 0, 0)$, $\mathcal{S}_2 = (0, 0, 1, 0, -1, 0)$ (an axis through $(1, 0, 0)$) and $M$ is the translation by $(2, 0, 0)$. The second exponential turns the point $(2, 0)$ by $\pi/2$ about $(1, 0)$, which gives $(1, 1)$, and the first one is the identity. A script that compared this with the Denavit-Hartenberg product $A_1 A_2$ at 1000 random joint vectors found a largest difference of $9 \times 10^{-16}$ in any entry.

**The order matters.** At $q = (\pi/2, \pi/2)$, $e^{[\mathcal{S}_1]\pi/2} e^{[\mathcal{S}_2]\pi/2} M$ has the end point at $(-1, 1)$, which is right: $x = \cos(\pi/2) + \cos\pi = -1$ and $y = \sin(\pi/2) + \sin\pi = 1$. The product in the other order gives $(-1, -1)$. The joint transforms do not commute, and the product must follow the chain from the base out.

**A spatial 3R arm.** The first axis is vertical, the second and third are horizontal, as in the shoulder and elbow of an industrial arm. With a shoulder height of 1 m and two links of 1 m, the point is at $p = (\cos q_1\, r, \ \sin q_1\, r, \ 1 + \sin q_2 + \sin(q_2 + q_3))$ with $r = \cos q_2 + \cos(q_2 + q_3)$. At $q = (\pi/2, 0, \pi/2)$, $r = 1$ and $p = (0, 1, 2)$ m. The [Denavit-Hartenberg convention](/denavit-hartenberg-convention/) page gives the table of this arm.

## Known algorithms

All costs are counts of arithmetic operations and of sine and cosine calls in the [real RAM](/real-ram/) model, for a serial chain with $n$ joints.

| method | cost | notes |
|---|---|---|
| [product of exponentials](/product-of-exponentials-formula/), space or body form | $O(n)$ | one exponential (by [Rodrigues' formula](/rodrigues-rotation-formula/)) and one $4 \times 4$ product per joint; no link frames needed |
| [Denavit-Hartenberg](/denavit-hartenberg-convention/) product $A_1 \cdots A_n$ | $O(n)$ | one closed form $4 \times 4$ matrix per joint, with 4 parameters per link |
| poses of all links at once | $O(n)$ | keep the partial products; the same prefix products give the columns of the space Jacobian |
| closed chain: Newton's method on the loop equations | per iteration, a Jacobian and a linear solve | local convergence from a good start; used to track a parallel robot in real time |
| closed chain: elimination or [homotopy continuation](/homotopy-continuation/) | fixed for a fixed design | finds all solutions; see [Stewart-Gough forward kinematics](/stewart-gough-forward-kinematics/) |

The product of exponentials and the Denavit-Hartenberg product give the same matrix for the same arm. They differ in how the model is written down and how easy it is to change, which matters for [kinematic calibration](/kinematic-calibration/).

## Bounds

- **Upper bound.** $O(n)$ operations for an open chain, by either product. The constant is a fixed number of multiplications per joint.
- **Lower bound.** $\Omega(n)$ in general, because the pose depends on every joint value, so an algorithm must read all $n$ inputs.
- **Number of solutions.** One for an open chain. For a closed chain the number depends on the design: 2 for a planar four-bar with a given crank angle, and up to 40 complex solutions for the general Stewart-Gough platform, all 40 of which can be real.

## Reductions

- **To matrix products.** Open chain forward kinematics is a product of $n$ elements of $SE(3)$, so it is a prefix product over a group, and the partial products can be computed in parallel with a scan.
- **From closed chains to polynomial systems.** Write each joint angle by $c = \cos q$, $s = \sin q$ with $c^2 + s^2 = 1$, or by $t = \tan(q/2)$. The loop equations become polynomial equations, which [polynomial system solving](/polynomial-system-solving/), resultants or homotopy continuation can solve.
- **Inside other problems.** [Inverse kinematics](/inverse-kinematics/) by Newton's method evaluates the forward map and its Jacobian at each step. [Kinematic calibration](/kinematic-calibration/) fits the parameters of the forward map to measured poses.

## Applications

Every robot controller evaluates forward kinematics many times a second, to show the tool position, to check limits, and to close loops in task space. Collision checking in [motion planning](/motion-planning/) needs the poses of all links, which the partial products give. Computer animation uses the same product on the skeleton of a character. Machine tools with five axes and coordinate measuring arms use it to map axis readings to the tool or probe position.

## References
