---
tag: EK3RJN
kind: algorithm
slug: slow-apsp-matrix-multiplication
name: Slow all-pairs shortest paths by matrix multiplication
aliases:
- SLOW-APSP
- EXTEND-SHORTEST-PATHS
area: graphs/shortest-paths
level: core
summary: Computes all-pairs shortest paths by extending path lengths one edge at a time with a min-plus matrix product, in cubic time per step.
solves: [all-pairs-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n^4), best: Θ(n^4)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [all-pairs-shortest-paths, shortest-path-optimal-substructure, adjacency-matrix]
see_also: [apsp-repeated-squaring, min-plus-matrix-multiplication, floyd-warshall, johnson, shortest-paths-fixed-length, all-pairs-shortest-paths, bellman-ford, transitive-closure]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.1, Shortest paths and matrix multiplication (the recurrence for l_ij^(r), the procedures EXTEND-SHORTEST-PATHS and SLOW-APSP, Figure 23.1 and the comparison with matrix multiplication)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 9, All-Pairs Shortest Paths (the dynamic program over the number of edges and its min-plus matrix form)
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 5, the sections on path-finding problems and closed semirings (the matrix form of shortest paths and transitive closure)
---

The slow all-pairs shortest-path algorithm computes the matrix of distances $\delta(i, j)$ of a weighted directed graph by dynamic programming on the number of arcs. The matrix $L^{(r)}$ holds the least weight of a walk with at most $r$ arcs between each pair, and $L^{(r)}$ is the [min-plus product](/min-plus-matrix-multiplication/) of $L^{(r-1)}$ and the weight matrix $W$. After $n - 1$ products, $L^{(n-1)}$ is the distance matrix when there is no [negative cycle](/negative-cycle/), and one more product tells whether there is one. Each product takes $\Theta(n^3)$ time, so the total is $\Theta(n^4)$. It is the start point of [repeated squaring](/apsp-repeated-squaring/) and shows that [all-pairs shortest paths](/all-pairs-shortest-paths/) is a matrix-product problem.

## In plain words

Make a table of the cheapest costs between all pairs of places, but allow only routes with at most one road. Then make a new table that allows at most two roads: for each pair, try every place as the last stop before the end, and take the cheapest "best route to that stop, then one road". Repeat this, one more road each time.

A cheapest route never needs to visit a place twice, so it never needs more roads than there are places minus one. When the table stops changing at that point, it holds the answers. If one more round still makes some cost from a place back to itself negative, there is a loop of roads with a negative total.

## The problem

The input is a directed graph on the vertices $1, \ldots, n$ with weights $w$, given as the matrix $W$ with $W[i][i] = 0$, $W[i][j] = w(i, j)$ for an arc $i \to j$ (the least weight, if there are parallel arcs) and $W[i][j] = \infty$ otherwise. The output is the matrix $D$ with $D[i][j] = \delta(i, j)$, with $\infty$ for the pairs where $j$ is not reachable from $i$, or the report that the graph has a negative cycle.

**Weight assumptions.** Any real weights, negative ones included. If the graph has a negative cycle anywhere, the algorithm reports it and returns no matrix. A self-loop of negative weight $c$ is a negative cycle and is put on the diagonal as $W[i][i] = c$; a self-loop of nonnegative weight is never useful and is ignored. Integer weights are not needed.

## The algorithm

```pseudo id=main
SLOW-APSP(W, n)
L1  L ← W                                  ▷ walks with at most 1 arc
L2  for r ← 2 to n do
L3      L ← EXTEND(L, W)                   ▷ walks with at most r arcs
L4  if L[i][i] < 0 for some i then return "negative cycle"
L5  return L

EXTEND(L, W)
L6  let L′ be a new n × n matrix
L7  for i ← 1 to n do for j ← 1 to n do
L8      L′[i][j] ← min over k of (L[i][k] + W[k][j])
L9  return L′
```

The recurrence behind line L8 is

$$l^{(r)}_{ij} = \min_{1 \le k \le n} \big( l^{(r-1)}_{ik} + w_{kj} \big),$$

where $k = j$ with $w_{jj} = 0$ keeps the walks with fewer than $r$ arcs. This is the ordinary matrix product with $+$ replaced by $\min$ and $\times$ replaced by $+$, so $L^{(r)} = W^r$ in the min-plus algebra. CLRS stops at $r = n - 1$ and assumes there is no negative cycle; line L2 does one more product so that line L4 can test for one, and with no negative cycle $L^{(n)} = L^{(n-1)}$.

## Example

The graph of CLRS Figure 23.1 has the vertices 1 to 5 and the arcs $1 \to 2$ (3), $1 \to 3$ (8), $1 \to 5$ ($-4$), $2 \to 4$ (1), $2 \to 5$ (7), $3 \to 2$ (4), $4 \to 1$ (2), $4 \to 3$ ($-5$) and $5 \to 4$ (6). The rows of the matrices are:

| row | $L^{(1)} = W$ | $L^{(2)}$ | $L^{(3)}$ | $L^{(4)} = D$ |
|---|---|---|---|---|
| 1 | $0, 3, 8, \infty, -4$ | $0, 3, 8, 2, -4$ | $0, 3, -3, 2, -4$ | $0, 1, -3, 2, -4$ |
| 2 | $\infty, 0, \infty, 1, 7$ | $3, 0, -4, 1, 7$ | $3, 0, -4, 1, -1$ | $3, 0, -4, 1, -1$ |
| 3 | $\infty, 4, 0, \infty, \infty$ | $\infty, 4, 0, 5, 11$ | $7, 4, 0, 5, 11$ | $7, 4, 0, 5, 3$ |
| 4 | $2, \infty, -5, 0, \infty$ | $2, -1, -5, 0, -2$ | $2, -1, -5, 0, -2$ | $2, -1, -5, 0, -2$ |
| 5 | $\infty, \infty, \infty, 6, 0$ | $8, \infty, 1, 6, 0$ | $8, 5, 1, 6, 0$ | $8, 5, 1, 6, 0$ |

For example $l^{(4)}_{12} = 1$ comes from the walk $1 \to 5 \to 4 \to 3 \to 2$ with $-4 + 6 - 5 + 4 = 1$, which has 4 arcs; with at most 3 arcs, the best is the arc $1 \to 2$ of weight 3. The product for $r = 5$ gives $L^{(5)} = L^{(4)}$, and its diagonal is 0, so there is no negative cycle.

**A negative cycle.** Add the arc $3 \to 4$ of weight 4. The cycle $3 \to 4 \to 3$ has weight $-1$, and $L^{(5)}[3][3] < 0$, so line L4 reports it.

**A negative cycle through every vertex.** On the vertices 1, 2, 3 with the arcs $1 \to 2$ (1), $2 \to 3$ (1), $3 \to 1$ ($-3$), the diagonal of $L^{(2)}$ is still 0, because the cycle has 3 arcs. Only $L^{(3)}$ shows $-1$ on the diagonal. This is why line L2 goes to $n$ and not to $n - 1$.

## Correctness

**Theorem.** For every $r \ge 1$, $L^{(r)}[i][j]$ is the least weight of a walk from $i$ to $j$ with at most $r$ arcs, or $\infty$ if there is none. Hence SLOW-APSP reports a negative cycle if and only if the graph has one, and otherwise it returns $D[i][j] = \delta(i, j)$ for all $i, j$.

The first part is an induction on $r$: a walk with at most $r$ arcs is either a walk with at most $r - 1$ arcs, which is the term $k = j$, or a walk with at most $r - 1$ arcs to some $k$ followed by the arc $k \to j$. For the second part, if there is no negative cycle, a shortest walk can be taken to be a simple path, with at most $n - 1$ arcs ([optimal substructure](/shortest-path-optimal-substructure/) and cycle removal), so $L^{(n-1)} = L^{(n)} = D$ and the diagonal is 0. If there is a negative cycle, it has at most $n$ arcs and gives a negative entry on the diagonal of $L^{(n)}$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** EXTEND has three nested loops of $n$ steps with $O(1)$ work, so it takes $\Theta(n^3)$ time. SLOW-APSP calls it $n - 1$ times, and line L4 takes $\Theta(n)$. The total is $\Theta(n^4)$ in every case, on the word RAM where an addition or comparison of two weights takes $O(1)$ time.
- **Space.** Two $n \times n$ matrices, the current $L$ and the new $L'$, plus $W$: $\Theta(n^2)$.

The time does not depend on the number of arcs. Compare $\Theta(n^3 \log n)$ for [repeated squaring](/apsp-repeated-squaring/), $\Theta(n^3)$ for [Floyd-Warshall](/floyd-warshall/) and $O(nm + n^2 \log n)$ for [Johnson's algorithm](/johnson/).

## Properties

- **Exact.** It returns exact distances for any real weights.
- **All or nothing on negative cycles.** A negative cycle anywhere makes line L4 stop, even when most pairs cannot reach it.
- **Fixed lengths for free.** Without the $W[i][i] = 0$ convention, the same products give the least weight of walks with exactly $r$ arcs. This is the problem of [shortest paths of fixed length](/shortest-paths-fixed-length/).
- **Intermediate matrices.** $L^{(r)}$ is useful in itself, for example for hop-limited routing, where a route may use at most $r$ links.
- **Paths.** A predecessor matrix can be kept with the minimizing $k$ of line L8. The $k$ of the last product is the vertex before $j$.

## Variants and improvements

- **Repeated squaring.** Since the min-plus product is associative, $W^{2r} = W^r \otimes W^r$, and $\lceil \log_2 (n-1) \rceil$ squarings give $L^{(n-1)}$ in $\Theta(n^3 \log n)$ time. See [repeated squaring](/apsp-repeated-squaring/).
- **Early stop.** If $L^{(r)} = L^{(r-1)}$ for some $r < n$, then no later product changes anything, and $L^{(r)}$ is the distance matrix when its diagonal is 0. This saves time when shortest paths have few arcs.
- **Floyd-Warshall.** Changing the meaning of the index $r$ from "at most $r$ arcs" to "only vertices $1, \ldots, r$ inside" gives a recurrence with one $\min$ of two terms per entry instead of $n$, and $\Theta(n^3)$ time. See [Floyd-Warshall](/floyd-warshall/).
- **Other semirings.** With $(\vee, \wedge)$ the same products compute the [transitive closure](/transitive-closure/), and with $(\max, \min)$ they compute widest paths.
- **Fast products.** Min-plus products have no known $O(n^{3 - \varepsilon})$ algorithm for real weights; the [APSP conjecture](/apsp-conjecture/) says there is none. For small integer weights, reductions to fast ordinary matrix multiplication exist.

## When to use it

Use it to teach the link between shortest paths and matrix products, to compute the hop-limited matrices $L^{(r)}$ for small $r$, or as a reference oracle in tests for tiny graphs. For all-pairs distances in practice, use [Floyd-Warshall](/floyd-warshall/) on dense graphs and [Johnson's algorithm](/johnson/) on sparse ones.

## Pitfalls

- **Forgetting the zero diagonal.** With $W[i][i] = \infty$, line L8 loses the walks with fewer arcs, and $L^{(r)}$ becomes walks with exactly $r$ arcs. Then $L^{(n-1)}$ is not the distance matrix.
- **Stopping at $n - 1$ and testing the diagonal.** A negative cycle through all $n$ vertices has $n$ arcs and does not show on the diagonal of $L^{(n-1)}$, as the 3-vertex example shows. Test $L^{(n)}$.
- **Updating in place.** Writing the result of line L8 into $L$ while it is read mixes walk lengths. For distances this is harmless, since every value is still the weight of a walk, but the meaning "at most $r$ arcs" is lost and the fixed-length use breaks. Use a new matrix, as line L6 does.
- **Infinity arithmetic.** With a large number as $\infty$ and negative weights, $\infty + w$ can become smaller than $\infty$ and look like a real walk. Use a true infinity, or skip terms with $L[i][k] = \infty$.
- **Parallel arcs and self-loops.** Keep the least weight of parallel arcs in $W$. A negative self-loop must lower the diagonal entry, or the negative cycle is missed.

## Implementations

## History

The use of matrix products over $(\min, +)$ for shortest paths goes back to the 1950s; Shimbel (1953 to 1955) described distances in networks by powers of a matrix with this product. The closed-semiring view that covers shortest paths, transitive closure and regular expressions with the same matrix algorithms was set out by Aho, Hopcroft and Ullman (1974). CLRS presents SLOW-APSP and repeated squaring as the bridge from single-source to all-pairs methods, before Floyd-Warshall.

## References
