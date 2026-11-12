---
tag: 01DVEW
kind: problem
slug: enumerating-simple-paths
name: Enumerating simple paths
aliases:
- listing all simple s-t paths
area: graphs/paths-and-cycles
level: advanced
summary: "List all simple paths between two given vertices. Backtracking with a reachability test gives polynomial delay; counting the paths is #P-complete."
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the number of s-t paths}
  time: {worst: O(n + m + m N)}
prereqs: [simple-path, enumeration-problem, output-sensitive-enumeration]
see_also: [read-tarjan-path-enumeration, enumerating-elementary-cycles, yen-k-shortest-paths, k-shortest-paths, counting-fixed-length-paths, longest-path-problem, generic-backtracking-algorithm, graph-reachability]
sources:
  - paper: "R. C. Read and R. E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3), 237 to 252 (1975)"
    locator: the whole paper (s-t paths in O(n + m + mN) time and O(n + m) space)
  - paper: "Etienne Birmelé, Rui Ferreira, Roberto Grossi, Andrea Marino, Nadia Pisanti, Romeo Rizzi and Gustavo Sacomoto, Optimal listing of cycles and st-paths in undirected graphs, Proceedings of the 24th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1884 to 1896 (2013)"
    locator: the whole paper (s-t paths of an undirected graph in time linear in the input plus the total length of the output)
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421 (1979)
    locator: "the whole paper (counting s-t paths is #P-complete)"
  - paper: doi:10.1287/mnsc.17.11.712
    title: Jin Y. Yen, Finding the k shortest loopless paths in a network, Management Science 17(11), 712 to 716 (1971)
    locator: the whole paper (the k shortest simple paths)
---

The problem asks for a list of every simple path from a vertex $s$ to a vertex $t$ in a [graph](/graph/), each once. There can be exponentially many, so algorithms are measured by their [output-sensitive](/output-sensitive-enumeration/) cost. A [backtracking](/generic-backtracking-algorithm/) search that extends the current path only to vertices from which $t$ can still be reached never enters a dead end, so it spends polynomial time per path; the [Read-Tarjan algorithm](/read-tarjan-path-enumeration/) does this in $O(n + m + mN)$ time for $N$ paths. Counting the paths without listing them is #P-complete, and finding a longest one is NP-hard.

## In plain words

Write down every route from home to work that never passes the same place twice. A computer can try routes one step at a time and step back when it is stuck. The trouble is that it can get stuck very often, in parts of the map from which work cannot be reached without going back through places already used.

The fix is to look ahead: before each step, check that work can still be reached from the next place without using the places already on the route. Then every step that the search takes leads to at least one complete route, and no time is wasted on dead ends.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n$ vertices and $m$ edges, directed or undirected, and two vertices $s$ and $t$.

**Output.** Every simple path from $s$ to $t$, each exactly once. A simple path is a walk $s = v_0, e_1, v_1, \ldots, e_k, v_k = t$ with distinct vertices; in a directed graph each $e_i$ goes from $v_{i-1}$ to $v_i$.

**Conventions.** If $s = t$, the only simple path is the path of length 0. [Self-loops](/self-loop/) never lie on a simple path. With parallel edges, paths are told apart by their edges, so a path through a pair of vertices joined by $p$ parallel edges counts $p$ times; many implementations work with vertex sequences and simple graphs, and multiply afterwards. Isolated vertices and vertices that cannot lie on an $s$-$t$ path have no effect.

## Variants

- **All simple paths from $s$.** To every vertex, or of a given length.
- **Bounded length.** Only paths with at most $k$ edges; the reachability test then uses distances.
- **$k$ shortest simple paths.** List the paths in order of weight and stop after $k$; [Yen's algorithm](/yen-k-shortest-paths/) does this with $k$ times $n$ shortest path computations. Without the simplicity condition, see [$k$ shortest paths](/k-shortest-paths/).
- **Counting.** Return the number $N$; #P-complete in general.
- **Cycles.** The cycles through an edge $uv$ are the $v$-$u$ paths of $G - uv$ closed by that edge; see [enumerating elementary cycles](/enumerating-elementary-cycles/).

## Examples

**The diamond.** The undirected graph with edges $01, 12, 23, 30, 02$ (a 4-cycle with the chord $02$) has four simple paths from $1$ to $3$: $1, 0, 3$; $1, 2, 3$; $1, 0, 2, 3$; and $1, 2, 0, 3$.

**Complete graphs.** In $K_n$ a simple $s$-$t$ path is an ordered choice of $k$ inner vertices from the other $n - 2$, for $k = 0, \ldots, n - 2$, so

$$N = \sum_{k=0}^{n-2} \frac{(n-2)!}{(n-2-k)!} = \lfloor e \cdot (n-2)! \rfloor \quad (n \ge 3),$$

which is $2, 5, 16, 65$ for $n = 3, 4, 5, 6$. This grows faster than any exponential $c^n$.

**Grids.** In the directed $a \times b$ grid with arcs right and down, every path is simple, and the number of paths between opposite corners is $\binom{a + b - 2}{a - 1}$; see [counting lattice paths](/counting-lattice-paths/).

**No path.** If $t$ is not reachable from $s$, $N = 0$, and a good algorithm notices this in $O(n + m)$ time.

**Dead ends.** Take a path $s, x, t$, and attach to $x$ a large part from which $t$ cannot be reached except through $x$. Plain backtracking explores every simple path inside that part, which can be exponentially many, before it finds the single answer. The reachability test rejects the whole part at once.

## Known algorithms

| algorithm | graphs | time | space |
|---|---|---|---|
| plain backtracking | both | exponential per path in the worst case | $O(n + m)$ |
| backtracking with a reachability test | both | $O(n(n + m))$ per path, polynomial delay | $O(n + m)$ |
| [Read and Tarjan](/read-tarjan-path-enumeration/) (1975) | both | $O(n + m + mN)$ | $O(n + m)$ |
| Birmelé and others (2013) | undirected | $O(m + \sum_P \lvert P \rvert)$, optimal | $O(n + m)$ |

**Backtracking with a reachability test.** Keep the current path from $s$ to $u$. For each edge from $u$ to a vertex $v$ not on the path, recurse into $v$ only if $t$ is [reachable](/graph-reachability/) from $v$ in $G$ minus the vertices of the path. Each recursive call then leads to at least one output, and a path has at most $n$ vertices, so between two outputs the search makes $O(n)$ calls, each with $O(n + m)$ work. Read and Tarjan arrange the tests so that the total work is $O(m)$ per path.

## Bounds

**Output.** Any algorithm needs $\Omega(n + m + \sum_P |P|)$ time to read the input and write the output. For undirected graphs this is achieved; for directed graphs the best general bound is of the form $O(m)$ per path.

**Number of paths.** As $K_n$ shows, $N$ can be about $e \cdot (n-2)!$, so no algorithm is polynomial in $n$ alone.

**Counting.** Valiant (1979) proved that counting $s$-$t$ paths is #P-complete, for directed and undirected graphs. So there is no polynomial algorithm for $N$ unless every #P function is polynomial, and listing, in time at least $N$, is the practical way to count when $N$ is small.

**Longest path.** A path with $n - 1$ edges is a Hamiltonian path, so finding a longest simple $s$-$t$ path is NP-hard; see the [longest path problem](/longest-path-problem/). Listing all paths solves it in time proportional to $N$, which is fine only when $N$ is small.

## Reductions

- **Restriction to useful vertices.** Delete every vertex that is not reachable from $s$ or cannot reach $t$; in a directed graph this is two searches. In an undirected graph, the useful part is the chain of [biconnected components](/biconnected-components/) between $s$ and $t$ in the block-cut tree.
- **Hamiltonian path to counting.** Counting $s$-$t$ paths with exactly $n - 1$ edges decides the Hamiltonian $s$-$t$ path problem, so counting by length is NP-hard.
- **Cycles to paths.** Listing cycles reduces to listing paths, one edge at a time, as above.

## Applications

- **Network reliability.** The probability that $s$ and $t$ stay connected when edges fail can be computed from the list of $s$-$t$ paths by inclusion and exclusion; Valiant's paper shows that this is also #P-hard in general.
- **Routing.** Lists of alternative loop-free routes, often with a length bound, for traffic and communication networks.
- **Program analysis and testing.** All acyclic paths through a control-flow graph, for path coverage.
- **Biology and knowledge graphs.** All short paths between two entities, used to explain a connection.

## References
