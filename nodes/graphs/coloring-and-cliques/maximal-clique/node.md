---
tag: DH9MMA
kind: definition
slug: maximal-clique
name: Maximal clique
aliases:
- maximal complete subgraph
area: graphs/coloring-and-cliques
level: intro
summary: A clique that is not contained in any larger clique.
prereqs: [clique]
see_also: [maximum-clique, clique-number, maximal-clique-enumeration, bron-kerbosch, maximal-independent-set, chordal-graph]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1 (cliques); the distinction between maximal and maximum is made in Section 3.1
  - paper: doi:10.1007/BF02760024
    title: J. W. Moon and L. Moser, On cliques in graphs, Israel Journal of Mathematics 3(1), 23 to 28 (1965)
    locator: the theorem on the largest number of maximal cliques in a graph with n vertices
  - paper: doi:10.1145/362342.362367
    title: Coen Bron and Joep Kerbosch, Algorithm 457, Finding all cliques of an undirected graph, Communications of the ACM 16(9), 575 to 577 (1973)
    locator: the whole paper (the word clique means a maximal complete subgraph there)
---

A maximal clique of a graph is a [clique](/clique/) that cannot be made larger by adding one more vertex: no vertex outside it is adjacent to all of its vertices. It is a local notion. A largest clique, a [maximum clique](/maximum-clique/), is always maximal, but a maximal clique can be much smaller than a maximum one. Some older papers, such as that of Bron and Kerbosch, use the plain word "clique" for a maximal clique.

## Definition

Let $G = (V, E)$ be a finite simple undirected graph and let $N(v)$ be the set of neighbors of $v$. A set $C \subseteq V$ is a **clique** if every two distinct vertices of $C$ are adjacent. A clique $C$ is **maximal** if

$$\forall v \in V \setminus C: \quad C \not\subseteq N(v),$$

that is, each vertex outside $C$ has a non-neighbor in $C$. Equivalently, $C$ is maximal under inclusion among the cliques of $G$: no clique $C'$ satisfies $C \subsetneq C'$. The two forms are the same because a clique $C' \supsetneq C$ contains some $v \notin C$, and then $C \cup \{v\}$ is already a clique.

A clique is **maximum** if no clique of $G$ has more vertices; its size is the [clique number](/clique-number/) $\omega(G)$.

By the definition, the empty set is a maximal clique only when $V = \emptyset$. Every vertex lies in at least one maximal clique, and so does every edge: grow the set one vertex at a time while some outside vertex is adjacent to all of it. This greedy step stops after at most $n$ additions.

## Examples and non-examples

Take the graph with vertices $0, \ldots, 5$ and edges $01, 02, 12, 13, 23, 34, 45$.

- **Maximal cliques.** $\{0, 1, 2\}$, $\{1, 2, 3\}$, $\{3, 4\}$ and $\{4, 5\}$. These are all of them.
- **Maximal but not maximum.** $\{3, 4\}$ is maximal: the only other neighbor of 4 is 5, and 5 is not adjacent to 3; the other neighbors of 3 are 1 and 2, and neither is adjacent to 4. But $\{0, 1, 2\}$ is larger, so $\{3, 4\}$ is not maximum. Here $\omega = 3$.
- **A clique that is not maximal.** $\{1, 2\}$ is a clique, but both 0 and 3 are adjacent to 1 and 2.
- **Not a clique.** $\{0, 1, 3\}$, because 0 and 3 are not adjacent.
- **Isolated vertex.** In a graph with an isolated vertex $v$, the set $\{v\}$ is a maximal clique.
- **Cycles and triangle-free graphs.** In a graph with no triangle, the maximal cliques are the edges and the isolated vertices. So $C_5$ has 5 maximal cliques, all of size 2, and the Petersen graph has 15.
- **Many maximal cliques.** The complete 3-partite graph $K_{3,3,3}$ (three groups of 3 vertices, with an edge between every two vertices of different groups) has $3^3 = 27$ maximal cliques: choose one vertex from each group. Moon and Moser proved that a graph with $n$ vertices has at most $3^{n/3}$ maximal cliques when $3$ divides $n$, at most $4 \cdot 3^{(n-4)/3}$ when $n \equiv 1 \pmod 3$ and $n \ge 4$, and at most $2 \cdot 3^{(n-2)/3}$ when $n \equiv 2 \pmod 3$. These bounds are reached by complete multipartite graphs whose groups have size 3, except for one group of size 4 (or two groups of size 2) when $n \equiv 1$, and one group of size 2 when $n \equiv 2$. For $n = 1$ to $6$ the largest counts are 1, 2, 3, 4, 6 and 9.

## Related definitions

- **Maximal independent set.** $C$ is a maximal clique of $G$ if and only if $C$ is a [maximal independent set](/maximal-independent-set/) of the [complement graph](/complement-graph/). So the two have the same counts and the same listing algorithms.
- **Maximum clique.** Finding a largest clique is the [maximum clique problem](/maximum-clique/), which is NP-hard. Finding one maximal clique is easy: the greedy growth above takes $O(n + m)$ time.
- **Listing them.** The [maximal clique enumeration](/maximal-clique-enumeration/) problem asks for all maximal cliques. The [Bron-Kerbosch algorithm](/bron-kerbosch/) with pivoting does this in $O(3^{n/3})$ time, which matches the Moon-Moser bound.
- **Chordal graphs.** A [chordal graph](/chordal-graph/) with $n$ vertices has at most $n$ maximal cliques, and a [perfect elimination ordering](/perfect-elimination-ordering/) lists them in linear time.

## References
