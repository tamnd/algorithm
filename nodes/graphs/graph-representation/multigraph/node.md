---
tag: TM13YX
kind: definition
slug: multigraph
name: Multigraph
aliases:
- multiple-edge graph
area: graphs/graph-representation
level: intro
summary: Graph that allows parallel edges between the same pair of vertices.
prereqs: [graph, edge, simple-graph]
see_also: [simple-graph, self-loop, incidence-list, eulerian-circuit, karger-min-cut, degree, handshake-lemma, hypergraph]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1 (Graphs), Section 1.1, graphs with an incidence function, loops and parallel edges, and simple graphs
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.10 (Other notions of graphs), multigraphs with loops and multiple edges
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the remark on multigraphs; Section 20.1, Exercise 20.1-4 on the equivalent undirected graph of a multigraph
---

A multigraph is a [graph](/graph/) in which two or more [edges](/edge/) may join the same pair of [vertices](/vertex/). Such edges are called parallel, and many authors also allow [self-loops](/self-loop/). Because two parallel edges have the same ends, an edge of a multigraph is not a pair of vertices but a name with an incidence function that gives its ends. Multigraphs arise from road and rail maps, from the bridges of Königsberg, and inside algorithms that contract edges, such as [Karger's minimum cut](/karger-min-cut/). The [simple graph](/simple-graph/) is the special case with no loops and no parallel edges.

## Definition

**Undirected multigraph.** An undirected multigraph is a triple $G = (V, E, \psi)$ of a finite set $V$ of vertices, a finite set $E$ of edges with $V \cap E = \emptyset$, and an incidence function

$$\psi : E \to \{\{u, v\} : u, v \in V\},$$

where $\{u, v\}$ has one element when $u = v$. The vertices in $\psi(e)$ are the *ends* of $e$. An edge with $\psi(e) = \{v\}$ is a self-loop at $v$. Two distinct edges $e \ne f$ with $\psi(e) = \psi(f)$ are *parallel*. This is the definition of Bondy and Murty, where every graph is of this kind.

**Directed multigraph.** The same, with $\psi : E \to V \times V$, so that each edge $e$ has a tail and a head, $\psi(e) = (t(e), h(e))$. Two edges with the same tail and head are parallel. The edges $(u, v)$ and $(v, u)$ are not parallel: they are antiparallel.

**Multiplicity.** The *multiplicity* $\mu(u, v) = |\{e \in E : \psi(e) = \{u, v\}\}|$ is the number of edges with the ends $u$ and $v$. The multigraph is determined, up to the names of its edges, by $V$ and the function $\mu$, so it can be seen as a *multiset* of pairs. The *underlying simple graph* has the edge $\{u, v\}$ for each $u \ne v$ with $\mu(u, v) \ge 1$.

**Words.** The terms vary between books. Some say *multigraph* only when there are no self-loops and *pseudograph* when loops are allowed. Diestel uses *multigraph* for loops and parallel edges together. CLRS define graphs without parallel edges and mention multigraphs only in remarks and exercises. A page that uses one of these words must say which one it means. On this site, "multigraph" allows both, unless the page says otherwise.

**Degree.** The degree $d(v)$ is the number of edge ends at $v$: each non-loop edge at $v$ adds 1 and each self-loop at $v$ adds 2. With this convention the [handshake lemma](/handshake-lemma/) $\sum_v d(v) = 2|E|$ holds, because each edge has exactly two ends. The degree can be larger than the number of neighbours, $|N(v)|$. In a directed multigraph, $d^+(v)$ and $d^-(v)$ count the edges with tail $v$ and with head $v$; see [in-degree and out-degree](/in-degree-and-out-degree/).

**Size.** A simple graph on $n$ vertices has at most $\binom{n}{2}$ edges. A multigraph on $n \ge 1$ vertices can have any number of edges, so its bounds must use $m$, never $n^2$.

**Representations.** The cost of each form, for $n$ vertices and $m$ edges:

| representation | how it stores parallel edges | space | notes |
|---|---|---|---|
| [incidence list](/incidence-list/) | one record for each edge | $\Theta(n + m)$ | each edge has a name; $O(1)$ removal of a given edge |
| [adjacency list](/adjacency-list/) | the neighbour repeated $\mu(u, v)$ times | $\Theta(n + m)$ | parallel copies cannot be told apart |
| [adjacency matrix](/adjacency-matrix/) | $A[u, v] = \mu(u, v)$ | $\Theta(n^2)$ | an entry counts edges; edge data is lost |
| [edge list](/edge-list/) | each edge once | $\Theta(m)$ | the natural input format |
| [incidence matrix](/incidence-matrix/) | equal columns | $\Theta(nm)$ | entry 2 for an undirected loop |

The matrix of multiplicities has a choice for a loop: some authors put the number of loops at $v$ in $A[v, v]$, others twice that number, so that the row sums are the degrees. The [weighted graph](/weighted-graph/) with $w(u, v) = \mu(u, v)$ is the same data when the edges need no names.

## Examples and non-examples

**Königsberg.** The seven bridges of Königsberg join four land masses $A$ (the island), $B$, $C$ and $D$. With $\mu(A, B) = 2$, $\mu(A, C) = 2$, $\mu(A, D) = 1$, $\mu(B, D) = 1$ and $\mu(C, D) = 1$, the multigraph has 7 edges and the degrees $d(A) = 5$, $d(B) = 3$, $d(C) = 3$, $d(D) = 3$. They sum to $14 = 2 \cdot 7$. All four degrees are odd, so there is no walk that crosses each bridge exactly once: such a walk exists in a connected multigraph only when at most two vertices have odd degree (see [Eulerian path](/eulerian-path/)). The underlying simple graph has only 5 edges.

**A loop and parallel edges.** Let $V = \{u, v\}$ and $E = \{a, b, c\}$ with $\psi(a) = \psi(b) = \{u, v\}$ and $\psi(c) = \{u\}$. Then $\mu(u, v) = 2$, $d(u) = 2 + 2 = 4$, $d(v) = 2$, and $4 + 2 = 2 \cdot 3$.

**Contraction.** Contracting the edge $\{x, y\}$ of the triangle on $x, y, z$ merges $x$ and $y$ into one vertex $w$. The edges $\{x, z\}$ and $\{y, z\}$ become two parallel edges between $w$ and $z$, and the edge $\{x, y\}$ itself is dropped. Karger's algorithm keeps such parallel edges, because a cut between $w$ and $z$ must cut both.

**A simple graph is a multigraph.** Each simple graph is a multigraph with $\mu \le 1$ and no loops. So results about multigraphs apply to simple graphs.

**Non-examples.**

- An edge with three ends is not allowed: that is a [hypergraph](/hypergraph/).
- A graph given only as a set $E$ of pairs, as in CLRS, cannot have parallel edges: adding $\{u, v\}$ twice to a set gives the same set. This is the law that a [graph](/graph/) type with `add-edge` meets and a multigraph breaks.

## Related definitions

- **Simple graph.** A multigraph with no loops and no parallel edges. See [simple graph](/simple-graph/).
- **Self-loop.** An edge whose two ends are the same vertex. See [self-loop](/self-loop/).
- **Weighted graph.** A simple graph with a weight on each edge can stand for a multigraph by $w = \mu$ when only the counts matter. See [weighted graph](/weighted-graph/).
- **Eulerian multigraphs.** Euler circuits are naturally a multigraph notion; [Hierholzer's algorithm](/eulerian-circuit/) works on an incidence list, where each parallel edge has its own name.
- **Line graph.** The [line graph](/line-graph/) is usually defined for simple graphs only; for multigraphs, parallel edges share two ends.

## References
