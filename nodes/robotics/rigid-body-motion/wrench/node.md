---
tag: 0H28MQ
kind: definition
slug: wrench
name: Wrench
aliases:
- spatial force
area: robotics/rigid-body-motion
level: core
summary: A six-vector of moment and force acting on a rigid body, dual to a twist so that their product is power.
prereqs: [rigid-body-twist, adjoint-map-se3]
see_also: [screw-motion, jacobian-statics-duality, grasp-matrix, grasp-wrench-space, contact-wrench-cone, spatial-vector-algebra, newton-euler-equations, small-displacement-torsor]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.4 (wrenches, the moment and force pair, power, and the change of frame by the transpose of the adjoint)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 5 (wrenches, screw coordinates for a wrench with Theorem 2.17 of Poinsot, and reciprocal screws)
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: Chapter 2 (spatial vector algebra; force vectors as the dual of motion vectors)
  - book: isbn:9780521636506
    title: Robert S. Ball, A Treatise on the Theory of Screws, Cambridge University Press, 1900 (reprinted 1998)
    locator: Chapter 1 (twists and wrenches)
---

A wrench is the total force and the total moment that act on a rigid body, written as one six-vector $\mathcal{F} = (m, f)$ in a chosen frame.
The force $f$ is the sum of the forces, and the moment $m$ is the sum of their moments about the origin of the frame, plus any pure couples.
Two loads with the same wrench have the same effect on a rigid body, so a wrench is what statics means by an equivalent force system.
In robotics the wrench is the dual of the [twist](/rigid-body-twist/): the power of a wrench on a moving body is the dot product of the two six-vectors, and this fixes how a wrench changes from one frame to another.

## Definition

Fix a frame $\{a\}$.
Let forces $f_1, \dots, f_k$ act at the points $r_1, \dots, r_k$, all in $\{a\}$ coordinates, and let $c$ be the sum of the pure couples on the body.
The **wrench** in frame $\{a\}$ is

$$\mathcal{F}_a = \begin{pmatrix} m_a \\ f_a \end{pmatrix}, \qquad f_a = \sum_i f_i, \qquad m_a = c + \sum_i r_i \times f_i .$$

The moment comes first, as in the order $(\omega, v)$ of a twist in Lynch and Park.
The units are newton metres for $m$ and newtons for $f$.

**Power.**
If the body moves with the twist $\mathcal{V}_a = (\omega_a, v_a)$, the point $r_i$ has the velocity $v_a + \omega_a \times r_i$.
The power of the load is

$$P = \sum_i f_i \cdot (v_a + \omega_a \times r_i) + c \cdot \omega_a = \mathcal{V}_a^{\mathsf T}\mathcal{F}_a = \omega_a \cdot m_a + v_a \cdot f_a ,$$

because $f_i \cdot (\omega_a \times r_i) = \omega_a \cdot (r_i \times f_i)$.
So a wrench is a linear function on twists, an element of the dual space $\mathfrak{se}^*(3)$.

**Change of frame.**
Let $T_{ab} = (R, p)$ be the pose of $\{b\}$ in $\{a\}$.
Power does not depend on the frame, and twists change by the [adjoint map](/adjoint-map-se3/), $\mathcal{V}_a = [\mathrm{Ad}_{T_{ab}}]\mathcal{V}_b$.
From $\mathcal{V}_b^{\mathsf T}\mathcal{F}_b = \mathcal{V}_a^{\mathsf T}\mathcal{F}_a = \mathcal{V}_b^{\mathsf T}[\mathrm{Ad}_{T_{ab}}]^{\mathsf T}\mathcal{F}_a$ for every $\mathcal{V}_b$,

$$\mathcal{F}_b = [\mathrm{Ad}_{T_{ab}}]^{\mathsf T}\mathcal{F}_a, \qquad \text{that is,} \qquad m_b = R^{\mathsf T}(m_a - p \times f_a), \quad f_b = R^{\mathsf T}f_a .$$

In words, take the moment about the new origin $p$, then write both parts in the axes of $\{b\}$.
This is the rule of statics for moving the reference point, in matrix form.

**The screw of a wrench (Poinsot).**
If $f \ne 0$, every wrench is a force $f$ along one line plus a moment parallel to that line.
The line has the direction $f$ and passes through $q = f \times m/|f|^2$, and the moment along it is $h f$ with the pitch $h = f \cdot m/|f|^2$.
If $h = 0$, the wrench is a pure force along a line.
If $f = 0$, the wrench is a pure couple, a screw with infinite pitch, and the moment $m$ is the same about every point.

## Examples and non-examples

**A weight at the end of a bar.**
A force $f = (0, 0, -10)$ N acts at $r = (0.5, 0, 0)$ m in frame $\{a\}$.
Then $m_a = r \times f = (0, 5, 0)$ N m and $\mathcal{F}_a = (0, 5, 0, 0, 0, -10)$.

- Move to the frame $\{b\}$ at $p = (0.5, 0, 0)$ with the same axes. Then $m_b = m_a - p \times f = (0, 5, 0) - (0, 5, 0) = 0$, and $\mathcal{F}_b = (0, 0, 0, 0, 0, -10)$. The force acts through the origin of $\{b\}$, so it has no moment there.
- Power: turn the bar about the $y$ axis of $\{a\}$ at 1 rad/s, $\mathcal{V}_a = (0, 1, 0, 0, 0, 0)$. The end point moves with $\omega \times r = (0, 0, -0.5)$ m/s, down with the weight, and the power is $\mathcal{V}_a^{\mathsf T}\mathcal{F}_a = 5$ W. In $\{b\}$ the same motion is $\mathcal{V}_b = (0, 1, 0, 0, 0, -0.5)$, and $\mathcal{V}_b^{\mathsf T}\mathcal{F}_b = (-0.5)(-10) = 5$ W again.
- Poinsot: $f \cdot m_a = 0$, so the pitch is 0, and $q = f \times m_a/|f|^2 = (50, 0, 0)/100 = (0.5, 0, 0)$. The line of the force is recovered from the wrench alone.
- A joint: a revolute joint about the $y$ axis of $\{a\}$ has the screw axis $S = (0, 1, 0, 0, 0, 0)$, and the load puts the torque $S^{\mathsf T}\mathcal{F}_a = 5$ N m on it. This is the one-joint case of $\tau = J^{\mathsf T}\mathcal{F}$ in [the duality of the Jacobian and statics](/jacobian-statics-duality/).

**A couple.**
The forces $(0, 0, 10)$ N at $(0.1, 0, 0)$ m and $(0, 0, -10)$ N at $(-0.1, 0, 0)$ m sum to $f = 0$ and give $m = (0, -1, 0) + (0, -1, 0) = (0, -2, 0)$ N m.
The wrench $(0, -2, 0, 0, 0, 0)$ is the same in every frame with the same axes, because $p \times f = 0$.

**A force and a parallel moment.**
A drill that pushes with $f = (0, 0, -20)$ N along its axis through the origin and turns with $m = (0, 0, -1)$ N m gives the wrench $(0, 0, -1, 0, 0, -20)$ with pitch $h = 20/400 = 0.05$ m.
No single force can replace it.

**Non-example: a force without its line.**
The vector $f$ alone is not a wrench.
The same $f$ at two points on different lines gives two wrenches with different moments and different effects on the body.

**Non-example: a twist.**
A twist also has six numbers, but it changes by $[\mathrm{Ad}_T]$ and not by $[\mathrm{Ad}_T]^{\mathsf T}$.
The product $\mathcal{V}^{\mathsf T}\mathcal{V}$ of a twist with itself changes from frame to frame and has no physical meaning, while $\mathcal{V}^{\mathsf T}\mathcal{F}$ is the power in every frame.

**Non-example: the wrong order.**
Murray, Li and Sastry write a wrench as $(f, \tau)$, force first, and their twists as $(v, \omega)$.
Both orders are correct within one book.
Mixing a twist in one order with a wrench in the other gives a number that is not the power.

## Related definitions

- [Rigid-body twist](/rigid-body-twist/) and the [adjoint map](/adjoint-map-se3/): the motion side of the pairing, and the matrix whose transpose moves wrenches.
- [Screw motion](/screw-motion/): the pitch and the axis of a wrench are the same kind of object as those of a twist. A twist and a wrench are reciprocal when $\mathcal{V}^{\mathsf T}\mathcal{F} = 0$, that is, when the wrench does no work on the motion.
- [Jacobian and statics duality](/jacobian-statics-duality/): the joint torques that balance a tip wrench are $\tau = J^{\mathsf T}\mathcal{F}$.
- [Grasp matrix](/grasp-matrix/), [grasp wrench space](/grasp-wrench-space/), [friction cone](/friction-cone/), [contact wrench cone](/contact-wrench-cone/) and [force closure](/force-closure/): contacts produce wrenches, and grasp analysis studies the set of wrenches they can produce.
- [Newton-Euler equations](/newton-euler-equations/): the net wrench on a body equals the rate of change of its momentum, with the [spatial inertia](/spatial-inertia/) as the mass term.
- [Spatial vector algebra](/spatial-vector-algebra/): Featherstone calls wrenches force vectors, dual to motion vectors.
- [Small displacement torsor](/small-displacement-torsor/): the small motion that is dual to a wrench in tolerance and fixture analysis.

## References
