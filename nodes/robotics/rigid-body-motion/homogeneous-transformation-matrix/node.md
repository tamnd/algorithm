---
tag: VNMX81
kind: definition
slug: homogeneous-transformation-matrix
name: Homogeneous transformation matrix
aliases:
- homogeneous transform
- 4x4 transformation matrix
area: robotics/rigid-body-motion
level: intro
summary: "The 4 by 4 matrix T = [[R, p], [0, 1]] of a rotation R and a translation p, so that composing rigid motions and changing frames become matrix products."
prereqs: [rigid-body-transformation]
see_also: [special-euclidean-group, homogeneous-coordinates, pose-compounding-operators, robot-pose, forward-kinematics, denavit-hartenberg-convention, se3-exponential-map, dual-quaternion]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.1 (homogeneous transformation matrices, their inverse and their uses)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 3.1 (homogeneous representation of rigid motions)
---

A homogeneous transformation matrix is a $4 \times 4$ matrix $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix}$ that stores a [rigid body transformation](/rigid-body-transformation/) $x \mapsto Rx + p$ in one matrix, where $R$ is a $3 \times 3$ rotation matrix and $p$ is a translation vector.
A point $x$ is written as the 4-vector $(x, 1)$, and then $T(x, 1) = (Rx + p, 1)$.
With this trick, the composition of two rigid motions is the product of their matrices, and a change of frame is one matrix-vector product.
Robot software uses these matrices to chain the poses of the links of an arm, of sensors and of objects.
The set of all such matrices is the [special Euclidean group](/special-euclidean-group/) SE(3).

## Definition

A homogeneous transformation matrix is a matrix

$$T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} r_{11} & r_{12} & r_{13} & p_1 \\ r_{21} & r_{22} & r_{23} & p_2 \\ r_{31} & r_{32} & r_{33} & p_3 \\ 0 & 0 & 0 & 1 \end{pmatrix}, \qquad R \in SO(3),\ p \in \mathbb{R}^3 .$$

Points and vectors.
A point $x$ has the [homogeneous coordinates](/homogeneous-coordinates/) $(x, 1)$, and $T(x, 1) = (Rx + p, 1)$.
A free vector $v$, such as a direction, has the coordinates $(v, 0)$, and $T(v, 0) = (Rv, 0)$, so it rotates but does not translate.

Frames.
$T_{ab}$ holds the orientation $R_{ab}$ and the origin $p_{ab}$ of frame $\{b\}$ in frame $\{a\}$.
For a point with coordinates $x_b$ in $\{b\}$, $(x_a, 1) = T_{ab}(x_b, 1)$.
The subscripts cancel in a product: $T_{ac} = T_{ab}T_{bc}$.

Inverse.
$$T^{-1} = \begin{pmatrix} R^{\mathsf T} & -R^{\mathsf T}p \\ 0 & 1 \end{pmatrix},$$
and $T_{ab}^{-1} = T_{ba}$.
This needs no general matrix inversion.

Three uses.
The same matrix $T_{sb}$ can be read in three ways: as the configuration of the frame $\{b\}$ relative to $\{s\}$; as the change of coordinates from $\{b\}$ to $\{s\}$; or as a displacement that moves a body.
A displacement $T$ applied by multiplication on the left, $TT_{sb}$, acts about the axes of the fixed frame $\{s\}$.
Applied on the right, $T_{sb}T$, it acts about the axes of the body frame $\{b\}$.

## Examples and non-examples

- Let $R = R_z(\pi/2)$ and $p = (1, 1, 0)$, so $T = \begin{pmatrix} 0 & -1 & 0 & 1 \\ 1 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$. The point $(1, 0, 0)$ goes to $(0, 1, 0) + (1, 1, 0) = (1, 2, 0)$. The direction $(1, 0, 0)$ goes to $(0, 1, 0)$.
- Its inverse is $T^{-1} = \begin{pmatrix} 0 & 1 & 0 & -1 \\ -1 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix}$, since $-R^{\mathsf T}p = -(1, -1, 0)$. It takes $(1, 2, 0)$ back to $(1, 0, 0)$.
- The pure translation by $p$ is $\begin{pmatrix} I & p \\ 0 & 1 \end{pmatrix}$, and the pure rotation is $\begin{pmatrix} R & 0 \\ 0 & 1 \end{pmatrix}$. Every $T$ is the rotation first and the translation second: $T = \begin{pmatrix} I & p \\ 0 & 1 \end{pmatrix}\begin{pmatrix} R & 0 \\ 0 & 1 \end{pmatrix}$.
- Non-example: the $4 \times 4$ matrices of computer graphics with a scale factor, a shear or a perspective last row are also called homogeneous transformations, but they are not rigid. They are affine or projective maps, and the inverse formula above does not hold for them.
- Non-example: a matrix of the right shape whose $3 \times 3$ block is only close to a rotation, for example after many floating-point products. It must be projected back onto SO(3) before the inverse formula is used.

## Related definitions

- The [special Euclidean group](/special-euclidean-group/) SE(3) is the group of these matrices under multiplication.
- The [exponential map of SE(3)](/se3-exponential-map/) builds $T$ from a twist, and its logarithm recovers the twist.
- In [forward kinematics](/forward-kinematics/), the pose of the end of an arm is a product of one matrix per joint, often written with the [Denavit-Hartenberg convention](/denavit-hartenberg-convention/).
- The [pose compounding operators](/pose-compounding-operators/) are the same products, written for poses with uncertainty.
- A [dual quaternion](/dual-quaternion/) stores the same rigid motion in 8 numbers instead of 12.

## References
