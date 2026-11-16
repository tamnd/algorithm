---
tag: XV896C
kind: definition
slug: cayley-rotation-parameters
name: Cayley parameterization of rotations
aliases:
- Gibbs vector
- Cayley-Gibbs-Rodrigues parameters
area: robotics/rigid-body-motion
level: advanced
summary: The rotation (I - [c])^-1 (I + [c]) of a vector c = tan(theta/2) times the axis, a rational three-parameter chart of SO(3) that misses only the half turns.
prereqs: [axis-angle-representation, skew-symmetric-matrix-of-a-vector]
see_also: [unit-quaternion-rotation, stuelpnagel-theorem, rodrigues-rotation-formula, so3-logarithm-map, euler-angles, special-orthogonal-group, wahba-problem, quest-algorithm]
sources:
  - paper: doi:10.1515/crll.1846.32.119
    title: Arthur Cayley, Sur quelques propriétés des déterminants gauches, Journal für die reine und angewandte Mathematik 32, 119-123, 1846
    locator: the whole paper (orthogonal matrices built from skew-symmetric matrices)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Appendix B, Section B.4 (Cayley-Rodrigues parameters, equations B.16 to B.18)
  - paper: doi:10.1137/1006093
    title: John Stuelpnagel, On the parametrization of the three-dimensional rotation group, SIAM Review 6(4), 422-430, 1964
    locator: Section 6 (three-dimensional parametrizations, the Cayley form and the rotations with trace -1)
---

The Cayley parameters describe a rotation by one vector $c \in \mathbb{R}^3$, the unit axis $\hat\omega$ times $\tan\frac\theta2$, where $\theta$ is the angle of rotation.
The rotation matrix is $R = (I - [c])^{-1}(I + [c])$, a rational function of $c$ with no sines or cosines, and the inverse is $c = \operatorname{vee}(R - R^{\mathsf T})/(1 + \operatorname{tr} R)$.
The chart is one-to-one and smooth on all of $\mathbb{R}^3$, but it misses the rotations by $\pi$, where $\tan\frac\theta2$ is infinite.
The vector is also called the Gibbs vector or the Rodrigues parameters; it equals the vector part of a [unit quaternion](/unit-quaternion-rotation/) divided by its scalar part.

Notation on this page: rotations are active, quaternions are in the Hamilton convention with the scalar first, and $[c]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $c$, so that $[c]v = c \times v$; vee is its inverse.

## Definition

**Definition.** The Cayley map is

$$\operatorname{cay}(c) = (I - [c])^{-1}(I + [c]) = I + \frac{2}{1 + |c|^2}\big([c] + [c]^2\big), \qquad c \in \mathbb{R}^3 .$$

The Cayley parameters of a rotation $R$ in the [special orthogonal group](/special-orthogonal-group/) SO(3) are the vector $c$ with $\operatorname{cay}(c) = R$.

The basic facts are:

- **It is a rotation.** $I - [c]$ is invertible for every $c$, because the eigenvalues of $[c]$ are $0$ and $\pm i|c|$. The factors $I - [c]$ and $I + [c]$ commute, and $(I + [c])^{\mathsf T} = I - [c]$, so $\operatorname{cay}(c)^{\mathsf T}\operatorname{cay}(c) = I$. The determinant is 1, because $\operatorname{cay}(0) = I$ and $\mathbb{R}^3$ is connected.
- **Axis and angle.** With $c = \tan\frac\theta2\,\hat\omega$, the second form of the map is $I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2$, which is [Rodrigues' formula](/rodrigues-rotation-formula/), because $2\tan\frac\theta2/(1 + \tan^2\frac\theta2) = \sin\theta$ and $2\tan^2\frac\theta2/(1 + \tan^2\frac\theta2) = 1 - \cos\theta$. So $c$ is the rotation by $\theta = 2\arctan|c|$ about $c/|c|$, with $\theta \in [0, \pi)$.
- **Inverse.** For $\operatorname{tr} R \ne -1$, that is $\theta \ne \pi$,
  $$[c] = (R - I)(R + I)^{-1}, \qquad c = \frac{1}{1 + \operatorname{tr} R}\begin{pmatrix} r_{32} - r_{23} \\ r_{13} - r_{31} \\ r_{21} - r_{12} \end{pmatrix}.$$
  The second formula follows from $R - R^{\mathsf T} = 2\sin\theta\,[\hat\omega]$ and $1 + \operatorname{tr} R = 2(1 + \cos\theta)$.
- **The image.** $\operatorname{cay}$ is a one-to-one map of $\mathbb{R}^3$ onto the rotations with $\operatorname{tr} R > -1$, which are all rotations except the half turns. Its derivative has full rank everywhere. This is one of the three ways of failing that [Stuelpnagel's theorem](/stuelpnagel-theorem/) allows: one-to-one and nonsingular, but not onto.
- **Quaternions.** If $q = (w, u)$ is a unit quaternion of $R$ with $w \ne 0$, then $c = u/w$. Conversely $q = (1, c)/\sqrt{1 + |c|^2}$. The half turns are exactly the rotations with $w = 0$.
- **Composition.** If $R_1 = \operatorname{cay}(c_1)$, $R_2 = \operatorname{cay}(c_2)$ and $c_1 \cdot c_2 \ne 1$, then
  $$R_1 R_2 = \operatorname{cay}\Big(\frac{c_1 + c_2 + c_1 \times c_2}{1 - c_1 \cdot c_2}\Big).$$
  This is the quaternion product $(1, c_1)(1, c_2) = (1 - c_1 \cdot c_2,\; c_1 + c_2 + c_1 \times c_2)$, divided by its scalar part. When $c_1 \cdot c_2 = 1$, the product is a half turn.

**The order of the factors.** The factors of $\operatorname{cay}(c)$ commute, so $(I - [c])^{-1}(I + [c]) = (I + [c])(I - [c])^{-1}$.
The other order of the signs, $(I - [c])(I + [c])^{-1}$, is $\operatorname{cay}(-c)$, the rotation by $-\theta$.
Lynch and Park, Appendix B.4, define the parameters as $\hat\omega\tan\frac\theta2$ in equation B.16, but write the matrix in equations B.17 and B.18 in the second form, so their formulas give the inverse rotation; with $c = (1, 0, 0)$ their form gives the turn by $-90°$ about $x$.
Stuelpnagel also writes the second form, $(I - S)(I + S)^{-1}$; in every form, the half turns are the rotations that the chart misses.
Before using a formula from a source, check it on one example.

## Examples and non-examples

- **A quarter turn.** $c = (1, 0, 0)$ gives $\theta = 2\arctan 1 = 90°$ about $x$, and $\operatorname{cay}(c) = R_x(90°)$, with rows $(1, 0, 0)$, $(0, 0, -1)$, $(0, 1, 0)$.
- **Rational entries.** $c = (0.5, 0, 0)$ gives the rows $(1, 0, 0)$, $(0, 0.6, -0.8)$, $(0, 0.8, 0.6)$, a rotation by $53.130°$ about $x$. Every rational $c$ gives a rotation with rational entries.
- **The cyclic rotation.** $(x, y, z) \mapsto (z, x, y)$ is the rotation by $120°$ about $(1, 1, 1)/\sqrt3$, so $c = \tan 60° \cdot (1, 1, 1)/\sqrt3 = (1, 1, 1)$. The inverse formula agrees: $\operatorname{tr} R = 0$, and $(r_{32} - r_{23}, r_{13} - r_{31}, r_{21} - r_{12}) = (1, 1, 1)$.
- **Composition.** $c_1 = (0, 0, 1)$ is the quarter turn about $z$ and $c_2 = (1, 0, 0)$ the quarter turn about $x$. Then $c_1 \cdot c_2 = 0$ and $c_1 + c_2 + c_1 \times c_2 = (1, 0, 1) + (0, 1, 0) = (1, 1, 1)$, so $R_z(90°)R_x(90°)$ is the cyclic rotation above.
- **Non-example: the half turn.** $R = \operatorname{diag}(1, -1, -1)$, the turn by $\pi$ about $x$, has $\operatorname{tr} R = -1$, so the inverse formula divides by zero. Along $c = (t, 0, 0)$ the angle is $2\arctan t$: $168.58°$ at $t = 10$ and $178.85°$ at $t = 100$. The half turn has no Cayley parameters.
- **Non-example: the angle as the length.** $|c|$ is $\tan\frac\theta2$, not $\theta$. For small angles $c \approx \frac\theta2\hat\omega$, half of the exponential coordinates of the [logarithm map](/so3-logarithm-map/), and a code that mixes the two is wrong by a factor of 2.

## Related definitions

- **[Unit quaternion](/unit-quaternion-rotation/).** $c$ is the quaternion in homogeneous form, $u/w$. Quaternions have no singular rotation, at the price of a fourth number and a sign.
- **[Axis-angle representation](/axis-angle-representation/) and [Rodrigues' formula](/rodrigues-rotation-formula/).** The exponential coordinates $\theta\hat\omega$ use the angle itself; the Cayley parameters use $\tan\frac\theta2$ and avoid all trigonometric functions.
- **Modified Rodrigues parameters.** The vector $\tan\frac\theta4\,\hat\omega$, which is singular only at $\theta = 2\pi$; with the switch to the parameters of $-q$, it covers every rotation with a bounded vector.
- **The Cayley transform.** In any dimension, $S \mapsto (I - S)^{-1}(I + S)$ maps the skew-symmetric matrices one-to-one onto the orthogonal matrices with determinant 1 and no eigenvalue $-1$. Cayley gave it in 1846.
- **[Wahba's problem](/wahba-problem/) and the [QUEST algorithm](/quest-algorithm/).** QUEST solves for the attitude in Cayley parameters, which reduces the eigenvector problem of the [q-method](/davenport-q-method/) to a linear system.

## References
