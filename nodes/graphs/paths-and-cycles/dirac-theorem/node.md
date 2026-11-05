---
tag: 4D32MN
kind: theorem
slug: dirac-theorem
name: Dirac's theorem
area: graphs/paths-and-cycles
level: advanced
summary: A simple graph on n ≥ 3 vertices in which every vertex has at least n/2 neighbours has a Hamiltonian cycle.
prereqs: [hamiltonian-cycle, degree, simple-path]
see_also: [ore-theorem, hamiltonian-cycle-problem, hamiltonian-path, chvatal-closure, longest-path-problem, bipartite-graph, articulation-point, hamiltonian-cycle-np-completeness]
sources:
  - paper: doi:10.1112/plms/s3-2.1.69
    title: G. A. Dirac, Some theorems on abstract graphs, Proceedings of the London Mathematical Society (3) 2, 69 to 81 (1952)
    locator: the whole paper (the minimum degree condition for a Hamiltonian cycle, and long cycles in 2-connected graphs)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 10.1, Sufficient conditions (Theorem of Dirac, with the longest path proof)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Chapter 18, Hamilton cycles (Section 18.1 and the degree conditions of Dirac, Ore and Bondy and Chvátal)
  - paper: "A. Ghouila-Houri, Une condition suffisante d'existence d'un circuit hamiltonien, Comptes Rendus de l'Académie des Sciences de Paris 251, 495 to 497 (1960)"
    locator: the whole note (the directed version)
---

Dirac's theorem gives a simple condition that forces a [Hamiltonian cycle](/hamiltonian-cycle/): if every vertex of a simple graph with $n \ge 3$ vertices has [degree](/degree/) at least $n/2$, the graph has a cycle through all its vertices. Deciding whether a graph has a Hamiltonian cycle is NP-complete in general, so a test that is easy to check and always sufficient is useful. The bound $n/2$ cannot be lowered: there are graphs with minimum degree $\lceil n/2 \rceil - 1$ and no Hamiltonian cycle. The theorem is for undirected simple graphs; for multigraphs the degree must count distinct neighbours, and the directed analogue is a theorem of Ghouila-Houri.

## Statement

**Theorem (Dirac, 1952).** Let $G$ be a simple undirected graph with $n \ge 3$ vertices and minimum degree $\delta(G) \ge n/2$. Then $G$ has a Hamiltonian cycle.

**Multigraphs.** If $G$ has parallel edges or self-loops, apply the theorem to the underlying simple graph, so that $d(v)$ is the number of distinct neighbours of $v$. Loops and repeated edges cannot help a Hamiltonian cycle, which uses each vertex once. With the multigraph degree the statement is false: the path $0, 1, 2$ with each edge doubled has degrees $2, 4, 2 \ge 3/2$ and no Hamiltonian cycle.

**Directed graphs (Ghouila-Houri, 1960).** A strongly connected directed graph on $n$ vertices in which $d^+(v) + d^-(v) \ge n$ for every vertex $v$ has a directed Hamiltonian cycle. In particular this holds when $d^+(v) \ge n/2$ and $d^-(v) \ge n/2$ for every $v$; such a graph is strongly connected.

## In plain words

Suppose that at a party of at least three people, everyone knows at least half of the others. Then they can sit around a round table so that everyone knows both neighbours.

The reason: take the longest line of people in which neighbours know each other. Both people at the ends know only people in the line, or the line could grow. Each end knows at least half of all people, and the line is shorter than the whole party, so their friends must overlap in a way that lets you close the line into a circle. Once there is a circle, anyone outside it who knows someone in it could be joined to make a longer line, so nobody is outside.

## Proof

Let $d(v)$ be the degree of $v$ and $N(v)$ its set of neighbours.

**Step 1: $G$ is connected.** Let $u$ and $v$ be non-adjacent. Both $N(u)$ and $N(v)$ lie in $V \setminus \{u, v\}$, which has $n - 2$ vertices, and $|N(u)| + |N(v)| \ge n$. So they share a vertex, and $u$ and $v$ are at distance 2.

**Step 2: a longest path and its ends.** Let $P = x_0 x_1 \cdots x_k$ be a longest path in $G$. Every neighbour of $x_0$ is on $P$: otherwise a neighbour $y \notin P$ gives the longer path $y x_0 \cdots x_k$. In the same way every neighbour of $x_k$ is on $P$. So $k \ge d(x_0) \ge n/2$.

**Step 3: a cycle on the vertices of $P$.** Let

$$A = \{ i : 0 \le i < k, \ x_0 x_{i+1} \in E \}, \qquad B = \{ i : 0 \le i < k, \ x_i x_k \in E \}.$$

By Step 2, $|A| = d(x_0) \ge n/2$ and $|B| = d(x_k) \ge n/2$. Both are subsets of $\{0, \ldots, k-1\}$, which has $k \le n - 1 < n$ elements. So $|A| + |B| \ge n > k$, and there is an index $i \in A \cap B$. Then

$$C = x_0 \, x_{i+1} \, x_{i+2} \cdots x_k \, x_i \, x_{i-1} \cdots x_1 \, x_0$$

is a cycle: it uses the edges $x_0 x_{i+1}$ and $x_i x_k$ and the edges of $P$ except $x_i x_{i+1}$. It passes all $k + 1$ vertices of $P$. If $i = 0$, the part from $x_i$ back to $x_0$ is empty, and $C$ is $P$ closed by the edge $x_k x_0$. Since $k \ge n/2 \ge 3/2$, $k \ge 2$, so $C$ has length $k + 1 \ge 3$.

**Step 4: $C$ contains every vertex.** Suppose some vertex is not on $C$. By Step 1, there is an edge $y x_j$ with $y \notin C$ and $x_j$ on $C$. Start at $y$, go to $x_j$, and walk once around $C$ to the vertex just before $x_j$. This is a path with $k + 2$ vertices, longer than $P$, a contradiction. So $C$ is a Hamiltonian cycle. $\square$

The proof is constructive: start from any path, extend it while an end has a neighbour off the path, close it with Step 3, and open the cycle at a vertex with a neighbour outside. Each round lengthens the path, so there are at most $n$ rounds, and each takes $O(n^2)$ time with an adjacency matrix, so a Hamiltonian cycle is found in $O(n^3)$ time, or faster with more care.

## Consequences

- **Hamiltonian paths.** If $\delta(G) \ge (n - 1)/2$, then $G$ has a Hamiltonian path: add a new vertex joined to all others, apply the theorem to the new graph on $n + 1$ vertices, and delete the new vertex from the cycle.
- **Ore's theorem.** The proof uses only $d(x_0) + d(x_k) \ge n$ for the two ends, and the ends of a longest path that does not close are non-adjacent. This gives [Ore's theorem](/ore-theorem/) (1960): $d(u) + d(v) \ge n$ for all non-adjacent $u \ne v$ suffices, which contains Dirac's theorem.
- **The closure.** Bondy and Chvátal (1976) showed that adding an edge $uv$ with $d(u) + d(v) \ge n$ does not change whether $G$ is Hamiltonian; see the [closure](/chvatal-closure/). Dirac's condition makes the closure complete.
- **Dense graphs are easy instances.** The [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) is NP-complete, but on the class of graphs with $\delta \ge n/2$ every instance is a yes instance, and the constructive proof finds the cycle in polynomial time. For $\delta \ge c n$ with a constant $c < 1/2$ the problem stays NP-complete, by padding a hard instance.
- **Long cycles.** Dirac's paper also proves that a 2-connected graph with minimum degree $\delta$ has a cycle of length at least $\min(n, 2\delta)$.

## Tightness

The bound $n/2$ is sharp in two ways, and $n \ge 3$ is needed.

| graph | $n$ | $\delta$ | why there is no Hamiltonian cycle |
|---|---|---|---|
| $K_{k, k+1}$, $k \ge 1$ | $2k + 1$ | $k = (n-1)/2$ | it is [bipartite](/bipartite-graph/) with unequal sides, and a cycle alternates sides |
| two copies of $K_{k+1}$ sharing one vertex | $2k + 1$ | $k = (n-1)/2$ | the shared vertex is an [articulation point](/articulation-point/), and a Hamiltonian cycle has none |
| $K_2$ | 2 | $1 = n/2$ | it has no cycle at all |

For odd $n = 2k + 1$, both families have $\delta = k = \lceil n/2 \rceil - 1$, the largest value below $n/2$. For even $n = 2k$, the graph $K_{k-1, k+1}$ has $\delta = k - 1$ and no Hamiltonian cycle. For $n \le 6$, a check of all labeled simple graphs confirms the theorem: every graph with $\delta \ge n/2$ has a Hamiltonian cycle (1, 10, 26 and 1858 graphs for $n = 3, 4, 5, 6$), and the graphs in the table, for $k = 1$ to 4, have none.

The condition is far from necessary: the cycle $C_n$ is Hamiltonian with $\delta = 2$.

## History

Gabriel Andrew Dirac proved the theorem in 1952 in the Proceedings of the London Mathematical Society, as part of a paper on long cycles and paths in graphs. Ore's degree-sum version followed in 1960, and Ghouila-Houri proved the directed version the same year. Bondy and Chvátal's closure (1976) unified these conditions. The theorem started a large body of work on degree conditions for Hamiltonicity, including Pósa's and Chvátal's degree sequence conditions and, much later, results on the number of Hamiltonian cycles in graphs with $\delta \ge n/2$.

## References
