---
tag: R12XWJ
kind: theorem
slug: bipartite-odd-cycle-theorem
name: Odd cycle characterization of bipartite graphs
aliases:
- König's bipartite theorem
area: graphs/coloring-and-cliques
level: core
summary: A graph is bipartite if and only if it contains no cycle of odd length.
prereqs: [bipartite-graph, breadth-first-search]
see_also: [bipartite-graph-test, bipartiteness-testing, bipartiteness-check, graph-coloring, chromatic-number, mycielski-graph, odd-cycle-transversal, konig-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.6, Bipartite graphs, Proposition 1.6.1 (a graph is bipartite if and only if it contains no odd cycle)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.2, Paths, cycles and trails (Lemma 1.2.15, every closed odd walk contains an odd cycle, and Theorem 1.2.18, König's characterization)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness (statements 3.14 to 3.16, the proof by breadth-first layers)
---

The odd cycle theorem says that a [graph](/graph/) is [bipartite](/bipartite-graph/) exactly when it has no cycle of odd length. One direction is easy: the vertices of a cycle in a bipartite graph alternate between the two sides, so the cycle has even length. The other direction gives a construction: in each connected component, color a vertex by the parity of its distance from a fixed root. The theorem turns a statement about all 2-colorings into a statement about a single object, an odd cycle, and so gives every NO answer of the [two-colorability problem](/bipartite-graph-test/) a short certificate.

## Statement

Let $G = (V, E)$ be an undirected graph. A *cycle* of length $k \ge 3$ is a sequence of distinct vertices $u_1, \ldots, u_k$ with $u_i u_{i+1} \in E$ for $i < k$ and $u_k u_1 \in E$. If $G$ has loops or parallel edges, a loop is a cycle of length 1 and two parallel edges form a cycle of length 2.

**Theorem (König 1936).** $G$ is bipartite, that is, $V$ has a partition $V = A \cup B$ such that each edge has one end in $A$ and one end in $B$, if and only if $G$ contains no cycle of odd length.

Equivalently, $\chi(G) \le 2$ if and only if $G$ has no odd cycle.

## In plain words

Split the points of a network into two teams so that every line joins the two teams. Walk around a loop in the network: each step changes the team, so you get back to the start only after an even number of steps. So a loop with an odd number of steps makes the split impossible.

The theorem says the converse is also true. If no such odd loop exists, a split always exists. Pick a start point, and put each point on the team given by whether its distance from the start is even or odd. A line inside one team would close an odd loop, and there is none.

## Proof

We prove a lemma first. A *closed walk* of length $k \ge 1$ is a sequence $w_0, w_1, \ldots, w_k = w_0$ in which consecutive vertices are joined by an edge; vertices and edges may repeat.

**Lemma.** Every closed walk of odd length contains an odd cycle, that is, the vertices of some odd cycle of $G$ appear on it with its edges.

*Proof of the lemma.* Induction on the length $k$. If $k = 1$, the walk is a loop, a cycle of length 1. Let $k \ge 3$ be odd. If the vertices $w_0, \ldots, w_{k-1}$ are distinct, the walk is a cycle of length $k$. Otherwise $w_i = w_j$ for some $0 \le i < j \le k - 1$. Cut the walk at this vertex into two closed walks: $w_i, w_{i+1}, \ldots, w_j$ of length $j - i$, and $w_j, \ldots, w_k = w_0, w_1, \ldots, w_i$ of length $k - (j - i)$. Both lengths are at least 1 and less than $k$, and their sum $k$ is odd, so one of them is odd. By induction it contains an odd cycle, which is also on the original walk. $\square$

**Bipartite implies no odd cycle.** Let $V = A \cup B$ be a bipartition and $u_1, \ldots, u_k$ a cycle. Each edge of the cycle joins $A$ and $B$, so the side changes at each of the $k$ steps from $u_1$ around back to $u_1$. Returning to the side of $u_1$ takes an even number of changes, so $k$ is even. A loop would join a vertex to itself, inside one side, so a bipartite graph has no loop either.

**No odd cycle implies bipartite.** Assume $G$ has no odd cycle. It is enough to two-color each connected component, since the components share no edges. Fix a component $C$ and a vertex $r \in C$. Let $\mathrm{dist}(v)$ be the length of a shortest path from $r$ to $v$, which is finite for $v \in C$. Put $v$ in $A$ if $\mathrm{dist}(v)$ is even and in $B$ if it is odd.

Suppose an edge $uv$ of $C$ has both ends on one side, so that $\mathrm{dist}(u) + \mathrm{dist}(v)$ is even. Follow a shortest path from $r$ to $u$, then the edge $uv$, then a shortest path from $v$ back to $r$. This is a closed walk of length $\mathrm{dist}(u) + 1 + \mathrm{dist}(v)$, which is odd. By the lemma, $G$ contains an odd cycle, a contradiction. So each edge of $C$ joins $A$ and $B$. Doing this in each component gives a bipartition of $G$. $\blacksquare$

## Consequences

- **Linear-time test with a certificate.** The second half of the proof is an algorithm: [breadth-first search](/breadth-first-search/) from a root of each component, color by the parity of the layer, and check all edges. A bad edge and the two BFS paths to their common ancestor give an odd cycle. This is [bipartiteness testing](/bipartiteness-testing/), in $\Theta(n + m)$ time.
- **Short proofs both ways.** Two-colorability has a polynomial certificate for YES (a coloring) and for NO (an odd cycle). For $k \ge 3$ colors no such NO certificate is known, and none exists unless NP = coNP, because [three-coloring](/three-coloring/) is NP-complete.
- **Classes of bipartite graphs.** Trees and forests have no cycles, so they are bipartite. Even cycles, grids, hypercubes $Q_d$, and the [bipartite double cover](/bipartite-double-cover/) of any graph have only even cycles.
- **Chromatic number 3 from an odd cycle.** A graph with an odd cycle has $\chi \ge 3$. In particular $\chi(C_{2k+1}) = 3$, the second extreme case of [Brooks' theorem](/brooks-theorem/).
- **Odd girth.** The length of a shortest odd cycle (the *odd girth*) is a measure of how far from bipartite a graph is locally. Breadth-first search from every vertex finds it in $O(n m)$ time.
- **Matching theory.** [König's theorem](/konig-theorem/) and Hall's theorem hold for bipartite graphs, and the odd cycles (blossoms) are exactly what makes matching in general graphs harder.

## Tightness

- **Odd cycles cannot be replaced by triangles.** A triangle-free graph need not be bipartite: $C_5$ has no triangle and $\chi(C_5) = 3$. The [Mycielski graphs](/mycielski-graph/) are triangle-free with arbitrarily large chromatic number. So no list of short odd cycles characterizes the bipartite graphs; all odd lengths are needed.
- **No analogue for three colors.** There is no characterization of 3-colorable graphs by a finite family of forbidden subgraphs. By Erdős (1959) there are graphs with no short cycles at all and arbitrarily large chromatic number.
- **Odd closed walks.** The theorem is often stated with "closed walk of odd length" in place of "odd cycle". The lemma shows that the two versions are the same.
- **Infinite graphs.** The same proof works for infinite graphs, with one root chosen in each component.

## History

Dénes König proved the theorem in his 1936 book on graph theory, *Theorie der endlichen und unendlichen Graphen*, the first textbook of the subject. It now appears in the first chapter of most graph theory texts, for example Diestel (Proposition 1.6.1) and West (Theorem 1.2.18). The algorithmic reading through breadth-first layers is standard in algorithms texts such as Kleinberg and Tardos.

## References
