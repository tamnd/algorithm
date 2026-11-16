---
tag: WRDGRM
kind: definition
slug: yoshikawa-manipulability-measure
name: Yoshikawa manipulability measure
aliases:
- manipulability index
area: robotics/robot-kinematics
level: core
summary: The number sqrt(det(J J^T)), proportional to the volume of the manipulability ellipsoid and zero at singularities.
model: real-ram
prereqs: [manipulability-ellipsoid]
see_also: [kinematic-singularity, condition-number, null-space-projection, kinematic-redundancy, singular-value-decomposition, qr-decomposition, space-and-body-jacobian, geometric-jacobian]
sources:
  - paper: doi:10.1177/027836498500400201
    title: Tsuneo Yoshikawa, Manipulability of robotic mechanisms, The International Journal of Robotics Research 4(2), 3-9, 1985
    locator: the whole paper (the definition of the measure w, its relation to the ellipsoid volume and to the singular values, and the best postures of simple arms)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 5, Section 5.4 (manipulability, the volume measure among three scalar measures)
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.5 (the manipulability measure as an objective for redundancy) and Section 3.9 (manipulability ellipsoids)
---

The Yoshikawa manipulability measure of a robot arm at a configuration $q$ is the number $w(q) = \sqrt{\det(J(q) J(q)^{\mathsf T})}$, where $J$ is the $m \times n$ Jacobian of the task and $m \le n$.
It is the product of the singular values of $J$, so it is proportional to the volume of the [manipulability ellipsoid](/manipulability-ellipsoid/), and it is zero exactly at the [kinematic singularities](/kinematic-singularity/).
Tsuneo Yoshikawa proposed it in 1985 as one number that says how freely the end effector can move in all directions at once.
A large $w$ is good; how small a $w$ counts as "near singular" is a rule of thumb that depends on the arm and its units.

## Definition

Let $J$ be an $m \times n$ real matrix with $m \le n$, the Jacobian of a task of dimension $m$ for an arm with $n$ joints.

**Definition.** The manipulability measure is

$$w = \sqrt{\det(J J^{\mathsf T})}.$$

The matrix $JJ^{\mathsf T}$ is symmetric and positive semidefinite, so its determinant is not negative, and the root is real.
For $m > n$ the matrix $JJ^{\mathsf T}$ has rank at most $n < m$, its determinant is always zero, and the measure is not defined.

**Equivalent forms.** With the [singular value decomposition](/singular-value-decomposition/) $J = U\Sigma V^{\mathsf T}$ and the singular values $\sigma_1 \ge \dots \ge \sigma_m \ge 0$,

$$w = \sigma_1 \sigma_2 \cdots \sigma_m,$$

because $\det(JJ^{\mathsf T}) = \det(U \Sigma\Sigma^{\mathsf T} U^{\mathsf T}) = \prod_i \sigma_i^2$.
For a square $J$, $w = |\det J|$.
The velocity ellipsoid $\{J\dot q : |\dot q| \le 1\}$ has the semi-axes $\sigma_i$, so its volume is $c_m w$, where $c_m$ is the volume of the unit ball of $\mathbb{R}^m$ ($c_2 = \pi$, $c_3 = 4\pi/3$).
By the Cauchy-Binet formula, $\det(JJ^{\mathsf T})$ is also the sum of the squares of all the $m \times m$ minors of $J$.

**Properties.**

- $w(q) = 0$ if and only if $\operatorname{rank} J(q) < m$, that is, at a singularity of an arm with generic rank $m$.
- $w(RJ) = w(J)$ for an orthogonal $m \times m$ matrix $R$, and $w(JQ) = w(J)$ for an orthogonal $n \times n$ matrix $Q$: a rotation of the task frame or an orthogonal change of joint coordinates does not change $w$.
- More generally, $w(AJ) = |\det A|\,w(J)$ for any invertible $m \times m$ matrix $A$. The adjoint map $\operatorname{Ad}_T$ and the factor between the geometric Jacobian and the [space and body Jacobians](/space-and-body-jacobian/) have determinant $\pm 1$, so all three give the same $w$.
- $w(cJ) = |c|^m w(J)$. If the linear rows of a $6 \times n$ Jacobian change from meters to millimeters, $w$ grows by $10^9$ at every configuration. This keeps the order of configurations of one arm, but a single value of $w$ has no meaning without its units, and values of arms of different size cannot be compared.

**Gradient.** For the [null space projection](/null-space-projection/) that pushes a redundant arm toward large $w$, the partial derivatives are

$$\frac{\partial w}{\partial q_i} = w\, \operatorname{tr}\!\left(J^{+} \frac{\partial J}{\partial q_i}\right), \qquad J^{+} = J^{\mathsf T}(JJ^{\mathsf T})^{-1},$$

from $d \log\det A = \operatorname{tr}(A^{-1} dA)$ with $A = JJ^{\mathsf T}$ and $dA = dJ\,J^{\mathsf T} + J\,dJ^{\mathsf T}$.

**Computation.** The code on this page follows the definition.

```pseudo id=main
MANIPULABILITY(J)                          ▷ J: m × n, with m ≤ n
L1  A ← J J^T                               ▷ m × m, symmetric
L2  d ← det A                               ▷ Gaussian elimination
L3  return sqrt(max(d, 0))                  ▷ rounding can make d slightly negative
```

Line L1 costs $\Theta(m^2 n)$ operations and line L2 costs $\Theta(m^3)$, so the total is $\Theta(m^2 n)$ in the [real RAM](/real-ram/), with $\Theta(m^2)$ extra space.
Forming $JJ^{\mathsf T}$ squares the singular values, so when $\sigma_m^2$ is close to the rounding unit times $\sigma_1^2$, most of $d$ is rounding error.
For example, in double precision, a rotated $2 \times 2$ matrix with the singular values 1 and $10^{-9}$ can give $w \approx 3.6 \cdot 10^{-9}$ in place of $10^{-9}$.
A [QR decomposition](/qr-decomposition/) $J^{\mathsf T} = QR$ avoids the square: then $w = |r_{11} r_{22} \cdots r_{mm}|$.

## Examples and non-examples

**The planar 2R arm.** For the position task of a 2R arm with link lengths $L_1$ and $L_2$, $J$ is square and $w = |\det J| = L_1 L_2 |\sin q_2|$.
At the check configuration $q = (0, \pi/2)$ with $L_1 = L_2 = 1$ m, $J = \begin{pmatrix} -1 & -1 \\ 1 & 0 \end{pmatrix}$, $w = 1$ m², and the singular values are $1.618$ and $0.618$, whose product is 1.
This is the largest $w$ over all configurations, since $|\sin q_2| \le 1$.
For a fixed total length $L_1 + L_2$, the product $L_1 L_2$ is largest when $L_1 = L_2$, so the equal link arm has the largest best value of $w$.

**Close to a singularity.** At $q = (0, 0.01)$ the same arm has $w = \sin 0.01 \approx 0.0100$, the singular values $2.236$ and $0.00447$, and the condition number $500$.
At $q_2 = 0$ or $q_2 = \pi$, $w = 0$.

**A redundant arm.** For the planar 3R arm with unit links and the position task, $m = 2$ and $n = 3$.
At $q = (0, \pi/2, -\pi/2)$,

$$J = \begin{pmatrix} -1 & -1 & 0 \\ 2 & 1 & 1 \end{pmatrix}, \qquad JJ^{\mathsf T} = \begin{pmatrix} 2 & -3 \\ -3 & 6 \end{pmatrix}, \qquad w = \sqrt 3 \approx 1.732.$$

The three $2 \times 2$ minors of $J$ are $1$, $-1$ and $-1$, and the sum of their squares is $3$, as the Cauchy-Binet formula says.

**Non-example: a distance to the singularities.** A 2R arm with $L_1 = L_2 = 0.1$ m at $q_2 = \pi/2$ has $w = 0.01$, the same as the 1 m arm at $q_2 = 0.01$, but its condition number is $2.618$, the same as at the best posture of the 1 m arm.
A small $w$ can come from a small arm, not from a nearby singularity; the [condition number](/condition-number/) $\sigma_1/\sigma_m$ does not depend on the scale.

**Non-example: the analytic Jacobian.** For the [analytic Jacobian](/analytic-jacobian/) $J_A$, $J = \operatorname{diag}(I, T(\phi))J_A$, so $w(J) = |\det T(\phi)|\,w(J_A)$.
The measure of $J_A$ depends on the choice of angles and is not a property of the arm.

**Non-example: a product of joint ranges.** The measure is a local, first order quantity at one configuration; it says nothing about how far the joints can move before a joint limit.

## Related definitions

- [Manipulability ellipsoid](/manipulability-ellipsoid/): the ellipsoid whose volume is $c_m w$.
- [Kinematic singularity](/kinematic-singularity/): the configurations where $w = 0$.
- [Condition number](/condition-number/): $\sigma_1/\sigma_m$, the ratio of the longest to the shortest axis, another scalar measure that is free of scale.
- [Null space projection](/null-space-projection/): with $z = k\,\nabla w$, it moves a redundant arm toward larger $w$ without disturbing the task.
- [Kinematic redundancy](/kinematic-redundancy/): the setting where $w$ is used as a secondary objective.
- [Singular value decomposition](/singular-value-decomposition/): $w$ is the product of the singular values.

## References
