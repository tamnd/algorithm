---
tag: DWMSS8
kind: definition
slug: simple-graph
name: Simple graph
aliases:
- loopless simple graph
area: graphs/graph-representation
level: intro
summary: Graph with no self-loops and no parallel edges.
prereqs: [graph, edge, vertex]
see_also: [multigraph, self-loop, undirected-graph, complete-graph, degree, handshake-lemma, labeled-graph, sparse-graph]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1 (Graphs), Section 1.1, simple graphs as graphs with no loops and no parallel edges
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), undirected graphs with edges as unordered pairs of distinct vertices
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, simple graphs, and the count of simple graphs with a fixed vertex set
---

A simple graph is an undirected [graph](/graph/) with no [self-loops](/self-loop/) and no parallel edges: each [edge](/edge/) joins two different [vertices](/vertex/), and two vertices are joined by at most one edge. So the graph is fixed by its vertex set and a set of 2-element subsets of it. This is the default graph of most algorithm books, including CLRS, and of most graph theory results. Its main use in algorithms is the bound $m \le n(n-1)/2$, which turns costs in $m$ into costs in $n$.

## Definition

A **simple graph** is a pair $G = (V, E)$ where $V$ is a finite set and

$$E \subseteq \binom{V}{2} = \{\{u, v\} : u, v \in V,\ u \ne v\}.$$

Equivalently, it is a [multigraph](/multigraph/) $(V, E, \psi)$ in which $\psi$ is injective (no parallel edges) and no $\psi(e)$ has one element (no loops). Equivalently again, it is a symmetric, irreflexive binary relation on $V$: $u \sim v \iff \{u, v\} \in E$.

**Directed version.** A *simple directed graph* is $(V, E)$ with $E \subseteq V \times V$ and no loops $(v, v)$. Each ordered pair occurs at most once, but $(u, v)$ and $(v, u)$ may both be edges. CLRS allow loops in directed graphs, so their directed graphs are simple in the sense of no parallel edges only. A page that says "simple digraph" must say which it means.

**Consequences.** For a simple graph with $n = |V|$ and $m = |E|$:

- $0 \le m \le \binom{n}{2} = n(n-1)/2$, with $m = \binom{n}{2}$ only for the [complete graph](/complete-graph/) $K_n$. For a simple directed graph without loops, $m \le n(n-1)$.
- $0 \le d(v) \le n - 1$ for each vertex, and $d(v) = |N(v)|$, the number of neighbours.
- $\sum_v d(v) = 2m$, the [handshake lemma](/handshake-lemma/).
- In every simple graph with $n \ge 2$ two vertices have the same degree. *Proof.* The $n$ degrees lie in $\{0, \ldots, n - 1\}$. The values $0$ and $n - 1$ cannot both occur: a vertex of degree $n - 1$ is adjacent to every other vertex, so none has degree 0. So the degrees take at most $n - 1$ values, and by the pigeonhole principle two are equal. $\square$
- There are $2^{\binom{n}{2}}$ simple graphs on a fixed set of $n$ [labeled](/labeled-graph/) vertices.
- $\lg m \le 2 \lg n$, so $O(\log m) = O(\log n)$. This is why bounds like $O(m \log m)$ and $O(m \log n)$ are the same for simple graphs.

**In the stored forms.** An [adjacency matrix](/adjacency-matrix/) of a simple graph is a symmetric 0-1 matrix with zero diagonal, and it holds $n^2$ bits for $\binom{n}{2}$ bits of information. An [adjacency list](/adjacency-list/) holds each edge twice, so it has $2m$ entries and $\Theta(n + m)$ words; it represents a simple graph only if no list repeats a vertex and no list of $v$ holds $v$. Checking that a list is simple costs $\Theta(n + m)$ time with an array of $n$ marks, and removing repeats and loops costs the same.

## Examples and non-examples

**Examples.**

- $K_n$, the complete graph: all $\binom{n}{2}$ edges. $K_4$ has 6 edges and each degree is 3.
- The path $1\text{-}2\text{-}3\text{-}4$, with $E = \{12, 23, 34\}$ and the degrees $1, 2, 2, 1$.
- The graph with $n$ vertices and no edges, the empty graph $\overline{K_n}$.

**Non-examples.**

- The bridges of Königsberg: two bridges join the island to each of two banks, so there are parallel edges. It is a [multigraph](/multigraph/).
- The graph on $\{1, 2\}$ with the edges $\{1, 2\}$ and the loop $\{1\}$: it has a loop.
- The directed graph with the edges $(1, 2)$ and $(2, 1)$ is a simple directed graph, but it is not a simple graph, because a simple graph is undirected. Its *underlying* simple graph has the one edge $\{1, 2\}$.

**Making a graph simple.** From an edge list with loops and repeats, keep $\{u, v\}$ when $u \ne v$ and it was not seen before. With the edges sorted by $(\min, \max)$ by [radix sort](/radix-sort/), this is one scan, so the whole step costs $\Theta(n + m)$ time.

## Related definitions

- **Multigraph.** Allows parallel edges and, usually, loops. See [multigraph](/multigraph/).
- **Self-loop.** An edge whose two ends are one vertex. See [self-loop](/self-loop/).
- **Undirected graph.** On this site an undirected graph is simple unless the page says otherwise. See [undirected graph](/undirected-graph/).
- **Complement.** The [complement](/complement-graph/) $\overline{G}$ of a simple graph has the edges $\binom{V}{2} \setminus E$. It is defined only for simple graphs.
- **Sparse and dense.** For simple graphs, $m$ ranges from 0 to $\Theta(n^2)$; [sparse graphs](/sparse-graph/) have $m = O(n)$, and [dense graphs](/dense-graph/) have $m = \Theta(n^2)$.

## References
