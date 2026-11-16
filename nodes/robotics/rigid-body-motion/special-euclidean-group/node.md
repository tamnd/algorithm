---
tag: S5FNP3
kind: definition
slug: special-euclidean-group
name: "Special Euclidean group SE(3)"
aliases:
- SE(3)
- group of rigid motions
area: robotics/rigid-body-motion
level: core
summary: "The group of all rigid body motions of space: pairs (R, p) of a rotation and a translation, written as 4 by 4 matrices, with composition as the product."
prereqs: [special-orthogonal-group, homogeneous-transformation-matrix]
see_also: [se3-exponential-map, rigid-body-twist, adjoint-map-se3, chasles-theorem, uncertainty-on-lie-groups, pose-graph-optimization, infinitesimal-rigidity, configuration-space]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.1 (the special Euclidean group SE(3) and its properties)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 3 (rigid motion in R^3, the homogeneous representation and SE(3))
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the rigid motion group as a Lie group, with its exponential, logarithm, adjoint and Jacobians
---

The special Euclidean group SE(3) is the set of all rigid body motions of three-dimensional space, each one a rotation followed by a translation, with the composition of motions as the group operation.
An element is a pair $(R, p)$ of a rotation matrix $R$ and a translation vector $p$, usually written as a $4 \times 4$ [homogeneous transformation matrix](/homogeneous-transformation-matrix/), so that composition is matrix multiplication.
It is a Lie group of dimension 6: a free rigid body has three degrees of freedom of rotation and three of translation.
SE(3) is the configuration space of a rigid body, the set of poses of a robot link, a tool or a camera, and the set of motions that keep the shape of a body or a framework unchanged.

## Definition

$$SE(3) = \left\{ T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in \mathbb{R}^{4 \times 4} : R \in SO(3),\ p \in \mathbb{R}^3 \right\}.$$

The product is $T_1T_2 = \begin{pmatrix} R_1R_2 & R_1p_2 + p_1 \\ 0 & 1 \end{pmatrix}$, the identity is $I_4$, and $T^{-1} = \begin{pmatrix} R^{\mathsf T} & -R^{\mathsf T}p \\ 0 & 1 \end{pmatrix}$.
Each element acts on points by $x \mapsto Rx + p$, and these maps are exactly the [rigid body transformations](/rigid-body-transformation/).

Structure.

- **Semidirect product.** As a set SE(3) is $SO(3) \times \mathbb{R}^3$, but the product mixes the parts: the rotation $R_1$ acts on the translation $p_2$. This makes SE(3) the semidirect product $SO(3) \ltimes \mathbb{R}^3$. The translations form a normal subgroup, and the rotations about the origin form a subgroup that is not normal.
- **Not commutative.** In general $T_1T_2 \ne T_2T_1$.
- **Manifold.** SE(3) is a connected manifold of dimension 6. It is not compact, because the translations are unbounded.
- **Lie algebra.** The tangent space at the identity is the set $\mathfrak{se}(3)$ of $4 \times 4$ matrices $[\mathcal{V}] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix}$, one for each [twist](/rigid-body-twist/) $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$.
- **Exponential.** The [exponential map](/se3-exponential-map/) from $\mathfrak{se}(3)$ to SE(3) is onto; this is the algebraic form of [Chasles' theorem](/chasles-theorem/).
- **Adjoint.** Each $T$ changes the frame of a twist by the $6 \times 6$ [adjoint map](/adjoint-map-se3/) $\mathrm{Ad}_T$.

Units.
The rotation part has no unit and the translation part has a unit of length.
So a distance between two poses that adds the two parts depends on the choice of a length scale; there is no single natural choice.

## Examples and non-examples

- $T = (R_z(\pi/2), (1, 1, 0))$ is in SE(3). It is the rotation by $90°$ about the vertical line through $(0, 1, 0)$, as one can check: it maps $(0, 1, 0)$ to $(-1, 0, 0) + (1, 1, 0) = (0, 1, 0)$.
- The translations $(I, p)$ form a subgroup isomorphic to $\mathbb{R}^3$, and the rotations $(R, 0)$ form a subgroup isomorphic to SO(3).
- The motions allowed by a joint form a subgroup: rotations about one line for a revolute joint, translations along one direction for a prismatic joint, and the screw motions of a fixed pitch about one line for a helical joint. The planar motions, rotations about the $z$ axis combined with translations in the $xy$ plane, form a subgroup isomorphic to SE(2).
- Non-example: a $4 \times 4$ matrix with a reflection in the $3 \times 3$ block keeps distances but reverses handedness, so it is in the larger Euclidean group E(3) but not in SE(3).
- Non-example: a scaling or a shear in the $3 \times 3$ block gives an affine map, not a rigid motion.
- Non-example: the set of pairs $(R, p)$ with the product $(R_1R_2, p_1 + p_2)$ is a group, the direct product $SO(3) \times \mathbb{R}^3$, but it does not describe the composition of rigid motions.

## Related definitions

- The [twist](/rigid-body-twist/) is the velocity of a curve in SE(3), and the [wrench](/wrench/) is the force that pairs with it.
- The [exponential map of SE(3)](/se3-exponential-map/) and its logarithm connect SE(3) with $\mathbb{R}^6$. Methods for [uncertainty on Lie groups](/uncertainty-on-lie-groups/) and [pose graph optimization](/pose-graph-optimization/) use them to work with small errors in SE(3).
- The [screw motion](/screw-motion/) is a one-parameter subgroup $e^{[S]\theta}$ of SE(3).
- In rigidity theory, a framework is [infinitesimally rigid](/infinitesimal-rigidity/) when its only infinitesimal motions are the trivial ones, the velocities $x \mapsto \omega \times x + v$ given by the twists of SE(3); when the joints do not lie on one line, these form a space of dimension 6.
- In motion planning, SE(3) is the [configuration space](/configuration-space/) of a free-flying rigid body.

## References
