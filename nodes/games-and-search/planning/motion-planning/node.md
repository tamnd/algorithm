---
tag: B8FG01
kind: problem
slug: motion-planning
name: Motion planning
aliases:
- path planning
- robot motion planning
area: games-and-search/planning
level: core
summary: Find a collision-free path for a robot from a start configuration to a goal configuration.
prereqs: [configuration-space]
see_also: [piano-movers-problem, cell-decomposition, probabilistic-roadmap, rapidly-exploring-random-tree, bug-algorithms, kinodynamic-planning, visibility-graph, a-star-search]
sources:
  - book: isbn:9780792391296
    title: Jean-Claude Latombe, Robot Motion Planning, Kluwer Academic Publishers, 1991
    locator: Chapter 1 (the basic motion planning problem and its extensions); later chapters cover roadmaps, cell decomposition and potential fields (general locator)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 4.3 (configuration space obstacles and the definition of the problem), Chapter 5 (sampling-based planning, resolution and probabilistic completeness), Chapter 6 (combinatorial planning, Section 6.5 on the complexity of motion planning)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 1 (introduction and the notions of completeness), Chapters 2 to 7 (bug algorithms, configuration space, potential functions, roadmaps, cell decompositions, sampling-based algorithms)
  - paper: doi:10.1109/SFCS.1979.10
    title: John H. Reif, Complexity of the mover's problem and generalizations, 20th Annual Symposium on Foundations of Computer Science (FOCS), 1979
    locator: pages 421 to 427 (the generalized mover's problem is PSPACE-hard)
  - book: isbn:9780262031363
    title: John F. Canny, The Complexity of Robot Motion Planning, MIT Press, 1988
    locator: the roadmap algorithm, singly exponential in the dimension, and the PSPACE upper bound (general locator)
  - paper: doi:10.1109/SFCS.1987.42
    title: John Canny and John Reif, New lower bound techniques for robot motion planning problems, 28th Annual Symposium on Foundations of Computer Science (FOCS), 1987
    locator: pages 49 to 60 (shortest paths among polyhedra in three dimensions are NP-hard)
---

Motion planning asks for a path that moves a robot from a start placement to a goal placement without a collision with the obstacles. The standard form of the problem lives in the [configuration space](/configuration-space/) of the robot, where the robot is a point and the obstacles become forbidden regions. For a robot with $d$ degrees of freedom and obstacles of total complexity $n$, exact algorithms take time polynomial in $n$ for fixed $d$ but exponential in $d$, and the general problem is PSPACE-hard. This page is about the problem, its variants and its hardness. The methods that solve it have their own pages.

## In plain words

A robot stands in a room with furniture. You know the shape of the robot, the shape of the furniture, where the robot is now and where it must go. You must find a way to move the robot there so that it never touches the furniture. The robot can turn, slide and bend its joints, so it is more than a point on a floor plan.

A good answer has two parts. If a way exists, the method must find one. If no way exists, the method must say so. Some methods only give the first part. Others give it only when the open space is not too thin, or only with high probability when they try many random placements.

## Definition

**The model.** A robot $\mathcal{A}$ moves in a workspace $\mathcal{W} = \mathbb{R}^2$ or $\mathbb{R}^3$ that holds closed obstacles $\mathcal{O}$. A *configuration* $q$ gives the placement of every point of the robot. The set of all configurations is the configuration space $\mathcal{C}$, a manifold of dimension $d$, the number of degrees of freedom. The configuration $q$ is in collision when $\mathcal{A}(q) \cap \mathcal{O} \neq \emptyset$. The set of these is the C-obstacle $\mathcal{C}_{obs}$, and $\mathcal{C}_{free} = \mathcal{C} \setminus \mathcal{C}_{obs}$ is the free space. When the obstacles and the robot are semi-algebraic, $\mathcal{C}_{obs}$ is described by $n$ polynomial constraints of degree at most $p$. We call $n$ the complexity of the obstacles.

**Input.** The robot, the obstacles, a start configuration $q_I \in \mathcal{C}_{free}$ and a goal configuration $q_G \in \mathcal{C}_{free}$.

**Output.** A continuous path $\tau : [0, 1] \to \mathcal{C}_{free}$ with $\tau(0) = q_I$ and $\tau(1) = q_G$, or the answer that no such path exists. The decision version asks only whether $q_I$ and $q_G$ lie in the same path-connected component of $\mathcal{C}_{free}$.

**What a method promises.** The promises differ, and each method page states which one holds.

- **Complete.** The method returns a path when one exists and reports failure otherwise, in finite time. Exact cell decompositions and roadmap algorithms are complete.
- **Resolution complete.** The method works on a grid or a cell tree at a resolution $h$. It is complete for the problem seen at resolution $h$: it finds a path when one exists with clearance larger than a constant times $h$, and it reports failure otherwise. A failure says nothing about thinner passages.
- **Probabilistically complete.** The method samples configurations. If a path exists, the probability that the method has found one after $N$ samples tends to 1 as $N \to \infty$. If no path exists, the method runs forever. The rate of convergence depends on the free space: on the clearance $\delta$ of a solution path, or on how *expansive* the free space is.

**Collision checking.** Almost every method touches the geometry only through two calls: is the configuration $q$ free, and is the straight segment from $q$ to $q'$ free. In practice these calls are the dominant cost of a planner, and the measured cost of a sampling method is the number of such calls.

## Variants

- **Point robot in the plane.** The robot is a point and the obstacles are polygons. A shortest path follows the [visibility graph](/visibility-graph/) and is a [Euclidean shortest path](/euclidean-shortest-path/). Inside one simple polygon see [shortest paths in a polygon](/euclidean-shortest-path-in-polygon/).
- **Translating robot.** A rigid polygon that only translates has $\mathcal{C} = \mathbb{R}^2$. Each C-obstacle is a [Minkowski sum](/minkowski-sum/) of an obstacle and the reflected robot, so the problem reduces to the point robot.
- **Rigid body with rotation.** In the plane $\mathcal{C} = SE(2)$, of dimension 3. In space $\mathcal{C} = SE(3)$, of dimension 6.
- **Articulated robots.** An arm with $k$ revolute joints has the torus $T^k$ as its configuration space.
- **The piano mover's problem.** The general decision problem for a rigid or linked body among polyhedra, studied for its complexity. See [piano movers' problem](/piano-movers-problem/).
- **Many robots.** Several robots move at the same time and must avoid each other. The configuration space is the product of the single spaces. The graph version is [multi-agent pathfinding](/multi-agent-pathfinding/).
- **Optimal planning.** Find a path of least cost, for example of least length. Sampling methods that converge to the optimum are [RRT*](/rrt-star/) and PRM*.
- **Kinodynamic planning.** The robot has velocity and acceleration bounds or other differential constraints. See [kinodynamic planning](/kinodynamic-planning/).
- **Unknown obstacles.** The robot learns the obstacles only by its sensors while it moves. The [Bug algorithms](/bug-algorithms/) work in this setting. On a grid, incremental replanning with [D* Lite](/d-star-lite/) is common.
- **Grid pathfinding.** The free space is given as a grid of cells. This is a graph search problem, solved by [A*](/a-star-search/) and its relatives. It is a discrete model, not a geometric one.

## Examples

**A translating square.** A unit square robot with its reference point at its lower-left corner moves among triangles. The C-obstacle of the triangle with corners $(3, 2)$, $(5, 2)$ and $(4, 4)$ is the hexagon with corners $(2, 1)$, $(5, 1)$, $(5, 2)$, $(4, 4)$, $(3, 4)$ and $(2, 2)$. The triangle has area 2 and the hexagon has area 7. A path of the reference point that avoids the hexagons is a free motion of the square. The [configuration space](/configuration-space/) page computes this.

**A two-link arm.** A planar arm with two unit links and its base at the origin has the torus of joint angles as its configuration space. A square obstacle $[0.6, 1.6]^2$ blocks some angle pairs. On a $72 \times 72$ grid of angle pairs, 4498 pairs are free. On the torus they form one connected region. If you forget that angle $2\pi$ equals angle $0$ and treat the grid as a square, the same free pairs fall into 3 pieces, and a planner on the square would report wrong failures.

**No path.** A point robot in the plane with its goal inside a closed ring of obstacles has no path. A complete method reports this. A sampling method never stops by itself. The [Bug algorithms](/bug-algorithms/) report it after they follow the outer boundary of the ring.

## Known algorithms

| method | promise | cost | page |
|---|---|---|---|
| visibility graph and Dijkstra | complete, optimal for a point among polygons | $O(n^2 \log n)$ time; a shortest path alone takes $O(n \log n)$ by other methods | [visibility graph](/visibility-graph/), [Euclidean shortest path](/euclidean-shortest-path/) |
| exact cell decomposition | complete | $O(n \log n)$ for a point among polygons; doubly exponential in $d$ in general | [cell decomposition](/cell-decomposition/), [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) |
| Canny's roadmap algorithm | complete | polynomial in $n$ for fixed $d$, singly exponential in $d$ | [piano movers' problem](/piano-movers-problem/) |
| approximate cell decomposition | resolution complete | exponential in $d$ at a fixed resolution | [cell decomposition](/cell-decomposition/) |
| potential fields | not complete (local minima) | per step, the cost of a distance query | [potential field method](/potential-field-method/) |
| Bug1, Bug2 | complete for a point in the plane with contact sensing | path length at most $D + 1.5 \sum p_i$ (Bug1) | [Bug algorithms](/bug-algorithms/) |
| probabilistic roadmap | probabilistically complete | no worst-case bound; measured in collision checks | [probabilistic roadmap](/probabilistic-roadmap/) |
| RRT and RRT-Connect | probabilistically complete | no worst-case bound | [RRT](/rapidly-exploring-random-tree/), [RRT-Connect](/rrt-connect/) |
| RRT*, PRM* | probabilistically complete and asymptotically optimal | $O(\log N)$ expected neighbors per sample | [RRT*](/rrt-star/), [asymptotic optimality](/rrt-star-asymptotic-optimality/) |

Exact methods give the strongest promise, but their cost grows so fast with $d$ that they are used only for $d \le 3$ or for special robots. Sampling methods work in tens of dimensions in practice. The price is that they cannot prove that no path exists.

## Bounds

- **Lower bounds.** Reif proved in 1979 that the generalized mover's problem, for a robot made of many linked polyhedra that moves among polyhedra in three dimensions, is PSPACE-hard. Hopcroft, Schwartz and Sharir proved in 1984 that the warehouseman's problem, for many rectangles in a rectangular box, is PSPACE-hard. So no algorithm polynomial in $d$ is expected. Canny and Reif proved in 1987 that the shortest path problem for a point among polyhedra in three dimensions is NP-hard. In the plane the shortest path is easy.
- **Upper bounds.** Schwartz and Sharir solved the general problem in 1983 with a [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/). Their time is polynomial in $n$ for fixed $d$ and doubly exponential in $d$. Canny's roadmap algorithm of 1988 is singly exponential in $d$ and puts the decision problem in [PSPACE](/pspace/). With the lower bound, the generalized problem is PSPACE-complete.
- **Sampling methods.** No worst-case bound on the number of samples holds, because a passage can be as thin as you like. The bounds that hold are in probability. For a path of clearance $\delta$ and length $L$, the failure probability of the probabilistic roadmap falls exponentially in the number of samples, with a rate that depends on $\delta$ and $L$ (Kavraki, Kolountzakis and Latombe 1998). These are the proved bounds. Running times of planners on benchmark scenes are measured numbers.

## Reductions

- A translating polygon among polygons reduces to a point among the C-obstacles, by the [Minkowski sum](/minkowski-sum/).
- The decision problem reduces to [graph reachability](/graph-reachability/) on a finite graph whenever a complete decomposition or roadmap of $\mathcal{C}_{free}$ exists. All complete methods follow this plan. They differ in how they build the graph.
- PSPACE-hardness is shown by a reduction from polynomial-space [Turing machines](/turing-machine/). The robot has many linked parts, and the obstacles are built so that the free motions of the parts copy the steps of the machine. The goal is free to reach exactly when the machine accepts.

## Applications

Industrial arms plan their motions between tasks. Mobile robots and cars plan paths among parked objects. Animation and games move characters and cameras. Computer-aided design checks that a part can be put in or taken out of an assembly. Computational biology uses the same methods to search for the folding paths of molecules and the binding paths of ligands.

## References
