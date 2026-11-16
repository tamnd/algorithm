---
tag: 51NHRY
kind: definition
slug: spatial-inertia
name: Spatial inertia
aliases:
- spatial inertia matrix
area: robotics/robot-dynamics
level: core
summary: The 6x6 symmetric matrix of a rigid body built from its mass, center of mass and rotational inertia, mapping a twist to momentum.
prereqs: [spatial-vector-algebra, newton-euler-equations]
see_also: [articulated-body-inertia, composite-rigid-body-algorithm, recursive-newton-euler-algorithm, joint-space-inertia-matrix, linearity-in-dynamic-parameters, base-inertial-parameters, centroidal-momentum-matrix, positive-definite-matrix]
sources:
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 2 (spatial vector algebra), the sections on rigid-body inertia, momentum and the equation of motion"
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.2 (dynamics of a single rigid body: the spatial inertia matrix and its change of frame)"
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
---

The spatial inertia of a rigid body is a symmetric $6 \times 6$ matrix that holds all its inertial properties: the mass, the position of the center of mass, and the rotational inertia. It maps the velocity of the body, a 6-dimensional twist, to its momentum, a 6-dimensional wrench-like vector of angular and linear momentum, and it gives the kinetic energy as a quadratic form. With it, the [Newton-Euler equations](/newton-euler-equations/) of a body become one line of [spatial vector algebra](/spatial-vector-algebra/).

## Definition

Let a rigid body have the mass $m > 0$, the center of mass at the point $c$ in a frame with origin $O$, and the rotational inertia $\bar I_c$ about the center of mass, a symmetric $3 \times 3$ matrix in the axes of the frame. Write $[c]$ for the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) with $[c]\, x = c \times x$. With the angular part first, the **spatial inertia** of the body in this frame is
$$I = \begin{pmatrix} \bar I_c + m [c][c]^T & m [c] \\ m [c]^T & m\, \mathbf{1} \end{pmatrix}.$$
The top-left block $\bar I_c + m[c][c]^T = \bar I_c + m(|c|^2 \mathbf{1} - c c^T)$ is the rotational inertia about $O$, by the parallel axis theorem.

For a body with the twist $v = (\omega, v_O)$, the **momentum** is $h = I v$. Its linear part is $m(v_O + \omega \times c)$, the mass times the velocity of the center of mass, and its angular part is the angular momentum about $O$. The kinetic energy is $T = \tfrac12 v^T I v$, and the equation of motion is $f = I a + \mathrm{crf}(v)\, I v$.

**Properties.**

- **Ten parameters.** $I$ depends on $m$, the first moment $m c$ and the six entries of the rotational inertia about $O$. It is linear in these ten numbers, which is the source of the [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/).
- **Positive definite.** If $m > 0$ and $\bar I_c$ is positive definite, then $I$ is positive definite, because $T > 0$ for every nonzero twist.
- **Change of frame.** If ${}^B X_A$ maps motion vectors from frame $A$ to frame $B$, then $I_A = {}^B X_A^T\, I_B\, {}^B X_A$, which keeps the kinetic energy the same. In a frame at the center of mass, the matrix is block diagonal, $\mathrm{diag}(\bar I_c,\ m \mathbf{1})$, the form of Lynch and Park.
- **Additive.** The inertia of two bodies joined rigidly is the sum of their inertias in the same frame. This is how the [composite rigid body algorithm](/composite-rigid-body-algorithm/) builds the inertias of subtrees.
- **Physical consistency.** Not every symmetric positive definite $6 \times 6$ matrix is a spatial inertia. The bottom-right block must be $m \mathbf{1}$, the off-diagonal block must be $m$ times a skew-symmetric matrix, and the principal moments $J_1, J_2, J_3$ of $\bar I_c$ must satisfy the triangle inequalities $J_1 + J_2 \ge J_3$ and so on, which hold for every real mass distribution.

## Examples and non-examples

**A rod about its end.** A thin rod of mass 2 kg and length 1 m lies along $x$, with the frame at one end. Then $c = (0.5, 0, 0)$ m and $\bar I_c = \mathrm{diag}(0, \tfrac16, \tfrac16)$ kg m$^2$, and
$$I = \begin{pmatrix} \mathrm{diag}(0, \tfrac23, \tfrac23) & m[c] \\ m[c]^T & 2\,\mathbf{1} \end{pmatrix}, \qquad m[c] = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix}.$$
The top-left block gives $\tfrac23 = mL^2/3$, the moment of inertia of a rod about its end. If the rod turns about the $z$ axis through the origin at 3 rad/s, then $v = (0, 0, 3,\ 0, 0, 0)$ and $h = I v = (0, 0, 2,\ 0, 3, 0)$. The linear momentum $(0, 3, 0)$ kg m/s is the mass times the velocity $(0, 1.5, 0)$ m/s of the center, and the kinetic energy is $\tfrac12 v^T h = 3$ J.

**A point mass.** A point mass $m$ at $c$ has $\bar I_c = 0$, and its spatial inertia $m \begin{pmatrix} [c][c]^T & [c] \\ [c]^T & \mathbf{1} \end{pmatrix}$ has rank 3: a rotation about an axis through the point gives it no energy. It is a valid spatial inertia, positive semidefinite but not positive definite.

**Non-example: unequal masses.** $\mathrm{diag}(1, 1, 1,\ 1, 2, 3)$ is symmetric and positive definite, but its bottom-right block is not a multiple of the identity, so no rigid body has it.

**Non-example: inertia without mass.** $\mathrm{diag}(1, 1, 1,\ 0, 0, 0)$ has a rotational inertia but zero mass. No real body has it.

**Non-example: a positive definite but impossible body.** With $m = 1$, $c = 0$ and $\bar I_c = \mathrm{diag}(1, 1, 3)$, the matrix is positive definite, but $1 + 1 < 3$ breaks the triangle inequality, so no mass distribution has these principal moments.

## Related definitions

- [Newton-Euler equations](/newton-euler-equations/): the equations of motion of one body that the spatial inertia puts in one line.
- [Articulated-body inertia](/articulated-body-inertia/): the apparent inertia of a body with a free subtree beyond it, which starts from the spatial inertia and is in general not one.
- [Joint-space inertia matrix](/joint-space-inertia-matrix/): the inertia of a whole robot in joint coordinates, the sum of $J_i^T I_i J_i$ over the bodies.
- [Centroidal momentum matrix](/centroidal-momentum-matrix/): maps the joint velocities to the total momentum, built from the spatial inertias of the bodies.
- [Base inertial parameters](/base-inertial-parameters/): the combinations of the ten parameters of each body that the dynamics of a robot can identify.

## References
