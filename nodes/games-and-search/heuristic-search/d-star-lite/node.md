---
tag: TCGXBA
kind: algorithm
slug: d-star-lite
name: "D* Lite"
aliases:
- "D*-Lite"
area: games-and-search/heuristic-search
level: advanced
summary: "LPA* run backward from the goal to a moving robot, with a key offset k_m so the queue needs no reordering; it moves the robot along shortest paths of the map it knows, as D* does."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the largest number of successors of a vertex}
  time: {per-call: O((n + m)(d + log n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [lifelong-planning-a-star, consistent-heuristic]
see_also: [d-star, replanning, bug-algorithms, motion-planning, learning-real-time-a-star, anytime-repairing-a-star, a-star-search]
sources:
  - paper: Sven Koenig and Maxim Likhachev, D* Lite, Proceedings of the Eighteenth National Conference on Artificial Intelligence (AAAI 2002)
    title: Sven Koenig and Maxim Likhachev, D* Lite, AAAI 2002
    locator: pp. 476 to 483; Figure 3 (D* Lite, lines 01 to 35), Figure 4 (the optimized version), the section on the key modifier k_m, Theorem 8 (termination and correctness), and the experiments on eight-connected grids
  - paper: doi:10.1109/TRO.2004.838026
    title: Sven Koenig and Maxim Likhachev, Fast replanning for navigation in unknown terrain, IEEE Transactions on Robotics 21(3) (2005)
    locator: pp. 354 to 363 (the journal version, with LPA*, D* Lite and the comparison with focussed D*)
  - paper: doi:10.1016/j.artint.2003.12.001
    title: Sven Koenig, Maxim Likhachev and David Furcy, Lifelong Planning A*, Artificial Intelligence 155(1-2) (2004)
    locator: pp. 93 to 146 (LPA*, the algorithm that D* Lite runs backward, and its theorems)
  - paper: Anthony Stentz, The focussed D* algorithm for real-time replanning, Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI 1995)
    title: Anthony Stentz, The focussed D* algorithm for real-time replanning, IJCAI 1995
    locator: pp. 1652 to 1659 (focussed D*, the biased keys that D* Lite replaces with k_m)
---

D* Lite moves a robot to a goal through terrain that it learns while it moves. It plans a shortest path on the map it knows, assumes that unknown cells are free, and plans again each time its sensors show that the map was wrong. It is [Lifelong planning A*](/lifelong-planning-a-star/) (LPA*) turned around: the search goes from the goal to the robot, so that the values $g$ that the search keeps stay valid when the robot moves. A single number $k_m$ is added to the priorities to keep the queue in order as the robot moves, so that the queue never has to be reordered. Koenig and Likhachev introduced it in 2002. It moves the robot in the same way as Stentz's [D*](/d-star/), with a shorter algorithm that is easier to prove correct.

## In plain words

You walk to a friend's house in fog. You draw a map and you assume that every street you cannot see is open. You find the shortest route on your map and start walking. When you see that a street ahead is closed, you mark it on the map and find a new route.

You do not redo the whole map each time. You wrote on each corner how far it is to your friend's house, counted from the house. Those numbers do not depend on where you stand, so most of them stay right when you walk on. When a street closes, only the corners whose route used that street need new numbers, and you fix those first that are close to where you stand now.

## The problem

The terrain is a finite directed graph with a goal vertex $s_{goal}$ and a robot at a vertex $s_{start}$ that changes as the robot moves. The robot knows a map: a cost $c(u, v) > 0$ for each edge, with $c = \infty$ for a blocked edge. Under the *free-space assumption* the first map gives unknown edges their lowest possible cost. The robot senses the true costs of some edges near it, usually the edges out of the cells within a sensor range, and the sensed costs replace the map costs. The task is to move the robot to $s_{goal}$, at each step along a shortest path of the current map, or to report that the map shows no path.

The heuristic $h(a, b)$ estimates the distance between two vertices. It must be nonnegative, at most the true distance $\mathrm{dist}(a, b)$ on every map, and satisfy the triangle inequality $h(a, c) \le h(a, b) + h(b, c)$. On a grid, a heuristic computed from the coordinates has these properties. In the experiments of the paper, the grid is 8-connected, each move to one of the 8 neighbours costs 1, diagonal moves included, and $h$ is the largest of the differences of the $x$ and $y$ coordinates.

The cost of planning is counted in vertex expansions, as for [A*](/a-star-search/).

## The algorithm

Each vertex $s$ has $g(s)$, the estimate of its distance *to* the goal, and
$$ \mathrm{rhs}(s) = \begin{cases} 0 & \text{if } s = s_{goal}, \\ \min_{s' \in \mathrm{Succ}(s)} \big(c(s, s') + g(s')\big) & \text{otherwise.} \end{cases} $$
As in LPA*, a vertex is locally consistent when $g(s) = \mathrm{rhs}(s)$, and the queue $U$ holds the vertices that are not. The key of $s$ is
$$ \big[\min(g(s), \mathrm{rhs}(s)) + h(s_{start}, s) + k_m;\ \min(g(s), \mathrm{rhs}(s))\big] , $$
compared in lexicographic order.

```pseudo id=main
CALCULATE-KEY(s)
L1  return [min(g(s), rhs(s)) + h(s_start, s) + k_m; min(g(s), rhs(s))]

INITIALIZE()
L2  U ← ∅, k_m ← 0
L3  for each s ∈ S do rhs(s) ← g(s) ← ∞
L4  rhs(s_goal) ← 0
L5  U.INSERT(s_goal, CALCULATE-KEY(s_goal))

UPDATE-VERTEX(u)
L6  if u ≠ s_goal then rhs(u) ← min over s′ ∈ Succ(u) of c(u, s′) + g(s′)
L7  if u ∈ U then U.REMOVE(u)
L8  if g(u) ≠ rhs(u) then U.INSERT(u, CALCULATE-KEY(u))

COMPUTE-SHORTEST-PATH()
L9  while U.TOPKEY() < CALCULATE-KEY(s_start) or rhs(s_start) ≠ g(s_start) do
L10     k_old ← U.TOPKEY(), u ← U.POP()
L11     if k_old < CALCULATE-KEY(u) then U.INSERT(u, CALCULATE-KEY(u))
L12     else if g(u) > rhs(u) then
L13         g(u) ← rhs(u)
L14         for each s ∈ Pred(u) do UPDATE-VERTEX(s)
L15     else
L16         g(u) ← ∞
L17         for each s ∈ Pred(u) ∪ {u} do UPDATE-VERTEX(s)

MAIN()
L18 s_last ← s_start
L19 INITIALIZE(), COMPUTE-SHORTEST-PATH()
L20 while s_start ≠ s_goal do
L21     if g(s_start) = ∞ then return "no known path"
L22     s_start ← a successor s′ of s_start that minimizes c(s_start, s′) + g(s′)
L23     move the robot to s_start
L24     sense the edge costs near the robot
L25     if some edge costs changed then
L26         k_m ← k_m + h(s_last, s_start)
L27         s_last ← s_start
L28         for each directed edge (u, v) whose cost changed do
L29             c(u, v) ← the new cost
L30             UPDATE-VERTEX(u)
L31         COMPUTE-SHORTEST-PATH()
```

This follows Figure 3 of the paper. Lines L1 to L17 are LPA* with the roles of start and goal exchanged: rhs looks at successors, and an expansion updates predecessors. Two lines are new.

**The key modifier $k_m$.** The heuristic in a key is $h(s_{start}, s)$, so it changes when the robot moves. When the robot goes from $s_{last}$ to $s_{start}$, each true key can drop by at most $h(s_{last}, s_{start})$, by the triangle inequality. Instead of lowering all keys in the queue by this amount, D* Lite adds it to $k_m$ at line L26, and $k_m$ is added to every key computed later. The old keys in the queue are then lower bounds on their true keys, and the order of the queue never has to be rebuilt.

**Lazy reinsertion.** Line L11 removes the vertex with the least stored key. If that key is below its true key, the vertex goes back with the true key and nothing else happens. Otherwise its stored key is its true key and it is the least true key in the queue, so the expansion is the expansion that LPA* would make.

The robot never needs a search tree. It moves to the successor with the least $c + g$, which is the next vertex on a shortest path of the map.

## Example

The map is a 4-connected grid of 5 columns and 3 rows, with unit costs and $h$ the Manhattan distance. The robot is at (0, 1) and the goal at (4, 1). The cell (2, 1) is blocked, but the robot does not know this. It sees the cells next to it.

**First call.** $k_m = 0$. The search expands, from the goal, (4, 1) with key [4; 0], then (3, 1) [4; 1], (2, 1) [4; 2], (1, 1) [4; 3] and (0, 1) [4; 4]. The robot has $g$ = 4 and plans the straight path. These are the 5 expansions of an A* search from the goal to the robot.

**The robot moves** to (1, 1) and sees that (2, 1) is blocked. Line L26 sets $k_m = h((0, 1), (1, 1)) = 1$. The 8 edges into and out of (2, 1) get cost $\infty$, and line L30 updates their start vertices. Now (2, 1) has rhs $= \infty$ but still $g = 2$, and (1, 1) has $g = 3$ but rhs $= 5$, through (0, 1). The cells (1, 0) and (1, 2) were never expanded, so their $g$ is still $\infty$.

**Second call.** It expands 12 vertices. It first expands (2, 1) and (1, 1) as underconsistent, with the keys [4; 2] and [4; 3], then the cells around the obstacle as overconsistent, with keys from [6; 1] up, and ends with (1, 1) as overconsistent with key [6; 5]. The new distance of the robot is $g(1, 1) = 5$. The robot walks (1, 2), (2, 2), (3, 2), (4, 2) and (4, 1) and sees no more change. The whole walk costs 6, which is the shortest path in the true grid.

On this small map, A* from scratch at (1, 1) expands 11 vertices, one fewer than the second call. The gain of D* Lite appears on larger maps, where a change touches a small part of the search.

**A measured experiment.** The grid is 50 by 50 and 8-connected, as in the paper: each move to one of the 8 neighbours costs 1, a diagonal move needs only its end cell to be free, and $h$ is the largest of the coordinate differences. Each cell is blocked with probability 0.3 (`random.Random(seed)` of Python), the robot starts at (0, 0), the goal is (49, 49), the robot knows nothing at the start and sees the 8 cells around it. At each position where it sees a change, D* Lite replans, and for comparison A* searches from scratch from the goal to the robot on the same map (ties toward smaller $g$).

| seed | first call | replanning calls | D* Lite expansions in them | A* expansions at the same points | moves | shortest true path |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 50 | 46 | 233 | 2,352 | 63 | 57 |
| 2 | 50 | 47 | 332 | 3,067 | 65 | 57 |
| 3 | 50 | 50 | 249 | 2,635 | 66 | 56 |

These are measurements on three random maps, not bounds. The robot walks a little more than the shortest true path, because it learns the obstacles only when it is next to them. This is a property of the free-space assumption, not of the search: every method that moves along shortest paths of the known map makes the same moves, up to ties.

## Correctness

The [proof](proofs/correctness.md) reduces a call of COMPUTE-SHORTEST-PATH to a call of LPA*.

- **The reversed problem.** On the graph with all edges reversed, the rhs-values of D* Lite are those of LPA* with start $s_{goal}$ and goal $s_{start}$. The conditions on $h$ make $h(s_{start}, \cdot)$ a [consistent heuristic](/consistent-heuristic/) for that search.
- **Stored keys are lower bounds.** By the triangle inequality, the key stored for a vertex is at most its true key with the current $s_{start}$ and $k_m$. Line L11 corrects a key that is too small without changing a value, so each expansion takes a vertex of least true key, as LPA* does. A vertex is reinserted at most once per call.
- **The result of a call.** The proof for LPA* then gives $g(s_{start}) = \mathrm{dist}(s_{start})$ on the current map, at most two expansions per vertex per call, and a shortest path by following the least $c + g$ (Theorem 8 of the paper).
- **The robot.** If the first map underestimates every cost and the robot senses each edge before it uses it, it never enters a blocked edge, reports "no known path" only when the goal cannot be reached, and reaches the goal when every vertex that it can reach can still reach the goal, for example on an undirected grid where the goal can be reached.

## Complexity

The model is the [word RAM](/word-ram/) with $n$ vertices, $m$ edges and $d$ the largest number of successors of a vertex. A call does at most $2n$ expansions and $n$ reinsertions, and each expansion runs UPDATE-VERTEX on the predecessors of a vertex. UPDATE-VERTEX takes a minimum over at most $d$ successors and does $O(1)$ heap operations, so a call takes $O((n + m)(d + \log n))$ time in the worst case with a [binary heap](/binary-heap/) that supports removal. The space is $O(n)$ for the values and the queue, besides the map. On an 8-connected grid, $d = 8$ and $m \le 8n$, so a call takes $O(n \log n)$.

The worst case of a call is no better than A* from scratch. The gain is measured, not proved. In the experiment above, the replanning calls of D* Lite expanded about a tenth of what A* from scratch expanded. Koenig and Likhachev (2002) measured on 8-connected grids of seven sizes, with obstacle densities from 10 to 40 percent and 50 random maps per size, that the optimized D* Lite was better than focussed D* in vertex expansions, heap percolates and vertex accesses, and much better than A* from scratch and than D* Lite without the heuristic.

## Properties

- **Exact on the map.** After each call, $g(s_{start})$ is the distance of the robot to the goal on the current map.
- **Backward search.** The search starts at the goal. This is what makes the old values useful after the robot moves: distances to the goal do not depend on where the robot is. LPA*, which searches forward, would have to start again at each move.
- **Same strategy as D*.** Both move the robot along a shortest path of the current map, so up to ties they make the same moves. D* Lite uses one key with one tie rule, and no nested cases for raised and lowered states.
- **Not optimal in the true terrain.** The walk can be longer than the shortest true path, because the map is wrong until the robot sees the obstacles. Under the free-space assumption the robot is optimistic, which keeps it complete in a finite undirected terrain.
- **Handles both increases and decreases** of edge costs, and changes far from the robot.

## Variants and improvements

- **Optimized D* Lite.** Figure 4 of the paper changes a key in place with an update operation instead of removing and inserting it, updates rhs in $O(1)$ when a successor improves, and stops when $s_{start}$ is not underconsistent instead of requiring it to be consistent.
- **Field D*.** Ferguson and Stentz interpolate the values $g$ along cell edges, so that the robot can move at any angle, not only along grid edges.
- **Anytime D*.** Likhachev and others (2005) add an inflation factor on $h$, as in [anytime repairing A*](/anytime-repairing-a-star/), to get a bounded suboptimal path fast and improve it.
- **Moving goal and other uses.** Koenig and Likhachev also used D* Lite for mapping unknown terrain, where the goal is the nearest unknown cell, and for a deterministic version of the parti-game algorithm.

## When to use it

Use D* Lite when a robot or a game unit must reach a fixed goal through terrain that it learns while it moves, and the map changes only near the unit. It is the standard choice for navigation on grids and lattices with a free-space assumption. When the start is fixed and the goal is fixed, use LPA*. When the terrain is fully known and does not change, use A* once. When time per move is fixed and small, real-time search such as [LRTA*](/learning-real-time-a-star/) bounds the work of each move instead of planning a full path. For robots that have no map at all and only touch sensors, the [bug algorithms](/bug-algorithms/) give simple strategies with bounds on the length of the walk. Planning in a continuous configuration space is the subject of [motion planning](/motion-planning/).

## Pitfalls

- **Searching in the wrong direction.** D* Lite searches from the goal. If you use LPA* forward from the robot, the old values become useless after each move.
- **Forgetting $k_m$.** Without line L26, keys computed after a move are not comparable with the keys in the queue, and the search expands vertices in a wrong order. The result can be wrong.
- **A heuristic without the triangle inequality.** The lower bound argument for old keys needs $h(a, c) \le h(a, b) + h(b, c)$. Consistency alone, as for A*, is not enough here.
- **Updating the wrong vertex.** For a changed edge $(u, v)$, line L30 updates $u$, the tail, because rhs looks at successors. Updating $v$ as in LPA* leaves rhs$(u)$ wrong.
- **Sensing after the move.** The robot must know the true cost of an edge before it uses it, so the first sensing must happen before the first move.
- **Counting reinsertions as expansions.** Line L11 does not change a value. Keep it apart when you compare counts.

## Implementations

## History

Stentz introduced D* in 1994 and focussed D* in 1995 for robot navigation in unknown terrain, and, as the D* Lite paper states, D* was used on outdoor HMMWVs and on Mars rover prototypes. Koenig and Likhachev noted that focussed D* is complex and hard to analyze and extend. In 2002 they presented D* Lite at AAAI: it applies their LPA* backward from the goal and borrows from focussed D* the idea of biased keys, in the simpler form of $k_m$. The journal version, Koenig and Likhachev (2005) in IEEE Transactions on Robotics, compares it with D* and gives the proofs. D* Lite and its variants became widely used in robotics.

## References
