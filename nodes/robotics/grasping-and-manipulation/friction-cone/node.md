---
tag: S7CVZ1
kind: definition
slug: friction-cone
name: Friction cone
aliases:
- Coulomb friction cone
area: robotics/grasping-and-manipulation
level: intro
summary: "The set of contact forces that a contact with Coulomb friction can apply: the tangential part is at most mu times the normal part, a circular cone about the normal."
prereqs: []
see_also: [polyhedral-friction-cone, grasp-contact-models, force-closure, antipodal-grasp, contact-wrench-cone, limit-surface, rigid-contact-complementarity, second-order-cone-programming]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12, Section 12.2.1 (Friction), with the friction cone in the plane and in space and its polyhedral approximation
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 6 (Friction), Coulomb's law and the friction cone; Chapter 5 for the contact wrench cones built from it
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (the contact models and their friction cones)
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.1 (contact models, Table 38.2) and Section 38.4.2 (friction cones and their linearization); the chapter is pages 955 to 988"
---

A friction cone is the set of forces that one contact between two rigid bodies can transmit under Coulomb's law of friction. The contact can push but not pull, and it can push sideways as long as the sideways part is at most a fixed multiple $\mu$ of the pushing part. In three dimensions these forces fill a circular cone about the contact normal, with half-angle $\arctan \mu$. The friction cone is the basic object behind [grasp contact models](/grasp-contact-models/), [force closure](/force-closure/), contact simulation and the stability of legged robots.

## Definition

Let a body touch another body at a point $p$, and let $n$ be the unit normal of the contact at $p$, pointing into the body that receives the force. Write a contact force $f \in \mathbb{R}^3$ as a normal part and a tangential part:

$$f_n = n^T f, \qquad f_t = f - f_n n.$$

Let $\mu \ge 0$ be the coefficient of static friction of the two surfaces. The **friction cone** at the contact is

$$FC = \{\, f \in \mathbb{R}^3 : \lVert f_t \rVert \le \mu f_n \,\}.$$

In a contact frame with the $z$ axis along $n$, this is $\sqrt{f_x^2 + f_y^2} \le \mu f_z$. The condition implies $f_n \ge 0$: the contact can push and cannot pull. The half-angle of the cone is $\alpha = \arctan \mu$, the angle between $n$ and each force on its boundary.

In the plane, a contact force has one tangential component, and the cone is the set of nonnegative combinations of its two edges:

$$FC = \{\, a (n + \mu t) + b (n - \mu t) : a, b \ge 0 \,\},$$

where $t$ is a unit tangent. In space the cone has no edges; it is the second-order (Lorentz) cone $\{(x, s) : \lVert x \rVert \le s\}$ after the tangential part is scaled by $1/\mu$.

The cone describes the forces at a contact that does not slide. While the contact slides, Coulomb's law puts the force on the boundary of the cone, with the tangential part opposite to the sliding velocity. Under the rigid body model the two cases combine into a complementarity condition, as in [rigid contact complementarity](/rigid-contact-complementarity/).

Properties that follow from the definition:

- $FC$ is a closed convex cone: if $f$ and $g$ are in it, so is $a f + b g$ for $a, b \ge 0$. Convexity follows from the triangle inequality, $\lVert f_t + g_t \rVert \le \mu (f_n + g_n)$.
- $FC$ is pointed: it contains no line, because $f$ and $-f$ are both in it only if $f = 0$.
- $FC$ grows with $\mu$. For $\mu = 0$ it is the ray $\{a n : a \ge 0\}$, which is a frictionless contact.
- A force $f$ applied at $p$ gives the wrench $(p \times f, f)$ about the reference point (moment first). The image of $FC$ under this linear map is the cone of contact wrenches, which is the building block of the [contact wrench cone](/contact-wrench-cone/) of a foot and of the [grasp wrench space](/grasp-wrench-space/).

## Examples and non-examples

**A force inside and a force outside.** Let $\mu = 0.5$, so $\alpha = \arctan 0.5 \approx 26.57$ degrees. In contact coordinates $(f_t, f_n)$, the force $(1, 3)$ has $1 \le 0.5 \cdot 3 = 1.5$, so it is in the cone and the contact sticks. The force $(2, 3)$ has $2 > 1.5$, so it is outside the cone: the contact cannot transmit it, and the bodies slide.

**A block on a ramp.** A block rests on a ramp that is tilted by the angle $\theta$. Gravity pulls it straight down, and the ramp must supply the opposite force, which makes the angle $\theta$ with the normal of the ramp. That force is in the friction cone exactly when $\theta \le \alpha$, that is when $\tan \theta \le \mu$. With $\mu = 0.5$ the block stays at rest up to $\theta \approx 26.57$ degrees and slides above it. This is the classic way to measure $\mu$.

**Two fingers squeezing a box.** Two fingers press on opposite sides of a box, at points on one line along the normals. Each finger force can point along that line, which is the axis of each cone, so any squeeze gives an internal force inside both cones. If the line through the contacts tilts by the angle $\beta$ from the normals, the squeeze stays inside the cones only when $\tan \beta < \mu$. This is the [antipodal grasp](/antipodal-grasp/) condition.

**Non-example: a pull.** A force with $f_n < 0$ is never in the cone. A suction cup or a magnet can pull, but then the contact is not a Coulomb contact, and a different model is needed.

**Non-example: a twist about the normal.** A point contact transmits no moment. A finger pad that touches over a small area can resist some twist about $n$; this is the soft finger model of [grasp contact models](/grasp-contact-models/), and the twist limit is a separate condition next to the friction cone.

**Non-example: the pyramid.** A [polyhedral friction cone](/polyhedral-friction-cone/) with $k$ edges is an approximation of $FC$ for linear programs. With the edges on the cone it is strictly smaller than $FC$ in space; with $k = 4$ it keeps only $\cos(\pi/4) \approx 0.7071$ of the tangential capacity in the worst direction.

## Related definitions

- [Polyhedral friction cone](/polyhedral-friction-cone/): the linearized cone with $k$ edges, used by linear programs such as the [force-closure test](/force-closure-test/).
- [Grasp contact models](/grasp-contact-models/): the frictionless point contact, the point contact with friction (whose force set is exactly $FC$) and the soft finger.
- [Force closure](/force-closure/): a grasp whose friction cones together can resist every external wrench.
- [Contact wrench cone](/contact-wrench-cone/): the wrenches that a foot or a flat contact can apply, built from friction cones at the corners.
- [Limit surface](/limit-surface/): the friction law for a planar sliding patch, where the friction force and the friction moment are coupled.
- [Second-order cone programming](/second-order-cone-programming/): the class of convex programs that handles circular friction cones without linearization.
- [Rigid contact complementarity](/rigid-contact-complementarity/): the contact model that combines the cone with the sticking and sliding cases.

## References
