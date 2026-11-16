---
tag: X9EWPH
kind: theorem
slug: rodrigues-rotation-formula
name: "Rodrigues' rotation formula"
aliases:
- Rodrigues formula
- Euler-Rodrigues formula
area: robotics/rigid-body-motion
level: core
summary: "The rotation by an angle theta about a unit axis w is exp([w] theta) = I + sin(theta) [w] + (1 - cos(theta)) [w]^2, the closed form of the exponential on so(3)."
prereqs: [skew-symmetric-matrix-of-a-vector, special-orthogonal-group, matrix-exponential]
see_also: [so3-logarithm-map, axis-angle-representation, se3-exponential-map, euler-rotation-theorem, unit-quaternion-rotation, angular-velocity, small-displacement-torsor, cayley-rotation-parameters]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.3 (exponential coordinate representation of rotation, the matrix exponential of a rotation and Rodrigues' formula)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2.2 (exponential coordinates for rotation and Rodrigues' formula)
  - paper: "Olinde Rodrigues, Des lois géométriques qui régissent les déplacements d'un système solide dans l'espace, et de la variation des coordonnées provenant de ces déplacements considérés indépendamment des causes qui peuvent les produire, Journal de Mathématiques Pures et Appliquées, série 1, 5, 380 to 440, 1840"
    locator: the whole paper (the geometry of rigid displacements and the composition of rotations)
  - paper: doi:10.1115/1.3176034
    title: Hui Cheng and K. C. Gupta, An historical note on finite rotations, Journal of Applied Mechanics 56(1), 139 to 145, 1989
    locator: the whole note (the history of the formula and of the rotation parameters, with the earlier work of Euler)
---

Rodrigues' rotation formula gives the matrix of the rotation by an angle $\theta$ about a unit axis $\hat\omega$ as $R = I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2$, where $[\hat\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\hat\omega$.
The same matrix is the [matrix exponential](/matrix-exponential/) $e^{[\hat\omega]\theta}$, so the formula sums the infinite exponential series in closed form with one sine and one cosine.
Applied to a vector $x$, it reads $Rx = \cos\theta\, x + \sin\theta\,(\hat\omega \times x) + (1 - \cos\theta)(\hat\omega \cdot x)\,\hat\omega$.
It is the basic tool to turn the [axis-angle representation](/axis-angle-representation/) of a rotation into a matrix in the [special orthogonal group](/special-orthogonal-group/) SO(3).

## Statement

**Theorem.** Let $\hat\omega \in \mathbb{R}^3$ be a unit vector and $\theta \in \mathbb{R}$.
Then

$$e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)[\hat\omega]^2 .$$

This matrix is in SO(3), it keeps $\hat\omega$ fixed, and it turns every vector orthogonal to $\hat\omega$ by the angle $\theta$, counterclockwise when seen from the tip of $\hat\omega$.

For a vector $\omega \ne 0$ that is not of unit length, put $\theta = |\omega|$ and $\hat\omega = \omega/\theta$:

$$e^{[\omega]} = I + \frac{\sin\theta}{\theta}[\omega] + \frac{1 - \cos\theta}{\theta^2}[\omega]^2 .$$

## In plain words

To turn a vector about an axis, split it into the part along the axis and the part across the axis.
The part along the axis does not change.
The part across the axis turns in its plane, like the hand of a clock.
After the turn, the part across the axis is a mix of its old direction and the direction at a right angle to it in the same plane.
The amounts of the mix are the cosine and the sine of the angle.
The formula writes these three steps as one matrix.
It also shows that adding up the infinite sum that defines the exponential of a turning speed gives exactly this matrix.

## Proof

We use two facts about the unit vector $\hat\omega$ and $K = [\hat\omega]$.
First, for every $x$, $K^2 x = \hat\omega \times (\hat\omega \times x) = (\hat\omega \cdot x)\hat\omega - x$, so $K^2 = \hat\omega\hat\omega^{\mathsf T} - I$.
Second, $K^3 = K\hat\omega\hat\omega^{\mathsf T} - K = -K$, because $K\hat\omega = \hat\omega \times \hat\omega = 0$.
By induction, $K^{2j+1} = (-1)^j K$ and $K^{2j+2} = (-1)^j K^2$ for every $j \ge 0$.

The exponential series converges absolutely, so we may split it into the term $k = 0$, the odd terms and the even terms with $k \ge 2$:

$$e^{K\theta} = I + \sum_{j \ge 0} \frac{\theta^{2j+1}}{(2j+1)!} K^{2j+1} + \sum_{j \ge 0} \frac{\theta^{2j+2}}{(2j+2)!} K^{2j+2} = I + \Big(\sum_{j \ge 0} \frac{(-1)^j\theta^{2j+1}}{(2j+1)!}\Big) K + \Big(\sum_{j \ge 0} \frac{(-1)^j\theta^{2j+2}}{(2j+2)!}\Big) K^2 .$$

The first sum is the series of $\sin\theta$, and the second sum is the series of $1 - \cos\theta$.
This proves the formula.

The matrix is a rotation.
Since $K^{\mathsf T} = -K$, $(e^{K\theta})^{\mathsf T} = e^{-K\theta}$, and $e^{K\theta}e^{-K\theta} = I$ because $K\theta$ and $-K\theta$ commute.
So $R = e^{K\theta}$ is orthogonal.
Also $\det e^{K\theta} = e^{\operatorname{tr} K\theta} = e^0 = 1$.
So $R \in SO(3)$.

The matrix is the rotation about $\hat\omega$.
$R\hat\omega = \hat\omega$, because $K\hat\omega = 0$.
Let $a$ be a unit vector orthogonal to $\hat\omega$ and $b = \hat\omega \times a$.
Then $Ka = b$, $K^2 a = -a$, $Kb = \hat\omega \times b = -a$ and $K^2 b = -b$.
So $Ra = a + \sin\theta\, b - (1 - \cos\theta)\, a = \cos\theta\, a + \sin\theta\, b$, and in the same way $Rb = -\sin\theta\, a + \cos\theta\, b$.
This is the rotation by $\theta$ in the plane of $a$ and $b$, in the direction from $a$ to $b = \hat\omega \times a$, which is counterclockwise seen from the tip of $\hat\omega$.

The vector form follows from $K x = \hat\omega \times x$ and $K^2 x = (\hat\omega \cdot x)\hat\omega - x$.
The form for a vector $\omega$ of any length follows from $[\omega] = \theta K$. $\square$

## Consequences

- **The angle from the trace.** $\operatorname{tr} R = 3 + 0 + (1 - \cos\theta)\operatorname{tr}K^2 = 1 + 2\cos\theta$, since $\operatorname{tr}K^2 = -2$.
- **The axis from the skew part.** $\tfrac12(R - R^{\mathsf T}) = \sin\theta\, K$. These two facts invert the formula; the [logarithm map of SO(3)](/so3-logarithm-map/) does this in a stable way.
- **The exponential is onto.** With [Euler's rotation theorem](/euler-rotation-theorem/), every rotation is $e^{[\hat\omega]\theta}$ for some $\hat\omega$ and $\theta \in [0, \pi]$.
- **Rigid motions.** The [exponential map of SE(3)](/se3-exponential-map/) uses the formula for its rotation block and a second closed form for its translation.
- **Unit quaternions.** The [unit quaternion](/unit-quaternion-rotation/) $q = (\cos\tfrac\theta2, \sin\tfrac\theta2\,\hat\omega)$ gives the same rotation. Inserting it into the quaternion rotation formula and using $\cos\theta = 1 - 2\sin^2\tfrac\theta2$ and $\sin\theta = 2\sin\tfrac\theta2\cos\tfrac\theta2$ gives Rodrigues' formula again.
- **Small rotations.** To first order in $\theta$, $R \approx I + \theta K$, so a small rotation moves a point $x$ by $\theta\,\hat\omega \times x$. This is the linear model behind the [small displacement torsor](/small-displacement-torsor/), and the second-order term $(1 - \cos\theta)K^2$ bounds its error by about $\theta^2|x|/2$.

Example.
For $\hat\omega = (1, 1, 1)/\sqrt3$ and $\theta = 2\pi/3$, $\sin\theta = \sqrt3/2$ and $1 - \cos\theta = 3/2$.
Then $\sin\theta\,K = \tfrac12[(1, 1, 1)]$ and $(1 - \cos\theta)K^2 = \tfrac12 J - \tfrac32 I$, where $J$ is the matrix of ones.
The sum is $R = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$, the rotation that maps $x \to y \to z \to x$.

## Tightness

- **The axis must be a unit vector.** The first form uses $K^3 = -K$, which holds only for $|\hat\omega| = 1$. For any other length, the angle is $|\omega|$ and the factors change as in the second form.
- **The angle is not unique.** $\theta$ and $\theta + 2\pi$ give the same $R$, and so do $(\hat\omega, \theta)$ and $(-\hat\omega, -\theta)$. At $\theta = \pi$, $\hat\omega$ and $-\hat\omega$ give the same $R$ with the same angle.
- **Dimension 3.** In dimension 4 and above, a skew-symmetric matrix can turn two orthogonal planes at different speeds, and then $A^3 = -c^2A$ fails for every $c$. The exponential is then a sum over the planes, one Rodrigues-type term per plane, not one formula with one angle.
- **Numerics.** The second form divides by $\theta$ and $\theta^2$. For small $\theta$, $(1 - \cos\theta)/\theta^2$ loses digits to cancellation, and code uses a Taylor series below a threshold.

## History

Euler studied finite rotations about an axis in the 1770s, and Cheng and Gupta (1989) report that the formula in its essence goes back to him.
Rodrigues (1840) studied the geometry of rigid displacements and the composition of two rotations, and the formula carries his name.
The form as the closed form of the matrix exponential $e^{[\hat\omega]\theta}$ is the one used in the robotics textbooks of Murray, Li and Sastry (1994) and of Lynch and Park (2017).

## References
