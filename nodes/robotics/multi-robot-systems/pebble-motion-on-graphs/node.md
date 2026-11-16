---
tag: XGM0YY
kind: problem
slug: pebble-motion-on-graphs
name: Pebble motion on graphs
aliases:
- Kornhauser-Miller-Spirakis problem
area: robotics/multi-robot-systems
level: advanced
summary: Move pebbles on distinct vertices of a graph to target vertices one step at a time; feasibility is decidable in polynomial time.
prereqs: [graph, permutation-parity]
see_also: [sliding-tile-puzzle, sliding-puzzle-solvability, multi-agent-pathfinding, coupled-and-decoupled-planning, prioritized-multi-robot-planning, np-hard, sokoban-problem, conflict-based-search]
sources:
  - paper: doi:10.1109/SFCS.1984.715921
    title: Daniel Kornhauser, Gary Miller and Paul Spirakis, Coordinating pebble motion on graphs, the diameter of permutation groups, and applications, 25th Annual Symposium on Foundations of Computer Science (FOCS), 1984
    locator: pages 241 to 250 (polynomial-time feasibility, the O(n^3) bound on moves and its tightness)
  - paper: doi:10.1007/PL00009259
    title: Vincenzo Auletta, Angelo Monti, Mimmo Parente and Pino Persiano, A linear-time algorithm for the feasibility of pebble motion on trees, Algorithmica 23(3), 1999
    locator: pages 223 to 245 (feasibility on trees in linear time)
  - paper: doi:10.1016/S0747-7171(08)80001-6
    title: Daniel Ratner and Manfred Warmuth, The (n^2 - 1)-puzzle and related relocation problems, Journal of Symbolic Computation 10(2), 1990
    locator: pages 111 to 137 (finding a shortest solution is NP-hard)
---

Pebble motion on graphs asks whether labeled pebbles, one per vertex at most, can be moved from given start vertices to given goal vertices when a move slides one pebble along an edge into an empty vertex. It is the discrete core of multi-robot path planning: the [sliding tile puzzle](/sliding-tile-puzzle/) is the case of a grid with one empty vertex. Unlike [multi-agent pathfinding](/multi-agent-pathfinding/), where many robots move at once and the plan should be short, pebble motion moves one pebble at a time and asks first whether a plan exists; Kornhauser, Miller and Spirakis (1984) showed that this is decidable in polynomial time, while finding a shortest plan is NP-hard.

## In plain words

Think of a train yard drawn as dots and lines. Some dots hold a numbered wagon, and the others are empty. In one move you push one wagon along a line onto an empty dot. You want each wagon to end on its own dot.

Sometimes this is impossible: on a single straight track two wagons can never pass each other. With a side track they can. The question is which yards and which wagon orders allow a solution, and how many moves it takes. The answer can be found quickly, and when a solution exists, the number of moves is never more than about the cube of the number of dots.

## Definition

Let $G = (V, E)$ be a connected undirected graph with $n$ vertices, and let there be $k < n$ pebbles with distinct labels. A *placement* puts the pebbles on distinct vertices. A *move* takes a pebble on vertex $u$ to an adjacent empty vertex $v$. Given a start placement $S$ and a goal placement $T$:

- **Feasibility.** Is there a sequence of moves from $S$ to $T$?
- **Plan.** If yes, output such a sequence.
- **Shortest plan.** Output a sequence with the fewest moves.

Each pebble stands for a robot, each vertex for a place a robot can be, and each edge for a short motion. Moves are sequential: one robot moves at a time.

## Variants

- **One empty vertex** ($k = n - 1$). The setting of Wilson (1974) and of the sliding tile puzzle.
- **Trees.** The graph is a tree; feasibility has a special linear-time algorithm.
- **Unlabeled pebbles.** Pebbles are interchangeable, so only the set of goal vertices matters. This is much easier.
- **Colored pebbles.** Pebbles of the same color are interchangeable; Goraly and Hassin (2010) studied feasibility in this setting.
- **Parallel moves.** Several pebbles move in the same step, and pebbles may follow each other along a path or rotate along a cycle. This is the model of multi-agent pathfinding, where the goal is usually the smallest makespan or the smallest total path length.
- **Robots with obstacles.** Some vertices hold fixed obstacles, which is the same as deleting them from the graph.

## Examples

**A path.** On a path of 3 vertices with pebbles $a$ at one end and $b$ in the middle, and the goal with $a$ and $b$ swapped, there is no plan: pebbles on a path keep their order.

**A star.** On a star with a center $c$ and leaves $1, 2, 3$, put $a$ on leaf 1 and $b$ on leaf 2, and ask to swap them. A plan with 6 moves: $a$ from 1 to $c$ to 3, then $b$ from 2 to $c$ to 1, then $a$ from 3 to $c$ to 2. The third leaf is the side track.

**A cycle.** On a cycle with one empty vertex, a pebble can only follow the others around, so the reachable placements are the rotations of the start, and two pebbles cannot be swapped.

**The 15-puzzle.** On the $4 \times 4$ grid with 15 pebbles, Wilson's theorem and the parity argument of the [sliding puzzle solvability](/sliding-puzzle-solvability/) page say that exactly half of the placements with the empty vertex in a fixed corner can be reached.

## Known algorithms

- **Kornhauser, Miller and Spirakis (1984).** Decides feasibility in polynomial time and builds a plan with $O(n^3)$ moves when one exists, for any connected graph and any $k < n$ (theorem).
- **Wilson (1974).** For one empty vertex on a 2-connected graph, gives the group of reachable permutations: all of them if the graph is not bipartite and not a cycle, the even ones if it is bipartite and not a cycle, the rotations on a cycle, with one exception, a special graph on 7 vertices (theorem).
- **Auletta, Monti, Parente and Persiano (1999).** Feasibility on trees in linear time (theorem).
- **Linear-time feasibility on general graphs.** Yu (2013, arXiv 1301.2342) gives a linear-time feasibility test for general graphs; the result is a preprint and is cited here as claimed.
- **Search.** For shortest plans on small instances, [A*](/a-star-search/) over placements, or [conflict-based search](/conflict-based-search/) in the parallel model.

## Bounds

- **Moves (theorem).** $O(n^3)$ moves always suffice when a plan exists, and some instances need $\Omega(n^3)$ moves, so the bound is tight (Kornhauser, Miller and Spirakis 1984).
- **Feasibility (theorem).** Polynomial time, and linear time on trees.
- **Shortest plans (theorem).** Finding a shortest plan is [NP-hard](/np-hard/) already for the $(n^2 - 1)$-puzzle on grids (Ratner and Warmuth 1990).
- **Parallel optimal plans (theorem).** In the parallel model, minimizing the makespan or the total distance is NP-hard, as Yu and LaValle (2013) showed.
- **Continuous versions.** Moving many rectangles in a box is PSPACE-hard (Hopcroft, Schwartz and Sharir 1984), so the graph abstraction hides hard geometry.

## Reductions

- The sliding tile puzzle is pebble motion on a grid graph with $k = n - 1$.
- Multi-agent pathfinding on a graph with sequential moves is pebble motion; with parallel moves it is a relaxation that allows more plans, such as rotations along a full cycle.
- Pebble motion with one empty vertex reduces to the study of a permutation group generated by the moves around cycles of the graph, which links feasibility to [permutation parity](/permutation-parity/). Wilson's paper (Journal of Combinatorial Theory, Series B 16(1), 1974, pages 86 to 96) is the source of this view.

## Applications

Pebble motion models warehouse robots on a grid of storage cells, trains in a yard with sidings, data packets in buffers with limited space, and automated parking systems. It gives the existence test that a complete multi-robot planner on a graph needs, and the $O(n^3)$ bound tells how long a feasible plan can be in the worst case.

## References
