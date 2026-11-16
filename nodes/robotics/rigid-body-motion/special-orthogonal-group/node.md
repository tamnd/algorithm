---
tag: JTD8RC
kind: definition
slug: special-orthogonal-group
name: "Special orthogonal group SO(3)"
aliases:
- SO(3)
- 3D rotation group
area: robotics/rigid-body-motion
level: core
summary: "The group of 3 by 3 real matrices R with R^T R = I and det R = 1: the rotations of space about the origin, with matrix product as composition."
prereqs: [determinant, eigenvalue]
see_also: [rodrigues-rotation-formula, so3-logarithm-map, euler-rotation-theorem, unit-quaternion-rotation, euler-angles, axis-angle-representation, special-euclidean-group, rotation-averaging]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.1 (properties of rotation matrices, the definition of SO(3) and its uses)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2.1 (properties of rotation matrices)
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the rotation group as a Lie group, with its exponential and logarithm maps
---

The special orthogonal group SO(3) is the set of $3 \times 3$ real matrices $R$ with $R^{\mathsf T}R = I$ and $\det R = 1$.
These matrices are exactly the rotations of three-dimensional space about the origin: they keep lengths, angles and the handedness of a frame.
With the matrix product as the operation, they form a group, and with its smooth structure it is a Lie group of dimension 3.
In robotics a rotation matrix describes the orientation of one frame relative to another, and it maps coordinates in the second frame to coordinates in the first.
Every element is a rotation by an angle about one axis, by [Euler's rotation theorem](/euler-rotation-theorem/), and [Rodrigues' formula](/rodrigues-rotation-formula/) builds the matrix from the axis and the angle.

## Definition

$$SO(3) = \{ R \in \mathbb{R}^{3 \times 3} : R^{\mathsf T}R = I,\ \det R = 1 \}.$$

The group of all orthogonal matrices, with $\det R = \pm 1$, is $O(3)$; SO(3) is the part with $\det R = +1$.
The condition $R^{\mathsf T}R = I$ says that the columns of $R$ are orthonormal; it gives six independent equations on nine entries, so three numbers are left free.
The condition $\det R = 1$ excludes the reflections, which reverse handedness.

Frames.
Let $\{s\}$ and $\{b\}$ be two right-handed orthonormal frames with a common origin.
The rotation matrix $R_{sb}$ has as its columns the unit axes of $\{b\}$, written in the coordinates of $\{s\}$.
For a point with coordinates $x_b$ in $\{b\}$, its coordinates in $\{s\}$ are $x_s = R_{sb} x_b$.
The rules of composition are $R_{ac} = R_{ab}R_{bc}$ and $R_{ba} = R_{ab}^{-1} = R_{ab}^{\mathsf T}$.

Properties, all proved from the definition:

- **Group.** The product of two rotations is a rotation, and $R^{-1} = R^{\mathsf T}$ is a rotation. Matrix multiplication is associative.
- **Not commutative.** In general $R_1 R_2 \ne R_2 R_1$.
- **Isometry.** $|Rx| = |x|$ and $Rx \cdot Ry = x \cdot y$, and $R(x \times y) = Rx \times Ry$.
- **Eigenvalues.** The eigenvalues are $1$, $e^{i\theta}$ and $e^{-i\theta}$ for an angle $\theta \in [0, \pi]$, so $\operatorname{tr} R = 1 + 2\cos\theta$. The eigenvector for 1 is the axis of rotation.
- **Manifold.** SO(3) is a compact, connected manifold of dimension 3. It is not simply connected; the unit quaternions cover it twice.
- **Lie algebra.** The tangent space at $I$ is the set $\mathfrak{so}(3)$ of $3 \times 3$ skew-symmetric matrices $[\omega]$, and the exponential map $[\omega] \mapsto e^{[\omega]}$ is onto SO(3).

## Examples and non-examples

- The rotations about the coordinate axes:
  $R_z(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}$, and $R_x(\theta)$ and $R_y(\theta)$ in the same way.
- The product $R_x(\pi/2)R_z(\pi/2) = \begin{pmatrix} 0 & -1 & 0 \\ 0 & 0 & -1 \\ 1 & 0 & 0 \end{pmatrix}$, but $R_z(\pi/2)R_x(\pi/2) = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$. The two differ, so the group is not commutative.
- The second matrix above permutes the axes, $x \to y \to z \to x$. Its trace is 0, so its angle is $\theta = 2\pi/3$, and its axis is $(1, 1, 1)/\sqrt3$.
- $\operatorname{diag}(1, -1, -1)$ is in SO(3): it is the rotation by $\pi$ about the $x$ axis.
- Non-example: $\operatorname{diag}(1, 1, -1)$ is orthogonal, but its determinant is $-1$. It is the reflection in the $xy$ plane, and it is in $O(3)$ but not in SO(3).
- Non-example: the matrix $\begin{pmatrix} 1 & 1 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ has determinant 1, but its columns are not orthonormal. It is a shear, not a rotation.
- Non-example: a matrix computed in floating point, such as a long product of rotations, is in general only close to SO(3). One projects it back with the [singular value decomposition](/singular-value-decomposition/), with the [QR decomposition](/qr-decomposition/), or with the [Gram-Schmidt process](/gram-schmidt-process/).

## Related definitions

- Parametrizations: [Euler angles](/euler-angles/), [roll-pitch-yaw angles](/roll-pitch-yaw-angles/), the [axis-angle representation](/axis-angle-representation/), [unit quaternions](/unit-quaternion-rotation/) and [Cayley parameters](/cayley-rotation-parameters/). The [Stuelpnagel theorem](/stuelpnagel-theorem/) says that no three-parameter set can be both global and free of singularities.
- [Rodrigues' formula](/rodrigues-rotation-formula/) and the [logarithm map of SO(3)](/so3-logarithm-map/) connect SO(3) with the vectors $\omega \in \mathbb{R}^3$.
- The [angular velocity](/angular-velocity/) is the velocity of a curve in SO(3).
- The [special Euclidean group](/special-euclidean-group/) SE(3) adds a translation to each rotation.
- The [Kabsch algorithm](/kabsch-algorithm/) finds the element of SO(3) that best aligns two point sets, and [rotation averaging](/rotation-averaging/) finds a mean of many elements.

## References
