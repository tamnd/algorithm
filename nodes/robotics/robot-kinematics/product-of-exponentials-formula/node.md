---
tag: BAWKYM
kind: theorem
slug: product-of-exponentials-formula
name: Product of exponentials formula
aliases:
- PoE formula
- "Brockett's product of exponentials"
area: robotics/robot-kinematics
level: core
summary: For a serial chain, the end effector pose is e^[S1]q1 ... e^[Sn]qn M, with the joint screw axes S_i and the pose M taken at the home configuration. No link frames are needed.
prereqs: [forward-kinematics, se3-exponential-map]
see_also: [denavit-hartenberg-convention, screw-motion, rigid-body-twist, space-and-body-jacobian, adjoint-map-se3, matrix-exponential, kinematic-calibration, special-euclidean-group]
sources:
  - paper: doi:10.1007/BFb0031048
    title: R. W. Brockett, Robotic manipulators and the product of exponentials formula, in P. A. Fuhrmann (editor), Mathematical Theory of Networks and Systems, Lecture Notes in Control and Information Sciences 58, Springer, 1984
    locator: pages 120 to 129, the formula and its use for the kinematics of open chains
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 4, Section 4.1 (Section 4.1.1, the product of exponentials in the space frame, and the body form in the same section), and Chapter 5 for the space and body Jacobians
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 3, Manipulator Kinematics, the product of exponentials formula and its proof by moving the joints from the last to the first
---

The product of exponentials formula writes the [forward kinematics](/forward-kinematics/) of a serial robot as $T(q) = e^{[\mathcal{S}_1] q_1} \cdots e^{[\mathcal{S}_n] q_n} M$. Here $M$ is the pose of the end effector at a chosen home configuration $q = 0$, and $\mathcal{S}_i$ is the screw axis of joint $i$ at that home configuration, written in the fixed frame. Each factor is the [screw motion](/screw-motion/) of one joint, computed by the [exponential map of SE(3)](/se3-exponential-map/). The formula needs only the joint axes and one home pose, and no frame on each link. Brockett (1984) introduced it to robotics. The theorem holds only with the axes taken at the home configuration: if the home configuration changes, every $\mathcal{S}_i$ and $M$ change too.

## Statement

**Setting.** A serial chain has links $0$ (the fixed base) to $n$ and joints $1$ to $n$, where joint $i$ joins link $i - 1$ to link $i$ and has one freedom: revolute, prismatic or helical. The joint values are $q = (q_1, \dots, q_n)$, measured from a chosen home configuration $q = 0$. The fixed frame $\{s\}$ is on link 0 and the end effector frame $\{b\}$ is on link $n$. A twist is written $\mathcal{V} = (\omega, v)$ with the angular part first, and $[\mathcal{V}] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix}$, where $[\omega]$ is the skew-symmetric matrix with $[\omega]x = \omega \times x$.

**Data at the home configuration.**

- $M = T_{sb}(0) \in SE(3)$, the home pose of $\{b\}$.
- $\mathcal{S}_i = (\omega_i, v_i) \in \mathbb{R}^6$, the screw axis of joint $i$ in $\{s\}$ when $q = 0$. For a revolute joint, $\omega_i$ is the unit axis direction and $v_i = -\omega_i \times r_i$ for any point $r_i$ on the axis. For a helical joint of pitch $h_i$, $v_i = -\omega_i \times r_i + h_i\omega_i$. For a prismatic joint, $\omega_i = 0$ and $v_i$ is the unit direction of travel.

**Theorem (product of exponentials).** For every $q \in \mathbb{R}^n$,

$$T_{sb}(q) = e^{[\mathcal{S}_1] q_1} e^{[\mathcal{S}_2] q_2} \cdots e^{[\mathcal{S}_n] q_n} M \qquad \text{(space form)},$$

$$T_{sb}(q) = M e^{[\mathcal{B}_1] q_1} e^{[\mathcal{B}_2] q_2} \cdots e^{[\mathcal{B}_n] q_n} \qquad \text{(body form)},$$

where $\mathcal{B}_i = \mathrm{Ad}_{M^{-1}} \mathcal{S}_i$ is the screw axis of joint $i$ at the home configuration written in $\{b\}$.

## In plain words

Put the robot in a pose you choose and call it home. Write down two things in that pose: where the gripper is, and where each joint axis is. That is all the formula needs.

To find the gripper for other joint values, move the joints one at a time, starting with the one nearest the gripper. While the joints closer to the base are still at home, the last joint axis is exactly where you wrote it down, so turning it moves the gripper by a known screw motion. Then turn the joint before it. Its axis is also still where you wrote it down, and it carries the last link and the gripper with it. Go on back to the base. The result is one known motion per joint, applied in order to the home pose of the gripper.

## Proof

**Two facts.**

(a) *Conjugation.* For $X \in SE(3)$ and a twist $\mathcal{A}$, $X[\mathcal{A}]X^{-1} = [\mathrm{Ad}_X \mathcal{A}]$, where $\mathrm{Ad}_X$ is the [adjoint map](/adjoint-map-se3/). Since $X A^k X^{-1} = (X A X^{-1})^k$, the power series of the [matrix exponential](/matrix-exponential/) gives $X e^{[\mathcal{A}]\theta} X^{-1} = e^{[\mathrm{Ad}_X\mathcal{A}]\theta}$.

(b) *One joint.* Fix a frame $\{i\}$ on link $i$ and let $\mathcal{A}_i$ be the screw axis of joint $i$ in $\{i\}$. The axis is fixed in both links $i - 1$ and $i$, and turning the joint by $q_i$ moves link $i$ relative to link $i - 1$ by the screw motion about that axis. Written in the frame of the moving link, that motion acts on the right, so $T_{i-1,i}(q_i) = T_{i-1,i}(0)\, e^{[\mathcal{A}_i] q_i}$.

**The product.** Let $T_{n,b}$ be the fixed pose of $\{b\}$ in $\{n\}$, with $\{0\} = \{s\}$. Then

$$T_{sb}(q) = T_{01}(0) e^{[\mathcal{A}_1] q_1}\, T_{12}(0) e^{[\mathcal{A}_2] q_2} \cdots T_{n-1,n}(0) e^{[\mathcal{A}_n] q_n}\, T_{n,b}.$$

Let $P_i = T_{01}(0) T_{12}(0) \cdots T_{i-1,i}(0)$ be the home pose of $\{i\}$ in $\{s\}$, so $P_{i-1}^{-1} P_i = T_{i-1,i}(0)$ and $M = P_n T_{n,b}$. Insert $P_i^{-1} P_i = I$ after each exponential:

$$T_{sb}(q) = \big(P_1 e^{[\mathcal{A}_1] q_1} P_1^{-1}\big)\big(P_2 e^{[\mathcal{A}_2] q_2} P_2^{-1}\big) \cdots \big(P_n e^{[\mathcal{A}_n] q_n} P_n^{-1}\big) P_n T_{n,b}.$$

To check this, expand: between the factors $e^{[\mathcal{A}_{i-1}] q_{i-1}}$ and $e^{[\mathcal{A}_i] q_i}$ the product has $P_{i-1}^{-1} P_i = T_{i-1,i}(0)$, as in the line before. By fact (a), $P_i e^{[\mathcal{A}_i] q_i} P_i^{-1} = e^{[\mathrm{Ad}_{P_i}\mathcal{A}_i] q_i}$, and $\mathrm{Ad}_{P_i}\mathcal{A}_i$ is the axis of joint $i$ written in $\{s\}$ with the robot at home, which is $\mathcal{S}_i$. With $P_n T_{n,b} = M$ this is the space form.

**The body form.** By fact (a) with $X = M^{-1}$, $e^{[\mathcal{S}_i] q_i} M = M e^{[\mathrm{Ad}_{M^{-1}}\mathcal{S}_i] q_i} = M e^{[\mathcal{B}_i] q_i}$. Move $M$ to the left through each factor, from the last one to the first. $\blacksquare$

The link frames $\{i\}$ were used only inside the proof. They cancel, and the result needs only $\mathcal{S}_i$ and $M$.

## Consequences

- **Cost.** Each exponential costs $O(1)$ operations by [Rodrigues' formula](/rodrigues-rotation-formula/), so the forward kinematics costs $O(n)$ operations in the [real RAM](/real-ram/) model, the same as the [Denavit-Hartenberg](/denavit-hartenberg-convention/) product.
- **Jacobians.** Differentiating the space form gives the space Jacobian: its column $i$ is $\mathrm{Ad}_{e^{[\mathcal{S}_1] q_1} \cdots e^{[\mathcal{S}_{i-1}] q_{i-1}}}\mathcal{S}_i$, the current axis of joint $i$ in $\{s\}$. The body form gives the body Jacobian in the same way. See [space and body Jacobian](/space-and-body-jacobian/).
- **Free choice of frames and home.** Any home configuration and any frames $\{s\}$ and $\{b\}$ can be used. Nothing has to lie on a common normal, so arms with parallel or intersecting axes need no special rules.
- **Calibration.** The parameters $\mathcal{S}_i$ and $M$ change smoothly with the geometry of the arm. The DH parameters jump when two parallel axes are tilted by a small angle. This makes the product of exponentials a natural model for [kinematic calibration](/kinematic-calibration/), at the cost of more parameters (6 per joint and 6 for $M$, against 4 per joint), with constraints $|\omega_i| = 1$ and $\omega_i^\top v_i = 0$ for revolute joints.

**Worked example.** The check value $\mathcal{S} = (0, 0, 1, 1, 0, 0)$, $\theta = \pi/2$ is a rotation about the vertical axis through $(0, 1, 0)$, since $-\omega \times (0, 1, 0) = (1, 0, 0)$. Its exponential has $R = R_z(\pi/2)$ and $p = (1, 1, 0)$: the origin is at $(0, -1)$ from the axis, and a quarter turn takes it to $(1, 0)$ from the axis, so to $(1, 1)$.

For a planar 2R arm with $L_1 = L_2 = 1$ m and home configuration stretched along $x$: $\mathcal{S}_1 = (0, 0, 1, 0, 0, 0)$, $\mathcal{S}_2 = (0, 0, 1, 0, -1, 0)$ (the axis through $(1, 0, 0)$), and $M$ is the translation by $(2, 0, 0)$. The body axes are $\mathcal{B}_1 = (0, 0, 1, 0, 2, 0)$ and $\mathcal{B}_2 = (0, 0, 1, 0, 1, 0)$, the same axes seen from the tip at $(2, 0, 0)$. At $q = (\pi/2, \pi/2)$ the space form gives the end point $(-1, 1)$, which agrees with $x = \cos(\pi/2) + \cos\pi$ and $y = \sin(\pi/2) + \sin\pi$.

## Tightness

- **The axes must be the home axes.** Take the 2R arm above at $q = (\pi/2, \pi/2)$. After joint 1 has turned by $\pi/2$, the axis of joint 2 passes through $(0, 1)$, with screw axis $\mathcal{S}_2' = (0, 0, 1, 1, 0, 0)$. Using this current axis with the old $M$ gives $e^{[\mathcal{S}_1]\pi/2} e^{[\mathcal{S}_2']\pi/2} M$: the point $(2, 0)$ turns about $(0, 1)$ to $(1, 3)$, then about the origin to $(-3, 1)$. The true end point is $(-1, 1)$.
- **A new home needs new data.** If the home configuration of the same arm is moved to $q_1 = \pi/2$, $q_2 = 0$, the data become $\mathcal{S}_1 = (0, 0, 1, 0, 0, 0)$, $\mathcal{S}_2 = (0, 0, 1, 1, 0, 0)$ and $M$ with $R = R_z(\pi/2)$ and $p = (0, 2, 0)$. With these, the new joint values $(0, \pi/2)$, which are the old $(\pi/2, \pi/2)$, give the correct end point: $(0, 2)$ turns about $(0, 1)$ to $(-1, 1)$. Both $\mathcal{S}_2$ and $M$ changed. Here $\mathcal{S}_1$ stayed the same only because joint 1 is the first joint.
- **The order of the factors.** The exponentials do not commute. For the 2R arm at $q = (\pi/2, \pi/2)$, the product with the factors swapped, $e^{[\mathcal{S}_2]\pi/2} e^{[\mathcal{S}_1]\pi/2} M$, puts the end point at $(-1, -1)$.
- **One freedom per joint.** A joint with more freedoms must be split. A spherical joint is three revolute joints whose axes meet in one point.
- **Open chains only.** For a closed chain, the formula gives the pose along each leg, but the joint values must also satisfy the loop closure equations, which the formula does not solve. See [Stewart-Gough forward kinematics](/stewart-gough-forward-kinematics/).

## History

Brockett (1984) introduced the product of exponentials to robot kinematics, at the Mathematical Theory of Networks and Systems symposium of 1983, with screw theory and the Lie group $SE(3)$ as the tools. Murray, Li and Sastry (1994) made it the main tool of their textbook, and Lynch and Park (2017) use it in place of Denavit-Hartenberg parameters, which they put in an appendix.

## References
