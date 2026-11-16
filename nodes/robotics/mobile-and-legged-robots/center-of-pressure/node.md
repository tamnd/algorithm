---
tag: G5QRQ3
kind: definition
slug: center-of-pressure
name: Center of pressure
aliases:
- CoP
area: robotics/mobile-and-legged-robots
level: core
summary: "The point on the ground where the resultant of the normal contact forces acts; it lies in the support polygon when the contacts can only push and the ground is flat."
prereqs: []
see_also: [support-polygon, zero-moment-point, contact-wrench-cone, linear-inverted-pendulum-model, capture-point, wrench, friction-cone, centroidal-dynamics]
sources:
  - paper: doi:10.1109/TSMCA.2004.832811
    title: Philippe Sardain and Guy Bessonnet, Forces acting on a biped robot. Center of pressure-zero moment point, IEEE Transactions on Systems, Man, and Cybernetics, Part A 34(5), 2004
    locator: pages 630 to 637
  - book: isbn:9783642545351
    title: Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada and Kazuhito Yokoi, Introduction to Humanoid Robotics, Springer Tracts in Advanced Robotics 101, Springer, 2014
    locator: Chapter 3 (ZMP and dynamics), with the ZMP measured by force sensors in the feet
  - paper: doi:10.1142/S0219843604000083
    title: Miomir Vukobratović and Branislav Borovac, Zero-moment point, thirty five years of its life, International Journal of Humanoid Robotics 1(1), 2004
    locator: pages 157 to 173
---

The center of pressure (CoP) of a contact is the point on the ground where the resultant of the normal contact forces acts. A foot on the floor feels a pressure that is spread over its sole; the CoP is the weighted mean of the points of the sole, with the pressure as the weight. Force sensors in the feet of a walking robot measure it, and balance controllers for legged robots use it as the point that they can move inside the [support polygon](/support-polygon/).

## Definition

Let the ground be the plane $z = 0$. Let the contact between a robot and the ground apply a normal pressure $\sigma(x, y) \ge 0$ over a contact region $D$, and point forces $f_{iz} \ge 0$ at points $(x_i, y_i)$ if there are point contacts. The **center of pressure** is

$$p = \frac{\int_D \sigma(x, y)\, (x, y)\, dA + \sum_i f_{iz} (x_i, y_i)}{\int_D \sigma\, dA + \sum_i f_{iz}},$$

defined when the total normal force $f_z$ in the denominator is positive. The tangential forces have no part in it.

An equivalent form uses moments. Put the resultant force $f$ of the contact at $p$. The moment of all contact forces about $p$ then has no horizontal part:

$$\tau_x(p) = \tau_y(p) = 0.$$

Only a moment $\tau_z$ about the vertical axis can remain, which friction makes. So the CoP is the point about which the ground reaction gives a pure force plus a twist about the normal.

**Theorem (the CoP is in the support polygon).** If the contacts are unilateral, which means $\sigma \ge 0$ and $f_{iz} \ge 0$, and the ground is flat, then $p$ lies in the convex hull of the contact region, which is the [support polygon](/support-polygon/).

*Proof.* The weights $\sigma\, dA / f_z$ and $f_{iz} / f_z$ are nonnegative and sum to $1$, so $p$ is a convex combination (an integral one for the distributed part) of points of the contact region. A convex combination of points of a set lies in the convex hull of that set. $\square$

Both conditions are needed. With a suction cup or a gripper that grasps a rail, the contact can pull, $\sigma$ can be negative, and the CoP can leave the polygon. On ground that is not one plane, there is a CoP for each flat contact surface, but no single point of the ground has the properties above for all contacts together.

**Measurement.** A six-axis force sensor in the ankle measures the force $f = (f_x, f_y, f_z)$ and the moment $\tau = (\tau_x, \tau_y, \tau_z)$ that the ground applies through the foot, about the sensor point. If the sensor point is at height $d$ above the sole and above the origin of the foot frame, then

$$p_x = \frac{-\tau_y - d f_x}{f_z}, \qquad p_y = \frac{\tau_x - d f_y}{f_z}.$$

To see this, write $\tau = (p - s) \times f + \tau_n e_z$ with $s = (0, 0, d)$ and $p = (p_x, p_y, 0)$. The $x$ part is $p_y f_z + d f_y$ and the $y$ part is $-d f_x - p_x f_z$. For two feet with CoPs $p_R$ and $p_L$ and normal forces $f_{Rz}$ and $f_{Lz}$, the CoP of both is $(f_{Rz} p_R + f_{Lz} p_L) / (f_{Rz} + f_{Lz})$.

## Examples and non-examples

**A sensor reading.** A sensor at $d = 0.04$ m above the sole reads $f = (10, -5, 400)$ N and $\tau = (6, -20, 1)$ N m. Then $p_x = (20 - 0.4) / 400 = 0.049$ m and $p_y = (6 + 0.2) / 400 = 0.0155$ m. The CoP is 4.9 cm in front of and 1.55 cm to the left of the point below the sensor.

**Two feet.** The right foot has its CoP at $(0, -0.1)$ with $300$ N, and the left foot at $(0.3, 0.1)$ with $100$ N. The total CoP is $((0 \cdot 300 + 0.3 \cdot 100) / 400, (-0.1 \cdot 300 + 0.1 \cdot 100) / 400) = (0.075, -0.05)$. It is on the segment between the two foot CoPs, nearer the foot that carries more load.

**A foot that starts to tip.** When a robot leans forward, its CoP moves toward the toes. When the CoP reaches the front edge of the sole, all the pressure is on that edge, and the CoP cannot move farther. If the robot needs a CoP beyond the edge, the foot rotates about the edge. This limit is the basis of the [zero moment point](/zero-moment-point/) condition for walking.

**Non-example: a pull.** A robot hand that holds a bar above the robot can pull. If such a contact is counted in the formula, a weight can be negative, and the resulting point can be outside the convex hull of the contacts. It is then not a center of pressure in the sense above.

**Non-example: a slope and a step.** One foot is on the floor and one is on a stair. Each foot has its own CoP on its own plane. A weighted mean of the two is a point in space with no physical meaning, and the theorem does not apply. The [contact wrench cone](/contact-wrench-cone/) is the tool for this case.

## Related definitions

- [Support polygon](/support-polygon/): the convex hull of the contacts, which contains the CoP for unilateral contacts on flat ground.
- [Zero moment point](/zero-moment-point/): a point computed from the motion of the robot; it equals the CoP while it is inside the support polygon (Sardain and Bessonnet, 2004).
- [Contact wrench cone](/contact-wrench-cone/): the wrenches that a flat foot can apply; the condition that the CoP stays in the sole is part of it.
- [Linear inverted pendulum model](/linear-inverted-pendulum-model/): a model whose input is the CoP, which moves the CoM.
- [Wrench](/wrench/): the force and moment pair whose moment part vanishes horizontally at the CoP.

## References
