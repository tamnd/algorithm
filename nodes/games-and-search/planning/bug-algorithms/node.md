---
tag: JJWB8E
kind: algorithm
slug: bug-algorithms
name: Bug algorithms
aliases:
- Bug0
- Bug1
- Bug2
area: games-and-search/planning
level: intro
summary: Sensor-based navigation that follows obstacle boundaries; Bug0, Bug1 and Bug2 differ in when they leave.
solves: [motion-planning]
model: real-ram
complexity:
  vars: {D: the distance from the start to the goal, P: the sum of the perimeters of the obstacles that meet the disk of radius D around the goal, m: the largest number of points where the start-goal segment meets one obstacle boundary}
  time: {worst: O(D + m P), best: Θ(D)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, local: true}
history:
  year: 1987
  people: [Vladimir J. Lumelsky, Alexander A. Stepanov]
  note: Lumelsky and Stepanov gave Bug1 and Bug2 with their bounds on the path length in Algorithmica in 1987.
prereqs: [motion-planning]
see_also: [d-star-lite, tremaux-traversal, potential-field-method, configuration-space, cell-decomposition, rapidly-exploring-random-tree]
sources:
  - paper: doi:10.1007/BF01840369
    title: Vladimir J. Lumelsky and Alexander A. Stepanov, Path-planning strategies for a point mobile automaton moving amidst unknown obstacles of arbitrary shape, Algorithmica 2, 1987
    locator: pages 403 to 430 (the lower bound for any strategy of the class, Bug1 with the bound D + 1.5 times the sum of the perimeters, Bug2 with the bound in the number of crossings of the start-goal line)
  - paper: doi:10.1177/027836499801700903
    title: Ishay Kamon, Elon Rimon and Ehud Rivlin, TangentBug, a range-sensor-based navigation algorithm, International Journal of Robotics Research 17(9), 1998
    locator: pages 934 to 953 (the local tangent graph, motion to goal and boundary following with a range sensor)
  - book: isbn:9780262033275
    title: Howie Choset, Kevin M. Lynch, Seth Hutchinson, George Kantor, Wolfram Burgard, Lydia E. Kavraki and Sebastian Thrun, Principles of Robot Motion, MIT Press, 2005
    locator: Chapter 2 (Bug1, Bug2 and TangentBug, their completeness and the path length bounds)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Chapter 12 (planning under sensing uncertainty in unknown environments, with the Bug strategies; the exact subsection not checked)
---

The Bug algorithms move a point robot to a goal in the plane among obstacles that it does not know in advance. The robot knows its own position and the position of the goal, and it senses an obstacle only when it touches it. It moves straight toward the goal, and when it hits an obstacle it follows the boundary until a rule tells it to leave. Bug1 and Bug2 of Lumelsky and Stepanov (1987) are complete, with proved bounds on the length of the path, and they need only a constant amount of memory.

## In plain words

An ant in a room wants to reach a crumb. It can see where the crumb is but not the furniture. It walks straight at the crumb. When it bumps into a chair leg, it walks around the leg, keeping one side against it.

The three versions differ in when the ant stops walking around and heads for the crumb again. Bug0 leaves as soon as the way to the crumb is open. Bug1 walks all the way around the obstacle first, remembers the spot that was closest to the crumb, goes back to that spot and leaves from there. Bug2 draws an imaginary line from the start to the crumb and leaves the obstacle when it meets this line again at a spot closer to the crumb. Bug0 can circle forever. Bug1 and Bug2 always arrive, or they find out that the crumb cannot be reached.

## The problem

**The model.** The workspace is the plane, so the configuration space has dimension $d = 2$. The obstacles are closed, pairwise disjoint sets with boundaries of finite length, and there are finitely many of them in any bounded region. In the implementation they are polygons, possibly with holes. The robot is a point. It knows its position $x$ and the goal $q_G$ at all times, and it has a *contact sensor*: it learns that it is on a boundary only when it is there, and it can then follow the boundary in a fixed direction. It cannot see a map. Write $D = \lVert q_{start} - q_G \rVert$, $p_i$ for the perimeter of obstacle $i$, and $P$ for the sum of the $p_i$ over the obstacles that meet the disk of radius $D$ around $q_G$.

**Output.** A path from $q_{start}$ to $q_G$ that does not enter the interior of an obstacle, or the answer that $q_G$ cannot be reached. The robot produces the path as it moves, so the cost is the length of the path.

**How it differs from close pages.** [D* Lite](/d-star-lite/) also works in unknown terrain, but on a grid, with a map that it builds and a full replanning step after each change. The Bug algorithms keep no map and move in the continuous plane. [Trémaux's method](/tremaux-traversal/) explores a maze graph and marks the passages. The Bug algorithms have no marks and use the known direction to the goal. The [potential field method](/potential-field-method/) also reacts only to nearby obstacles, but it is not complete.

## The algorithm

The *m-line* is the segment from $q_{start}$ to $q_G$. A *hit point* $H$ is a point where the robot meets an obstacle, and a *leave point* is where it leaves the boundary. The robot follows each boundary with the obstacle on the same side, say on its left.

```pseudo id=main
BUG1(q_start, q_G)
L1  x ← q_start
L2  loop
L3      move from x straight toward q_G until q_G is reached or an obstacle is hit
L4      if q_G is reached then return success
L5      H ← the hit point
L6      follow the boundary all the way around, back to H, and record the boundary point L closest to q_G
L7      go along the boundary from H to L the shorter way
L8      if the robot cannot move from L toward q_G then return failure     ▷ q_G is unreachable
L9      x ← L

BUG2(q_start, q_G)
L10 x ← q_start
L11 loop
L12     move from x along the m-line toward q_G until q_G is reached or an obstacle is hit
L13     if q_G is reached then return success
L14     H ← the hit point
L15     follow the boundary until a point Q on the m-line with ‖Q − q_G‖ < ‖H − q_G‖ from which the robot can move toward q_G
L16     if the robot comes back to H first then return failure              ▷ q_G is unreachable
L17     x ← Q
```

Bug0 has the same loop as Bug2, but line L15 leaves at the first boundary point from which the robot can move toward $q_G$, on the m-line or not, and line L16 is missing. It needs no memory at all, but it is not complete: Choset et al. (Chapter 2) give maps on which it circles forever.

## Example

The obstacle is the U-shaped polygon with corners $(3, 2)$, $(7, 2)$, $(7, 8)$, $(3, 8)$, $(3, 7)$, $(6, 7)$, $(6, 3)$, $(3, 3)$, open to the left. Its perimeter is 26. The start $(4.5, 5)$ is inside the U and the goal $(9, 5.5)$ is to its right, so $D = 4.5277$. The m-line meets the boundary twice, on the inner wall $x = 6$ and the outer wall $x = 7$.

| step | Bug1 | Bug2 |
|---|---|---|
| straight move | to the hit point $H = (6, 5.167)$ | to the same hit point $H = (6, 5.167)$ |
| boundary | the whole boundary, 26, back to $H$ | down the inner wall to $(6, 3)$, out along $y = 3$ to $(3, 3)$, around the end to $(3, 2)$, along $y = 2$ to $(7, 2)$, up the outer wall |
| leave point | $L = (7, 5.5)$, the boundary point closest to the goal, reached the short way with 12.333 more | $Q = (7, 5.278)$, the first point on the m-line closer to the goal than $H$ |
| last move | 2 to the goal | 2.012 to the goal |
| path length | 41.8426 | 16.966 |
| proved bound | $D + 1.5 \cdot 26 = 43.53$ | $D + \tfrac{1}{2} \cdot 2 \cdot 26 = 30.53$ |

Both paths stay within their bounds. Here Bug2 is much shorter, because it leaves at the first good point while Bug1 must finish its full loop. On a map where the m-line crosses an obstacle many times, Bug2 can pass the same boundary several times and Bug1 is the shorter one.

## Correctness

The [proof](proofs/correctness/) shows four things. A leave point of Bug1 is the closest point of its boundary to the goal, so if the robot cannot move from it toward the goal, the boundary separates the robot from the goal. The distance to the goal falls strictly from one hit point to the next, so Bug1 hits each boundary at most once and Bug2 uses each crossing of the m-line at most once, and both stop. When Bug2 comes back to $H$ without a leave point, the last crossing of the m-line with that boundary would have been a valid leave point if the goal were reachable. The path length bounds follow by adding the straight parts, at most $D$ in total, and the boundary parts.

## Complexity

The cost that matters is the length of the path. For a robot that moves at unit speed it is also the time, and the bounds $O(D + mP)$ and $\Theta(D)$ in the summary of the page are path lengths. These bounds are proved.

- **Bug1.** The path has length at most $D + 1.5 P$: at most $D$ for the straight parts, and for each boundary it hits, one full loop and at most half a loop back.
- **Bug2.** The path has length at most $D + \sum_i n_i p_i / 2$, where $n_i$ is the number of points where the m-line meets the boundary of obstacle $i$. With $m = \max_i n_i$ this is at most $D + m P / 2$.
- **Lower bound.** Lumelsky and Stepanov proved that for every strategy of this class, with contact sensing only, there are maps on which the path is at least $D + P - \delta$ long, for any $\delta > 0$. So Bug1 is within a factor of 1.5 of the best possible bound on the boundary part.
- **Memory.** Bug1 keeps the hit point, the best point so far and its distance, and Bug2 keeps the hit point and its distance. Both need $O(1)$ points.
- **Computation.** Each step of the robot needs only its sensor and a distance test. In the implementation, on a polygon map with $n$ edges, finding the next hit point takes $O(n)$ time and a boundary walk takes time linear in the number of edges it passes.

## Properties

- **Complete, for this model.** Bug1 and Bug2 reach the goal when it can be reached and report failure otherwise, in finite time, for a point robot in the plane with obstacles of finite perimeter.
- **Online and local.** The robot uses only what it senses at its position, plus its own position and the goal.
- **Not optimal.** The path is not the shortest path. The shortest path among known polygons comes from the [visibility graph](/visibility-graph/).
- **Not for higher dimensions.** Following a boundary is a one-dimensional motion only in the plane. In three dimensions a surface has no single direction to follow, and the Bug method does not extend directly.

## Variants and improvements

- **TangentBug.** Kamon, Rimon and Rivlin (1998) give the robot a range sensor of radius $R$. It moves toward the visible endpoint $O$ of an obstacle that minimizes $\lVert x - O \rVert + \lVert O - q_G \rVert$, and it follows a boundary only when this sum stops falling. It is complete, and in practice its paths are much shorter than those of Bug2.
- **Alg1 and Alg2.** Sankaranarayanan and Vidyasagar changed Bug2 so that it remembers its hit points and does not pass the same boundary in the same way twice.
- **DistBug and VisBug.** Variants that leave earlier when a range sensor shows a free way to a point closer to the goal than the best one so far.
- **Grid versions.** On a grid, contour following with a left-hand rule plays the role of boundary following. A planner that keeps a map is then better served by [D* Lite](/d-star-lite/).

## When to use it

Use a Bug algorithm when the robot has no map, only a contact or short-range sensor and a position estimate, and the obstacles are in the plane. It is the standard example of a sensor-based planner with a proof. When a map is known, use an exact method such as the [visibility graph](/visibility-graph/) or a [cell decomposition](/cell-decomposition/). When the map is built as the robot moves on a grid, use D* Lite. When the robot has many degrees of freedom, use a sampling planner such as the [RRT](/rapidly-exploring-random-tree/).

## Pitfalls

- **Bug0 is not complete.** Leaving as soon as the way looks open can make the robot circle between two obstacles forever.
- **The m-line is fixed.** In Bug2 the m-line is the segment from the start to the goal. It is not the line from the last leave point. With a moving m-line the proof fails.
- **Crossings on the hit edge.** A point of the m-line on the hit edge, behind $H$ in the direction of travel, is passed only at the end of a full loop. An implementation that tests it at the start leaves at once and loops.
- **Touching is not crossing.** If the m-line only touches a vertex, the robot cannot leave there. The leave test must check that the robot can move toward the goal, not only that it is on the m-line.
- **Position errors.** The proofs assume that the robot knows its position exactly. With odometry drift the robot may not recognize $H$ or the m-line, and the failure test of line L16 can fire wrongly or never.
- **Holes and rings.** If the goal is inside a ring, the robot circles the outer boundary of the ring and reports failure. If the start is inside a ring, it circles the inner boundary. Both cases are correct failures, and the implementation tests both.

## Implementations

## History

Lumelsky and Stepanov introduced Bug1 and Bug2 in a paper in Algorithmica in 1987. They also proved the lower bound for the whole class of strategies with contact sensing. Kamon, Rimon and Rivlin added a range sensor in TangentBug in 1998. Choset et al. made the Bug algorithms the first chapter on planning in their textbook of 2005.

## References
