---
tag: K6YJC5
kind: definition
slug: complement-graph
name: Complement graph
aliases:
- graph complement
area: graphs/graph-representation
level: intro
summary: Graph on the same vertices with exactly the non-edges of the original.
prereqs: [graph, complete-graph]
see_also: [complete-graph, clique, independent-set, adjacency-matrix, independence-number, perfect-graph, dense-graph, sparse-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1 (Graphs), the complement of a graph; Chapter 5 (Colouring) on perfect graphs and complements
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1 (complement, clique and independent set, self-complementary graphs) and the exercises of Section 1.1 on self-complementary graphs; Section 1.2 (the statement that G or its complement is connected)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.5.1 (The clique problem), the reduction to and from vertex cover through the complement graph
---

The complement of a simple undirected [graph](/graph/) $G = (V, E)$ is the graph $\overline{G}$ on the same vertices in which two distinct vertices are adjacent exactly when they are not adjacent in $G$. So the edges of $G$ and of $\overline{G}$ split the edges of the [complete graph](/complete-graph/) $K_n$. A [clique](/clique/) of $G$ is an [independent set](/independent-set/) of $\overline{G}$, and this swap is the base of several reductions between NP-complete problems. Building $\overline{G}$ explicitly costs $\Theta(n^2)$ time when $G$ is sparse, so fast algorithms often work on the complement without building it.

## Definition

Let $G = (V, E)$ be a simple undirected graph with $n = |V|$ and $m = |E|$. Its **complement** is

$$\overline{G} = \left(V,\ \binom{V}{2} \setminus E\right),$$

where $\binom{V}{2}$ is the set of all 2-element subsets of $V$. So for $u \ne v$, $\{u, v\} \in E(\overline{G}) \iff \{u, v\} \notin E$. A vertex is never adjacent to itself in either graph. The basic facts follow directly:

- $\overline{\overline{G}} = G$, because $\binom{V}{2} \setminus (\binom{V}{2} \setminus E) = E$ when $E \subseteq \binom{V}{2}$.
- $|E(\overline{G})| = \binom{n}{2} - m$.
- $d_{\overline{G}}(v) = n - 1 - d_G(v)$ for each $v$, since $v$ has $n - 1$ possible neighbours.
- $S \subseteq V$ is a clique of $G$ if and only if $S$ is an independent set of $\overline{G}$. So $\omega(G) = \alpha(\overline{G})$, where $\omega$ is the [clique number](/clique-number/) and $\alpha$ the [independence number](/independence-number/).

**Directed complement.** For a directed graph $G = (V, E)$ without self-loops, $\overline{G} = (V, \{(u, v) : u \ne v\} \setminus E)$. If loops are allowed, the complement is taken in $V \times V$. The definition must say which convention it uses.

**Self-complementary.** $G$ is *self-complementary* when $G$ is isomorphic to $\overline{G}$. Then $m = \binom{n}{2} - m$, so $\binom{n}{2} = 2m$ is even, and $n \equiv 0$ or $1 \pmod 4$. Self-complementary graphs exist for each such $n$.

**Theorem.** For each simple graph $G$, at least one of $G$ and $\overline{G}$ is connected.

*Proof.* Assume $G$ is not connected, and let $u, v$ be two vertices. If $u$ and $v$ are in different components of $G$, then $\{u, v\} \notin E$, so they are adjacent in $\overline{G}$. If they are in the same component $C$, pick a vertex $x$ in another component, which exists because $G$ is not connected. Then $\{u, x\}$ and $\{x, v\}$ are not edges of $G$, so $u, x, v$ is a path in $\overline{G}$. So each two vertices are joined in $\overline{G}$, and $\overline{G}$ is connected. $\square$

## Examples and non-examples

**A worked example.** Let $G$ be the graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$, so $m = 7$. Then $\overline{G}$ has the $\binom{6}{2} - 7 = 8$ edges

$$03, 04, 05, 14, 15, 24, 25, 35.$$

The degrees in $G$ are $2, 3, 3, 3, 2, 1$, and in $\overline{G}$ they are $3, 2, 2, 2, 3, 4$; each pair sums to $n - 1 = 5$. The triangle $\{0, 1, 2\}$ of $G$ is an independent set of $\overline{G}$. The set $\{0, 4\}$ is independent in $G$ and an edge of $\overline{G}$.

**Self-complementary graphs.** The path $P_4$ with the edges $01, 12, 23$ has the complement with the edges $02, 03, 13$, which is the path $2, 0, 3, 1$. So $P_4$ is self-complementary, with $n = 4$ and $m = 3 = \binom{4}{2}/2$. The cycle $C_5$ with the edges $01, 12, 23, 34, 40$ has the complement $02, 03, 13, 14, 24$, which is the cycle $0, 2, 4, 1, 3$. So $C_5$ is self-complementary too.

**Extreme cases.** The complement of $K_n$ is the empty graph on $n$ vertices. The complement of the complete bipartite graph $K_{p, q}$ is the disjoint union $K_p \cup K_q$.

**Non-examples.**

- Taking the complement does not mean reversing the edges of a directed graph. That is the [transpose graph](/transpose-graph/).
- The complement of a [multigraph](/multigraph/) is not defined in this sense, because "not an edge" does not say how many parallel edges to add.
- No graph on 3 vertices is self-complementary, because $\binom{3}{2} = 3$ is odd.

**The cost of the complement.** With $n$ vertices and $m$ edges:

| input | output | time |
|---|---|---|
| [adjacency matrix](/adjacency-matrix/) | adjacency matrix of $\overline{G}$ | $\Theta(n^2)$: flip each cell off the diagonal |
| [bitset adjacency matrix](/bitset-adjacency-matrix/) | bitset matrix of $\overline{G}$ | $\Theta(n^2/w)$: one NOT per word, then clear the diagonal and the padding bits |
| [adjacency list](/adjacency-list/) | adjacency list of $\overline{G}$ | $\Theta(n^2)$, since the output alone has $2(\binom{n}{2} - m)$ entries |
| adjacency list | an adjacency query on $\overline{G}$ | the cost of a query on $G$, with the answer negated |

So a sparse graph has a dense complement. A [breadth-first search](/breadth-first-search/) of $\overline{G}$ can still run in $O(n + m)$ time from the adjacency list of $G$, without building $\overline{G}$. Keep the set $U$ of unvisited vertices in a linked list. To scan a vertex $u$, mark the $G$-neighbours of $u$, then move each unmarked vertex of $U$ to the queue, and keep the marked ones in $U$. Each vertex leaves $U$ once, and each vertex that stays in $U$ during the scan of $u$ is charged to an edge of $G$ at $u$. So the total work is $O(n + m)$.

## Related definitions

- [Complete graph](/complete-graph/): $G$ and $\overline{G}$ split its edges.
- [Clique](/clique/) and [independent set](/independent-set/): the complement swaps them.
- [Perfect graph](/perfect-graph/): by the weak perfect graph theorem of Lovász, $G$ is perfect if and only if $\overline{G}$ is.
- [Transpose graph](/transpose-graph/): a different operation, for directed graphs.

## References
