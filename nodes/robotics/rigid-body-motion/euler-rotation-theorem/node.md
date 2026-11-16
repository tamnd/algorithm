---
tag: SRDX8E
kind: theorem
slug: euler-rotation-theorem
name: Euler's rotation theorem
aliases:
- Euler's theorem on rotations
area: robotics/rigid-body-motion
level: intro
summary: Every rotation of space about a fixed point is a rotation by some angle about a single axis through that point.
prereqs: [special-orthogonal-group, eigenvalue]
see_also: [axis-angle-representation, rodrigues-rotation-formula, so3-logarithm-map, chasles-theorem, unit-quaternion-rotation, characteristic-polynomial, determinant, euler-angles]
sources:
  - paper: "Leonhard Euler, Formulae generales pro translatione quacunque corporum rigidorum, Novi Commentarii Academiae Scientiarum Petropolitanae 20 (1775), 189 to 207, published 1776; Opera Omnia, series 2, volume 9, 84 to 98 (Eneström number E478)"
    locator: the whole paper (the theorem that a sphere turned about its center keeps one diameter in place)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2.2 (exponential coordinates for rotation, Theorem 2.6, Euler)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.3 (exponential coordinate representation of rotation)
---

Euler's rotation theorem says that every rotation of space that keeps a point fixed is a rotation by one angle about one axis through that point.
In matrix form, every $R$ in the [special orthogonal group](/special-orthogonal-group/) SO(3) has a unit vector $\hat\omega$ with $R\hat\omega = \hat\omega$, and $R$ turns the plane orthogonal to $\hat\omega$ by an angle $\theta$.
The theorem is the reason why the [axis-angle representation](/axis-angle-representation/) covers every rotation, and why the exponential of SO(3) in [Rodrigues' formula](/rodrigues-rotation-formula/) is onto.
The proof below uses only the [determinant](/determinant/) and the [eigenvalue](/eigenvalue/) 1 of $R$.

## Statement

**Theorem.** Let $R$ be a real $3 \times 3$ matrix with $R^{\mathsf T}R = I$ and $\det R = 1$.
Then there is a unit vector $\hat\omega$ and an angle $\theta \in [0, \pi]$ such that $R\hat\omega = \hat\omega$ and, for every unit vector $a$ orthogonal to $\hat\omega$,

$$Ra = \cos\theta\, a + \sin\theta\, (\hat\omega \times a) .$$

The angle satisfies $\operatorname{tr} R = 1 + 2\cos\theta$.
If $R \ne I$, the fixed vectors of $R$ form exactly one line, so the axis is unique up to its sign.
For $0 < \theta < \pi$, the pair $(\hat\omega, \theta)$ is unique.
For $\theta = \pi$, both $(\hat\omega, \pi)$ and $(-\hat\omega, \pi)$ give $R$.
For $R = I$, $\theta = 0$ and every axis works.

A distance-preserving map $f$ of space with $f(0) = 0$ is such a matrix or a reflection of one, so the theorem covers every rigid motion that keeps a point fixed and keeps the handedness of space.

## In plain words

Take a ball and turn it in any way you like about its center, in one move or in many moves.
Then look at the final position.
There is always one line through the center that ends where it started.
The whole change is one single turn about that line.
You can find the size of the turn from the matrix with one simple sum.
If the ball moved at all, there is only one such line.
A turn by half a circle is a special case: you get the same result if you turn the other way about the same line.

## Proof

**Step 1: the eigenvalue 1.**
Since $R^{\mathsf T}R = I$ and $\det R = 1$,

$$\det(R - I) = \det\big(R(I - R^{\mathsf T})\big) = \det R \cdot \det\big((I - R)^{\mathsf T}\big) = \det(I - R) = (-1)^3 \det(R - I) .$$

So $\det(R - I) = -\det(R - I)$, and $\det(R - I) = 0$.
Thus 1 is an eigenvalue of $R$, and there is a unit vector $\hat\omega$ with $R\hat\omega = \hat\omega$.

**Step 2: the plane orthogonal to the axis.**
Let $P$ be the plane of vectors orthogonal to $\hat\omega$.
For $x \in P$, $(Rx) \cdot \hat\omega = (Rx) \cdot (R\hat\omega) = x \cdot \hat\omega = 0$, because $R$ keeps dot products.
So $R$ maps $P$ into $P$.
Choose a unit vector $a \in P$ and put $b = \hat\omega \times a$.
Then $(\hat\omega, a, b)$ is a right-handed orthonormal basis, and in this basis $R$ is the block matrix $\operatorname{diag}(1, A)$, where $A$ is a $2 \times 2$ orthogonal matrix.
Since $\det R = 1 \cdot \det A$, $\det A = 1$.
The first column of $A$ is a unit vector $(c, s)$, and the second column is a unit vector orthogonal to it, so it is $\pm(-s, c)$.
Only the sign $+$ gives $\det A = 1$.
Write $c = \cos\theta$ and $s = \sin\theta$ for a $\theta \in (-\pi, \pi]$.
Then $Ra = \cos\theta\, a + \sin\theta\, b$, which is the formula of the statement.
If $\theta < 0$, replace $\hat\omega$ by $-\hat\omega$: then $b$ changes sign, and the same $R$ has the angle $-\theta \in (0, \pi)$.
So we may take $\theta \in [0, \pi]$.

**Step 3: the trace.**
The trace does not depend on the basis, so $\operatorname{tr} R = 1 + \operatorname{tr} A = 1 + 2\cos\theta$.
This fixes $\theta \in [0, \pi]$ from $R$ alone.

**Step 4: uniqueness of the axis.**
Suppose $R \ne I$, so $\theta \ne 0$.
Let $x = \alpha\hat\omega + y$ with $y \in P$ be a fixed vector.
Then $Rx = \alpha\hat\omega + Ay$, so $Ay = y$.
For $y \ne 0$, this means $A$ has the eigenvalue 1, and a planar rotation by $\theta$ has the real eigenvalue 1 only when $\theta = 0$, because $\det(A - I) = (\cos\theta - 1)^2 + \sin^2\theta = 2(1 - \cos\theta)$.
So $y = 0$, and every fixed vector lies on the line of $\hat\omega$.
For $0 < \theta < \pi$, the sign of $\hat\omega$ is fixed by the condition $\sin\theta > 0$ in Step 2.
For $\theta = \pi$, $\sin\theta = 0$, and the formula $Ra = -a$ does not change when $\hat\omega$ changes sign.

**Step 5: maps that keep a point fixed.**
Let $f$ keep distances and $f(0) = 0$.
Then $|f(x)| = |x|$ for every $x$, and from $|f(x) - f(y)|^2 = |x - y|^2$ we get $f(x) \cdot f(y) = x \cdot y$.
Expanding $|f(x + y) - f(x) - f(y)|^2$ with this rule gives 0, and in the same way $f(\lambda x) = \lambda f(x)$.
So $f$ is linear, its matrix $Q$ has $Q^{\mathsf T}Q = I$, and $\det Q = \pm 1$.
If the motion keeps the handedness of space, $\det Q = 1$ and Steps 1 to 4 apply. $\square$

### A check by hand

Let $R = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$, the map $(x, y, z) \mapsto (z, x, y)$.
It is orthogonal, and $\det R = 1$.

- The fixed vectors solve $(z, x, y) = (x, y, z)$, so $x = y = z$, and $\hat\omega = (1, 1, 1)/\sqrt3$.
- $\operatorname{tr} R = 0 = 1 + 2\cos\theta$, so $\cos\theta = -1/2$ and $\theta = 2\pi/3 \approx 2.0943951$.
- For the sign, take $a = (1, -1, 0)/\sqrt2$. Then $Ra = (0, 1, -1)/\sqrt2$ and $\hat\omega \times a = (1, 1, -2)/\sqrt6$. The product $Ra \cdot (\hat\omega \times a) = 3/\sqrt{12} = \sqrt3/2 > 0$, which is $\sin\theta$. So the angle is $+2\pi/3$ about $+\hat\omega$.

The [logarithm map of SO(3)](/so3-logarithm-map/) returns the same answer as the vector $\theta\hat\omega \approx (1.2092, 1.2092, 1.2092)$.

## Consequences

- **Composition.** The product of two rotations about the same point is a rotation, so by the theorem it is again one turn about one axis. This was the question that Euler answered.
- **Exponential coordinates.** With [Rodrigues' formula](/rodrigues-rotation-formula/), every $R \in SO(3)$ is $e^{[\hat\omega]\theta}$ with $\theta \in [0, \pi]$. The map $\exp : \mathfrak{so}(3) \to SO(3)$ is onto, and the [axis-angle representation](/axis-angle-representation/) covers every rotation.
- **Eigenvalues.** The eigenvalues of $R$ are $1$, $e^{i\theta}$ and $e^{-i\theta}$. The [characteristic polynomial](/characteristic-polynomial/) is $(\lambda - 1)(\lambda^2 - 2\cos\theta\,\lambda + 1)$.
- **Two fixed directions are enough.** A rotation that fixes two vectors that are not parallel is the identity (Step 4).
- **Unit quaternions.** The axis and the angle give the [unit quaternion](/unit-quaternion-rotation/) $(\cos\tfrac\theta2, \sin\tfrac\theta2\,\hat\omega)$, so every rotation has a quaternion.
- **Rigid motions.** [Chasles' theorem](/chasles-theorem/) adds a translation and shows that every rigid motion is a [screw motion](/screw-motion/). Its proof starts with the axis that Euler's theorem gives.

## Tightness

- **The determinant must be 1.** For $R = -I$ (the point reflection, $\det R = -1$), $\det(R - I) = -8 \ne 0$, so no vector is fixed. The reflection $\operatorname{diag}(1, 1, -1)$ fixes a whole plane and is not a turn about any axis.
- **Dimension 3, or odd.** In the plane, a rotation by $\theta \ne 0$ fixes only the origin, so there is a center but no axis. In dimension 4, $\operatorname{diag}(A_1, A_2)$ with two planar rotations by nonzero angles fixes no vector. Step 1 uses $(-1)^3 = -1$, so it works in every odd dimension, but there the rest of the space can split into several planes with different angles.
- **The angle at $\pi$.** At $\theta = \pi$ the axis is fixed only up to its sign, and the skew part $R - R^{\mathsf T}$ is zero. Methods that read the axis from the skew part fail there and must use $R + I$ instead.
- **The identity.** For $R = I$ every axis is valid. Formulas that divide by $\sin\theta$ break down near $\theta = 0$.

## History

Euler stated the theorem in 1775 in a paper on the general motion of rigid bodies, printed in 1776 in volume 20 of the Novi Commentarii of the Saint Petersburg Academy.
He stated it for a sphere turned about its center: some diameter has the same position after the motion as before, and he proved it by geometry on the sphere.
The short proof with the eigenvalue 1 belongs to linear algebra and is the one in the robotics books, for example Murray, Li and Sastry (1994).

## References
