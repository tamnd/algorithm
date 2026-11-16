---
tag: DK6ZQE
kind: algorithm
slug: shepperd-method
name: Shepperd's method
aliases:
- quaternion from rotation matrix
area: robotics/rigid-body-motion
level: advanced
summary: Converts a rotation matrix to a unit quaternion by taking the square root of the largest of the four squared components, so that every division is by a number of at least 2.
model: floating-point-model
complexity:
  vars: {n: "the size of the matrix, fixed at n = 3"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
prereqs: [unit-quaternion-rotation]
see_also: [so3-logarithm-map, spherical-linear-interpolation, quaternion-kinematic-equation, davenport-q-method, euler-rotation-theorem, catastrophic-cancellation, rotation-averaging, axis-angle-representation]
sources:
  - paper: doi:10.2514/3.55767b
    title: S. W. Shepperd, Quaternion from rotation matrix, Journal of Guidance and Control 1(3), 223-224, 1978
    locator: the whole note (the four candidate squares from the trace and the diagonal, and the choice of the largest one)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.3 (unit quaternions, equations B.9 to B.12, with the formula that divides by 4 q0)
  - paper: arxiv:1711.02508
    title: Joan Sola, Quaternion kinematics for the error-state Kalman filter, 2017
    locator: Section 2.5 (rotation matrix and quaternion) and Section 3 (Hamilton and JPL conventions)
---

Shepperd's method converts a 3 by 3 rotation matrix $R$ into the [unit quaternion](/unit-quaternion-rotation/) $q = (w, x, y, z)$ of the same rotation.
Each of the four squares $w^2, x^2, y^2, z^2$ is a linear function of the diagonal of $R$, and each product of two components is a sum or a difference of two entries off the diagonal.
The method takes the square root of the largest square, which is at least $1/4$, and gets the other three components by division by four times that component.
The simple formula that always divides by $4w$ fails for rotations by angles near $\pi$, where $w$ is near zero; Shepperd's choice makes the result accurate in [floating point](/floating-point-model/) for every rotation.

## In plain words

A quaternion stores a turn as four numbers.
A rotation matrix stores the same turn as nine numbers.
From the matrix you can find the square of each of the four numbers by simple sums.
You can also find the product of each pair of numbers.
So you take one number as a square root, and you get the other three from the products by division.
If the number you divide by is almost zero, the answer is bad.
The method always takes the largest of the four numbers first, so the division is always safe.
The quaternion and its negative give the same turn, so the method picks the sign that makes the first number not negative.

## The problem

The input is a matrix $R = (r_{ij})$ in the [special orthogonal group](/special-orthogonal-group/) SO(3), so $R^{\mathsf T}R = I$ and $\det R = 1$.
The output is a unit quaternion $q = (w, x, y, z)$ in the Hamilton convention, scalar first, such that $R v$ is the vector part of $q\,(0, v)\,q^*$ for every $v \in \mathbb{R}^3$.
Both $q$ and $-q$ are correct answers.
The method returns the one with $w \ge 0$, which is unique when $w > 0$, that is, when the rotation angle is less than $\pi$.

For a unit quaternion, the rotation matrix is

$$R = \begin{pmatrix} 1 - 2(y^2 + z^2) & 2(xy - wz) & 2(xz + wy) \\ 2(xy + wz) & 1 - 2(x^2 + z^2) & 2(yz - wx) \\ 2(xz - wy) & 2(yz + wx) & 1 - 2(x^2 + y^2) \end{pmatrix}.$$

With $t = r_{11} + r_{22} + r_{33}$ and $w^2 + x^2 + y^2 + z^2 = 1$, this gives ten identities:

$$4w^2 = 1 + t, \quad 4x^2 = 1 + 2r_{11} - t, \quad 4y^2 = 1 + 2r_{22} - t, \quad 4z^2 = 1 + 2r_{33} - t,$$

$$4wx = r_{32} - r_{23}, \quad 4wy = r_{13} - r_{31}, \quad 4wz = r_{21} - r_{12},$$

$$4xy = r_{21} + r_{12}, \quad 4xz = r_{13} + r_{31}, \quad 4yz = r_{32} + r_{23}.$$

## The algorithm

The four squares grow in the same order as the four numbers $t, r_{11}, r_{22}, r_{33}$, because, for example, $4w^2 - 4x^2 = 2(t - r_{11})$ and $4x^2 - 4y^2 = 2(r_{11} - r_{22})$.
So line L2 finds the largest square without computing all four.

```pseudo id=main
SHEPPERD(R)                                   ▷ R in SO(3); returns q = (w, x, y, z) with w ≥ 0
L1  t ← r₁₁ + r₂₂ + r₃₃
L2  k ← the index of the largest of (t, r₁₁, r₂₂, r₃₃), from 0 to 3
L3  if k = 0 then                               ▷ w² is the largest square
L4      w ← √(1 + t) / 2
L5      (x, y, z) ← (r₃₂ - r₂₃, r₁₃ - r₃₁, r₂₁ - r₁₂) / (4w)
L6  else if k = 1 then                          ▷ x² is the largest square
L7      x ← √(1 + 2r₁₁ - t) / 2
L8      (w, y, z) ← (r₃₂ - r₂₃, r₂₁ + r₁₂, r₁₃ + r₃₁) / (4x)
L9  else if k = 2 then                          ▷ y² is the largest square
L10     y ← √(1 + 2r₂₂ - t) / 2
L11     (w, x, z) ← (r₁₃ - r₃₁, r₂₁ + r₁₂, r₃₂ + r₂₃) / (4y)
L12 else                                        ▷ z² is the largest square
L13     z ← √(1 + 2r₃₃ - t) / 2
L14     (w, x, y) ← (r₂₁ - r₁₂, r₁₃ + r₃₁, r₃₂ + r₂₃) / (4z)
L15 if w < 0 then q ← -q                        ▷ q and -q are the same rotation
L16 return q = (w, x, y, z)
```

Lines L4, L7, L10 and L13 are the square identities, each solved for one component with the positive root.
Lines L5, L8, L11 and L14 are the product identities, each divided by four times the component that is already known.
Line L15 picks one of the two signs.

## Example

Take the rotation by 170 degrees about the axis $(2, 3, 6)/7$.
Its exact quaternion is $(\cos 85°, \sin 85° \cdot (2, 3, 6)/7) = (0.0871557, 0.2846271, 0.4269406, 0.8538812)$.
Rodrigues' formula gives, to 7 digits,

$$R = \begin{pmatrix} -0.8227826 & 0.0941964 & 0.5604960 \\ 0.3918790 & -0.6202512 & 0.6794993 \\ 0.4116547 & 0.7787268 & 0.4734184 \end{pmatrix}.$$

- Line L1: $t = -0.9696155$.
- Line L2: the largest of $(-0.9696155, -0.8227826, -0.6202512, 0.4734184)$ is $r_{33}$, so $k = 3$. The four squares are $4w^2 = 0.0303845$, $4x^2 = 0.3240503$, $4y^2 = 0.7291131$ and $4z^2 = 2.9164523$.
- Line L13: $z = \sqrt{2.9164523}/2 = 0.8538812$, and $4z = 3.4155247$.
- Line L14: $w = (0.3918790 - 0.0941964)/3.4155247 = 0.0871557$, $x = (0.5604960 + 0.4116547)/3.4155247 = 0.2846271$, and $y = (0.7787268 + 0.6794993)/3.4155247 = 0.4269406$.
- Line L15: $w > 0$, so the sign stays.

The result agrees with the exact quaternion in all 7 digits.

Two short checks use the values of the area.
For $R_z(\pi/2)$, $t = 1$ and $r_{33} = 1$; line L2 takes the first of the two equal values, $k = 0$, and lines L4 and L5 give $w = 1/\sqrt2$ and $(x, y, z) = (0, 0, 2)/(4/\sqrt2)$, so $q = (0.70711, 0, 0, 0.70711)$.
For the rotation by $\pi$ about $x$, $R = \operatorname{diag}(1, -1, -1)$, $t = -1$ and $k = 1$.
Line L7 gives $x = \sqrt{1 + 2 + 1}/2 = 1$, line L8 gives $w = y = z = 0$, and the output is $q = (0, 1, 0, 0)$.
The formula that always divides by $4w$ divides by zero here.

The table is a measurement in IEEE double precision with the implementation of this page.
The axis is $(2, 3, 6)/7$, $R$ comes from Rodrigues' formula, and the error is the largest component error against the exact quaternion, up to the sign.

| angle | error of the formula that divides by $4w$ | error of SHEPPERD |
|---|---|---|
| $\pi - 10^{-1}$ | 1.7e-14 | 1.1e-16 |
| $\pi - 10^{-3}$ | 5.2e-10 | 2.2e-16 |
| $\pi - 10^{-5}$ | 9.2e-7 | 2.2e-16 |
| $\pi - 10^{-7}$ | 3.5e-2 | 1.1e-16 |
| $\pi - 10^{-9}$ | division by zero | 2.2e-16 |

At $\pi - 10^{-9}$, $1 + t$ rounds to 0, and the simple formula has nothing left to divide by.

## Correctness

The ten identities follow from the matrix of $q$ by direct expansion and from $w^2 + x^2 + y^2 + z^2 = 1$.
The four numbers $4w^2, 4x^2, 4y^2, 4z^2$ sum to 4, so the largest one is at least 1, and the component that line L2 selects has an absolute value of at least $1/2$.
The square root in that branch is of a number of at least 1, so it is defined, and the divisor is at least 2.
The branch returns that component with a positive sign and the other three from the product identities, which gives one of $\pm q$; both are the same rotation, and line L15 picks the one with $w \ge 0$.
Every unit quaternion gives a rotation, and every rotation has a unit quaternion by [Euler's rotation theorem](/euler-rotation-theorem/), so there is always a $q$ to find.
The [proof](proofs/correctness.md) gives the details and a first-order error bound in floating point.

## Complexity

The input has a fixed size, so time and space are $\Theta(1)$.
The method uses 3 comparisons, one square root, about 10 additions and 4 divisions (or one division and 3 multiplications).
It uses no trigonometric function.
The route through the [logarithm map](/so3-logarithm-map/) and the axis and angle needs an atan2, a sine and a cosine, and has its own branches near $0$ and $\pi$.

## Properties

- **Accuracy.** For a rotation matrix with rounding errors of the order of the unit roundoff $u$ in its entries, every output component has an absolute error of order $u$, at every angle. The formula that divides by $4w$ has an error of order $u / d^2$ at the angle $\pi - d$, as the table shows.
- **No special cases.** No branch tests for the identity or for the angle $\pi$. The rotations by $\pi$ about $x$, $y$ and $z$ use the branches $k = 1, 2, 3$, and the identity uses $k = 0$.
- **Uniqueness.** With line L15, the output is unique for every rotation by an angle less than $\pi$. At the angle $\pi$, $w = 0$ and both $q$ and $-q$ have $w = 0$; the output is then the one with a positive component $k$.
- **Continuity.** All four branches compute the same $q$ in exact arithmetic, so the switch between branches does not make a jump. The only jump is the sign flip of line L15 at the angle $\pi$, which no continuous choice can avoid.
- **Input that is not orthogonal.** If $R$ is close to a rotation, the output is close to the quaternion of that rotation, but its length is not exactly 1. Normalize it if the length matters.

## Variants and improvements

- **Normalization at the end.** Divide $q$ by its length. This costs one more square root and makes the output a unit quaternion even when $R$ is slightly off SO(3).
- **The sign of a time series.** For a sequence of rotations, as in a recorded trajectory, choose the sign of each quaternion so that its dot product with the previous one is positive, and not by $w \ge 0$. This keeps the sequence continuous, which [spherical linear interpolation](/spherical-linear-interpolation/) and filters need.
- **The eigenvector method.** Build the 4 by 4 symmetric matrix of the [Davenport q-method](/davenport-q-method/) from $R$ and take the eigenvector of its largest eigenvalue. This gives the quaternion of a nearby rotation for a matrix that is far from orthogonal, at the cost of an eigenvalue problem.
- **Through the logarithm.** Compute $\theta\hat\omega$ with the [logarithm map of SO(3)](/so3-logarithm-map/), then $q = (\cos\frac\theta2, \sin\frac\theta2\,\hat\omega)$. This needs trigonometric functions, and it must handle the angle $\pi$ with its own branch.
- **The JPL convention.** Some attitude papers write the quaternion with the scalar last and with $ij = -k$. In that convention the signs of the three differences in lines L5, L8, L11 and L14 change. Convert at the interface, and do not mix the two.

## When to use it

Use the method whenever a rotation matrix must become a quaternion: after [forward kinematics](/forward-kinematics/), from the output of a camera pose or a point set alignment such as the [Kabsch algorithm](/kabsch-algorithm/), or to store attitude in a filter state.
It is the standard step before [spherical linear interpolation](/spherical-linear-interpolation/), before an integration of the [quaternion kinematic equation](/quaternion-kinematic-equation/), and before [rotation averaging](/rotation-averaging/) methods that work on quaternions.

## Pitfalls

- **The formula that divides by $4w$.** It is the first one in many books, and it is correct, but only for angles well below $\pi$. Its error grows as $u/d^2$ near $\pi - d$, and it divides by zero at $\pi$. This is a [loss of accuracy by cancellation](/catastrophic-cancellation/) in $1 + t$.
- **A transposed matrix.** If $R$ maps world coordinates to body coordinates, the method returns the conjugate quaternion. Check which way the matrix maps before you convert.
- **Equal values in line L2.** Ties are harmless: any branch with the largest square works, because its component is at least $1/2$.
- **Comparing quaternions.** Two correct results can differ in sign. Compare $q_1$ and $q_2$ by $\min(|q_1 - q_2|, |q_1 + q_2|)$, or compare the matrices.
- **A matrix that is not a rotation.** A reflection ($\det R = -1$) also gives four numbers, but they mean nothing. Check $\det R$ when the input is not trusted.

## Implementations

## History

Shepperd, at the Charles Stark Draper Laboratory, published the method in 1978 as a short engineering note in the Journal of Guidance and Control.
The note gives the four candidate squares from the trace and the diagonal and selects the largest one to avoid a division by a small number.
Lynch and Park (2017) print the formula that divides by $4w$ in Appendix B.3, together with the form of $R$ in terms of $q$.
Sola (2017) lists the conversions and compares the Hamilton and JPL conventions.

## References
