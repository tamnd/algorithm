---
tag: 4QZM2W
kind: problem
slug: cycle-detection
name: Cycle detection
aliases:
- detecting cycles
area: graphs/paths-and-cycles
level: intro
summary: Decide whether a graph contains a cycle, for directed or undirected graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [simple-cycle, directed-and-undirected-graphs, depth-first-search]
see_also: [dfs-cycle-detection, cycle-detection-in-graph, topological-ordering-theorem, kahns-algorithm, dag-source-lemma, union-find-connectivity, girth, floyd-cycle-detection]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (classification of edges; an undirected DFS has only tree and back edges) and Section 20.4, Topological sort (a directed graph is acyclic if and only if a DFS yields no back edges); Exercise 20.4-3 (an O(V) test for a cycle in an undirected graph)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3.2, Directed acyclic graphs (a directed graph has a cycle if and only if its DFS reveals a back edge)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (cycle detection with DFS) and Section 4.2, Directed graphs (directed cycle detection and the class DirectedCycle)
  - paper: "Arthur B. Kahn, Topological sorting of large networks, Communications of the ACM 5(11), 558 to 562 (1962)"
    locator: the whole paper (repeated removal of vertices with no predecessors; left-over vertices signal a cycle)
---

Cycle detection is the problem of deciding whether a [graph](/graph/) has a cycle: a closed walk of at least one edge that repeats no vertex and no edge. For a [directed graph](/directed-graph/) the cycle must follow the edge directions, and the graphs with no directed cycle are the [directed acyclic graphs](/directed-acyclic-graph/); for an [undirected graph](/undirected-graph/) the graphs with no cycle are the forests. Both versions take $\Theta(n + m)$ time by one [depth-first search](/depth-first-search/), and the undirected version even takes only $O(n)$ time, because a graph with $n$ or more edges always has a cycle. This page is about the yes or no question; returning the cycle itself is the problem [finding a cycle in a graph](/cycle-detection-in-graph/).

## In plain words

You have a set of points and arrows between them, and you want to know whether you can start at a point, follow arrows, and come back to the same point. Such a loop can be a bug: tasks that each wait for the next one, files that include each other, cells of a spreadsheet that depend on each other.

The usual method walks as deep as it can. It keeps track of the points on the current route. If an arrow leads back to a point that is still on the current route, there is a loop. If the walk ends everywhere without that event, there is no loop. For lines without arrows, it is even easier: lines that form no loop are few, fewer than the points.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n = |V|$ and $m = |E|$ in adjacency lists. $G$ is directed or undirected, and it may be a [multigraph](/multigraph/) with parallel edges and [self-loops](/self-loop/).

**Cycles.** A *cycle* is a closed walk $(v_0, e_1, v_1, \ldots, e_k, v_k = v_0)$ with $k \ge 1$, pairwise distinct edges $e_1, \ldots, e_k$, and pairwise distinct vertices $v_0, \ldots, v_{k-1}$. In a directed graph each $e_i$ goes from $v_{i-1}$ to $v_i$. So:

- a self-loop is a cycle of length 1, in both kinds of graph;
- in an undirected graph, two parallel edges between $u$ and $v$ form a cycle of length 2, but one edge used twice, $u \to v \to u$, is not a cycle, because its edges are not distinct;
- in a directed graph, the two edges $u \to v$ and $v \to u$ form a cycle of length 2, while two parallel edges $u \to v$ do not form a cycle.

**Output.** "yes" if $G$ has a cycle, else "no". An undirected graph has no cycle exactly when it is a forest; a directed graph has no cycle exactly when it is a DAG.

**Equivalent forms, directed.** By the [topological ordering theorem](/topological-ordering-theorem/), these are equivalent: $G$ has no directed cycle; $G$ has a [topological ordering](/topological-ordering/); one (or every) depth-first search of $G$ finds no back edge; every nonempty set of vertices induces a subgraph with a source (the [DAG source lemma](/dag-source-lemma/)).

**Equivalent forms, undirected.** $G$ has no cycle if and only if $m = n - c$, where $c$ is the number of [connected components](/connected-components/), if and only if each depth-first search finds no back edge. In particular, every undirected graph with $m \ge n$ has a cycle.

## Variants

- **Search.** Return a cycle, not only "yes". See [finding a cycle in a graph](/cycle-detection-in-graph/). The DFS methods give the cycle at no extra cost.
- **Through a given vertex or edge.** Does some cycle contain the vertex $v$? In a directed graph, that holds if and only if $v$ has a self-loop or an edge $v \to u$ with $v$ reachable from $u$, so one search from each out-neighbour, or one [strong components](/strongly-connected-components/) computation, answers it. In an undirected graph, an edge lies on a cycle if and only if it is not a [bridge](/bridge/).
- **Odd cycle.** An undirected graph has an odd cycle if and only if it is not bipartite; see [bipartite testing](/bipartite-testing/).
- **Shortest cycle.** The length of a shortest cycle is the [girth](/girth/); see the [shortest cycle problem](/shortest-cycle-problem/).
- **Negative cycle.** With edge weights, does a cycle of negative total weight exist? See [negative cycle detection](/negative-cycle-detection/), solved by [Bellman-Ford](/bellman-ford/) in $O(nm)$ time.
- **Long cycles.** Deciding whether a cycle of length at least $k$, or exactly $n$ (a [Hamiltonian cycle](/hamiltonian-cycle-problem/)), exists is NP-complete.
- **Incremental.** Edges arrive one by one, and the first edge that closes a directed cycle must be reported. See [incremental topological ordering](/incremental-topological-ordering/). For undirected graphs, a [disjoint-set](/disjoint-set/) structure reports the first edge whose two ends are already connected, in near-constant amortized time per edge.
- **Cycles of a function.** For a function $f$ on a finite set, the sequence $x, f(x), f(f(x)), \ldots$ always enters a cycle. Finding it with $O(1)$ memory is a different problem, solved by [Floyd's](/floyd-cycle-detection/) and [Brent's](/brent-cycle-detection/) algorithms. Its graph is a [functional graph](/functional-graph/), in which each vertex has out-degree 1.

## Examples

| graph | kind | cycle? |
|---|---|---|
| path $0 - 1 - 2 - 3$ | undirected | no: a tree |
| triangle $0, 1, 2$ | undirected | yes, length 3 |
| two vertices, two parallel edges | undirected | yes, length 2 |
| two vertices, one edge | undirected | no |
| one vertex with a self-loop | either | yes, length 1 |
| $n$ isolated vertices | either | no |
| $0 \to 1$, $1 \to 2$, $0 \to 2$ | directed | no: a DAG, though its underlying graph is a triangle |
| $0 \to 1$, $1 \to 0$ | directed | yes, length 2 |
| $0 \to 1$ twice (parallel) | directed | no |
| $0 \to 1$, $1 \to 2$, $2 \to 3$, $3 \to 1$, $4 \to 0$ | directed | yes: $1 \to 2 \to 3 \to 1$; vertices 0 and 4 are on no cycle |

**A DFS run.** In the last graph, with the vertices tried in the order $0, 1, \ldots$, the search starts at 0 and goes $0 \to 1 \to 2 \to 3$. At 3 it scans the edge $3 \to 1$, and vertex 1 is still on the current path (gray). That is a back edge, so the answer is "yes".

## Known algorithms

| algorithm | graphs | time | remark |
|---|---|---|---|
| [DFS cycle detection](/dfs-cycle-detection/) | both | $\Theta(n + m)$ directed, $O(n)$ undirected | a back edge exists if and only if a cycle exists; undirected graphs must skip the parent edge by its identifier, not by the parent vertex |
| [Kahn's algorithm](/kahns-algorithm/) | directed | $\Theta(n + m)$ | remove sources until none is left; a cycle exists if and only if vertices remain |
| [Union-find](/union-find-connectivity/) | undirected | $O(n \, \alpha(n))$ | a cycle exists if and only if some edge joins two vertices that are already connected; at most $n$ edges are processed |
| [Strong components](/strongly-connected-components/) ([Tarjan](/tarjan-scc/), [Kosaraju](/kosaraju-sharir/)) | directed | $\Theta(n + m)$ | a cycle exists if and only if some component has two or more vertices or some vertex has a self-loop |
| Edge count | undirected | $\Theta(n + m)$, or $O(n)$ with the count of components | a cycle exists if and only if $m > n - c$ |

**Why undirected graphs need only $O(n)$ time.** A forest on $n$ vertices has at most $n - 1$ edges. So union-find, or DFS, finds a cycle among the first $n$ edges that it examines, if not earlier. In DFS, each list entry that is scanned is a tree edge, the parent edge seen from the child, or a back edge, which stops the search; the first two kinds number at most $2(n - 1)$. So DFS looks at $O(n)$ list entries in total, whatever $m$ is.

## Bounds

**Upper bounds.** $O(n + m)$ time for directed graphs and $O(n)$ time for undirected graphs, in the [word RAM](/word-ram/) model with adjacency lists. The extra space is $\Theta(n)$ for colours and the stack.

**Lower bound, directed.** Each deterministic algorithm reads $\Omega(n + m)$ list entries in the worst case. *Proof.* Take the transitive tournament on $k$ vertices, with the edges $i \to j$ for all $0 \le i < j < k$, plus $n - k$ vertices with empty lists. It is acyclic. Suppose that the algorithm answers "no" without reading the entry $j$ in the list of $i$. Change that entry to $0$. The edge $i \to j$ becomes $i \to 0$, which closes the cycle $0 \to 1 \to \cdots \to i \to 0$ (the edges $\ell \to \ell + 1$ with $\ell < i$ are still there, and for $i = 0$ the new edge is a self-loop). The algorithm sees the same input and gives the same wrong answer. So it reads all $k(k-1)/2$ entries. In the same way, if it never probes the list of an isolated vertex, a self-loop there goes unseen. With $k(k-1)/2 \approx m$ this gives $\Omega(n + m)$.

**Lower bound, undirected.** $\Omega(n)$ probes: an unprobed vertex list could hold a self-loop.

## Reductions

- **Directed to topological sorting.** $G$ is acyclic if and only if [topological sort](/topological-sort/) succeeds. Any topological sort that checks its output decides the problem in the same time.
- **Undirected to directed, with care.** Replacing each undirected edge by two opposite arcs turns every edge into a directed 2-cycle, so the reduction is wrong. The right reduction keeps the undirected search and skips the edge it arrived by.
- **From cycle detection to strong components.** A directed graph is acyclic if and only if each strong component is one vertex with no self-loop. This costs one $\Theta(n + m)$ computation.
- **To matrix products, for dense graphs.** A directed graph has a cycle if and only if some diagonal entry of the [transitive closure](/transitive-closure/) is 1. This costs $O(n^\omega \log n)$ by repeated squaring of the [Boolean adjacency matrix](/boolean-matrix-multiplication/), which is slower than DFS on any input, but it shows that the problem is in NC.

## Applications

- **Deadlock detection.** Processes wait for resources held by other processes. A cycle in the [wait-for graph](/wait-for-graph/) is a deadlock; see [deadlock detection](/deadlock-detection/).
- **Build systems and package managers.** A dependency cycle among modules, targets or packages makes a build order impossible. The tool runs a topological sort and reports a cycle when it fails.
- **Spreadsheets.** A formula that refers back to itself through other cells is a circular reference. The spreadsheet detects it before it evaluates the cells.
- **Garbage collection.** [Reference counting](/reference-counting/) cannot free objects that refer to each other in a cycle; a separate pass looks for such cycles.
- **Minimum spanning trees.** [Kruskal's algorithm](/kruskal/) adds an edge only if it does not close a cycle, which is the incremental undirected test with union-find.
- **Scheduling.** A project plan with precedence rules is feasible only if the precedence graph is a DAG; then the [critical path](/critical-path/) is a [longest path in the DAG](/dag-longest-path/).

## References
