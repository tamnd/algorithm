---
tag: 735KNH
kind: theorem
slug: finger-bounds-for-form-closure
name: Finger bounds for form closure
aliases:
- Markenscoff-Ni-Papadimitriou theorem
area: robotics/grasping-and-manipulation
level: advanced
summary: "Form closure needs at least 4 frictionless fingers in the plane and 7 in space; these suffice for bodies other than a disc or a surface of revolution."
prereqs: [form-closure, force-closure]
see_also: [form-closure, force-closure, force-closure-test, caratheodory-theorem, convex-hull, antipodal-grasp, fixture-planning, three-two-one-locating-principle]
sources:
  - paper: doi:10.1177/027836499000900102
    title: "Xanthippi Markenscoff, Luqun Ni and Christos H. Papadimitriou, The geometry of grasping, International Journal of Robotics Research 9(1), 61-74, 1990"
    locator: the upper bounds of 4 frictionless fingers in the plane and 7 in space, and of 3 and 4 fingers with friction
  - paper: "Bhubaneswar Mishra, Jacob T. Schwartz and Micha Sharir, On the existence and synthesis of multifinger positive grips, Algorithmica 2(4), 541-558, 1987"
    locator: the bounds of 6 fingers in the plane and 12 in space through the theorem of Steinitz
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.1 (Form Closure), the necessary conditions of Somov and Lakshminarayana, Table 38.9 (minimum number of contacts), and the remark on surfaces of revolution; the chapter is pages 955 to 988"
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12, Section 12.1.7 (Form Closure), the number of contacts needed for first-order form closure
  - paper: "P. Somov, Über Schraubengeschwindigkeiten eines festen Körpers bei verschiedener Zahl von Stützflächen, Zeitschrift für Mathematik und Physik 42, 133-153 and 161-182, 1897"
    locator: the proof that a rigid body in space needs at least seven contacts to be form closed
  - paper: "K. Lakshminarayana, Mechanics of Form Closure, ASME technical paper 78-DET-32, 1978"
    locator: the general bound of n + 1 contacts for a body with n degrees of freedom
---

How many frictionless fingers does it take to hold a rigid body so that it cannot move at all? The answer has two halves. Below a count, no placement works, for any shape: 4 fingers in the plane and 7 in space are needed. And for almost every shape that count is also enough: Markenscoff, Ni and Papadimitriou showed in 1990 that 4 fingers in the plane and 7 in space suffice, except for the shapes that can turn in place, the disc and the surfaces of revolution, which no number of frictionless fingers can hold. With friction the counts drop to 3 and 4.

## Statement

Let a bounded rigid body $B$ be held by $c$ frictionless point contacts. Let $d = 3$ in the plane and $d = 6$ in space. Form closure means [first-order form closure](/form-closure/): the contact wrenches $(p_i \times n_i, n_i)$ positively span $\mathbb{R}^d$.

**Theorem.**

1. **Lower bound** (Somov 1897 in space; Lakshminarayana 1978 in general). If $c$ frictionless contacts hold $B$ in form closure, then $c \ge d + 1$: at least 4 in the plane and 7 in space.
2. **Exceptions.** If $B$ is a disc, or in space a body whose surface is a surface of revolution, then no finite set of frictionless contacts holds $B$ in form closure.
3. **Upper bound, weak form** (Mishra, Schwartz and Sharir 1987). If $B$ is not one of the exceptions, then $2d$ contacts suffice: 6 in the plane and 12 in space.
4. **Upper bound, tight form** (Markenscoff, Ni and Papadimitriou 1990). A planar body with a piecewise smooth boundary that is not a disc can be held in form closure by 4 contacts. A body in space whose surface is not a surface of revolution can be held in form closure by 7 contacts, under general conditions on the surface. With Coulomb friction, 3 fingers suffice in the plane and 4 in space.

## In plain words

Each frictionless finger can only push straight into the surface. To pin a body, the pushes together must be able to oppose any shove or twist. In the plane a body can move in three ways, two slides and a turn, and in space in six. A set of pushes that covers all directions of those motions needs one push more than the number of motions, so at least 4 fingers in the plane and 7 in space. A round disc or a ball can spin under any set of such fingers, because every push points at the center or the axis and cannot stop the spin. For every other reasonable shape, the minimum is also enough: a careful choice of 4 or 7 points pins it. Friction lets each finger push a little sideways, which saves fingers.

## Proof

**Part 1.** Let $w_1, \ldots, w_c$ positively span $\mathbb{R}^d$. They span it, so $c \ge d$. Suppose $c = d$. Then the $w_i$ form a basis. The vector $-(w_1 + \cdots + w_d)$ is a nonnegative combination $\sum_i k_i w_i$, so $\sum_i (1 + k_i) w_i = 0$ with all coefficients positive, which contradicts the linear independence of a basis. So $c \ge d + 1$.

**Part 2.** For a disc with center $o$, every normal line passes through $o$, so every contact wrench has zero moment about $o$. All wrenches lie in the plane $m_z = 0$ of $\mathbb{R}^3$, they do not span, and the rotation about $o$ is a free motion. For a surface of revolution with axis $a$, every normal line meets $a$ (or is parallel to it), so every contact force has zero moment about $a$. The wrenches lie in a hyperplane of $\mathbb{R}^6$, and the rotation about $a$ is free. This is a free motion of the body, not only a first-order one, because the rotation maps the body onto itself.

**Part 3.** Let $W$ be the set of all wrenches $(p \times n, n)$ over the smooth points $p$ of the boundary. A finite set of wrenches positively spans $\mathbb{R}^d$ if and only if the origin is in the interior of its [convex hull](/convex-hull/).

*Step 1: $W$ positively spans.* Suppose not. As in the proof on the [form closure](/form-closure/) page, there is a twist $\mathcal{V} \ne 0$ with $w^T \mathcal{V} \ge 0$ for all $w \in W$. Let $u(x)$ be the velocity field of $\mathcal{V}$, which has zero divergence, as every rigid velocity field has. The condition says $u \cdot n \ge 0$ with the inward normal $n$ at every smooth boundary point. By the divergence theorem, the flux of $u$ out of $B$ is $\int_B \operatorname{div} u = 0$, and it is a sum of terms $-u \cdot n \le 0$. So $u \cdot n = 0$ on the boundary: the flow of $\mathcal{V}$ is tangent to the boundary and maps $B$ to itself. A screw motion with a nonzero pitch, or a translation, carries every point to infinity, which a bounded body cannot follow. So $\mathcal{V}$ is a rotation about an axis, and $B$ is a body of revolution about it (a disc in the plane). This is excluded.

*Step 2: Steinitz.* The theorem of Steinitz states that a point in the interior of the convex hull of a set $S \subset \mathbb{R}^d$ is in the interior of the convex hull of at most $2d$ points of $S$. This is the interior version of [Carathéodory's theorem](/caratheodory-theorem/). By Step 1, the origin is in the interior of the convex hull of $W$, so it is in the interior of the convex hull of $2d$ wrenches of $W$. The $2d$ boundary points that give them hold $B$ in form closure. The argument needs care at corners, where we use only the smooth points, and in the claim that the flow maps $B$ to itself; Mishra, Schwartz and Sharir treat the details.

**Part 4.** The proof of Markenscoff, Ni and Papadimitriou is a construction that goes through the cases of the boundary geometry, and we do not reproduce it. With friction each cone gives two or more directions per contact, so fewer contacts are needed. A 2020 paper in Mechanism and Machine Theory points out that the original paper ends its analysis of the spatial case with the remark that the proof "would entail a much more exhaustive case analysis". The spatial bound of 7 is widely cited, but a reader who needs it inside a proof should check the original argument for the shapes at hand. $\square$

## Consequences

- **Fixtures.** A fixture that holds a planar part needs at least 4 contacts and a spatial part at least 7, counting clamps. The [3-2-1 locating principle](/three-two-one-locating-principle/) uses 6 locators to fix the position and adds clamps to hold the part. With one well-placed clamp the count is 7, the minimum. [Fixture planning](/fixture-planning/) searches for such sets.
- **The test.** For a given set of contacts, the [force-closure test](/force-closure-test/) with $\mu = 0$ decides form closure. The theorem tells a planner how many contacts to try.
- **Smaller hands with friction.** A hand with three fingers and friction can hold most planar parts, and four fingers can hold most spatial parts. With hard fingers in space, three non-collinear contacts can already give [force closure](/force-closure/), and two soft fingers can.
- **Two fingers in the plane.** A smooth convex planar body can always be held by two frictional fingers: at the two ends of a diameter (a longest chord), the boundary is perpendicular to the chord, so the line of the fingers is along both normals. This is an [antipodal grasp](/antipodal-grasp/) for any $\mu > 0$.

## Tightness

- **The lower bound is tight.** The square $[-1, 1]^2$ is held in form closure by 4 contacts, one per side and placed off the center lines, and the cube $[-1, 1]^3$ by 7 contacts (both examples are on the [form closure](/form-closure/) page, with exact certificates). So 4 and 7 cannot be improved.
- **The lower bound is not sufficient.** Placing $d + 1$ contacts is not enough by itself: seven contacts on one face of a cube do not hold it, since the cube can lift off. The positions matter, and the force-closure test checks them.
- **The weak upper bound is tight for general sets.** Steinitz's bound $2d$ is tight for arbitrary point sets: the $2d$ points $\pm e_j$ contain the origin in the interior of their hull, and no proper subset does. The improvement to $d + 1$ uses the special structure of the wrench sets of real bodies.
- **The exceptions are real.** A disc rotates under any frictionless grasp, so no bound holds for it. Higher-order form closure (Rimon and Burdick 1998) can hold some bodies with fewer contacts than $d + 1$ by using curvature, but such grasps are not first-order and are less robust.

## History

Franz Reuleaux studied pairs of machine parts that hold each other by their form in his book on the kinematics of machinery (German 1875, English translation 1876). P. Somov proved in 1897 that a rigid body in space needs at least seven contacts to be held by form. K. Lakshminarayana extended the bound to $n + 1$ contacts for $n$ degrees of freedom in 1978, using the theory of polyhedral convex cones. In robotics, Mishra, Schwartz and Sharir (1987) gave the first general upper bounds, 6 and 12, with the theorem of Steinitz, and algorithms to place the fingers. Markenscoff, Ni and Papadimitriou (1990) brought the upper bounds down to the lower ones, 4 and 7, and gave the counts 3 and 4 for fingers with friction.

## References
