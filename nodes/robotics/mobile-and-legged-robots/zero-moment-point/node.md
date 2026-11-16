---
tag: YGVAT6
kind: definition
slug: zero-moment-point
name: Zero moment point
aliases:
- ZMP
area: robotics/mobile-and-legged-robots
level: core
summary: "The ground point where the horizontal moment of the ground reaction is zero; on flat ground it equals the center of pressure, but only while it lies inside the support polygon."
prereqs: []
see_also: [center-of-pressure, support-polygon, linear-inverted-pendulum-model, zmp-preview-control, capture-point, contact-wrench-cone, centroidal-dynamics, newton-euler-equations]
sources:
  - paper: doi:10.1016/0025-5564(72)90061-2
    title: Miomir Vukobratović and Yu. Stepanenko, On the stability of anthropomorphic systems, Mathematical Biosciences 15(1-2), 1972
    locator: pages 1 to 37
  - paper: doi:10.1142/S0219843604000083
    title: Miomir Vukobratović and Branislav Borovac, Zero-moment point, thirty five years of its life, International Journal of Humanoid Robotics 1(1), 2004
    locator: pages 157 to 173
  - paper: doi:10.1109/TSMCA.2004.832811
    title: Philippe Sardain and Guy Bessonnet, Forces acting on a biped robot. Center of pressure-zero moment point, IEEE Transactions on Systems, Man, and Cybernetics, Part A 34(5), 2004
    locator: pages 630 to 637
  - book: isbn:9783642545351
    title: Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada and Kazuhito Yokoi, Introduction to Humanoid Robotics, Springer Tracts in Advanced Robotics 101, Springer, 2014
    locator: Chapter 3 (ZMP and dynamics)
---

The zero moment point (ZMP) is the point on the ground about which the ground reaction on a legged robot has no horizontal moment. It can be computed in two ways: from the contact forces, where it is the [center of pressure](/center-of-pressure/), or from the motion of the robot, where it follows from the rate of change of the momentum. The two agree while the feet stay flat on the ground. Walking pattern generators for humanoid robots plan the motion so that the computed ZMP stays inside the [support polygon](/support-polygon/); then the stance foot does not tip over its edge.

## Definition

Let the ground be the plane $z = p_z$ (often $p_z = 0$), with gravity $g = 9.81$ along $-z$. Let the robot have mass $M$, CoM $c = (x, y, z)$, linear momentum $P$ and angular momentum $L$ about the origin. Newton and Euler give the total ground reaction force $f$ and its moment $\tau$ about the origin:

$$f = \dot P + M g e_z, \qquad \tau = \dot L + c \times M g e_z.$$

The **zero moment point** is the point $p = (p_x, p_y, p_z)$ on the ground such that the moment of the ground reaction about $p$ has zero horizontal components, $\tau - p \times f = (0, 0, \tau_n)$. Solving the two horizontal equations gives

$$p_x = \frac{M g x + p_z \dot P_x - \dot L_y}{M g + \dot P_z}, \qquad p_y = \frac{M g y + p_z \dot P_y + \dot L_x}{M g + \dot P_z},$$

defined when $M g + \dot P_z > 0$, which means that the ground pushes up. For a single point mass, $P = M \dot c$ and $L = c \times M \dot c$, and the formula becomes

$$p_x = x - \frac{(z - p_z)\, \ddot x}{g + \ddot z}, \qquad p_y = y - \frac{(z - p_z)\, \ddot y}{g + \ddot z}.$$

These are the formulas of the computed ZMP. They use only the motion, so they give a point for any motion, possible or not.

**Proposition (ZMP and CoP).** On flat ground, if the motion is produced by contact forces that push ($f_{iz} \ge 0$), then the computed ZMP equals the center of pressure of those forces, so it lies in the support polygon.

*Proof.* The contact forces are the only external forces besides gravity, so their resultant is $f$ and their moment about the origin is $\tau$. The center of pressure is, by its definition, the ground point about which the contact forces have zero horizontal moment. That point is unique when $f_z > 0$, because the two horizontal equations are linear in $(p_x, p_y)$ with the coefficient $f_z$. So it equals the computed ZMP, and the theorem on the center of pressure puts it in the support polygon. $\square$

So the claim "the ZMP equals the CoP on flat ground" holds while the ZMP is inside the support polygon. If a planned motion gives a computed point outside the polygon, no pushing contact forces can produce that motion with the foot flat. The foot rotates about its edge, the real CoP stays on that edge, and the computed point has no contact meaning. Vukobratović and Borovac call it the fictitious ZMP; Sardain and Bessonnet (2004) discuss the same distinction.

The **ZMP criterion** for a robot that walks with flat feet: the computed ZMP must stay strictly inside the support polygon at all times. It is a condition that the foot does not tip, together with friction conditions so that it does not slide. It does not say that the robot will not fall later.

## Examples and non-examples

**A robot that speeds up.** A robot with its CoM at constant height $z = 0.8$ m above the ground, at $x = 0$, accelerates forward with $\ddot x = 1$ m/s². The point mass formula gives $p_x = -0.8 \cdot 1 / 9.81 = -0.0815$ m. The ZMP is 8.15 cm behind the CoM: to push the body forward, the ground must push at a point behind it.

**The limit of a foot.** If the CoM is above the ankle at $x = 0$ and the heel is at $x = -0.05$ m, the ZMP stays in the sole only for $\ddot x \le 0.05 \cdot 9.81 / 0.8 \approx 0.613$ m/s². A planner that asks for $1$ m/s² from this stance makes the computed ZMP leave the sole, and the foot rolls back onto its heel.

**Standing still.** With no motion, $\dot P = 0$ and $\dot L = 0$, and the formula gives $p = (x, y)$: the ZMP is the projection of the CoM. The ZMP criterion becomes the static condition of the [support polygon](/support-polygon/).

**Non-example: the ZMP inside but the robot falls.** A robot can have its ZMP in the middle of the foot at every instant and still fall, for example when the CoM moves away fast and the next step comes too late. The ZMP criterion is a condition at one instant. The [capture point](/capture-point/) adds the question of where the robot must step.

**Non-example: uneven ground.** With one foot on a stair, or with a hand on a wall, there is no single ground plane, and the ZMP of one plane does not describe the contacts. The [contact wrench cone](/contact-wrench-cone/) gives the general condition.

## Related definitions

- [Center of pressure](/center-of-pressure/): the same point computed from the contact forces; it always lies in the support polygon when the contacts push.
- [Support polygon](/support-polygon/): the region that the ZMP must stay in.
- [Linear inverted pendulum model](/linear-inverted-pendulum-model/): the point mass at constant height, where the formula becomes $p = x - \ddot x / \omega^2$ with $\omega^2 = g / (z - p_z)$.
- [ZMP preview control](/zmp-preview-control/): plans a CoM motion so that the ZMP follows a reference inside the feet.
- [Centroidal dynamics](/centroidal-dynamics/): the equations for $\dot P$ and $\dot L$ that the formula uses.
- [Contact wrench cone](/contact-wrench-cone/): the condition that replaces the ZMP criterion on uneven ground.

## References
