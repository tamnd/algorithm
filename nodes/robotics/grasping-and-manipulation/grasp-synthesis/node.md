---
tag: YWQQFV
kind: problem
slug: grasp-synthesis
name: Grasp synthesis
aliases:
- grasp planning
area: robotics/grasping-and-manipulation
level: core
summary: Choose contact points on an object, or a hand pose, that give a force-closure grasp of good quality.
prereqs: [force-closure, grasp-quality-measures]
see_also: [independent-contact-regions, antipodal-grasp, ferrari-canny-metric, force-closure-test, caging-grasp, in-hand-manipulation, inverse-kinematics, grasp]
sources:
  - paper: doi:10.1109/TRO.2013.2289018
    title: Jeannette Bohg, Antonio Morales, Tamim Asfour and Danica Kragic, Data-driven grasp synthesis, a survey, IEEE Transactions on Robotics 30(2), 289-309, 2014
    locator: the whole paper (a survey of analytic and data-driven methods of grasp synthesis)
  - paper: doi:10.1177/027836498800700301
    title: Van-Duc Nguyen, Constructing force-closure grasps, The International Journal of Robotics Research 7(3), 3-16, 1988
    locator: the whole paper (force-closure grasps by two fingers with friction in the plane, and independent regions of contact)
  - paper: doi:10.1177/027836499701600102
    title: Jean Ponce, Steve Sullivan, Attawith Sudsang, Jean-Daniel Boissonnat and Jean-Pierre Merlet, On computing four-finger equilibrium and force-closure grasps of polyhedral objects, The International Journal of Robotics Research 16(1), 11-35, 1997
    locator: the whole paper (contact regions on the faces of a polyhedron for four-finger grasps)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: the chapter on grasping
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 12 (grasping and manipulation, form and force closure)
---

Grasp synthesis is the problem of choosing where a robot hand should touch an object so that it can hold it. At the level of contacts, the answer is a set of points on the object's surface that give a [force-closure](/force-closure/) grasp, often the best one under a quality measure. At the level of the hand, the answer is a pose of the hand and its fingers that reaches those points without collision. The name has nothing to do with [GRASP](/grasp/), the greedy randomized adaptive search procedure of combinatorial optimization.

## In plain words

You see a mug and reach for it. Before your hand moves, you have chosen where your fingers go: around the body, or through the handle. A robot must make the same choice. It needs places where its fingers can push so that the mug cannot slip out in any direction, and among those, places where small errors and outside pushes do not matter much. Then it needs a hand position that puts the fingers there without hitting the table.

## Definition

An object $O$ with surface $\partial O$, a hand that makes $k$ contacts, and a contact model (for example point contacts with Coulomb friction coefficient $\mu$) are given.

- **Contact-level synthesis.** Find contact points $p_1, \ldots, p_k \in \partial O$ such that the grasp is in force closure: the contact wrenches allowed by the [friction cones](/friction-cone/) positively span the whole wrench space. The *optimal* version maximizes a [grasp quality measure](/grasp-quality-measures/) $Q(p_1, \ldots, p_k)$, such as the [Ferrari-Canny metric](/ferrari-canny-metric/), over force-closure grasps.
- **Hand-level synthesis.** Find a hand pose $T \in SE(3)$ and joint angles $\theta$ such that the fingers touch $O$ at a force-closure set of contacts, the hand does not penetrate $O$ or the environment, and the arm can reach $T$ by [inverse kinematics](/inverse-kinematics/).

The input can be an exact model of $O$ (a polygon, a polyhedron, a mesh) or only sensor data, such as a point cloud from a depth camera.

## Variants

- **Two-finger grasps.** In the plane, two frictional point contacts are in force closure exactly when the line between them lies strictly inside both friction cones, the [antipodal](/antipodal-grasp/) condition (Nguyen 1988). Parallel-jaw grippers use this case.
- **Frictionless grasps.** With no friction the goal is [form closure](/form-closure/), which needs at least four contacts in the plane and seven in space ([finger bounds](/finger-bounds-for-form-closure/)).
- **Robust grasps.** Find regions of contacts instead of points, so that every choice of one point per region gives force closure. These are the [independent contact regions](/independent-contact-regions/) of Nguyen (1988), extended by Ponce and others (1997) to four fingers on a polyhedron.
- **Task-oriented grasps.** The quality is measured against the wrenches that a task needs, such as the torque of a screwdriver, instead of all wrenches.
- **Known, familiar and unknown objects.** Bohg and others (2014) sort data-driven methods by what is known of the object: an exact model, a similar object seen before, or nothing but sensor data.
- **Caging.** Trap the object without holding it still, as a weaker goal or a first step ([caging](/caging-grasp/)).

## Examples

**Two fingers on a rectangle.** Two point fingers with friction $\mu$ touch the two long sides of a rectangle of width $w$, at points whose positions along the sides differ by $\delta$. The line between the fingers makes the angle $\arctan(\delta / w)$ with the normals, so the grasp is in force closure if and only if $\delta / w < \mu$. With $w = 2$ and $\mu = 1/2$, any pair with $\lvert \delta \rvert < 1$ works.

**Independent regions on a square.** On the square with side 2 and $\mu = 1/2$, the largest independent regions on two opposite sides are the open segments of length 1 at the middle of each side, as computed on the [independent contact regions](/independent-contact-regions/) page. A finger anywhere in one and a finger anywhere in the other give force closure.

**A mug from a point cloud.** A depth camera sees part of a mug. A data-driven method samples many candidate parallel-jaw grasps on the visible points, scores each with a learned model, and runs the best one. Nothing is proved about the result; its success rate is measured.

## Known algorithms

- **Force-closure test.** For given contacts with polyhedral friction cones, decide force closure by one [linear feasibility](/linear-feasibility/) problem ([force-closure test](/force-closure-test/)). This is the inner test of many search methods.
- **Analytic construction.** For polygons and two or three fingers, construct force-closure grasps and independent regions from the geometry of the edges and the friction cones (Nguyen 1988). With every pair of edges tried, the regions for two fingers on an $n$-gon take $O(n^2)$ linear programs of constant size ([independent contact regions](/independent-contact-regions/)).
- **Optimization of a quality measure.** Search over contact points, or over hand poses, to maximize a quality measure, with local search, sampling or a grid. The quality measures are not concave in the contact positions, so these methods find good grasps, not provably optimal ones.
- **Sampling and ranking.** Sample many hand poses near the object, keep those that are in force closure and without collision, and rank them. This is simple and works with meshes of any shape.
- **Data-driven methods.** Learn a map from images or point clouds to good grasps, from simulated grasps or from robot trials (Bohg and others 2014). These handle unknown objects, and their results are measurements.

## Bounds

- **Deciding force closure.** For a fixed set of contacts with polyhedral friction cones, force closure is decided by a linear program, so in polynomial time.
- **Existence without friction.** Every planar object other than a disc has a form-closure grasp by four frictionless fingers, and every spatial object other than a surface of revolution has one with seven (the theorem on the [finger bounds](/finger-bounds-for-form-closure/) page).
- **Two-finger regions.** On an $n$-gon, the best pair of independent regions over all pairs of edges takes $O(n^2)$ time in the real RAM (the analysis on the [independent contact regions](/independent-contact-regions/) page).

No complexity bound for the general problem of optimal hand-level synthesis is given here.

## Reductions

- **Force closure to linear feasibility.** With friction cones replaced by [polyhedral cones](/polyhedral-friction-cone/), force closure is the condition that the primitive contact wrenches positively span the wrench space, a linear feasibility problem.
- **Independent regions to linear programming.** For two fingers on two edges of a polygon, the largest regions are the solution of a [linear program](/linear-programming-problem/).
- **Hand-level to motion planning.** Reaching a grasp pose without collision is a query in the [configuration space](/configuration-space/) of the arm and hand.

## Applications

Bin picking and warehouse order picking, where a robot must grasp many unknown objects; assembly, where the grasp fixes the pose of a part for the next step; service robots that handle household objects; and the first step of every [manipulation plan](/manipulation-planning/), which needs a grasp before it can move an object.

## References
