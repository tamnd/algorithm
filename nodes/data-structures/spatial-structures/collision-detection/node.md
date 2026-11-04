---
tag: EQYZ8S
kind: problem
slug: collision-detection
name: Collision detection
aliases:
- broad-phase collision detection
- narrow-phase collision detection
area: data-structures/spatial-structures
level: core
summary: Determine which pairs of moving objects intersect, usually filtered by a broad phase that uses bounding volumes.
prereqs: [minimum-bounding-rectangle, bounding-volume]
see_also: [convex-collision-detection, rectangle-intersection-reporting, bounding-volume-hierarchy, uniform-grid, spatial-hashing, gjk-algorithm, separating-axis-theorem, loose-octree]
sources:
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 2 (the design of a collision system, broad phase and narrow phase), Chapter 4 (bounding volumes), Chapters 6 and 7 (bounding volume hierarchies and spatial partitioning, with grids, trees and sort and sweep)
  - paper: doi:10.1145/199404.199437
    title: Jonathan D. Cohen, Ming C. Lin, Dinesh Manocha and Madhav K. Ponamgi, I-COLLIDE, an interactive and exact collision detection system for large-scale environments, Proceedings of the 1995 Symposium on Interactive 3D Graphics
    locator: the sweep and prune of the bounding boxes, kept sorted from frame to frame by insertion sort
  - paper: "Jon L. Bentley and Derick Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7), 1980"
    locator: the O(n log n + k) algorithm for reporting all intersecting pairs of n axis-parallel rectangles
  - paper: "Elmer G. Gilbert, Daniel W. Johnson and S. Sathiya Keerthi, A fast procedure for computing the distance between complex objects in three-dimensional space, IEEE Journal of Robotics and Automation 4(2), 1988"
    locator: the distance algorithm for convex objects, used as the narrow phase
---

Collision detection is the problem of finding which pairs of objects in a scene intersect, either at one moment or during a time step. A scene of $n$ objects has $\binom{n}{2}$ pairs, so the standard solution has two phases: a *broad phase* that uses cheap [bounding volumes](/bounding-volume/), usually [bounding boxes](/minimum-bounding-rectangle/), to find a small set of candidate pairs, and a *narrow phase* that runs an exact test on each candidate. The broad phase uses a spatial structure: a sorted list (sweep and prune), a [uniform grid](/uniform-grid/), [spatial hashing](/spatial-hashing/), or a tree such as a [bounding volume hierarchy](/bounding-volume-hierarchy/). Physics engines, games, robotics and CAD all solve it many times each second.

## In plain words

You have a box of moving toys, and you want to know which toys touch. Comparing the exact shapes of each pair of toys takes too long when there are many toys.

So you first put each toy in the smallest box that holds it. Two boxes that do not touch cannot hold toys that touch, and a box test is fast. You then look only at the toys whose boxes touch, and compare their exact shapes. To avoid testing every pair of boxes, you sort the boxes from left to right, and compare a box only with the boxes that start before it ends. Since the toys move only a little between two frames, the order of the boxes changes little, and keeping it sorted is cheap.

## Definition

**Input.** A set of objects $o_1, \ldots, o_n$, each a closed bounded set in $\mathbb{R}^d$ with $d = 2$ or $3$. In the dynamic form, each object has a motion $o_i(t)$ for $t$ in a time interval.

**Output (discrete form).** The set of colliding pairs at one time,
$$K = \{\{i, j\} : i \ne j,\ o_i \cap o_j \ne \emptyset\},$$
with $k = |K|$.

**The two phases.** A *broad phase* computes a set $C$ of pairs with $K \subseteq C$. It must never miss a pair; it may report pairs that do not collide. A *narrow phase* tests each pair of $C$ exactly and returns $K$. With bounding volumes $b_i \supseteq o_i$, the rule "keep $\{i, j\}$ when $b_i \cap b_j \ne \emptyset$" gives a valid $C$, because $o_i \cap o_j \subseteq b_i \cap b_j$.

**Output (continuous form).** For two moving objects, the least time $t \in [0, 1]$ with $o_i(t) \cap o_j(t) \ne \emptyset$, or "none". This is the *time of impact*, and it prevents a fast object from passing through a thin one between two frames.

## Variants

- **Decision.** Is any pair of objects in contact? This is the question of a motion planner that checks one configuration.
- **Reporting.** List all of $K$. This is the form that a physics engine needs, since it must respond to each contact.
- **Pair query.** Do two given objects intersect, and if not, how far apart are they? The convex case is [convex collision detection](/convex-collision-detection/).
- **One against many.** Which objects does one query object (a ray, a moving character) hit? This is a range query on a [spatial index](/spatial-index/).
- **Self-collision.** The parts of one deformable object, such as cloth, against each other.
- **Contact data.** Beyond yes or no, the narrow phase may return the contact points, the normal and the depth of penetration, which the physics solver needs.

## Examples

**Sweep and prune.** Six boxes in the plane, each written as $[x_0, x_1] \times [y_0, y_1]$:

| box | $x$ interval | $y$ interval |
|---|---|---|
| A | [0, 3] | [0, 2] |
| B | [2, 5] | [1, 4] |
| C | [4, 7] | [5, 7] |
| D | [6, 8] | [0, 3] |
| E | [7, 9] | [2, 6] |
| F | [1, 3] | [6, 8] |

Sort the boxes by $x_0$: A, F, B, C, D, E. Scan them in that order with an *active list* of the boxes whose $x$ interval is still open. At each new box, drop each active box whose $x_1$ is less than the new $x_0$, pair the new box with each box that remains, and then add it.

| new box | dropped | active before | new candidate pairs |
|---|---|---|---|
| A ($x_0 = 0$) | | none | none |
| F (1) | | A | A-F |
| B (2) | | A, F | A-B, F-B |
| C (4) | A, F | B | B-C |
| D (6) | B | C | C-D |
| E (7) | | C, D | C-E, D-E |

The $x$ sweep keeps 7 of the 15 pairs. The test of the $y$ intervals then keeps A-B, C-E and D-E, which are exactly the pairs of boxes that intersect. The narrow phase runs on these 3 pairs, not on 15.

**A false candidate.** Two parallel rods along $y = x$ and $y = x + 1$, each from $x = 0$ to $x = 10$, have boxes that overlap in $[0, 10] \times [1, 10]$, and the rods never touch. The broad phase passes this pair, and the narrow phase rejects it.

**Tunneling.** A ball of radius 0.1 moves from $x = 0$ to $x = 1$ in one step, and a wall fills $0.5 \le x \le 0.55$. At the two sample times the ball does not touch the wall, so the discrete form finds no collision. The swept volume of the ball over the step, a capsule from $x = -0.1$ to $x = 1.1$, meets the wall, and the continuous form finds the contact at $t = 0.4$, when the front of the ball reaches $x = 0.5$.

## Known algorithms

**Broad phase.**

- **All pairs.** Test each of the $\binom{n}{2}$ pairs of boxes: $\Theta(n^2)$ time. Fast for a few dozen objects.
- **Sweep and prune** (sort and sweep). Sort the box intervals on one axis and report the pairs that overlap there, then test the other axes. It takes $O(n \log n + k_x)$ time, where $k_x$ is the number of pairs whose intervals overlap on the sweep axis. Between frames, the sorted order changes little, so [insertion sort](/insertion-sort/) restores it in $O(n + s)$ time, where $s$ is the number of swaps; this is the method of I-COLLIDE. It degrades when many objects line up on the sweep axis.
- **Optimal rectangle reporting.** In the plane, all $k$ intersecting pairs of $n$ axis-parallel rectangles can be reported in $O(n \log n + k)$ time by a [sweep line](/sweep-line-technique/) with a segment tree or an interval tree (Bentley and Wood, 1980). See [rectangle intersection reporting](/rectangle-intersection-reporting/) and the [rectangle intersection sweep](/rectangle-intersection-sweep/).
- **Uniform grid** and **spatial hashing.** Put each box in the grid cells it meets, and test pairs that share a cell. When each object meets $O(1)$ cells and each cell holds $O(1)$ objects, the time is $O(n)$, expected when the cells are kept in a hash table. This holds when the objects have about the size of a cell and do not crowd. See [uniform grid](/uniform-grid/) and [spatial hashing](/spatial-hashing/).
- **Trees.** A [bounding volume hierarchy](/bounding-volume-hierarchy/) tested against itself, an [octree](/octree/), a [loose octree](/loose-octree/), or a [k-d tree](/kd-tree/). Trees handle objects of very different sizes better than a grid.

**Narrow phase.**

- For convex polytopes, the [GJK algorithm](/gjk-algorithm/) computes the distance through the Minkowski difference, and the [separating axis theorem](/separating-axis-theorem/) gives a finite set of axes to test for boxes and polyhedra.
- For non-convex meshes, a bounding volume hierarchy of each mesh, tested tree against tree, down to triangle pairs.

## Bounds

- **Output.** Any algorithm that reports $K$ takes $\Omega(k)$ time, and $k$ can be $\binom{n}{2}$, for example when all objects contain one common point.
- **Lower bound for the decision form.** In the [algebraic decision tree](/algebraic-decision-tree/) model, deciding whether any two of $n$ intervals on a line intersect takes $\Omega(n \log n)$ operations in the worst case, by the reduction from element distinctness below. So $\Omega(n \log n + k)$ is a lower bound for reporting, and the sweep of Bentley and Wood meets it for rectangles in the plane.
- **Practice.** The worst-case bounds hide the fact that real scenes have coherence: objects move little between frames. Methods that update the previous answer, such as sweep and prune with insertion sort, take close to linear time per frame on such scenes, with no worst-case guarantee.

## Reductions

- **From element distinctness.** Given numbers $x_1, \ldots, x_n$, make the degenerate intervals $[x_i, x_i]$. Two of them intersect exactly when two numbers are equal. The reduction takes $O(n)$ time, so the $\Omega(n \log n)$ lower bound of [element distinctness](/element-distinctness/) in the algebraic decision tree model ([Ben-Or's theorem](/ben-or-theorem/)) carries over to the decision form of collision detection.
- **To pair tests.** The broad phase reduces the problem to $|C|$ instances of the pair query, which is a [convex collision detection](/convex-collision-detection/) problem when the objects are convex or are split into convex pieces.
- **Continuous to static.** For a translation of an object $A$ by a vector $v$ during the step, $A$ and a fixed object $B$ collide during the step exactly when the swept set $\{a + tv : a \in A, t \in [0, 1]\}$ meets $B$. For convex objects this is a static test of a convex set against $B$, which a [Minkowski sum](/minkowski-sum/) also expresses.

## Applications

- Physics engines for games and simulation, which run a broad phase and a narrow phase in each frame.
- [Motion planning](/motion-planning/) in robotics, where each sample of the [configuration space](/configuration-space/) needs a collision test.
- CAD and assembly, to check that parts do not interpenetrate.
- Cloth and hair simulation, with many self-collisions.
- Molecular and particle simulation, where a grid of cells finds the pairs of particles within a cutoff distance.

## References
