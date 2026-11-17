---
tag: CV81YD
kind: problem
slug: continuous-collision-detection
name: Continuous collision detection
aliases:
- time of impact computation
area: graphics-and-signals/rigid-body-simulation
level: core
summary: Find the first time in a time step at which two moving objects touch, so that fast objects do not pass through each other.
prereqs: [collision-detection, polynomial-root-finding]
see_also: [conservative-advancement, elementary-ccd-tests, robust-cloth-collision, impact-zones, incremental-potential-contact, screw-motion, interval-arithmetic, gjk-algorithm]
sources:
  - paper: doi:10.1007/978-3-7091-6874-5_13
    title: Xavier Provot, Collision and self-collision handling in cloth model dedicated to design garments, Computer Animation and Simulation 97 (Proceedings of the Eurographics Workshop), Springer, 1997, 177 to 189
    locator: the continuous tests of a vertex against a triangle and of two edges, with linear motion during the time step
  - paper: doi:10.1109/ROBOT.2009.5152234
    title: Min Tang, Young J. Kim and Dinesh Manocha, C2A, controlled conservative advancement for continuous collision detection of polygonal models, Proceedings of the 2009 IEEE International Conference on Robotics and Automation
    locator: the time of impact of rigid polygonal models under rigid motion, by conservative advancement
  - paper: doi:10.1145/2185520.2185592
    title: Tyson Brochu, Essex Edwards and Robert Bridson, Efficient geometrically exact continuous collision detection, ACM Transactions on Graphics 31(4), 2012, article 96
    locator: the exact answer of the elementary tests with linear motion
  - paper: doi:10.1145/3460775
    title: Bolun Wang, Zachary Ferguson, Teseo Schneider, Xin Jiang, Marco Attene and Daniele Panozzo, A large-scale benchmark and an inclusion-based algorithm for continuous collision detection, ACM Transactions on Graphics 40(5), 2021, article 188
    locator: the benchmark of elementary queries, and the comparison of the false negatives and false positives of many methods
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: the material on dynamic intersection tests of moving objects
---

Continuous collision detection (CCD) asks for the first time in a time step at which two moving objects touch. A simulation that only tests the positions at the start and at the end of each step can miss a contact: a small, fast object can be on one side of a thin wall at the start and on the other side at the end, with no overlap at either time. This is called tunneling. CCD looks at the whole motion during the step. It returns the time of impact, or reports that there is no contact in the step, so that the simulator can stop the motion at the contact or handle the contact in the right order. The answer depends on how the objects move between the two positions, so the problem includes a motion model.

## In plain words

A simulator moves objects in small jumps of time. If it only looks at where things are after each jump, a fast bullet can jump right through a thin wall and never be seen touching it.

Continuous collision detection asks a different question. It looks at the whole path from one moment to the next, and it finds the first moment when the two objects touch. Then the simulator can stop them there. To answer, it must assume how the objects move between the two moments, for example in a straight line, or in a straight line while they spin at a steady rate.

## Definition

**Input.** Two objects $A$ and $B$, and their motions over a time interval, scaled to $[0, 1]$. Common motion models are:

- **Linear vertices.** Each vertex of a mesh moves on a straight line from its start position to its end position. This is the model of cloth and deformable solids.
- **Rigid motion.** Each object is rigid, with a position and an orientation that are functions of time. A common choice is a constant linear and angular velocity, or a [screw motion](/screw-motion/) between the two poses.
- **Pure translation.** Each object moves on a straight line without turning.

**Output.** The time of impact $t^* = \min \{ t \in [0, 1] : A(t) \cap B(t) \ne \emptyset \}$, or "none" if the objects do not touch in the step. Many uses also want the contact point and the normal at $t^*$. A conservative answer is a time $t \le t^*$ such that the objects do not touch in $[0, t)$, together with a bound on $t^* - t$.

**Cost model.** For meshes, the number of elementary tests of a vertex against a triangle or of an edge against an edge, after a broad phase. For rigid convex objects, the number of distance queries. For exact methods, the arithmetic model matters: with linear vertices each elementary test is a cubic equation, and floating point roots can miss a contact, so the claims of exactness are made in exact or [interval arithmetic](/interval-arithmetic/), or in floating point with a stated tolerance.

## Variants

- **A minimum gap.** Find the first time at which the distance drops to a given gap $\eta > 0$. Many simulators keep such a gap, so that the next step does not start in contact.
- **Boolean CCD.** Only decide whether the objects touch during the step.
- **All contacts.** For two meshes, find all pairs of primitives that touch during the step, each with its time. Cloth simulation needs this for its self-collisions.
- **Many objects.** A broad phase over the boxes of the swept volumes, for example with [sweep and prune](/sweep-and-prune/) or a [bounding volume hierarchy](/bounding-volume-hierarchy/), picks candidate pairs, and CCD runs on each pair.
- **Discrete detection with sub-steps.** Test the positions at several times inside the step. This is not CCD: it shrinks the risk of tunneling but does not remove it.

## Examples

**A ball and a thin wall.** A ball of radius $0.1$ moves from the center $(-1, 0)$ to the center $(1, 0)$ during the step, and a wall fills $0 \le x \le 0.05$. At $t = 0$ the ball covers $x \in [-1.1, -0.9]$, and at $t = 1$ it covers $[0.9, 1.1]$, so neither end of the step shows an overlap. The center is at $x = -1 + 2t$, and the ball first touches the wall when $-1 + 2t + 0.1 = 0$, that is at $t^* = 0.45$.

**Two moving disks.** A disk of radius 1 rests at the origin. A second disk of radius 1 moves from the center $(5, 1)$ with the velocity $(-6, 0)$ per step. The disks touch when the distance of the centers is 2, that is when $(5 - 6t)^2 + 1 = 4$. The smaller root is $t^* = (5 - \sqrt{3}) / 6 \approx 0.545$. For moving spheres, the test is a quadratic equation.

**A vertex and a triangle.** With linear vertices, the four points are coplanar exactly when a triple product is zero, and this is a cubic polynomial in $t$. The page on [elementary CCD tests](/elementary-ccd-tests/) works through one cubic with two roots in the step, where the first root is a coplanar time with the vertex outside the triangle, and the second root at $t = 0.8$ is the contact.

## Known algorithms

**Elementary tests for meshes.** For linear vertices, the [elementary CCD tests](/elementary-ccd-tests/) solve the cubic of a vertex and a triangle, or of two edges, and check the geometry at each root in increasing order. Provot (1997) used them for cloth. Brochu, Edwards and Bridson (2012) gave an exact version based on the parity of root crossings, and Wang and others (2021) compared many versions on a large benchmark and gave a conservative method based on inclusion. [Robust cloth collision](/robust-cloth-collision/) and [impact zones](/impact-zones/) build on these tests.

**Conservative advancement.** For rigid convex objects under any motion with a known bound on the speed, [conservative advancement](/conservative-advancement/) measures the distance, advances the time by the distance divided by the speed bound, and repeats. It never steps past the first contact and needs only a distance query, such as [GJK](/gjk-algorithm/). Tang, Kim and Manocha (2009) applied it to general polygonal models with a bounding volume hierarchy.

**Ray casting on the Minkowski difference.** If two convex objects only translate, the relative motion is a line, and the time of impact is the first time that the moving origin enters $A - B$, the [Minkowski difference](/minkowski-sum/). A ray cast against $A - B$ with support functions finds it.

**Closed forms for simple shapes.** Moving spheres and capsules, a moving sphere against a plane, and moving boxes along a line have closed forms or short interval tests, as in the examples above.

**Interval and root isolation methods.** For rigid motion in which the angle grows at a constant rate, the contact conditions contain sines and cosines of $t$ and are not polynomial. Methods based on [interval arithmetic](/interval-arithmetic/) bound the conditions on subintervals of time and split the intervals that may hold a root, in the manner of the [bisection method](/bisection-method/), so that no contact is lost.

## Bounds

With linear vertices, each elementary test is a cubic equation and takes $O(1)$ arithmetic operations in exact arithmetic, for example with a [Sturm sequence](/sturm-sequence/) to isolate the roots. Two meshes with $n$ and $m$ primitives need $O(n m)$ elementary tests in the worst case, and any method that reports all contacts needs time at least the number of contacts, which can be $\Theta(n m)$. Conservative advancement takes a number of steps that depends on the distance tolerance and the speed bound, not on the sizes of the objects. Its time is the number of steps times the cost of one distance query.

## Reductions

- **To root finding.** With linear vertices, CCD of two meshes reduces to finding the smallest root in $[0, 1]$ of cubic polynomials, one for each candidate pair of primitives, with a check at each root. See [polynomial root finding](/polynomial-root-finding/).
- **To distance queries.** For rigid convex objects, conservative advancement reduces CCD to a sequence of distance queries.
- **To a ray cast.** For two translating convex objects, CCD is a ray cast of the origin against their Minkowski difference.
- **From static detection.** A static [collision detection](/collision-detection/) test is CCD with a motion that does not move, so CCD is at least as hard.

## Applications

- **Rigid body simulation.** A [rigid body simulator](/rigid-body-simulation-problem/) uses the time of impact to stop fast bodies at the contact, or to order the contacts in a step, so that thin walls and small objects do not let bodies pass through.
- **Cloth and deformable bodies.** Cloth needs all contacts in the step for its self-collisions, and any missed contact leaves the cloth tangled. [Robust cloth collision](/robust-cloth-collision/) and [impact zones](/impact-zones/) use CCD for this.
- **Contact models with barriers.** [Incremental potential contact](/incremental-potential-contact/) limits each step of its line search by the time of impact, so that the state stays free of intersections.
- **Motion planning.** A planner checks that the whole path between two configurations is free, not only the two ends.
- **Games.** Fast projectiles and thin level geometry need CCD for the shots and the bodies that must not tunnel.

## References
