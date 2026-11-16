---
tag: 47MX73
kind: model
slug: quasi-static-pushing
name: Quasi-static pushing
aliases:
- quasistatic pushing mechanics
area: robotics/grasping-and-manipulation
level: advanced
summary: A model of planar pushing in which inertia is negligible, so the pushed object moves as the balance of the pusher force and the support friction allows.
prereqs: [limit-surface, friction-cone, rigid-body-twist]
see_also: [mason-voting-theorem, sensorless-part-orienting, goldberg-part-orienting-algorithm, instant-center-of-velocity, rigid-contact-complementarity, nonholonomic-constraint, dubins-path, manipulation-planning]
sources:
  - paper: doi:10.1177/027836498600500303
    title: Matthew T. Mason, Mechanics and planning of manipulator pushing operations, The International Journal of Robotics Research 5(3), 53-71, 1986
    locator: the whole paper (the quasi-static analysis of pushing and the rule for the sense of rotation)
  - paper: doi:10.1177/027836499601500602
    title: Kevin M. Lynch and Matthew T. Mason, Stable pushing, mechanics, controllability, and planning, The International Journal of Robotics Research 15(6), 533-556, 1996
    locator: the whole paper (pushing with a line contact so that the object stays fixed to the pusher, and planning of such pushes)
  - paper: doi:10.1109/IROS.1992.587370
    title: Kevin M. Lynch, Hitoshi Maekawa and Kazuo Tanie, Manipulation and active sensing by pushing using tactile feedback, IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 1992
    locator: the whole paper (the motion of a pushed object in closed form with an ellipsoidal limit surface)
  - paper: doi:10.1016/0043-1648(91)90104-3
    title: Suresh Goyal, Andy Ruina and Jim Papadopoulos, Planar sliding with dry friction. Part 1. Limit surface and moment function, Wear 143(2), 307-330, 1991
    locator: the whole paper (the limit surface that relates the friction wrench to the motion)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 7, Section 7.2 (pushing)
---

Quasi-static pushing is a model of a robot that pushes an object across a table, slowly enough that the object's inertia does not matter. At each instant the force of the pusher balances the friction of the table, and the object moves in the way that this balance allows. The model predicts how the object turns and slides for a given motion of the pusher. It rests on the [limit surface](/limit-surface/), which is the set of friction wrenches of the support and is defined on its own page. [Mason's voting theorem](/mason-voting-theorem/) is one result in this model: it gives the sense of rotation without knowing the support pressure.

## The machine

The object is a rigid body on a horizontal plane, with planar pose $(x, y, \theta)$. The pusher is a rigid body with one point of contact on the object (or a line contact, for stable pushing). The input is the velocity $v_p$ of the pusher at the contact point, set by the robot. The output is the twist $\xi = (\omega, v_x, v_y)$ of the object. All vectors are written in the object frame, with the origin at the center of friction of the support, which is the center of pressure when the friction coefficient is uniform.

The parameters are:

- the friction coefficient $\mu_s$ and the pressure distribution of the support, which fix the limit surface;
- the friction coefficient $\mu_c$ between the pusher and the object;
- the contact point $r_c = (x_c, y_c)$ and the inward normal $n$ of the object at the contact.

The standing assumptions: rigid bodies, motion in the plane, Coulomb friction at the support and at the contact, and quasi-static motion, which means that the inertial forces are small against the friction forces. The model has no time scale: doubling the pusher speed doubles the object twist.

The equations are a balance and a contact law.

1. **Balance.** The pusher force $f_c$ at $r_c$ gives the wrench $w_c = (\operatorname{cross}(r_c, f_c),\ f_c)$, with $\operatorname{cross}(a, b) = a_x b_y - a_y b_x$. Quasi-statically it cancels the support friction, so while the object slides, $w_c$ is on the limit surface of the wrenches needed to keep it sliding, and $\xi$ is the outward normal of that surface at $w_c$.
2. **Contact force.** The force $f_c$ lies in the [friction cone](/friction-cone/) at the contact, with half angle $\arctan \mu_c$ about $n$.
3. **Contact velocity.** The contact point of the object moves with $v_c = (v_x - \omega y_c,\ v_y + \omega x_c)$. The normal parts agree, $v_c \cdot n = v_p \cdot n$. In the *sticking* mode $v_c = v_p$ and $f_c$ is anywhere in the cone. In the *sliding* mode the tangential parts differ, $f_c$ is on the edge of the cone, and the friction at the contact opposes the slip.

**The ellipsoid case in closed form.** With the [ellipsoid approximation](/limit-surface/) of the limit surface, with $f_{\max} = \mu_s N$, $m_{\max}$ the friction moment of a pure rotation and $c = m_{\max} / f_{\max}$, the sticking mode has the closed form of Lynch, Maekawa and Tanie (1992). With $(x, y) = r_c$ and $v_p = (v_{px}, v_{py})$:

$$v_x = \frac{(c^2 + x^2) v_{px} + x y\, v_{py}}{c^2 + x^2 + y^2}, \qquad v_y = \frac{(c^2 + y^2) v_{py} + x y\, v_{px}}{c^2 + x^2 + y^2}, \qquad \omega = \frac{x v_y - y v_x}{c^2}.$$

These come from the normal of the ellipsoid, $(v_x, v_y) \propto f_c / f_{\max}^2$ and $\omega \propto \operatorname{cross}(r_c, f_c) / m_{\max}^2$, together with $v_c = v_p$. The answer is valid if the force $f_c$, which points along $(v_x, v_y)$, is inside the friction cone at the contact. If it is not, the contact slides. Then $f_c$ is on the edge of the cone that opposes the slip, the twist is the normal of the limit surface at the wrench of that force, and the scale of the twist is fixed by $v_c \cdot n = v_p \cdot n$.

## What it counts

The model predicts the twist of the object as a function of the pusher motion and the contact mode, sticking or sliding. Integrated over a pusher path, it predicts the path of the object. It does not predict how fast the object moves in time, only how it moves per unit of pusher motion, and it does not predict anything when the pusher loses contact or when the inertial forces are large.

The prediction depends on the pressure distribution, which is rarely known. Some predictions are robust: the sense of rotation is the same for every pressure distribution ([Mason's voting theorem](/mason-voting-theorem/)). Others, such as the exact rate of rotation, depend on the distribution.

**Example.** A uniform disc of radius 1 gives $c = (2/3) \cdot 1 = 2/3$, so $c^2 = 4/9$. The pusher touches the bottom point $r_c = (0, -1)$, with inward normal $n = (0, 1)$, and moves with $v_p = (1/2, 1)$. Then $c^2 + x^2 + y^2 = 13/9$, and

$$v_x = \frac{(4/9)(1/2)}{13/9} = \frac{2}{13}, \qquad v_y = \frac{(13/9)(1)}{13/9} = 1, \qquad \omega = \frac{0 - (-1)(2/13)}{4/9} = \frac{9}{26}.$$

The check: the contact point moves with $(v_x - \omega y_c,\ v_y + \omega x_c) = (2/13 + 9/26,\ 1) = (1/2, 1) = v_p$. The force points along $(2/13, 1)$, at $\arctan(2/13) \approx 8.7$ degrees from the normal, so the contact sticks for every $\mu_c \ge 2/13$. The disc turns counterclockwise by $9/26$ radians per unit of pusher travel in $y$.

## Relation to other models

- **Dynamic pushing.** With inertia, the object can keep moving after the pusher stops, and the twist depends on the speed. The quasi-static model is the limit of slow pushing. With rigid contacts and Coulomb friction, the full dynamics can be a [complementarity problem](/rigid-contact-complementarity/) with no solution or several solutions, as in Painlevé's example; the quasi-static model avoids some of these cases but has its own indeterminate cases when the pressure is unknown.
- **Quasi-static grasping.** The same balance with several fingers and no support friction gives grasp statics and [force closure](/force-closure/).
- **Nonholonomic models.** A stable push with a line contact makes the object and pusher one body that can only move along the directions of a cone of motions. It behaves like a car that drives forward with a bounded turning radius, so the tools of [nonholonomic](/nonholonomic-constraint/) planning, such as [Dubins paths](/dubins-path/), apply.
- **Squeezing.** A parallel-jaw squeeze without friction at the jaws is a quasi-static push from two sides. Its outcome, a turn to a local minimum of the width, is the action of [Goldberg's algorithm](/goldberg-part-orienting-algorithm/).

## Known results in the model

- **Sense of rotation.** [Mason's voting theorem](/mason-voting-theorem/) (Mason 1986): the two edges of the friction cone at the contact and the pushing direction vote, by their side of the center of friction, on the sense of rotation. The result does not depend on the pressure distribution.
- **Limit surface properties.** The set of support friction wrenches is convex and the twist is normal to its boundary (Goyal, Ruina and Papadopoulos 1991). This is what makes the balance equation above well posed.
- **Closed form with the ellipsoid.** The sticking formulas above (Lynch, Maekawa and Tanie 1992) are exact for the ellipsoid model and approximate for a real support.
- **Stable pushing.** Lynch and Mason (1996) give the conditions under which a line contact pushes an object without slip at the contact, whatever the pressure distribution, and plan paths made of such pushes.
- **Orienting by pushing.** Pushes against a fence turn a polygon to a stable edge, which gives the push functions used in [sensorless part orienting](/sensorless-part-orienting/).

## References
