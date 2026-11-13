---
tag: RXK2FN
kind: concept
slug: configuration-space
name: Configuration space
aliases:
- C-space
area: games-and-search/planning
level: core
summary: The space of all robot configurations, in which planning a path reduces to moving a point.
prereqs: [minkowski-sum]
see_also: [motion-planning, minkowski-sum-convex-polygons, cell-decomposition, probabilistic-roadmap, piano-movers-problem, kinodynamic-planning, collision-detection, convex-collision-detection]
sources:
  - paper: doi:10.1109/TC.1983.1676196
    title: Tomás Lozano-Pérez, Spatial planning, a configuration space approach, IEEE Transactions on Computers C-32(2), 1983
    locator: pages 108 to 120 (the configuration space, C-obstacles of a polygon as the set of placements that overlap an obstacle, and their computation for convex polygons)
  - paper: doi:10.1145/359156.359164
    title: Tomás Lozano-Pérez and Michael A. Wesley, An algorithm for planning collision-free paths among polyhedral obstacles, Communications of the ACM 22(10), 1979
    locator: pages 560 to 570 (the grown obstacles of a translating robot and the visibility graph of their vertices)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 4.2 (SE(2), SE(3) and the configuration spaces of chains), Section 4.3 (configuration space obstacles, with the translational case in Section 4.3.2 and the general case in Section 4.3.3)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 3 (configuration space, its topology and the C-obstacles of a translating polygon)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 13 (robot motion planning, with the configuration space of a translating robot and the Minkowski sum; section numbers not checked)
---

The configuration space of a robot is the set of all its placements, with one coordinate for each degree of freedom. In this space the robot is a single point, and each obstacle becomes a *C-obstacle*, the set of placements in which the robot touches the obstacle. A [motion planning](/motion-planning/) problem then asks for a path of a point in the free space, the part outside all C-obstacles. Lozano-Pérez made the idea the base of planning in 1979 and 1983, and nearly every planner since works in this space.

## In plain words

A robot can have a complex shape, and it can turn and bend. That makes it hard to say which motions hit a wall. So we change the view. We list all the numbers that fix the robot's placement, for example its position and its angle. Each list of numbers is one point in a new space. Moving the robot is moving that point.

Then we paint, in this new space, every point where the robot would touch something. The painted parts are the obstacles of the new space. Now the planner only has to move one point through the unpainted part. This is the same for a small vacuum robot, a car or an arm with six joints. Only the number of coordinates changes.

## The idea

**Configurations.** A *configuration* $q$ of a robot $\mathcal{A}$ fixes the position of every point of $\mathcal{A}$ in the workspace $\mathcal{W}$. We write $\mathcal{A}(q) \subset \mathcal{W}$ for the set of points that the robot covers at $q$. The set $\mathcal{C}$ of all configurations is the *configuration space*. Its dimension $d$ is the number of degrees of freedom.

**Topology.** The space $\mathcal{C}$ is a manifold, and it is often not a box in $\mathbb{R}^d$.

| robot | configuration space | dimension |
|---|---|---|
| point or translating body in the plane | $\mathbb{R}^2$ | 2 |
| translating body in space | $\mathbb{R}^3$ | 3 |
| rigid body in the plane, with rotation | $SE(2) = \mathbb{R}^2 \times S^1$ | 3 |
| rigid body in space | $SE(3) = \mathbb{R}^3 \times SO(3)$ | 6 |
| arm with $k$ revolute joints | the torus $T^k = S^1 \times \cdots \times S^1$ | $k$ |
| car-like robot in the plane | $\mathbb{R}^2 \times S^1$, with constraints on the velocity | 3 |

The angle coordinates wrap around. A planner that stores an angle as a number in $[0, 2\pi)$ must treat $0$ and $2\pi$ as the same point, and must measure the distance between angles the short way around the circle. The space $SO(3)$ of rotations is not a product of three circles. It is often stored with unit quaternions, where $u$ and $-u$ give the same rotation.

**C-obstacles and free space.** For closed obstacles $\mathcal{O} \subset \mathcal{W}$,

$$\mathcal{C}_{obs} = \{ q \in \mathcal{C} : \mathcal{A}(q) \cap \mathcal{O} \neq \emptyset \}, \qquad \mathcal{C}_{free} = \mathcal{C} \setminus \mathcal{C}_{obs}.$$

A collision-free motion of the robot is the same as a continuous path in $\mathcal{C}_{free}$. With closed obstacles, $\mathcal{C}_{obs}$ is closed and $\mathcal{C}_{free}$ is open. Some books also allow contact and plan in the closure of $\mathcal{C}_{free}$. Then a path may touch the obstacles, as the shortest paths of the [visibility graph](/visibility-graph/) do.

**The translating case.** Let the robot be given in its own frame, with a reference point at the origin, and let $q \in \mathbb{R}^2$ be a translation, so $\mathcal{A}(q) = \mathcal{A} + q$. Then $\mathcal{A}(q)$ meets an obstacle $\mathcal{O}_i$ if and only if there are $a \in \mathcal{A}$ and $o \in \mathcal{O}_i$ with $a + q = o$, that is, $q = o - a$. So

$$\mathcal{C}_{obs,i} = \mathcal{O}_i \oplus (-\mathcal{A}) = \{ o - a : o \in \mathcal{O}_i,\ a \in \mathcal{A} \},$$

the [Minkowski sum](/minkowski-sum/) of the obstacle and the robot reflected through its reference point. For two convex polygons with $m$ and $k$ vertices, the sum is a convex polygon with at most $m + k$ vertices, and the [merge of the edge directions](/minkowski-sum-convex-polygons/) computes it in $O(m + k)$ time. For a nonconvex robot or obstacle, split it into convex parts and take the union of the sums. The union of the C-obstacles of a convex robot among disjoint polygons with $n$ vertices in total has $O(n)$ edges, because the C-obstacles of disjoint convex obstacles form a family of pseudodisks (de Berg et al., Chapter 13). The geometry pages give the sum and its computation. This page uses only the result.

**Rotation.** If the robot also rotates, the C-obstacle is a solid in $\mathbb{R}^2 \times S^1$. Each slice at a fixed angle $\theta$ is the Minkowski sum for the robot rotated by $\theta$. The surfaces of the solid are no longer flat, and exact methods describe them by polynomial constraints after a change of variable such as $t = \tan(\theta/2)$. This is the setting of the [piano movers' problem](/piano-movers-problem/).

**Implicit representation.** For more than three degrees of freedom nobody builds $\mathcal{C}_{obs}$ explicitly. A planner instead asks a collision checker whether one configuration $q$ is free, or whether the segment from $q$ to $q'$ is free. The checker places the robot in the workspace and runs a [collision detection](/collision-detection/) test, for example [GJK](/gjk-algorithm/) on convex parts. Sampling planners such as the [probabilistic roadmap](/probabilistic-roadmap/) are built on this view.

**Distance.** A planner needs a metric on $\mathcal{C}$ to pick near configurations. For $SE(2)$ a common choice is $\sqrt{\Delta x^2 + \Delta y^2 + w^2 \Delta\theta^2}$, where $\Delta\theta$ is taken the short way and $w$ is a length that weights rotation against translation. There is no natural choice of $w$, and the choice changes the behavior of the planner.

## Examples

**A square that translates past a triangle.** The robot is the unit square with corners $(0, 0)$, $(1, 0)$, $(1, 1)$ and $(0, 1)$, and its reference point is its lower-left corner. The obstacle is the triangle with corners $(3, 2)$, $(5, 2)$ and $(4, 4)$. The reflected robot $-\mathcal{A}$ is the square from $(-1, -1)$ to $(0, 0)$. The Minkowski sum of the triangle and this square is the hexagon

$$(2, 1),\ (5, 1),\ (5, 2),\ (4, 4),\ (3, 4),\ (2, 2).$$

The triangle has area 2, and the hexagon has area 7. For example, the placement $q = (2, 1)$ puts the upper-right corner of the square at $(3, 2)$, the left corner of the triangle, so the square just touches the obstacle. The placement $q = (4.5, 3.5)$ is outside the hexagon, and the square from $(4.5, 3.5)$ to $(5.5, 4.5)$ does not meet the triangle. If the reference point is the center of the square, the robot is the square from $(-1/2, -1/2)$ to $(1/2, 1/2)$, and the same hexagon moves by $(1/2, 1/2)$. The choice of reference point moves the C-obstacles but does not change which motions are free.

**A two-link arm.** The arm has its base at the origin and two links of length 1. Its configuration is the pair of joint angles $(\theta_1, \theta_2)$, so $\mathcal{C}$ is the torus $T^2$. The obstacle is the square $[0.6, 1.6]^2$. We test each of the $72 \times 72$ angle pairs $(2\pi i/72, 2\pi j/72)$: a pair is free when neither link segment meets the square. 4498 of the 5184 pairs are free.

| grid treated as | connected pieces of free pairs |
|---|---|
| a torus (angles wrap around) | 1 |
| a square (no wrap) | 3 |

The free space is one connected region on the torus. A planner that forgets the wrap sees three pieces, and it would report that no motion exists between configurations that are in fact connected.

**A rotating ladder.** A ladder in a corridor that turns a corner may pass only if it rotates while it moves. In $\mathbb{R}^2$ alone no path exists for the fixed angle, but in $SE(2)$ one does. The extra coordinate is what makes the path possible.

## Where it is used

- **Exact planners.** [Cell decomposition](/cell-decomposition/) and the roadmap methods of the [piano movers' problem](/piano-movers-problem/) work on an explicit description of $\mathcal{C}_{free}$.
- **Shortest paths for a translating robot.** Grow the obstacles by the reflected robot, then run the [visibility graph](/visibility-graph/) method on the grown obstacles. This is the method of Lozano-Pérez and Wesley.
- **Sampling planners.** The [probabilistic roadmap](/probabilistic-roadmap/), [RRT](/rapidly-exploring-random-tree/) and [RRT*](/rrt-star/) sample $\mathcal{C}$ and use a collision checker as an oracle for $\mathcal{C}_{free}$.
- **Potential fields.** The [potential field method](/potential-field-method/) defines its field on $\mathcal{C}$, with repulsion from the C-obstacles.
- **Planning with dynamics.** [Kinodynamic planning](/kinodynamic-planning/) works in the state space, which adds the velocities to the configuration.

## References
