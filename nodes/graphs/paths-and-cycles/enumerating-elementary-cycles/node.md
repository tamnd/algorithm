---
tag: GRY838
kind: problem
slug: enumerating-elementary-cycles
name: Enumerating elementary cycles
aliases:
- listing all simple cycles
area: graphs/paths-and-cycles
level: advanced
summary: List every simple cycle of a directed or undirected graph. Johnson's algorithm takes O((n + m)(c + 1)) time for c cycles; optimal output-sensitive bounds exist for undirected graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, c: the number of cycles}
  time: {worst: O((n + m)(c + 1))}
prereqs: [simple-cycle, enumeration-problem, output-sensitive-enumeration]
see_also: [johnson-elementary-cycles-algorithm, enumerating-simple-paths, read-tarjan-path-enumeration, cycle-detection-in-graph, cycle-basis, strongly-connected-components, generic-backtracking-algorithm, counting-fixed-length-paths]
sources:
  - paper: doi:10.1137/0204007
    title: Donald B. Johnson, Finding all the elementary circuits of a directed graph, SIAM Journal on Computing 4(1), 77 to 84 (1975)
    locator: the whole paper (O((n + e)(c + 1)) time and O(n + e) space)
  - paper: doi:10.1137/0202017
    title: Robert Tarjan, Enumeration of the elementary circuits of a directed graph, SIAM Journal on Computing 2(3), 211 to 216 (1973)
    locator: the whole paper (backtracking with marked vertices, O(n e (c + 1)) time)
  - paper: doi:10.1145/362814.362819
    title: James C. Tiernan, An efficient search algorithm to find the elementary circuits of a graph, Communications of the ACM 13(12), 722 to 726 (1970)
    locator: the whole paper (plain backtracking, exponential time per circuit in the worst case)
  - paper: "R. C. Read and R. E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3), 237 to 252 (1975)"
    locator: the whole paper (cycles of undirected graphs in O(n + m + mc) time and O(n + m) space)
  - paper: "Etienne Birmelé, Rui Ferreira, Roberto Grossi, Andrea Marino, Nadia Pisanti, Romeo Rizzi and Gustavo Sacomoto, Optimal listing of cycles and st-paths in undirected graphs, Proceedings of the 24th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1884 to 1896 (2013)"
    locator: the whole paper (cycles of an undirected graph in time proportional to the input plus the total length of the output)
---

The problem asks for a list of every elementary (simple) cycle of a [graph](/graph/): every closed walk that repeats no vertex, each listed once. The number $c$ of cycles can be exponential in $n$, so the algorithms are judged by their [output-sensitive](/output-sensitive-enumeration/) cost. [Johnson's algorithm](/johnson-elementary-cycles-algorithm/) lists the cycles of a directed graph in $O((n + m)(c + 1))$ time and $O(n + m)$ space, and for undirected graphs there are algorithms whose time is linear in the input plus the total length of the output. Counting the cycles, without listing them, is #P-complete.

## In plain words

Find every round trip in a network that never passes the same point twice, and write each one down once. There can be a huge number of them, so the time to write them all is unavoidable. A good method spends only a little extra time for each trip it writes.

The simple way is to try every route from each point and back, but it can waste a lot of time in dead ends that lead to no round trip at all. The good methods remember which points cannot lead back, and they do not try them again until something changes.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n$ vertices and $m$ edges, directed or undirected.

**Output.** Every elementary cycle of $G$, each exactly once. An elementary cycle of length $k \ge 1$ is a closed walk $v_0, e_1, v_1, \ldots, e_k, v_0$ with distinct vertices $v_0, \ldots, v_{k-1}$ and distinct edges. Two closed walks that differ only by the start vertex, or, in an undirected graph, only by the direction, are the same cycle.

**Conventions for multigraphs.** A [self-loop](/self-loop/) is a cycle of length 1. In a directed graph, $u \to v \to u$ is a cycle of length 2. In an undirected graph, two parallel edges between $u$ and $v$ form a cycle of length 2, and one edge used back and forth is not a cycle. When there are parallel edges, cycles are distinguished by their edge sets, so $k$ parallel edges give $\binom{k}{2}$ cycles of length 2, and each cycle through a vertex sequence with parallel choices counts once for each choice. Many implementations take simple graphs and list vertex sequences; they must be given the multiplicities separately.

**Cost model.** An algorithm has total time $O(f(n, m) \cdot (c + 1))$ if its time is linear in the number of cycles; it has *polynomial delay* if the time between two consecutive outputs is polynomial. Writing the output costs $\Theta(\sum_C |C|)$, which is a lower bound.

## Variants

- **Directed or undirected.** Undirected graphs allow better bounds, because every edge that is not a [bridge](/bridge/) lies on a cycle.
- **Cycles through a given vertex or edge.** The same algorithms with a fixed start.
- **Cycles of bounded length.** List only cycles with at most $k$ edges; used in fraud detection and in chemistry.
- **Chordless (induced) cycles.** List cycles with no chord; there are separate output-sensitive algorithms.
- **Counting.** Return $c$ without listing; #P-complete (see Bounds).
- **Simple paths.** The related problem of listing all simple $s$-$t$ paths; see [enumerating simple paths](/enumerating-simple-paths/). An algorithm for one gives one for the other: the cycles through an edge $uv$ are the $v$-$u$ paths of $G - uv$ closed by that edge.

## Examples

**$K_4$ undirected.** The cycles are the 4 triangles and the 3 four-cycles $0123$, $0132$ and $0213$: 7 cycles.

**Complete graphs.** $K_n$ has $\sum_{k=3}^{n} \binom{n}{k} \frac{(k-1)!}{2}$ cycles, choosing $k$ vertices and a cyclic order up to direction: $1, 7, 37, 197$ for $n = 3, 4, 5, 6$. The complete directed graph on $n$ vertices, with both arcs between every pair, has $\sum_{k=2}^{n} \binom{n}{k} (k-1)!$ cycles: $5, 20, 84, 409$ for $n = 3, 4, 5, 6$. These grow like $(n-1)!$, far more than any polynomial.

**A directed graph.** The arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $1 \to 0$ and a loop $2 \to 2$ have three cycles: $0 \to 1 \to 0$, $0 \to 1 \to 2 \to 0$ and the loop at 2.

**No cycles.** A directed acyclic graph, a forest, or a graph of isolated vertices has $c = 0$; the algorithms then take $O(n + m)$ time.

**A bad case for plain backtracking.** Take a directed cycle $0 \to 1 \to 0$ and attach to vertex 1 a large acyclic part that every search enters but that never leads back. The graph has one cycle, but a search that does not remember dead ends explores all paths of the acyclic part, which can be exponentially many. Johnson's blocking rule explores them only once.

## Known algorithms

| algorithm | graphs | time | space |
|---|---|---|---|
| Tiernan (1970), plain backtracking | directed | exponential per cycle in the worst case | $O(n + m)$ |
| Tarjan (1973), marking | directed | $O(nm(c + 1))$ | $O(n + m)$ |
| [Johnson](/johnson-elementary-cycles-algorithm/) (1975), blocking | directed | $O((n + m)(c + 1))$ | $O(n + m)$ |
| Read and Tarjan (1975) | undirected | $O(n + m + mc)$ | $O(n + m)$ |
| Birmelé and others (2013) | undirected | $O(m + \sum_C \lvert C \rvert)$, optimal | $O(n + m)$ |
| cycle space search | both | exponential in $m - n + 1$ | |

**Johnson's algorithm.** Order the vertices. For each vertex $s$ in turn, take the [strongly connected component](/strongly-connected-components/) of $s$ in the subgraph induced by $s$ and the later vertices, and list the cycles whose least vertex is $s$ by a [backtracking](/generic-backtracking-algorithm/) search from $s$. A vertex on the current path is *blocked*. When the search returns from a vertex $v$ without finding a cycle, $v$ stays blocked, and it is recorded in the lists $B[w]$ of its out-neighbours $w$. It is unblocked, recursively through these lists, only when one of those neighbours is unblocked because it reached $s$. This guarantees that between two outputs, or between the start and the first output, the search does $O(n + m)$ work.

**Cycle space.** Every cycle is a sum of elements of a [cycle basis](/cycle-basis/), so one can test all $2^{m - n + 1}$ sums and keep those that are cycles. This is slow in general but fast when $m - n$ is small.

## Bounds

**Lower bound.** Any algorithm must write the output, so it needs $\Omega(n + m + \sum_C |C|)$ time, and the result of Birmelé and others meets this bound for undirected graphs. For directed graphs, Johnson's bound can exceed the output size by a factor of order $n + m$ when the cycles are short.

**Number of cycles.** $c$ is larger than $(n-1)!$ in the complete directed graph on $n$ vertices, since the Hamiltonian cycles alone number $(n-1)!$, so no algorithm is polynomial in $n$ alone.

**Counting.** Valiant (1979) showed that counting the simple cycles of a directed graph is #P-complete; the same holds for undirected graphs. So there is no polynomial time counting method unless every #P function is computable in polynomial time, and the listing algorithms, which take time at least $c$, are the practical way to count when $c$ is small. With the length $k$ as parameter, counting cycles of length $k$ is #W[1]-complete (Flum and Grohe 2004), see [counting fixed-length paths](/counting-fixed-length-paths/).

**Longest and Hamiltonian cycles.** Deciding whether some cycle has length $n$ is the NP-complete Hamiltonian cycle problem, so finding the longest cycle cannot be done fast by listing unless $c$ is small.

## Reductions

- **Cycles to $s$-$t$ paths.** For each edge $e = uv$ in a fixed order, list the $v$-$u$ paths in $G$ minus $e$ and the edges before it; each, closed by $e$, is a cycle whose first edge in the order is $e$, so every cycle appears once.
- **Restriction to strong components.** A directed cycle lies inside one strongly connected component, so the components can be processed independently, and arcs between components are deleted first. In an undirected graph, cycles lie inside one [biconnected component](/biconnected-components/).
- **Hamiltonian cycle to counting.** The number of cycles of length $n$ is positive if and only if a Hamiltonian cycle exists, so counting cycles by length is NP-hard.

## Applications

- **Deadlock and dependency analysis.** List all cycles of a [wait-for graph](/wait-for-graph/) or of a dependency graph to show every circular dependency, not just one.
- **Circuit and program analysis.** Feedback loops in digital circuits and loops in control-flow graphs.
- **Chemistry and biology.** Ring structures of molecules, feedback loops in gene regulatory and metabolic networks.
- **Finance.** Cycles of transactions in money laundering and arbitrage detection, usually with bounded length.

## References
