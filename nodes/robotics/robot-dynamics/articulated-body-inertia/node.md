---
tag: M2V3VX
kind: definition
slug: articulated-body-inertia
name: Articulated-body inertia
aliases:
- articulated body inertia matrix
area: robotics/robot-dynamics
level: advanced
summary: The apparent spatial inertia of a body together with the free subtree beyond it, as felt by a force at its inboard joint.
prereqs: [spatial-inertia, schur-complement]
see_also: [articulated-body-algorithm, composite-rigid-body-algorithm, joint-space-inertia-matrix, forward-dynamics, operational-space-formulation, gauss-principle-of-least-constraint, positive-definite-matrix, spatial-vector-algebra]
sources:
  - paper: doi:10.1177/027836498300200102
    title: Roy Featherstone, The calculation of robot dynamics using articulated-body inertias, The International Journal of Robotics Research 2(1), 1983
    locator: pages 13 to 30
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 7 (forward dynamics by propagation methods): the articulated-body inertia, its calculation and the articulated-body algorithm"
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 3, Dynamics, by Roy Featherstone and David E. Orin"
---

The articulated-body inertia of a body in a robot is the $6 \times 6$ inertia that the body seems to have when the joints beyond it are free to move. A push on the body moves it and also makes the bodies beyond it swing, and the swing takes up some of the push, so the body feels lighter than the whole subtree locked together, but heavier than the body alone. Featherstone (1983) introduced the articulated-body inertia, and the [articulated-body algorithm](/articulated-body-algorithm/) computes the [forward dynamics](/forward-dynamics/) of a tree in $\Theta(n)$ time with it.

## Definition

Take a kinematic tree of rigid bodies with one-degree-of-freedom joints, in the notation of [spatial vector algebra](/spatial-vector-algebra/): body $i$ has the [spatial inertia](/spatial-inertia/) $I_i$, joint $i$ connects body $i$ to its parent $\lambda(i)$ with the axis $S_i$, and $X_c$ maps motion vectors from the frame of the parent of body $c$ to the frame of body $c$. The articulated body $i$ is body $i$ together with all its descendants, cut free from the parent at joint $i$, with the joints inside the subtree free to move.

Apply a test wrench $f$ to body $i$ and let $a_i$ be the spatial acceleration of body $i$ that results, with the state $(q, \dot q)$ and the joint forces of the subtree fixed. Then $f$ is an affine function of $a_i$:
$$f = I^A_i\, a_i + p^A_i .$$
The symmetric $6 \times 6$ matrix $I^A_i$ is the **articulated-body inertia** of body $i$, and the 6-vector $p^A_i$ is the **articulated-body bias force**, the wrench needed to give body $i$ zero acceleration. $I^A_i$ depends only on the joint positions in the subtree. $p^A_i$ also contains the velocity product terms, the joint forces and the external forces of the subtree.

**As a Schur complement.** Write the kinetic energy of the free subtree with the twist $v$ of body $i$ and the joint rates $\dot q_s$ of the joints in the subtree as $\tfrac12 \begin{pmatrix} v \\ \dot q_s \end{pmatrix}^T \begin{pmatrix} I^c_i & F \\ F^T & H_s \end{pmatrix} \begin{pmatrix} v \\ \dot q_s \end{pmatrix}$, where $I^c_i$ is the composite inertia of the subtree locked into one rigid body, $H_s$ is the joint-space inertia matrix of the subtree joints, and $F$ is the coupling. With the joints free and the bias terms set to zero, $f = I^c_i a_i + F \ddot q_s$ and $0 = F^T a_i + H_s \ddot q_s$, so
$$I^A_i = I^c_i - F H_s^{-1} F^T ,$$
the [Schur complement](/schur-complement/) of $H_s$.

**The recursion.** For a leaf, $I^A_i = I_i$. For an inner body,
$$I^A_i = I_i + \sum_{c\,:\,\lambda(c) = i} X_c^T \Big( I^A_c - \frac{U_c U_c^T}{D_c} \Big) X_c, \qquad U_c = I^A_c S_c, \quad D_c = S_c^T U_c .$$
The matrix $I^a_c = I^A_c - U_c U_c^T / D_c$ is the inertia that the parent feels through the free joint $c$. The scalar $D_c$ is the inertia that joint $c$ itself feels.

**Properties.**

- $I^A_i$ is symmetric and positive semidefinite, and positive definite when $I_i$ is positive definite.
- In the order of positive semidefinite matrices, $I_i \preceq I^A_i \preceq I^c_i$. For a given $a_i$ at zero velocity and zero joint forces, the free joints move so as to minimize $\sum_j \tfrac12 a_j^T I_j a_j$ over the subtree (Gauss's principle), and the minimum is $\tfrac12 a_i^T I^A_i a_i$. Dropping all bodies but $i$ gives a smaller value, and locking the joints gives a larger one, $\tfrac12 a_i^T I^c_i a_i$.
- $I^a_c S_c = 0$: the parent feels no inertia along the motion that the free joint $c$ allows.
- In general $I^A_i$ is not the spatial inertia of any rigid body. Its linear block need not be a multiple of the identity, and $I^a_c$ is always singular.

## Examples and non-examples

**A slider.** Let body 1 be massless, and let body 2 be a point mass $m$ at the origin of frame 1 on a prismatic joint along $x$, so $S_2 = (0, 0, 0,\ 1, 0, 0)$. Locked, the subtree is a point mass at the origin, with $I^c_1 = \mathrm{diag}(0, 0, 0,\ m, m, m)$. Free, $U_2 = (0, 0, 0,\ m, 0, 0)$ and $D_2 = m$, so
$$I^A_1 = \mathrm{diag}(0, 0, 0,\ 0, m, m).$$
A push along $x$ meets no inertia, because the mass slides away, and a push along $y$ or $z$ meets the whole mass. This $I^A_1$ is not a spatial inertia: no mass gives the linear block $\mathrm{diag}(0, m, m)$.

**The planar arm with two links.** Take two revolute joints about $z$, links of 1 m and point masses of 1 kg at the link ends, with the joint-space inertia matrix $M = \begin{pmatrix} 3 + 2c_2 & 1 + c_2 \\ 1 + c_2 & 1 \end{pmatrix}$, $c_2 = \cos q_2$. Joint 1 feels the scalar
$$D_1 = S_1^T I^A_1 S_1 = M_{11} - \frac{M_{12}^2}{M_{22}} = 2 - c_2^2$$
kg m$^2$ with joint 2 free. It lies between $1$, the inertia of the first mass alone about joint 1, and $3 + 2c_2$, the inertia of the arm with joint 2 locked, because $3 + 2c_2 - (2 - c_2^2) = (1 + c_2)^2 \ge 0$. At $q_2 = \pi/2$, $D_1 = 2$ and the full $I^A_1$ is the matrix in the example of the [articulated-body algorithm](/articulated-body-algorithm/). For a serial chain in general, $D_1 = 1 / (M^{-1})_{11}$.

**A single body.** For a leaf, nothing is free beyond the body, and $I^A_i = I_i$, its own spatial inertia.

**Non-example: the composite inertia.** $I^c_i$, the inertia of the subtree with all joints locked, is what the [composite rigid body algorithm](/composite-rigid-body-algorithm/) uses. It equals $I^A_i$ for a leaf, and in general it is larger, as the slider shows.

**Non-example: the joint inertia.** The scalar $D_i = S_i^T I^A_i S_i$ is the inertia felt along joint $i$, not the $6 \times 6$ articulated-body inertia.

**Non-example: the operational-space inertia.** The inertia $\Lambda$ of the [operational-space formulation](/operational-space-formulation/) is felt at an end effector of the whole robot, with the base fixed and every joint free. $I^A_i$ is felt at body $i$ with only the subtree beyond $i$, and with body $i$ itself free in all six directions.

## Related definitions

- [Spatial inertia](/spatial-inertia/): the inertia of one rigid body, the starting value $I^A_i = I_i$ of the recursion.
- [Composite rigid body algorithm](/composite-rigid-body-algorithm/): uses the locked inertia $I^c_i$ in place of $I^A_i$ to build the joint-space inertia matrix.
- [Joint-space inertia matrix](/joint-space-inertia-matrix/): the scalars $D_i$ are Schur complements of it.
- [Schur complement](/schur-complement/): the algebra behind $I^A_i = I^c_i - F H_s^{-1} F^T$.
- [Gauss's principle of least constraint](/gauss-principle-of-least-constraint/): the minimum that gives the bounds $I_i \preceq I^A_i \preceq I^c_i$.
- [Positive definite matrix](/positive-definite-matrix/): the order in which the bounds hold.

## References
