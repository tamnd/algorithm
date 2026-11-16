---
tag: YWG58S
kind: definition
slug: adjoint-map-se3
name: "Adjoint map of SE(3)"
aliases:
- adjoint representation of SE(3)
area: robotics/rigid-body-motion
level: core
summary: "The 6 by 6 matrix Ad_T = [[R, 0], [[p] R, R]] that moves a twist from one frame to another for T = (R, p); its transpose moves a wrench the other way."
prereqs: [rigid-body-twist, special-euclidean-group]
see_also: [wrench, se3-exponential-map, space-and-body-jacobian, product-of-exponentials-formula, small-displacement-torsor, jacobian-torsor-model, uncertainty-on-lie-groups, spatial-vector-algebra]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Sections 3.3.2 and 3.4 (the adjoint representation of a transformation for twists, and the change of frame of wrenches)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Sections 4 and 5 (the adjoint transformation of twists, and the transformation of wrenches); the book orders a twist as (v, omega), so its matrix has the blocks in other places
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the adjoint action and the adjoint matrix, and their use to move tangent vectors between the local and the global frame
---

The adjoint map of SE(3) is the $6 \times 6$ matrix $\mathrm{Ad}_T$ that converts a [twist](/rigid-body-twist/), a 6-vector of angular and linear velocity, from one frame to another.
For the rigid motion $T = (R, p)$ with rotation $R$ and translation $p$, it is $\mathrm{Ad}_T = \begin{pmatrix} R & 0 \\ [p]R & R \end{pmatrix}$, where $[p]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $p$.
The rotation turns both parts of the twist, and the term $[p]R$ adds the linear velocity $p \times \omega$ that a rotation produces at a point away from its axis.
Its transpose converts a [wrench](/wrench/), a moment and a force, in the opposite direction, so that power stays the same in every frame.
In the language of Lie groups it is the adjoint representation of the group SE(3) on its Lie algebra $\mathfrak{se}(3)$.

## Definition

We use the conventions of Lynch and Park: a twist is $\mathcal{V} = (\omega, v)$ and a wrench is $\mathcal{F} = (m, f)$, the angular part first.
For $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$,

$$\mathrm{Ad}_T = \begin{pmatrix} R & 0 \\ [p]R & R \end{pmatrix} \in \mathbb{R}^{6 \times 6}.$$

It is defined by the identity $T[\mathcal{V}]T^{-1} = [\mathrm{Ad}_T\mathcal{V}]$ for every twist $\mathcal{V}$, where $[\mathcal{V}] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix}$.
To check it, multiply out: $T[\mathcal{V}]T^{-1} = \begin{pmatrix} R[\omega]R^{\mathsf T} & -R[\omega]R^{\mathsf T}p + Rv \\ 0 & 0 \end{pmatrix}$.
The upper left block is $[R\omega]$, and the upper right block is $-R\omega \times p + Rv = p \times R\omega + Rv = [p]R\omega + Rv$.

Change of frame.

- **Twists.** If $\mathcal{V}_b$ is a twist written in frame $\{b\}$, then the same twist written in frame $\{a\}$ is $\mathcal{V}_a = \mathrm{Ad}_{T_{ab}}\mathcal{V}_b$. In particular the spatial and the body twist of a moving body satisfy $\mathcal{V}_s = \mathrm{Ad}_{T_{sb}}\mathcal{V}_b$.
- **Wrenches.** If $\mathcal{F}_a$ is a wrench written in $\{a\}$, then the same wrench in $\{b\}$ is $\mathcal{F}_b = \mathrm{Ad}_{T_{ab}}^{\mathsf T}\mathcal{F}_a$. This follows from the invariance of power, $\mathcal{F}_a^{\mathsf T}\mathcal{V}_a = \mathcal{F}_b^{\mathsf T}\mathcal{V}_b$ for all $\mathcal{V}_b$.

Properties, all proved from the definition:

- **Composition.** $\mathrm{Ad}_{T_1T_2} = \mathrm{Ad}_{T_1}\mathrm{Ad}_{T_2}$, because $T_1T_2[\mathcal{V}](T_1T_2)^{-1} = T_1(T_2[\mathcal{V}]T_2^{-1})T_1^{-1}$.
- **Inverse.** $\mathrm{Ad}_T^{-1} = \mathrm{Ad}_{T^{-1}} = \begin{pmatrix} R^{\mathsf T} & 0 \\ -R^{\mathsf T}[p] & R^{\mathsf T} \end{pmatrix}$, with no general matrix inversion.
- **Determinant.** $\det \mathrm{Ad}_T = (\det R)^2 = 1$, because the matrix is block lower triangular.
- **Exponentials.** $Te^{[\mathcal{V}]}T^{-1} = e^{[\mathrm{Ad}_T\mathcal{V}]}$, so a screw motion seen from another frame is the screw motion about the moved axis.
- **Small adjoint.** The derivative of $\mathrm{Ad}$ at the identity is $\mathrm{ad}_{\mathcal{V}} = \begin{pmatrix} [\omega] & 0 \\ [v] & [\omega] \end{pmatrix}$, and $\mathrm{ad}_{\mathcal{V}_1}\mathcal{V}_2$ is the Lie bracket of the two twists. It appears in the [Newton-Euler equations](/newton-euler-equations/) of a rigid body.

Cost.
Applying $\mathrm{Ad}_T$ to a twist by blocks costs two $3 \times 3$ matrix-vector products and one cross product: $\omega' = R\omega$ and $v' = p \times \omega' + Rv$.

## Examples and non-examples

- Let $T_{ab} = (R_z(\pi/2), (1, 1, 0))$. The unit rotation about the $z$ axis of $\{b\}$, $\mathcal{V}_b = (0, 0, 1, 0, 0, 0)$, becomes $\mathcal{V}_a = (0, 0, 1, 1, -1, 0)$ in $\{a\}$. This is the rotation about the vertical line through $q = (1, 1, 0)$, the origin of $\{b\}$: $-\omega \times q = (1, -1, 0)$.
- For the same $T_{ab}$, the unit translation along the $x$ axis of $\{b\}$, $\mathcal{V}_b = (0, 0, 0, 1, 0, 0)$, becomes $\mathcal{V}_a = (0, 0, 0, 0, 1, 0)$, the translation along the $y$ axis of $\{a\}$. A translation only rotates.
- Power check, for the same $T_{ab}$: with $\mathcal{V}_b = (0.1, 0.2, 0.3, 1, 2, 3)$ and $\mathcal{F}_a = (1, -1, 2, 0.5, 0, 1)$, both $\mathcal{F}_a \cdot \mathrm{Ad}_{T_{ab}}\mathcal{V}_b$ and $(\mathrm{Ad}_{T_{ab}}^{\mathsf T}\mathcal{F}_a) \cdot \mathcal{V}_b$ equal 2.75 (computed).
- For a pure translation $T = (I, p)$, $\mathrm{Ad}_T\mathcal{V} = (\omega, v + p \times \omega)$. This is the rule for moving the velocity field of a body from one point to another, the transport of a torsor used in the [small displacement torsor](/small-displacement-torsor/) model.
- Non-example: the $6 \times 6$ matrix $\begin{pmatrix} R & 0 \\ 0 & R \end{pmatrix}$ rotates both parts but ignores the translation $p$. It gives the right answer only when the two frames share their origin.
- Non-example: with the order $(v, \omega)$ of Murray, Li and Sastry, the same map is $\begin{pmatrix} R & [p]R \\ 0 & R \end{pmatrix}$. Using one order for the twist and the other for the matrix gives wrong results without a warning.

## Related definitions

- The [twist](/rigid-body-twist/) and the [wrench](/wrench/) are the vectors that the adjoint map and its transpose move between frames.
- The [space and body Jacobians](/space-and-body-jacobian/) of an arm are related by $J_s = \mathrm{Ad}_{T_{sb}}J_b$, and the columns of the space Jacobian in the [product of exponentials formula](/product-of-exponentials-formula/) are adjoints of the joint screw axes.
- The [exponential map of SE(3)](/se3-exponential-map/) satisfies $Te^{[\mathcal{V}]}T^{-1} = e^{[\mathrm{Ad}_T\mathcal{V}]}$.
- Methods for [uncertainty on Lie groups](/uncertainty-on-lie-groups/) use $\mathrm{Ad}_T$ to move a covariance between a local and a global perturbation, as $\mathrm{Ad}_T\Sigma\mathrm{Ad}_T^{\mathsf T}$.
- The [Jacobian-torsor model](/jacobian-torsor-model/) of tolerancing chains small displacements of parts with the same transport rule.
- [Spatial vector algebra](/spatial-vector-algebra/) writes the same matrices as the transforms of motion vectors and of force vectors.

## References
