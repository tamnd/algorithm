---
tag: RSFJ2H
kind: definition
slug: contact-wrench-cone
name: Contact wrench cone
aliases:
- CWC
area: robotics/mobile-and-legged-robots
level: research
summary: "The set of total wrenches that contact forces in their friction cones can apply to a robot; a polyhedral cone that gives a balance test on any terrain."
prereqs: [friction-cone, wrench]
see_also: [friction-cone, polyhedral-friction-cone, wrench, zero-moment-point, center-of-pressure, support-polygon, grasp-wrench-space, centroidal-dynamics]
sources:
  - paper: doi:10.1109/ICRA.2015.7139910
    title: Stéphane Caron, Quang-Cuong Pham and Yoshihiko Nakamura, Stability of surface contacts for humanoid robots, closed-form formulae of the contact wrench cone for rectangular support areas, IEEE International Conference on Robotics and Automation, 2015
    locator: pages 5107 to 5112
  - paper: doi:10.1109/TRO.2008.2001360
    title: Timothy Bretl and Sanjay Lall, Testing static equilibrium for legged robots, IEEE Transactions on Robotics 24(4), 2008
    locator: pages 794 to 807
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12 (grasping and manipulation), with wrench cones of contacts with friction
---

The contact wrench cone (CWC) of a set of contacts is the set of all total wrenches, a moment and a force together, that the contacts can apply to a robot when each contact force lies in its friction cone. A legged robot can perform a motion only if the wrench that the motion needs, given by the rate of change of its momentum and by gravity, lies in this cone. On flat ground with one flat foot, the cone contains the [zero moment point](/zero-moment-point/) condition and the friction condition together. On uneven ground and with several contacts, where the ZMP is not defined in a useful way, the cone is the general balance condition. Caron, Pham and Nakamura (2015) gave it in closed form for a rectangular foot.

## Definition

Write a wrench as $w = (\tau, f) \in \mathbb{R}^6$, moment first, with the moment taken about a fixed reference point $O$. Let a robot touch its surroundings at points $p_1, \dots, p_c$, with a [friction cone](/friction-cone/) $FC_i$ at each point (coefficient $\mu_i$, normal $n_i$ that points into the robot). A force $f_i$ at $p_i$ gives the wrench $(p_i \times f_i, f_i)$ about $O$. The **contact wrench cone** is

$$CWC = \left\{ \sum_{i=1}^{c} (p_i \times f_i,\ f_i) : f_i \in FC_i \right\}.$$

It is the image of the product of the friction cones under a linear map, so it is a convex cone. If each friction cone is replaced by a [polyhedral friction cone](/polyhedral-friction-cone/) with $k$ edges, the CWC is the convex cone spanned by the $c k$ edge wrenches: a polyhedral cone, given by its generators. For a balance test, it is often converted to a list of linear inequalities $A w \le 0$ by a cone projection or a double description method.

A flat contact surface, such as a foot sole, is a contact at every point of its area. If the area is a convex polygon, its CWC equals the CWC of its corners, because a force $f$ in the friction cone at a point $x = \sum_j \lambda_j v_j$ of the polygon gives the wrench $\sum_j \lambda_j (v_j \times f, f)$, a sum of corner wrenches with corner forces $\lambda_j f$ in the same cone.

**The balance condition.** Let the robot have mass $m$, center of mass $c$, linear momentum $P$ and angular momentum $L$ about $O$, with gravity $g = 9.81$ along $-z$. By the Newton and Euler equations of [centroidal dynamics](/centroidal-dynamics/), the contacts must supply the wrench

$$w_{\text{contact}} = \left( \dot L - c \times m g_v,\ \dot P - m g_v \right), \qquad g_v = (0, 0, -g).$$

A motion is possible with the given contacts if and only if $w_{\text{contact}} \in CWC$. For a robot at rest, $\dot L = 0$ and $\dot P = 0$, and the test becomes the static equilibrium test of Bretl and Lall (2008).

**The rectangular foot in closed form.** Take a rectangular sole with half-lengths $X$ along $x$ and $Y$ along $y$, the reference point at its center, $z$ along the normal, and at each corner the square friction pyramid $|f_x| \le \mu f_z$, $|f_y| \le \mu f_z$ (a pyramid with $k = 4$ edges $(\pm \mu, \pm \mu, 1)$). Caron, Pham and Nakamura (2015) show that a wrench $(\tau, f)$ is in the CWC if and only if

$$|f_x| \le \mu f_z, \qquad |f_y| \le \mu f_z, \qquad |\tau_x| \le Y f_z, \qquad |\tau_y| \le X f_z, \qquad \tau_{\min} \le \tau_z \le \tau_{\max},$$

with

$$\tau_{\min} = -\mu (X + Y) f_z + |Y f_x - \mu \tau_x| + |X f_y - \mu \tau_y|,$$
$$\tau_{\max} = \mu (X + Y) f_z - |Y f_x + \mu \tau_x| - |X f_y + \mu \tau_y|.$$

The absolute values expand to $16$ linear inequalities, and $f_z \ge 0$ follows from them. Caron et al. write the wrench with the force first; the formulas above are the same with the moment first. With $X = 0.1$ m, $Y = 0.05$ m and $\mu = 0.7$, the cone spanned by the $16$ corner edge wrenches has exactly these $16$ facets.

The five groups of rows have a direct meaning. The first two are the friction pyramid of the whole foot. The rows on $\tau_x$ and $\tau_y$ say that the [center of pressure](/center-of-pressure/), at $(-\tau_y / f_z, \tau_x / f_z)$, lies in the sole, which is the ZMP condition. The last row bounds the yaw moment that friction can resist, and the bound shrinks when the foot already uses friction for a tangential force or when the center of pressure is near an edge.

## Examples and non-examples

**A foot that carries a load.** Let $X = 0.1$ m, $Y = 0.05$ m, $\mu = 0.7$ and $f = (0, 0, 500)$ N. The CWC allows $|\tau_x| \le 25$ N m, $|\tau_y| \le 50$ N m and, with $\tau_x = \tau_y = 0$, $|\tau_z| \le \mu (X + Y) f_z = 52.5$ N m.

**Sideways force reduces the yaw moment.** With $f = (100, 0, 500)$ N and $\tau_x = \tau_y = 0$, the bounds become $\tau_{\min} = -52.5 + 5 = -47.5$ N m and $\tau_{\max} = 52.5 - 5 = 47.5$ N m. The foot can resist less twist while it also pushes sideways.

**A wrench outside the cone.** With $f = (0, 0, 500)$ N and $\tau_y = 60$ N m, the row $|\tau_y| \le X f_z = 50$ fails. The center of pressure would be at $x = -0.12$ m, behind the heel: the foot tips back.

**Two feet on different heights.** A robot with one foot on the floor and one on a step has a total CWC that is the [Minkowski sum](/minkowski-sum/) of the two foot cones, each expressed about the same point $O$. The [support polygon](/support-polygon/) and the ZMP are not defined for this case, but the condition $w_{\text{contact}} \in CWC$ is.

**Non-example: the grasp wrench space.** The [grasp wrench space](/grasp-wrench-space/) of a grasp is also built from contact wrenches, but it is a bounded set: the forces are scaled to a total size of at most 1, so it measures how strong the grasp is. The CWC is a cone: it has no size limit and only says which wrench directions the contacts can apply.

**Non-example: a pull.** A wrench with $f_z < 0$ on a flat foot is never in the CWC. A contact that can pull, such as a gripper on a rail, needs a different model.

## Related definitions

- [Friction cone](/friction-cone/) and [polyhedral friction cone](/polyhedral-friction-cone/): the force set at one contact point, from which the CWC is built; the pyramid with $k$ edges gives a polyhedral CWC.
- [Wrench](/wrench/): the pair of a moment and a force; this page puts the moment first.
- [Zero moment point](/zero-moment-point/) and [center of pressure](/center-of-pressure/): on flat ground, two rows of the foot CWC are the condition that the ZMP is in the sole.
- [Support polygon](/support-polygon/): the static balance test on flat ground, a special case of the CWC test.
- [Grasp wrench space](/grasp-wrench-space/): the bounded set of contact wrenches used to score grasps.
- [Centroidal dynamics](/centroidal-dynamics/): gives the wrench that a motion needs, which the CWC test compares with the contacts.

## References
