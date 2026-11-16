---
tag: TB3AFJ
kind: definition
slug: geometric-jacobian
name: Geometric Jacobian
aliases:
- manipulator Jacobian
area: robotics/robot-kinematics
level: core
summary: The 6 by n matrix that maps the joint velocities of an arm to the linear velocity of the end effector origin and the angular velocity, built column by column from the joint axes.
model: real-ram
prereqs: [forward-kinematics, rigid-body-twist, angular-velocity]
see_also: [space-and-body-jacobian, analytic-jacobian, kinematic-singularity, jacobian-statics-duality, manipulability-ellipsoid, denavit-hartenberg-convention, resolved-rate-motion-control, jacobian-linearization]
sources:
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.1 (the geometric Jacobian, linear velocity first) and Section 3.2 (Jacobian computation, the columns for revolute and prismatic joints)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, 2nd edition, Wiley, 2020
    locator: Chapter 4 (velocity kinematics and the manipulator Jacobian, with the same column formulas)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.1 (the space and body Jacobians, angular part first) and Section 5.1.5 (other notions of the Jacobian)
---

The geometric Jacobian of a robot arm is the matrix $J(q)$ that turns the joint velocities $\dot q$ into the velocity of the end effector: the linear velocity $\dot p_e$ of its origin and its angular velocity $\omega_e$, both in the base frame.
For an arm with $n$ joints it has 6 rows and $n$ columns, and column $i$ depends only on the axis of joint $i$ and on where the end effector is, so it can be written down from the geometry without any differentiation.
This page uses the form of Siciliano et al. and Spong et al., with the linear part first.
The [space and body Jacobians](/space-and-body-jacobian/) of Lynch and Park carry the same information as twists, with the angular part first, and the [analytic Jacobian](/analytic-jacobian/) is the derivative of a minimal pose vector; the conversions are below.

## Definition

Take a serial chain with joints $1, \dots, n$, each revolute or prismatic, and the joint values $q = (q_1, \dots, q_n)$.
Let $T_i(q) = \begin{pmatrix} R_i & p_i \\ 0 & 1 \end{pmatrix}$ be the pose of the frame of link $i$ in the base frame {s}, with $T_0 = I$, and attach the frames by the [Denavit-Hartenberg convention](/denavit-hartenberg-convention/), so that the axis of joint $i$ is the $z$ axis of frame $i - 1$.
Write $z_{i-1}$ for the third column of $R_{i-1}$ and $p_e = p_n$ for the end effector origin.

**Definition.** The geometric Jacobian is the $6 \times n$ matrix

$$J(q) = \begin{pmatrix} J_P(q) \\ J_O(q) \end{pmatrix}, \qquad \dot p_e = J_P(q)\,\dot q, \qquad \omega_e = J_O(q)\,\dot q,$$

where $\omega_e$ is the [angular velocity](/angular-velocity/) of the end effector frame, $\dot R_e = [\omega_e] R_e$, and $[\omega]$ is the skew-symmetric matrix with $[\omega]x = \omega \times x$.
Its columns are

$$J_i = \begin{pmatrix} z_{i-1} \times (p_e - p_{i-1}) \\ z_{i-1} \end{pmatrix} \text{ for a revolute joint}, \qquad J_i = \begin{pmatrix} z_{i-1} \\ 0 \end{pmatrix} \text{ for a prismatic joint}.$$

The column formula follows from rigid motion.
If only joint $i$ moves, with rate $\dot q_i$, the links after it turn about the line through $p_{i-1}$ with direction $z_{i-1}$.
A point $p$ of a body that turns with angular velocity $\omega$ about a line through $a$ has the velocity $\omega \times (p - a)$, so the end effector origin moves with $\dot q_i\, z_{i-1} \times (p_e - p_{i-1})$, and the angular velocity is $\dot q_i z_{i-1}$.
A prismatic joint slides the rest of the arm along $z_{i-1}$ without rotation.
The velocities of all joints add, because both $\dot p_e$ and $\omega_e$ are linear in $\dot q$.
So $J_P = \partial p_e / \partial q$, the ordinary derivative of the position, while $J_O$ is not the derivative of any vector of angles: angular velocity is not integrable.
That second fact is what "geometric" means here, as opposed to the [analytic Jacobian](/analytic-jacobian/).

**Conversion to twists.** Lynch and Park write a twist as $\mathcal V = (\omega, v)$, with the angular part first.
In the spatial twist $\mathcal V_s = (\omega_s, v_s)$, $\omega_s = \omega_e$, and $v_s$ is the velocity of the point of the moving body that is at the origin of {s}, not the velocity of $p_e$.
The two are related by $v_s = \dot p_e - \omega_e \times p_e$.
In the body twist $\mathcal V_b = (\omega_b, v_b)$, both parts are in end effector coordinates: $\omega_b = R_e^{\mathsf T}\omega_e$ and $v_b = R_e^{\mathsf T}\dot p_e$.
So the space Jacobian $J_s$ and the body Jacobian $J_b$ are

$$J_s = \begin{pmatrix} J_O \\ J_P + [p_e] J_O \end{pmatrix}, \qquad J_b = \begin{pmatrix} R_e^{\mathsf T} J_O \\ R_e^{\mathsf T} J_P \end{pmatrix}, \qquad J_P = (\text{lower block of } J_s) - [p_e]\,(\text{upper block of } J_s).$$

All three matrices differ by an invertible $6 \times 6$ factor, so they have the same rank at every $q$, and the same [kinematic singularities](/kinematic-singularity/).

**Computation.**
The code on this page follows these lines.
Each $A_i(q_i) = R_z(\theta_i) T_z(d_i) T_x(a_i) R_x(\alpha_i)$ is the standard Denavit-Hartenberg link transform, with $\theta_i$ or $d_i$ replaced by $q_i$ for a revolute or a prismatic joint.

```pseudo id=main
GEOMETRIC-JACOBIAN(dh, q)                    ▷ dh: one DH row per joint
L1  T ← I
L2  for i ← 1 to n
L3      T ← T A_i(q_i)                        ▷ pose of frame i
L4      T_i ← T                               ▷ store it; T_0 = I
L5  p_e ← translation part of T_n
L6  for i ← 1 to n
L7      z ← third column of R_{i-1} ; p ← p_{i-1}
L8      if joint i is revolute then J_i ← (z × (p_e - p), z)
L9      else J_i ← (z, 0)                     ▷ prismatic
L10 return J
```

Lines L1 to L4 are [forward kinematics](/forward-kinematics/), $n$ products of $4 \times 4$ matrices.
Lines L6 to L9 cost one cross product per column.
So the whole matrix costs $\Theta(n)$ operations and $\Theta(n)$ space in the [real RAM](/real-ram/), the same order as forward kinematics.

## Examples and non-examples

**The planar 2R arm.** Two revolute joints with parallel vertical axes, links $L_1 = L_2 = 1$ m, DH rows $(\theta_i = q_i, d_i = 0, a_i = 1, \alpha_i = 0)$.
At $q = (0, \pi/2)$, the frames have $p_0 = (0, 0, 0)$, $p_1 = (1, 0, 0)$, $z_0 = z_1 = (0, 0, 1)$, and the end effector is at $p_e = (1, 1, 0)$.
Column 1 is $z_0 \times (p_e - p_0) = (-1, 1, 0)$ over $(0, 0, 1)$, and column 2 is $z_1 \times (p_e - p_1) = (-1, 0, 0)$ over $(0, 0, 1)$:

$$J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \\ 0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 1 & 1 \end{pmatrix}.$$

Only rows $x$, $y$ and $\omega_z$ are nonzero, as they must be for a planar arm.
The $2 \times 2$ block of rows $x$ and $y$ is $\begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}$, and its determinant is $L_1 L_2 \sin q_2 = 1$.
For general $q$, the same block is

$$J_P^{xy} = \begin{pmatrix} -L_1 s_1 - L_2 s_{12} & -L_2 s_{12} \\ L_1 c_1 + L_2 c_{12} & L_2 c_{12} \end{pmatrix},$$

with $s_1 = \sin q_1$ and $s_{12} = \sin(q_1 + q_2)$, which is the derivative of $p_e = (L_1 c_1 + L_2 c_{12}, L_1 s_1 + L_2 s_{12})$.
The conversion gives the space Jacobian: column 1 is $(0, 0, 1, 0, 0, 0)$ and column 2 is $(0, 0, 1, 0, -1, 0)$, the two joint screw axes of the [product of exponentials formula](/product-of-exponentials-formula/).
The $v_s$ part of column 1 is zero, although the end effector moves, because the body point at the base origin does not move when joint 1 turns.

**A prismatic joint.** In a PRP arm, the column of the prismatic joint is its axis over zero, whatever the other joints do, because a slide does not turn the end effector.

**A test by finite differences.** For any arm, column $i$ of $J_P$ is $(p_e(q + h e_i) - p_e(q - h e_i)) / (2h) + O(h^2)$, and column $i$ of $J_O$ is the vector of the skew-symmetric part of $(R_e(q + h e_i) - R_e(q - h e_i)) R_e^{\mathsf T} / (2h)$, up to $O(h^2)$.
This gives a simple test of hand-written columns: with $h = 10^{-6}$, a correct Jacobian of a 7R arm with random DH rows agrees with the differences to about $3 \cdot 10^{-10}$ in double precision, and a wrong axis or a wrong frame shows up as an error of order 1.

**Non-example: the derivative of the orientation angles.** If the orientation is given by three [Euler angles](/euler-angles/) $\phi$, then $\partial \phi / \partial q$ is not $J_O$; it is the lower block of the analytic Jacobian, and it is related to $J_O$ by a matrix $T(\phi)$ that is singular at the gimbal lock of the angles.

**Non-example: the derivative of the matrix entries.** The $12 \times n$ matrix of derivatives of the entries of $T(q)$ holds the same information, but it is not a map to a velocity vector, and it is not called the geometric Jacobian.

**Non-example: the twist Jacobian of Lynch and Park.** $J_s$ and $J_b$ are 6 by $n$ maps of the same joint rates, but with the angular part first and with $v_s$ or $v_b$ in place of $\dot p_e$.
Code that mixes the two orders, or that reads $v_s$ as the velocity of the end effector, gives wrong results without an error.

## Related definitions

- [Space and body Jacobians](/space-and-body-jacobian/): the same map with twists as outputs; the conversion is above.
- [Analytic Jacobian](/analytic-jacobian/): the derivative of a minimal pose vector, equal to $J$ times a representation matrix.
- [Kinematic singularity](/kinematic-singularity/): a configuration where $J$ loses rank.
- [Jacobian statics duality](/jacobian-statics-duality/): the joint torques that balance an end effector wrench are $J^{\mathsf T}$ times the wrench, in the same frame.
- [Manipulability ellipsoid](/manipulability-ellipsoid/) and [Yoshikawa manipulability measure](/yoshikawa-manipulability-measure/): the shape of the image of $J$.
- [Resolved-rate motion control](/resolved-rate-motion-control/) and the [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/): they invert $J$ to move the end effector.
- [Jacobian linearization](/jacobian-linearization/): the control view, where a Jacobian is the linear part of any smooth map at a point.
- [Interaction matrix](/interaction-matrix/): the Jacobian of image features with respect to the camera twist, used with this matrix in visual servoing.

## References
