---
tag: X85DD4
kind: definition
slug: axis-angle-representation
name: Axis-angle representation
aliases:
- angle-axis representation
- rotation vector
area: robotics/rigid-body-motion
level: intro
summary: A rotation given by a unit axis and an angle, or by one vector whose direction is the axis and whose length is the angle.
prereqs: [euler-rotation-theorem, rodrigues-rotation-formula]
see_also: [so3-logarithm-map, unit-quaternion-rotation, cayley-rotation-parameters, euler-angles, stuelpnagel-theorem, spherical-linear-interpolation, rotation-averaging, error-state-kalman-filter]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.3 (exponential coordinate representation of rotation, the matrix exponential and the matrix logarithm of rotations)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Sections 2.2 and 2.3 (exponential coordinates for rotation and other representations)
---

The axis-angle representation gives a rotation of space by a unit vector $\hat\omega$, the axis, and an angle $\theta$, the amount of turn about that axis by the right-hand rule.
The same data fit in one vector $r = \theta\hat\omega$, the rotation vector, whose direction is the axis and whose length is the angle.
By [Euler's rotation theorem](/euler-rotation-theorem/) every rotation has this form, and [Rodrigues' formula](/rodrigues-rotation-formula/) turns it into a matrix.
The rotation vector is also called the exponential coordinates of the rotation, because the matrix is the [matrix exponential](/matrix-exponential/) $e^{[r]}$.

## Definition

An **axis-angle pair** is a pair $(\hat\omega, \theta)$ with $\hat\omega \in \mathbb{R}^3$, $|\hat\omega| = 1$, and $\theta \in \mathbb{R}$.
It stands for the rotation

$$R = \operatorname{Rot}(\hat\omega, \theta) = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2 ,$$

where $[\hat\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\hat\omega$.
The **rotation vector** is $r = \theta\hat\omega \in \mathbb{R}^3$, and it stands for $R = e^{[r]}$.
The zero vector stands for $I$.

**The canonical choice.**
Many pairs give the same $R$: $(\hat\omega, \theta + 2\pi k)$ and $(-\hat\omega, -\theta)$ for every integer $k$.
The usual choice is $\theta \in [0, \pi]$, so that $|r| \le \pi$.
With this choice:

- $R = I$ has $\theta = 0$ and no defined axis, and $r = 0$.
- $R \ne I$ with $\operatorname{tr} R \ne -1$ has exactly one canonical $r$, with $0 < |r| < \pi$.
- $\operatorname{tr} R = -1$ (a half turn) has the two vectors $r$ and $-r$, with $|r| = \pi$.

So the canonical rotation vectors fill the closed ball of radius $\pi$, with each pair of opposite points on its surface standing for one rotation.

**From the matrix to the vector.**
$\cos\theta = (\operatorname{tr} R - 1)/2$, and for $0 < \theta < \pi$ the axis comes from the skew part, $[\hat\omega] = (R - R^{\mathsf T})/(2\sin\theta)$.
Near $\theta = 0$ and $\theta = \pi$ these formulas lose precision, and the [logarithm map of SO(3)](/so3-logarithm-map/) handles both cases.

**To a quaternion.**
The pair gives the [unit quaternion](/unit-quaternion-rotation/) $q = (\cos\tfrac\theta2,\ \sin\tfrac\theta2\,\hat\omega)$ in the scalar-first Hamilton convention, and $-q$ gives the same rotation.

## Examples and non-examples

**The (1, 1, 1) rotation.**
$R = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ has $\operatorname{tr} R = 0$, so $\theta = 2\pi/3 \approx 2.0943951$.
The skew part gives $\hat\omega = (1, 1, 1)/\sqrt3$, and $r = \theta\hat\omega \approx (1.2092, 1.2092, 1.2092)$.
The quaternion is $(\cos\tfrac\pi3, \sin\tfrac\pi3\,\hat\omega) = (0.5, 0.5, 0.5, 0.5)$.

**A quarter turn about $z$.**
$R_z(\pi/2)$ has $r = (0, 0, \pi/2) \approx (0, 0, 1.5708)$ and the quaternion $(0.70711, 0, 0, 0.70711)$.

**A half turn about $x$.**
$R_x(\pi) = \operatorname{diag}(1, -1, -1)$ has $\theta = \pi$, and both $r = (\pi, 0, 0)$ and $r = (-\pi, 0, 0)$ are canonical.
The skew part is zero, so the axis must come from $R + I = \operatorname{diag}(2, 0, 0)$, whose nonzero column is along $x$.
The quaternion is $(0, 1, 0, 0)$, and $(0, -1, 0, 0)$ is the same rotation.

**A vector longer than $\pi$.**
$r = (0, 0, 3\pi/2)$ is a valid rotation vector, but not the canonical one.
It is the same rotation as $(0, 0, -\pi/2)$, which the logarithm returns.

**Non-example: adding rotation vectors.**
Let $r_1 = (\pi/2, 0, 0)$ and $r_2 = (0, \pi/2, 0)$.
The product $e^{[r_1]}e^{[r_2]} = R_x(\pi/2)R_y(\pi/2)$ is the (1, 1, 1) rotation above, with $r \approx (1.2092, 1.2092, 1.2092)$.
The product in the other order, $R_y(\pi/2)R_x(\pi/2)$, has $r \approx (1.2092, 1.2092, -1.2092)$.
The sum $r_1 + r_2 = (\pi/2, \pi/2, 0)$ is a turn by $\pi/\sqrt2 \approx 2.2214$ about $(1, 1, 0)/\sqrt2$, which is neither.
Rotation vectors add only when they are parallel. For small vectors, the error of the sum is of second order, $\tfrac12 r_1 \times r_2$ by the Baker-Campbell-Hausdorff series.

**Non-example: an axis that is not a unit vector.**
The pair $((0, 0, 2), \pi/2)$ is not an axis-angle pair.
Read as a rotation vector, $(0, 0, 2) \cdot \pi/2 = (0, 0, \pi)$ is a half turn and not a quarter turn.
Code that takes an axis must normalize it or reject it.

**Non-example: Euler angles.**
[Euler angles](/euler-angles/) are three numbers too, but they are three turns about fixed or moving coordinate axes, not one turn.
The vector $(\alpha, \beta, \gamma)$ of Euler angles is not a rotation vector.

## Related definitions

- [Rodrigues' rotation formula](/rodrigues-rotation-formula/): the map from the pair to the matrix.
- [Logarithm map of SO(3)](/so3-logarithm-map/): the map from the matrix to the canonical rotation vector, with care at $\theta = 0$ and $\theta = \pi$.
- [Unit quaternion](/unit-quaternion-rotation/): the half-angle form of the same data, with no singular point.
- [Cayley rotation parameters](/cayley-rotation-parameters/): the Gibbs vector $\tan\tfrac\theta2\,\hat\omega$, the same axis with another function of the angle, which is infinite at a half turn.
- [Stuelpnagel theorem](/stuelpnagel-theorem/): no three numbers describe all rotations without a singular point. For the rotation vector, the canonical choice jumps at $|r| = \pi$, and the map $r \mapsto e^{[r]}$ is not locally invertible at $|r| = 2\pi$.
- [Spherical linear interpolation](/spherical-linear-interpolation/): $R(t) = R_0\, e^{t[r]}$ with $r$ the rotation vector of $R_0^{\mathsf T}R_1$ turns at a constant rate about a fixed axis.
- [Rotation averaging](/rotation-averaging/): the angle $|r|$ of $R_1^{\mathsf T}R_2$ is the geodesic distance between two rotations.
- [Error-state Kalman filter](/error-state-kalman-filter/): a small rotation vector is the attitude error state, because near $r = 0$ the representation has no singular point and $e^{[r]} \approx I + [r]$.
- [Screw motion](/screw-motion/): the same idea for rigid motions, an axis line, an angle and a slide along the line.

## References
