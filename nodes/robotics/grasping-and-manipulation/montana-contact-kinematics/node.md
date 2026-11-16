---
tag: 4G4JMF
kind: theorem
slug: montana-contact-kinematics
name: Montana's contact kinematics equations
aliases:
- rolling contact kinematics
area: robotics/grasping-and-manipulation
level: research
summary: Equations that give how the contact points move on two smooth surfaces in rolling and sliding contact from their relative motion and curvatures.
prereqs: [rigid-body-twist, special-euclidean-group, grasp-contact-models]
see_also: [in-hand-manipulation, nonholonomic-constraint, grasp-matrix, cooperative-manipulation, positive-definite-matrix, unicycle-model, forward-kinematics, rigid-contact-complementarity]
sources:
  - paper: doi:10.1177/027836498800700302
    title: David J. Montana, The kinematics of contact and grasp, The International Journal of Robotics Research 7(3), 17-32, 1988
    locator: the whole paper (the contact equations for two smooth surfaces and their use in grasping and tactile sensing)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5, Theorem 5.11 (page 250, equation 5.28), its proof, Corollary 5.11.1 for rolling, and Example 5.7 for the sphere
  - paper: doi:10.1109/70.88118
    title: Zexiang Li and John F. Canny, Motion of two rigid bodies with rolling constraint, IEEE Transactions on Robotics and Automation 6(1), 62-72, 1990
    locator: the whole paper (the rolling equations as a nonholonomic system, and the use of Chow's theorem to decide which contact configurations can be reached)
---

Montana's contact kinematics equations describe how the point of contact moves over two smooth bodies that touch at one point while the bodies move. Given the relative motion of the bodies and the shape of the two surfaces near the contact, they give the speed of the contact point in a chart on each surface and the rate at which the two surfaces turn against each other about the common normal. They hold for rolling and for sliding, and they are the basis of the analysis of fingers that roll on a grasped object.

## Statement

**Charts and frames.** Each body $i \in \{f, o\}$ (finger and object) has a surface $S_i$ and a chart $c_i : U_i \subset \mathbb{R}^2 \to S_i$, written in the body's own frame, with these properties:

- $c_i$ is a smooth (at least $C^2$) embedding of an open set $U_i$, so it covers a patch of the surface near the contact;
- $c_i$ is *orthogonal*: the partial derivatives $c_{iu}$ and $c_{iv}$ are orthogonal and not zero at every point;
- it is *right-handed*: the unit outward normal is $n_i = c_{iu} \times c_{iv} / \lvert c_{iu} \times c_{iv} \rvert$.

A point $\alpha_i = (u_i, v_i) \in U_i$ has the *Gauss frame* $(x_i, y_i, n_i)$ with $x_i = c_{iu} / \lvert c_{iu} \rvert$ and $y_i = c_{iv} / \lvert c_{iv} \rvert$. At that point the chart has three $2 \times 2$ and $1 \times 2$ forms:

$$M_i = \begin{bmatrix} \lvert c_{iu} \rvert & 0 \\ 0 & \lvert c_{iv} \rvert \end{bmatrix}, \qquad K_i = \begin{bmatrix} x_i^T \\ y_i^T \end{bmatrix} \begin{bmatrix} \dfrac{n_{iu}}{\lvert c_{iu} \rvert} & \dfrac{n_{iv}}{\lvert c_{iv} \rvert} \end{bmatrix}, \qquad T_i = y_i^T \begin{bmatrix} \dfrac{x_{iu}}{\lvert c_{iu} \rvert} & \dfrac{x_{iv}}{\lvert c_{iv} \rvert} \end{bmatrix}.$$

These are the *metric*, the *curvature form* (symmetric; positive definite for a strictly convex surface) and the *torsion form* of the chart.

**Contact coordinates.** The bodies touch at one point, $c_f(\alpha_f)$ on the finger and $c_o(\alpha_o)$ on the object, with opposite normals. The *angle of contact* $\psi$ is the angle between $x_f$ and $x_o$, measured so that $x_o = \cos\psi\, x_f - \sin\psi\, y_f$. The vector $\eta = (\alpha_f, \alpha_o, \psi) \in U_f \times U_o \times S^1$ fixes the contact up to the motion of the pair as a whole. Write

$$R_\psi = \begin{bmatrix} \cos\psi & -\sin\psi \\ -\sin\psi & -\cos\psi \end{bmatrix}, \qquad \tilde K_o = R_\psi K_o R_\psi,$$

so $\tilde K_o$ is the curvature form of the object in the $(x_f, y_f)$ axes. The matrix $K_f + \tilde K_o$ is the *relative curvature form*.

**Relative motion.** Let $(v_x, v_y, v_z, \omega_x, \omega_y, \omega_z)$ be the velocity of the object relative to the finger: the [twist](/rigid-body-twist/) of the object frame seen from the finger frame, written in a frame fixed to the object that agrees with the object's contact frame at this instant.

**Theorem (Montana 1988; Murray, Li and Sastry 1994, Theorem 5.11).** Assume the hypotheses above and that the contact is *nondegenerate*: $K_f + \tilde K_o$ is invertible. If the bodies stay in contact, the contact coordinates move by

$$\dot\alpha_f = M_f^{-1} (K_f + \tilde K_o)^{-1} \left( \begin{bmatrix} -\omega_y \\ \omega_x \end{bmatrix} - \tilde K_o \begin{bmatrix} v_x \\ v_y \end{bmatrix} \right),$$

$$\dot\alpha_o = M_o^{-1} R_\psi (K_f + \tilde K_o)^{-1} \left( \begin{bmatrix} -\omega_y \\ \omega_x \end{bmatrix} + K_f \begin{bmatrix} v_x \\ v_y \end{bmatrix} \right),$$

$$\dot\psi = \omega_z + T_f M_f \dot\alpha_f + T_o M_o \dot\alpha_o, \qquad 0 = v_z.$$

**Rolling and sliding.** The equations hold for every motion that keeps contact, which is the meaning of $v_z = 0$.

- *Sliding* is the case $(v_x, v_y) \ne 0$: the material points at the contact move against each other. For pure sliding, $\omega = 0$, the contact moves on the finger by $\dot\alpha_f = -M_f^{-1}(K_f + \tilde K_o)^{-1} \tilde K_o v$ and on the object by $\dot\alpha_o = M_o^{-1} R_\psi (K_f + \tilde K_o)^{-1} K_f v$.
- *Rolling* is the case $v = 0$ and $\omega_z = 0$: no slip and no spin about the normal (Corollary 5.11.1 in Murray, Li and Sastry). Then

$$\dot\alpha_f = M_f^{-1} (K_f + \tilde K_o)^{-1} \begin{bmatrix} -\omega_y \\ \omega_x \end{bmatrix}, \qquad \dot\alpha_o = M_o^{-1} R_\psi (K_f + \tilde K_o)^{-1} \begin{bmatrix} -\omega_y \\ \omega_x \end{bmatrix},$$

and $\dot\psi = T_f M_f \dot\alpha_f + T_o M_o \dot\alpha_o$. With a soft finger contact, which allows spin, $\omega_z$ is free and adds to $\dot\psi$.

## In plain words

Roll a ball on a table. The point where they touch moves over the table and over the ball. How fast it moves on each depends on how the ball turns and on how curved the two surfaces are: a small ball moves its contact point over its surface faster than a large one for the same turn. If the ball also slides, the slip moves the contact point too. The equations give these speeds, in coordinates drawn on each surface, and the rate at which the ball twists against the table.

## Proof

This is a sketch; the full proof is in Murray, Li and Sastry (1994), with the conventions above. Write $a = M_f \dot\alpha_f$ and $b = R_\psi M_o \dot\alpha_o$. Both are velocities of the contact point in the $(x_f, y_f)$ axes: $a$ is its speed over the finger surface, and $b$ is its speed over the object surface, turned from the object axes to the finger axes by $R_\psi$ (which also accounts for the opposite normals).

1. **The contact points coincide.** Differentiate $c_f(\alpha_f(t)) = $ the image of $c_o(\alpha_o(t))$ under the relative pose. The velocity of the contact point over the finger is the velocity of the object's material point at the contact plus the velocity of the contact point over the object. In the tangent axes this gives $b = a + (v_x, v_y)$, and in the normal direction it gives $v_z = 0$.
2. **The normals stay opposite.** Differentiate $n_f = -n_o$. As the contact moves by $a$, the finger normal turns by $K_f a$ (the Weingarten map of the surface in the chart), and as it moves by $b$ over the object, the object normal turns by $\tilde K_o b$ in the finger axes. The difference of the two turns is the tangential part of the relative rotation, which turns a normal by $(-\omega_y, \omega_x)$. This gives $K_f a + \tilde K_o b = (-\omega_y, \omega_x)$.
3. **The angle of contact.** Differentiate the relation between $x_f$ and $x_o$. Moving along a surface turns its Gauss frame about the normal by the torsion form, so the angle grows by the relative spin plus these two turns: $\dot\psi = \omega_z + T_f a + T_o M_o \dot\alpha_o$.

Solve steps 1 and 2. Put $b = a + v$ into step 2: $(K_f + \tilde K_o) a = (-\omega_y, \omega_x) - \tilde K_o v$. The relative curvature form is invertible, so $a = (K_f + \tilde K_o)^{-1}((-\omega_y, \omega_x) - \tilde K_o v)$, and $\dot\alpha_f = M_f^{-1} a$. Then $b = a + v = (K_f + \tilde K_o)^{-1}((-\omega_y, \omega_x) + K_f v)$, and since $R_\psi^{-1} = R_\psi$, $\dot\alpha_o = M_o^{-1} R_\psi b$. These are the stated equations. The rolling case is the substitution $v = 0$, $\omega_z = 0$. $\square$

## Consequences

- **A ball on a plane.** The finger is the plane $c_f(u, v) = (u, v, 0)$, so $M_f = I$, $K_f = 0$, $T_f = 0$. The object is a sphere of radius $\rho$ with the orthogonal chart by latitude $u$ and longitude $v$ of Murray, Li and Sastry's Example 5.7, for which they give $M_o = \operatorname{diag}(\rho, \rho \cos u)$, $K_o = \operatorname{diag}(1/\rho, 1/\rho)$ and $T_o = [0,\ -(1/\rho) \tan u]$. Since $R_\psi^2 = I$, $\tilde K_o = I / \rho$ and $(K_f + \tilde K_o)^{-1} = \rho I$. In rolling, $\dot\alpha_f = \rho\, (-\omega_y, \omega_x)$: the contact moves over the plane at speed $\rho$ times the rolling rate, as expected for a wheel. The chart is singular at the poles $u = \pm \pi/2$, where $M_o$ is not invertible, so near a pole a second chart is needed.
- **Rolling is nonholonomic.** The rolling equations constrain the velocities, not the positions, of the five contact coordinates. Li and Canny (1990) study them as a [nonholonomic](/nonholonomic-constraint/) system and use Chow's theorem to decide which contact configurations can be reached. For a sphere on a plane every contact configuration can be reached by rolling alone (a theorem), and Li and Canny give an algorithm that finds such a rolling path when one of the bodies is flat.
- **Dexterous manipulation.** A finger that rolls on an object changes the contact point without breaking contact. The equations give the change of the [grasp map](/grasp-matrix/) during rolling, and so they are the kinematic layer of [in-hand manipulation](/in-hand-manipulation/) with rolling fingers.
- **Tactile sensing.** Montana (1988) also used the equations the other way: from the motion of a sensed contact point on a known finger, a robot can estimate the curvature of an unknown object.

## Tightness

- **Nondegenerate contact.** If $K_f + \tilde K_o$ is singular the theorem says nothing. Two planes, or two cylinders with parallel axes, touch along a set that is not a single point, and the contact point is not defined by the motion. A ball inside a hollow sphere of the same radius is another degenerate case.
- **Smooth surfaces.** The curvature form needs second derivatives. At an edge or a vertex of a polyhedron, the normal jumps and the equations do not apply; polyhedral contact is handled with contact modes and [complementarity](/rigid-contact-complementarity/) instead.
- **Charts.** The forms depend on the chart, and an orthogonal chart may not cover the whole surface; the sphere chart above fails at the poles. The contact coordinates are local coordinates, and a global analysis must change charts.
- **Kinematics only.** The equations say nothing about forces. Whether a finger can roll without slipping depends on the friction cone at the contact, which is a separate condition.

## History

Montana (1988) derived the equations, with the aim of using them for grasping with rolling fingers and for tactile sensing. Murray, Li and Sastry (1994) gave the form used here, with the rolling case as a corollary, in their textbook on manipulation. Li and Canny (1990) used the rolling equations to study motion planning with the rolling constraint as a nonholonomic problem.

## References
