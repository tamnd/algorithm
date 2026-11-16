---
tag: 93TG1A
kind: definition
slug: form-closure
name: Form closure
aliases:
- geometric closure
area: robotics/grasping-and-manipulation
level: core
summary: A set of fixed frictionless contacts holds a rigid body in form closure when the contacts alone, by their geometry, prevent every motion of the body.
prereqs: [grasp-contact-models, rigid-body-twist]
see_also: [force-closure, finger-bounds-for-form-closure, force-closure-test, caging-grasp, fixture-planning, kinematic-fixture-analysis, three-two-one-locating-principle, modular-fixture-design]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: "Chapter 12, Section 12.1.7 (Form Closure): first-order form closure, the linear program test of Section 12.1.7.2 and the choice of contacts in Section 12.1.7.4"
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.1 (Form Closure), Definition 38.6 by gap functions and the first-order condition; the chapter is pages 955 to 988"
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 5 (Rigid Body Statics), Section 5.4 (cones in velocity twist space) and Section 5.6 (instantaneous centers and Reuleaux's method)
  - paper: "Elon Rimon and Joel W. Burdick, Mobility of bodies in contact, Part I: A 2nd-order mobility index for multiple-finger grasps, IEEE Transactions on Robotics and Automation 14(5), 696-708, 1998"
    locator: form closure of second order, from the curvature of the body and of the fingers
  - book: "Franz Reuleaux, The Kinematics of Machinery, translated by A. B. W. Kennedy, Macmillan, 1876; reprinted by Dover, 1963"
    locator: the early study of pairs of elements that hold each other by their form
---

A body is in form closure when a set of fixed contacts holds it so that it cannot move at all, by geometry alone: every motion of the body, however small, would push it into one of the contacts. Friction plays no part, and the contacts need not push; they only have to be there. A peg in a tight hole and a part in a well-designed fixture are in form closure. The idea is older than robotics, and machine designers have used it for pairs of parts that hold each other by their shape. It is the strongest kind of grasp, and it is the property that [fixture planning](/fixture-planning/) and the [3-2-1 locating principle](/three-two-one-locating-principle/) aim for.

## Definition

Let a rigid body $B$ touch $c$ fixed obstacles (fingers or locators) at the points $p_1, \ldots, p_c$ of its surface. Let $n_i$ be the unit normal at $p_i$, pointing into $B$. All quantities are in a body frame. The contacts are frictionless, and the fingers are rigid and do not move.

**Form closure.** The contacts hold $B$ in form closure if every motion of $B$ makes some point of $B$ penetrate some finger. The Handbook writes this with gap functions $\psi_i(u)$, the distance between $B$ and finger $i$ after a displacement $u$ of $B$: form closure holds if $\psi_i(u) \ge 0$ for all $i$ implies $u = 0$, for small $u$ (its Definition 38.6).

**First-order form closure.** Let $B$ move with the twist $\mathcal{V} = (\omega, v)$ (the angular part first, as the moment comes first in a wrench). The point $p_i$ moves with velocity $v + \omega \times p_i$. To first order, contact $i$ does not penetrate if this velocity has no component into the finger:

$$n_i^T (v + \omega \times p_i) \ge 0 \quad\Longleftrightarrow\quad \mathcal{F}_i^T \mathcal{V} \ge 0, \qquad \mathcal{F}_i = (p_i \times n_i,\ n_i).$$

The vector $\mathcal{F}_i$ is the wrench of a unit normal force at $p_i$. The contacts give **first-order form closure** if the only twist that satisfies all $c$ inequalities is $\mathcal{V} = 0$.

**The force view.** First-order form closure holds if and only if the wrenches $\mathcal{F}_1, \ldots, \mathcal{F}_c$ positively span the wrench space: every wrench is $\sum_i k_i \mathcal{F}_i$ with $k_i \ge 0$. Proof. Assume they positively span, and let $\mathcal{V}$ satisfy all inequalities. Write $-\mathcal{V} = \sum_i k_i \mathcal{F}_i$ with $k_i \ge 0$. Then $-\lVert \mathcal{V} \rVert^2 = \sum_i k_i \mathcal{F}_i^T \mathcal{V} \ge 0$, so $\mathcal{V} = 0$. Conversely, assume the cone $\operatorname{pos}\{\mathcal{F}_i\}$ is not the whole space. It is a closed convex cone, so by the [separating hyperplane theorem](/separating-hyperplane-theorem/) there is a $\mathcal{V} \ne 0$ with $\mathcal{F}^T \mathcal{V} \ge 0$ for every $\mathcal{F}$ in the cone, and in particular $\mathcal{F}_i^T \mathcal{V} \ge 0$ for all $i$. That twist moves $B$ without first-order penetration. $\square$

So first-order form closure is the same as [force closure](/force-closure/) with frictionless contacts: the normal forces alone can balance any external wrench. The test is a linear program, the [force-closure test](/force-closure-test/) with $\mu = 0$. In matrix form it reads: $\operatorname{rank} F = d$ and $F k = 0$ for some $k > 0$, where $F = [\mathcal{F}_1 \cdots \mathcal{F}_c]$ and $d$ is 3 in the plane and 6 in space.

**Higher order.** First-order form closure implies form closure. The converse is false: if a twist $\mathcal{V} \ne 0$ has $\mathcal{F}_i^T \mathcal{V} = 0$ for some contacts, the first-order test cannot decide, and the curvatures of the body and the fingers at those contacts decide whether the motion penetrates. Rimon and Burdick (1998) give the second-order theory. Such grasps can hold a body with fewer contacts than the first-order count, but they depend on exact curvature and are less robust.

## Examples and non-examples

**A square held by four contacts.** The square $[-1, 1]^2$ is touched at $(-1, 0.5)$ with $n = (1, 0)$, at $(1, -0.2)$ with $n = (-1, 0)$, at $(0.3, -1)$ with $n = (0, 1)$ and at $(-0.4, 1)$ with $n = (0, -1)$. With the planar moment $p_x n_y - p_y n_x$, the wrenches $(m_z, f_x, f_y)$ are

$$\mathcal{F}_1 = (-0.5, 1, 0),\ \mathcal{F}_2 = (-0.2, -1, 0),\ \mathcal{F}_3 = (0.3, 0, 1),\ \mathcal{F}_4 = (0.4, 0, -1).$$

They span $\mathbb{R}^3$, and their sum is $(0, 0, 0)$, since $-0.5 - 0.2 + 0.3 + 0.4 = 0$. So $k = (1, 1, 1, 1)$ is a strictly positive combination that gives zero, and the square is in first-order form closure. Four is the least number of frictionless contacts that can do this in the plane.

**Non-example: a pinwheel.** Move the contacts to $(-1, 0.5)$, $(1, -0.5)$, $(0.5, 1)$ and $(-0.5, -1)$, with the same inward normals. Each wrench now has the moment $-0.5$. The twist $\mathcal{V} = (\omega, v_x, v_y) = (-1, 0, 0)$, a clockwise turn about the center, gives $\mathcal{F}_i^T \mathcal{V} = 0.5 > 0$ at every contact: all four contacts open, and the square turns out of the grasp.

**Non-example: a disc.** Each normal of a disc passes through its center, so each contact wrench has zero moment about the center. The twist of a rotation about the center gives $\mathcal{F}_i^T \mathcal{V} = 0$ for every contact, and the disc turns in place. No number of frictionless contacts holds a disc in form closure. In space the same is true for a sphere, a cylinder, and any other surface of revolution (about its axis).

**A cube held by seven contacts.** The cube $[-1, 1]^3$ is held in first-order form closure by contacts at $(1, 0, -\tfrac12)$, $(-1, -\tfrac12, 0)$, $(\tfrac12, 1, 0)$, $(0, -1, 0)$, $(-\tfrac12, 0, 1)$, $(0, -\tfrac12, -1)$ and $(0, \tfrac12, -1)$, each with the inward normal of its face. The coefficients $k = (2, 2, 2, 2, 2, 1, 1)$ make the seven wrenches sum to zero, and the wrenches span $\mathbb{R}^6$. Removing any one contact leaves six, and six vectors never positively span $\mathbb{R}^6$.

**Non-example: six locators.** The [3-2-1 locating principle](/three-two-one-locating-principle/) puts a part against three points on one face, two on a second face and one on a third. The six contacts fix the position of the part when it is pushed against them, but they do not hold it: the part can lift off in the opposite directions. Clamps that push the part onto the locators complete the fixture. [Kinematic fixture analysis](/kinematic-fixture-analysis/) and [modular fixture design](/modular-fixture-design/) check and plan such layouts.

**Non-example: caging.** A ring around a body can prevent it from escaping while leaving it free to rattle. That is [caging](/caging-grasp/), a weaker property than form closure.

## Related definitions

- [Force closure](/force-closure/): the contact forces, with friction, can balance any external wrench. Form closure with frictionless contacts is the case $\mu = 0$.
- [Finger bounds for form closure](/finger-bounds-for-form-closure/): at least 4 contacts in the plane and 7 in space are needed, and for bodies that are not surfaces of revolution these numbers suffice.
- [Force-closure test](/force-closure-test/): the linear program that decides first-order form closure when $\mu = 0$.
- [Grasp contact models](/grasp-contact-models/): form closure uses the frictionless point model.
- [Fixture planning](/fixture-planning/): the choice of locators and clamps that put a part in form closure.
- [Caging](/caging-grasp/): trapping a body without immobilizing it.

## References
