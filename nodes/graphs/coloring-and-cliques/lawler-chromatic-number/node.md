---
tag: E447F2
kind: algorithm
slug: lawler-chromatic-number
name: Lawler's chromatic number algorithm
aliases:
- subset dynamic programming for coloring
area: graphs/coloring-and-cliques
level: advanced
summary: Exact chromatic number by dynamic programming over independent sets, running in about 2.4423^n time.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(2.4423^n)}
  space: {extra: Θ(2^n)}
properties: {deterministic: true, recursive: false}
prereqs: [chromatic-number, maximal-independent-set, bron-kerbosch, exact-exponential-algorithms]
see_also: [bjorklund-chromatic-number, k-coloring, maximal-clique-enumeration, maximal-independent-set-enumeration, welsh-powell-algorithm, sum-over-subsets]
sources:
  - paper: doi:10.1016/0020-0190(76)90065-X
    title: Eugene L. Lawler, A note on the complexity of the chromatic number problem, Information Processing Letters 5(3), 66 to 67 (1976)
    locator: the whole paper (the dynamic program over subsets with maximal independent sets, and 3-colorability in O(1.4423^n))
  - paper: doi:10.1007/BF02760024
    title: J. W. Moon and L. Moser, On cliques in graphs, Israel Journal of Mathematics 3(1), 23 to 28 (1965)
    locator: the bound 3^(n/3) on the number of maximal cliques, hence of maximal independent sets
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 3, Dynamic programming (graph coloring by dynamic programming over subsets) and Chapter 4, Inclusion-exclusion (the O*(2^n) algorithm)
  - paper: doi:10.7155/jgaa.00064
    title: David Eppstein, Small maximal independent sets and faster exact graph coloring, Journal of Graph Algorithms and Applications 7(2), 131 to 140 (2003)
    locator: the improvement to O(2.4150^n) by small maximal independent sets
  - paper: doi:10.1016/j.tcs.2006.06.015
    title: Etsuji Tomita, Akira Tanaka and Haruhisa Takahashi, The worst-case time complexity for generating all maximal cliques and computational experiments, Theoretical Computer Science 363(1), 28 to 42 (2006)
    locator: the pivot rule and the O(3^(n/3)) bound for listing maximal cliques
---

Lawler's algorithm computes the [chromatic number](/chromatic-number/) of a graph exactly by dynamic programming over all subsets of the vertices. For each subset $S$ it finds the least number of colors for the induced subgraph $G[S]$, by trying each [maximal independent set](/maximal-independent-set/) of $G[S]$ as one color class. The number of maximal independent sets is bounded by the Moon-Moser bound $3^{k/3}$, and summing over all subsets gives $O((1 + 3^{1/3})^n) = O(2.4423^n)$ time, with $\Theta(2^n)$ space. It was the fastest exact coloring algorithm for decades, until [Björklund, Husfeldt and Koivisto](/bjorklund-chromatic-number/) reached $O^*(2^n)$ by inclusion-exclusion.

## In plain words

To color a graph with as few colors as possible, pick one group of vertices that can all share a color, give them the first color, and color the rest with as few colors as possible. The best answer is the best choice of the first group.

Two ideas make this work. First, the first group can always be made as large as possible, so that no other vertex can join it; there are far fewer such groups than all groups. Second, the rest of the graph is always a set of vertices, so we can solve every set of vertices once, from small to large, and look the answers up in a table.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$. The output is $\chi(G)$, the least $k$ such that $G$ has a proper $k$-coloring, together with an optimal coloring. This is the optimization version of [graph coloring](/graph-coloring/), and it is NP-hard, so an exponential time is expected.

## The algorithm

Represent each subset of $V$ as a bitmask. For $S \subseteq V$, let $X[S] = \chi(G[S])$.

```pseudo id=main
LAWLER-CHROMATIC(G)
L1  X[∅] ← 0
L2  for each nonempty S ⊆ V, in increasing order of the bitmask do
L3      X[S] ← ∞
L4      for each maximal independent set I of G[S] do
L5          X[S] ← min(X[S], X[S \ I] + 1)
L6  return X[V]
```

Line L2 visits the subsets in increasing numeric order. Since $S \setminus I$ is a proper subset of $S$, its bitmask is smaller, so $X[S \setminus I]$ is already final when line L5 reads it. Line L4 lists the maximal independent sets of $G[S]$ with the [Bron-Kerbosch algorithm](/bron-kerbosch/) on the complement, with Tomita's pivot rule, in $O^*(3^{|S|/3})$ time. To output a coloring as well, store the set $I$ that gives the minimum at each $S$, and follow these choices down from $V$.

## Example

Take the 5-cycle $C_5$ with edges $01, 12, 23, 34, 40$.

| $\lvert S \rvert$ | subsets | $X[S]$ |
|---|---|---|
| 1 | 5 | 1 each |
| 2 | 10 | 1 for the 5 non-edges, 2 for the 5 edges |
| 3 | 10 | 2 each (a path or an edge plus a vertex) |
| 4 | 5 | 2 each (a path on 4 vertices) |
| 5 | 1 | 3 |

For $S = \{0, 1, 2\}$, the path $0\!-\!1\!-\!2$, the maximal independent sets are $\{1\}$ and $\{0, 2\}$. They give $X[\{0, 2\}] + 1 = 2$ and $X[\{1\}] + 1 = 2$, so $X[S] = 2$. For $S = V$, the maximal independent sets are $\{0, 2\}$, $\{0, 3\}$, $\{1, 3\}$, $\{1, 4\}$ and $\{2, 4\}$. Each leaves a path on 3 vertices with $X = 2$, so $X[V] = 3$. Over all 31 nonempty subsets, line L5 runs 60 times, against the bound $(1 + 3^{1/3})^5 \approx 86.9$.

## Correctness

**Claim.** For each $S \subseteq V$, the value $X[S]$ after its turn of line L2 equals $\chi(G[S])$.

The proof is by strong induction on $|S|$. Each value $X[S \setminus I] + 1$ is the cost of a real coloring: color $I$ with a new color and $S \setminus I$ optimally. So $X[S] \ge \chi(G[S])$. For the other direction, take an optimal coloring of $G[S]$ and one of its classes $C$. Extend $C$ greedily to a maximal independent set $I$ of $G[S]$. The other classes, minus the vertices of $I$, color $S \setminus I$ with $\chi(G[S]) - 1$ colors, so the term for $I$ is at most $\chi(G[S])$. The full proof is below.

## Complexity

**Time.** For a set $S$ of size $k$, $G[S]$ has at most $3^{k/3}$ maximal independent sets (Moon and Moser), and line L4 lists them in $O(3^{k/3} \cdot \mathrm{poly}(n))$ time. The sum over all subsets is

$$\sum_{k=0}^{n} \binom{n}{k} 3^{k/3} = (1 + 3^{1/3})^n \approx 2.44225^n$$

by the binomial theorem. With the polynomial factor, the time is $O^*(2.4423^n)$, and since $2.4423 > 2.44225$ the polynomial factor is absorbed: the time is $O(2.4423^n)$.

**Space.** The table $X$ has $2^n$ entries of $O(\log n)$ bits, so the space is $\Theta(2^n)$ words. The listing of line L4 needs only polynomial extra space.

**How sharp the analysis is.** The bound $3^{k/3}$ is reached by $k/3$ disjoint triangles, but the sum bounds each subset separately. For $G$ made of $n/3$ disjoint triangles, the subsets of one triangle have $1 + 3 + 6 + 3 = 13$ maximal independent sets in total, so line L5 runs $13^{n/3} - 1 \approx 2.3513^n$ times. Sharper bounds for the whole sum are what the improvements below exploit.

## Properties

- **Exact.** It returns $\chi(G)$ and an optimal coloring.
- **Exponential space.** The table of $2^n$ values limits it to about 30 to 35 vertices in practice.
- **3-colorability as a by-product.** The same idea decides 3-colorability faster: $G$ is 3-colorable if and only if some maximal independent set $I$ of $G$ leaves a bipartite graph $G - I$. This takes $O^*(3^{n/3}) = O(1.4423^n)$ time and polynomial space; see [k-coloring](/k-coloring/).

## Variants and improvements

- **Small maximal independent sets (Eppstein 2003).** Line L4 only needs to try maximal independent sets of bounded size, and bounds on the number of small maximal independent sets then give $O(2.4150^n)$. Byskov later reached $O(2.4023^n)$.
- **Inclusion-exclusion (Björklund, Husfeldt and Koivisto 2009).** Count the $k$-tuples of independent sets that cover $V$ with the [zeta transform](/sum-over-subsets/) of the independent set indicator. This gives $O^*(2^n)$ time; see [Björklund's algorithm](/bjorklund-chromatic-number/).
- **All independent sets instead of maximal ones.** The recurrence $X[S] = 1 + \min_{I} X[S \setminus I]$ over all nonempty independent $I \subseteq S$ is also correct, but its cost is $\sum_S 2^{|S|} = 3^n$.
- **Bounds first.** Start with an upper bound from [Welsh-Powell](/welsh-powell-algorithm/) or [DSatur](/dsatur/) and a lower bound from a clique; when they meet, the search can stop.

## When to use it

Use it for an exact chromatic number on graphs of up to about 30 vertices, or as a building block in other exact algorithms over subsets. For larger graphs, the $O^*(2^n)$ inclusion-exclusion algorithm is faster in the worst case, and branch-and-bound solvers with good bounds, such as DSatur-based exact search, usually win on sparse practical instances.

## Pitfalls

- **Wrong order of the subsets.** Line L2 must finish each proper subset before the set itself. Any order by the bitmask value or by size works; an order by some other key can read a value that is still $\infty$.
- **Using all independent sets.** Replacing "maximal independent set" in line L4 by "independent set" keeps the result correct but raises the time to $3^n$, which loses the point of the method.
- **Forgetting the empty set.** Line L1 sets $X[\emptyset] = 0$. Without it, the recursion has no base, and the case $V = \emptyset$ must return $0$, not $1$.
- **Listing without a pivot.** A Bron-Kerbosch listing without a pivot can spend time far above $3^{k/3}$ on some subsets, which breaks the time bound of line L4.

## Implementations

## History

Eugene Lawler published the algorithm in a two-page note in Information Processing Letters in 1976, together with the $O(1.4423^n)$ test for 3-colorability. Eppstein improved the base to 2.4150 in 2003, Byskov to 2.4023 in 2004, and Björklund, Husfeldt and Koivisto reached $O^*(2^n)$ in 2006 (journal version 2009).

## References
