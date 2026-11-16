---
tag: 12BS1H
kind: definition
slug: skew-symmetric-matrix-of-a-vector
name: Skew-symmetric matrix of a vector
aliases:
- hat operator
- cross product matrix
area: robotics/rigid-body-motion
level: intro
summary: "The 3 by 3 skew-symmetric matrix [w] with [w] v = w x v for every v, which turns a cross product into a matrix product and identifies R^3 with so(3)."
prereqs: [cross-product]
see_also: [rodrigues-rotation-formula, angular-velocity, special-orthogonal-group, rigid-body-twist, small-displacement-torsor, lie-bracket, matrix-exponential, so3-logarithm-map]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.2.2 (angular velocities, where the skew-symmetric matrix of a vector and its properties are introduced)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 2 (rotational motion, the hat map from a vector to a skew-symmetric matrix)
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the hat and vee operators between the Lie algebra and the vector space of a Lie group
---

The skew-symmetric matrix of a vector $\omega = (\omega_1, \omega_2, \omega_3)$ is the $3 \times 3$ matrix $[\omega]$ that multiplies a vector $x$ the same way as the [cross product](/cross-product/) $\omega \times x$.
It changes a cross product into a matrix product, so that the tools of linear algebra apply to rotations and velocities.
Other names are the hat operator, written $\hat\omega$, and the cross product matrix, written $\omega^\times$.
The map from $\omega$ to $[\omega]$ is linear and one to one, and its image is the set of all $3 \times 3$ skew-symmetric matrices, the Lie algebra $\mathfrak{so}(3)$ of the rotation group.
Its exponential is a rotation, by [Rodrigues' formula](/rodrigues-rotation-formula/), and it gives the [angular velocity](/angular-velocity/) of a rotating frame.

## Definition

For $\omega = (\omega_1, \omega_2, \omega_3) \in \mathbb{R}^3$,

$$[\omega] = \begin{pmatrix} 0 & -\omega_3 & \omega_2 \\ \omega_3 & 0 & -\omega_1 \\ -\omega_2 & \omega_1 & 0 \end{pmatrix}.$$

Then $[\omega] x = \omega \times x$ for every $x \in \mathbb{R}^3$.
The matrix is skew-symmetric: $[\omega]^{\mathsf T} = -[\omega]$.

The inverse map is the vee operator.
For a skew-symmetric $M$, $M^\vee = (m_{32}, m_{13}, m_{21})$, so $[\omega]^\vee = \omega$.
Every real $3 \times 3$ skew-symmetric matrix has only three free entries, so every such matrix is $[\omega]$ for exactly one $\omega$.

The following properties hold for all $\omega, x \in \mathbb{R}^3$; each one is a short computation.

- $[\omega]\omega = 0$, so $\omega$ spans the null space of $[\omega]$ when $\omega \ne 0$, and $[\omega]$ has rank 2.
- $x^{\mathsf T}[\omega] x = 0$.
- $[\omega]^2 = \omega\omega^{\mathsf T} - |\omega|^2 I$, and so $[\omega]^3 = -|\omega|^2 [\omega]$.
- $\operatorname{tr}[\omega] = 0$ and $\operatorname{tr}[\omega]^2 = -2|\omega|^2$.
- The eigenvalues of $[\omega]$ are $0$ and $\pm i|\omega|$.
- For a rotation $R$, $R[\omega]R^{\mathsf T} = [R\omega]$.
- $[\omega][x] - [x][\omega] = [\omega \times x]$. So the cross product is the [Lie bracket](/lie-bracket/) of $\mathfrak{so}(3)$.

The identity $R[\omega]R^{\mathsf T} = [R\omega]$ holds because $R(\omega \times R^{\mathsf T}y) = R\omega \times y$ for a rotation $R$; it fails for a reflection, where the sign of the cross product changes.

## Examples and non-examples

- For $\omega = (1, 2, 3)$, $[\omega] = \begin{pmatrix} 0 & -3 & 2 \\ 3 & 0 & -1 \\ -2 & 1 & 0 \end{pmatrix}$, and for $x = (4, 5, 6)$, $[\omega]x = (-3, 6, -3) = \omega \times x$.
- For the same $\omega$, $[\omega]^2 = \begin{pmatrix} -13 & 2 & 3 \\ 2 & -10 & 6 \\ 3 & 6 & -5 \end{pmatrix} = \omega\omega^{\mathsf T} - 14 I$, which is symmetric, as the third property says.
- For the unit vector $\hat z = (0, 0, 1)$, $[\hat z]$ is the rotation by $\pi/2$ in the $xy$ plane followed by the projection onto that plane. Its exponential $e^{[\hat z]\theta}$ is the rotation $R_z(\theta)$ about the $z$ axis.
- Non-example: the $4 \times 4$ matrix $[S]$ of a [twist](/rigid-body-twist/) has a skew-symmetric block $[\omega]$ but is not skew-symmetric itself, because its last row is zero and its last column holds $v$.
- Non-example: in $\mathbb{R}^n$ with $n \ne 3$, a skew-symmetric matrix has $n(n-1)/2$ free entries, which is not $n$, so there is no matching vector with a cross product. In the plane, the one number $\omega$ gives the matrix $\begin{pmatrix} 0 & -\omega \\ \omega & 0 \end{pmatrix}$.

## Related definitions

- [Rodrigues' rotation formula](/rodrigues-rotation-formula/) gives the exponential $e^{[\omega]\theta}$ in closed form.
- The [special orthogonal group](/special-orthogonal-group/) SO(3) is the group whose Lie algebra is the set of matrices $[\omega]$.
- The [angular velocity](/angular-velocity/) of a rotating frame $R(t)$ is the vector $\omega$ with $[\omega] = \dot R R^{\mathsf T}$.
- The [twist](/rigid-body-twist/) uses $[\omega]$ in the $4 \times 4$ matrix $[\mathcal{V}]$, and the [adjoint map](/adjoint-map-se3/) uses $[p]$ for the position $p$.
- The [logarithm map of SO(3)](/so3-logarithm-map/) recovers $\omega$ from a rotation by the vee operator applied to the skew part.
- In the [small displacement torsor](/small-displacement-torsor/) model of tolerancing, a small rotation $\omega$ moves a point $M$ by $\omega \times \vec{OM} = [\omega]\vec{OM}$.

## References
