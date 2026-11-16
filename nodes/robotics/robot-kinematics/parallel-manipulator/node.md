---
tag: 4MW7GX
kind: definition
slug: parallel-manipulator
name: Parallel manipulator
aliases:
- parallel robot
- closed-chain manipulator
area: robotics/robot-kinematics
level: core
summary: A robot whose end effector is joined to the base by two or more chains, as in the Stewart-Gough platform or the Delta robot. Inverse kinematics is easy and forward kinematics is hard.
prereqs: [kinematic-chain, grubler-formula]
see_also: [stewart-gough-forward-kinematics, grubler-formula, kinematic-singularity, robot-workspace, forward-kinematics, inverse-kinematics, kinematic-calibration, kinematic-chain]
sources:
  - book: isbn:9781402041327
    title: J.-P. Merlet, Parallel Robots, 2nd edition, Springer, 2006
    locator: the definition of a parallel robot in the introduction, and the chapters on inverse kinematics, direct kinematics, singular configurations and calibration (general locator)
  - paper: doi:10.1109/70.56660
    title: C. Gosselin and J. Angeles, Singularity analysis of closed-loop kinematic chains, IEEE Transactions on Robotics and Automation 6(3), 1990
    locator: pages 281 to 290, the three types of singularity from the two Jacobian matrices of the input-output equation
  - paper: doi:10.1243/PIME_PROC_1965_180_029_02
    title: D. Stewart, A platform with six degrees of freedom, Proceedings of the Institution of Mechanical Engineers 180(1), 1965
    locator: pages 371 to 386, the platform for flight simulation, with the discussion in which V. E. Gough describes his earlier tyre testing machine
  - book: "Reymond Clavel, DELTA, a fast robot with parallel geometry, Proceedings of the 18th International Symposium on Industrial Robots, Lausanne, IFS Publications, 1988"
    locator: pages 91 to 100, the Delta robot with three parallelogram legs and three translational freedoms
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 7, Kinematics of Closed Chains (inverse and forward kinematics of parallel mechanisms and their singularities)
---

A parallel manipulator is a robot whose moving platform, the part that carries the tool, is joined to the fixed base by two or more separate chains of links, the legs. Each leg usually has one motor, and the motors together set the pose of the platform. The legs share the load, so a parallel robot can be stiff, light and fast, and its workspace is small for its size. A serial arm is the opposite case, with one chain from the base to the tool. The kinematics are also the reverse of a serial arm: from a given pose of the platform, the motor values follow leg by leg, but from given motor values, the pose of the platform must be found by solving the loop equations of a closed [kinematic chain](/kinematic-chain/).

## Definition

**Parallel manipulator.** A parallel manipulator is a mechanism made of a fixed base, a moving platform with $d$ degrees of freedom ($d \le 6$), and $k \ge 2$ open chains, the **legs**, each of which joins the base to the platform. No two legs share a link other than the base and the platform. Some joints are **actuated** (driven by motors) and the others are **passive**. Merlet (2006) uses this definition in his book.

A parallel manipulator is **fully parallel** if it has $k = d$ legs with one actuated joint in each. Legs are named by their joints from the base up, with the actuated joint underlined in some texts: a UPS leg has a universal joint at the base, an actuated prismatic joint, and a spherical joint at the platform.

**Its kinematics.** Let $\theta \in \mathbb{R}^d$ be the actuated joint values and $x$ the pose of the platform. The loop closure of each leg, after the passive joints are eliminated, gives the input-output equations $F(x, \theta) = 0$.

- **Inverse kinematics**: from $x$, find $\theta$. Each leg is solved on its own, often in closed form.
- **Forward kinematics**: from $\theta$, find $x$. All the equations must be solved together, and there are often several solutions. See [forward kinematics of the Stewart-Gough platform](/stewart-gough-forward-kinematics/).

**Singularities.** Differentiating $F(x, \theta) = 0$ gives $A\,\dot x + B\,\dot\theta = 0$, with $A = \partial F / \partial x$ and $B = \partial F / \partial \theta$. Gosselin and Angeles (1990) defined three types of singular configuration:

1. $B$ is singular: some actuator velocity $\dot\theta \ne 0$ gives no platform motion, and the platform loses a freedom. This is often a leg at the edge of its own workspace.
2. $A$ is singular: some platform velocity $\dot x \ne 0$ is possible while all actuators are locked. The platform gains a freedom that the motors cannot control, and it cannot resist some loads. This type does not occur in a serial arm.
3. Both are singular.

## Examples and non-examples

**The Stewart-Gough platform.** Six UPS legs join a base to a platform. Each leg length is the distance between its two end points, $\ell_i = |p + R b_i - a_i|$, where $a_i$ is the base point, $b_i$ the platform point in the platform frame and $(R, p)$ the pose of the platform. So inverse kinematics is six distance computations. Grübler's count is $6(14 - 1 - 18) + 36 = 6$. Forward kinematics has up to 40 solutions. Flight simulators, machine tools and positioners for telescopes use this design.

**The Delta robot.** Clavel (1988) joined a platform to the base by three legs. Each leg has a motor at the base that turns an arm, and a parallelogram of four ball joints from the arm to the platform. The three parallelograms keep the platform parallel to the base, so it has three translational freedoms. Delta robots are common in fast pick and place lines.

**A planar 3-RPR robot, worked by hand.** Base points $B_1 = (0, 0)$, $B_2 = (4, 0)$, $B_3 = (0, 4)$ m. Platform points in the platform frame $b_1 = (0, 0)$, $b_2 = (1, 0)$, $b_3 = (0, 1)$ m. Each leg has a revolute joint at the base, an actuated prismatic joint and a revolute joint at the platform. Grübler's count is $3(8 - 1 - 9) + 9 = 3$, the position and the heading of the platform.

- Pose $p = (1, 1)$, heading $\varphi = \pi/2$. The platform points are $(1, 1)$, $(1, 2)$ and $(0, 1)$, and the leg lengths are $\sqrt{2} = 1.4142$, $\sqrt{3^2 + 2^2} = \sqrt{13} = 3.6056$ and $3$ m. This is inverse kinematics, solved leg by leg.
- Pose $p = (1, 1)$, heading $\varphi = 0$. The platform points are $(1, 1)$, $(2, 1)$ and $(1, 2)$, and the leg lengths are $\sqrt{2}$, $\sqrt{5}$ and $\sqrt{5}$ m. The three leg lines meet at the point $(4/3, 4/3)$. A small turn of the platform about that point moves each platform point at right angles to its leg, so to first order no leg length changes: this is a singularity of type 2. In fact every pose with $\varphi = 0$ is singular for this design, because the platform triangle is then a scaled copy of the base triangle, and the leg lines all pass through the center of that scaling. At $\varphi = \pi/2$ the lines of legs 1 and 3 meet at $(0, 0)$, which is not on the line of leg 2, so that pose is not singular of type 2.

**Non-example: a serial arm with a parallelogram.** Some palletizing arms drive the elbow through a parallelogram linkage. The arm contains a closed loop, but the tool is held by one chain, so the arm is a serial robot with a closed sub-chain, not a parallel manipulator.

**Non-example: a serial arm.** A serial arm has $k = 1$ chain. Its forward kinematics is a product of transforms with one answer, and its inverse kinematics can have many answers.

## Related definitions

- [Kinematic chain](/kinematic-chain/): a parallel manipulator is a closed chain with $L = J - N + 1 \ge 1$ loops.
- [Grübler's formula](/grubler-formula/): counts the freedoms of the platform, with care for idle freedoms such as the spin of an SPS leg.
- [Forward kinematics of the Stewart-Gough platform](/stewart-gough-forward-kinematics/): the hard direction for the best known parallel robot.
- [Kinematic singularity](/kinematic-singularity/): for a serial arm only the analog of type 1 exists.
- [Robot workspace](/robot-workspace/): for a parallel robot it is limited by the leg lengths, the joint ranges and collisions between the legs.
- [Kinematic calibration](/kinematic-calibration/): parallel robots can be calibrated from leg length readings and loop constraints.

### History

Gough built a platform with six legs of variable length in the 1950s to test tyres, and Stewart (1965) proposed a six-freedom platform for flight simulators, with Gough's machine described in the published discussion of the paper. The name Stewart-Gough platform credits both. Clavel (1988) introduced the Delta robot. Gosselin and Angeles (1990) gave the classification of singularities, and Merlet's book is the standard survey of the field.

## References
