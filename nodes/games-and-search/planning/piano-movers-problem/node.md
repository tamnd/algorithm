---
tag: P9TNC1
kind: problem
slug: piano-movers-problem
name: Piano movers problem
aliases:
- piano mover's problem
area: games-and-search/planning
level: advanced
summary: Decide if a rigid or linked body can move between two placements among polyhedra. PSPACE-hard when the number of parts grows (Reif).
prereqs: [motion-planning, pspace]
see_also: [motion-planning, configuration-space, cylindrical-algebraic-decomposition, cell-decomposition, tarski-seidenberg-theorem, rush-hour-problem, kinodynamic-planning]
sources:
  - paper: doi:10.1109/SFCS.1979.10
    title: John H. Reif, Complexity of the mover's problem and generalizations, 20th Annual Symposium on Foundations of Computer Science (FOCS), 1979
    locator: pages 421 to 427 (the generalized mover's problem, a linked set of polyhedra among polyhedra in three dimensions, is PSPACE-hard)
  - paper: doi:10.1002/cpa.3160360305
    title: Jacob T. Schwartz and Micha Sharir, On the piano movers' problem I, the case of a two-dimensional rigid polygonal body moving amidst polygonal barriers, Communications on Pure and Applied Mathematics 36(3), 1983
    locator: pages 345 to 398 (a polynomial-time exact method for a polygon that translates and rotates among polygons)
  - paper: doi:10.1016/0196-8858(83)90014-3
    title: Jacob T. Schwartz and Micha Sharir, On the piano movers' problem II, general techniques for computing topological properties of real algebraic manifolds, Advances in Applied Mathematics 4(3), 1983
    locator: pages 298 to 351 (the general problem solved with a cylindrical algebraic decomposition, polynomial in the input size for a fixed number of degrees of freedom)
  - paper: doi:10.1177/027836498400300405
    title: John E. Hopcroft, Jacob T. Schwartz and Micha Sharir, On the complexity of motion planning for multiple independent objects; PSPACE-hardness of the warehouseman's problem, International Journal of Robotics Research 3(4), 1984
    locator: pages 76 to 88 (rectangles in a rectangular box, PSPACE-hard)
  - book: isbn:9780262031363
    title: John F. Canny, The Complexity of Robot Motion Planning, MIT Press, 1988
    locator: the roadmap algorithm, singly exponential in the dimension, and the PSPACE upper bound (general locator)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 50, Algorithmic motion planning, by Dan Halperin, Oren Salzman and Micha Sharir, Section 50.1 (Theorem 50.1.2 on the roadmap algorithm and the lower bound on the number of free components)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 6.4.2 (cylindrical algebraic decomposition), Section 6.4.3 (Canny's roadmap algorithm), Section 6.5 (complexity of motion planning)
---

The piano movers' problem asks whether a body can move from one placement to another without a collision, when the body and the obstacles are polyhedra or are described by polynomial inequalities. It is the exact, decision form of [motion planning](/motion-planning/), studied for its complexity and not for a fast planner. For a fixed number $d$ of degrees of freedom it is solvable in time polynomial in the obstacle complexity $n$, and Reif proved that it is PSPACE-hard when the body has many linked parts, so that $d$ grows with the input. Canny's roadmap algorithm puts it in [PSPACE](/pspace/), so the general problem is PSPACE-complete.

## In plain words

You must carry a sofa through the doors and halls of a house. You may slide it and turn it in any way. Is there a way to get it from the living room to the street? The name of the problem comes from this picture.

The question is only yes or no. The answer can turn on small details. A sofa a little too long can fail at one corner, and turning it on its side can save it. For one sofa there is a method that always gives the right answer, and its time grows as a power of the size of the house. When the object has many parts that move on their own, the problem becomes as hard as any puzzle that a computer can solve with a fixed amount of memory.

## Definition

**The model.** The workspace is $\mathbb{R}^2$ or $\mathbb{R}^3$. The obstacles are closed polyhedra, or more generally semi-algebraic sets. The robot is a rigid polyhedron, or a set of polyhedra linked by joints. Its configuration space $\mathcal{C}$ has dimension $d$, the number of degrees of freedom. After a change of variables that turns angles into algebraic coordinates, such as $t = \tan(\theta / 2)$, the free space $\mathcal{C}_{free}$ is a semi-algebraic set described by $n$ polynomial constraints of degree at most $p$ in $d$ variables. The size of the input is measured by $n$, $p$ and $d$.

**Input.** The robot, the obstacles, and two configurations $q_I, q_G \in \mathcal{C}_{free}$.

**Question.** Is there a continuous path $\tau : [0, 1] \to \mathcal{C}_{free}$ with $\tau(0) = q_I$ and $\tau(1) = q_G$? Equivalently, are $q_I$ and $q_G$ in the same connected component of $\mathcal{C}_{free}$?

**How it differs from motion planning.** The [motion planning](/motion-planning/) page covers every kind of planner and every kind of promise. This page keeps only the exact decision question and its complexity. A method for the piano movers' problem must be complete: it must also say "no" when no path exists. Sampling planners do not solve it.

## Variants

| variant | robot | $d$ | status |
|---|---|---|---|
| ladder | a segment in the plane among polygons | 3 | polynomial in $n$ |
| planar piano | a polygon that translates and rotates among polygons | 3 | polynomial in $n$ (Schwartz and Sharir I) |
| classic piano | a rigid polyhedron in space among polyhedra | 6 | polynomial in $n$ for this fixed $d$ |
| generalized mover | many polyhedra linked by joints, in space | grows with the input | PSPACE-hard (Reif 1979) |
| warehouseman | many independent rectangles in a rectangular box | $2m$ for $m$ rectangles | PSPACE-hard (Hopcroft, Schwartz and Sharir 1984) |
| planar linkage | a tree of bars joined at their ends, in the plane | grows with the input | PSPACE-hard (Hopcroft, Joseph and Whitesides 1984) |
| sliding blocks on a grid | blocks that slide by unit steps | discrete | PSPACE-complete, for example [Rush Hour](/rush-hour-problem/) |

The difference between the rows is whether $d$ is fixed. When $d$ is fixed, the exact methods are polynomial in $n$, with a degree that grows with $d$. When $d$ grows with the input, the problem is PSPACE-hard. The grid versions such as Rush Hour and [Sokoban](/sokoban-problem/) are discrete cousins with the same flavor of hardness, but they have no continuous geometry. Adding velocity and force bounds gives [kinodynamic planning](/kinodynamic-planning/).

## Examples

**A ladder at a corner.** Two halls of widths $a$ and $b$ meet at a right angle. A ladder is a segment of length $L$ that stays in the floor plane. It can turn the corner if and only if

$$L \le \min_{0 < \theta < \pi/2} \left( \frac{a}{\sin \theta} + \frac{b}{\cos \theta} \right) = \left( a^{2/3} + b^{2/3} \right)^{3/2},$$

because the right side is the shortest segment that touches the inner corner and both outer walls. A numeric minimum over $\theta$ agrees with the closed form.

| $a$ | $b$ | longest ladder that turns |
|---|---|---|
| 1 | 1 | 2.8284 |
| 1 | 2 | 4.1619 |

So in halls of width 1, a ladder of length 2.5 gets through and a ladder of length 3 does not. The answer depends on real numbers, not only on the combinatorics of the obstacles. This is why exact methods work with polynomial constraints.

**Why rotation matters.** The configuration space of the ladder is $\mathbb{R}^2 \times S^1$, with $d = 3$. If the ladder were not allowed to turn, its configuration space would be $\mathbb{R}^2$ and it could never pass the corner at all. The path that a yes answer needs lives in the three-dimensional space.

**Many parts.** A robot made of $k$ rigid bodies in space has up to $6k$ degrees of freedom. In Reif's reduction $k$ grows with the size of the Turing machine to be simulated, and this growth in $d$ is the source of the hardness.

## Known algorithms

| method | time | notes |
|---|---|---|
| Schwartz and Sharir, [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) of $\mathcal{C}_{free}$ (1983) | polynomial in $n$ for fixed $d$, doubly exponential in $d$ | the first general method; it decides connectivity from the adjacency of the cells |
| Canny's roadmap algorithm (1988) | $n^d (\log n)\, p^{O(d^4)}$ deterministic, $n^d (\log n)\, p^{O(d^2)}$ randomized | singly exponential in $d$; assumes general position, which Basu, Pollack and Roy later removed |
| special-purpose methods for $d \le 3$ | low-degree polynomials in $n$ | built on the structure of the free space of one polygon or one segment, see [cell decomposition](/cell-decomposition/) |

These bounds are proved. LaValle notes in Section 6.4.3 that no general implementation of Canny's algorithm appears to exist. In practice, robots with $d \ge 4$ use sampling planners, which do not decide the problem.

## Bounds

- **Upper bound.** Canny's algorithm runs in polynomial space, so the problem is in PSPACE for every $d$ given in the input.
- **Lower bound.** Reif reduced the acceptance problem of a polynomial-space Turing machine to the generalized mover's problem, so the problem is PSPACE-hard. With the upper bound, it is PSPACE-complete.
- **Output size for fixed $d$.** The free space can have $\Omega(n^d)$ connected components, so any method that lists them all needs $\Omega(n^d)$ time. Apart from the factor in $p$, Canny's bound is close to this (Halperin, Salzman and Sharir, Section 50.1).
- **Real numbers.** The bounds count arithmetic operations on algebraic numbers in the [real RAM](/real-ram/) model. The algorithms use the decision methods of the theory of real closed fields, which rest on the [Tarski-Seidenberg theorem](/tarski-seidenberg-theorem/).

## Reductions

- **From Turing machines.** Reif built, from a machine that uses polynomial space, a body of many linked parts and a set of obstacles. The free motions of the parts copy the steps of the machine, and the goal placement is reachable exactly when the machine accepts. Hopcroft, Schwartz and Sharir did the same with independent rectangles in a box, where the rectangles act as gates that block one another.
- **To connectivity of a semi-algebraic set.** The problem is a special case of the question whether two points lie in the same component of a set given by polynomial inequalities. A cylindrical algebraic decomposition or a roadmap of the set answers it, and the graph of cells or roadmap curves is then searched by [graph reachability](/graph-reachability/).
- **To the point robot.** For a robot that only translates, the C-obstacles are [Minkowski sums](/minkowski-sum/), and the problem becomes the planar or spatial problem for a point, which is much easier.

## Applications

The problem is mostly of theoretical use. Its hardness explains why practical planners give up completeness for speed. Its exact algorithms are used for small $d$, for example to decide whether a part can be taken out of an assembly or whether a given object can pass through a given opening. The PSPACE-hardness results are also the base for the hardness of many sliding-block puzzles.

## References
