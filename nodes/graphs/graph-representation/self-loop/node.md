---
tag: G87QYC
kind: definition
slug: self-loop
name: Self-loop
aliases:
- loop
area: graphs/graph-representation
level: intro
summary: Edge whose two endpoints are the same vertex.
prereqs: [graph, edge, vertex]
see_also: [multigraph, simple-graph, degree, handshake-lemma, adjacency-matrix, incidence-matrix, directed-graph, functional-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), self-loops in directed graphs and their exclusion from undirected graphs
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1 (Graphs), Section 1.1, loops, and the convention that a loop counts twice in the degree
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, loops and multiple edges; Section 1.2, the degree of a vertex and the degree-sum formula
---

A self-loop, or loop, is an [edge](/edge/) whose two ends are the same [vertex](/vertex/). In a [directed graph](/directed-graph/) it is the pair $(v, v)$, and it says that $v$ is related to itself. Whether loops are allowed depends on the kind of graph: CLRS allow them in directed graphs and forbid them in undirected graphs, a [simple graph](/simple-graph/) has none, and a [multigraph](/multigraph/) usually allows them. Loops change the rules for degree and for the stored forms, so code that reads graphs must know whether they can occur.

## Definition

**Directed.** In a directed graph $G = (V, E)$ with $E \subseteq V \times V$, a self-loop is an edge $(v, v) \in E$. A vertex has at most one loop, because $E$ is a set. The loop is an out-edge and an in-edge of $v$, so it adds 1 to the out-degree $d^+(v)$ and 1 to the in-degree $d^-(v)$, and $v \in N^+(v)$ and $v \in N^-(v)$. With this, $\sum_v d^+(v) = \sum_v d^-(v) = |E|$ still holds.

**Undirected.** If the edges are 2-element subsets $\{u, v\}$ with $u \ne v$, as in CLRS, there are no loops. To allow them, the edge set is a set of subsets of $V$ of size 1 or 2, and $\{v\}$ is the loop at $v$. In a multigraph $(V, E, \psi)$, an edge $e$ with $\psi(e) = \{v\}$ is a loop, and $v$ may carry many loops.

**Degree.** In an undirected graph a loop at $v$ adds **2** to the degree $d(v)$, since both of its ends are at $v$. Then the [handshake lemma](/handshake-lemma/) $\sum_v d(v) = 2|E|$ holds for all graphs with loops. A loop adds only 1 to the number of neighbours $|N(v)|$, and only if $v$ was not already counted.

**In the stored forms.** For $n$ vertices and $m$ edges:

| representation | how a loop at $v$ is stored | note |
|---|---|---|
| directed [adjacency matrix](/adjacency-matrix/) | $A[v, v] = 1$ | the trace counts the loops |
| undirected adjacency matrix | $A[v, v] = 1$, or 2 | with 2, each row sum is the degree; authors differ |
| directed [adjacency list](/adjacency-list/) | $v$ in $\text{Adj}[v]$ once | the list length is $d^+(v)$ |
| undirected adjacency list | $v$ in $\text{Adj}[v]$ once, or twice | once is usual; then the list length is not $d(v)$ |
| [incidence matrix](/incidence-matrix/) | undirected: entry 2 in the row of $v$; directed signed form: column of zeros | the signed form cannot show a loop, so CLRS forbid it |
| [edge list](/edge-list/) | the pair $(v, v)$ | |

Detecting all loops costs $\Theta(n)$ with a matrix (read the diagonal) and $\Theta(n + m)$ with an adjacency list or an edge list.

## Examples and non-examples

**A directed example.** $V = \{1, 2, 3\}$, $E = \{(1, 1), (1, 2), (2, 3), (3, 3)\}$. The loops are at 1 and 3. The out-degrees are $2, 1, 1$ and the in-degrees are $1, 1, 2$; both sum to $4 = |E|$. The adjacency matrix has the diagonal $(1, 0, 1)$.

**An undirected example.** A multigraph on $\{a, b\}$ with one edge $\{a, b\}$ and one loop at $a$: $d(a) = 1 + 2 = 3$, $d(b) = 1$, and $3 + 1 = 2 \cdot 2$. With the degree of the loop taken as 1, the sum would be 3, which is odd, and the handshake lemma would fail.

**Relations.** A binary relation $R$ on $V$ is a directed graph. $R$ is *reflexive* when each vertex has a loop, and *irreflexive* when no vertex has one. The transitive-reflexive closure, the reachability relation, puts a loop on every vertex; the [transitive closure](/transitive-closure/) alone puts a loop on $v$ exactly when $v$ lies on a cycle.

**Functional graphs.** In the [functional graph](/functional-graph/) of $f : V \to V$, with the edges $(v, f(v))$, a loop at $v$ is a fixed point $f(v) = v$. In a [parent-pointer tree](/parent-pointer-tree/), some code marks the root with a loop, $\text{parent}[r] = r$.

**Non-examples.**

- A cycle of length 2, the edges $(u, v)$ and $(v, u)$ with $u \ne v$, is not a loop. In a directed graph it is a pair of antiparallel edges.
- A vertex with no edges is not a loop; it is an isolated vertex, with degree 0.
- Two parallel edges between $u$ and $v$ are not loops; a loop has one end vertex, parallel edges have two.

## Related definitions

- **Simple graph.** A graph with no loops and no parallel edges. See [simple graph](/simple-graph/).
- **Multigraph.** A graph that may have parallel edges and, in most books, loops. See [multigraph](/multigraph/).
- **Loopless graph.** A multigraph with parallel edges but no loops. Bondy and Murty use this term.
- **Degree.** The number of edge ends at a vertex, where a loop has two ends. See [degree](/degree/).
- **Cycle.** A loop is a closed walk of length 1. In a directed graph a loop is a cycle, so a graph with a loop is not a [directed acyclic graph](/directed-acyclic-graph/).

## References
