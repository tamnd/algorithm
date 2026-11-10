---
tag: 95C34P
kind: problem
slug: online-graph-exploration-problem
name: Online graph exploration problem
aliases:
- graph exploration
- online exploration of an unknown graph
- online TSP in unknown graphs
area: online-and-streaming/competitive-analysis
level: advanced
summary: An explorer starts at a vertex of an unknown weighted graph, learns the edges at each vertex it visits, and must visit all vertices and return with little travel.
prereqs: [graph-exploration, competitive-ratio, online-algorithm, depth-first-search]
see_also: [nearest-neighbor-tsp, online-traveling-salesman-problem, traveling-salesman-problem, planar-graph, graph-genus, tremaux-traversal, linear-search-problem, online-dial-a-ride-problem]
sources:
  - paper: "Bala Kalyanasundaram and Kirk R. Pruhs, Constructing competitive tours from local information, Theoretical Computer Science 130(1) (1994), 125-138"
    title: "Kalyanasundaram and Pruhs, Constructing competitive tours from local information (1994)"
    locator: the fixed graph model, the algorithm ShortCut, and its 16-competitive bound on planar graphs
  - paper: "Nicole Megow, Kurt Mehlhorn and Pascal Schweitzer, Online graph exploration: new results on old and new algorithms, Theoretical Computer Science 463 (2012), 62-72"
    title: "Megow, Mehlhorn and Schweitzer, Online graph exploration: new results on old and new algorithms (2012)"
    locator: the algorithm Blocking, the bound 16(1 + 2g) for graphs of genus g, and the 2k-competitive algorithm hDFS for graphs with k distinct edge weights
  - paper: "Shuichi Miyazaki, Naoyuki Morimoto and Yasuo Okabe, The online graph exploration problem on restricted graphs, IEICE Transactions on Information and Systems E92-D(9) (2009)"
    title: "Miyazaki, Morimoto and Okabe, The online graph exploration problem on restricted graphs (2009)"
    locator: the tight bound (1 + sqrt 3)/2 on cycles and the lower bound 2 for unweighted graphs
  - paper: "Daniel J. Rosenkrantz, Richard E. Stearns and Philip M. Lewis II, An analysis of several heuristics for the traveling salesman problem, SIAM Journal on Computing 6(3) (1977)"
    title: "Rosenkrantz, Stearns and Lewis, An analysis of several heuristics for the traveling salesman problem (1977)"
    locator: the O(log n) bound for the nearest neighbor rule
  - paper: "Alexander Birx, Yann Disser, Alexander V. Hopp and Christina Karousatou, An improved lower bound for competitive graph exploration, Theoretical Computer Science (2021)"
    title: "Birx, Disser, Hopp and Karousatou, An improved lower bound for competitive graph exploration (2021)"
    locator: the lower bound 10/3 for general weighted graphs
---

The online graph exploration problem asks an explorer, or a robot, to visit every vertex of an unknown graph and return to the start, while it walks as little as possible. The graph is undirected, connected and has nonnegative edge weights. At the start, the explorer knows only its own vertex. When it reaches a vertex, it learns all edges at that vertex, their weights, and the names of their other ends. The cost is the total weight walked, and it is compared with the shortest closed walk that visits all vertices, which an offline explorer that knows the graph could take. Kalyanasundaram and Pruhs (1994) gave a $16$-competitive algorithm for planar graphs. For general graphs, the nearest neighbor rule is $\Theta(\log n)$-competitive, and whether a constant ratio is possible is a famous open question. The best known lower bound for deterministic algorithms is $10/3$.

The offline problem of visiting all vertices of a known graph is the [traveling salesman problem](/traveling-salesman-problem/) in the shortest path metric. Offline traversal methods are on the [graph exploration](/graph-exploration/) page.

## In plain words

A robot is placed in a building with no map. In each room it can see the doors and the length of each corridor, and it can tell whether it has been in the next room before. It must visit every room and come back to the start.

With a map, the robot would plan the shortest round trip. Without one, it must guess which corridor to try next. A robot that always walks to the nearest room it has not seen yet can be fooled into long walks back and forth. A careful rule that sometimes skips a short corridor to avoid a long one works well in buildings whose map can be drawn without crossings. No one knows whether some rule works well in every building.

## Definition

**Notation.**

| Symbol | Meaning |
|---|---|
| $G = (V, E)$, $w$ | the unknown graph, undirected and connected, with nonnegative edge weights |
| $n$ | the number of vertices |
| $s$ | the start vertex |
| $d$ | the shortest path distance in $G$ |
| $\mathrm{ALG}(G)$ | the total weight of the walk of the explorer |
| $\mathrm{OPT}(G)$ | the weight of a shortest closed walk from $s$ that visits all vertices, which is the optimal TSP tour in the metric $d$ |

**Input.** The start vertex $s$. When the explorer is at a vertex $v$ for the first time, it learns each edge $\{v, u\}$, its weight $w(v, u)$, and a unique label of $u$. This is the *fixed graph* model of Kalyanasundaram and Pruhs. The explorer has unlimited memory.

**Output.** A closed walk from $s$ in $G$ that visits every vertex. The explorer may move only along edges, and it decides each step with the knowledge it has so far.

**Cost.** $\mathrm{ALG}(G) = $ the total weight of the walk, counted with repetitions.

**Competitive ratio.** A deterministic algorithm is $c$-competitive on a class of graphs if $\mathrm{ALG}(G) \le c \cdot \mathrm{OPT}(G)$ for every graph $G$ of the class and every start vertex, with additive constant $0$. The class matters a lot: trees, cycles, planar graphs and graphs of bounded genus have different answers.

## Variants

- **Unweighted graphs.** All edges have weight $1$. Depth-first search is $2$-competitive (Theorem 2), and Miyazaki, Morimoto and Okabe proved that no deterministic algorithm is better than $2$.
- **Trees.** Depth-first search walks each edge twice, and so does every closed walk that visits all leaves. It is optimal (Theorem 2).
- **Cycles.** Miyazaki, Morimoto and Okabe showed that the best ratio on weighted cycles is $(1 + \sqrt 3)/2 \approx 1.37$.
- **Planar graphs and bounded genus.** Kalyanasundaram and Pruhs gave the algorithm ShortCut, which is $16$-competitive on planar graphs. Megow, Mehlhorn and Schweitzer gave a generalized version, Blocking, which is $16(1 + 2g)$-competitive on graphs of genus $g$; see [graph genus](/graph-genus/).
- **Few distinct weights.** If the edge weights take only $k$ distinct values, the algorithm hierarchical DFS of Megow, Mehlhorn and Schweitzer is $2k$-competitive.
- **Directed graphs.** In a strongly connected directed graph, the explorer must also find a way back. The cost of exploring all edges then depends on how far the graph is from being Eulerian, as studied by Deng and Papadimitriou and by Albers and Henzinger.
- **Exploring all edges.** If every edge must be walked, as in the [Tremaux traversal](/tremaux-traversal/) of a maze, depth-first search walks each edge exactly twice. Every such walk has weight at least $w(E)$, so this is $2$-competitive, also with weights.
- **Open version and search.** The explorer may stop at the last new vertex, or it must find one target vertex, as in the [linear search problem](/linear-search-problem/) on a line.

## Examples

**A cycle.** Let $G$ be a cycle of $n$ unit edges, with $s$ on it. Depth-first search walks around the cycle to the last vertex, and then backtracks along its search tree, for a total of $2(n - 1)$. The nearest neighbor rule walks around the cycle and then takes the last edge back to $s$, for a total of $n$, which is optimal. So depth-first search has ratio $2(n - 1)/n$, close to $2$, on cycles.

**Depth-first search on weights.** Take a triangle on $s, u, v$ with $w(s, u) = w(u, v) = 1$ and $w(s, v) = W \ge 2$. A depth-first search that tries the edge to $v$ first walks $s \to v \to u$, backtracks $u \to v \to s$, and pays $2W + 2$. The nearest neighbor rule walks $s \to u \to v$ and returns along the known path $v \to u \to s$, for a total of $4$, which is optimal. So depth-first search has ratio $(W + 1)/2$ here, which is unbounded.

## Known algorithms

- **Depth-first search.** Explore an unvisited neighbor if there is one, and otherwise go back to the parent. It walks each edge of its search tree twice, so its cost is twice the weight of a spanning tree that it cannot choose. It is $2$-competitive on unweighted graphs and optimal on trees, but not competitive on weighted graphs: a heavy edge to a vertex that is also reachable by a cheap path can be taken first.
- **Nearest neighbor.** Go to the nearest unvisited vertex along a shortest path in the known part of the graph. It is the online version of the [nearest neighbor TSP heuristic](/nearest-neighbor-tsp/), with the same tours (Lemma 1), so it costs at most $\tfrac12 (\lceil \log_2 n \rceil + 1)\,\mathrm{OPT}$ (Rosenkrantz, Stearns and Lewis 1977), and some graphs force $\Omega(\log n)$ (Hurkens and Woeginger 2004).
- **ShortCut and Blocking.** Kalyanasundaram and Pruhs (1994), and Megow, Mehlhorn and Schweitzer (2012). The explorer follows depth-first search but does not take an edge $e$ to a new vertex if there is a *blocking* edge: a shorter edge to an unvisited vertex whose end is within a constant factor of $w(e)$ from the start of $e$. With the right constant, Blocking is $16(1 + 2g)$-competitive on graphs of genus $g$. On general graphs, Megow, Mehlhorn and Schweitzer showed that Blocking is not constant-competitive.
- **Hierarchical DFS.** Run depth-first search on the edges of the smallest weight class, then allow the next class, and so on. It is $2k$-competitive for $k$ weight classes.

## Bounds

| Graph class | Lower bound | Upper bound |
|---|---|---|
| general weighted graphs | $10/3$ (Birx, Disser, Hopp and Karousatou 2021); earlier $5/2$ (Dobrev, Kralovic and Markou 2012) | $O(\log n)$, nearest neighbor (Rosenkrantz, Stearns and Lewis 1977) |
| planar graphs | | $16$ (Kalyanasundaram and Pruhs 1994) |
| graphs of genus $g$ | | $16(1 + 2g)$ (Megow, Mehlhorn and Schweitzer 2012) |
| $k$ distinct edge weights | | $2k$ (Megow, Mehlhorn and Schweitzer 2012) |
| unweighted graphs | $2$ (Miyazaki, Morimoto and Okabe 2009) | $2$, depth-first search |
| cycles | $(1 + \sqrt 3)/2$ (Miyazaki, Morimoto and Okabe 2009) | $(1 + \sqrt 3)/2$ (Miyazaki, Morimoto and Okabe 2009) |
| trees | $1$ | $1$, depth-first search |

The lower bounds are for deterministic algorithms. A 2026 preprint claims a lower bound of $4$ for general graphs. For the nearest neighbor rule alone, the ratio is $\Theta(\log n)$ in the worst case.

**Lemma 1 (nearest neighbor sees enough).** Let the explorer be at $u$, and let $v$ be an unvisited vertex with the smallest $d(u, v)$. Then every vertex before $v$ on a shortest path from $u$ to $v$ is visited. So the explorer knows this path, and the online nearest neighbor rule makes the same choices as the offline nearest neighbor heuristic in the metric $d$, when ties are broken in the same way.

*Proof.* Assume that all weights are positive; edges of weight $0$ can be contracted first. Let $x$ be a vertex before $v$ on a shortest path $P$ from $u$ to $v$. Then $d(u, x) < d(u, v)$, so $x$ is visited by the choice of $v$. The explorer has seen all edges at visited vertices, so it knows every edge of $P$, including the last one, from a visited vertex to $v$. When all vertices are visited, the return to $s$ along a shortest path also uses known edges only. $\square$

**Theorem 2 (depth-first search).** On trees, depth-first search is optimal. On unweighted connected graphs with $n \ge 2$ vertices, it is $2$-competitive, and $\mathrm{ALG} = 2(n - 1) < 2\,\mathrm{OPT}$.

*Proof.* Depth-first search walks each edge of its search tree $T$ twice, once down and once back, and no other edge. So $\mathrm{ALG} = 2 w(T)$. On a tree, $T = G$, and every closed walk from $s$ that visits all vertices uses each edge at least twice, because removing an edge splits the tree and the walk must cross into the far side and back. So $\mathrm{OPT} = 2 w(G) = \mathrm{ALG}$. On an unweighted graph, $\mathrm{ALG} = 2(n - 1)$, and a closed walk that visits $n \ge 2$ distinct vertices has at least $n$ edges, so $\mathrm{OPT} \ge n$. $\square$

## Reductions

- **From offline TSP.** If the whole graph is known, the problem is the [traveling salesman problem](/traveling-salesman-problem/) in the shortest path metric. The online explorer may compute anything, so the online bounds come only from the missing information.
- **Relation to online TSP.** In the [online traveling salesman problem](/online-traveling-salesman-problem/), the points are revealed by time, while here they are revealed by the position of the explorer. Both compare the cost with an offline TSP tour.
- **Relation to search.** Finding one hidden vertex instead of all of them gives search problems such as the [linear search problem](/linear-search-problem/), where doubling strategies are the main tool.

## Applications

- **Robot exploration.** A mobile robot maps an unknown building or cave, where rooms are vertices and corridors are edges.
- **Network discovery.** A crawler or a mobile agent visits all nodes of a network, where it learns the links only at the nodes it reaches.
- **Maze solving.** Exploring all rooms of a maze, as in [Tremaux traversal](/tremaux-traversal/), is the unweighted case.

## References
