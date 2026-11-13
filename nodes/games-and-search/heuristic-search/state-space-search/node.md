---
tag: T55Q8E
kind: problem
slug: state-space-search
name: State-space search
aliases:
- State-space search problem
- goal search
- path finding in a state space
- path search in a state space
- state space search
area: games-and-search/heuristic-search
level: intro
summary: Given a start state, a successor function, action costs and a goal test, find a path from the start to a goal, or a cheapest one, or report that none exists.
prereqs: [state-space]
see_also: [search-strategy, search-tree, completeness-and-optimality-of-search, a-star-search, heuristic-function, single-source-shortest-paths, classical-planning, sliding-tile-puzzle]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Sections 3.1 to 3.4 (search problems and solutions, example problems, search algorithms and uninformed search strategies)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (basic heuristic search procedures)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 1 (state space problems and solutions) and Chapter 2 (basic search algorithms)
  - paper: doi:10.1016/0004-3702(94)90081-7
    title: "Tom Bylander, The computational complexity of propositional STRIPS planning, Artificial Intelligence 69(1-2) (1994)"
    locator: pp. 165 to 204 (deciding whether a STRIPS task has a plan is PSPACE-complete)
  - paper: doi:10.1016/S0747-7171(08)80001-6
    title: Daniel Ratner and Manfred Warmuth, The (n^2 - 1)-puzzle and related relocation problems, Journal of Symbolic Computation 10(2) (1990)
    locator: pp. 111 to 137 (finding a shortest solution of the n by n sliding puzzle is NP-hard)
---

State-space search is the problem of finding a path through a [state space](/state-space/): from a start state, by a sequence of actions, to a state that passes the goal test. In the *optimal* version the path must have the least total cost. The space is given implicitly, by a successor function, so the input is short and the graph behind it can be exponentially large or infinite. This is the difference from the [shortest path problem](/single-source-shortest-paths/) of graph theory, which has the same goal but takes the whole graph as input. Puzzles, route planning, [classical planning](/classical-planning/) and many scheduling and verification tasks are cases of it. The algorithms differ in the order in which they visit states, which is their [search strategy](/search-strategy/), and in what they know about the distance to a goal, which is their [heuristic function](/heuristic-function/).

## In plain words

You are given a puzzle and the rules for a move, and you must find moves that solve it. Nobody gives you a map of all the positions, because there are far too many. You can only start at the position you have, try the moves that are legal there, and see where each one leads.

Sometimes any solution is good enough. Sometimes you want the shortest one, or the cheapest one if moves have different prices. The hard part is to find it without looking at most of the positions.

## Definition

**Input.** A state space given implicitly:

- a start state $s_0$;
- a successor function $\mathrm{succ}(s)$ that returns, for each action $a$ that applies in $s$, the next state $T(s, a)$ and the cost $c(s, a) \ge 0$;
- a goal test, which says whether a state is in the goal set $G$.

**Output.** A *solution*, a sequence of actions $a_1, \ldots, a_k$ whose states $s_i = T(s_{i-1}, a_i)$ end in $s_k \in G$, or the answer that no solution exists.

**Optimal state-space search** asks for a solution of least cost $C^* = \min \sum_{i} c(s_{i-1}, a_i)$. The cost of a cheapest path from a state $n$ to a goal is written $h^*(n)$, so $C^* = h^*(s_0)$.

**Decision version.** Given also a bound $K$, decide whether a solution of cost at most $K$ exists.

The measure of the input is not the number of states. The costs of an algorithm are given in terms of the branching factor $b$, the depth $d$ of the shallowest or cheapest goal and the largest depth $m$ of a path, or in terms of the number of states that it visits.

## Variants

- **Satisficing search.** Any solution is good enough. It is often much cheaper than optimal search.
- **Bounded-suboptimal search.** Find a solution of cost at most $w C^*$ for a given $w \ge 1$. [Weighted A*](/weighted-a-star/) is the standard method.
- **Bounded-cost search.** Find a solution of cost at most a given $K$, as fast as possible.
- **Anytime search.** Return a first solution fast and improve it while time remains, as [anytime repairing A*](/anytime-repairing-a-star/) does.
- **Unit costs.** All actions cost 1, so the cheapest path is the shortest one, and [breadth-first search](/breadth-first-search/) is optimal.
- **Real-time search.** The agent must commit to a move after a bounded amount of search, as in [real-time A*](/real-time-a-star/).
- **Dynamic or unknown spaces.** Costs change or are learned while the agent moves, and the search must be repaired, as in [D* Lite](/d-star-lite/).
- **Several agents.** Paths for several agents that must not collide, which is [multi-agent pathfinding](/multi-agent-pathfinding/).
- **Backward and bidirectional search.** If a predecessor function is given, the search can also run from the goals, as in [bidirectional search](/bidirectional-search/).

## Examples

- **The 8-puzzle.** The start state of Russell and Norvig, with rows 7 2 4, 5 _ 6 and 8 3 1, and the goal with the blank in the top left corner and the tiles 1 to 8 in order. Its shortest solution has 26 moves, found by a breadth-first search of all 181,440 states of its class. See [sliding tile puzzle](/sliding-tile-puzzle/).
- **A small weighted graph.** On the graph of the page [A* search](/a-star-search/), with 8 states and 9 edges, the cheapest path from S to G is S, B, C, G with cost 7.
- **Route planning.** The states are road junctions and the costs are travel times. The space is explicit but large, and the searches use lower bounds from geometry or from landmarks.
- **No solution.** In the 8-puzzle, a start state of the other parity class, such as the goal with tiles 1 and 2 swapped, has no solution. A search proves this only by exhausting the 181,440 states that it can reach, unless it uses the parity argument.

## Known algorithms

The algorithms are on their own pages, and their completeness and optimality are compared on [completeness and optimality of search](/completeness-and-optimality-of-search/).

| algorithm | uses $h$ | optimal when |
| --- | --- | --- |
| [breadth-first search](/breadth-first-search/) | no | unit costs |
| [uniform-cost search](/uniform-cost-search/), [Dijkstra's algorithm](/dijkstra/) | no | costs $\ge 0$ |
| [depth-first search](/depth-first-search/) | no | never in general |
| [iterative deepening search](/iterative-deepening-search/) | no | unit costs |
| [greedy best-first search](/greedy-best-first-search/) | yes | never in general |
| [A*](/a-star-search/) | yes | $h$ admissible, with reopening |
| [IDA*](/iterative-deepening-a-star/) | yes | $h$ admissible |
| [recursive best-first search](/recursive-best-first-search/) | yes | $h$ admissible |
| [beam search](/beam-search/) | yes | never in general |

The algorithms that keep one node per state, with [duplicate detection](/duplicate-detection/), use memory in proportion to the states that they reach. The depth-first ones use memory in proportion to the depth, and they pay for it with repeated work.

## Bounds

- **Explicit graphs.** If the space is given as a graph with $V$ states and $E$ arcs, a goal can be found in $O(V + E)$ time by breadth-first search, and a cheapest path with nonnegative costs in $O(E + V \log V)$ time by Dijkstra's algorithm with a Fibonacci heap.
- **Blind search, lower bound.** Let an algorithm only call the successor function and the goal test. In a uniform tree of branching factor $b$ whose goals are only at depth $d$, it must test, in the worst case, all $b^d$ states at depth $d$. Proof: while an untested state of depth $d$ remains, an adversary can answer "not a goal" to each test so far and still make that state the only goal. So the uninformed searches in the table above are within a constant factor of the best possible on such trees, and only a heuristic can do better.
- **Succinct spaces.** When the space is given by a compact description, such as a set of propositional STRIPS actions, the number of states is exponential in the input. Deciding whether a solution exists is then PSPACE-complete (Bylander 1994), see [STRIPS plan existence](/strips-plan-existence-pspace-complete/). Some solvable tasks need plans of exponential length.
- **Optimal solutions of puzzles.** For the $(n^2 - 1)$-puzzle on an $n$ by $n$ board, whether a solution exists can be decided in polynomial time, by parity, but finding a shortest solution is NP-hard (Ratner and Warmuth 1990).

## Reductions

- **To shortest paths.** If the reachable space is small enough to build, state-space search is the single-pair case of the [single-source shortest path problem](/single-source-shortest-paths/) on the state graph.
- **From planning.** A classical planning task is a state-space search problem in which a state is a set of facts and an action applies when its preconditions hold, see [state-space planning](/state-space-planning/).
- **To satisfiability.** The decision version with a bound on the number of steps, written as one copy of the state variables per step, becomes a [bounded plan existence](/bounded-plan-existence-np-complete/) problem, which is in NP when the bound is given in unary.
- **To reachability.** The question whether any goal can be reached, without costs, is [reachability](/reachability/) in the state graph.

## Applications

- Puzzles such as the sliding tile puzzles, the [Rubik's cube](/rubiks-cube-problem/) and the [Tower of Hanoi](/tower-of-hanoi/), as benchmarks and for finding optimal solutions.
- Route finding in road networks and on game maps.
- Automated planning, where a planner searches the states of a task with a domain-independent heuristic.
- [Multiple sequence alignment](/multiple-sequence-alignment/), as a cheapest path through a lattice of partial alignments.
- [Explicit state model checking](/explicit-state-model-checking/), which searches the states of a system for one that violates a property.

## References
