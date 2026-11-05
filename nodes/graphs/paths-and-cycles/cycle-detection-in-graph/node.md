---
tag: NFJCMK
kind: problem
slug: cycle-detection-in-graph
name: Finding a cycle in a graph
area: graphs/paths-and-cycles
level: intro
summary: Problem of finding a cycle in a directed or undirected graph, or proving there is none, usually solved with depth-first search and vertex colors.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [cycle-detection, depth-first-search, simple-cycle]
see_also: [dfs-cycle-detection, kahns-algorithm, topological-sort, edge-classification, union-find-connectivity, shortest-cycle-problem, enumerating-elementary-cycles, color-coding]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (white, gray and black vertices, and back edges) and Section 20.4, Topological sort (acyclic if and only if no back edge)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (the class DirectedCycle, which returns the cycle through the edgeTo links and the onStack marks)
  - paper: doi:10.1016/j.cosrev.2010.09.009
    title: Ross M. McConnell, Kurt Mehlhorn, Stefan Näher and Pascal Schweitzer, Certifying algorithms, Computer Science Review 5(2), 119 to 161 (2011)
    locator: the sections on graph algorithms (a cycle certifies that a graph is not acyclic, a topological order certifies that it is)
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the whole paper (cycles and paths of a given length k in 2^O(k) times polynomial time)
---

Finding a cycle in a graph is the search version of [cycle detection](/cycle-detection/): given a directed or undirected [graph](/graph/), return the edges of one cycle, or report that the graph has none. A [depth-first search](/depth-first-search/) solves it in $\Theta(n + m)$ time: the first back edge that it meets, together with the path of tree edges above it, is a cycle. The answer is a *certificate*: a cycle can be checked in time proportional to its length, and when there is no cycle a [topological ordering](/topological-ordering/) or the depth-first forest proves it. Asking for a cycle of a given length, instead of any cycle, makes the problem NP-hard.

## In plain words

It is not enough to say "there is a loop somewhere": a programmer who must fix a circular dependency wants to see the loop. So the task is to print the loop, step by step, or to show that there is none.

Depth-first search does this almost for free. It always knows the route from where it started to where it is now. When it finds an arrow back to a point on that route, the loop is the part of the route from that point to here, plus the arrow. If no such arrow exists, the order in which the search finishes the points is a proof that there is no loop.

## Definition

**Input.** A finite graph $G = (V, E)$, directed or undirected, with $n$ vertices and $m$ edges in incidence lists, so that each edge has an identifier. Parallel edges and [self-loops](/self-loop/) are allowed. The identifiers are needed: in a [multigraph](/multigraph/) a list of vertices does not name the edges of a cycle.

**Output.** Either a sequence of edges $(e_1, \ldots, e_k)$, $k \ge 1$, that forms a cycle: the edges are distinct, $e_i$ goes from $v_{i-1}$ to $v_i$ (in the undirected case, joins them), $v_k = v_0$, and $v_0, \ldots, v_{k-1}$ are distinct. Or "acyclic", when no cycle exists.

**Certificates.** A cycle is checked in $O(k)$ time. For "acyclic", a directed graph has the certificate of a topological ordering, checked in $O(n + m)$ time by testing that each edge goes forward. An undirected graph has the certificate of a spanning forest equal to the whole edge set, checked by counting $m = n - c$. An algorithm that always outputs one of the two certificates is a *certifying algorithm*: a user can trust its output without trusting its code.

**Conventions.** A self-loop is a cycle of length 1. In an undirected graph, two parallel edges form a cycle of length 2, but the walk $u, e, v, e, u$ that uses one edge twice is not a cycle. In a directed graph, $u \to v$ with $v \to u$ is a cycle of length 2.

## Variants

- **Any cycle.** The problem of this page.
- **A cycle through a given vertex $v$ or edge $e$.** In a directed graph, run a search from the head of an edge out of $v$ that tries to reach $v$, for each such edge, or use [strong components](/strongly-connected-components/): an edge $u \to w$ lies on a cycle if and only if $u$ and $w$ are in the same strong component. In an undirected graph, an edge lies on a cycle if and only if it is not a [bridge](/bridge/).
- **A shortest cycle.** Return a cycle of least length, which is the [girth](/girth/). See the [shortest cycle problem](/shortest-cycle-problem/); breadth-first search from each vertex gives $O(nm)$ time.
- **An odd cycle.** A certificate that an undirected graph is not bipartite. A [BFS](/breadth-first-search/) 2-colouring finds an edge inside one layer, and the two tree paths up to the common ancestor plus that edge form an odd cycle.
- **A negative cycle or a cycle of least mean weight.** See [negative cycle detection](/negative-cycle-detection/) and [Karp's minimum mean cycle algorithm](/karp-minimum-mean-cycle/).
- **A cycle of length exactly $k$, or at least $k$.** NP-complete when $k$ is part of the input, since $k = n$ is the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). Alon, Yuster and Zwick's [color-coding](/color-coding/) finds a cycle of length exactly $k$ in $2^{O(k)} \cdot nm$ time in expectation, so the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in $k$. For $k = 3$, see [triangle counting](/triangle-counting/).
- **All cycles.** See [enumerating elementary cycles](/enumerating-elementary-cycles/). There can be exponentially many.

## Examples

**Directed.** The edges $e_0 = 0 \to 1$, $e_1 = 1 \to 2$, $e_2 = 2 \to 3$, $e_3 = 3 \to 1$ and $e_4 = 4 \to 0$. A DFS from 0 follows $e_0$, $e_1$ and $e_2$, then scans $e_3$ and finds vertex 1 gray. Walking up the tree edges from 3 to 1 gives $e_2$, then $e_1$. The output is the cycle $(e_1, e_2, e_3)$, that is $1 \to 2 \to 3 \to 1$.

**The same graph with Kahn's algorithm.** The in-degrees are 1, 2, 1, 1, 0. The algorithm removes 4, then 0, and stops: vertices 1, 2 and 3 are left, each with an incoming edge from a left-over vertex. Walking backwards inside the left-over set, $1 \leftarrow 3 \leftarrow 2 \leftarrow 1$, repeats vertex 1, and the edges walked, in reverse, form the cycle $1 \to 2 \to 3 \to 1$.

**Undirected.** The edges $e_0 = \{0, 1\}$, $e_1 = \{1, 2\}$, $e_2 = \{2, 0\}$ and $e_3 = \{2, 3\}$. A DFS from 0 goes along $e_0$ to 1 and along $e_1$ to 2. At 2 it skips $e_1$, the edge it came by, and scans $e_2$ to vertex 0, which is gray. The output is $(e_0, e_1, e_2)$.

**Multigraph.** Two vertices with the parallel edges $a$ and $b$. A DFS from 0 goes along $a$ to 1. At 1 it skips $a$ by its identifier, scans $b$, and finds 0 gray. The output is $(a, b)$, a cycle of length 2. A search that skips every edge to the parent *vertex* misses this cycle and answers "acyclic", which is wrong.

**No cycle.** For the directed graph $0 \to 1$, $1 \to 2$, $0 \to 2$, the output is "acyclic" with the certificate $0, 1, 2$, the vertices in decreasing order of DFS finish time.

## Known algorithms

| algorithm | graphs | time | how it extracts the cycle |
|---|---|---|---|
| [DFS cycle detection](/dfs-cycle-detection/) | both | $\Theta(n + m)$; $O(n)$ for undirected | back edge $(u, v)$ plus the parent edges from $u$ up to $v$ |
| [Kahn's algorithm](/kahns-algorithm/) with a backward walk | directed | $\Theta(n + m)$ | from a left-over vertex, step to a left-over predecessor until a vertex repeats |
| [Union-find](/union-find-connectivity/) with a forest search | undirected | $O(n \, \alpha(n))$ for the test, $O(n)$ for the path | the edge that joins two connected vertices, plus the path between them in the forest built so far |
| [Tarjan's strong components](/tarjan-scc/) | directed | $\Theta(n + m)$ | inside a strong component with two vertices, search from one vertex back to itself |
| BFS from each vertex | both | $O(nm)$ | gives a shortest cycle |

The DFS method keeps, for each vertex, its colour (white: not seen; gray: on the current path; black: finished) and the edge by which it was discovered. In a directed graph, a scanned edge to a gray vertex closes a cycle. In an undirected graph, the edge by which the current vertex was reached is skipped by its identifier, and any other edge to a gray vertex closes a cycle. The proofs are on the [DFS cycle detection](/dfs-cycle-detection/) page.

## Bounds

**Upper bound.** $\Theta(n + m)$ time and $\Theta(n)$ extra space in the [word RAM](/word-ram/) model, with the output of length at most $n$. For undirected graphs, $O(n)$ time, because DFS stops after $O(n)$ list entries.

**Lower bound.** The decision version already needs $\Omega(n + m)$ probes on directed graphs and $\Omega(n)$ on undirected graphs, as shown on the [cycle detection](/cycle-detection/) page, and the search version is at least as hard.

**Length of the answer.** DFS can return a long cycle when a short one exists: on a directed cycle $0 \to 1 \to \cdots \to n-1 \to 0$ with the extra edge $1 \to 0$ listed last at vertex 1, the search goes all the way round and returns the cycle of length $n$. If a short cycle is wanted, use the shortest cycle methods.

## Reductions

- **Search to decision.** With a decision oracle, delete edges one at a time and keep each deletion that leaves a cycle; at the end the remaining edges form one cycle. This costs $m$ oracle calls, which is much worse than DFS, but it shows that the two versions are polynomially equivalent.
- **Cycle through $v$ to reachability.** A directed cycle through $v$ exists if and only if $v$ has a self-loop or $v$ is [reachable](/reachability/) from an out-neighbour of $v$.
- **Topological sort as a certifying algorithm.** A topological sort that returns either an ordering or a cycle solves both this problem and its complement at once.

## Applications

- **Error messages.** Compilers, build tools and package managers print the actual import or dependency cycle, so that the user can break it.
- **Deadlock recovery.** A database or operating system that finds a cycle in the [wait-for graph](/wait-for-graph/) chooses a process on that cycle as the victim.
- **Fixing a graph.** Algorithms for the [feedback arc set](/feedback-arc-set-problem/) and [feedback vertex set](/feedback-vertex-set-problem/) problems repeatedly find a cycle and remove one of its edges or vertices.
- **Cycle canceling.** Min-cost flow algorithms find a negative cycle in the residual graph and push flow around it; see [cycle canceling](/cycle-canceling/).

## References
