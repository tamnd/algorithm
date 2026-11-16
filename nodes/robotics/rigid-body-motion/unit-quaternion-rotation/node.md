---
tag: F08Y79
kind: definition
slug: unit-quaternion-rotation
name: Unit quaternion representation of rotation
aliases:
- rotation quaternion
- versor
area: robotics/rigid-body-motion
level: core
summary: A rotation as a unit quaternion q = (cos(theta/2), sin(theta/2) times the axis), acting on a vector v by q v q*, where q and -q give the same rotation.
prereqs: [special-orthogonal-group, axis-angle-representation]
see_also: [shepperd-method, spherical-linear-interpolation, quaternion-kinematic-equation, stuelpnagel-theorem, euler-angles, cayley-rotation-parameters, dual-quaternion, rodrigues-rotation-formula]
sources:
  - paper: doi:10.1080/14786444408644923
    title: William Rowan Hamilton, On quaternions; or on a new system of imaginaries in algebra, Philosophical Magazine (third series) 25, 10-13, 1844
    locator: the first part of the series (the units i, j, k and their products)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.3 (unit quaternions, equations B.9 to B.12)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 2, Section 2.6 (unit quaternion)
  - paper: arxiv:1711.02508
    title: Joan Sola, Quaternion kinematics for the error-state Kalman filter, 2017
    locator: Sections 1 and 2 (quaternion algebra and the rotation by a unit quaternion) and Section 3 (the Hamilton and JPL conventions)
---

A unit quaternion is a list of four numbers $q = (w, x, y, z)$ with $w^2 + x^2 + y^2 + z^2 = 1$, and it describes a rotation of 3D space.
The rotation by the angle $\theta$ about the unit axis $\hat\omega$ has the quaternion $q = (\cos\frac\theta2, \sin\frac\theta2\,\hat\omega)$, and it moves a vector $v$ to the vector part of the product $q\,(0, v)\,q^*$, where $q^* = (w, -x, -y, -z)$.
The product of two quaternions gives the composition of the two rotations, and $q$ and $-q$ give the same rotation.
Quaternions are compact, have no singular orientation, and are easy to keep valid by normalization, so robotics, aerospace, computer graphics and CAD use them to store and combine orientations.

Notation on this page: quaternions are in the Hamilton convention with the scalar first, rotations are active (they move vectors), and $[\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\omega$, so that $[\omega]v = \omega \times v$.

## Definition

The quaternions $\mathbb{H}$ are the numbers $q = w + x\,i + y\,j + z\,k$ with real $w, x, y, z$ and the rules of Hamilton,

$$i^2 = j^2 = k^2 = ijk = -1, \qquad ij = k, \quad jk = i, \quad ki = j, \quad ji = -k.$$

Write $q = (w, u)$ with the scalar part $w$ and the vector part $u = (x, y, z) \in \mathbb{R}^3$.
The product, the conjugate and the norm are

$$(a, u)(b, v) = (ab - u \cdot v,\; a v + b u + u \times v), \qquad q^* = (w, -u), \qquad |q|^2 = q q^* = w^2 + |u|^2 .$$

The product is associative but not commutative, and $|pq| = |p|\,|q|$.
A **unit quaternion** has $|q| = 1$; the unit quaternions form the sphere $S^3$ in $\mathbb{R}^4$, and for them $q^{-1} = q^*$.
A vector $v \in \mathbb{R}^3$ is identified with the pure quaternion $(0, v)$.

**Definition.** The rotation of a unit quaternion $q$ is the map $R(q) : \mathbb{R}^3 \to \mathbb{R}^3$ with

$$(0, R(q)\,v) = q\,(0, v)\,q^* .$$

A **unit quaternion representation** of a rotation $R \in SO(3)$ is a unit quaternion $q$ with $R(q) = R$.

For $q = (w, x, y, z)$ the matrix is

$$R(q) = \begin{pmatrix} 1 - 2(y^2 + z^2) & 2(xy - wz) & 2(xz + wy) \\ 2(xy + wz) & 1 - 2(x^2 + z^2) & 2(yz - wx) \\ 2(xz - wy) & 2(yz + wx) & 1 - 2(x^2 + y^2) \end{pmatrix} = (w^2 - |u|^2) I + 2 u u^{\mathsf T} + 2w[u].$$

The basic facts are:

- **It is a rotation.** $R(q)$ keeps lengths, because $|q (0, v) q^*| = |v|$, and it has determinant 1, because $S^3$ is connected and $R(1) = I$. So $R(q)$ is in the [special orthogonal group](/special-orthogonal-group/) SO(3).
- **Axis and angle.** If $q = (\cos\frac\theta2, \sin\frac\theta2\,\hat\omega)$ with a unit $\hat\omega$, the matrix above is $I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2$, which is [Rodrigues' formula](/rodrigues-rotation-formula/). Every unit quaternion has this form with $\theta \in [0, 2\pi]$, and by [Euler's rotation theorem](/euler-rotation-theorem/) every rotation is reached.
- **Composition.** $R(pq) = R(p)\,R(q)$, because $pq\,(0, v)\,(pq)^* = p\,(q\,(0, v)\,q^*)\,p^*$.
- **Double cover.** $R(p) = R(q)$ if and only if $p = \pm q$. So $q \mapsto R(q)$ is a two-to-one map from $S^3$ onto SO(3), and the angles $\theta$ and $\theta + 2\pi$ give $q$ and $-q$.
- **Inverse.** $R(q^*) = R(q)^{\mathsf T}$, the inverse rotation.

The **JPL convention**, used in some estimation papers, writes the scalar last and takes $ij = -k$.
Its quaternion of a given rotation equals the Hamilton quaternion with the vector part negated, and its products come in the reverse order.
Convert at every interface, and never mix the two in one formula.

## Examples and non-examples

- **A quarter turn about $z$.** $\theta = \pi/2$ and $\hat\omega = (0, 0, 1)$ give $q = (\cos\frac\pi4, 0, 0, \sin\frac\pi4) = (0.70711, 0, 0, 0.70711)$. The matrix formula gives $R(q) = R_z(\pi/2)$, which maps $x$ to $y$.
- **A half turn about $x$.** $q = (0, 1, 0, 0)$, and $R(q) = \operatorname{diag}(1, -1, -1)$. Here $w = 0$, so a formula that divides by $w$ fails; [Shepperd's method](/shepperd-method/) handles this case.
- **Composition.** With $c = 0.70711$, the quarter turns $q_z = (c, 0, 0, c)$ about $z$ and $q_x = (c, c, 0, 0)$ about $x$ give $q_z q_x = (c^2,\; c(c, 0, 0) + c(0, 0, c) + (0, 0, c) \times (c, 0, 0)) = (0.5, 0.5, 0.5, 0.5)$. This is $\theta = 2\pi/3$ about $(1, 1, 1)/\sqrt3$, so $R_z(\pi/2) R_x(\pi/2) = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$, the map $(x, y, z) \mapsto (z, x, y)$. The product in the other order, $q_x q_z = (0.5, 0.5, -0.5, 0.5)$, is a different rotation.
- **Acting on a vector.** With $q = (0.5, 0.5, 0.5, 0.5)$ and $v = (1, 0, 0)$: $q\,(0, v) = (-0.5, 0.5, 0.5, -0.5)$, and $(-0.5, 0.5, 0.5, -0.5)\,q^* = (0, 0, 1, 0)$. So $R(q)$ maps $x$ to $y$, as the matrix says.
- **The sign.** $-q = (-0.5, -0.5, -0.5, -0.5)$ is the rotation by $2\pi/3 + 2\pi$ about the same axis, which is the same rotation. A test that compares two quaternions must allow both signs.
- **Non-example: a quaternion that is not a unit.** For $q = (2, 0, 0, 0)$, $q\,(0, v)\,q^* = (0, 4v)$, a scaling by $|q|^2 = 4$. After a numerical integration or many products, $|q|$ drifts from 1, and the map is then a rotation times a scaling. Divide by $|q|$ to return to $S^3$.
- **Non-example: the product without the conjugate.** $q\,(0, v)\,q$ is not a rotation of $v$ in general; for $q = (c, 0, 0, c)$ and $v = (0, 0, 1)$ it gives $(-1, 0, 0, 0)$, which is not even a pure quaternion. The conjugate on the right is essential.
- **Non-example: a pure quaternion as a rotation.** $(0, v)$ with $|v| = 1$ is the rotation by $\pi$ about $v$. It is not "the vector $v$ turned into a rotation" in any other sense.

## Related definitions

- **[Axis-angle representation](/axis-angle-representation/).** The pair $(\hat\omega, \theta)$ that the quaternion encodes by the half angle. The vector $\theta\hat\omega$ is the result of the [logarithm map of SO(3)](/so3-logarithm-map/).
- **Euler-Rodrigues parameters.** The four numbers $(\cos\frac\theta2, \sin\frac\theta2\,\hat\omega)$ under their older name, used for the composition of rotations before the quaternion notation.
- **[Cayley parameters](/cayley-rotation-parameters/).** The vector $c = u/w = \tan\frac\theta2\,\hat\omega$, the quaternion divided by its scalar part. It is singular at the half turn, where $w = 0$.
- **[Euler angles](/euler-angles/) and [roll-pitch-yaw angles](/roll-pitch-yaw-angles/).** Three-angle charts of SO(3) with [gimbal lock](/gimbal-lock/). [Stuelpnagel's theorem](/stuelpnagel-theorem/) shows that every three-parameter chart has a singular point, which is the reason for the fourth number of the quaternion.
- **[Dual quaternion](/dual-quaternion/).** Two quaternions that represent a rigid motion, a rotation and a translation together.
- **Algorithms.** [Shepperd's method](/shepperd-method/) converts a matrix to a quaternion, [spherical linear interpolation](/spherical-linear-interpolation/) interpolates two quaternions, and the [quaternion kinematic equation](/quaternion-kinematic-equation/) moves a quaternion with an angular velocity.

## References
