---
tag: HET1XR
kind: concept
slug: spatial-vector-algebra
name: Spatial vector algebra
aliases:
- spatial notation
- Featherstone spatial vectors
area: robotics/robot-dynamics
level: advanced
summary: Six-dimensional motion and force vectors with their cross products, which write rigid body dynamics in a short frame-free form.
prereqs: [rigid-body-twist, wrench, adjoint-map-se3]
see_also: [spatial-inertia, recursive-newton-euler-algorithm, articulated-body-algorithm, composite-rigid-body-algorithm, newton-euler-equations, lie-bracket, screw-motion, special-euclidean-group]
sources:
  - book: isbn:9780387743141
    title: Roy Featherstone, Rigid Body Dynamics Algorithms, Springer, 2008
    locator: "Chapter 2 (spatial vector algebra: motion and force vectors, Plücker coordinates, coordinate transforms, cross products, differentiation, acceleration and the equation of motion)"
  - paper: doi:10.1109/MRA.2010.937853
    title: "Roy Featherstone, A beginner's guide to 6-D vectors (part 1), IEEE Robotics and Automation Magazine 17(3), 2010"
    locator: pages 83 to 94
  - paper: doi:10.1109/MRA.2010.939560
    title: "Roy Featherstone, A beginner's guide to 6-D vectors (part 2), IEEE Robotics and Automation Magazine 17(4), 2010"
    locator: pages 88 to 99
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 8, Section 8.2 (dynamics of a single rigid body, with the Lie bracket of twists)"
---

Spatial vector algebra describes the motion of a rigid body and the forces on it with 6-dimensional vectors. A **motion vector** holds an angular and a linear velocity, and a **force vector** holds a moment and a linear force. With two cross products, one for each kind of vector, the equations of rigid body dynamics take a short form, about one line per body, that holds in any coordinate frame. Roy Featherstone developed this notation for robot dynamics, and the [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/), the [composite rigid body algorithm](/composite-rigid-body-algorithm/) and the [articulated-body algorithm](/articulated-body-algorithm/) are written in it.

## In plain words

To describe how a solid object moves, you need two things: how fast it turns and how fast it slides. To describe a push on it, you also need two things: the twist and the straight push. The classic way keeps these as separate pairs of 3-dimensional arrows and writes separate equations for them. Spatial vector algebra puts each pair into one list of six numbers and gives rules to move such a list from one viewpoint to another, to multiply it by mass, and to take its rate of change. The equations then get much shorter, and fewer terms are forgotten. A computer program that follows a long chain of links, such as a robot arm, can use the same few lines for every link.

## The idea

**Two spaces.** Motion vectors form a 6-dimensional space $M^6$ and force vectors form its dual $F^6$. The scalar product $m \cdot f$ of a motion vector and a force vector is the power that the force does on the motion. There is no scalar product of two motion vectors that has a physical meaning and does not depend on the units and the frame.

**Plücker coordinates.** In a frame with origin $O$, the velocity of a rigid body is the motion vector $\hat v = (\omega,\ v_O)$, where $\omega$ is the angular velocity and $v_O$ is the velocity of the body point that is at $O$ at this instant. A force system is the force vector $\hat f = (n_O,\ f)$, where $f$ is the resultant force and $n_O$ is the moment about $O$. These are the [twist](/rigid-body-twist/) and the [wrench](/wrench/) in the same order as in Lynch and Park, with the angular part first.

**Transforms.** If the motion vectors of frame $A$ map to frame $B$ by the $6 \times 6$ matrix ${}^B X_A$, then force vectors map by ${}^B X_A^* = {}^B X_A^{-T}$. This keeps the power $m \cdot f$ the same in both frames. ${}^B X_A$ is the [adjoint map](/adjoint-map-se3/) $\mathrm{Ad}(T_{BA})$ of the rigid transform.

**Two cross products.** For motion vectors $v = (\omega, v_O)$ and $m = (m_\omega, m_O)$ and a force vector $f = (n, f_l)$,
$$\mathrm{crm}(v)\, m = (\omega \times m_\omega,\ v_O \times m_\omega + \omega \times m_O), \qquad \mathrm{crf}(v)\, f = (\omega \times n + v_O \times f_l,\ \omega \times f_l),$$
with $\mathrm{crf}(v) = -\mathrm{crm}(v)^T$. A motion vector $m$ that is fixed in a body that moves with the velocity $v$ changes at the rate $\mathrm{crm}(v)\, m$, and a force vector fixed in the body changes at the rate $\mathrm{crf}(v)\, f$. In Lie group terms, $\mathrm{crm}(v) = \mathrm{ad}_v$, the [Lie bracket](/lie-bracket/) of twists, and $\mathrm{crf}(v) = -\mathrm{ad}_v^T$.

**Spatial acceleration.** The spatial acceleration is the time derivative $a = \dot{\hat v}$ in a fixed frame. Its linear part is the rate of change of the velocity of whatever body point is at the fixed point $O$, not the acceleration of one body point. The classical acceleration of the body point at $O$ is $\dot v_O + \omega \times v_O$.

**The equation of motion.** With the [spatial inertia](/spatial-inertia/) $I$ of the body, the momentum is $h = I v$ and the [Newton-Euler equations](/newton-euler-equations/) become
$$f = \frac{d}{dt}(I v) = I a + \mathrm{crf}(v)\, I v .$$
The same line holds in any frame, fixed or moving, as long as $f$, $I$, $v$ and $a$ are all in it.

**Joints and chains.** A joint with one degree of freedom has a motion subspace $S$, a motion vector, and the velocity across it is $S \dot q$. The velocity of body $i$ is the velocity of its parent, transformed, plus $S_i \dot q_i$, and its acceleration is $a_i = X_i a_{\lambda(i)} + S_i \ddot q_i + \mathrm{crm}(v_i) S_i \dot q_i$. The joint force is $\tau_i = S_i^T f_i$, the power that the joint wrench does on unit joint motion.

## Examples

**Rotation about an offset axis.** A body turns at 2 rad/s about the vertical axis through the point $(1, 0, 0)$ m. In a frame at the origin, $\omega = (0, 0, 2)$ and the body point at the origin moves with $v_O = \omega \times (O - (1, 0, 0)) = (0, -2, 0)$ m/s, so $\hat v = (0, 0, 2,\ 0, -2, 0)$.

**Spatial and classical acceleration differ.** For the same steady rotation, $\hat v$ does not change in time, so the spatial acceleration is $0$. But the body point at the origin moves on a circle of radius 1 m and has the classical acceleration $\dot v_O + \omega \times v_O = (0, 0, 2) \times (0, -2, 0) = (4, 0, 0)$ m/s$^2$, toward the axis.

**A force and its power.** A force $(0, 1, 0)$ N acts at the point $(2, 0, 0)$ m. Its moment about the origin is $(2, 0, 0) \times (0, 1, 0) = (0, 0, 2)$ N m, so $\hat f = (0, 0, 2,\ 0, 1, 0)$. On the rotation above, the power is $\hat v \cdot \hat f = 2 \cdot 2 + (-2) \cdot 1 = 2$ W. As a check, the point $(2, 0, 0)$ moves with $\omega \times ((2, 0, 0) - (1, 0, 0)) = (0, 2, 0)$ m/s, and $(0, 1, 0) \cdot (0, 2, 0) = 2$ W.

**A vector crossed with itself.** $\mathrm{crm}(v)\, v = (\omega \times \omega,\ v_O \times \omega + \omega \times v_O) = 0$, so a body does not see its own velocity change because of its own motion. This is why the term $\mathrm{crm}(v_i) S_i \dot q_i$ vanishes for a joint at the base, where $v_i = S_i \dot q_i$.

## Where it is used

- **Dynamics algorithms.** The [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/), the [composite rigid body algorithm](/composite-rigid-body-algorithm/), the [articulated-body algorithm](/articulated-body-algorithm/) and the [analytical derivatives of rigid body dynamics](/rigid-body-dynamics-derivatives/) are written in spatial vectors, with one short block of code per body.
- **Inertia.** The [spatial inertia](/spatial-inertia/), the [articulated-body inertia](/articulated-body-inertia/) and the [centroidal momentum matrix](/centroidal-momentum-matrix/) are maps from motion vectors to force vectors.
- **Floating bases and contacts.** [Floating-base dynamics](/floating-base-dynamics/) treats the base as a body with a 6-dimensional joint, and contact forces enter as force vectors on the bodies.
- **Software.** Robot dynamics libraries such as Pinocchio and RBDL use spatial vectors for their algorithms.

## References
