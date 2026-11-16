---
tag: 1KXH7W
kind: definition
slug: screw-motion
name: Screw motion
aliases:
- screw displacement
- screw axis
area: robotics/rigid-body-motion
level: core
summary: A rotation about an axis together with a translation along it, given by the axis, the pitch and the magnitude.
prereqs: [rigid-body-transformation, special-euclidean-group, rigid-body-twist]
see_also: [chasles-theorem, se3-exponential-map, wrench, dual-quaternion, kinematic-pair, product-of-exponentials-formula, instant-center-of-velocity, small-displacement-torsor]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Sections 3.3.2 and 3.3.3 (the screw interpretation of a twist, the screw axis S, and exponential coordinates of rigid-body motions)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 3.3 (screws, a geometric description of twists, with the pitch, axis and magnitude of a screw)
  - book: isbn:9780521636506
    title: Robert S. Ball, A Treatise on the Theory of Screws, Cambridge University Press, 1900 (reprinted 1998)
    locator: Chapter 1 (twists and wrenches; the screw as a line with a pitch)
---

A screw motion is a rigid motion that turns a body by an angle $\theta$ about a fixed line, the screw axis, and at the same time slides it by the distance $h\theta$ along the same line, where $h$ is the pitch.
A nut that turns on a bolt makes a screw motion, and so does every joint of a robot: a revolute joint is a screw with pitch 0, and a prismatic joint is a screw with infinite pitch.
By [Chasles' theorem](/chasles-theorem/), every rigid motion of space is a screw motion, so the axis, the pitch and the magnitude describe any element of the [special Euclidean group](/special-euclidean-group/) SE(3).
In coordinates, the screw is the unit [twist](/rigid-body-twist/) $S$, and the motion is the [exponential](/se3-exponential-map/) $e^{[S]\theta}$.

## Definition

A **screw** is a line $L$ in space together with a number $h$, the **pitch**, where $h$ may also be $\infty$.
Give the line by a point $q$ on it and a unit direction $\hat s$.

For a finite pitch $h$ and a **magnitude** $\theta \in \mathbb{R}$ (an angle in radians), the **screw motion** about the screw is the map

$$x \mapsto R\,(x - q) + q + h\theta\,\hat s, \qquad R = \operatorname{Rot}(\hat s, \theta),$$

where $\operatorname{Rot}(\hat s, \theta)$ is the rotation by $\theta$ about $\hat s$ from [Rodrigues' formula](/rodrigues-rotation-formula/).
As a [homogeneous transformation matrix](/homogeneous-transformation-matrix/),

$$T = \begin{pmatrix} R & (I - R)\,q + h\theta\,\hat s \\ 0 & 1 \end{pmatrix} .$$

The body turns by $\theta$ about $L$ and moves by $d = h\theta$ along $L$.
Pitch 0 gives a pure rotation about $L$.

For infinite pitch, the screw motion is the pure translation $x \mapsto x + \theta\,\hat s$, and the magnitude $\theta$ is the distance.
Only the direction of $L$ matters then, not its position.

**The screw axis as a six-vector.**
In the order (angular, linear) of Lynch and Park, the screw axis is

$$S = (\hat s,\; -\hat s \times q + h\hat s) \quad (h \text{ finite}), \qquad S = (0,\; \hat s) \quad (h = \infty).$$

Conversely, for $S = (\omega, v)$ with $|\omega| = 1$, the pitch is $h = \omega^{\mathsf T}v / \omega^{\mathsf T}\omega$, and the point $q = \omega \times v / |\omega|^2$ lies on the axis.
A twist $\mathcal{V} = S\dot\theta$ is a screw axis times a speed, so a screw motion is the motion of a body that keeps a constant twist for unit time with total angle $\theta$.

**Why the two forms agree.**
Let $x(t) = R(t)(x_0 - q) + q + h t\,\hat s$ with $R(t) = \operatorname{Rot}(\hat s, t)$.
Its velocity is $\dot x = \hat s \times R(t)(x_0 - q) + h\hat s = \hat s \times (x(t) - q) + h\hat s = \hat s \times x(t) + (-\hat s \times q + h\hat s)$.
This is the linear equation $\dot x = [\hat s]x + v$ given by $S$, with $x(0) = x_0$.
Its solution at $t = \theta$ is $e^{[S]\theta}$ applied to $x_0$, so $T = e^{[S]\theta}$.

## Examples and non-examples

**A rotation about an offset axis (pitch 0).**
Take the vertical line through $q = (0, 1, 0)$, $\hat s = (0, 0, 1)$, $h = 0$ and $\theta = \pi/2$.
Then $S = (0, 0, 1, 1, 0, 0)$, $R = R_z(\pi/2)$, and the translation is $(I - R)q = (0, 1, 0) - (-1, 0, 0) = (1, 1, 0)$.
The origin goes to $(1, 1, 0)$: it is 1 m from the axis and turns by a quarter turn about it.
This is the check value of the [exponential map of SE(3)](/se3-exponential-map/), read as a screw.

**The same axis with pitch 0.5 m/rad.**
Now $S = (0, 0, 1, 1, 0, 0.5)$, and the translation is $(1, 1, 0) + 0.5 \cdot \tfrac\pi2\,(0, 0, 1) = (1, 1, 0.7854)$.
The rotation part does not change.

**A nut on a bolt.**
A nut with a right-hand thread that advances 1.5 mm per full turn along $\hat s$ makes the screw motion with pitch $h = 1.5/(2\pi) \approx 0.2387$ mm/rad.
A right-hand thread has positive pitch: when the nut turns in the positive sense about $\hat s$, it advances along $+\hat s$.
A left-hand thread has negative pitch.

**A pure translation.**
Moving a drawer by 0.3 m along $\hat s = (1, 0, 0)$ is the screw motion with infinite pitch, $S = (0, 0, 0, 1, 0, 0)$ and $\theta = 0.3$.

**The pair $(S, \theta)$ is not unique.**
The pair $(-S, -\theta)$ gives the same motion: the rotation by $-\theta$ about $-\hat s$ is the rotation by $\theta$ about $\hat s$, and $h(-\theta)(-\hat s) = h\theta\,\hat s$.
So the pitch does not depend on the direction chosen for the axis.
It tells right-handed screws from left-handed screws.
For pitch 0, $\theta$ and $\theta + 2\pi$ also give the same motion, but for $h \ne 0$ they do not.

**Non-example: a rotation followed by a translation that is not along the axis.**
The motion $x \mapsto R_z(\pi/2)\,x + (1, 1, 0)$ is not a screw motion about the $z$ axis, because it moves the $z$ axis.
It is still a screw motion, but about the parallel line through $(0, 1, 0)$, as the first example shows.
[Chasles' theorem](/chasles-theorem/) finds this axis for every motion.

**Non-example: reflections.**
A mirror reflection, or a reflection followed by a translation along the mirror plane, has a matrix with $\det R = -1$.
It is not a screw motion and is not in SE(3).

**Non-example: a twist.**
A twist is a velocity and lives in the Lie algebra $\mathfrak{se}(3)$.
It is a screw axis times a speed, the instantaneous screw of Mozzi, and not a finite motion.

## Related definitions

- [Rigid-body twist](/rigid-body-twist/): the velocity form, $\mathcal{V} = S\dot\theta$. The screw axis of a twist gives the axis and the pitch of the motion.
- [Exponential map of SE(3)](/se3-exponential-map/): computes $e^{[S]\theta}$ in closed form and its inverse, the logarithm, which recovers $(S, \theta)$ from $T$.
- [Chasles' theorem](/chasles-theorem/): every element of SE(3) is a screw motion.
- [Wrench](/wrench/): a force and a moment also reduce to a screw, a force along a line plus a moment about the same line (Poinsot), with the pitch $f \cdot m/|f|^2$.
- [Kinematic pair](/kinematic-pair/): the helical pair allows one screw motion with a fixed pitch, and the revolute and prismatic pairs are the cases $h = 0$ and $h = \infty$.
- [Product of exponentials formula](/product-of-exponentials-formula/): the pose of an arm is a product of screw motions, one per joint.
- [Dual quaternion](/dual-quaternion/): writes a screw motion as $\cos(\hat\theta/2) + \hat{\mathbf{s}}\sin(\hat\theta/2)$ with a dual angle $\hat\theta = \theta + \varepsilon h\theta$.
- [Instant center of velocity](/instant-center-of-velocity/): in the plane, every motion is a rotation about a point or a translation, the planar case of a screw.
- [Small displacement torsor](/small-displacement-torsor/): the first-order screw motion that tolerance analysis uses.

## References
