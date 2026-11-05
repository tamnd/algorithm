---
tag: G10SM7
kind: theorem
slug: ore-theorem
name: Ore's theorem
area: graphs/paths-and-cycles
level: advanced
summary: If deg(u) + deg(v) ≥ n for every pair of distinct non-adjacent vertices of a simple graph with n ≥ 3 vertices, the graph has a Hamiltonian cycle.
prereqs: [hamiltonian-cycle, degree]
see_also: [dirac-theorem, hamiltonian-cycle-problem, hamiltonian-path, menger-theorem, biconnected-graph, bipartite-graph, traveling-salesman-problem, simple-cycle]
sources:
  - paper: Øystein Ore, Note on Hamilton circuits, American Mathematical Monthly 67(1), 55 (1960)
    title: Ore, the degree-sum condition for Hamilton circuits
    locator: the whole note
  - paper: J. A. Bondy and V. Chvátal, A method in graph theory, Discrete Mathematics 15(2), 1976
    title: Bondy and Chvátal, the closure of a graph
    locator: the closure lemma for Hamiltonian cycles and its corollaries
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 7.2 (Hamiltonian cycles), Ore's condition, the closure and Chvátal's condition
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 18 (Hamilton cycles), the closure and the degree conditions of Dirac, Ore and Chvátal
  - paper: Edgar M. Palmer, The hidden algorithm of Ore's theorem on Hamiltonian cycles, Computers and Mathematics with Applications 34(11), 1997
    title: Palmer, an algorithm from the proof of Ore's theorem
    locator: the algorithm that removes gaps from a cyclic order
---

Ore's theorem gives a degree condition that forces a [Hamiltonian cycle](/hamiltonian-cycle/): in a simple graph with $n \ge 3$ vertices, if any two vertices that are not adjacent have degrees adding up to at least $n$, then the graph is Hamiltonian. It contains [Dirac's theorem](/dirac-theorem/), where every degree is at least $n/2$, as a special case. The bound $n$ cannot be lowered to $n - 1$, and the proof gives an $O(n^2)$ algorithm that finds the cycle. Deciding Hamiltonicity in general is NP-complete, so a condition like this is only sufficient.

## Statement

Let $G = (V, E)$ be a finite simple undirected graph, with no loops and no parallel edges, on $n = |V| \ge 3$ vertices, and let $\deg(v)$ be the number of neighbours of $v$.

**Theorem (Ore, 1960).** If $\deg(u) + \deg(v) \ge n$ for every pair of distinct vertices $u, v$ with $uv \notin E$, then $G$ has a Hamiltonian cycle.

**The condition for multigraphs and digraphs.** For a multigraph, apply the theorem to the underlying simple graph and count neighbours, not edges; with edges counted, the statement is false (see Tightness). The theorem is about undirected graphs. Directed analogues are Woodall's theorem and Meyniel's theorem, listed under Consequences.

## In plain words

Some people must sit at a round table so that each person sits between two friends. Look at any two people who are not friends with each other. Count the friends of the first and the friends of the second. If this total is always at least the number of people, a good seating exists.

The idea is: if two strangers sit next to each other, then they have so many friends between them that cutting the table at the right place and turning one part around puts friends next to each other. Each such fix removes a bad pair, so after a few fixes everyone sits between friends.

## Proof

Write $\sigma(u, v) = \deg(u) + \deg(v)$. The proof rests on one lemma.

**Lemma (rotation).** Let $(v_1, v_2, \ldots, v_n)$ be an ordering of $V$, with $n \ge 3$, such that $v_1 v_n \notin E$ and $\sigma(v_1, v_n) \ge n$. Then there is an index $i$ with $2 \le i \le n - 2$ such that $v_1 v_{i+1} \in E$ and $v_i v_n \in E$.

*Proof.* Let $A = \{ i : 1 \le i \le n - 1,\ v_1 v_{i+1} \in E \}$ and $B = \{ i : 1 \le i \le n - 1,\ v_i v_n \in E \}$. Each neighbour of $v_1$ is some $v_{i+1}$ with $1 \le i \le n - 1$, so $|A| = \deg(v_1)$; in the same way $|B| = \deg(v_n)$. Both sets lie in $\{1, \ldots, n - 1\}$, which has $n - 1$ elements, and $|A| + |B| \ge n$, so some $i$ is in $A \cap B$. Now $i \ne n - 1$, since $n - 1 \in A$ would mean $v_1 v_n \in E$, and $i \ne 1$, since $1 \in B$ would mean $v_1 v_n \in E$. So $2 \le i \le n - 2$. $\square$

**Proof of the theorem.** Suppose the theorem is false, and choose a counterexample $G$ on $n \ge 3$ vertices with the largest number of edges. Then $G$ meets the condition and has no Hamiltonian cycle. $G$ is not complete, because $K_n$ with $n \ge 3$ is Hamiltonian. So there are distinct vertices $u, v$ with $uv \notin E$. The graph $G + uv$ also meets the condition, because adding an edge does not lower any degree and does not create a new non-adjacent pair. It has more edges than $G$, so it is not a counterexample, and it has a Hamiltonian cycle $C$. $C$ uses the edge $uv$, since $G$ has no Hamiltonian cycle. Deleting $uv$ from $C$ leaves a Hamiltonian path $(v_1, \ldots, v_n)$ of $G$ with $v_1 = u$ and $v_n = v$.

By the lemma there is $i$ with $2 \le i \le n - 2$, $v_1 v_{i+1} \in E$ and $v_i v_n \in E$. Then

$$(v_1, v_2, \ldots, v_i, v_n, v_{n-1}, \ldots, v_{i+1}, v_1)$$

is a Hamiltonian cycle of $G$: it visits every vertex once, its steps $v_j v_{j+1}$ are edges of the path, and the two new steps are $v_i v_n$ and $v_{i+1} v_1$. This contradicts the choice of $G$. $\blacksquare$

**An algorithm from the proof.** The lemma does not need $(v_1, \ldots, v_n)$ to be a path. Start from any cyclic order of $V$, and call a pair of consecutive vertices that are not adjacent a *gap*. While there is a gap, rotate the order so that the gap is $v_n, v_1$, find $i$ by the lemma, and reverse the segment $v_{i+1}, \ldots, v_n$. The consecutive pairs inside the segment stay the same, the pairs $v_i v_{i+1}$ and $v_n v_1$ are replaced by the edges $v_i v_n$ and $v_{i+1} v_1$, and so the number of gaps goes down by at least 1. There are at most $n$ gaps at the start, and each step takes $O(n)$ time with an [adjacency matrix](/adjacency-matrix/), so a Hamiltonian cycle is found in $O(n^2)$ time (Palmer, 1997).

## Consequences

- **Dirac's theorem.** If $\deg(v) \ge n/2$ for every vertex and $n \ge 3$, then $\sigma(u, v) \ge n$ for every pair, so $G$ is Hamiltonian. See [Dirac's theorem](/dirac-theorem/).
- **Hamiltonian paths.** If $\sigma(u, v) \ge n - 1$ for every non-adjacent pair, then $G$ has a [Hamiltonian path](/hamiltonian-path/). *Proof.* Add a vertex $z$ joined to all of $V$. The new graph has $n + 1 \ge 3$ vertices, the non-adjacent pairs are the same, and each of their degrees grows by 1, so $\sigma \ge n + 1$. By Ore's theorem it has a Hamiltonian cycle, and deleting $z$ gives a Hamiltonian path of $G$.
- **Hamilton-connected graphs.** If $\sigma(u, v) \ge n + 1$ for every non-adjacent pair, then every two vertices are the ends of a Hamiltonian path (Ore, 1963).
- **The closure.** The rotation argument proves more: if $uv \notin E$ and $\sigma(u, v) \ge n$, then $G$ is Hamiltonian if and only if $G + uv$ is. Adding such edges until none is left gives the closure of Bondy and Chvátal, and $G$ is Hamiltonian if and only if its closure is. Ore's condition makes the closure complete in one round.
- **Chvátal's condition.** A degree-sequence condition that contains both Dirac's and Ore's: if the degrees $d_1 \le \cdots \le d_n$ satisfy, for every $i < n/2$, $d_i \le i \Rightarrow d_{n-i} \ge n - i$, then $G$ is Hamiltonian (Chvátal, 1972). It also follows from the closure.
- **Pancyclic graphs.** Bondy (1971) showed that a graph that meets Ore's condition has cycles of every length from 3 to $n$, unless it is the complete bipartite graph $K_{n/2, n/2}$.
- **Directed graphs.** Woodall (1972): a digraph without loops on $n \ge 2$ vertices is Hamiltonian if $\mathrm{out}(u) + \mathrm{in}(v) \ge n$ for every pair of distinct vertices with no arc from $u$ to $v$. Meyniel (1973): a strongly connected digraph on $n \ge 2$ vertices is Hamiltonian if $\deg(u) + \deg(v) \ge 2n - 1$ for every pair of non-adjacent vertices, with $\deg$ the in-degree plus the out-degree.
- **Algorithms.** On graphs that meet the condition, a Hamiltonian cycle is found in $O(n^2)$ time, although the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) is NP-complete in general.

## Tightness

- **The bound $n$ cannot be $n - 1$.** Take two copies of $K_k$, $k \ge 3$, that share one vertex $x$, so $n = 2k - 1$. Two non-adjacent vertices lie in different copies, and each has degree $k - 1$, so $\sigma = 2k - 2 = n - 1$. The vertex $x$ is a cut vertex, so the graph is not [biconnected](/biconnected-graph/) and has no Hamiltonian cycle.
- **A bipartite example.** The complete bipartite graph $K_{k, k+1}$, $k \ge 2$, has $n = 2k + 1$. Two vertices on the side of size $k + 1$ have degree $k$, so $\sigma = 2k = n - 1$; two vertices on the side of size $k$ have $\sigma = 2k + 2$. The graph is [bipartite](/bipartite-graph/) with sides of different sizes, so it has no Hamiltonian cycle.
- **$n \ge 3$ is needed.** $K_1$ and $K_2$ have no pair of non-adjacent vertices, so they meet the condition, but a simple graph on 1 or 2 vertices has no cycle.
- **Simple graphs only.** Take the path $a, b, c$ and double both edges. Counting edges, $\deg(a) + \deg(c) = 2 + 2 = 4 \ge 3$, but $a$ and $c$ are not adjacent, and a Hamiltonian cycle on 3 vertices needs all three pairs to be adjacent. Loops fail in the same way: a loop at $a$ and at $c$ adds 2 to each degree. With neighbours counted, the sum is $1 + 1 = 2 < 3$, and the theorem does not apply.
- **The condition is not necessary.** The cycle $C_n$ with $n \ge 5$ is Hamiltonian, but two non-adjacent vertices have $\sigma = 4 < n$.

## History

Gabriel Dirac proved the minimum-degree condition in 1952. Øystein Ore replaced it by the condition on non-adjacent pairs in a one-page note in the American Mathematical Monthly in 1960, with the proof by a longest counterexample and a rotation. In 1963 he gave the stronger condition for Hamilton-connected graphs. Chvátal's degree-sequence condition (1972) and the closure of Bondy and Chvátal (1976) generalize both theorems; Bondy and Chvátal took the closure step directly from Ore's proof. Palmer (1997) wrote out the algorithm that the proof contains.

## References
