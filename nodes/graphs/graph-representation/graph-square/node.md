---
tag: 6TQ8YN
kind: definition
slug: graph-square
name: Square of a graph
area: graphs/graph-representation
level: intro
summary: Graph on the same vertices that joins two vertices whenever the original graph has a path of at most two edges between them.
prereqs: [graph, adjacency-matrix]
see_also: [adjacency-matrix, boolean-matrix-multiplication, transitive-closure, matrix-power, graph-coloring, hamiltonian-cycle, line-graph, neighborhood]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Exercise 20.1-5 in Section 20.1 (the square of a directed graph, from adjacency lists and from an adjacency matrix)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: the definition of the k-th power of a graph, in the chapters on Hamiltonian cycles and coloring
  - paper: "Herbert Fleischner, The square of every two-connected graph is Hamiltonian, Journal of Combinatorial Theory, Series B 16, 1974"
    locator: pages 29 to 34, the main theorem
---

The square of a [graph](/graph/) $G$ is the graph $G^2$ on the same vertices in which two distinct vertices are adjacent when their distance in $G$ is 1 or 2. So $G^2$ keeps each [edge](/edge/) of $G$ and adds an edge between each two vertices with a common neighbour. With an [adjacency matrix](/adjacency-matrix/) $A$, the edges of $G^2$ are the nonzero cells of $A + A^2$ off the diagonal, so the square takes one [Boolean matrix product](/boolean-matrix-multiplication/). The square is used for distance-2 coloring, in Fleischner's theorem on Hamiltonian cycles, and as a step of computing distances by repeated squaring.

## Definition

**Undirected.** Let $G = (V, E)$ be a simple undirected graph, with the distance $\operatorname{dist}_G(u, v)$ equal to the least number of edges of a path from $u$ to $v$. Its **square** is

$$G^2 = \big(V,\ \{\{u, v\} : u \ne v,\ \operatorname{dist}_G(u, v) \le 2\}\big).$$

So $\{u, v\} \in E(G^2)$ if and only if $\{u, v\} \in E$, or $u \ne v$ and $N(u) \cap N(v) \ne \emptyset$, where $N(x)$ is the [neighborhood](/neighborhood/) of $x$.

**Directed.** For a directed graph $G = (V, E)$, CLRS defines $G^2 = (V, E^2)$ where $(u, w) \in E^2$ if and only if $G$ has a directed walk of at most two edges from $u$ to $w$, that is, $(u, w) \in E$ or $(u, v), (v, w) \in E$ for some $v$. Under this rule a 2-cycle $(u, v), (v, u)$ gives a loop $(u, u)$ in $G^2$; many authors drop such loops.

**Powers.** More generally, $G^k$ joins $u \ne v$ when $\operatorname{dist}_G(u, v) \le k$. Then $(G^j)^k = G^{jk}$ for undirected graphs, since a path of length at most $jk$ splits into at most $k$ parts of length at most $j$, and conversely. So $G^{2^t}$ is $t$ squarings away from $G$.

**With matrices.** Let $A$ be the adjacency matrix of $G$ over the integers, with a zero diagonal. Then $(A^2)_{uv} = \sum_x A_{ux} A_{xv}$ is the number of walks of length 2 from $u$ to $v$, which for $u \ne v$ is $|N(u) \cap N(v)|$. So

$$\{u, v\} \in E(G^2) \iff u \ne v \text{ and } (A + A^2)_{uv} > 0.$$

In Boolean arithmetic, the matrix of $G^2$ is $A \lor (A \land A)$ with the diagonal cleared, where $A \land A$ is the Boolean product.

## Examples and non-examples

**A worked example.** Let $G$ be the graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$. The square adds the pairs at distance 2:

| new edge | common neighbour |
|---|---|
| $03$ | 1 (and 2) |
| $14$ | 3 |
| $24$ | 3 |
| $35$ | 4 |

So $G^2$ has $7 + 4 = 11$ edges. The pair $\{0, 4\}$ has distance 3, so it is not an edge of $G^2$; it is an edge of $G^3$.

**A directed example.** Let $G$ have the edges $(0,1), (0,2), (1,2), (2,3), (3,1), (3,4)$. The walks of two edges add $(0, 3)$ through 2, $(1, 3)$ through 2, $(2, 1)$ and $(2, 4)$ through 3, and $(3, 2)$ through 1. The walk $0 \to 1 \to 2$ gives $(0, 2)$, which is already an edge. So $G^2$ has $6 + 5 = 11$ edges.

**Paths and cycles.** The square of the path $P_n$ on $0, \ldots, n-1$ has the edges $\{i, i+1\}$ and $\{i, i+2\}$, so $2n - 3$ edges for $n \ge 2$. The square of the cycle $C_5$ is $K_5$, since each two vertices of $C_5$ are at distance at most 2. The square of a star $K_{1, k}$ is $K_{k+1}$.

**Degrees.** Each vertex of $G^2$ has degree at most $d(v) + \sum_{x \in N(v)} (d(x) - 1) \le \Delta^2$, where $\Delta$ is the maximum degree of $G$. So greedy [graph coloring](/graph-coloring/) colors $G^2$ with at most $\Delta^2 + 1$ colors. A proper coloring of $G^2$ is a *distance-2 coloring* of $G$: two vertices at distance 1 or 2 get different colors, as radio transmitters with a common neighbour must.

**Fleischner's theorem.** The square of each 2-connected graph has a [Hamiltonian cycle](/hamiltonian-cycle/). This was proved by Fleischner in 1974.

**The cost of the square.** With $n$ vertices, $m$ edges and degrees $d(v)$:

| input | method | time |
|---|---|---|
| [adjacency list](/adjacency-list/) | for each $u$, mark $N(u)$ and the neighbours of each $x \in N(u)$ | $O(n + \sum_{x} d(x)^2)$ |
| [adjacency matrix](/adjacency-matrix/) | the Boolean product $A^2$ by the naive method | $\Theta(n^3)$ |
| adjacency matrix | fast matrix multiplication over the integers | $O(n^\omega)$, with $\omega < 2.372$ |
| [bitset adjacency matrix](/bitset-adjacency-matrix/) | row $u$ of $G^2$ is the OR of the rows of $N(u)$ | $O((n^2 + nm)/w)$ for $w$-bit words |

The list method works because each pair $(u, x)$ with $x \in N(u)$ is the middle step of $d(x)$ walks, and $\sum_u \sum_{x \in N(u)} d(x) = \sum_x d(x)^2$. For the example above, $\sum_x d(x)^2 = 4 + 9 + 9 + 9 + 4 + 1 = 36$.

**Non-examples.**

- The square is not the [line graph](/line-graph/), whose vertices are the edges of $G$.
- The square is not the Cartesian product $G \square G$, whose vertex set is $V \times V$.
- $G^2$ is not $G$ with each edge doubled: it has the same vertex set, and it is simple.

## Related definitions

- [Adjacency matrix](/adjacency-matrix/) and [Boolean matrix multiplication](/boolean-matrix-multiplication/): the square by one matrix product.
- [Matrix power](/matrix-power/) and [transitive closure](/transitive-closure/): $G^k$ for large $k$, and the limit, which joins each pair with a path.
- [Neighborhood](/neighborhood/): $G^2$ joins the vertices with a common neighbour.
- [Graph coloring](/graph-coloring/): distance-2 coloring is coloring of $G^2$.
- [Hamiltonian cycle](/hamiltonian-cycle/): Fleischner's theorem.

## References
