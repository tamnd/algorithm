---
tag: X12EA0
kind: definition
slug: antipodal-grasp
name: Antipodal grasp
aliases:
- two-finger antipodal grasp
area: robotics/grasping-and-manipulation
level: core
summary: A grasp by two fingers whose connecting line lies strictly inside both friction cones; in the plane this is exactly two-finger force closure.
prereqs: [force-closure, friction-cone]
see_also: [force-closure, friction-cone, grasp-contact-models, force-closure-test, finger-bounds-for-form-closure, grasp-synthesis, independent-contact-regions, caging-grasp]
sources:
  - paper: doi:10.1177/027836498800700301
    title: "Van-Duc Nguyen, Constructing force-closure grasps, International Journal of Robotics Research 7(3), 3-16, 1988"
    locator: the condition for force closure with two frictional fingers in the plane, and the regions of the boundary where the fingers can be placed
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (force-closure grasps, the antipodal condition in the plane and with soft fingers in space)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12, Section 12.2.3 (Force Closure), with planar two-contact examples
  - book: isbn:9783319325507
    title: "Domenico Prattichizzo and Jeffrey C. Trinkle, Grasping, Chapter 38 of the Springer Handbook of Robotics, second edition, Springer, 2016"
    locator: "Section 38.4.2 (Force Closure), where Nguyen's graphical test is applied to planar grasps with two frictional contacts; the chapter is pages 955 to 988"
---

An antipodal grasp holds an object between two fingers that press toward each other along one line, with that line inside the friction cone of each finger. It is the grasp of a parallel-jaw gripper, of tweezers, and of a thumb and index finger. In the plane the condition is exactly what two fingers need for [force closure](/force-closure/): squeeze along the line, and friction does the rest. In space two hard fingers cannot stop the object from spinning about their line, so the antipodal condition there needs soft fingers, which resist twist.

## Definition

Two fingers touch a rigid object at the points $p_1 \ne p_2$ with inward unit normals $n_1$ and $n_2$ and coefficient of friction $\mu > 0$. Let $FC_1$ and $FC_2$ be their [friction cones](/friction-cone/), with half-angle $\alpha = \arctan \mu$, and let $u = (p_2 - p_1) / \lVert p_2 - p_1 \rVert$.

**Antipodal grasp.** The grasp is antipodal if $u$ is in the interior of $FC_1$ and $-u$ is in the interior of $FC_2$. In angles: the line through $p_1$ and $p_2$ makes an angle less than $\alpha$ with each normal,

$$\angle(u, n_1) < \arctan \mu \quad\text{and}\quad \angle(-u, n_2) < \arctan \mu.$$

The two points are then called antipodal points of the object for that $\mu$. With $\mu = 0$ the cones have empty interior, and the points are antipodal in the exact sense only if both normals lie along the line.
**The planar theorem** (Nguyen 1988). In the plane, two hard fingers hold an object in force closure if and only if the grasp is antipodal, or the same holds with $u$ replaced by $-u$ (an inside grasp, where the fingers push apart).

*Proof.* The squeeze $f_1 = u$, $f_2 = -u$ consists of two opposite forces on one line, so its total force and its total moment are zero. It is strictly inside both cones. The wrenches of forces through $p_1$ form a 2-dimensional subspace of $\mathbb{R}^3$, and so do those through $p_2$; the two subspaces differ because $p_1 \ne p_2$, so together they span $\mathbb{R}^3$ and the [grasp matrix](/grasp-matrix/) has rank 3. By the rank and interior form of force closure, the grasp is in force closure. Conversely, force closure gives forces $f_1$ and $f_2$ strictly inside the cones with $f_1 + f_2 = 0$ and $(p_1 - p_2) \times f_1 = 0$. The second equation makes $f_1$ parallel to $u$, and $f_1 \ne 0$, so $f_1 = a u$ with $a \ne 0$. If $a > 0$ the grasp is antipodal; if $a < 0$ it is an inside grasp. $\square$

**In space.** Two hard fingers are never in force closure: every contact force passes through the line $p_1 p_2$ and has no moment about it, so the grasp matrix has rank 5. With soft fingers, each finger also resists a moment $\lvert m_n \rvert \le \gamma f_n$ about its normal. If the grasp is antipodal and $\gamma > 0$, the normals have a component along the line, and the torsion of the two fingers resists a moment about it; then the grasp is in force closure. The size of that resisted moment grows with $\gamma$ and with the squeeze.

## Examples and non-examples

**A box between parallel jaws.** Jaws touch the sides $x = \pm 1$ of a box at $(-1, 0)$ and $(1, 0)$. The line is along both normals, the angles are 0, and the grasp is antipodal for every $\mu > 0$. With $\mu = 0.5$ and a box of 1 kg, the squeeze must be at least 9.81 N to carry the weight on friction alone (the example on the [grasp matrix](/grasp-matrix/) page).

**Off-axis contacts.** Move the contacts to $(-1, 0.5)$ and $(1, -0.5)$. The line makes the angle $\arctan(1/2) \approx 26.57$ degrees with each normal. The grasp is antipodal, and in force closure, exactly when $\mu > 0.5$. At $\mu = 0.6$ the [force-closure test](/force-closure-test/) answers closed; at $\mu = 0.5$ the line lies on the boundary of both cones, and the test answers not closed.

**A tapered part.** A parallel-jaw gripper grips a part whose two sides taper, each tilted by 10 degrees from the closing direction. The normals make 10 degrees with the line of the jaws, so the grasp is antipodal when $\arctan \mu > 10$ degrees, that is $\mu > \tan(10 \text{ degrees}) \approx 0.176$. With a slippery part, $\mu = 0.15$, the squeeze pushes the part out of the jaws.

**Every smooth convex body has antipodal points.** On a smooth convex planar body, take the two ends of a longest chord. The boundary at each end is perpendicular to the chord (otherwise a nearby chord would be longer), so the chord lies along both normals. These two points form an antipodal grasp for every $\mu > 0$.

**Two soft fingers on a ball.** Two fingertips press on opposite points of a ball. The grasp is antipodal. With hard fingers the ball spins freely about the line of the fingers. With soft fingers of torsion coefficient $\gamma$ and squeeze $s$, it resists a moment about that line of up to $2\gamma s$.

**Non-example: a corner.** A finger on a vertex of a polygon has no single normal. The usual models use the normal of the other body, or treat the vertex as having a cone of normals. The antipodal test is not defined there without such a convention.

**Non-example: adjacent sides.** Fingers on two adjacent sides of the square $[-1, 1]^2$, at $(-1, 0)$ with normal $(1, 0)$ and at $(0, 1)$ with normal $(0, -1)$, have a line at 45 degrees to both normals. The grasp is antipodal only for $\mu > 1$, which few pairs of materials reach.

## Related definitions

- [Force closure](/force-closure/): the general property; in the plane, two fingers have it exactly when they are antipodal.
- [Friction cone](/friction-cone/): the cone that the line between the contacts must enter.
- [Grasp contact models](/grasp-contact-models/): hard and soft fingers; the soft model is what makes a spatial antipodal grasp closed.
- [Finger bounds for form closure](/finger-bounds-for-form-closure/): without friction, 4 fingers are needed in the plane; with friction, two antipodal fingers can suffice.
- [Independent contact regions](/independent-contact-regions/): regions around each contact inside which every choice of points keeps force closure; for two fingers in the plane, regions that stay antipodal.
- [Grasp synthesis](/grasp-synthesis/): many planners for parallel-jaw grippers sample pairs of surface points and keep the antipodal ones.
- [Caging](/caging-grasp/): a weaker way to hold an object with two fingers, by trapping it without force closure.

## References
