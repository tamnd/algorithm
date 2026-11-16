---
tag: G9YJE0
kind: definition
slug: rigid-body-transformation
name: Rigid body transformation
aliases:
- rigid motion
- proper rigid transformation
area: robotics/rigid-body-motion
level: intro
summary: "A map of space that keeps distances and handedness; every such map is x -> R x + p with a rotation R and a translation p."
prereqs: [special-orthogonal-group]
see_also: [homogeneous-transformation-matrix, special-euclidean-group, chasles-theorem, screw-motion, robot-pose, pose-compounding-operators, datum-reference-frame, kabsch-algorithm]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.1 (homogeneous transformation matrices and the uses of a rigid-body motion as a configuration, a change of frame and a displacement)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 1 (rigid body transformations, defined by the preservation of distance and of the cross product)
---

A rigid body transformation is a map of three-dimensional space that keeps the distance between every two points and keeps the handedness of every frame, so that it moves a solid body without bending, stretching or mirroring it.
Every such map has the form $x \mapsto Rx + p$, where $R$ is a rotation matrix and $p$ is a translation vector.
It is used in two ways: to move a body to a new place, and to change the coordinates of a point from one frame to another.
The set of all rigid body transformations, with composition as the operation, is the [special Euclidean group](/special-euclidean-group/) SE(3), and the [homogeneous transformation matrix](/homogeneous-transformation-matrix/) writes each one as a $4 \times 4$ matrix.

## Definition

A map $g : \mathbb{R}^3 \to \mathbb{R}^3$ is a rigid body transformation if

1. it keeps distances: $|g(x) - g(y)| = |x - y|$ for all points $x$ and $y$, and
2. it keeps handedness: the map of vectors $g_*(y - x) = g(y) - g(x)$ satisfies $g_*(a \times b) = g_*(a) \times g_*(b)$.

**Characterization.** A map $g$ is a rigid body transformation if and only if $g(x) = Rx + p$ with $R \in SO(3)$ and $p \in \mathbb{R}^3$.
This is a proved result; we sketch the proof.
Put $p = g(0)$ and $f(x) = g(x) - p$.
Then $f(0) = 0$ and $f$ keeps distances, so it also keeps lengths, $|f(x)| = |x|$.
From $|f(x) - f(y)|^2 = |x - y|^2$ it follows that $f(x) \cdot f(y) = x \cdot y$.
So $f$ maps the standard basis to an orthonormal basis $r_1, r_2, r_3$, and the coordinates of $f(x)$ in that basis are $r_i \cdot f(x) = e_i \cdot x = x_i$.
So $f(x) = Rx$ with the orthogonal matrix $R = (r_1\ r_2\ r_3)$.
Condition 2 gives $r_1 \times r_2 = r_3$, so $\det R = 1$.
The converse is a direct check.

Frames.
Attach a frame $\{b\}$ to the body, and let $\{s\}$ be a fixed frame.
The configuration of the body is the pair $(R_{sb}, p_{sb})$: $R_{sb}$ is the orientation of $\{b\}$ and $p_{sb}$ is the position of the origin of $\{b\}$, both written in $\{s\}$.
A point with coordinates $x_b$ in $\{b\}$ has the coordinates $x_s = R_{sb}x_b + p_{sb}$ in $\{s\}$.

Composition and inverse.
If $g_1(x) = R_1x + p_1$ and $g_2(x) = R_2x + p_2$, then $g_1(g_2(x)) = R_1R_2x + R_1p_2 + p_1$.
The inverse of $g(x) = Rx + p$ is $g^{-1}(x) = R^{\mathsf T}x - R^{\mathsf T}p$.
Composition is not commutative.

Points and vectors.
A point moves by $x \mapsto Rx + p$, but a free vector, the difference of two points, moves by $v \mapsto Rv$ only.
A velocity or a force direction is a vector, not a point.

## Examples and non-examples

- A pure translation: $R = I$, $x \mapsto x + p$.
- A pure rotation about the origin: $p = 0$, $x \mapsto Rx$.
- A rotation $R$ about an axis through a point $q$: $x \mapsto R(x - q) + q$, so the translation part is $p = (I - R)q$, which is not zero if $q$ is not on the axis through the origin. For $R = R_z(\pi/2)$ and $q = (0, 1, 0)$, $p = (1, 1, 0)$.
- A screw motion: a rotation about a line and a translation along the same line. By [Chasles' theorem](/chasles-theorem/), every rigid body transformation is a [screw motion](/screw-motion/).
- Non-example: the reflection $x \mapsto (x_1, x_2, -x_3)$ keeps distances but reverses handedness. It is an improper rigid transformation, and a real body cannot be moved this way.
- Non-example: the scaling $x \mapsto 2x$ keeps angles and handedness but not distances.
- Non-example: the map that rotates each point about the $z$ axis by an angle that depends on its height, a twist of a bar in the everyday sense, keeps the distance to the axis but not the distances between points at different heights.

## Related definitions

- The [homogeneous transformation matrix](/homogeneous-transformation-matrix/) $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix}$ makes composition a matrix product.
- The [special Euclidean group](/special-euclidean-group/) SE(3) is the group of all rigid body transformations.
- A [robot pose](/robot-pose/) is a rigid body transformation that gives the place of a robot or a sensor, and the [pose compounding operators](/pose-compounding-operators/) compose and invert poses.
- In tolerancing, a [datum reference frame](/datum-reference-frame/) fixes the coordinates of a part up to a rigid body transformation.
- The [Kabsch algorithm](/kabsch-algorithm/) finds the rigid body transformation that best maps one set of points to another.
- The [twist](/rigid-body-twist/) is the velocity of a curve of rigid body transformations.

## References
