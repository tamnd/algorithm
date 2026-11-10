---
tag: R3VG3J
kind: algorithm
slug: jones-plassmann
name: Jones-Plassmann coloring
aliases:
- Jones-Plassmann algorithm
- parallel greedy coloring
area: parallel/parallel-graph-algorithms
level: advanced
summary: Parallel greedy colouring in which each vertex is coloured once all higher-priority neighbours are coloured.
solves: [graph-coloring]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the largest degree}
  time: {worst: O(n + m)}
  depth: {expected: O((d + log n) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [greedy-coloring, maximal-independent-set, union-bound, work-span-model]
see_also: [luby-mis, delta-plus-one-bound, distributed-vertex-coloring, graph-coloring, degeneracy-ordering, welsh-powell-algorithm, coloring-scc, cole-vishkin]
sources:
  - paper: doi:10.1137/0914041
    title: Mark T. Jones and Paul E. Plassmann, A parallel graph coloring heuristic, SIAM Journal on Scientific Computing 14(3), 1993
    locator: pp. 654 to 669 (the algorithm with random weights, and the expected O(log n / log log n) rounds for graphs of bounded degree)
  - paper: doi:10.1145/2612669.2612697
    title: William Hasenplaugh, Tim Kaler, Tao B. Schardl and Charles E. Leiserson, Ordering heuristics for parallel graph coloring, SPAA 2014
    locator: the analysis of the span of Jones-Plassmann for random orders, and the orderings largest-log-degree-first and smallest-log-degree-last
  - paper: doi:10.1137/0215074
    title: Michael Luby, A simple parallel algorithm for the maximal independent set problem, SIAM Journal on Computing 15(4), 1986
    locator: pp. 1036 to 1053 (the local-maximum rule with random values, on which the coloring is based)
---

Jones-Plassmann coloring is the [greedy coloring](/greedy-coloring/) of a graph in a random vertex order, computed in parallel. Every vertex gets a random priority once. A vertex takes its color, the least color not used by its neighbours of higher priority, as soon as all those neighbours have colors. The result is exactly the greedy coloring of the vertices in decreasing priority, so it uses at most $\Delta + 1$ colors, and the number of rounds is the number of vertices on the longest path of decreasing priority, which is $O(\Delta + \log n)$ with high probability.

Notation on this page: $G = (V, E)$ is an undirected graph with $n$ vertices, $m$ edges and largest degree $\Delta$ ($d$ in the front matter). $\rho(v)$ is the priority of $v$; the priorities are a uniformly random permutation, drawn once. $W$ is the work, $S$ the span and $T_p$ the time on $p$ processors. The model is the work-span model with an atomic fetch-and-add, which counts as $O(1)$ work. The work bound is worst case; the round bound holds with high probability (w.h.p.), that is, with probability at least $1 - n^{-c}$ for any fixed $c > 0$.

## In plain words

Every person draws a random ticket. People will pick a shirt color, and two rivals must not wear the same color.

A person waits until every rival with a higher ticket has picked. Then the person takes the first color in the list that none of those rivals wears. Rivals with lower tickets wait for this person, so they never clash with the choice.

Many people pick at once: everybody whose higher rivals are done picks in the same round. The colors come out the same as if people picked one by one in ticket order, so nobody needs more colors than the number of rivals plus one.

The number of rounds is the length of the longest chain of rivals with falling tickets, which random tickets keep short.

## The problem

The input is an undirected graph $G$ as adjacency lists. The output is a proper [coloring](/graph-coloring/) $c : V \to \{0, 1, 2, \ldots\}$, with $c(u) \ne c(v)$ for every edge $\{u, v\}$. The goal is few colors; the greedy order gives at most $\Delta + 1$, the bound of the [Δ + 1 argument](/delta-plus-one-bound/).

## The algorithm

$wait(v)$ counts the neighbours of $v$ with higher priority that have no color yet.

```pseudo id=main
JONES-PLASSMANN(V, E)
L1  ρ ← a uniformly random permutation of V, drawn once
L2  for all v in parallel do wait(v) ← the number of neighbours u with ρ(u) > ρ(v)
L3  ready ← the vertices with wait(v) = 0
L4  while ready is not empty do
L5      for all v in ready in parallel do
L6          c(v) ← the least color not used by a neighbour u with ρ(u) > ρ(v)
L7      for all v in ready, for all neighbours u of v with ρ(u) < ρ(v), in parallel do
L8          fetch-and-add wait(u) by −1, and if it reaches 0, put u in the next ready set
L9      ready ← the next ready set
L10 return c
```

Two adjacent vertices are never ready in one round: the one of lower priority waits for the other. So the vertices of a round form an independent set, and their colors do not interact. The first ready set is the set of local maxima of $\rho$, as in [Luby's algorithm](/luby-mis/).

## Example

The graph has the vertices 0 to 4 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{2,3\}$, $\{3,4\}$, $\{1,4\}$, so $\Delta = 3$. The priorities are $\rho = (3, 5, 1, 4, 2)$ for the vertices 0 to 4.

| round | ready | higher neighbours and their colors | colors given |
|---|---|---|---|
| 1 | 1, 3 | none for 1; none for 3 | $c(1) = 0$, $c(3) = 0$ |
| 2 | 0, 4 | 0: vertex 1 with 0; 4: vertices 1 and 3 with 0 | $c(0) = 1$, $c(4) = 1$ |
| 3 | 2 | vertices 0, 1, 3 with 1, 0, 0 | $c(2) = 2$ |

The coloring $(1, 0, 2, 0, 1)$ uses 3 colors, at most $\Delta + 1 = 4$. It is the greedy coloring in the order 1, 3, 0, 4, 2. The longest path of decreasing priority is $1, 0, 2$ with priorities $5, 3, 1$; it has 3 vertices, and the algorithm takes 3 rounds.

## Correctness

The proof file shows, by induction along the decreasing priority order, that each vertex gets the color that the sequential greedy algorithm gives it in that order: when $v$ is colored, exactly its neighbours of higher priority have colors, and they are the vertices that the greedy algorithm has colored before $v$ among its neighbours. A vertex has at most $\Delta$ such neighbours, so the least free color is at most $\Delta$, and the coloring is proper because each vertex avoids the colors of all neighbours colored before it, and the neighbours colored after it avoid its color.

## Complexity

**Rounds.** A vertex with no higher neighbour is colored in round 1, and any other vertex in the round after the last of its higher neighbours, so the number of rounds $R$ is the number of vertices on the longest path $v_1, \ldots, v_k$ with $\rho(v_1) > \cdots > \rho(v_k)$. The proof file proves, in full, that

$$\Pr[R \ge k] \le \frac{n \Delta^{k-1}}{k!},$$

since there are at most $n \Delta^{k-1}$ paths with $k$ vertices and each is decreasing with probability $1/k!$. It follows that $R \le \max(e^2 \Delta, (c + 1) \ln n)$ with probability at least $1 - n^{-c}$, and $E[R] \le e^2 \Delta + \ln n + 3$. For graphs of bounded degree, Jones and Plassmann (1993) show that the expected number of rounds is $O(\log n / \log \log n)$; this page cites that bound.

**Work and span.** Line L2 looks at each edge once. Each vertex is ready once; it scans its higher neighbours to pick its color and its lower neighbours to decrement their counts, so each edge is looked at $O(1)$ times in total. So

$$W = O(n + m),$$

in the worst case, the same as the sequential greedy algorithm. A round has $O(\log n)$ span for the color choice (a minimum over a bit mask of at most $\Delta + 1$ colors) and for collecting the next ready set, so $S = O(R \log n)$, which is $O((\Delta + \log n) \log n)$ w.h.p. By [Brent's theorem](/brent-theorem/), $T_p = O((n + m) / p + R \log n)$. In the tests, on random graphs with average degree 4, the mean number of rounds is 8.3 for $n = 64$, 10.6 for $n = 256$ and 11.6 for $n = 1{,}024$.

## Properties

- **Same colors as sequential greedy.** For a fixed priority order, the output does not depend on the schedule. A seeded order gives a reproducible coloring.
- **At most $\Delta + 1$ colors.** And at most one more than the largest number of higher neighbours of any vertex, which an ordering by degree can make small.
- **Work-efficient.** It does the same $O(n + m)$ work as the sequential greedy algorithm.
- **Rounds depend on the order.** A bad order, such as decreasing priority along a long path, takes $n$ rounds; the random order is what keeps the paths short.

## Variants and improvements

- **Other orders.** The algorithm works with any priority order and computes the greedy coloring of that order. Degree-based orders such as largest-first ([Welsh-Powell](/welsh-powell-algorithm/)) or smallest-last ([degeneracy order](/degeneracy-ordering/)) often use fewer colors but can make longer paths. Hasenplaugh, Kaler, Schardl and Leiserson (2014) propose largest-log-degree-first and smallest-log-degree-last, which group the vertices by the logarithm of their degree and order randomly inside each group, to get few colors with short paths.
- **Repeated independent sets.** An older scheme colors one [maximal independent set](/maximal-independent-set/) per color: find an MIS with [Luby's algorithm](/luby-mis/), give it the next color, remove it, and repeat. It can need many more rounds, since each color costs a whole MIS computation.
- **Speculative coloring.** Practical codes on shared memory often color all vertices at once, detect conflicts between neighbours, and recolor the conflicting ones. This does not reproduce a greedy order.
- **Distributed coloring.** In the LOCAL model, $(\Delta + 1)$-coloring has faster algorithms; see [distributed vertex coloring](/distributed-vertex-coloring/).

## When to use it

Use it when a coloring is needed in parallel to schedule conflicting tasks: rows of a sparse matrix for parallel Gauss-Seidel or incomplete factorization, finite elements that share nodes, or updates of a graph that touch neighbouring vertices. It gives the greedy quality with the greedy work, and the coloring is reproducible from the seed.

## Pitfalls

- **Ties in the priorities.** With equal priorities, two neighbours can both be ready and take the same color. Break ties by vertex name.
- **Choosing the color from all neighbours.** At the time $v$ is ready, its lower neighbours have no color yet, so looking at all neighbours gives the same result; but in a speculative implementation that reads colors written in the same round, it does not.
- **Rescanning every vertex in every round.** Testing all uncolored vertices in each round gives $O((n + m) R)$ work. The counts $wait(v)$ make the work $O(n + m)$.
- **Expecting few colors from a random order.** A random order gives at most $\Delta + 1$ colors but often more than a degree-based order. If colors matter more than rounds, use a better order.

## Implementations

## History

Jones and Plassmann (1993) proposed the algorithm for coloring the graphs of sparse matrices on distributed-memory machines, building on Luby's random local-maximum rule, and proved the $O(\log n / \log \log n)$ bound on the expected rounds for bounded degree. Hasenplaugh, Kaler, Schardl and Leiserson (2014) analysed it as a work-efficient multicore algorithm and introduced ordering heuristics for it.

## References
