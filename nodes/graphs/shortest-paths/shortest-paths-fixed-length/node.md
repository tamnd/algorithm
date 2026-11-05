---
tag: VGF0WD
kind: problem
slug: shortest-paths-fixed-length
name: Shortest paths of fixed length
aliases:
- shortest walks with exactly k edges
- exact-hop shortest paths
area: graphs/shortest-paths
level: core
summary: Problem of finding shortest walks using exactly k edges between vertices, solved by min-plus matrix exponentiation of the weight matrix.
prereqs: [shortest-path, all-pairs-shortest-paths, slow-apsp-matrix-multiplication]
see_also: [slow-apsp-matrix-multiplication, apsp-repeated-squaring, min-plus-matrix-multiplication, matrix-exponentiation, karp-minimum-mean-cycle, color-coding, bellman-ford, apsp-conjecture]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (the min-plus product, the matrices L^(r) and repeated squaring)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths (the dynamic program indexed by the number of edges)
  - paper: doi:10.1016/0012-365X(78)90011-0
    title: Richard M. Karp, A characterization of the minimum cycle mean in a digraph, Discrete Mathematics 23(3), 309 to 311 (1978)
    locator: the values D_k(v), least weights of walks with exactly k edges from a source
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the algorithms for simple paths of a given length k
  - paper: doi:10.1145/3186893
    title: Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), article 27 (2018)
    locator: the equivalence of all-pairs shortest paths and the min-plus product under subcubic reductions
---

The problem of shortest paths of fixed length asks, for a weighted directed graph and an integer $k \ge 0$, for the least weight of a walk with exactly $k$ arcs between given vertices. In matrix form, the answer for all pairs is the $k$-th power of the weight matrix in the [min-plus algebra](/min-plus-matrix-multiplication/), which [repeated squaring](/apsp-repeated-squaring/) computes with $O(\log k)$ products. A single source takes $O(km)$ time by dynamic programming. The answer concerns walks, which may repeat vertices; the same question for simple paths is NP-hard.

## In plain words

You must make a trip with exactly a given number of roads, no more and no less, and you want the cheapest such trip between two places. You may pass the same place more than once.

One way: for each place, keep the cheapest cost to reach it with exactly one road, then exactly two roads, and so on. The cheapest trip with one more road is a cheapest trip to some place just before, plus the last road. For all pairs of places at once, the same step is a kind of table product, and a large count of roads needs only a few such products if you double the count each time.

Loops of roads with a negative total are no problem here, because the number of roads is fixed.

## Definition

Let $G = (V, E)$ be a directed graph with $n$ vertices, $m$ arcs and weights $w : E \to \mathbb{R}$, and let $k \ge 0$ be an integer. For $u, v \in V$,

$$\delta_k(u, v) = \min \{ w(p) : p \text{ is a walk from } u \text{ to } v \text{ with exactly } k \text{ arcs} \},$$

with $\delta_k(u, v) = \infty$ if there is no such walk and $\delta_0(u, u) = 0$. A walk may repeat vertices and arcs. There are finitely many walks with $k$ arcs, so the minimum exists and $\delta_k$ is always a real number or $\infty$.

**Weight assumptions.** Any real weights. Negative cycles are allowed and do not make any value $-\infty$, because the number of arcs is fixed. Unreachable pairs, and pairs joined only by walks of other lengths, have the value $\infty$. Integer weights are not needed, but the bounds for fast algorithms below use them.

**Matrix form.** Let $A$ be the matrix with $A[u][v]$ the least weight of an arc $u \to v$ (a self-loop counts as an arc), and $\infty$ if there is none; unlike the matrix $W$ of [SLOW-APSP](/slow-apsp-matrix-multiplication/), the diagonal is not set to 0. With the min-plus product $(X \otimes Y)[u][v] = \min_x (X[u][x] + Y[x][v])$, the matrix of $\delta_k$ is $A^{\otimes k}$, and $A^{\otimes 0}$ is the min-plus identity, with 0 on the diagonal and $\infty$ elsewhere.

## Variants

- **Single pair or single source.** Compute $\delta_k(s, \cdot)$ for one source $s$.
- **At most $k$ arcs.** The least weight of a walk with at most $k$ arcs, the hop-constrained problem. It is $\min_{j \le k} \delta_j$, and it is the power $W^{\otimes k}$ of the matrix with 0 on the diagonal. With no negative cycle, at most $n - 1$ arcs gives the ordinary distance.
- **Simple paths of length $k$.** Ask for a path with no repeated vertex and exactly $k$ arcs. For $k = n - 1$ this asks for a Hamiltonian path, so it is NP-hard. See [color coding](/color-coding/).
- **Exactly $k$ arcs, maximum weight.** Use the max-plus product. For walks, this is the same problem with negated weights.
- **Other products.** Over the Boolean semiring, the power tells whether a walk of exactly $k$ arcs exists; over ordinary arithmetic, it counts walks of length $k$.

## Examples

Take the graph of CLRS Figure 23.1, with the vertices 1 to 5 and the arcs $1 \to 2$ (3), $1 \to 3$ (8), $1 \to 5$ ($-4$), $2 \to 4$ (1), $2 \to 5$ (7), $3 \to 2$ (4), $4 \to 1$ (2), $4 \to 3$ ($-5$) and $5 \to 4$ (6). The values $\delta_k(1, \cdot)$ for the targets 1 to 5 are:

| $k$ | $\delta_k(1, 1)$ | $\delta_k(1, 2)$ | $\delta_k(1, 3)$ | $\delta_k(1, 4)$ | $\delta_k(1, 5)$ |
|---|---|---|---|---|---|
| 0 | 0 | $\infty$ | $\infty$ | $\infty$ | $\infty$ |
| 1 | $\infty$ | 3 | 8 | $\infty$ | $-4$ |
| 2 | $\infty$ | 12 | $\infty$ | 2 | 10 |
| 3 | 4 | $\infty$ | $-3$ | 13 | 19 |
| 4 | 15 | 1 | 8 | 25 | 0 |

For example $\delta_2(1, 4) = 2$ by $1 \to 5 \to 4$, and $\delta_4(1, 2) = 1$ by $1 \to 5 \to 4 \to 3 \to 2$. The value $\delta_4(1, 5) = 0$ is the walk $1 \to 5 \to 4 \to 1 \to 5$, which visits 1 and 5 twice. The ordinary distance $\delta(1, 5) = -4$ is the minimum over all $k$; for a fixed $k$ the value can be larger, or $\infty$, as $\delta_2(1, 1)$ is.

**With a negative cycle.** Add the arc $3 \to 4$ of weight 4, so that $3 \to 4 \to 3$ has weight $-1$. The ordinary distance $\delta(3, 3)$ is $-\infty$, but $\delta_k(3, 3)$ is finite for every $k$: it is $\infty$ for $k = 1$ and $-1$, 0, $-2$, $-1$, $-3$ for $k = 2, \ldots, 6$. Each two more arcs can add one more turn around the cycle.

**Walks, not paths.** In the graph with the arcs $a \to b$ (1), $b \to a$ (1) and $a \to c$ (10), $\delta_3(a, c) = 12$ by $a \to b \to a \to c$, but no simple path from $a$ to $c$ has 3 arcs.

## Known algorithms

| algorithm | output | time |
|---|---|---|
| dynamic program on $k$ (Bellman-Ford rounds with a copy) | $\delta_k(s, \cdot)$ | $O(k(n + m))$ |
| $k - 1$ min-plus products ([SLOW-APSP](/slow-apsp-matrix-multiplication/) without the zero diagonal) | all pairs | $O(k n^3)$ |
| [repeated squaring](/apsp-repeated-squaring/) ([matrix exponentiation](/matrix-exponentiation/) by the bits of $k$) | all pairs | $O(n^3 \log k)$ |
| fast min-plus product for integer weights in $[-M, M]$ | all pairs | $\tilde O(M n^{\omega} \log k)$ |
| [color coding](/color-coding/), simple paths | one pair | $2^{O(k)} m$ expected |

The single-source dynamic program starts with $d_0(s) = 0$ and $d_0(v) = \infty$ for $v \ne s$, and sets $d_j(v) = \min_{(u, v) \in E} (d_{j-1}(u) + w(u, v))$. It must use a fresh array for $d_j$; updating in place, as Bellman-Ford does, mixes walks of different lengths.

## Bounds

- **Lower bound for one source.** Every arc can be on a best walk, so $\Omega(n + m)$ time is needed to read the input.
- **All pairs.** One product, $k = 2$, is already a min-plus product of two arbitrary matrices, since any $n \times n$ matrices $X, Y$ can be put on a three-layer graph. So the all-pairs problem is as hard as the min-plus product, which is equivalent to [all-pairs shortest paths](/all-pairs-shortest-paths/) under subcubic reductions (Vassilevska Williams and Williams). By the [APSP conjecture](/apsp-conjecture/), no $O(n^{3 - \varepsilon})$ algorithm exists for real or large integer weights.
- **Simple paths.** NP-hard for $k$ part of the input, by the reduction from the Hamiltonian path problem. With color coding it is fixed-parameter tractable in $k$.

## Reductions

- **From the min-plus product.** Given $X$ and $Y$, build the vertices $a_i$, $b_j$, $c_l$ with the arcs $a_i \to b_j$ of weight $X[i][j]$ and $b_j \to c_l$ of weight $Y[j][l]$. Then $\delta_2(a_i, c_l) = (X \otimes Y)[i][l]$.
- **To hop-constrained shortest paths.** Add a self-loop of weight 0 at every vertex; then exactly $k$ arcs in the new graph is at most $k$ arcs in the old graph.
- **From hop-constrained to exact, by layers.** Make $k + 1$ copies $V_0, \ldots, V_k$ of the vertex set and an arc from $u$ in $V_{j-1}$ to $v$ in $V_j$ for each arc $(u, v)$. The new graph is acyclic, and $\delta_k(s, v)$ is the ordinary distance from $s$ in $V_0$ to $v$ in $V_k$, computed by [DAG shortest paths](/dag-shortest-paths/) in $O(k(n + m))$ time. This is the dynamic program above.

## Applications

- **Minimum mean cycle.** [Karp's algorithm](/karp-minimum-mean-cycle/) computes $D_k(v) = \delta_k(s, v)$ for $k = 0, \ldots, n$ from an added source and gets the least mean weight of a cycle as $\min_v \max_{k < n} \frac{D_n(v) - D_k(v)}{n - k}$.
- **Hop-limited routing.** In networks where each hop costs delay or reliability, routes may be limited to $k$ links.
- **Markov chains and most likely paths.** With weights $-\log P(u, v)$, $\delta_k$ gives the most likely sequence of $k$ steps of a [Markov chain](/markov-chain/) between two states, the max-product form of a Viterbi computation.
- **Counting and existence.** The Boolean and counting versions of the same powers decide whether walks of length $k$ exist and count them.

## References
