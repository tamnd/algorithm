---
tag: WEB21S
kind: definition
slug: sparse-graph
name: Sparse graph
area: graphs/graph-representation
level: intro
summary: Graph with far fewer edges than the maximum, typically O(V) edges.
prereqs: [graph, simple-graph]
see_also: [dense-graph, adjacency-list, compressed-sparse-row, planar-graph, degeneracy, arboricity, sparse-matrix, webgraph-compression]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), sparse graphs with |E| much less than |V|^2 and the choice of adjacency lists for them
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the discussion of sparse and dense graphs and of the choice of representation
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 4 (Planar graphs), Section 4.2, the bound of at most 3n - 6 edges on a planar graph with n at least 3 vertices
---

A sparse graph is a [graph](/graph/) with far fewer [edges](/edge/) than the largest possible number, usually $m = O(n)$ for $n$ vertices. Road networks, power grids, meshes, [planar graphs](/planar-graph/), trees and most real networks are sparse: each vertex has a few neighbours, however large the graph is. Like "dense", the word is about a family of growing graphs, not one graph. For sparse graphs, an [adjacency list](/adjacency-list/) uses $\Theta(n + m) = \Theta(n)$ space, while an [adjacency matrix](/adjacency-matrix/) would use $\Theta(n^2)$, and linear-time algorithms run in $\Theta(n)$ time.

## Definition

Let $\mathcal{G}$ be an infinite family of [simple](/simple-graph/) graphs, and write $n$ and $m$ for the numbers of vertices and edges of a member. The family is **sparse** if

$$m = O(n),$$

that is, there is a constant $c$ with $m \le c n$ for every member. It is **dense** if $m = \Theta(n^2)$; see [dense graph](/dense-graph/). Between them lie families like $m = \Theta(n \log n)$ or $m = \Theta(n^{3/2})$, which some authors also call sparse, in the weaker sense $m = o(n^2)$. CLRS use the informal form "$|E|$ much less than $|V|^2$". A page that uses "sparse" in a bound must say which form it means.

**Average degree.** Since $\sum_v d(v) = 2m$, the family is sparse if and only if the average degree $2m/n$ is bounded by a constant. Sparse does not mean that every degree is small: the star $K_{1, n-1}$ has $m = n - 1$ but one vertex of degree $n - 1$.

**Hereditary sparsity.** $m = O(n)$ for the whole graph does not stop a dense part: a graph made of a clique on $\sqrt{n}$ vertices and $n - \sqrt{n}$ isolated vertices has $m < n/2$. Stronger notions ask every [subgraph](/subgraph/) to be sparse:

- **Degeneracy** $d$: each subgraph has a vertex of degree at most $d$. Then $m \le d n$, and the vertices can be ordered so that each has at most $d$ neighbours after it. See [degeneracy](/degeneracy/).
- **Arboricity** $a$: the edges split into $a$ forests, so $m \le a(n - 1)$. By the Nash-Williams theorem, $a = \max_H \lceil m_H / (n_H - 1) \rceil$ over subgraphs $H$ with $n_H \ge 2$. See [arboricity](/arboricity/).
- **Bounded degree** $\Delta$: $m \le \Delta n / 2$.

Each bounded-degree family has bounded degeneracy, and bounded degeneracy is the same as bounded arboricity, since $a \le d \le 2a - 1$.

**Costs on a sparse graph.** For $m = O(n)$:

| operation | adjacency list | adjacency matrix |
|---|---|---|
| space | $\Theta(n)$ | $\Theta(n^2)$ |
| [breadth-first](/breadth-first-search/) or [depth-first search](/depth-first-search/) | $\Theta(n)$ | $\Theta(n^2)$ |
| test $\{u, v\} \in E$ | $O(1 + d(u))$, or $O(1)$ expected with [hashing](/hash-based-adjacency/) | $O(1)$ |
| list $N(v)$ | $\Theta(1 + d(v))$ | $\Theta(n)$ |
| Dijkstra with a binary heap | $O(n \log n)$ | not useful |

Even reading an adjacency matrix costs $\Theta(n^2)$ time, so no algorithm that reads a matrix can be linear on a sparse graph. The [compressed sparse row](/compressed-sparse-row/) form stores a static sparse graph in $n + 1 + m$ integers, and [WebGraph compression](/webgraph-compression/) goes down to a few bits per edge for web graphs.

## Examples and non-examples

**Sparse families.**

- Trees and forests: $m \le n - 1$.
- [Planar graphs](/planar-graph/): $m \le 3n - 6$ for $n \ge 3$, by [Euler's formula](/euler-formula/). Planar graphs are 5-degenerate, since each one has a vertex of degree at most 5.
- $k$-[regular graphs](/regular-graph/) for a fixed $k$: $m = kn/2$.
- Grids: the $r \times r$ grid has $n = r^2$ and $m = 2r(r - 1) < 2n$.
- Road networks: a junction meets only a few roads, so the average degree stays small as the network grows.

**Not sparse.**

- The complete graphs $K_n$: $m = n(n-1)/2$. They are dense.
- The hypercubes $Q_d$ with $n = 2^d$: $m = \tfrac12 n \lg n$. They are not sparse in the sense $m = O(n)$, but they are sparse in the weaker sense $m = o(n^2)$.
- One graph alone, such as a graph with 10 vertices and 12 edges, is neither sparse nor dense: the words describe growth.

## Related definitions

- **Dense graph.** $m = \Theta(n^2)$. See [dense graph](/dense-graph/).
- **Sparse matrix.** A matrix with few nonzero entries; the adjacency matrix of a sparse graph is one. See [sparse matrix](/sparse-matrix/).
- **Degeneracy and arboricity.** Measures of sparsity that hold for every subgraph. See [degeneracy](/degeneracy/) and [arboricity](/arboricity/).
- **Planar graph.** The main example of a hereditarily sparse family. See [planar graph](/planar-graph/).

## References
