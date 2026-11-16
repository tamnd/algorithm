---
tag: 3A64S7
kind: definition
slug: kinematic-redundancy
name: Kinematic redundancy
aliases:
- redundant manipulator
area: robotics/robot-kinematics
level: core
summary: A robot has more joint freedoms than its task needs, so a set of joint motions leaves the task unchanged.
prereqs: [geometric-jacobian, configuration-space]
see_also: [null-space-projection, jacobian-pseudoinverse-method, kinematic-singularity, task-priority-inverse-kinematics, inverse-kinematics, pseudoinverse, yoshikawa-manipulability-measure, whole-body-control]
sources:
  - book: isbn:9781846286414
    title: "Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics: Modelling, Planning and Control, Springer, 2009"
    locator: Chapter 3, Section 3.4 (analysis of redundancy, the range and null spaces of the Jacobian) and Section 3.5 (inverse differential kinematics of redundant manipulators)
  - book: isbn:9780201151985
    title: "Yoshihiko Nakamura, Advanced Robotics: Redundancy and Optimization, Addison-Wesley, 1991"
    locator: the chapter on differential kinematics and redundancy (the pseudoinverse solution, the null space term and redundancy as an optimization problem)
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics: Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: Chapter 6, Section 6.3 (inverse velocity kinematics, the pseudoinverse for a redundant arm)
---

A robot is kinematically redundant for a task when it has more joints than the task has coordinates: $n > m$, where $n$ is the number of joints and $m$ the dimension of the task, for example 6 for a full pose of the hand.
The spare freedom shows up as joint motions that leave the task unchanged, the self-motions, which a controller can use for a second goal such as keeping away from joint limits, obstacles or [singularities](/kinematic-singularity/).
Redundancy is a relation between an arm and a task: a 6-joint arm is not redundant for placing a hand in 6 dimensions, but it is redundant for pointing a drill, where the turn about the drill axis does not matter.
It is a different thing from having several separate [inverse kinematics](/inverse-kinematics/) solutions, which also happens without redundancy.

## Definition

Let the task be given by a smooth map $x = f(q)$ from the joint values $q \in \mathbb{R}^n$ to the task coordinates $x \in \mathbb{R}^m$, with the $m \times n$ Jacobian $J(q) = \partial f / \partial q$ (or a [geometric Jacobian](/geometric-jacobian/) when the task includes an orientation).

**Definition.** The robot is kinematically redundant for the task if $n > m$.
The number $n - m$ is the degree of redundancy.

At a configuration where $J$ has full row rank $m$, the joint velocity space splits into two orthogonal parts,

$$\mathbb{R}^n = \operatorname{range}(J^{\mathsf T}) \oplus \operatorname{null}(J), \qquad \dim \operatorname{null}(J) = n - m.$$

A joint velocity in $\operatorname{null}(J)$ is a self-motion: $\dot x = J\dot q = 0$, so the task does not change to first order.
The set of all configurations that give the same task value, $f^{-1}(x)$, is the self-motion set.
By the regular value theorem, near a configuration where $J$ has rank $m$ this set is a smooth manifold of dimension $n - m$ in the [configuration space](/configuration-space/), and its tangent space at $q$ is $\operatorname{null}(J(q))$.

Every joint velocity that gives the task velocity $\dot x$ has the form

$$\dot q = J^{+}\dot x + (I - J^{+}J)\,z, \qquad z \in \mathbb{R}^n,$$

where $J^{+} = J^{\mathsf T}(J J^{\mathsf T})^{-1}$ is the [pseudoinverse](/pseudoinverse/).
The first term is the solution of least norm, and the second term is the [null space projection](/null-space-projection/) of an arbitrary vector $z$, which is where a second goal enters.

**Two sources of redundancy.** Intrinsic redundancy comes from the arm: a spatial arm with $n > 6$ joints is redundant for every pose task.
Functional, or task, redundancy comes from the task: a 6-joint arm that only has to place a point and an axis (welding, drilling, spray painting with a round nozzle) has $m = 5$ and one degree of redundancy.

## Examples and non-examples

**The planar 3R arm.** Three revolute joints with unit links in the plane, used to place the tip at a point: $n = 3$, $m = 2$, one degree of redundancy.
At $q = (0, \pi/2, -\pi/2)$ the tip is at $(2, 1)$ m and

$$J = \begin{pmatrix} -1 & -1 & 0 \\ 2 & 1 & 1 \end{pmatrix}, \qquad \operatorname{null}(J) = \operatorname{span}\{(1, -1, -1)\}.$$

Turning joint 1 forward while joints 2 and 3 turn back by the same rate keeps the tip still to first order; following this direction, and correcting for curvature, traces a closed curve of configurations that all put the tip at $(2, 1)$.

**A 7-joint arm.** An arm with a 3-joint shoulder, an elbow and a 3-joint wrist, used for a full 6-dimensional pose of the hand, has one degree of redundancy.
The self-motion swings the elbow on a circle about the line from the shoulder to the wrist while the hand stays fixed.
Such arms are built for this extra freedom.

**A mobile manipulator.** A 6-joint arm on a wheeled base with 3 planar freedoms has $n = 9$ for a 6-dimensional hand task, so 3 degrees of redundancy.

**Non-example: a 6R arm and a full pose.** $n = m = 6$; there is no self-motion at a nonsingular configuration, although there can be up to 16 separate solutions.
Several solutions are not redundancy.

**Non-example: the planar 3R arm with orientation.** If the task also fixes the angle of the last link, $m = 3 = n$, and the arm is no longer redundant.

**Non-example: a singularity.** At a singular configuration of a 6R arm, $J$ has a null space, and some joint motions leave the pose unchanged to first order, but the arm is not redundant; the null space exists only on a thin set of configurations, and it does not lead to a manifold of solutions of dimension $n - m$.
A redundant arm can also be singular, when the rank of $J$ drops below $m$; then the null space is larger than $n - m$.

## Related definitions

- [Null space projection](/null-space-projection/): the technique that uses the self-motions for a second goal.
- [Jacobian pseudoinverse method](/jacobian-pseudoinverse-method/): inverse kinematics that picks the joint step of least norm.
- [Task priority inverse kinematics](/task-priority-inverse-kinematics/): several tasks ranked by priority, each in the null space of the ones above it.
- [Kinematic singularity](/kinematic-singularity/): a loss of rank of $J$; redundancy is a surplus of columns.
- [Pseudoinverse](/pseudoinverse/): the matrix $J^{+}$ in the general solution.
- [Whole-body control](/whole-body-control/): the control of robots with many redundant joints, such as humanoids.

## References
