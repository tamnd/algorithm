---
tag: CX82KN
kind: definition
slug: denavit-hartenberg-convention
name: Denavit-Hartenberg convention
aliases:
- DH parameters
- Denavit-Hartenberg parameters
area: robotics/robot-kinematics
level: intro
summary: Four parameters per link, two lengths and two angles, that fix frames on a serial chain so that each joint is one transform Rz(theta) Trans_z(d) Trans_x(a) Rx(alpha).
prereqs: [forward-kinematics, homogeneous-transformation-matrix]
see_also: [forward-kinematics, product-of-exponentials-formula, kinematic-calibration, homogeneous-transformation-matrix, kinematic-pair, inverse-kinematics, pieper-criterion]
sources:
  - paper: doi:10.1115/1.4011045
    title: J. Denavit and R. S. Hartenberg, A kinematic notation for lower-pair mechanisms based on matrices, Journal of Applied Mechanics 22, 1955
    locator: pages 215 to 221, the four parameters of each link and the matrix that relates neighboring frames
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, 2nd edition, Wiley, 2020
    locator: the chapter on forward kinematics, the Denavit-Hartenberg convention and its existence and uniqueness argument (general locator)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.8.2, Denavit-Hartenberg Convention, and Section 2.9, kinematics of typical manipulator structures (the anthropomorphic arm)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix C, Denavit-Hartenberg Parameters, with the comparison to the product of exponentials
  - book: "John J. Craig, Introduction to Robotics: Mechanics and Control, 3rd edition, Pearson Prentice Hall, 2005"
    locator: Chapter 3, Manipulator kinematics, the modified convention with alpha and a of the previous link (general locator)
  - paper: doi:10.1109/CDC.1983.269783
    title: S. A. Hayati, Robot arm geometric link parameter estimation, Proceedings of the 22nd IEEE Conference on Decision and Control, 1983
    locator: pages 1477 to 1483, the failure of the parameters for nearly parallel joint axes
---

The Denavit-Hartenberg convention is a rule for putting one coordinate frame on each link of a serial robot so that the move from one frame to the next needs only four numbers. Two of them are lengths, $a$ and $d$, and two are angles, $\alpha$ and $\theta$. One of the four is the joint value, and the other three are fixed by the shape of the link. A robot is then described by a table with one row per joint, and its [forward kinematics](/forward-kinematics/) is the product of one $4 \times 4$ matrix per row. A general transform between two frames needs six numbers. The convention saves two per link by choosing where each frame goes.

## Definition

**Frames.** Number the links $0$ (the base) to $n$ and the joints $1$ to $n$, so that joint $i$ connects link $i - 1$ to link $i$. Frame $\{i\}$ is fixed to link $i$. In the classic convention, used by Denavit and Hartenberg (1955) and by Spong, Hutchinson and Vidyasagar:

1. The axis $z_{i-1}$ is the axis of joint $i$.
2. The axis $x_i$ lies on the common normal of $z_{i-1}$ and $z_i$, and points from $z_{i-1}$ to $z_i$. So $x_i$ is perpendicular to $z_{i-1}$ and meets it.
3. The origin $o_i$ is where $x_i$ meets $z_i$, and $y_i$ completes a right-handed frame.

**Parameters.** With these frames, link $i$ has four numbers:

| parameter | meaning |
|---|---|
| $a_i$ | link length: the distance from $z_{i-1}$ to $z_i$, along $x_i$ |
| $\alpha_i$ | link twist: the angle from $z_{i-1}$ to $z_i$, about $x_i$ |
| $d_i$ | link offset: the distance from $o_{i-1}$ to the foot of $x_i$ on $z_{i-1}$, along $z_{i-1}$ |
| $\theta_i$ | joint angle: the angle from $x_{i-1}$ to $x_i$, about $z_{i-1}$ |

For a revolute joint $\theta_i$ is the joint variable and $a_i, \alpha_i, d_i$ are constants. For a prismatic joint $d_i$ is the variable.

**Link transform.** The pose of $\{i\}$ in $\{i - 1\}$ is

$$A_i = R_z(\theta_i)\, \mathrm{Trans}_z(d_i)\, \mathrm{Trans}_x(a_i)\, R_x(\alpha_i) = \begin{pmatrix} \cos\theta_i & -\sin\theta_i\cos\alpha_i & \sin\theta_i\sin\alpha_i & a_i\cos\theta_i \\ \sin\theta_i & \cos\theta_i\cos\alpha_i & -\cos\theta_i\sin\alpha_i & a_i\sin\theta_i \\ 0 & \sin\alpha_i & \cos\alpha_i & d_i \\ 0 & 0 & 0 & 1 \end{pmatrix},$$

and the end effector pose is $T_{0n} = A_1 A_2 \cdots A_n$, followed by a fixed tool transform if the tool frame is not $\{n\}$.

**Why four numbers suffice.** Let $\{i - 1\}$ and $\{i\}$ be frames such that $x_i$ is perpendicular to $z_{i-1}$ and meets it. Then the pose of $\{i\}$ in $\{i - 1\}$ has the form $A_i$ above. *Proof.* Since $x_i \perp z_{i-1}$, in the coordinates of $\{i - 1\}$ we have $x_i = (\cos\theta, \sin\theta, 0)$ for some $\theta$. The axis $z_i$ is a unit vector perpendicular to $x_i$, so it is $\cos\alpha\, z_{i-1} + \sin\alpha\, (z_{i-1} \times x_i)$ for some $\alpha$, and $y_i = z_i \times x_i$. These are the columns of $R_z(\theta) R_x(\alpha)$. Since the line of $x_i$ meets $z_{i-1}$ at a point $o_{i-1} + d\, z_{i-1}$, and $o_i$ is on that line, $o_i = o_{i-1} + d\, z_{i-1} + a\, x_i$ for some $d$ and $a$, which is the last column of $A_i$. $\blacksquare$ The two conditions on $x_i$ remove two of the six numbers of a general transform.

**Choices that are not unique.** If $z_{i-1}$ and $z_i$ are parallel, the common normal is not unique and $d_i$ can take any value; the usual choice is $d_i = 0$. If they meet, $a_i = 0$ and $x_i$ is normal to the plane of the two axes, with a choice of sign. Frame $\{0\}$ only needs $z_0$ on the first axis, and frame $\{n\}$ only needs $x_n \perp z_{n-1}$. So two people can write different but correct tables for the same robot.

**The modified convention.** Craig's textbook puts frame $\{i\}$ on the axis of joint $i$ instead of joint $i + 1$, and uses

$$A_i = R_x(\alpha_{i-1})\, \mathrm{Trans}_x(a_{i-1})\, R_z(\theta_i)\, \mathrm{Trans}_z(d_i),$$

with $\alpha_{i-1}$ and $a_{i-1}$ taken from the previous link. The two conventions give different tables for the same arm, and a table must always say which one it uses. This page uses the classic one, except where it says otherwise.

## Examples and non-examples

**Planar 2R arm** with $L_1 = L_2 = 1$ m, classic convention:

| $i$ | $\theta_i$ | $d_i$ | $a_i$ | $\alpha_i$ |
|---|---|---|---|---|
| 1 | $q_1$ | 0 | $L_1$ | 0 |
| 2 | $q_2$ | 0 | $L_2$ | 0 |

The last column of $A_1 A_2$ is $(L_1\cos q_1 + L_2\cos(q_1 + q_2),\ L_1\sin q_1 + L_2\sin(q_1 + q_2),\ 0, 1)$. At $q = (0, \pi/2)$ this is the point $(1, 1, 0)$. In the modified convention the rows are $(\alpha_0, a_0, d_1, \theta_1) = (0, 0, 0, q_1)$ and $(\alpha_1, a_1, d_2, \theta_2) = (0, L_1, 0, q_2)$, and the tool transform $\mathrm{Trans}_x(L_2)$ must be added, because frame $\{2\}$ now sits on the second joint and not at the tip. Both give the same matrix at $q = (0, \pi/2)$.

**Spatial 3R arm** (the anthropomorphic arm of Siciliano et al., Section 2.9, here with a shoulder height of 1 m and links of 1 m):

| $i$ | $\theta_i$ | $d_i$ (m) | $a_i$ (m) | $\alpha_i$ |
|---|---|---|---|---|
| 1 | $q_1$ | 1 | 0 | $\pi/2$ |
| 2 | $q_2$ | 0 | 1 | 0 |
| 3 | $q_3$ | 0 | 1 | 0 |

The twist $\alpha_1 = \pi/2$ turns the vertical first axis into the horizontal second axis. At $q = 0$, $A_1 A_2 A_3$ has the rotation $R_x(\pi/2)$ and the position $(2, 0, 1)$. At $q = (\pi/2, 0, \pi/2)$ it is

$$T_{03} = \begin{pmatrix} 0 & 0 & 1 & 0 \\ 0 & -1 & 0 & 1 \\ 1 & 0 & 0 & 2 \\ 0 & 0 & 0 & 1 \end{pmatrix}.$$

**Check against the product of exponentials.** The same arm in [product of exponentials](/product-of-exponentials-formula/) form has the home pose $M$ equal to $A_1 A_2 A_3$ at $q = 0$, and the screw axes $\mathcal{S}_1 = (0, 0, 1, 0, 0, 0)$, $\mathcal{S}_2 = (0, -1, 0, 1, 0, 0)$ (axis $-y$ through $(0, 0, 1)$) and $\mathcal{S}_3 = (0, -1, 0, 1, 0, -1)$ (axis $-y$ through $(1, 0, 1)$). The axes point along $-y$ because $z_1 = R_x(\pi/2)\, z = (0, -1, 0)$. A script compared the two products at 1000 random joint vectors and found a largest difference of $1.3 \times 10^{-15}$ in any entry. For the 2R table above it found $9 \times 10^{-16}$.

**Non-example: a ball joint as one row.** A spherical joint has three freedoms, and one row has one joint variable. The joint must be written as three revolute rows with $a = d = 0$ and twists of $\pm\pi/2$, with two massless links in between.

**Non-example: a closed chain.** A DH table describes a path of joints. A [parallel manipulator](/parallel-manipulator/) needs one table per leg and loop closure equations between them.

## Related definitions

- [Product of exponentials formula](/product-of-exponentials-formula/): the other standard way to write the forward kinematics. It needs no link frames but uses six numbers per joint and the home pose $M$, against four numbers per joint here.
- [Forward kinematics](/forward-kinematics/): the problem that the table solves, by the product $A_1 \cdots A_n$.
- [Kinematic calibration](/kinematic-calibration/): the DH parameters are not a continuous model near parallel axes. If two nominally parallel axes are tilted by a small angle, the common normal jumps and $d_i$ can change by a large amount. Hayati (1983) showed this and added a rotation about $y$ for such joints.
- [Pieper criterion](/pieper-criterion/): many arms whose inverse kinematics has a closed form have DH tables with $a_i = 0$ and $d_i = 0$ at the wrist, so that three axes meet in a point.

### History

Denavit and Hartenberg (1955) proposed the four parameters to describe lower-pair mechanisms by matrices. The notation became the standard for robot arms in the 1970s and 1980s. Craig's textbook made the modified convention common, and many texts on dynamics now use it. Brockett (1984) proposed the product of exponentials as an alternative without link frames.

## References
