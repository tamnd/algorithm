---
tag: DQFEN4
kind: definition
slug: space-and-body-jacobian
name: Space and body Jacobian
aliases:
- space Jacobian
- body Jacobian
area: robotics/robot-kinematics
level: core
summary: The Jacobians of a chain that give the end effector twist in the fixed frame and in the end effector frame, related by an adjoint.
model: real-ram
prereqs: [product-of-exponentials-formula, adjoint-map-se3, rigid-body-twist]
see_also: [geometric-jacobian, analytic-jacobian, jacobian-statics-duality, kinematic-singularity, jacobian-pseudoinverse-method, se3-exponential-map, screw-motion, wrench]
sources:
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.1.1 (the space Jacobian), Section 5.1.2 (the body Jacobian), Section 5.1.3 (visualizing them) and Section 5.1.4 (the relation by the adjoint)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 3 (the spatial and body manipulator Jacobians); the book writes a twist with the linear part first
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.1 (the geometric Jacobian, for the comparison with the twist form)
---

The space Jacobian $J_s(q)$ and the body Jacobian $J_b(q)$ of a robot arm map the joint velocities $\dot q$ to the velocity of the end effector, written as a [twist](/rigid-body-twist/): $\mathcal V_s = J_s(q)\dot q$ in the fixed frame {s}, and $\mathcal V_b = J_b(q)\dot q$ in the end effector frame {b}.
Both are $6 \times n$ matrices for an arm with $n$ joints, and they come straight from the screw axes of the [product of exponentials formula](/product-of-exponentials-formula/): column $i$ is the screw axis of joint $i$ at the current configuration, seen from {s} or from {b}.
The two are related by the [adjoint map](/adjoint-map-se3/), $J_b = \mathrm{Ad}_{T_{bs}} J_s$.
This page uses the conventions of Lynch and Park, with the angular part first; the [geometric Jacobian](/geometric-jacobian/) of Siciliano et al. puts the linear part first and uses the velocity of the end effector origin, and the conversion is below.

## Definition

A twist is $\mathcal V = (\omega, v) \in \mathbb{R}^6$, angular part first, with the $4 \times 4$ matrix $[\mathcal V] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix}$, where $[\omega] x = \omega \times x$.
For a moving pose $T(t) \in SE(3)$ of the end effector frame {b} in {s}, the spatial twist and the body twist are defined by

$$[\mathcal V_s] = \dot T T^{-1}, \qquad [\mathcal V_b] = T^{-1} \dot T.$$

In $\mathcal V_s = (\omega_s, v_s)$, $\omega_s$ is the angular velocity in {s} coordinates, and $v_s$ is the velocity of the point of the body that is at the origin of {s}.
In $\mathcal V_b = (\omega_b, v_b)$, $\omega_b$ is the angular velocity in {b} coordinates and $v_b$ is the velocity of the origin of {b}, in {b} coordinates.

Let the arm have forward kinematics in the space form $T(q) = e^{[\mathcal S_1] q_1} \cdots e^{[\mathcal S_n] q_n} M$ and in the body form $T(q) = M e^{[\mathcal B_1] q_1} \cdots e^{[\mathcal B_n] q_n}$, with the screw axes $\mathcal S_i$ in {s} and $\mathcal B_i = \mathrm{Ad}_{M^{-1}} \mathcal S_i$ in {b}, all at the home configuration.

**Definition.** The space Jacobian $J_s(q)$ is the $6 \times n$ matrix with $\mathcal V_s = J_s(q)\dot q$ for every $\dot q$.
Its columns are

$$J_{s1} = \mathcal S_1, \qquad J_{si}(q) = \mathrm{Ad}_{e^{[\mathcal S_1] q_1} \cdots e^{[\mathcal S_{i-1}] q_{i-1}}}(\mathcal S_i), \quad i = 2, \dots, n.$$

The body Jacobian $J_b(q)$ is the $6 \times n$ matrix with $\mathcal V_b = J_b(q)\dot q$.
Its columns are

$$J_{bn} = \mathcal B_n, \qquad J_{bi}(q) = \mathrm{Ad}_{e^{-[\mathcal B_n] q_n} \cdots e^{-[\mathcal B_{i+1}] q_{i+1}}}(\mathcal B_i), \quad i = 1, \dots, n - 1.$$

Here $\mathrm{Ad}_T = \begin{pmatrix} R & 0 \\ [p] R & R \end{pmatrix}$ for $T = (R, p)$, and $\mathrm{Ad}_T \mathcal V$ is the twist $\mathcal V$ written in the frame that $T$ maps from.

**Why the columns are right.** By the product rule, $\dot T T^{-1} = \sum_i \frac{\partial T}{\partial q_i} T^{-1} \dot q_i$.
Write $E_i = e^{[\mathcal S_1] q_1} \cdots e^{[\mathcal S_{i-1}] q_{i-1}}$.
Since $\frac{d}{dq_i} e^{[\mathcal S_i] q_i} = [\mathcal S_i] e^{[\mathcal S_i] q_i}$, all factors after $E_i$ cancel against $T^{-1}$, and $\frac{\partial T}{\partial q_i} T^{-1} = E_i [\mathcal S_i] E_i^{-1} = [\mathrm{Ad}_{E_i} \mathcal S_i]$.
So column $i$ of $J_s$ is $\mathrm{Ad}_{E_i} \mathcal S_i$: the screw axis of joint $i$ after joints $1$ to $i - 1$ have moved it.
The body case is the mirror image: $T^{-1} \partial T / \partial q_i$ keeps the factors after joint $i$, which gives the adjoint of $e^{-[\mathcal B_n] q_n} \cdots e^{-[\mathcal B_{i+1}] q_{i+1}}$.

**The relation.** Since $T^{-1} \dot T = T^{-1} (\dot T T^{-1}) T$, the two twists satisfy $\mathcal V_b = \mathrm{Ad}_{T^{-1}} \mathcal V_s$, so for all $q$

$$J_b(q) = \mathrm{Ad}_{T_{bs}(q)} J_s(q), \qquad J_s(q) = \mathrm{Ad}_{T_{sb}(q)} J_b(q),$$

with $T_{sb} = T(q)$ and $T_{bs} = T(q)^{-1}$.
$\mathrm{Ad}_T$ is invertible, so $J_s$ and $J_b$ have the same rank at every $q$, and the [kinematic singularities](/kinematic-singularity/) do not depend on the frame.

**Relation to the geometric Jacobian.** The [geometric Jacobian](/geometric-jacobian/) $J = (J_P, J_O)$ gives the velocity $\dot p_e$ of the end effector origin and the angular velocity, linear part first.
With $T(q) = (R_e, p_e)$, $\omega_s = J_O \dot q$, $v_s = \dot p_e - \omega_s \times p_e$, $\omega_b = R_e^{\mathsf T} \omega_s$ and $v_b = R_e^{\mathsf T} \dot p_e$.
So $J_s$ has the blocks $J_O$ over $J_P + [p_e] J_O$, and $J_b$ has $R_e^{\mathsf T} J_O$ over $R_e^{\mathsf T} J_P$.
Murray, Li and Sastry use the same twists as Lynch and Park but write the linear part first, so their Jacobians have the two blocks of rows swapped.

**Computation.**
Both forms build the product of exponentials once, from one end of the chain.
The code on this page follows these lines.

```pseudo id=main
SPACE-JACOBIAN(S_1, ..., S_n, q)
L1  T ← I
L2  for i ← 1 to n
L3      J_si ← Ad_T S_i                       ▷ T = e^[S_1]q_1 ... e^[S_(i-1)]q_(i-1)
L4      T ← T e^{[S_i] q_i}
L5  return J_s
BODY-JACOBIAN(B_1, ..., B_n, q)
L6  T ← I
L7  for i ← n down to 1
L8      J_bi ← Ad_T B_i                       ▷ T = e^-[B_n]q_n ... e^-[B_(i+1)]q_(i+1)
L9      T ← T e^{-[B_i] q_i}
L10 return J_b
```

Each pass of the loop costs one [exponential of SE(3)](/se3-exponential-map/), one $4 \times 4$ product and one $6 \times 6$ adjoint times a vector, which is a constant number of operations.
So each Jacobian costs $\Theta(n)$ operations and $\Theta(n)$ space in the [real RAM](/real-ram/).

## Examples and non-examples

**The planar 2R arm.** Two revolute joints about vertical axes through $(0, 0, 0)$ and $(1, 0, 0)$, links $L_1 = L_2 = 1$ m, and the end effector frame at $(2, 0, 0)$ at home, so $M = (I, (2, 0, 0))$.
A revolute axis with unit direction $\omega$ through the point $a$ has the screw axis $(\omega, -\omega \times a)$, so

$$\mathcal S_1 = (0, 0, 1, 0, 0, 0), \quad \mathcal S_2 = (0, 0, 1, 0, -1, 0), \quad \mathcal B_1 = (0, 0, 1, 0, 2, 0), \quad \mathcal B_2 = (0, 0, 1, 0, 1, 0).$$

At $q = (0, \pi/2)$, $T(q) = (R_z(\pi/2), (1, 1, 0))$.
Column 1 of $J_s$ is $\mathcal S_1$, and column 2 is $\mathrm{Ad}_{e^{[\mathcal S_1] \cdot 0}} \mathcal S_2 = \mathcal S_2$.
Column 2 of $J_b$ is $\mathcal B_2$, and column 1 is $\mathrm{Ad}_{e^{-[\mathcal B_2]\pi/2}} \mathcal B_1 = (0, 0, 1, 1, 1, 0)$.
In full, with the rows $(\omega_x, \omega_y, \omega_z, v_x, v_y, v_z)$:

$$J_s = \begin{pmatrix} 0 & 0 \\ 0 & 0 \\ 1 & 1 \\ 0 & 0 \\ 0 & -1 \\ 0 & 0 \end{pmatrix}, \qquad J_b = \begin{pmatrix} 0 & 0 \\ 0 & 0 \\ 1 & 1 \\ 1 & 0 \\ 1 & 1 \\ 0 & 0 \end{pmatrix}.$$

The relation $J_b = \mathrm{Ad}_{T^{-1}} J_s$ holds: $T^{-1} = (R_z(-\pi/2), (-1, 1, 0))$, and for column 1, $R_z(-\pi/2)\,\omega = (0, 0, 1)$ and $[(-1, 1, 0)](0, 0, 1) = (1, 1, 0)$.
The velocity of the end effector origin is $R_e v_b$: for $\dot q = (1, 0)$ it is $R_z(\pi/2)(1, 1, 0) = (-1, 1, 0)$, the first column of the linear Jacobian $\begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}$ of the 2R check values, whose determinant is $\sin q_2 = 1$.
The $v_s$ part of column 1 of $J_s$ is zero although the end effector moves, because $v_s$ is the velocity of the body point at the origin of {s}, which is on the axis of joint 1.

**Where the columns depend on $q$.** Column $i$ of $J_s$ depends only on $q_1, \dots, q_{i-1}$, so the first column is constant.
Column $i$ of $J_b$ depends only on $q_{i+1}, \dots, q_n$, so the last column is constant.
In the 2R example, moving $q_2$ changes column 1 of $J_b$ but not column 1 of $J_s$.

**A prismatic joint.** Its screw axis is $(0, v)$ with $|v| = 1$, and the adjoint keeps the first three entries zero, so its column has no angular part in either Jacobian.

**Non-example: the geometric Jacobian.** The lower block of $J_s$ is $J_P + [p_e] J_O$, not $J_P$; the two agree only for columns whose angular part is zero or when $p_e = 0$.

**Non-example: the analytic Jacobian.** The derivative of a minimal pose vector such as position and Euler angles is the [analytic Jacobian](/analytic-jacobian/); it is not a map to a twist, and it has extra singular points from the angles.

**Non-example: $\partial \xi / \partial q$ for $\xi = \log T(q)$.** The derivative of the exponential coordinates of the pose is not $J_s$ or $J_b$; it differs by the Jacobian of the exponential map of SE(3), which equals $I$ only at $\xi = 0$.

## Related definitions

- [Geometric Jacobian](/geometric-jacobian/): linear part first, with the velocity of the end effector origin.
- [Analytic Jacobian](/analytic-jacobian/): the derivative of a minimal pose vector.
- [Adjoint map](/adjoint-map-se3/): the change of frame of twists that relates $J_s$ and $J_b$.
- [Jacobian statics duality](/jacobian-statics-duality/): $\tau = J_s^{\mathsf T} \mathcal F_s = J_b^{\mathsf T} \mathcal F_b$, where $\mathcal F_s$ and $\mathcal F_b$ are the same [wrench](/wrench/) in {s} and in {b}.
- [Kinematic singularity](/kinematic-singularity/): a configuration where $J_s$, and so $J_b$, loses rank.
- [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/): numerical inverse kinematics that uses $J_b$ and the body twist error.
- [Screw motion](/screw-motion/): the motion that a single column produces when only its joint moves.

## References
