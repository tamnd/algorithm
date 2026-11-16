---
tag: YTDVB1
kind: definition
slug: dual-quaternion
name: Dual quaternion
aliases:
- unit dual quaternion
area: robotics/rigid-body-motion
level: advanced
summary: A quaternion with dual number entries; unit dual quaternions represent rigid motions as quaternions represent rotations.
model: real-ram
prereqs: [screw-motion, special-euclidean-group]
see_also: [unit-quaternion-rotation, chasles-theorem, rigid-body-twist, se3-exponential-map, spherical-linear-interpolation, robot-pose, homogeneous-transformation-matrix, product-of-exponentials-formula]
sources:
  - paper: doi:10.1112/plms/s1-4.1.381
    title: "W. K. Clifford, Preliminary sketch of biquaternions, Proceedings of the London Mathematical Society s1-4, 381 to 395, 1873"
    locator: the whole paper (biquaternions, with a unit whose square is zero, and their use for motors)
  - paper: doi:10.1007/BF01199824
    title: "E. Study, Von den Bewegungen und Umlegungen, Mathematische Annalen 39(4), 441 to 565, 1891"
    locator: the whole paper (dual numbers and the representation of the motions of space)
  - paper: doi:10.1177/02783649922066213
    title: "Konstantinos Daniilidis, Hand-eye calibration using dual quaternions, The International Journal of Robotics Research 18(3), 286 to 298, 1999"
    locator: the dual quaternion of a screw motion and the hand-eye calibration that uses it
  - paper: doi:10.1145/1409625.1409627
    title: "Ladislav Kavan, Steven Collins, Jiří Žára and Carol O'Sullivan, Geometric skinning with approximate dual quaternion blending, ACM Transactions on Graphics 27(4), article 105, 2008"
    locator: the dual quaternion product, the conversion from a rigid transformation, the sign choice and the blending with normalization
---

A dual quaternion is a quaternion whose four entries are dual numbers $a + \varepsilon b$ with $\varepsilon^2 = 0$, or, the same thing, a pair of quaternions written $\sigma = r + \varepsilon d$.
A unit dual quaternion holds a rigid motion of space in 8 numbers: the real part $r$ is the [unit quaternion](/unit-quaternion-rotation/) of the rotation, and the dual part $d$ is half the translation times $r$.
The product of two unit dual quaternions is the composition of their motions, in the same way as the product of unit quaternions composes rotations.
Unit dual quaternions double cover the [special Euclidean group](/special-euclidean-group/) SE(3): $\sigma$ and $-\sigma$ give the same motion, as $q$ and $-q$ give the same rotation.
A unit dual quaternion is also the algebraic form of a [screw motion](/screw-motion/): its dual angle holds the rotation angle and the slide, and its dual axis holds the screw axis as a line.
Clifford introduced the algebra in 1873 under the name biquaternions, and Study used it in 1891 for the motions of space.

## Definition

A **dual number** is $\hat a = a + \varepsilon b$ with real $a, b$ and $\varepsilon^2 = 0$, $\varepsilon \neq 0$.
For a smooth function, $f(a + \varepsilon b) = f(a) + \varepsilon b f'(a)$; for example $\cos(\theta + \varepsilon d) = \cos\theta - \varepsilon d \sin\theta$.

A **dual quaternion** is $\sigma = r + \varepsilon d$ with Hamilton quaternions $r$ (the real part) and $d$ (the dual part), scalar first.
The product follows from $\varepsilon^2 = 0$:

$$(r_1 + \varepsilon d_1)(r_2 + \varepsilon d_2) = r_1 r_2 + \varepsilon (r_1 d_2 + d_1 r_2).$$

It is associative and not commutative.
Two conjugates are used: the quaternion conjugate $\sigma^* = r^* + \varepsilon d^*$, and the combined conjugate $r^* - \varepsilon d^*$, which moves points.
The norm is $\sigma \sigma^* = |r|^2 + 2\varepsilon (r \cdot d)$, where $r \cdot d$ is the dot product of the two 4-vectors.

$\sigma$ is a **unit dual quaternion** when $\sigma \sigma^* = 1$, that is

$$|r| = 1 \quad\text{and}\quad r \cdot d = 0 .$$

These are two scalar conditions on 8 numbers, so the unit dual quaternions form a 6-dimensional set, one dimension for each degree of freedom of a rigid body.
Each unit dual quaternion has the inverse $\sigma^{-1} = \sigma^*$.

**The rigid motion of a unit dual quaternion.**
Let $x \mapsto R x + t$ be a rigid motion, and let $r$ be a unit quaternion of $R$.
Write $t$ and $x$ as pure quaternions $(0, t)$ and $(0, x)$.
The dual quaternion of the motion is

$$\sigma = r + \varepsilon\, \tfrac12\, t\, r, \qquad t = 2\, d\, r^* .$$

It is unit: $r \cdot d$ is the scalar part of $r^* d = \tfrac12 r^* t r$, which is a pure quaternion, so $r \cdot d = 0$.
A point is the dual quaternion $1 + \varepsilon x$, and the motion acts by the sandwich

$$\sigma\,(1 + \varepsilon x)\,(r^* - \varepsilon d^*) = 1 + \varepsilon (R x + t).$$

To check it, expand to $1 + \varepsilon (d r^* + r x r^* - r d^*)$, and use $d r^* = \tfrac12 t$, $r d^* = \tfrac12 r r^* t^* = -\tfrac12 t$ and $r x r^* = R x$.
Composition is the product: if $\sigma_1$ and $\sigma_2$ belong to $T_1$ and $T_2$, then

$$\sigma_1 \sigma_2 = r_1 r_2 + \varepsilon\, \tfrac12 (t_1 + r_1 t_2 r_1^*)\, r_1 r_2 ,$$

which is the dual quaternion of $T_1 T_2$, with rotation $R_1 R_2$ and translation $R_1 t_2 + t_1$.
The map from unit dual quaternions to SE(3) is a group homomorphism onto SE(3), and its kernel is $\{1, -1\}$: $\sigma$ and $-\sigma$ have the same $R$, and the same $t = 2 d r^*$.
So unit dual quaternions double cover SE(3), as unit quaternions double cover the rotation group.

**Screw form.**
By [Chasles' theorem](/chasles-theorem/), every rigid motion is a screw motion: a rotation by $\theta$ about a line with unit direction $s$ through a point $q$, and a slide $d_s = h\theta$ along it, with pitch $h$.
Let the dual angle be $\hat\theta = \theta + \varepsilon d_s$, and let the dual axis be $\hat s = s + \varepsilon m$ with the moment $m = q \times s$ (the Plücker coordinates of the line).
Then

$$\sigma = \cos\frac{\hat\theta}{2} + \hat s \sin\frac{\hat\theta}{2}
= \Big(\cos\frac{\theta}{2},\ s \sin\frac{\theta}{2}\Big) + \varepsilon \Big(-\frac{d_s}{2}\sin\frac{\theta}{2},\ m \sin\frac{\theta}{2} + \frac{d_s}{2} \cos\frac{\theta}{2}\, s\Big).$$

This is the same shape as $(\cos\frac{\theta}{2}, s \sin\frac{\theta}{2})$ for a rotation, with dual numbers in place of reals.
Because $\hat s \hat\theta = \theta (s + \varepsilon v)$ with $v = -s \times q + h s$, the unit [twist](/rigid-body-twist/) $\mathcal S = (s, v)$ gives $\sigma = \exp\big(\tfrac{\theta}{2}(s + \varepsilon v)\big)$, the dual quaternion form of the [exponential](/se3-exponential-map/) $e^{[\mathcal S]\theta}$.

**Operations.**
The code on this page follows these lines; quaternion products are Hamilton products.

```pseudo id=main
MUL(a, b), FROM-POSE(q, t), TO-POSE(σ), APPLY(σ, x)
L1  (r1, d1) ← a ; (r2, d2) ← b
L2  MUL returns (r1 r2, r1 d2 + d1 r2)
L3  FROM-POSE returns (q, ½ (0, t) q)
L4  TO-POSE: (r, d) ← σ ; return (r, vector part of 2 d r*)
L5  APPLY: y ← MUL(MUL(σ, (1, (0, x))), (r*, -d*))
L6  APPLY returns the vector part of the dual part of y
```

One product costs three quaternion products, 48 multiplications and 40 additions.
The product of two 4x4 rigid transforms costs 36 multiplications and 27 additions, so the dual quaternion product is not faster; its gains are 8 numbers in place of 12, a cheap renormalization and the smooth blending below.
After many products, rounding moves $\sigma$ off the unit conditions.
To renormalize, divide both parts by $|r|$ and then remove from $d$ its component along $r$: $d \leftarrow d - (r \cdot d)\, r$.

## Examples and non-examples

**A quarter turn with a translation.**
Let $R = R_z(\pi/2)$ and $t = (1, 1, 0)$.
Then $r = (\cos\frac{\pi}{4}, 0, 0, \sin\frac{\pi}{4}) = (0.70711, 0, 0, 0.70711)$.
The product $(0, 1, 1, 0)(0.70711, 0, 0, 0.70711)$ is $(0, 1.41421, 0, 0)$, so $d = (0, 0.70711, 0, 0)$ and

$$\sigma = (0.70711, 0, 0, 0.70711) + \varepsilon (0, 0.70711, 0, 0).$$

The unit conditions hold: $|r| = 1$ and $r \cdot d = 0$.
The point $x = (1, 0, 0)$ goes to $R x + t = (0, 1, 0) + (1, 1, 0) = (1, 2, 0)$.
The same motion is the screw with axis $s = (0, 0, 1)$ through $q = (0, 1, 0)$, pitch 0 and $\theta = \pi/2$: the moment is $m = q \times s = (1, 0, 0)$, and the screw form gives $(0.70711, 0, 0, 0.70711) + \varepsilon\, (0, 0.70711 \cdot (1, 0, 0))$, the same $\sigma$.
The point $(0, 1, 0)$ is on the axis, and indeed $R (0, 1, 0) + t = (-1, 0, 0) + (1, 1, 0) = (0, 1, 0)$.

**Composition.**
Apply the same motion twice.
The real part is $r^2 = (0, 0, 0, 1)$, a half turn about $z$.
The dual part is $r d + d r = (0, 0.5, 0.5, 0) + (0, 0.5, -0.5, 0) = (0, 1, 0, 0)$.
Then $t = 2 d r^* = 2 (0, 1, 0, 0)(0, 0, 0, -1) = (0, 0, 2, 0)$, so the translation is $(0, 2, 0)$.
The matrix product gives the same: $R_z(\pi/2) (1, 1, 0) + (1, 1, 0) = (-1, 1, 0) + (1, 1, 0) = (0, 2, 0)$.

**Pure translation and pure rotation.**
A translation by $t$ is $1 + \varepsilon \tfrac12 (0, t)$.
A rotation about a line through the origin is $r + \varepsilon\, 0$.
A half turn about the $x$ axis is $(0, 1, 0, 0) + \varepsilon\, 0$.

**The double cover.**
$-\sigma = (-0.70711, 0, 0, -0.70711) + \varepsilon (0, -0.70711, 0, 0)$ is a different dual quaternion with the same motion: $R(-r) = R(r)$, and $2(-d)(-r)^* = 2 d r^*$.
A program that compares or averages dual quaternions must handle both signs.

**Non-example: a dual quaternion that is not unit.**
$\sigma = 1 + \varepsilon (1, 0, 0, 0)$ has $|r| = 1$ but $r \cdot d = 1$.
The formula $2 d r^*$ gives $(2, 0, 0, 0)$, which has a scalar part and so is not a translation.
$\sigma$ is not a rigid motion; to use it, first renormalize, which here gives $1$.

**Non-example: a dual quaternion with zero real part.**
$\sigma = \varepsilon\, (1, 0, 0, 0)$ has no inverse, because $\varepsilon \cdot \varepsilon = 0$.
Dual quaternions are not a division algebra.

**Non-example: linear blending without normalization.**
The average $\tfrac12 (\sigma_1 + \sigma_2)$ of two unit dual quaternions is usually not unit.
Kavan, Collins, Žára and O'Sullivan blend $\sum_i w_i \sigma_i$ and then normalize; before the sum they flip the sign of each $\sigma_i$ whose real part has a negative dot product with that of the first, so that all lie on one side of the double cover.
The result is a rigid motion, which is why this blending removes the volume loss of linear blend skinning.

## Related definitions

- [Unit quaternion rotation](/unit-quaternion-rotation/) is the real part alone; a dual quaternion with $d = 0$ is a rotation about a line through the origin.
- [Screw motion](/screw-motion/) and [Chasles' theorem](/chasles-theorem/) give the geometric meaning of the dual angle and the dual axis.
- [Twists](/rigid-body-twist/) and the [SE(3) exponential](/se3-exponential-map/) give the same motion as $e^{[\mathcal S]\theta}$; the dual quaternion is $\exp(\frac{\theta}{2}(s + \varepsilon v))$.
- The [homogeneous transformation matrix](/homogeneous-transformation-matrix/) is the 4x4 form of the same element of SE(3).
- Screw linear interpolation, $\sigma_1 (\sigma_1^* \sigma_2)^\tau$ for $\tau \in [0, 1]$, moves along the constant screw from $\sigma_1$ to $\sigma_2$; it is the dual form of [spherical linear interpolation](/spherical-linear-interpolation/).
- Study's kinematic mapping sends a motion to the point $[\sigma]$ of real projective 7-space; the condition $r \cdot d = 0$ is the Study quadric.
- Daniilidis writes the hand-eye equation $AX = XB$ with dual quaternions, which solves for the rotation and the translation in one step.

## References
