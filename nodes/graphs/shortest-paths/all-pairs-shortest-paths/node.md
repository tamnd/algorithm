---
tag: 3YR346
kind: problem
slug: all-pairs-shortest-paths
name: All-pairs shortest paths
aliases:
- APSP
area: graphs/shortest-paths
level: core
summary: Compute shortest-path distances between every ordered pair of vertices.
prereqs: [shortest-path, single-source-shortest-paths, adjacency-matrix]
see_also: [floyd-warshall, johnson, apsp-repeated-squaring, slow-apsp-matrix-multiplication, min-plus-matrix-multiplication, apsp-conjecture, distance-oracle, transitive-closure]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 23, All-Pairs Shortest Paths (the problem and the predecessor matrix in the introduction; Sections 23.1 to 23.3)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths
  - paper: doi:10.1137/15M1024524
    title: Ryan Williams, Faster all-pairs shortest paths via circuit complexity, SIAM Journal on Computing 47(5), 1965 to 1985 (2018)
    locator: main theorem, time n^3 / 2^(Ω(sqrt(log n))) for real-weighted APSP
  - paper: doi:10.1145/3186893
    title: Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), article 27 (2018)
    locator: the equivalence of APSP, min-plus product and negative triangle under subcubic reductions
  - paper: doi:10.1006/jcss.1995.1078
    title: Raimund Seidel, On the all-pairs-shortest-path problem in unweighted undirected graphs, Journal of Computer and System Sciences 51(3), 400 to 403 (1995)
    locator: the whole paper, time O(M(n) log n)
  - paper: doi:10.1137/0222071
    title: David R. Karger, Daphne Koller and Steven J. Phillips, Finding the hidden path, time bounds for all-pairs shortest paths, SIAM Journal on Computing 22(6), 1199 to 1217 (1993)
    locator: the Ω(nm) lower bound for path-comparison algorithms
---

The all-pairs shortest-path problem (APSP) asks for the distance $\delta(u, v)$ between every ordered pair of vertices of a weighted graph, or a report that the graph has a [negative cycle](/negative-cycle/). The answer is an $n \times n$ matrix, so every algorithm needs $\Omega(n^2)$ time. The classic methods take $\Theta(n^3)$ time ([Floyd-Warshall](/floyd-warshall/)) or $O(nm + n^2 \log n)$ ([Johnson](/johnson/)), and no algorithm is known that takes $O(n^{3 - \varepsilon})$ time for general weights. That gap is the [APSP conjecture](/apsp-conjecture/) of fine-grained complexity.

## In plain words

A road atlas often has a table at the back: for every two cities, the length of the shortest drive. This problem is to fill in that whole table for a network.

You could solve the one-start problem once for every city. That works, and for sparse networks it is the best way. For dense networks, one method fills the table in three nested loops by allowing more and more cities as stops. Another treats the table like a matrix and "multiplies" it with itself, where adding replaces multiplying and taking the smaller value replaces adding.

If some loop of roads has a negative total, some trips have no shortest version, and the table cannot be filled. Then the task is to report the loop.

## Definition

**Input.** A directed graph $G = (V, E)$ with $V = \{1, \ldots, n\}$, $m = |E|$, and a weight function $w : E \to \mathbb{R}$. An undirected graph is a directed graph with each edge in both directions.

**Output.** If $G$ has no cycle of negative weight, the matrix $D \in (\mathbb{R} \cup \{+\infty\})^{n \times n}$ with

$$D[u][v] = \delta(u, v) = \min\{ w(p) : p \text{ is a path from } u \text{ to } v \},$$

with $D[u][v] = +\infty$ when no path exists and $D[u][u] = 0$. Optionally, a successor matrix $S$ with $S[u][v]$ the vertex after $u$ on a shortest path, or a predecessor matrix $\Pi$ with $\Pi[u][v]$ the vertex before $v$. If $G$ has a negative cycle, the output is a report of one.

**Weight assumptions.** The general problem allows any real weights, negative ones included. Without a negative cycle, each $\delta(u, v)$ is a finite number or $+\infty$, and a shortest path can be taken to be simple. With a negative cycle through a vertex that $u$ reaches and that reaches $v$, $\delta(u, v) = -\infty$; the standard algorithms then report the cycle instead of the matrix. Important special cases assume nonnegative weights, integer weights in $\{-M, \ldots, M\}$, or no weights at all (each edge has length 1).

## Variants

- **Nonnegative weights.** No negative cycle can occur, and [Dijkstra's algorithm](/dijkstra/) from each vertex applies.
- **Small integer weights.** Weights in $\{-M, \ldots, M\}$ allow algorithms based on fast matrix multiplication, with time that grows with $M$.
- **Unweighted graphs.** For undirected graphs, Seidel's algorithm takes $O(M(n) \log n)$, where $M(n)$ is the time to multiply two $n \times n$ integer matrices. For directed graphs the best known bounds are higher.
- **Reachability only.** The Boolean version is the [transitive closure](/transitive-closure/).
- **Paths of a fixed length.** The least weight of a walk with exactly $k$ edges, which is the $k$-th min-plus power of the weight matrix; see [shortest paths of fixed length](/shortest-paths-fixed-length/).
- **Approximate distances.** Allow an answer within a factor $(1 + \varepsilon)$ or a stretch $2k - 1$; this is the setting of [distance oracles](/distance-oracle/), which also limit the space.
- **Dynamic APSP.** Keep the matrix under edge insertions and deletions; see [dynamic all-pairs shortest paths](/dynamic-all-pairs-shortest-paths/).
- **Decision versions.** Is $\delta(u, v) \le k$? Is there a negative triangle? These have the same subcubic complexity as APSP (see Reductions).

## Examples

**A small graph.** Vertices $1, 2, 3, 4$ and edges $1 \to 2$ (4), $2 \to 3$ ($-1$), $1 \to 3$ (5), $3 \to 1$ (2). Vertex 4 has no edges.

| | to 1 | to 2 | to 3 | to 4 |
|---|---|---|---|---|
| from 1 | 0 | 4 | 3 | ∞ |
| from 2 | 1 | 0 | −1 | ∞ |
| from 3 | 2 | 6 | 0 | ∞ |
| from 4 | ∞ | ∞ | ∞ | 0 |

The entry $D[1][3] = 3$ comes from $1 \to 2 \to 3$, not from the direct edge of weight 5. The entry $D[2][1] = 1$ is $2 \to 3 \to 1$. The cycle $1 \to 2 \to 3 \to 1$ has weight $4 - 1 + 2 = 5 \ge 0$, so there is no negative cycle. The successor of 1 toward 3 is 2.

**A negative cycle.** Vertices $1, 2, 3$ and edges $1 \to 2$ (4), $2 \to 3$ ($-1$), $3 \to 2$ ($-4$). The cycle $2 \to 3 \to 2$ has weight $-5$. So $\delta(1, 2) = \delta(1, 3) = \delta(2, 2) = -\infty$, and the right output is a report of the cycle. Floyd-Warshall ends with $D[2][2] = -5$ and $D[3][3] = -10$, negative entries on the diagonal.

**A non-example.** A matrix with $D[u][u] = 0$ for all $u$ and $D[u][v] \le D[u][x] + D[x][v]$ for all $u, x, v$ is a valid distance matrix for some graph (take each entry as an edge weight). But it is not the answer for a given graph unless each finite $D[u][v]$ is the weight of an actual path of that graph and $D[u][v] \le w(u, v)$ for each edge.

## Known algorithms

| algorithm | weights | time |
|---|---|---|
| [Floyd-Warshall](/floyd-warshall/) | real, detects negative cycles | $\Theta(n^3)$ |
| [Slow matrix-multiplication method](/slow-apsp-matrix-multiplication/) | real, no negative cycle | $\Theta(n^4)$ |
| [Repeated squaring](/apsp-repeated-squaring/) | real, no negative cycle | $\Theta(n^3 \log n)$ |
| [Dijkstra](/dijkstra/) from each vertex | nonnegative | $O(nm + n^2 \log n)$ with a Fibonacci heap |
| [Bellman-Ford](/bellman-ford/) from each vertex | real | $O(n^2 m)$ |
| [Johnson's algorithm](/johnson/) | real, detects negative cycles | $O(nm + n^2 \log n)$ |
| [BFS](/breadth-first-search/) from each vertex | unweighted | $O(nm)$ |
| Seidel's algorithm | unweighted, undirected | $O(M(n) \log n)$ |
| Williams' algorithm | real | $n^3 / 2^{\Omega(\sqrt{\log n})}$ |

Johnson's algorithm is the standard choice for sparse graphs, Floyd-Warshall for dense graphs. On a DAG with any weights, [DAG shortest paths](/dag-shortest-paths/) from each vertex takes $O(n(n + m))$.

## Bounds

- **Output size.** Each of the $n^2$ entries must be written, so $\Omega(n^2)$ time is needed in every model.
- **Upper bound for dense real weights.** Williams (2014, journal version 2018) gives $n^3 / 2^{\Omega(\sqrt{\log n})}$ on the word RAM. This is faster than $n^3 / \log^c n$ for every constant $c$, but not $O(n^{3 - \varepsilon})$ for any $\varepsilon > 0$.
- **Sparse graphs.** With nonnegative weights, $O(nm + n^2 \log n)$ follows from $n$ runs of Dijkstra with a Fibonacci heap; Johnson's reweighting extends it to negative weights.
- **Path-comparison lower bound.** Karger, Koller and Phillips (1993) show that an algorithm that only compares the weights of paths needs $\Omega(nm)$ comparisons on some graphs. Dijkstra from each vertex is optimal in that model up to the $n^2 \log n$ term.
- **The APSP conjecture.** No algorithm is known that solves APSP with integer weights in $\{-n^c, \ldots, n^c\}$ in $O(n^{3 - \varepsilon})$ time for some $\varepsilon > 0$, and the [APSP conjecture](/apsp-conjecture/) states that none exists. Many problems are known to be equivalent to it (see Reductions).

## Reductions

- **APSP and min-plus product.** Define $(A \star B)[i][j] = \min_k (A[i][k] + B[k][j])$, the [min-plus product](/min-plus-matrix-multiplication/). With $W$ the weight matrix (with 0 on the diagonal), $W^{\star (n-1)}$ is the distance matrix when no negative cycle exists, so APSP takes $O(\log n)$ products by [repeated squaring](/apsp-repeated-squaring/). Conversely, a min-plus product of two $n \times n$ matrices is an APSP instance on a graph with three layers of $n$ vertices. So the two problems have the same time up to a factor $O(\log n)$, and with more care up to a constant factor.
- **Negative triangle.** Vassilevska Williams and Williams show that APSP has an $O(n^{3 - \varepsilon})$ algorithm if and only if deciding whether a weighted graph has a triangle of negative weight has one. The same holds for several other problems, among them the [minimum-weight cycle](/shortest-cycle-problem/), replacement paths and the second-shortest simple path.
- **From SSSP.** APSP reduces to $n$ instances of [single-source shortest paths](/single-source-shortest-paths/). After one Bellman-Ford run, [reduced costs](/potential-function-reduced-costs/) make all weights nonnegative, so all $n$ instances can use Dijkstra.
- **Transitive closure.** Reachability is APSP over the Boolean semiring; it reduces to Boolean matrix multiplication, which is faster than the min-plus product with current methods.

## Applications

- **Routing tables.** A network with a fixed topology can precompute the next hop for every pair of nodes from the successor matrix.
- **Graph measures.** The diameter, the radius, the [eccentricity](/eccentricity/) of each vertex and closeness centrality are read off the distance matrix.
- **Distance matrices for other algorithms.** Clustering, [multidimensional scaling](/multidimensional-scaling/) of graphs, and the metric closure used in [TSP approximation](/mst-tsp-heuristic/) and Steiner tree heuristics all start from APSP.
- **Difference constraints and timing.** A system of [difference constraints](/difference-constraints/) gives the tightest bounds between every two variables after APSP on its constraint graph, as in the analysis of timing in circuits and of time intervals in planning.

## References
