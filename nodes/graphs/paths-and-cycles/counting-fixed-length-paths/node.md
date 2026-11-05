---
tag: C7G2BQ
kind: problem
slug: counting-fixed-length-paths
name: Number of paths of fixed length
aliases:
- counting walks of length k
area: graphs/paths-and-cycles
level: core
summary: Problem of counting walks with exactly k edges between vertices, solved by the k-th power of the adjacency matrix; counting simple paths of length k is #P-hard.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of edges of a walk, ω: the matrix multiplication exponent, counted in arithmetic operations on the walk counts}
  time: {worst: O(n^ω log k)}
prereqs: [adjacency-matrix, matrix-exponentiation, counting-problem]
see_also: [apsp-repeated-squaring, cayley-hamilton-theorem, linear-recurrence-nth-term, triangle-counting, k-path-color-coding, enumerating-simple-paths, parameterized-counting-complexity, counting-lattice-paths]
sources:
  - book: isbn:9780521458979
    title: Norman Biggs, Algebraic Graph Theory, second edition, Cambridge University Press (1993)
    locator: Chapter 2, The spectrum of a graph (walks counted by the powers of the adjacency matrix, and closed walks by the eigenvalues)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Section 1.5 and its exercises on the adjacency matrix and walks
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 410 to 421 (1979)
    locator: the whole paper (counting s-t paths in a graph is #P-complete)
  - paper: doi:10.1137/S0097539703427203
    title: Jörg Flum and Martin Grohe, The parameterized complexity of counting problems, SIAM Journal on Computing 33(4), 892 to 922 (2004)
    locator: the whole paper (counting paths and cycles of length k is #W[1]-complete)
  - paper: doi:10.1007/BF02523189
    title: Noga Alon, Raphael Yuster and Uri Zwick, Finding and counting given length cycles, Algorithmica 17(3), 209 to 223 (1997)
    locator: the whole paper (counting cycles of length at most 7 with matrix products)
---

The problem asks for the number of walks with exactly $k$ edges from a vertex $u$ to a vertex $v$ in a [graph](/graph/), for one pair or for all pairs. The answer is the entry $(A^k)_{uv}$ of the $k$-th power of the [adjacency matrix](/adjacency-matrix/), so [matrix exponentiation](/matrix-exponentiation/) solves it with $O(\log k)$ matrix products, and a simple dynamic program solves it for one source in $O(k(n + m))$ operations. A walk may repeat vertices; counting *simple* paths of length $k$ is a much harder problem, which is #P-hard when $k$ is part of the input.

## In plain words

In a road map, how many routes of exactly $k$ steps go from one town to another, if a route may pass the same town twice? Count them step by step. After one step, the number of routes to each town is the number of roads from the start to it. To reach a town in $j + 1$ steps, you must reach one of its neighbours in $j$ steps, so add up the counts of the neighbours. Repeat $k$ times.

Writing the roads as a table of numbers turns each step into a multiplication of tables, and multiplying a table by itself again and again reaches large $k$ fast. The question becomes hard if a route may not pass any town twice: then the past of a route matters, not only where it is now.

## Definition

**Input.** A graph $G$ with vertices $1, \ldots, n$, directed or undirected, given by its adjacency matrix $A$, where $A_{uv}$ is the number of edges from $u$ to $v$. In a [multigraph](/multigraph/), $A_{uv}$ counts the parallel edges. A [self-loop](/self-loop/) at $u$ adds 1 to $A_{uu}$, because a walk can use it as one step; this differs from the degree convention, where a loop adds 2. In an undirected graph $A$ is symmetric. Also given: an integer $k \ge 0$, and optionally a pair $u, v$.

**Output.** $W_k(u, v)$, the number of walks $u = x_0, e_1, x_1, \ldots, e_k, x_k = v$ with $k$ edges, where each $e_i$ is an edge from $x_{i-1}$ to $x_i$. Two walks are different if their edge sequences differ, so in a multigraph parallel edges give different walks.

**Theorem.** $W_k(u, v) = (A^k)_{uv}$ for all $k \ge 0$.

*Proof.* By induction on $k$. For $k = 0$ the only walk is the empty walk from $u$ to $u$, and $A^0 = I$. A walk with $k + 1$ edges from $u$ to $v$ is a walk with $k$ edges from $u$ to some $x$, followed by one of the $A_{xv}$ edges from $x$ to $v$. So $W_{k+1}(u, v) = \sum_x W_k(u, x) A_{xv} = \sum_x (A^k)_{ux} A_{xv} = (A^{k+1})_{uv}$. $\square$

## Variants

- **One source, all lengths up to $k$.** Keep the row vector $w_j = e_u^{\top} A^j$ and update $w_{j+1}(v) = \sum_{(x, v) \in E} w_j(x)$. This is a [dynamic program over the layers](/dag-dynamic-programming/) of the time-expanded graph.
- **Walks of length at most $k$.** Sum the powers, or add a loop at a new absorbing vertex; the generating function is $\sum_{k \ge 0} A^k z^k = (I - zA)^{-1}$.
- **Closed walks.** The number of closed walks of length $k$ is $\mathrm{tr}(A^k) = \sum_i \lambda_i^k$, where the $\lambda_i$ are the eigenvalues of $A$.
- **Cycles of length $k$.** For undirected simple graphs, the number of triangles is $\mathrm{tr}(A^3)/6$ and the number of 4-cycles is $(\mathrm{tr}(A^4) - 2 \sum_v d(v)^2 + 2m)/8$. Alon, Yuster and Zwick give such matrix formulas for cycles of length up to 7. For general $k$, see the hardness below; for $k = 3$, see [triangle counting](/triangle-counting/).
- **Simple paths of length $k$.** Count walks that never repeat a vertex. This is the hard version; see [enumerating simple paths](/enumerating-simple-paths/) for listing them.
- **Counting modulo $p$ or with weights.** The same algebra works over any semiring; with the (min, +) semiring it gives shortest walks with $k$ edges, the base of [repeated squaring for all-pairs shortest paths](/apsp-repeated-squaring/).

## Examples

**The diamond.** The undirected graph with vertices $0, 1, 2, 3$ and edges $01, 12, 23, 30, 02$ (a 4-cycle with the chord $02$) has

$$A = \begin{pmatrix} 0 & 1 & 1 & 1 \\ 1 & 0 & 1 & 0 \\ 1 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \end{pmatrix}, \quad A^2 = \begin{pmatrix} 3 & 1 & 2 & 1 \\ 1 & 2 & 1 & 2 \\ 2 & 1 & 3 & 1 \\ 1 & 2 & 1 & 2 \end{pmatrix}, \quad A^3 = \begin{pmatrix} 4 & 5 & 5 & 5 \\ 5 & 2 & 5 & 2 \\ 5 & 5 & 4 & 5 \\ 5 & 2 & 5 & 2 \end{pmatrix}.$$

$(A^3)_{01} = 5$: the walks are $0, 1, 0, 1$; $0, 2, 0, 1$; $0, 3, 0, 1$; $0, 1, 2, 1$; and $0, 3, 2, 1$. Only the last one is a simple path. $\mathrm{tr}(A^3) = 12$, so the graph has $12 / 6 = 2$ triangles, $\{0, 1, 2\}$ and $\{0, 2, 3\}$. $(A^2)_{00} = 3$ is the degree of 0.

**Complete graphs.** In $K_n$, $A = J - I$, where $J$ is the all-ones matrix. Since $J^2 = nJ$, the powers are $A^k = \frac{(n-1)^k - (-1)^k}{n} J + (-1)^k I$. So two distinct vertices are joined by $((n-1)^k - (-1)^k)/n$ walks of length $k$, and each vertex has $((n-1)^k + (n-1)(-1)^k)/n$ closed walks of length $k$. For $K_4$ and $k = 3$ these are 7 and 6. The number of simple paths with $k$ edges between two distinct vertices of $K_n$ is $(n-2)!/(n-1-k)!$, which is 2 for $K_4$ and $k = 3$.

**Directed graph and loops.** In the directed graph with the arcs $0 \to 1$, $1 \to 0$ and a loop at 1, $A = \begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$, and $(A^k)_{00}$ is a Fibonacci number: $1, 0, 1, 1, 2, 3, 5, \ldots$ for $k = 0, 1, 2, \ldots$.

**No walk.** For an isolated vertex, or for $u$ and $v$ in different components, every $W_k(u, v)$ with $u \ne v$ is 0. In an acyclic directed graph, $A^n = 0$, since no walk has $n$ or more edges.

## Known algorithms

| method | output | cost |
|---|---|---|
| repeated vector update | $W_j(u, \cdot)$ for $j \le k$ | $O(k(n + m))$ operations |
| [matrix exponentiation](/matrix-exponentiation/) by squaring | all $W_k(u, v)$ | $O(n^{\omega} \log k)$ operations |
| [Cayley-Hamilton](/cayley-hamilton-theorem/) and a [linear recurrence](/linear-recurrence-nth-term/) | $W_k(u, v)$ for one pair | $O(n(n + m))$ to find the recurrence, then $O(n^2 \log k)$, or less with fast polynomial arithmetic |
| eigenvalues | $\mathrm{tr}(A^k)$ | one eigendecomposition, then $O(n)$ per $k$ (floating point) |

The sequence $W_k(u, v)$ satisfies a linear recurrence of order at most $n$, given by the characteristic polynomial of $A$. The [Berlekamp-Massey algorithm](/berlekamp-massey/) recovers it from $2n$ terms, and the [Bostan-Mori algorithm](/bostan-mori-algorithm/) then gives the $k$-th term.

## Bounds

**Size of the numbers.** $W_k(u, v) \le \Delta^k$, where $\Delta$ is the largest out-degree counted with multiplicity, so the answer has up to $k \log_2 \Delta$ bits. For large $k$ the exact answer has $\Theta(k)$ bits in most graphs, and the cost in bit operations grows with $k$ also for the logarithmic method. In practice one counts modulo a prime.

**Matrix powers.** Computing $A^k$ for all pairs is at least as hard as one matrix product of 0-1 matrices up to the size of the numbers, and with $\omega < 2.372$ (see [the matrix multiplication exponent](/matrix-multiplication-exponent/)) the method takes $O(n^{2.372} \log k)$ operations.

**Simple paths.** Valiant (1979) proved that counting all simple $s$-$t$ paths in a graph is #P-complete, directed or undirected. Counting simple paths with exactly $k = n - 1$ edges counts Hamiltonian paths, so the fixed-length version is #P-hard when $k$ is part of the input. Flum and Grohe (2004) proved that counting paths, and cycles, of length $k$ is #W[1]-complete with parameter $k$, so an algorithm with time $f(k) \cdot n^{O(1)}$ is not expected (see [parameterized counting complexity](/parameterized-counting-complexity/)). Deciding whether a simple path of length $k$ exists is, by contrast, fixed-parameter tractable by [color coding](/k-path-color-coding/).

## Reductions

- **Walks to matrix powers.** The theorem above; any fast matrix multiplication gives a fast walk counter.
- **Triangles to walks.** Triangle counting reduces to the diagonal of $A^3$; this is the $O(n^{\omega})$ triangle algorithm.
- **Hamiltonian paths to simple paths of length $k$.** Take $k = n - 1$; the count is positive if and only if a Hamiltonian path exists.
- **Hamiltonian paths by inclusion and exclusion.** A walk with $n - 1$ edges that meets every vertex is a Hamiltonian path, so the number of Hamiltonian paths is $\sum_{S \subseteq V} (-1)^{|S|} \cdot (\text{number of walks with } n - 1 \text{ edges in } G - S)$. Each term is a walk count, which gives an exact algorithm with $O(2^n \cdot \mathrm{poly}(n))$ time and polynomial space. Applied to each set of $k + 1$ vertices, the same sum counts simple paths with $k$ edges.

## Applications

- **Network analysis.** Walk counts are the base of Katz centrality, $\sum_k \beta^k A^k$, and of the communicability of two vertices.
- **Combinatorics on words.** The number of words of length $k$ accepted by a finite automaton, or of strings avoiding a pattern, is a walk count in the transition graph; the graph of the Fibonacci example above is the automaton of binary strings with no two consecutive 0s.
- **Markov chains.** With transition probabilities in place of 0 and 1, $A^k$ gives the $k$-step transition probabilities.
- **Lattice paths.** Grid walks with fixed steps are walk counts in an infinite graph; see [counting lattice paths](/counting-lattice-paths/).

## References
