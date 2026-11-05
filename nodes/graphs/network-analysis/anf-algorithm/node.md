---
tag: MDNVAV
kind: algorithm
slug: anf-algorithm
name: ANF algorithm
aliases:
- approximate neighbourhood function
- HyperANF
area: graphs/network-analysis
level: advanced
summary: Estimates neighbourhood functions with Flajolet-Martin style sketches.
solves: [network-diameter-estimation]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, h: the number of rounds, r: the number of sketches per vertex}
  time: {worst: Θ(h r (n + m)), best: Θ(h r (n + m))}
  space: {extra: Θ(n r)}
properties: {directed: true, weighted: false, deterministic: false, recursive: false}
prereqs: [neighborhood-function, flajolet-martin-sketch, breadth-first-search]
see_also: [neighborhood-function, network-diameter-estimation, effective-diameter, flajolet-martin-sketch, hyperloglog, small-world-network, all-pairs-shortest-paths, transitive-closure]
sources:
  - paper: doi:10.1145/775047.775059
    title: Christopher R. Palmer, Phillip B. Gibbons and Christos Faloutsos, ANF, a fast and scalable tool for data mining in massive graphs, Proceedings of the 8th ACM SIGKDD Conference (KDD 2002), 81 to 90
    locator: the whole paper (the neighbourhood function, the bitmask iteration, the use of several bitmasks per vertex, and the hop plot and effective diameter of real graphs)
  - paper: doi:10.1016/0022-0000(85)90041-8
    title: Philippe Flajolet and G. Nigel Martin, Probabilistic counting algorithms for data base applications, Journal of Computer and System Sciences 31(2), 182 to 209 (1985)
    locator: the bitmap, the position R of the lowest zero, the constant φ ≈ 0.77351, and the analysis of the bias and of the standard error
  - paper: doi:10.1145/1963405.1963493
    title: Paolo Boldi, Marco Rosa and Sebastiano Vigna, HyperANF, approximating the neighbourhood function of very large graphs on a budget, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 625 to 634
    locator: the whole paper (HyperLogLog counters in place of bitmasks, the broadword union, and the error bounds)
  - paper: doi:10.1006/jcss.1997.1534
    title: Edith Cohen, Size-estimation framework with applications to transitive closure and reachability, Journal of Computer and System Sciences 55(3), 441 to 453 (1997)
    locator: the whole paper (estimates of the sizes of all reachability sets by minimum ranks)
---

The ANF algorithm (approximate neighbourhood function) estimates, for a graph with $n$ vertices and $m$ edges, the [neighbourhood function](/neighborhood-function/) $N(h)$, the number of ordered pairs of vertices at distance at most $h$, for $h = 0, 1, 2, \ldots$ Each vertex keeps a [Flajolet-Martin sketch](/flajolet-martin-sketch/) of the set of vertices it reaches in $h$ steps. One round sets the sketch of each vertex to the bitwise OR of its own sketch and those of its out-neighbours, which costs $O(n + m)$ word operations, and the size of each set is read from its sketch. So $h$ rounds take $O(h(n + m))$ time per sketch and $O(n)$ words of memory, where exact [breadth-first search](/breadth-first-search/) from every vertex would take $O(n(n + m))$ time. Palmer, Gibbons and Faloutsos proposed it in 2002, and the [effective diameter](/effective-diameter/) of large networks is usually computed with it or with its successor HyperANF.

## In plain words

How many pairs of people in a huge network are at most three handshakes apart? Running a search from every person takes far too long.

ANF gives each person a tiny note instead of a full list of who they can reach. The note is a short row of bits, built so that the note for a group is the bits of all members put together, and so that a long row of ones means a large group.

In each round, every person copies onto their note all the bits from the notes of their neighbours. After three rounds, each note covers everyone within three steps. Reading the length of the run of ones gives a rough count, and averaging several notes per person makes it accurate. Adding the counts over all people estimates the number of close pairs.

## The problem

The input is a graph $G = (V, E)$, directed or undirected, without weights, given by adjacency lists, with $V = \{0, \ldots, n-1\}$; an undirected edge is in both lists. It need not be connected. Let $B_h(v)$ be the set of vertices reachable from $v$ by a path of at most $h$ arcs, $v$ included. The neighbourhood function is

$$N(h) = \sum_{v \in V} |B_h(v)|,$$

so $N(0) = n$, $N$ does not decrease, and it stops growing at the largest finite distance. For a disconnected graph, $N(h)$ tends to the number of ordered pairs $(v, u)$ with $u$ reachable from $v$, not to $n^2$; the [effective diameter](/effective-diameter/) is taken relative to this limit. The output is an estimate $\hat N(h)$ for each $h \le h_{\max}$. From it one reads the hop plot, the effective diameter and, as the last $h$ with $N(h) > N(h-1)$, the diameter, when the estimates are good enough to see the last change.

**The sketch.** Fix $r$ independent copies. In copy $j$, each vertex $u$ gets a random bit position $\rho_j(u)$ with $\Pr[\rho_j(u) = i] = 2^{-(i+1)}$. The sketch of a set $S$ in copy $j$ is the bitmask $M_j(S) = \bigvee_{u \in S} 2^{\rho_j(u)}$. Let $R(x)$ be the position of the lowest 0 bit of a bitmask $x$. Flajolet and Martin estimate $|S|$ by

$$\widehat{|S|} = \frac{1}{\varphi}\, 2^{\frac{1}{r}\sum_{j=1}^{r} R(M_j(S))}, \qquad \varphi \approx 0.77351.$$

The key fact is $M_j(S \cup T) = M_j(S) \vee M_j(T)$: the sketch of a union is the OR of the sketches, whatever the overlap.

## The algorithm

```pseudo id=main
ANF(G, h_max, ρ)
L1  for each v ∈ V do for j ← 1 to r do M[v][j] ← 2^ρ_j(v)          ▷ the sketch of B_0(v) = {v}
L2  N̂[0] ← Σ_v ESTIMATE(M[v])
L3  for h ← 1 to h_max do
L4      for each v ∈ V do M′[v] ← M[v]
L5      for each v ∈ V do for each u ∈ Adj[v] do for j ← 1 to r do M′[v][j] ← M′[v][j] OR M[u][j]
L6      M ← M′
L7      N̂[h] ← Σ_v ESTIMATE(M[v])
L8  return N̂
```

Here ESTIMATE$(x_1, \ldots, x_r) = \varphi^{-1}\, 2^{\frac1r \sum_j R(x_j)}$. Line L5 reads only the old array $M$, so each round extends every ball by exactly one step. With $O(\log n)$ bits, each bitmask fits in one machine word, and $R(x)$ is one word operation: the lowest set bit of $x + 1$.

## Example

Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. Breadth-first search gives the exact values

$$N(0), \ldots, N(4) = 7, 25, 35, 45, 49,$$

since 18 ordered pairs are at distance 1, 10 at distance 2, 10 at distance 3 and 4 at distance 4.

To see the iteration, take one copy, $r = 1$, with the bit positions $\rho(0), \ldots, \rho(6) = 2, 0, 1, 0, 3, 0, 1$.

| $h$ | $M[0]$ | $M[1]$ | $M[2]$ | $M[3]$ | $M[4]$ | $M[5]$ | $M[6]$ | $\hat N(h)$ | $N(h)$ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0100 | 0001 | 0010 | 0001 | 1000 | 0001 | 0010 | 12.93 | 7 |
| 1 | 0111 | 0111 | 0111 | 1011 | 1011 | 1011 | 1011 | 51.71 | 25 |
| 2 | 0111 | 1111 | 1111 | 1111 | 1011 | 1011 | 1011 | 87.91 | 35 |
| 3 | 1111 | 1111 | 1111 | 1111 | 1111 | 1011 | 1011 | 113.77 | 45 |
| 4 | 1111 | 1111 | 1111 | 1111 | 1111 | 1111 | 1111 | 144.79 | 49 |

For $h = 1$, $B_1(3) = \{1, 2, 3, 4\}$ has the bits $0, 1, 0, 3$, so $M[3] = 1011$, $R = 2$, and the estimate is $2^2/\varphi \approx 5.17$ for a set of 4. With one copy the estimates are crude: each is a power of 2 divided by $\varphi$. With $r = 64$ copies from a seeded generator, the estimates become $13.1, 28.0, 36.8, 45.9, 48.0$, within 12 percent of the exact values for $h \ge 1$. At $h = 0$ the estimate is about $1.8$ per vertex, because the Flajolet-Martin estimator is biased upward for very small sets; ANF can use the exact $N(0) = n$ instead.

## Correctness

**Theorem.** ANF stops, and after round $h$, $M[v][j] = M_j(B_h(v))$ for every vertex $v$ and copy $j$. So $\hat N(h)$ is the sum over $v$ of the Flajolet-Martin estimate of $|B_h(v)|$ from $r$ independent sketches.

The proof is an induction on $h$ with the identity $B_h(v) = \{v\} \cup \bigcup_{u \in \mathrm{Adj}[v]} B_{h-1}(u)$, and the fact that the sketch of a union is the OR of the sketches; the overlaps between the balls do not matter, which is why sketches with OR fit this problem. The quality of the estimate is then that of the Flajolet-Martin estimator: Flajolet and Martin show that $\mathbb{E}[R] \approx \log_2(\varphi |S|)$ for large $|S|$, up to a small periodic term, and averaging $r$ copies makes the relative standard error fall like $1/\sqrt{r}$. If each term is within a relative error $\varepsilon$, so is the sum $\hat N(h)$; since all terms use the same random positions, their errors need not cancel. The full proof of the sketch identity is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with each bitmask in one word of $\Theta(\log n)$ bits.

- **Initialization.** Line L1 draws $nr$ positions, $\Theta(nr)$.
- **One round.** Line L4 copies $nr$ words, and line L5 does $r$ ORs for each of the $m$ arcs (or $2m$ for an undirected graph). Line L7 computes $nr$ values of $R$ and $n$ powers. So a round costs $\Theta(r(n + m))$.
- **All rounds.** $\Theta(h_{\max}\, r (n + m))$ time, and $\Theta(nr)$ words for the two arrays $M$ and $M'$.

The rounds scan the edges in order, so ANF works well with the graph on disk or compressed, which was its first purpose. To get the whole function, run until $\hat N$ stops changing, which takes about the diameter of rounds.

## Properties

- **Directed or undirected, no weights.** For a directed graph, $B_h(v)$ is the set reached by out-arcs; to count the vertices that reach $v$, use the reversed lists. Weights are not supported: the rounds count arcs.
- **Randomized.** The estimates depend on the random positions $\rho$. With the positions fixed, as with a seed, the run is deterministic, and the sketches are exact functions of the balls.
- **Not recursive.** Rounds of loops over arrays.
- **Monotone.** Each sketch only gains bits, so each $\hat N(h)$ is at least $\hat N(h-1)$, like $N$ itself.
- **Ties and disconnected graphs.** There are no choices between equal items; a vertex in a separate component simply never receives the bits of the others.

## Variants and improvements

- **HyperANF.** Boldi, Rosa and Vigna replace each group of Flajolet-Martin bitmasks by a [HyperLogLog](/hyperloglog/) counter, whose registers hold maxima instead of bits and whose union is a register-wise maximum, computed with broadword tricks. For the same memory it gives a much smaller error, and it was used to compute the distance distribution of the whole Facebook graph.
- **Minimum ranks.** Cohen estimates the size of every reachability set by giving each vertex a random rank and propagating the minimum rank, with the same OR-like union. This works also for the full transitive closure of a directed graph.
- **Exact methods.** For small graphs, a BFS from each vertex gives $N(h)$ exactly in $O(n(n + m))$ time; see [all-pairs shortest paths](/all-pairs-shortest-paths/).
- **Local values.** The sketches also give, for each vertex, its estimated ball sizes, which yields approximate [closeness](/closeness-centrality/) and [harmonic centrality](/harmonic-centrality/) for all vertices.

## When to use it

Use ANF or HyperANF to get the distance distribution, the [effective diameter](/effective-diameter/) or the average distance of a graph too large for one BFS per vertex, such as a web crawl or a social network with millions of vertices. The answer is approximate but the cost is a few scans of the edge list per round. For the exact diameter of a large graph, use methods based on a few BFS runs with bounds on eccentricities instead; ANF's estimates cannot certify the last value of $h$ at which $N$ grows.

## Pitfalls

- **Writing into the array being read.** If line L5 updates $M$ in place, a sketch can travel several steps in one round, and the ball sizes are too large for the given $h$. Keep the old array, as line L4 does; using the new values only speeds up the growth when the exact $h$ does not matter.
- **Small sets.** The Flajolet-Martin estimate of a set of size 1 is about $\sqrt{2}/\varphi \approx 1.83$ for large $r$. Use the exact $N(0) = n$, or a small-range correction, when small balls matter.
- **Too few copies.** With $r = 1$ every estimate is a power of 2 divided by $\varphi$. Use tens of copies, or HyperLogLog counters.
- **Correlated errors.** The same random positions are used for all vertices, so the errors of the terms of $\hat N(h)$ do not cancel. Do not expect the error of the sum to shrink with $n$.
- **Too narrow bitmasks.** The bitmask needs about $\log_2 n$ plus a few bits; a 32-bit mask is too short for graphs with billions of vertices.

## Implementations

## History

Flajolet and Martin introduced probabilistic counting with bitmasks in 1985. Cohen used random ranks in 1997 to estimate the sizes of all reachability sets of a graph. Palmer, Gibbons and Faloutsos built ANF in 2002 on the Flajolet-Martin sketches, to compute hop plots and effective diameters of graphs that do not fit in memory. Boldi, Rosa and Vigna replaced the bitmasks with HyperLogLog counters in HyperANF in 2011, and the method was later used to measure the degrees of separation of Facebook.

## References
