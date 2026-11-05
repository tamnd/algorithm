---
tag: SZHYV4
kind: definition
slug: simple-cycle
name: Simple cycle
aliases:
- cycle
- elementary cycle
- elementary circuit
area: graphs/paths-and-cycles
level: intro
summary: A closed walk that repeats no vertex except the start and end and uses no edge twice; length at least 3 in a simple undirected graph.
prereqs: [walk, trail, simple-path]
see_also: [cycle-detection, girth, hamiltonian-cycle, johnson-elementary-cycles-algorithm, cycle-basis, directed-acyclic-graph, minimum-mean-cycle-problem, negative-cycle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the definitions of cycle and simple cycle in directed and undirected graphs, self-loops as cycles of length 1, and acyclic graphs
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.3 (Paths and cycles), the definition of a cycle, its length, girth and circumference, and the proposition that minimum degree at least 2 gives a cycle of length at least the minimum degree plus 1
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 2 (Subgraphs) and Chapter 3 (Connected Graphs), cycles in graphs and digraphs, loops and parallel edges as cycles of length 1 and 2
---

A simple cycle is a closed [walk](/walk/) that returns to its start and visits no other vertex twice. In a simple undirected graph it has at least three edges, as in a triangle. In a [directed graph](/directed-graph/) a [self-loop](/self-loop/) is a cycle of length 1 and two opposite arcs form a cycle of length 2; in an undirected [multigraph](/multigraph/) a loop and a pair of parallel edges are cycles of length 1 and 2. A graph with no cycle is a forest if undirected and a [directed acyclic graph](/directed-acyclic-graph/) if directed, and much of algorithmic graph theory begins by asking whether a cycle exists.

## Definition

Let $G = (V, E)$ be a graph, directed or undirected, possibly a multigraph with self-loops.

**Simple cycle.** A *simple cycle* of length $k \ge 1$ is a closed walk

$$C = (v_0, e_1, v_1, \ldots, e_k, v_k), \qquad v_k = v_0,$$

such that

1. the edges $e_1, \ldots, e_k$ are pairwise distinct (so $C$ is a closed [trail](/trail/)), and
2. the vertices $v_1, \ldots, v_k$ are pairwise distinct.

In a directed graph, each $e_i$ is an arc from $v_{i-1}$ to $v_i$. Condition 1 then follows from condition 2, since two arcs of $C$ have different tails when $k \ge 2$.

**What this gives for each kind of graph.**

| graph | smallest possible length | the short cycles |
|---|---|---|
| undirected, simple | 3 | a triangle |
| undirected, multigraph with loops | 1 | a loop (length 1), two parallel edges (length 2) |
| directed, simple (no loops, no parallel arcs) | 2 | $u \to v \to u$ |
| directed, with loops | 1 | a loop $v \to v$ |

In a simple undirected graph, a closed walk $(u, v, u)$ of length 2 uses the edge $uv$ twice, so condition 1 rules it out. This is why CLRS and most books require $k \ge 3$ for undirected cycles.

**Same cycle, different start.** The rotations $(v_i, e_{i+1}, \ldots, e_k, v_k = v_0, e_1, \ldots, e_i, v_i)$ of $C$ describe the same cycle. In an undirected graph, so does the reverse. As a subgraph, a cycle is the set of its vertices and edges; counts of cycles on this site count these subgraphs, so a cycle of length $k \ge 3$ in a simple undirected graph is written in $2k$ ways as a sequence.

**Acyclic.** A graph is *acyclic* if it has no simple cycle. The terms *cycle* and *elementary cycle* (Johnson) mean simple cycle; a *circuit* is a cycle in some books and a closed trail in others.

**Two basic facts.**

- *A closed walk of length $k \ge 1$ in a directed graph contains a simple cycle.* Take a shortest closed subwalk $(v_i, \ldots, v_j)$ with $v_i = v_j$ and $i < j$. By minimality, $v_{i+1}, \ldots, v_j$ are distinct, so it is a simple cycle. In an undirected graph the same holds for a closed trail, but not for a closed walk: $(u, v, u)$ has no cycle in it.
- *If every vertex of a finite simple undirected graph has degree at least $d \ge 2$, the graph has a simple cycle of length at least $d + 1$.* Let $P = (v_0, \ldots, v_k)$ be a longest simple path. Each neighbour of $v_k$ lies on $P$, or $P$ could be extended. $v_k$ has at least $d$ neighbours, all among $v_0, \ldots, v_{k-1}$. Let $v_i$ be the one with the smallest index; then $i \le k - d$. So $(v_i, v_{i+1}, \ldots, v_k, v_i)$ is a simple cycle of length $k - i + 1 \ge d + 1$. $\square$ For $d = 2$ this shows that a nonempty forest has a vertex of degree at most 1.

**Measures.** The *length* of $C$ is $k$; with edge weights, its weight is $\sum_i w(e_i)$ and its mean is that sum divided by $k$. The [girth](/girth/) is the length of a shortest cycle and the *circumference* the length of a longest one. A cycle through every vertex is a [Hamiltonian cycle](/hamiltonian-cycle/).

## Examples and non-examples

Take the undirected simple graph with vertices $0, 1, 2, 3$ and edges $01, 12, 23, 30, 02$ (a square with one diagonal).

- $(0, 1, 2, 0)$ and $(0, 2, 3, 0)$ are cycles of length 3.
- $(0, 1, 2, 3, 0)$ is a cycle of length 4, a Hamiltonian cycle.
- $(0, 1, 2, 3, 0, 1, 2, 3, 0)$ is a closed walk around the square twice. It is not a simple cycle: it repeats every vertex and every edge.
- $(0, 2, 0)$ is not a cycle: it uses the edge $02$ twice.

So this graph has exactly three cycles: two triangles and the square. The girth is 3 and the circumference is 4.

**Complete graphs.** A cycle of length $k$ in $K_n$ is a choice of $k$ vertices and a cyclic order of them up to reversal, so $K_n$ has $\sum_{k=3}^{n} \binom{n}{k} \frac{(k-1)!}{2}$ cycles. For $n = 4$ this is $4 + 3 = 7$, and for $n = 5$ it is $10 + 15 + 12 = 37$.

**Directed.** The complete directed graph on 4 vertices (all 12 arcs, no loops) has $6$ cycles of length 2, $8$ of length 3 and $6$ of length 4, so 20 in all. Each set of $k$ vertices carries $(k - 1)!$ directed cycles.

**Self-loops and parallel edges.** In a directed graph, a loop $v \to v$ is the cycle $(v, v)$ of length 1. In an undirected multigraph with edges $a \ne b$ both joining $u$ and $v$, $(u, a, v, b, u)$ is a cycle of length 2.

**Acyclic graphs.** A tree on $n$ vertices has $n - 1$ edges and no cycle. Adding any one edge between two of its vertices creates exactly one cycle, the [fundamental cycle](/fundamental-cycle/) of that edge.

## Related definitions

- **Closed walk and closed trail.** A cycle is a closed trail with no repeated inner vertex. See [walk](/walk/) and [trail](/trail/).
- **Simple path.** Deleting one edge of a cycle of length $k$ leaves a [simple path](/simple-path/) of length $k - 1$.
- **Girth and shortest cycle.** See [girth](/girth/) and the [shortest cycle problem](/shortest-cycle-problem/).
- **Detecting and listing cycles.** See [cycle detection](/cycle-detection/) and [Johnson's algorithm](/johnson-elementary-cycles-algorithm/) for listing all simple cycles of a directed graph.
- **Weighted cycles.** See [negative cycle](/negative-cycle/) and the [minimum mean cycle problem](/minimum-mean-cycle-problem/).
- **Cycle space.** The edge sets of cycles span a vector space over $\mathrm{GF}(2)$; see [cycle basis](/cycle-basis/).
- **Hamiltonian cycle.** A cycle that contains every vertex. See [Hamiltonian cycle](/hamiltonian-cycle/).

## References
