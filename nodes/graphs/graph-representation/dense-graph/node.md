---
tag: 1YGYZ1
kind: definition
slug: dense-graph
name: Dense graph
area: graphs/graph-representation
level: intro
summary: Graph with a number of edges close to the maximum, typically Θ(V^2).
prereqs: [graph, complete-graph]
see_also: [sparse-graph, complete-graph, adjacency-matrix, adjacency-list, bitset-adjacency-matrix, prim, dijkstra, floyd-warshall]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the choice of the adjacency matrix for dense graphs; Section 21.2 (Prim's algorithm) and Section 22.3 (Dijkstra's algorithm), the running times with an array and with heaps
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the discussion of sparse and dense graphs and of the choice of representation
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 7 (Extremal graph theory), Turan's theorem and the edge density that forces a subgraph
---

A dense graph is a [graph](/graph/) whose number of [edges](/edge/) is within a constant factor of the largest possible number, so $m = \Theta(n^2)$ for $n$ vertices. The word applies to a family of graphs whose size grows, not to one fixed graph. The opposite is a [sparse graph](/sparse-graph/). The distinction decides the choice of representation: an [adjacency matrix](/adjacency-matrix/) costs $\Theta(n^2)$ space, which is the input size of a dense graph anyway, and algorithms such as [Prim's](/prim/) and [Dijkstra's](/dijkstra/) with a plain array run in the optimal $\Theta(n^2)$ time on it.

## Definition

Let $G = (V, E)$ be a simple undirected graph with $n \ge 2$ vertices and $m$ edges. Its **edge density** is

$$\rho(G) = \frac{m}{\binom{n}{2}} \in [0, 1].$$

For a directed graph without loops the denominator is $n(n-1)$. So $\rho(K_n) = 1$ and the empty graph has $\rho = 0$.

A family $\mathcal{G}$ of graphs with unbounded $n$ is **dense** when there is a constant $c > 0$ with $\rho(G) \ge c$ for each $G \in \mathcal{G}$, that is, $m = \Theta(n^2)$. A family is [sparse](/sparse-graph/) when $m = O(n)$, or in a weaker use, when $m = o(n^2)$.

These words have no single standard meaning, and the bounds that use them always state $m$ and $n$. Common uses are:

- **Algorithms.** "Dense" means $m = \Theta(n^2)$, and the analysis compares $n^2$ with $m \log n$ or $m + n \log n$.
- **Extremal graph theory.** "Dense" means $\rho \ge c$ for a fixed $c > 0$, as above.
- **Some texts.** "Dense" means $m = \Omega(n^{1 + \varepsilon})$ for a fixed $\varepsilon > 0$, which is far fewer edges than $\Theta(n^2)$.

The definition is about the growth of $m$ with $n$. A single graph with 10 vertices and 30 edges has $\rho = 30/45 = 2/3$, but it is not dense or sparse by itself.

## Examples and non-examples

**Dense families.**

- The [complete graphs](/complete-graph/) $K_n$, with $\rho = 1$.
- The complete bipartite graphs $K_{n/2, n/2}$ for even $n$, with $m = n^2/4$ and $\rho = \frac{n^2/4}{n(n-1)/2} = \frac{n}{2(n-1)}$, which tends to $\frac12$. They have no triangle, so a dense graph need not have small cycles.
- Random graphs $G(n, p)$ of the [Erdős-Rényi model](/erdos-renyi-model/) with a fixed $p$, whose expected density is exactly $p$.
- The complete graph with distances of the metric [travelling salesman problem](/metric-tsp/), and the distance matrix of [all-pairs shortest paths](/all-pairs-shortest-paths/).

**Sparse families, so non-examples.**

- [Trees](/tree/): $m = n - 1$, so $\rho = 2/n$.
- [Planar graphs](/planar-graph/): $m \le 3n - 6$ for $n \ge 3$, so $\rho \le \frac{6}{n}$.
- Graphs of maximum degree at most $\Delta$: $m \le \Delta n / 2$.
- Road maps and most social networks: their average degree $2m/n$ stays small while $n$ grows.

**Numbers.** The table gives $m$ and the cost of the main representations for three graphs on $n = 10^4$ vertices, with 32-bit vertex numbers.

| graph | $m$ | $\rho$ | adjacency matrix, 1 bit per cell | adjacency list, $2m$ entries |
|---|---|---|---|---|
| tree | 9999 | 0.0002 | 12.5 MB | 80 KB |
| average degree 20 | 100000 | 0.002 | 12.5 MB | 800 KB |
| half of all pairs | 24997500 | 0.5 | 12.5 MB | 200 MB |

The matrix with one bit per cell takes $n^2/8$ bytes. The list takes $4 \cdot 2m$ bytes, without the $n + 1$ offsets. For the dense graph the matrix is 16 times smaller, and for the tree the list is about 156 times smaller.

**Running times on dense graphs.** With $m = \Theta(n^2)$:

| algorithm | sparse-friendly bound | dense bound | which is better when $m = \Theta(n^2)$ |
|---|---|---|---|
| [Prim](/prim/) or [Dijkstra](/dijkstra/) with a binary heap | $O(m \log n)$ | $O(n^2 \log n)$ | |
| the same with a plain array | $O(n^2)$ | $O(n^2)$ | the array |
| the same with a [Fibonacci heap](/fibonacci-heap/) | $O(m + n \log n)$ | $O(n^2)$ | the array, by a constant factor |
| [BFS](/breadth-first-search/) or [DFS](/depth-first-search/) | $O(n + m)$ | $O(n^2)$ | either representation |
| [Floyd-Warshall](/floyd-warshall/) | $O(n^3)$ | $O(n^3)$ | |

On a dense graph each algorithm that reads all edges needs $\Omega(n^2)$ time, so the array versions are optimal. The binary heap loses a factor $\log n$ there.

## Related definitions

- [Sparse graph](/sparse-graph/): the opposite case.
- [Complete graph](/complete-graph/): the densest graph, with $\rho = 1$.
- [Complement graph](/complement-graph/): the complement of a sparse graph is dense.
- [Adjacency matrix](/adjacency-matrix/) and [bitset adjacency matrix](/bitset-adjacency-matrix/): the representations for dense graphs.
- [Turán's theorem](/turan-theorem/): the largest density of a graph without $K_{r+1}$.

## References
