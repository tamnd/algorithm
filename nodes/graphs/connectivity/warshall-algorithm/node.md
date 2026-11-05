---
tag: 036P3Q
kind: algorithm
slug: warshall-algorithm
name: Warshall's algorithm
aliases:
- Warshall-Floyd transitive closure
area: graphs/connectivity
level: core
summary: A dynamic program over intermediate vertices computes the transitive closure in cubic time.
solves: [transitive-closure]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, w: the word size in bits}
  time: {worst: Θ(n³), best: Θ(n²)}
  space: {extra: Θ(n²)}
properties: {deterministic: true, in_place: true}
history:
  year: 1962
  people: [Stephen Warshall]
  note: Published as a theorem on Boolean matrices; Floyd's shortest path algorithm of the same year has the same loop structure.
prereqs: [transitive-closure, adjacency-matrix]
see_also: [floyd-warshall, boolean-matrix-multiplication, reachability, condensation-graph, four-russians-method, bit-vector, transitive-reduction]
sources:
  - paper: doi:10.1145/321105.321107
    title: Stephen Warshall, A theorem on Boolean matrices, Journal of the ACM 9(1), 11 to 12 (1962)
    locator: the whole paper (the procedure and its proof)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.2, The Floyd-Warshall algorithm (the procedure TRANSITIVE-CLOSURE and the recurrence over intermediate vertices)
  - paper: doi:10.1145/367766.368168
    title: Robert W. Floyd, Algorithm 97, Shortest path, Communications of the ACM 5(6), 345 (1962)
    locator: the whole note (the same triple loop with min and plus)
  - paper: doi:10.1145/360715.360746
    title: Henry S. Warren Jr., A modification of Warshall's algorithm for the transitive closure of binary relations, Communications of the ACM 18(4), 218 to 220 (1975)
    locator: the whole paper (the row-wise version in two passes)
---

Warshall's algorithm computes the [transitive closure](/transitive-closure/) of a [directed graph](/directed-graph/) from its [adjacency matrix](/adjacency-matrix/) with three nested loops. The outer loop admits the vertices one at a time as allowed stops on a path, and after vertex $k$ is admitted, the matrix records every pair joined by a path whose inner vertices are all among the first $k + 1$. It takes $\Theta(n^3)$ bit operations, or $\Theta(n^3 / w)$ word operations when rows are stored as bit vectors, and works in place. It is the Boolean form of the [Floyd-Warshall](/floyd-warshall/) shortest path algorithm.

## In plain words

Start with a table that says, for each pair of places, whether a direct one-way street leads from the first to the second. Now allow drivers to stop at place 0 on the way. Every place that can reach 0 can now reach everything 0 reaches, so copy the row of 0 into the row of each such place.

Then allow stops at place 1 as well, and do the same with the row of 1. Keep going through all places. When every place is allowed as a stop, the table says for every pair whether any route exists. Each round needs only the table from the round before, which is why the method is so short.

## The problem

The input is a directed graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$. [Parallel arcs](/multigraph/) and [self-loops](/self-loop/) are allowed: parallel arcs give the same matrix entry, and a loop at $v$ sets $R[v][v] = 1$. The output is the matrix $R$ with $R[u][v] = 1$ exactly when $G$ has a [walk](/walk/) of length at least 1 from $u$ to $v$. So $R[v][v] = 1$ exactly when $v$ lies on a directed cycle. For the reflexive closure, set the diagonal to 1 at the end. An undirected graph, given with both arcs of each edge, gives a symmetric $R$ whose blocks are its [connected components](/connected-components/).

## The algorithm

```pseudo id=main
WARSHALL(G)
L1  for each vertex u do R[u] ← the row of n bits with R[u][v] = 1 for each arc (u, v)
L2  for k ← 0 to n − 1 do
L3      for i ← 0 to n − 1 do
L4          if R[i][k] = 1 then
L5              R[i] ← R[i] OR R[k]            ▷ for each j: if R[k][j] = 1 then R[i][j] ← 1
L6  return R
```

Line L5 is the inner loop over $j$ written as one operation on rows. Stored as an array of bits, it costs $\Theta(n)$ bit operations or $\Theta(\lceil n / w \rceil)$ word operations. The test of line L4 skips the rows that cannot gain anything in round $k$. The matrix is updated in place: entries only change from 0 to 1, and row $k$ does not change in round $k$, because when $i = k$, line L5 takes the OR of row $k$ with itself.

## Example

Take the graph of the [depth-first search](/depth-first-search/) page, with the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. The new 1 entries in each round are:

| round $k$ | rows $i$ with $R[i][k] = 1$ | new entries $(i, j)$ |
|---|---|---|
| 0 | 2 | $(2, 1)$, $(2, 2)$, $(2, 3)$ |
| 1 | 0, 2 | none |
| 2 | 0, 1, 2, 3 | $(0, 0)$, $(1, 0)$, $(1, 1)$, $(1, 3)$, $(3, 0)$, $(3, 1)$, $(3, 3)$ |
| 3 | 0, 1, 2, 3 | $(0, 4)$, $(1, 4)$, $(2, 4)$ |
| 4 | 0, 1, 2, 3, 5 | none |
| 5 | 6 | $(6, 4)$, $(6, 6)$ |
| 6 | 5, 6 | $(5, 5)$ |

The input has 10 arcs, and the result has 26 entries: the rows of 0, 1, 2 and 3 are $\{0, 1, 2, 3, 4\}$, the row of 4 is empty, and the rows of 5 and 6 are $\{4, 5, 6\}$. In round 0, vertex 2 learns the arcs of 0 through $2 \to 0$, including $2 \to 0 \to 2$, which sets $R[2][2]$. In round 2, every vertex that reaches 2 learns the row of 2, which by then contains 0, 1, 2 and 3.

## Correctness

For $k = 0, \ldots, n$, let $P_k$ be the set of pairs $(i, j)$ joined by a walk of length at least 1 whose inner vertices, all but the first and the last, are in $\{0, \ldots, k - 1\}$. Then $P_0$ is the set of arcs, which line L1 stores, and $P_n$ is the transitive closure. The invariant is that after round $k$ of line L2, $R = P_{k+1}$. Two facts give it. A pair set in round $k$ joins two walks through $k$, so it is in $P_{k+1}$. And a pair of $P_{k+1}$ that is not in $P_k$ has a walk that passes through $k$; cut it at the first and the last visit to $k$ to get two walks with inner vertices below $k$, whose pairs are already in $R$ when row $i$ is treated. The full proof, which also handles the in-place updates, is in [the proof page](proofs/correctness.md).

## Complexity

- **Time.** Line L1 takes $\Theta(n^2)$ to clear the matrix and $\Theta(m)$ to set the arcs. Lines L2 to L4 make $n^2$ tests. Line L5 runs at most $n^2$ times, at $\Theta(n)$ bit operations each. So the worst case is $\Theta(n^3)$ bit operations, reached for example by the complete directed graph, where every test of line L4 succeeds; with $w$-bit words it is $\Theta(n^3 / w)$ word operations. The best case is $\Theta(n^2)$, for a graph with no arcs, where line L5 never runs.
- **Space.** The matrix takes $n^2$ bits, counted as the extra space $\Theta(n^2)$ when the input is given as lists; besides it the algorithm uses $O(1)$ words. The input matrix can be overwritten.
- **Comparison.** On sparse graphs, $n$ searches take $O(n(n + m))$ time and are faster. With fast [Boolean matrix multiplication](/boolean-matrix-multiplication/), the closure takes $O(n^\omega)$ time. Warshall's algorithm wins on dense graphs of moderate size, where its simple loops and bit operations run fast.

## Properties

- **In place.** The matrix is its own workspace, and entries only change from 0 to 1.
- **Order of rows is free, order of rounds is not.** Inside a round, the rows can be treated in any order, and even in parallel, because row $k$ does not change in round $k$. The rounds must run in the order $k = 0, 1, \ldots, n - 1$ as the outer loop; any order of the $n$ vertices works, but each must be a full round.
- **Data independent.** Without the test of line L4, the sequence of memory accesses depends only on $n$, which suits hardware and vector code.
- **Semiring form.** Replacing OR and AND by min and $+$ gives [Floyd-Warshall](/floyd-warshall/) for shortest paths. Over a closed semiring the same loops give Kleene's construction of regular expressions from automata.

## Variants and improvements

- **Reflexive closure.** Set $R[v][v] = 1$ before or after the loops.
- **Bit-parallel rows.** Store each row as $\lceil n / w \rceil$ words, as the implementation does with Python integers. This is the version to use in practice.
- **Warren's two-pass version.** Warren reordered the loops so that the outer loop runs over the rows: one pass treats, for each row $i$, the columns $k < i$, and a second pass the columns $k > i$. This reads the matrix row by row, which is better when the matrix is stored on disk or in pages.
- **Through the condensation.** First contract the [strong components](/strongly-connected-components/), run the closure on the [condensation](/condensation-graph/), which is a DAG and may be much smaller, and expand. On a DAG in topological order a single pass over the rows in reverse order suffices.
- **Blocked versions.** Cut the matrix into tiles of size $b \times b$ that fit in cache and run the rounds tile by tile, as for Floyd-Warshall. The work is the same and the cache misses drop by a factor near $b$.

## When to use it

Use Warshall's algorithm for dense graphs with up to a few thousand vertices, when the whole closure matrix is wanted and an adjacency matrix is at hand. It is a few lines, easy to check, and with bit rows its inner loop is a fast memory-bound OR. For sparse graphs, use a search from each vertex, or contract the strong components first. For very large dense graphs, use fast Boolean matrix multiplication. For single queries, a single [reachability](/reachability/) search is enough.

## Pitfalls

- **Loop order.** The intermediate vertex $k$ must be the outer loop. With $i$ outside and $k$ inside, the algorithm is wrong. For the arcs $0 \to 2$, $1 \to 0$, $2 \to 1$, a directed 3-cycle, row 0 meets $k = 1$ while $R[0][1] = 0$, and only later, at $k = 2$, gains bit 1 from row 2; it never goes back, so $R[0][0]$ stays 0.
- **Diagonal convention.** The algorithm computes walks of length at least 1, so $R[v][v] = 1$ only on cycles. Code that expects the reflexive closure must set the diagonal.
- **Cubic cost on sparse graphs.** On a graph with $10^5$ vertices and few arcs, $n^3 = 10^{15}$ bit operations are far too many, and $n^2$ bits of output are already 1.25 gigabytes. Use searches, and store rows only when needed.

## Implementations

## History

Stephen Warshall published the algorithm in 1962 as a theorem on Boolean matrices. Robert Floyd's shortest path algorithm, published the same year, uses the same triple loop with min and plus, which is why both are often called the Floyd-Warshall algorithm. Henry Warren gave a row-oriented variant in 1975.

## References
