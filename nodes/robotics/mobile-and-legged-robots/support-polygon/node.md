---
tag: PK9YWK
kind: definition
slug: support-polygon
name: Support polygon
aliases:
- support region
area: robotics/mobile-and-legged-robots
level: intro
summary: "The convex hull of the ground contact points of a legged robot on flat ground; a robot at rest can balance only if its center of mass projects into this polygon."
prereqs: []
see_also: [center-of-pressure, zero-moment-point, contact-wrench-cone, convex-hull, capture-point, footstep-planning, friction-cone, point-in-convex-polygon]
sources:
  - paper: doi:10.1016/0025-5564(68)90090-4
    title: R. B. McGhee and A. A. Frank, On the stability properties of quadruped creeping gaits, Mathematical Biosciences 3, 1968
    locator: pages 331 to 351
  - paper: doi:10.1109/TRO.2008.2001360
    title: Timothy Bretl and Sanjay Lall, Testing static equilibrium for legged robots, IEEE Transactions on Robotics 24(4), 2008
    locator: pages 794 to 807
  - book: isbn:9783642545351
    title: Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada and Kazuhito Yokoi, Introduction to Humanoid Robotics, Springer Tracts in Advanced Robotics 101, Springer, 2014
    locator: Chapter 3 (ZMP and dynamics)
---

The support polygon of a legged robot is the convex hull of the points where it touches the ground, seen from above. On flat ground, a robot that does not move can stand still exactly when the vertical projection of its center of mass (CoM) lies in this polygon. The polygon is the basic test of static balance, and it is also the region that must contain the [center of pressure](/center-of-pressure/) and the [zero moment point](/zero-moment-point/) when the robot moves.

## Definition

Let the ground be the horizontal plane $z = 0$, with gravity $g = 9.81$ along $-z$. Let the robot touch the ground at the points $p_1, \dots, p_n$, with $p_i = (x_i, y_i, 0)$. For a foot with a flat sole, these are the corners of the sole; for a point foot, the foot point. The **support polygon** is

$$S = \operatorname{conv}\{(x_1, y_1), \dots, (x_n, y_n)\} \subset \mathbb{R}^2,$$

the [convex hull](/convex-hull/) of the contact points in the plane. It contains the ground between two feet, where there is no contact.

The contacts are unilateral: the force $f_i = (f_{ix}, f_{iy}, f_{iz})$ at $p_i$ has $f_{iz} \ge 0$, so the ground pushes and never pulls. The friction law can be any law, for example a [friction cone](/friction-cone/).

**Theorem (static balance on flat ground).** Let a robot of mass $m$ with CoM $c = (c_x, c_y, c_z)$ have zero linear and angular momentum and stay at rest. Contact forces $f_i$ with $f_{iz} \ge 0$ that hold the robot in equilibrium exist if and only if $(c_x, c_y) \in S$. If such forces exist, purely vertical ones also do, so the friction coefficient does not matter.

*Proof.* Equilibrium means that the total force and the total moment about the origin are zero:

$$\sum_i f_i + (0, 0, -m g) = 0, \qquad \sum_i p_i \times f_i + c \times (0, 0, -m g) = 0.$$

Since $p_i$ has zero height, the $x$ and $y$ parts of $p_i \times f_i$ are $y_i f_{iz}$ and $-x_i f_{iz}$; the tangential forces do not enter them. The $x$ and $y$ parts of $c \times (0, 0, -m g)$ are $-m g c_y$ and $m g c_x$. So the force and moment equations give

$$\sum_i f_{iz} = m g, \qquad \sum_i f_{iz} x_i = m g c_x, \qquad \sum_i f_{iz} y_i = m g c_y.$$

With $\lambda_i = f_{iz} / (m g) \ge 0$ and $\sum_i \lambda_i = 1$, this says that $(c_x, c_y) = \sum_i \lambda_i (x_i, y_i)$ is a convex combination of the contact points, so it lies in $S$. Conversely, if $(c_x, c_y) \in S$, write it as such a convex combination and set $f_i = (0, 0, m g \lambda_i)$. These forces satisfy all six equations, because vertical forces give no moment about the vertical axis. $\square$

The proof uses three facts: the ground is one plane, the contacts can only push, and the robot is at rest. Each is needed, as the non-examples below show.

The **static stability margin** of McGhee and Frank (1968) is the distance from the CoM projection to the nearest edge of $S$, taken as negative outside $S$. A gait is statically stable when the margin stays positive at all times.

## Examples and non-examples

**A quadruped on four feet.** Let the feet be at $(\pm 0.2, \pm 0.12)$ m. The support polygon is the rectangle $[-0.2, 0.2] \times [-0.12, 0.12]$. With the CoM projection at $(0.03, 0.03)$, the distances to the four edges are $0.17$, $0.23$, $0.09$ and $0.15$, so the static stability margin is $0.09$ m. Four contacts give three equations for four normal forces, so the force distribution is not unique.

**The same robot on three feet.** Lift the rear right foot at $(-0.2, -0.12)$. The support polygon is now the triangle with corners $A = (0.2, 0.12)$, $B = (0.2, -0.12)$ and $C = (-0.2, 0.12)$. Its long edge $BC$ is the diagonal $0.24 x + 0.4 y = 0$, which goes through the center of the body. A CoM at the origin is on that edge, with margin $0$, so the robot must shift its body before it lifts the foot. This is why a statically stable walk moves the body toward the three stance feet before each step. With the CoM at $(0.03, 0.03)$, the distance to $BC$ is $(0.24 \cdot 0.03 + 0.4 \cdot 0.03) / \sqrt{0.24^2 + 0.4^2} = 0.0192 / 0.46648 \approx 0.0412$ m, and the other two edges are farther, so the margin is $0.0412$ m. With three contacts that are not on one line, the forces are unique: the convex weights are $\lambda_A = 0.2$, $\lambda_B = 0.375$ and $\lambda_C = 0.425$, and with $m = 10$ kg the normal forces are $19.62$, $36.79$ and $41.69$ N.

**A biped.** In single support, $S$ is the outline of the sole of the stance foot. In double support, it is the convex hull of both soles, a hexagon or a quadrilateral that includes the ground between the feet.

**Non-example: point feet on a line.** A biped with point feet has a segment as its support polygon in double support and a single point in single support. The CoM projection can be on the segment, but a small push moves it off, so such a robot cannot stand still in a robust way. It must balance by motion, as the walkers of [hybrid zero dynamics](/hybrid-zero-dynamics/) do.

**Non-example: uneven ground or hands on a wall.** If the contacts are not in one horizontal plane, the tangential forces enter the moment equations, and the set of CoM positions that allow balance depends on the friction coefficients. It is a projection of a polyhedron, not the convex hull of the contacts. Bretl and Lall (2008) give an algorithm that computes this region. The general condition uses the [contact wrench cone](/contact-wrench-cone/).

**Non-example: a robot in motion.** A running or walking robot can have its CoM projection outside the support polygon for some time, because the momentum changes. The polygon then bounds the center of pressure, not the CoM. The [zero moment point](/zero-moment-point/) and the [capture point](/capture-point/) are the conditions for this case.

## Related definitions

- [Center of pressure](/center-of-pressure/): the point where the resultant normal force acts; it is in the support polygon for unilateral contacts on flat ground.
- [Zero moment point](/zero-moment-point/): the dynamic counterpart of the CoM projection, which must stay in the support polygon while the feet stay flat.
- [Contact wrench cone](/contact-wrench-cone/): the set of wrenches that the contacts can apply, which replaces the polygon on uneven ground.
- [Capture point](/capture-point/): the point where the robot must put its support polygon to come to rest.
- [Footstep planning](/footstep-planning/): chooses the feet positions, and so the sequence of support polygons.
- [Convex hull](/convex-hull/) and [point in convex polygon](/point-in-convex-polygon/): the geometric operations that build the polygon and test the CoM against it.

## References
