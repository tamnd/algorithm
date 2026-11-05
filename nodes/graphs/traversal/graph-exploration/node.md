---
tag: 7G8D2X
kind: problem
slug: graph-exploration
name: Graph exploration
aliases:
- exploring unknown graphs
- online graph exploration
area: graphs/traversal
level: advanced
summary: Visit all vertices of an unknown graph by walking its edges while minimizing the total number of moves.
prereqs: [depth-first-search, online-algorithm, competitive-ratio]
see_also: [tremaux-traversal, online-graph-exploration-problem, chinese-postman-problem, traveling-salesman-problem, nearest-neighbor-tsp, eulerian-graph, strongly-connected-graph, graph-reachability]
sources:
  - paper: doi:10.1006/jagm.1999.1043
    title: Petrişor Panaite and Andrzej Pelc, Exploring unknown undirected graphs, Journal of Algorithms 33(2), 281 to 295 (1999)
    locator: the main theorem (an exploration of every edge and vertex with at most m + 3n edge traversals) and the comparison with depth-first search
  - paper: doi:10.1002/(sici)1097-0118(199911)32:3<265::aid-jgt6>3.0.co;2-8
    title: Xiaotie Deng and Christos H. Papadimitriou, Exploring an unknown graph, Journal of Graph Theory 32(3), 265 to 297 (1999)
    locator: the model of exploring a strongly connected directed graph, the deficiency of a graph, and the algorithm for Eulerian graphs with ratio 2
  - paper: doi:10.1137/s009753979732428x
    title: Susanne Albers and Monika R. Henzinger, Exploring unknown environments, SIAM Journal on Computing 29(4), 1164 to 1188 (2000)
    locator: the algorithm for directed graphs of deficiency d with d^O(log d) m edge traversals, and the lower bounds for natural algorithms
  - paper: doi:10.1016/0304-3975(94)90155-4
    title: Bala Kalyanasundaram and Kirk R. Pruhs, Constructing competitive tours from local information, Theoretical Computer Science 130(1), 125 to 138 (1994)
    locator: the vertex exploration of weighted planar graphs with a constant competitive ratio (the algorithm ShortCut)
  - paper: doi:10.1109/sfcs.1979.34
    title: Romas Aleliunas, Richard M. Karp, Richard J. Lipton, László Lovász and Charles Rackoff, Random walks, universal traversal sequences, and the complexity of maze problems, 20th Annual Symposium on Foundations of Computer Science (1979), 218 to 223
    locator: the bound on the expected cover time of a random walk on a connected graph, and the existence of universal traversal sequences of polynomial length
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition (edited by Guy Even), Cambridge University Press
    locator: Chapter 3, Section 3.1 (Trémaux's algorithm, the exploration of a maze with 2m passage traversals)
---

Graph exploration is the problem of an agent that starts at one vertex of a graph it does not know, can see only what is at its current vertex, and must visit every vertex, or walk every edge, by moving along edges, with as few moves as possible. Because the graph is revealed only as the agent walks, it is an [online problem](/online-algorithm/), and algorithms are judged by their [competitive ratio](/competitive-ratio/): the cost of the agent divided by the cost of the best walk for a person who knows the graph in advance. On undirected graphs, [depth-first search](/depth-first-search/) as a walk, the [Trémaux traversal](/tremaux-traversal/), walks every edge with $2m$ moves, and better algorithms use $m + O(n)$ moves. On directed graphs, the difficulty is measured by the *deficiency*, how far the graph is from being Eulerian. On graphs with edge lengths, exploration is an online form of the [travelling salesman problem](/traveling-salesman-problem/), and whether a constant ratio is possible on every graph is not known.

## In plain words

A robot is put in a building it has never seen. In each room it sees the doors, and it can only move through doors. It must see every room, or go through every door, and it wants to walk as little as possible.

If the robot knew the map, it could plan the shortest tour. It does not, so it must sometimes walk back a long way because of something it could not know. The question is how much worse the robot does than a planner with the map, in the worst building.

A simple answer is to explore depth-first: always go through a new door, and go back only when there is none. This never walks through a door more than twice. Better methods come close to walking each door only once, plus a little extra.

## Definition

**Model.** A connected graph $G = (V, E)$, with $n = |V|$ and $m = |E|$, and a start vertex $s$. Vertices have distinct names. An agent with unlimited memory starts at $s$. When it is at a vertex $v$, it learns the edges at $v$ and, in the vertex model, the names of their other ends. A *move* is a walk along one edge at the current vertex. In the directed version, edges can be walked only in their direction, and $G$ is strongly connected so that the agent cannot get stuck.

**Tasks.**

- *Edge exploration*: walk every edge at least once.
- *Vertex exploration*: visit every vertex at least once.
- Either task may require the agent to end at $s$.

**Cost.** The cost of an exploration is the number of moves, or, if the edges have lengths, the total length walked. For an online algorithm $A$, the *competitive ratio* is the supremum over inputs of $\mathrm{cost}_A(G, s) / \mathrm{OPT}(G, s)$, where $\mathrm{OPT}$ is the cost of the shortest walk that does the task in the known graph. The *penalty* of an edge exploration is the number of moves beyond $m$.

## Variants

- **Undirected edge exploration.** The classical maze problem. Here $\mathrm{OPT} \ge m$.
- **Directed edge exploration.** Every edge of a strongly connected digraph must be walked in its direction. The *deficiency* $d$ is the least number of edges that must be added to make the digraph [Eulerian](/eulerian-graph/); equivalently, it is the sum of $\max(0, \mathrm{out}(v) - \mathrm{in}(v))$ over all vertices.
- **Vertex exploration with lengths.** Visit all vertices of an undirected graph with edge lengths and return to $s$, at least cost. The offline optimum is a shortest closed walk through all vertices, which is the travelling salesman problem in the graph metric.
- **Tethered and fuel-limited exploration.** The agent must return to $s$ every $B$ moves, as a robot with a battery or a rope must.
- **Limited memory.** The agent has few bits of memory or may leave marks, such as the chalk of the Trémaux rule or a movable pebble. With no memory and no marks, a random walk still explores, in expected polynomial time.
- **Several agents.** A team of $k$ agents shares the work, and the cost is the time until all vertices are seen.

## Examples

**A star.** Let $s$ be the centre of a star with $n - 1$ leaves, so $m = n - 1$. Every leaf is a dead end, so after each leaf except the last one, the agent must walk back to the centre. Any edge exploration uses at least $2(n - 2) + 1 = 2m - 1$ moves, so the penalty is at least $m - 1 = n - 2$. A penalty of order $n$ cannot be avoided, and the bound $m + 3n$ of Panaite and Pelc is optimal up to the constant factor of the $n$ term.

**A cycle.** On the cycle $C_n$, the Trémaux walk goes around to the last new vertex, tries the edge back to $s$, turns back, and then walks back along the entry edges: $2n = 2m$ moves, ending at $s$. A walk once around the cycle does the same job with $n$ moves. In the vertex model, an agent that does not need to return can stop after $n - 1$ moves, when it sees that all neighbours are visited.

**A complete graph.** On $K_n$ in the vertex model, the agent sees all names at $s$, so it can visit the vertices in any order with $n - 1$ moves. In the edge model, every one of the $n(n-1)/2$ edges must be walked, and DFS uses twice that number, while an [Eulerian circuit](/eulerian-circuit/) of $K_n$ for odd $n$ uses each edge once. This is the gap that the $m + O(n)$ algorithms close.

## Known algorithms

- **Depth-first exploration.** The agent walks the [Trémaux traversal](/tremaux-traversal/): take a new edge, turn back at once if it leads to a visited vertex, and go back along the entry edge when no new edge is left. It walks each edge exactly twice, $2m$ moves, and returns to $s$. For vertex exploration in the vertex model, where the agent sees which neighbours are already visited, it walks only the edges of the DFS tree, each twice: $2(n - 1)$ moves.
- **Panaite and Pelc.** An edge exploration of an undirected graph with at most $m + 3n$ moves, so with penalty $O(n)$, independent of $m$. For dense graphs, this is close to $m$, while DFS uses $2m$.
- **Eulerian digraphs.** On a strongly connected directed graph with deficiency 0, Deng and Papadimitriou give an algorithm with at most $2m$ moves, a ratio of 2.
- **Digraphs of deficiency $d$.** Deng and Papadimitriou show that a ratio that depends only on $d$ is possible, and Albers and Henzinger give an algorithm with $d^{O(\log d)} m$ moves.
- **Weighted vertex exploration.** The greedy rule "go to the nearest unvisited vertex that is known" is the online form of the [nearest-neighbour heuristic](/nearest-neighbor-tsp/); its ratio grows like $\log n$. Kalyanasundaram and Pruhs give the algorithm ShortCut, with a constant ratio on planar graphs.
- **Random walk.** An agent with no memory that moves along a random edge at each step visits all vertices of a connected undirected graph in expected time at most $2m(n - 1)$, by the cover time bound of Aleliunas, Karp, Lipton, Lovász and Rackoff.

## Bounds

**DFS is 2-competitive for unweighted vertex exploration.** In the vertex model, DFS uses at most $2(n - 1)$ moves, and any walk that visits $n$ vertices has at least $n - 1$ moves, because each move adds at most one new vertex. So the ratio is less than 2. With return to $s$, a closed walk through $n \ge 2$ vertices has at least $n$ moves, so the ratio is still below 2. On a tree, every closed walk through all vertices walks each edge twice, so DFS is optimal on trees.

**Edge exploration of undirected graphs.** Every exploration walks each edge, so $\mathrm{OPT} \ge m$, and DFS has ratio at most 2. The star example gives penalty at least $n - 2$ for every algorithm, and the algorithm of Panaite and Pelc has penalty at most $3n$. So the best possible penalty is $\Theta(n)$, and the best ratio tends to 1 on graphs with $m / n \to \infty$.

**Directed graphs.** The deficiency controls the difficulty. With $d = 0$, a ratio of 2 is possible. For general $d$, the best known upper bound is $d^{O(\log d)}$, and no algorithm has a ratio that does not grow with $d$.

**Weighted graphs.** Whether some online algorithm has a constant ratio for vertex exploration on all weighted undirected graphs is an open question. Constant ratios are known for planar graphs, and the nearest-neighbour rule has ratio $\Theta(\log n)$ in the worst case.

**Lower bound by an adversary.** The online agent knows nothing about the part of the graph that it has not seen, so an adversary may build that part as the agent moves. The star example is of this kind: the adversary decides which leaf the agent reaches last only after the agent has chosen its order.

## Reductions

- **Offline edge exploration is the Chinese postman problem.** In a known undirected graph, the shortest closed walk that uses every edge is the [Chinese postman problem](/chinese-postman-problem/), which is solvable in polynomial time by matching. Its value is $m$ plus the length of the cheapest set of paths that pairs up the vertices of odd degree.
- **Offline vertex exploration is the travelling salesman problem.** In a known graph with lengths, the shortest closed walk through all vertices is the [travelling salesman problem](/traveling-salesman-problem/) in the graph metric. It is NP-hard, which is one reason why exploration is judged by the competitive ratio and not by exact optimality.
- **Exploration solves reachability.** An exploration from $s$ visits exactly the vertices reachable from $s$, so it solves [graph reachability](/graph-reachability/). With limited memory, the random walk and universal traversal sequences give space-bounded algorithms for undirected reachability.

## Applications

- **Robots.** Mapping a building, a cave or a network of pipes by a robot that sees only its surroundings.
- **Web crawling and network discovery.** A crawler or a mobile software agent learns the links of a page or a host only when it is there.
- **Mazes.** The Trémaux rule and the wall follower are the classical exploration rules for mazes.
- **Space-bounded computation.** Random walks and universal traversal sequences, which explore any graph from a family without memory, are tools for the space complexity of reachability.

## References
