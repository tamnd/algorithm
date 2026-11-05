---
tag: TRREJZ
kind: algorithm
slug: apsp-repeated-squaring
name: All-pairs shortest paths by repeated squaring
aliases:
- Faster all-pairs shortest paths by repeated squaring
area: graphs/shortest-paths
level: core
summary: Speeds up min-plus matrix multiplication for all-pairs shortest paths by squaring the weight matrix, needing only a logarithmic number of products.
solves: [all-pairs-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n^3 log n), best: Θ(n^3 log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [slow-apsp-matrix-multiplication, min-plus-matrix-multiplication, binary-exponentiation]
see_also: [all-pairs-shortest-paths, floyd-warshall, johnson, shortest-paths-fixed-length, transitive-closure, apsp-conjecture, kleene-algebra, matrix-multiplication-exponent]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (EXTEND-SHORTEST-PATHS, SLOW-APSP and FASTER-APSP)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths (the sections on the funny matrix multiplication and on repeated squaring)
  - paper: doi:10.1137/0205006
    title: Michael L. Fredman, New bounds on the complexity of the shortest path problem, SIAM Journal on Computing 5(1), 83 to 89 (1976)
    locator: the whole paper (a min-plus product in o(n^3) time, and so APSP in o(n^3) time)
  - paper: doi:10.1145/567112.567114
    title: Uri Zwick, All pairs shortest paths using bridging sets and rectangular matrix multiplication, Journal of the ACM 49(3), 289 to 317 (2002)
    locator: the whole paper (APSP with small integer weights from fast matrix products)
  - paper: doi:10.1137/15M1024524
    title: Ryan Williams, Faster all-pairs shortest paths via circuit complexity, SIAM Journal on Computing 47(5), 1965 to 1985 (2018)
    locator: main theorem, a min-plus product in n^3 / 2^(Ω(sqrt(log n))) time
---

All-pairs shortest paths by repeated squaring computes every distance of a weighted directed graph by squaring its weight matrix in the [min-plus product](/min-plus-matrix-multiplication/), where "plus" takes the place of "times" and "min" takes the place of "plus". After $j$ squarings the matrix holds the least weight of a walk with at most $2^j$ edges, so $\lceil \log_2 n \rceil$ products of $\Theta(n^3)$ time each are enough. The total is $\Theta(n^3 \log n)$, a factor $n / \log n$ better than the [slow method](/slow-apsp-matrix-multiplication/) that adds one edge per product, and the diagonal of the last matrix reveals any [negative cycle](/negative-cycle/).

## In plain words

Start with a table that says, for every two places, the cheapest way to go between them using at most one road. Combine the table with itself: to go from one place to another with at most two roads, try every middle stop and keep the cheapest. Now the table covers trips of up to two roads.

Combine the new table with itself, and it covers up to four roads. Then eight, then sixteen. The number of roads doubles each time, so after a few rounds it covers every trip that does not visit a place twice.

At the end, look at the cost from each place back to itself. If one is below zero, some loop of roads has a negative total, and there are no true shortest trips.

## The problem

The input is a directed graph on the vertices $1, \ldots, n$ with a real weight $w(u, v)$ on each edge. The output is the matrix of distances $\delta(u, v)$ of the [all-pairs shortest-path problem](/all-pairs-shortest-paths/), with $+\infty$ when $v$ cannot be reached from $u$, or a report that the graph has a negative cycle.

**Weight assumptions.** Weights are any real numbers; negative weights are allowed and need not be integers. Parallel edges and self-loops are allowed. If the graph has no cycle of negative weight, the algorithm returns the distances. If it has one, the algorithm reports it. CLRS's FASTER-ALL-PAIRS-SHORTEST-PATHS assumes there is no negative cycle and stops one step sooner; the version below squares until it covers walks of $n$ edges, which is what the check needs.

## The algorithm

Write $L^{(k)}[i][j]$ for the least weight of a walk from $i$ to $j$ with at most $k$ edges. Then $L^{(1)}$ is the weight matrix with $\min(0, \text{self-loop})$ on the diagonal, and $L^{(2k)} = L^{(k)} \star L^{(k)}$, where $(A \star B)[i][j] = \min_t (A[i][t] + B[t][j])$.

```pseudo id=main
APSP-REPEATED-SQUARING(G, w)
L1  L ← n × n matrix with L[i][i] ← 0 and L[i][j] ← ∞ for i ≠ j
L2  for each edge (u, v) do L[u][v] ← min(L[u][v], w(u, v))
L3  k ← 1                                  ▷ L = L^(k)
L4  while k < n do
L5      M ← a copy of L                    ▷ the term t = i, since L[i][i] ≤ 0
L6      for each i and each t with L[i][t] ≠ ∞ do
L7          for each j do M[i][j] ← min(M[i][j], L[i][t] + L[t][j])
L8      L ← M, k ← 2k                      ▷ M = L^(k) ⋆ L^(k) = L^(2k)
L9  if L[i][i] < 0 for some i then return NEGATIVE-CYCLE
L10 return L
```

Lines L5 to L7 compute one min-plus square. Starting $M$ as a copy of $L$ is the term $t = i$ of the minimum when $L[i][i] = 0$, and it can only make $M$ larger than the true product when $L[i][i] < 0$, in which case line L9 rejects the input anyway (see Correctness). The loop ends with $k$ the least power of two with $k \ge n$.

## Example

The graph has the vertices $1, 2, 3, 4$ and the edges $1 \to 2$ (3), $1 \to 3$ (8), $2 \to 4$ (1), $2 \to 3$ (4), $3 \to 2$ ($-2$), $4 \to 1$ (2), $4 \to 3$ (2), the same graph as on the [Floyd-Warshall](/floyd-warshall/) page. Rows are sources, columns are targets.

$$L^{(1)} = \begin{pmatrix} 0 & 3 & 8 & \infty \\ \infty & 0 & 4 & 1 \\ \infty & -2 & 0 & \infty \\ 2 & \infty & 2 & 0 \end{pmatrix}, \quad L^{(2)} = \begin{pmatrix} 0 & 3 & 7 & 4 \\ 3 & 0 & 3 & 1 \\ \infty & -2 & 0 & -1 \\ 2 & 0 & 2 & 0 \end{pmatrix}, \quad L^{(4)} = \begin{pmatrix} 0 & 3 & 6 & 4 \\ 3 & 0 & 3 & 1 \\ 1 & -2 & 0 & -1 \\ 2 & 0 & 2 & 0 \end{pmatrix}.$$

In $L^{(2)}$, the entry $[1][3]$ drops from 8 to 7 by the walk $1 \to 2 \to 3$, and $[4][2] = 0$ by $4 \to 3 \to 2$. The entry $[3][1]$ is still $\infty$: every walk from 3 to 1 needs at least three edges, $3 \to 2 \to 4 \to 1$, of weight $-2 + 1 + 2 = 1$, which appears in $L^{(4)}$. The entry $[1][3]$ becomes $6$ by $1 \to 2 \to 4 \to 3$. Two squarings are done, since $k = 4 \ge n = 4$. The diagonal of $L^{(4)}$ is zero, so there is no negative cycle, and $L^{(4)}$ equals the Floyd-Warshall result.

**A negative cycle.** With $n = 2$ and the edges $1 \to 2$ (1) and $2 \to 1$ ($-2$), $L^{(1)}$ has a zero diagonal. One squaring gives $L^{(2)}[1][1] = 1 - 2 = -1$, and line L9 reports the cycle. A version that stops when $k \ge n - 1 = 1$ would do no squaring and miss it.

## Correctness

**Lemma 1.** After lines L1 and L2, $L = L^{(1)}$, and $L^{(1)}[i][i] \le 0$.

**Lemma 2.** If $A = L^{(a)}$ and $B = L^{(b)}$, then $A \star B = L^{(a + b)}$. A walk from $i$ to $j$ with at most $a + b$ edges splits at the vertex $t$ reached after $\min(a, \text{its length})$ edges into a walk with at most $a$ edges and one with at most $b$ edges, so $L^{(a + b)} \ge A \star B$. Conversely, joining a walk $i \leadsto t$ with at most $a$ edges and a walk $t \leadsto j$ with at most $b$ edges gives a walk with at most $a + b$ edges, so $A \star B \ge L^{(a + b)}$.

**Lemma 3.** Line L5 does not change the result. The true product has $M[i][j] \le L[i][i] + L[i][j] \le L[i][j]$, so the term $t = i$ already makes the minimum at most the copied value; taking the minimum with the copy changes nothing.

So after the loop, $L = L^{(k)}$ with $k \ge n$. If the graph has no negative cycle, every walk can be shortened to a simple path of at most $n - 1$ edges with no larger weight, so $L^{(k)}[i][j] = \delta(i, j)$, the diagonal is 0, and $\infty$ stays exactly where no path exists. If the graph has a negative cycle, it contains a simple negative cycle $C$ with at most $n$ edges, and for a vertex $i$ on $C$, $L^{(k)}[i][i] \le w(C) < 0$. Conversely, $L^{(k)}[i][i] < 0$ is the weight of a closed walk, which is negative only if some cycle in it is negative. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with additions and comparisons of weights in $O(1)$.

- **Time.** Each squaring takes $\Theta(n^3)$ in the worst case, and there are $\lceil \log_2 n \rceil$ of them, so the time is $\Theta(n^3 \log n)$. Skipping rows with $L[i][t] = \infty$ helps on graphs where few pairs are connected, but a strongly connected graph gets no help.
- **Space.** Two $n \times n$ matrices, $\Theta(n^2)$ extra space.
- **Number size.** Each finite entry is the weight of a walk with at most $2n$ edges, so its absolute value is at most $2n \max |w|$, even when a negative cycle exists. With integer weights the numbers stay small.
- **With a faster product.** The algorithm makes $O(\log n)$ calls to a min-plus product, so any product in time $T(n)$ gives APSP in $O(T(n) \log n)$. Fredman (1976) gave a product in $O(n^3 (\log \log n / \log n)^{1/3})$ time, and Williams (2014) one in $n^3 / 2^{\Omega(\sqrt{\log n})}$.

## Properties

- **Any real weights.** Negative weights are allowed; negative cycles are detected.
- **Only min-plus products.** The algorithm uses the product as a black box. This makes it the bridge between APSP and matrix products used in the [APSP conjecture](/apsp-conjecture/).
- **Associativity.** It relies on the min-plus product being associative, which holds because $(\mathbb{R} \cup \{\infty\}, \min, +)$ is a semiring.
- **Worse than Floyd-Warshall.** For APSP alone it is slower than [Floyd-Warshall](/floyd-warshall/) by a factor $\log n$. Its value is in the product view.
- **No paths by default.** It returns only distances; paths need a witness matrix (see Variants).

## Variants and improvements

- **Exactly $k$ edges.** Without the zeros on the diagonal, the $k$-th min-plus power holds the least weight of a walk with exactly $k$ edges; [binary exponentiation](/binary-exponentiation/) computes it in $O(n^3 \log k)$. See [shortest paths of fixed length](/shortest-paths-fixed-length/).
- **Witnesses for paths.** In line L7, record the $t$ that gave each new minimum. A path from $i$ to $j$ is then rebuilt by recursion on $(i, t)$ and $(t, j)$, each with half the edge budget.
- **Boolean version.** Over the semiring (or, and), the same squaring gives the [transitive closure](/transitive-closure/) with $O(\log n)$ [Boolean matrix products](/boolean-matrix-multiplication/), each in $O(n^{\omega})$ time.
- **Small integer weights.** With weights in $\{-M, \ldots, M\}$, a min-plus product reduces to an ordinary product of matrices with entries of size about $n^{O(M)}$, which brings fast matrix multiplication to bear. Zwick (2002) uses this with sampling to get APSP in $\tilde O(M^{0.681} n^{2.575})$ time for directed graphs.
- **Recursion on the diagonal.** Splitting the matrix into blocks and using Kleene's closure gives $O(T(n))$ instead of $O(T(n) \log n)$; see [Kleene algebra](/kleene-algebra/).

## When to use it

Use it when a fast min-plus product is available, for example on hardware or in a library built for matrix products, or when the distances for walks with a bounded number of edges are what you need. For APSP on its own, [Floyd-Warshall](/floyd-warshall/) is simpler and faster on dense graphs, and [Johnson's algorithm](/johnson/) is faster on sparse ones. The algorithm is mostly a teaching and theory tool: it shows that APSP is no harder than a logarithmic number of min-plus products.

## Pitfalls

- **Stopping too early for the check.** Stopping when $k \ge n - 1$ gives the distances when there is no negative cycle, but it can miss a negative cycle of $n$ edges. With $n = 2$ and the cycle $1 \to 2 \to 1$, no squaring happens at all. Square until $k \ge n$.
- **Forgetting the zero diagonal.** Without $L[i][i] = 0$, the square gives walks with exactly $2k$ edges, not at most $2k$, and the result is not the distance matrix.
- **Infinity in arithmetic.** If $\infty$ is stored as a large number, $\infty + (-5)$ is less than $\infty$, and wrong finite entries appear. Skip the term when either factor is $\infty$, as line L6 does.
- **Overwriting while squaring.** Writing the result into $L$ during the product mixes $L^{(k)}$ and $L^{(2k)}$. That still gives correct distances (each value is still a walk weight and only decreases), but the invariant $L = L^{(k)}$ no longer holds, which matters for the exact-$k$ variant.

## Implementations

The Python version keeps two matrices, skips infinite terms, and returns `None` when the diagonal has a negative entry.

## History

The view of shortest paths as powers of a matrix in the $(\min, +)$ semiring is the basis of CLRS Section 23.1, which presents the slow method and the squaring method before Floyd-Warshall. Fredman (1976) used the product view to give the first APSP algorithm in $o(n^3)$ time, and Williams (2014) used it to give the current best bound for real weights.

## References
