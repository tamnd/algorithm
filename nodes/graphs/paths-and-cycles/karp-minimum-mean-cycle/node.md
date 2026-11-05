---
tag: CDP661
kind: algorithm
slug: karp-minimum-mean-cycle
name: Karp's minimum mean cycle algorithm
aliases:
- Karp's algorithm for the minimum cycle mean
area: graphs/paths-and-cycles
level: advanced
summary: Solves the minimum mean cycle problem in O(nm) time with a dynamic program over walk lengths.
solves: [minimum-mean-cycle-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: Θ(n(n + m)), best: Θ(n(n + m))}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1978
  people: [Richard M. Karp]
  note: A characterization of the minimum cycle mean in a digraph, Discrete Mathematics; the formula with walks of exactly k arcs.
prereqs: [minimum-mean-cycle-problem, bellman-ford, simple-cycle]
see_also: [negative-cycle, cycle-canceling, min-plus-matrix-multiplication, shortest-cycle-problem, strongly-connected-components, weighted-graph, johnson-elementary-cycles-algorithm, walk]
sources:
  - paper: doi:10.1016/0012-365X(78)90011-0
    title: Richard M. Karp, A characterization of the minimum cycle mean in a digraph, Discrete Mathematics 23(3), 309 to 311 (1978)
    locator: the theorem that gives the minimum cycle mean as a min over vertices of a max over k, and the O(nm) algorithm
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Prentice Hall, 1993
    locator: Chapter 5, Label-correcting algorithms (the minimum mean cycle problem and Karp's formula)
  - paper: Mark Hartmann and James B. Orlin, Finding minimum cost to time ratio cycles with small integral transit times, Networks 23(6), 1993
    title: Hartmann and Orlin, early termination of Karp's algorithm
    locator: the improved version of Karp's algorithm that may stop before n rounds
---

Karp's algorithm finds the smallest average arc weight of a directed cycle, and a cycle with that average, in $\Theta(n(n + m))$ time. It fills a table $D_k(v)$, the least weight of a [walk](/walk/) with exactly $k$ arcs that ends at $v$, for $k = 0, \ldots, n$, with one pass over the arcs for each $k$, as in [Bellman-Ford](/bellman-ford/). Karp proved that the minimum cycle mean is $\min_v \max_k (D_n(v) - D_k(v))/(n - k)$, and a cycle with that mean lies on the walk that gives $D_n(v)$. The graph is directed; parallel arcs and self-loops are allowed, and weights may have any sign. It solves the [minimum mean cycle problem](/minimum-mean-cycle-problem/).

## In plain words

Each one-way road has a cost, which can be negative. You want a round trip whose cost per road is as small as possible.

Make a table. For each place and each number of steps from 0 to the number of places, write the cheapest cost of a trip with exactly that many steps that ends at the place. Each row comes from the row before, by trying every road once.

A trip with as many steps as there are places must go around some loop. Karp found a short formula that reads the best cost per road of a loop from the first and the last rows of the table. To get the loop itself, follow the cheapest longest trip backwards until a place repeats.

## The problem

Given a directed graph $G = (V, A)$ with $V = \{0, \ldots, n - 1\}$ and arcs $a = (u, v)$ with real weights $w(a)$, the *mean* of a directed cycle $C$ with $|C|$ arcs is $w(C)/|C|$. Find $\lambda^* = \min_C w(C)/|C|$ over all directed cycles and a cycle that attains it, or report that $G$ has no cycle. A self-loop is a cycle with one arc, and two opposite arcs form a cycle with two arcs. Parallel arcs are allowed; a cycle uses one of them. The graph need not be strongly connected and may have isolated vertices. The minimum over all cycles equals the minimum over [simple cycles](/simple-cycle/), because a closed walk splits into simple cycles and its mean is a weighted average of theirs.

## The algorithm

The table starts at $D_0(v) = 0$ for every $v$, which is the same as a new source joined to every vertex by an arc of weight 0. An entry is $\infty$ when no walk with exactly $k$ arcs ends at $v$; terms with $D_k(v) = \infty$ are skipped in the max.

```pseudo id=main
KARP(G, w)
L1  D[0][v] ← 0 for every vertex v
L2  for k ← 1 to n do
L3      D[k][v] ← ∞ and P[k][v] ← NIL for every vertex v
L4      for each arc a = (u, v) do
L5          if D[k-1][u] + w(a) < D[k][v] then D[k][v] ← D[k-1][u] + w(a); P[k][v] ← a
L6  λ ← ∞; t ← NIL
L7  for each vertex v with D[n][v] < ∞ do
L8      μ ← max over k = 0 .. n-1 with D[k][v] < ∞ of (D[n][v] − D[k][v]) / (n − k)
L9      if μ < λ then λ ← μ; t ← v
L10 if t = NIL then return "G has no cycle"
L11 follow P back from (n, t): the arc P[k][v] = (u, v) leads to (k − 1, u); stop at the first vertex seen twice, and let C be the arcs between its two visits
L12 return λ, C
```

Line L8 uses exact arithmetic: with integer or rational weights the values are rational, and the implementation uses fractions. If no walk of $n$ arcs exists, line L7 finds no vertex and the graph is acyclic, since a cycle would give walks of every length.

## Example

Arcs, numbered from 0: $0 \to 1$ (weight 2), $1 \to 0$ (4), $1 \to 2$ (1), $2 \to 3$ (1), $3 \to 1$ (4), $3 \to 0$ (0). The directed cycles are $0, 1$ with mean $6/2 = 3$, $1, 2, 3$ with mean $6/3 = 2$, and $0, 1, 2, 3$ with mean $4/4 = 1$.

| $k$ | $D_k(0)$ | $D_k(1)$ | $D_k(2)$ | $D_k(3)$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 2 | 1 | 1 |
| 2 | 1 | 2 | 3 | 2 |
| 3 | 2 | 3 | 3 | 4 |
| 4 | 4 | 4 | 4 | 4 |

The values $(D_4(v) - D_k(v))/(4 - k)$ for $k = 0, 1, 2, 3$ are $1, 4/3, 3/2, 2$ for $v = 0$; $1, 2/3, 1, 1$ for $v = 1$; $1, 1, 1/2, 1$ for $v = 2$; and $1, 1, 1, 0$ for $v = 3$. The maxima are 2, 1, 1 and 1, and their minimum is $\lambda^* = 1$, first at $t = 1$. Line L11 follows the walk behind $D_4(1) = 4$ backwards: arc $0 \to 1$, then $3 \to 0$, then $2 \to 3$, then $1 \to 2$, and vertex 1 repeats. The cycle is $1 \to 2 \to 3 \to 0 \to 1$, arcs 2, 3, 5, 0, with weight 4 and mean 1.

## Correctness

Subtracting $\lambda$ from every arc weight subtracts $k\lambda$ from $D_k(v)$ and $\lambda$ from every cycle mean, so the formula shifts with the weights, and one may assume $\lambda^* = 0$. Then no cycle is negative, and $D_n(v)$ is at least the shortest walk weight $\min_k D_k(v)$, because a walk of $n$ arcs contains a cycle that can be removed. So every max at line L8 is at least 0. A vertex $v$ on a zero-weight cycle $C$, chosen so that the shortest walk to $v$ continued around $C$ has weight equal to the shortest walk to its end, gives max exactly 0. For the cycle: at the chosen vertex, $D_n(t) \le D_k(t)$ for every $k$, and removing a cycle from the walk of $D_n(t)$ gives a shorter walk to $t$, so every cycle on that walk has weight at most 0, hence exactly 0. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with weights and sums that fit in a word.

- **Lines L1 to L5.** $n$ rounds, each $\Theta(n)$ for line L3 and $\Theta(m)$ for lines L4 and L5. Total $\Theta(n(n + m))$, which is $\Theta(nm)$ when $m \ge n$.
- **Lines L7 to L9.** $\Theta(n^2)$ for all the quotients.
- **Line L11.** At most $n$ steps back.

The table takes $\Theta(n^2)$ space with the pointers $P$. The rounds always run to $k = n$, so the best case is the same as the worst case.

## Properties

- **Exact.** It returns the minimum mean exactly, as a fraction, and a cycle that attains it.
- **Any weights.** Negative weights and negative cycles are allowed; the answer is then negative.
- **Directed.** An undirected edge used in both directions is a cycle of two arcs with mean $w(e)$, so undirected graphs need a different problem statement.
- **No strong connectivity needed.** With $D_0 = 0$ at every vertex, the formula holds for any digraph. Karp's paper fixes a source in a strongly connected graph; running it per [strongly connected component](/strongly-connected-components/) is the other common choice.
- **Deterministic and not recursive.**

## Variants and improvements

- **Maximum mean cycle.** Negate the weights.
- **Early termination.** Hartmann and Orlin (1993) stop the rounds early when the table shows that the answer is reached, which often saves most of the work in practice; the worst case is unchanged.
- **Less space.** The formula needs only $D_n$ and each $D_k$ once, so a second pass that recomputes the rows gives $\Theta(n)$ extra space, at twice the time; the cycle then needs a separate step.
- **Binary search on $\lambda$.** Shift the weights by $\lambda$ and test for a [negative cycle](/negative-cycle/) with Bellman-Ford. With integer weights this gives $O(nm \log(nW))$ time, where $W$ is the largest absolute weight.
- **Policy iteration.** Howard's algorithm has no good worst-case bound known, but it is often the fastest in practice.
- **Min-plus algebra.** $D_k$ is a min-plus matrix-vector product, see [min-plus matrix multiplication](/min-plus-matrix-multiplication/), and $\lambda^*$ is the eigenvalue of the min-plus weight matrix of a strongly connected graph.
- **Cycle canceling.** The minimum mean cycle canceling algorithm of Goldberg and Tarjan for minimum cost flow calls a minimum mean cycle routine in each step; see [cycle canceling](/cycle-canceling/).

## When to use it

Use it when you need the exact minimum or maximum cycle mean of a graph with up to a few thousand vertices: the cycle time of a periodic schedule, the throughput of a synchronous circuit or data flow graph, or the cycle to cancel in a minimum cost flow. It is simple and has a guaranteed bound. For large sparse graphs, the early termination version or policy iteration is usually faster.

## Pitfalls

- **Taking the max over all $k$ including infinite rows.** When $D_k(v) = \infty$, the quotient is $-\infty$ and must be skipped, not treated as a large number.
- **Taking the min instead of the max.** The formula is min over $v$ of max over $k$; with the max and min swapped, the result is wrong.
- **Floating point.** Comparing quotients in floating point can select a wrong vertex when two means are close. Use fractions, or compare $(D_n(v) - D_k(v))(n - k')$ with $(D_n(v') - D_{k'}(v'))(n - k)$ in integers.
- **Starting only from one source.** If $D_0$ is 0 at one vertex and the graph is not strongly connected, cycles not reachable from it are missed.
- **Reading the cycle at a wrong vertex.** Only the walk at a vertex that attains the minimum is guaranteed to hold an optimal cycle; at another vertex, the walk of $n$ arcs can contain a worse cycle.

## Implementations

## History

Richard Karp published the characterization of the minimum cycle mean in Discrete Mathematics in 1978, as a three-page note. The problem had come up in the analysis of periodic systems and of minimum cost flows, and earlier methods used a search over $\lambda$ with a negative cycle test. Karp's formula needs no search. Later work made the algorithm stop early (Hartmann and Orlin, 1993) and compared it in experiments with policy iteration and parametric methods.

## References
